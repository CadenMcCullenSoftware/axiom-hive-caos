"""The Ledger: an append-only, hash-chained record.

The implementation follows the platform architecture specification at
`operational/platform-architecture-and-agent-containment.md` §11, which
fixes the record structure, the canonicalisation, the digest computation, the
verification procedure, and the export format. The specification's worked
example is reproduced in the test suite as a test vector, so that a divergence
between the code and the document is a failing test rather than a discrepancy
found by inspection.

The chain is:

    digest(record) = SHA-256( ASCII(prev_hex) || canonical_bytes(body) )

where `prev_hex` is the 64 lower-case hexadecimal characters of the preceding
record's digest as ASCII bytes with no separator, and the canonical body is
the JSON object serialised as UTF-8 with keys ordered by Unicode code point,
no whitespace between tokens, and minimal string escaping. For the genesis
record `prev_hex` is 64 `0` characters.

What the chain provides is tamper evidence for the recorded sequence. What it
does not provide is protection against an attacker with write access to the
whole chain rewriting history consistently, and it is no proof that the
records were true when written. The mitigation is external anchoring and
periodic independent export, specified at §11.3 and §11.4.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

from .version import PLATFORM_BUILD

__all__ = [
    "GENESIS_DIGEST",
    "RECORD_SCHEMA",
    "EXPORT_FORMAT_VERSION",
    "LedgerRecord",
    "Ledger",
    "canonical_bytes",
    "canonical_json",
]


#: The `prev` value of the genesis record: 64 zero characters.
GENESIS_DIGEST = "0" * 64

#: The record schema identifier and version.
RECORD_SCHEMA = "caos.ledger.record/1"

#: The export format identifier and version.
EXPORT_FORMAT_VERSION = "caos.ledger.export/1"


#: The canonical JSON form is defined once, in `caos.canonical`, and the
#: Ledger's digest is computed over it. See that module for the rules.
from .canonical import canonical_bytes, canonical_json  # noqa: E402


@dataclass(frozen=True)
class LedgerRecord:
    """One record in the chain: the envelope of §11.1.

    The envelope carries `seq`, `prev`, `body`, and `digest`. The body carries
    `schema`, `ts`, `kind`, `subject`, `actor`, `card_ref`, `integrity`,
    `payload`, and the sequence number, which the worked example places in the
    canonical body and which therefore enters the hash.
    """

    seq: int
    prev: str
    body: Dict[str, Any]
    digest: str

    @property
    def kind(self) -> str:
        return str(self.body.get("kind", ""))

    @property
    def timestamp(self) -> datetime:
        return datetime.fromisoformat(str(self.body["ts"]).replace("Z", "+00:00"))

    @property
    def payload(self) -> Dict[str, Any]:
        value = self.body.get("payload")
        return value if isinstance(value, dict) else {}

    @property
    def card_id(self) -> Optional[str]:
        value = self.body.get("card_ref")
        return str(value) if value else None

    def compute_digest(self) -> str:
        """Recompute this record's digest from its own contents."""
        return hashlib.sha256(
            self.prev.encode("ascii") + canonical_bytes(self.body)
        ).hexdigest()

    def is_intact(self) -> bool:
        """Whether this record's digest still matches its contents."""
        return self.compute_digest() == self.digest

    def as_dict(self) -> Dict[str, Any]:
        """Return the record's envelope in the export form of §11.6."""
        return {
            "seq": self.seq,
            "prev": self.prev,
            "body": self.body,
            "digest": self.digest,
        }


class Ledger:
    """An append-only, hash-chained record.

    The Ledger is written on the critical path for dispatch. If it cannot be
    written, the dispatch does not happen; a decision that is not recorded is
    not a decision the framework recognises.
    """

    def __init__(self, records: Optional[Sequence[LedgerRecord]] = None) -> None:
        self._records: List[LedgerRecord] = list(records or [])
        self.anchor_kind: str = "external-witness"
        #: The head digest of the last anchor taken. A chain that has been
        #: rewritten no longer matches it, and the comparison is what makes
        #: the anchor a control rather than a note.
        self.anchor_head: str = ""
        self.manifest_head: str = ""

    # -- properties ------------------------------------------------------

    def __len__(self) -> int:
        return len(self._records)

    def __iter__(self):
        return iter(self._records)

    @property
    def records(self) -> List[LedgerRecord]:
        return list(self._records)

    @property
    def head(self) -> str:
        """The digest of the most recent record, or the genesis value."""
        if not self._records:
            return GENESIS_DIGEST
        return self._records[-1].digest

    # -- writing ---------------------------------------------------------

    def append(
        self,
        kind: str,
        payload: Dict[str, Any],
        *,
        subject: str = "platform",
        actor: str = "system",
        card_ref: Optional[str] = None,
        integrity: str = "trustworthy",
        timestamp: Optional[datetime] = None,
    ) -> LedgerRecord:
        """Append a record and return it.

        The record is chained to the previous one. A failure to write is a
        failure to dispatch, not a condition to be logged later.
        """
        moment = (timestamp or datetime.now(timezone.utc)).astimezone(timezone.utc)
        body: Dict[str, Any] = {
            "schema": RECORD_SCHEMA,
            "ts": moment.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "kind": kind,
            "subject": subject,
            "actor": actor,
            "card_ref": card_ref,
            "integrity": integrity,
            "payload": payload,
            "seq": len(self._records) + 1,
        }
        prev = self.head
        digest = hashlib.sha256(
            prev.encode("ascii") + canonical_bytes(body)
        ).hexdigest()
        record = LedgerRecord(
            seq=int(body["seq"]), prev=prev, body=body, digest=digest
        )
        self._records.append(record)
        return record

    # -- reading ---------------------------------------------------------

    def of_kind(self, kind: str) -> List[LedgerRecord]:
        """Return every record of a given kind."""
        return [r for r in self._records if r.kind == kind]

    def for_card(self, card_id: str) -> List[LedgerRecord]:
        """Return every record associated with a card."""
        return [r for r in self._records if r.card_id == card_id]

    def verify(self) -> Dict[str, Any]:
        """Verify the chain and return a verification report.

        The procedure is §11.5: check that the sequence is contiguous from 1,
        recompute each digest, check that each `prev` equals the preceding
        record's stored digest, check the genesis link, and compare the head
        against the anchors.

        The report states what was checked. It does not claim more than it
        establishes: an intact chain is evidence that the recorded sequence
        has not been altered since it was written, not evidence that what was
        recorded was correct.
        """
        problems: List[Dict[str, Any]] = []
        if self.anchor_head and self.anchor_head != self.head:
            problems.append(
                {
                    "position": "chain",
                    "problem": "the head does not match the anchor",
                    "expected": self.anchor_head,
                    "observed": self.head,
                }
            )
        previous = GENESIS_DIGEST
        for position, record in enumerate(self._records, start=1):
            if record.seq != position:
                problems.append(
                    {
                        "position": position,
                        "problem": "sequence discontinuity",
                        "expected": position,
                        "observed": record.seq,
                    }
                )
            if record.prev != previous:
                problems.append(
                    {
                        "position": position,
                        "problem": "chain link mismatch",
                        "expected": previous,
                        "observed": record.prev,
                    }
                )
            recomputed = record.compute_digest()
            if recomputed != record.digest:
                problems.append(
                    {
                        "position": position,
                        "problem": "digest mismatch",
                        "expected": recomputed,
                        "observed": record.digest,
                    }
                )
            previous = record.digest
        return {
            "records": len(self._records),
            "intact": not problems,
            "head": self.head,
            "problems": problems,
            "establishes": (
                "the recorded sequence has not been altered since it was written, "
                "and the point of the first divergence is identifiable"
                if not problems
                else "the chain does not verify; the recorded sequence may have been altered"
            ),
            "does_not_establish": (
                "that the recorded decisions were correct, that the authorisation "
                "was lawful, or that the chain cannot have been rewritten in full "
                "by an attacker with write access to the chain and to the anchor; "
                "external anchoring and periodic independent export are the "
                "stated mitigation"
            ),
        }

    # -- anchoring and export --------------------------------------------

    def anchor(self) -> Dict[str, Any]:
        """Return an anchorable summary of the chain head.

        The anchor is exported independently of the chain, so that a later
        full rewrite of the chain is detectable by comparison.
        """
        self.anchor_head = self.head
        return {
            "anchored_at": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z"),
            "anchor": self.anchor_kind,
            "head": self.head,
            "records": len(self._records),
            "chain_digest": hashlib.sha256(
                canonical_bytes([r.digest for r in self._records])
            ).hexdigest(),
        }

    def export(self) -> Dict[str, Any]:
        """Return the chain in the export form of §11.6.

        The export is a JSON document containing a manifest and the records in
        sequence, and is readable by a party with no access to the platform.

        The reference implementation does not sign its exports. The standard
        library offers no signing primitive that would be appropriate here
        without a cryptographic dependency, and an unsigned export that is
        labelled as unsigned is more useful to a verifier than one that
        appears signed and is not. The `signature` field is present and
        `null`, and the manifest states the fact.
        """
        return {
            "format_version": EXPORT_FORMAT_VERSION,
            "manifest": {
                "scope": "caos-platform",
                "range": {"from_seq": 1, "to_seq": len(self._records)},
                "genesis_digest": GENESIS_DIGEST,
                "head_digest": self.head,
                "anchors_consulted": [self.anchor_kind],
                "exported_at": datetime.now(timezone.utc)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z"),
                "platform_build": PLATFORM_BUILD,
                "complete": True,
                "signature": None,
                "signature_note": (
                    "this reference implementation does not sign exports; the "
                    "verification procedure is implementable from the export alone"
                ),
            },
            "records": [r.as_dict() for r in self._records],
        }

    def replay(self, card_id: str) -> List[Dict[str, Any]]:
        """Return the recorded sequence for a card, for reconstruction.

        The result is the timeline a reviewer needs: the world state as
        understood at each step, the choice, the authority, and the
        contingency that was pre-registered at the time.
        """
        timeline: List[Dict[str, Any]] = []
        for record in self.for_card(card_id):
            timeline.append(
                {
                    "seq": record.seq,
                    "timestamp": record.body.get("ts"),
                    "kind": record.kind,
                    "actor": record.body.get("actor"),
                    "subject": record.body.get("subject"),
                    "payload": record.payload,
                    "digest": record.digest,
                }
            )
        return timeline

    @classmethod
    def from_export(cls, exported: Dict[str, Any]) -> "Ledger":
        """Rebuild a Ledger from an exported chain, for independent verification.

        A document that is not an export is refused with a statement of what
        is wrong, rather than raising a raw attribute or type error. The
        caller is an auditor, and an auditor needs to be told what is wrong
        with the file.
        """
        if not isinstance(exported, dict):
            raise ValueError(
                "an export is a JSON object; this document is a "
                f"{type(exported).__name__}"
            )
        manifest = exported.get("manifest")
        if not isinstance(manifest, dict):
            raise ValueError("the export has no manifest")
        records_raw = exported.get("records")
        if not isinstance(records_raw, list):
            raise ValueError("the export has no records array")
        format_version = exported.get("format_version")
        if format_version != EXPORT_FORMAT_VERSION:
            raise ValueError(
                f"the export's format is {format_version!r}; this implementation "
                f"reads {EXPORT_FORMAT_VERSION!r}"
            )
        records: List[LedgerRecord] = []
        for position, raw in enumerate(records_raw, start=1):
            if not isinstance(raw, dict):
                raise ValueError(f"record {position} is not an object")
            for field in ("seq", "prev", "body", "digest"):
                if field not in raw:
                    raise ValueError(f"record {position} has no {field!r}")
            if not isinstance(raw["seq"], int):
                raise ValueError(f"record {position} has a non-integer sequence")
            if not isinstance(raw["body"], dict):
                raise ValueError(f"record {position} has a non-object body")
            records.append(
                LedgerRecord(
                    seq=raw["seq"],
                    prev=str(raw["prev"]),
                    body=dict(raw["body"]),
                    digest=str(raw["digest"]),
                )
            )
        ledger = cls(records)
        if manifest.get("anchor"):
            ledger.anchor_kind = str(manifest["anchor"])
        ledger.anchor_head = str(manifest.get("head_digest") or "")
        ledger.manifest_head = str(manifest.get("head_digest") or "")
        return ledger
