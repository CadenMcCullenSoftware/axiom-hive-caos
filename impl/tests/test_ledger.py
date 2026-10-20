"""Tests for the Ledger.

The Ledger is the substrate of auditability, and its specification is
precise: `operational/platform-architecture-and-agent-containment.md` §11
fixes the record structure, the canonicalisation, and the digest
computation, and publishes a worked example with two stated digests.

That worked example is used here as a test vector. A divergence between this
implementation and the specification is therefore a failing test rather than a
discrepancy that has to be found by inspection.
"""

from __future__ import annotations

import unittest
from dataclasses import replace

from caos.ledger import (
    EXPORT_FORMAT_VERSION,
    GENESIS_DIGEST,
    Ledger,
    LedgerRecord,
    canonical_bytes,
    canonical_json,
)
from caos.models import DecisionRecord, utc_now


# -- the specification's worked example, transcribed ------------------------

EXAMPLE_GENESIS_BODY = {
    "actor": "system",
    "card_ref": None,
    "integrity": "trustworthy",
    "kind": "ledger.genesis",
    "payload": {
        "anchor": "external-witness",
        "platform_build": "0.1.0",
        "scope": "caos-platform",
    },
    "schema": "caos.ledger.record/1",
    "seq": 1,
    "subject": "platform",
    "ts": "2026-02-11T09:00:00Z",
}

EXAMPLE_GENESIS_DIGEST = (
    "88a8e9ed2bc4844e982322db028c8fd9b76ea034e43cf20c80a1b8dccda994cf"
)

EXAMPLE_SECOND_BODY = {
    "actor": "role:analyst",
    "card_ref": "CARD-EXAMPLE-001",
    "integrity": "trustworthy",
    "kind": "policy.decision",
    "payload": {
        "conditions_evaluated": [
            "AD-1", "AD-2", "AD-3", "AD-4", "AD-5", "AD-6",
            "AD-7", "AD-8", "AD-9", "AD-10", "AD-11", "AD-12",
        ],
        "engine_version": "0.1.0",
        "evaluation_phase": "pre-selection",
        "margin": {
            "condition": "AD-9",
            "delta": -0.08,
            "observed": 0.62,
            "required": 0.7,
        },
        "outcome": "refuse",
        "policy_set_version": "0.1.0",
    },
    "schema": "caos.ledger.record/1",
    "seq": 2,
    "subject": "countermeasure:illustrative",
    "ts": "2026-02-11T09:14:22Z",
}

EXAMPLE_SECOND_DIGEST = (
    "cd205aed6d1cf506074798631e4134150a2f05541ebaa8fb85992b8e8a90bcf6"
)

#: The digest the specification states for the tampered second record.
EXAMPLE_TAMPERED_DIGEST = (
    "6dd570fcd02604da3ce35a7e57c4c11392e6890179cb87135ff6ca2966fffd57"
)


class WorkedExampleTests(unittest.TestCase):
    """The specification's worked example, reproduced as a test vector."""

    def test_the_genesis_digest_reproduces(self) -> None:
        import hashlib

        digest = hashlib.sha256(
            GENESIS_DIGEST.encode("ascii") + canonical_bytes(EXAMPLE_GENESIS_BODY)
        ).hexdigest()
        self.assertEqual(digest, EXAMPLE_GENESIS_DIGEST)

    def test_the_second_digest_reproduces(self) -> None:
        import hashlib

        digest = hashlib.sha256(
            EXAMPLE_GENESIS_DIGEST.encode("ascii") + canonical_bytes(EXAMPLE_SECOND_BODY)
        ).hexdigest()
        self.assertEqual(digest, EXAMPLE_SECOND_DIGEST)

    def test_the_canonical_form_matches_the_specification_byte_for_byte(self) -> None:
        self.assertEqual(
            canonical_json(EXAMPLE_SECOND_BODY),
            (
                '{"actor":"role:analyst","card_ref":"CARD-EXAMPLE-001",'
                '"integrity":"trustworthy","kind":"policy.decision","payload":'
                '{"conditions_evaluated":["AD-1","AD-2","AD-3","AD-4","AD-5",'
                '"AD-6","AD-7","AD-8","AD-9","AD-10","AD-11","AD-12"],'
                '"engine_version":"0.1.0","evaluation_phase":"pre-selection",'
                '"margin":{"condition":"AD-9","delta":-0.08,"observed":0.62,'
                '"required":0.7},"outcome":"refuse","policy_set_version":"0.1.0"},'
                '"schema":"caos.ledger.record/1","seq":2,'
                '"subject":"countermeasure:illustrative",'
                '"ts":"2026-02-11T09:14:22Z"}'
            ),
        )

    def test_the_tampered_digest_reproduces(self) -> None:
        import hashlib

        body = dict(EXAMPLE_SECOND_BODY)
        payload = dict(body["payload"])
        payload["outcome"] = "permit"
        body["payload"] = payload
        digest = hashlib.sha256(
            EXAMPLE_GENESIS_DIGEST.encode("ascii") + canonical_bytes(body)
        ).hexdigest()
        self.assertEqual(digest, EXAMPLE_TAMPERED_DIGEST)

    def test_the_example_chain_verifies(self) -> None:
        ledger = Ledger(
            [
                LedgerRecord(1, GENESIS_DIGEST, EXAMPLE_GENESIS_BODY, EXAMPLE_GENESIS_DIGEST),
                LedgerRecord(
                    2,
                    EXAMPLE_GENESIS_DIGEST,
                    EXAMPLE_SECOND_BODY,
                    EXAMPLE_SECOND_DIGEST,
                ),
            ]
        )
        report = ledger.verify()
        self.assertTrue(report["intact"], report["problems"])


class CanonicalisationTests(unittest.TestCase):
    def test_keys_are_ordered_recursively(self) -> None:
        self.assertEqual(
            canonical_json({"b": 1, "a": {"d": 2, "c": 3}}),
            '{"a":{"c":3,"d":2},"b":1}',
        )

    def test_no_whitespace_is_emitted(self) -> None:
        self.assertNotIn(" ", canonical_json({"a": 1, "b": [1, 2]}))

    def test_nulls_are_present_not_omitted(self) -> None:
        self.assertEqual(canonical_json({"a": None}), '{"a":null}')

    def test_non_ascii_is_emitted_literally(self) -> None:
        self.assertEqual(canonical_json({"a": "é"}), '{"a":"é"}')

    def test_a_non_serialisable_value_is_rejected(self) -> None:
        with self.assertRaises(TypeError):
            canonical_json({"a": object()})


class LedgerChainTests(unittest.TestCase):
    def test_a_new_ledger_is_empty_with_a_genesis_head(self) -> None:
        ledger = Ledger()
        self.assertEqual(len(ledger), 0)
        self.assertEqual(ledger.head, GENESIS_DIGEST)

    def test_sequence_numbers_start_at_one(self) -> None:
        ledger = Ledger()
        record = ledger.append("signal.ingested", {"summary": "something happened"})
        self.assertEqual(record.seq, 1)
        self.assertEqual(record.prev, GENESIS_DIGEST)

    def test_records_are_chained(self) -> None:
        ledger = Ledger()
        first = ledger.append("signal.ingested", {"n": 1})
        second = ledger.append("signal.ingested", {"n": 2})
        self.assertEqual(second.prev, first.digest)
        self.assertNotEqual(first.digest, second.digest)

    def test_the_body_carries_the_specified_fields(self) -> None:
        ledger = Ledger()
        record = ledger.append(
            "policy.decision",
            {"outcome": "refuse"},
            subject="countermeasure:illustrative",
            actor="role:analyst",
            card_ref="CARD-1",
        )
        for field in (
            "schema", "ts", "kind", "subject", "actor",
            "card_ref", "integrity", "payload", "seq",
        ):
            self.assertIn(field, record.body)

    def test_chain_verifies(self) -> None:
        ledger = Ledger()
        for index in range(5):
            ledger.append("signal.ingested", {"index": index})
        report = ledger.verify()
        self.assertTrue(report["intact"])
        self.assertEqual(report["problems"], [])
        self.assertEqual(report["records"], 5)

    def test_tampering_with_a_payload_is_detected(self) -> None:
        ledger = Ledger()
        ledger.append("signal.ingested", {"summary": "original"})
        ledger.append("signal.ingested", {"summary": "second"})
        records = list(ledger.records)
        body = dict(records[0].body)
        body["payload"] = {"summary": "amended"}
        records[0] = replace(records[0], body=body)
        report = Ledger(records).verify()
        self.assertFalse(report["intact"])
        self.assertTrue(report["problems"])
        self.assertEqual(report["problems"][0]["position"], 1)

    def test_tampering_with_a_digest_is_detected(self) -> None:
        ledger = Ledger()
        ledger.append("signal.ingested", {"summary": "original"})
        records = list(ledger.records)
        records[0] = replace(records[0], digest="0" * 64)
        self.assertFalse(Ledger(records).verify()["intact"])

    def test_reordering_records_is_detected(self) -> None:
        ledger = Ledger()
        ledger.append("signal.ingested", {"n": 1})
        ledger.append("signal.ingested", {"n": 2})
        records = list(ledger.records)[::-1]
        self.assertFalse(Ledger(records).verify()["intact"])

    def test_a_truncated_chain_closes_only_against_a_different_head(self) -> None:
        ledger = Ledger()
        ledger.append("signal.ingested", {"n": 1})
        ledger.append("signal.ingested", {"n": 2})
        ledger.append("signal.ingested", {"n": 3})
        truncated = Ledger(list(ledger.records)[:2])
        self.assertTrue(truncated.verify()["intact"])
        # The truncated chain verifies internally, but its head no longer
        # matches the anchored head, which is what the anchor catches.
        self.assertNotEqual(truncated.head, ledger.head)

    def test_verification_states_what_it_does_not_establish(self) -> None:
        ledger = Ledger()
        ledger.append("signal.ingested", {"n": 1})
        report = ledger.verify()
        self.assertIn("does_not_establish", report)
        self.assertIn("correct", report["does_not_establish"])
        self.assertIn("rewritten", report["does_not_establish"])


class ExportTests(unittest.TestCase):
    def test_the_export_carries_a_manifest_and_the_records(self) -> None:
        ledger = Ledger()
        ledger.append("signal.ingested", {"n": 1})
        exported = ledger.export()
        self.assertEqual(exported["format_version"], EXPORT_FORMAT_VERSION)
        self.assertIn("manifest", exported)
        self.assertEqual(len(exported["records"]), 1)
        self.assertEqual(exported["manifest"]["head_digest"], ledger.head)

    def test_the_export_states_that_it_is_unsigned(self) -> None:
        ledger = Ledger()
        exported = ledger.export()
        self.assertIsNone(exported["manifest"]["signature"])
        self.assertIn("does not sign", exported["manifest"]["signature_note"])

    def test_export_and_reimport_preserves_the_chain(self) -> None:
        ledger = Ledger()
        for index in range(4):
            ledger.append("signal.ingested", {"index": index})
        restored = Ledger.from_export(ledger.export())
        self.assertEqual(restored.head, ledger.head)
        self.assertTrue(restored.verify()["intact"])

    def test_anchor_reports_the_chain_digest(self) -> None:
        ledger = Ledger()
        ledger.append("signal.ingested", {"n": 1})
        anchor = ledger.anchor()
        self.assertEqual(anchor["head"], ledger.head)
        self.assertEqual(anchor["records"], 1)
        self.assertEqual(len(anchor["chain_digest"]), 64)


class QueryTests(unittest.TestCase):
    def test_for_card_filters_by_card(self) -> None:
        ledger = Ledger()
        ledger.append("policy.decision", {}, card_ref="OC-1")
        ledger.append("policy.decision", {}, card_ref="OC-2")
        ledger.append("policy.decision", {}, card_ref="OC-1")
        self.assertEqual(len(ledger.for_card("OC-1")), 2)
        self.assertEqual(len(ledger.for_card("OC-2")), 1)

    def test_of_kind_filters_by_kind(self) -> None:
        ledger = Ledger()
        ledger.append("signal.ingested", {})
        ledger.append("execution.aborted", {})
        self.assertEqual(len(ledger.of_kind("execution.aborted")), 1)

    def test_replay_returns_a_timeline(self) -> None:
        ledger = Ledger()
        record = DecisionRecord(
            record_id="DR-1",
            card_id="OC-1",
            timestamp=utc_now(),
            decision_point="countermeasure selection",
            known_at_the_time=("threat score 3.00",),
            options_considered=("OCC-01", "OCC-24"),
            grounds_for_rejection="AD-2 exceeded the ceiling",
            choice="OCC-01",
            authority_relied_on="EA-TEST",
            confidence_at_the_time=0.6,
            residual_risk=1.2,
            risk_of_inaction="the service may degrade",
            pre_registered_contingency="abort on degradation",
        )
        ledger.append("policy.decision", record.as_payload(), card_ref="OC-1")
        timeline = ledger.replay("OC-1")
        self.assertEqual(len(timeline), 1)
        self.assertEqual(timeline[0]["kind"], "policy.decision")
        self.assertIn("OCC-24", timeline[0]["payload"]["options_considered"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
