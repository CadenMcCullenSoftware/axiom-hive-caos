"""Regenerate the implementation's countermeasure data from the canonical document.

The countermeasure catalogue in `operational/countermeasure-catalogue.md` is
authoritative. This tool parses it and writes `caos/catalogue_data.py`, so
that the executable catalogue and the written catalogue cannot drift apart
without that drift being visible in a diff.

Usage:

    python3 tools/sync_catalogue.py            # write the data module
    python3 tools/sync_catalogue.py --check    # report drift, write nothing

The parser is deliberately strict. A value it does not recognise is an error,
not a default, because a silently defaulted countermeasure attribute is
exactly the kind of divergence this tool exists to prevent.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT = ROOT.parent / "operational" / "countermeasure-catalogue.md"
TARGET = ROOT / "caos" / "catalogue_data.py"

CLASS_MAP = {
    "CM-A Detect": "CM_A",
    "CM-B Harden": "CM_B",
    "CM-C Contain": "CM_C",
    "CM-D Observe": "CM_D",
    "CM-E Deceive": "CM_E",
    "CM-F Disrupt": "CM_F",
    "CM-G Recover": "CM_G",
}

DIRECTION_MAP = {
    "Inward": "OWN_ESTATE",
    "Outward": "ADVERSARY_SYSTEM",
    "Inward/outward": "ADVERSARY_BEHAVIOUR",
    "None": "NONE",
}

TARGET_MAP = {
    "Own estate": "own estate",
    "Adversary behaviour in own environment": "adversary behaviour in own environment",
    "Adversary system": "adversary system",
    "Adversary infrastructure": "adversary infrastructure",
}

REVERSIBILITY_MAP = {
    "Reversible": "REVERSIBLE",
    "Reversed": "REVERSED",
    "Low": "LOW",
    "None": "NONE",
}

AUTONOMY_MAP = {
    "AC-0 (Manual)": "AC0_MANUAL",
    "AC-1 (Assisted)": "AC1_ASSISTED",
    "AC-2 (Supervised)": "AC2_SUPERVISED",
    "AC-3 (Delegated)": "AC3_DELEGATED",
    "AC-4 (Autonomous, read-only)": "AC4_AUTONOMOUS",
}

PROFILE_MAP = {
    "R0 Observe": "R0_OBSERVE",
    "R1 Shield": "R1_SHIELD",
    "R2 Trap": "R2_TRAP",
    "R3 Deceive": "R3_DECEIVE",
    "R4 Disrupt": "R4_DISRUPT",
    "R5 Neutralise": "R5_NEUTRALISE",
}

ATTRIBUTION_MAP = {
    "None": "NONE",
    "Behavioural": "BEHAVIOURAL",
    "Class": "CLASS",
    "Identity": "IDENTITY",
    "External": "EXTERNAL",
}

STATUS_MAP = {
    "Active": "ACTIVE",
    "Conditional": "CONDITIONAL",
    "Retired": "RETIRED",
    "Withheld": "WITHHELD",
}

#: Confidence bands map to a nominal midpoint, because the catalogue states
#: the band and the basis, not a point value. The point value is an estimate
#: of the band's midpoint and is labelled as such in the generated module.
CONFIDENCE_MAP = {
    "Very low": 0.20,
    "Low": 0.40,
    "Moderate": 0.60,
    "High": 0.80,
}

FIELD_ORDER = [
    "Class",
    "Summary",
    "Direction of effect",
    "Target",
    "Collateral class",
    "Reversibility",
    "Autonomy class",
    "Minimum ROE profile",
    "Attribution dependency",
    "AAT technique bindings",
    "Preconditions",
    "Procedure summary",
    "Failure modes",
    "Side effects",
    "Detection objective satisfied",
    "Intelligence yield",
    "Operator burden",
    "Degradation behaviour",
    "Evidence produced",
    "Residual risk reduction",
    "Status",
]


class ParseError(Exception):
    """Raised when the document cannot be parsed unambiguously."""


def split_entries(text: str) -> List[Tuple[str, str]]:
    """Split the document into (identifier, body) pairs, one per entry."""
    pattern = re.compile(r"^#### (OCC-\d\d) — (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    entries: List[Tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end]
        # Bound each entry at the next heading of any level so that the
        # combination rules in a later section are not absorbed into the last
        # entry.
        boundary = re.search(r"^#{2,4} ", body, re.MULTILINE)
        if boundary:
            body = body[: boundary.start()]
        entries.append((match.group(1), body))
    return entries


def parse_fields(body: str) -> Dict[str, str]:
    """Extract the metadata table from one entry body."""
    fields: Dict[str, str] = {}
    for line in body.splitlines():
        match = re.match(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$", line)
        if not match:
            continue
        key, value = match.group(1), match.group(2)
        if key in FIELD_ORDER and key not in fields:
            fields[key] = value
    return fields


def parse_residual(value: str) -> Tuple[float, float]:
    """Return (midpoint, confidence) from the residual-risk reduction field."""
    match = re.match(
        r"([0-9.]+)\s*[–-]\s*([0-9.]+)\s*;\s*basis\s*(\S+)\s*"
        r"\(([^)]*)\)\s*;\s*confidence\s*([^.]+)\.",
        value,
    )
    if not match:
        raise ParseError(f"unparsable residual-risk reduction: {value!r}")
    low, high = float(match.group(1)), float(match.group(2))
    confidence_text = match.group(5).strip()
    if confidence_text not in CONFIDENCE_MAP:
        raise ParseError(f"unknown confidence band: {confidence_text!r}")
    return (low + high) / 2.0, CONFIDENCE_MAP[confidence_text]


def require(fields: Dict[str, str], key: str, identifier: str) -> str:
    if key not in fields:
        raise ParseError(f"{identifier}: missing field {key!r}")
    return fields[key]


def build(entries: List[Tuple[str, str]]) -> List[Dict[str, object]]:
    records: List[Dict[str, object]] = []
    for identifier, body in entries:
        fields = parse_fields(body)
        for key in FIELD_ORDER:
            require(fields, key, identifier)
        residual, confidence = parse_residual(fields["Residual risk reduction"])
        bindings = [
            b.strip() for b in fields["AAT technique bindings"].split(",") if b.strip()
        ]
        for binding in bindings:
            if not re.fullmatch(r"AAT-\d{1,2}", binding):
                raise ParseError(f"{identifier}: malformed AAT binding {binding!r}")
        record = {
            "identifier": identifier,
            "name": None,  # filled from the heading
            "cm_class": CLASS_MAP[require(fields, "Class", identifier)],
            "summary": fields["Summary"],
            "direction": DIRECTION_MAP[require(fields, "Direction of effect", identifier)],
            "target_scope": TARGET_MAP[require(fields, "Target", identifier)],
            "collateral": fields["Collateral class"],
            "reversibility": REVERSIBILITY_MAP[require(fields, "Reversibility", identifier)],
            "autonomy": AUTONOMY_MAP[require(fields, "Autonomy class", identifier)],
            "min_profile": PROFILE_MAP[require(fields, "Minimum ROE profile", identifier)],
            "attribution_dependency": ATTRIBUTION_MAP[
                require(fields, "Attribution dependency", identifier)
            ],
            "techniques": tuple(bindings),
            "preconditions": fields["Preconditions"],
            "procedure": fields["Procedure summary"],
            "failure_modes": fields["Failure modes"],
            "side_effects": fields["Side effects"],
            "detection_objective": fields["Detection objective satisfied"],
            "intelligence_yield": fields["Intelligence yield"],
            "operator_burden": fields["Operator burden"],
            "degradation": fields["Degradation behaviour"],
            "evidence": fields["Evidence produced"],
            "residual_reduction": residual,
            "effectiveness_confidence": confidence,
            "status": STATUS_MAP[require(fields, "Status", identifier)],
        }
        records.append(record)
    return records


def render(records: List[Dict[str, object]], version: str) -> str:
    lines = [
        '"""Countermeasure catalogue data, generated from the canonical document.',
        "",
        "DO NOT EDIT THIS FILE BY HAND. It is written by",
        "`tools/sync_catalogue.py` from `operational/countermeasure-catalogue.md`,",
        "which is authoritative. Run the tool after any change to the document.",
        "",
        "The residual-risk reduction figures are the midpoints of the bands stated",
        "in the document, at the design-intent evidence basis the document records.",
        "They are estimates, not measurements, and no figure in the catalogue has",
        "been calibrated against outcome data.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "CATALOGUE_VERSION = " + repr(version),
        "CATALOGUE_REDUCED: tuple[dict, ...] = (",
    ]
    for record in records:
        lines.append("    {")
        for key, value in record.items():
            lines.append(f"        {key!r}: {value!r},")
        lines.append("    },")
    lines.append(")")
    lines.append("")
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report drift against the existing data module and write nothing",
    )
    args = parser.parse_args(argv)

    if not DOCUMENT.exists():
        print(f"error: canonical document not found at {DOCUMENT}", file=sys.stderr)
        return 2
    text = DOCUMENT.read_text(encoding="utf-8")
    try:
        entries = split_entries(text)
    except ParseError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if len(entries) != 43:
        print(
            f"error: expected 43 entries, found {len(entries)}", file=sys.stderr
        )
        return 2
    try:
        records = build(entries)
        for record in records:
            record["name"] = _name_for(text, str(record["identifier"]))
    except ParseError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    # A duplicate identifier is not caught by the entry count, and the
    # catalogue index would silently shadow one of the two.
    identifiers = [str(r["identifier"]) for r in records]
    duplicates = sorted({i for i in identifiers if identifiers.count(i) > 1})
    if duplicates:
        print(
            "error: duplicate countermeasure identifiers in the document: "
            + ", ".join(duplicates),
            file=sys.stderr,
        )
        return 2

    # The series is permanent and never renumbered, so a gap in it is a
    # defect rather than a vacancy.
    expected = [f"OCC-{i:02d}" for i in range(1, len(records) + 1)]
    if identifiers != expected:
        missing = sorted(set(expected) - set(identifiers))
        unexpected = sorted(set(identifiers) - set(expected))
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if unexpected:
            detail.append("unexpected " + ", ".join(unexpected))
        print(
            "error: the countermeasure series is not contiguous: " + "; ".join(detail),
            file=sys.stderr,
        )
        return 2

    version_match = re.search(r"^\| Version \| (.+?) \|$", text, re.MULTILINE)
    version = version_match.group(1) if version_match else "1.0"
    rendered = render(records, version)

    if args.check:
        if not TARGET.exists():
            print("drift: the data module does not exist")
            return 1
        if TARGET.read_text(encoding="utf-8") != rendered:
            print("drift: the data module does not match the canonical document")
            return 1
        print("in sync")
        return 0

    TARGET.write_text(rendered, encoding="utf-8")
    print(f"wrote {TARGET} ({len(records)} entries, version {version})")
    return 0


def _name_for(text: str, identifier: str) -> str:
    match = re.search(
        rf"^#### {re.escape(identifier)} — (.+)$", text, re.MULTILINE
    )
    if not match:
        raise ParseError(f"{identifier}: heading not found")
    return match.group(1).strip()


if __name__ == "__main__":
    sys.exit(main())
