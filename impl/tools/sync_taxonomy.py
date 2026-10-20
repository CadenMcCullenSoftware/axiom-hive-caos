"""Regenerate the implementation's technique registry from the canonical document.

`operational/adversary-ai-taxonomy-and-threat-model.md` §5 is the canonical
source for the adversary-AI technique list: the identifier, the name, the
definition, the observable artefact, and the category. This tool parses it and
writes `caos/taxonomy_data.py`, so that the executable registry and the
written taxonomy cannot drift apart without that drift being visible in a
diff.

`reference/ai-attack-technique-library.md` is the canonical source for the
per-technique indicators, detection methods, countermeasure bindings, and
external-mapping verification status. Where the two documents disagree about
the identity or the behaviour of a technique, the taxonomy document prevails
and the library is to be re-keyed.

Usage:

    python3 tools/sync_taxonomy.py            # write the data module
    python3 tools/sync_taxonomy.py --check    # report drift, write nothing

The parser is deliberately strict. A technique row it cannot parse is an
error, not a skipped row, because a technique that silently fails to import
is a technique the implementation cannot detect or counter.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT = ROOT.parent / "operational" / "adversary-ai-taxonomy-and-threat-model.md"
LIBRARY = ROOT.parent / "reference" / "ai-attack-technique-library.md"
TARGET = ROOT / "caos" / "taxonomy_data.py"

HEADER = "| ID | Name | Description | Observable artefact in telemetry | Most often combines with | Countermeasure binding |"

#: The columns the generator reads, in order.
_COLUMNS = 6


class ParseError(Exception):
    """Raised when the document cannot be parsed unambiguously."""


def technique_section(text: str) -> str:
    """Return the document's technique section.

    The technique tables live in the section that defines them, and the
    reconciliation register later in the document also carries rows beginning
    with a technique identifier. Only the defining section is parsed, so that
    a row elsewhere in the document is not mistaken for a technique that has
    gone missing.
    """
    start = re.search(r"^##\s+5\.", text, re.MULTILINE)
    if not start:
        return text
    end = re.search(r"^##\s+6\.", text[start.end():], re.MULTILINE)
    if not end:
        return text[start.start():]
    return text[start.start(): start.end() + end.start()]


def extract_rows(text: str) -> List[Dict[str, str]]:
    """Extract every technique row from the taxonomy document."""
    rows: List[Dict[str, str]] = []
    lines = technique_section(text).splitlines()
    for index, line in enumerate(lines):
        strict = re.match(r"^\| \*\*AAT-\d{1,2}\.\d{1,2}\*\* \|", line)
        if not strict:
            # A row that looks like a technique row but does not match the
            # strict form is a row the parser cannot read. Dropping it
            # silently would remove the technique from the registry, and
            # everything bound to it, with no indication that it had
            # happened.
            loose = re.match(r"^\|\s*\**AAT-\d{1,2}\.\d{1,2}", line)
            if loose:
                raise ParseError(
                    f"line {index + 1}: the technique row cannot be read; the "
                    "identifier must be written as | **AAT-n.m** |"
                )
            continue
        if index + 1 < len(lines) and lines[index + 1].startswith("| ---"):
            # This is the header row of the technique table; the header text
            # itself does not begin with a bolded identifier, so a row that
            # does is a data row.
            pass
        cells = _split_row(line)
        if len(cells) != _COLUMNS:
            raise ParseError(
                f"line {index + 1}: expected {_COLUMNS} columns, found {len(cells)}: "
                f"{line[:90]}"
            )
        identifier = cells[0].strip().strip("*")
        if not re.fullmatch(r"AAT-\d{1,2}\.\d{1,2}", identifier):
            raise ParseError(f"line {index + 1}: malformed technique identifier {identifier!r}")
        bindings = tuple(
            sorted({b for b in re.findall(r"OCC-\d{2}", cells[5])})
        )
        rows.append(
            {
                "identifier": identifier,
                "name": cells[1].strip(),
                "description": cells[2].strip(),
                "artefacts": cells[3].strip(),
                "combines_with": cells[4].strip(),
                "countermeasure_bindings": bindings,
            }
        )
    return rows


def _split_row(line: str) -> List[str]:
    """Split a markdown table row into its cells."""
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [cell.strip() for cell in inner.split("|")]


def extract_library_objectives(text: str) -> Dict[str, str]:
    """Extract the per-technique detection objectives from the technique library.

    The library is canonical for the detection objectives; the taxonomy
    document is canonical for the identity and the behaviour of a technique.
    The library's detail tables carry nine columns, of which the fifth is the
    detection objectives.
    """
    objectives: Dict[str, str] = {}
    for line in text.splitlines():
        if not re.match(r"^\| AAT-\d{1,2}\.\d{1,2} \|", line):
            continue
        cells = _split_row(line)
        if len(cells) != 9:
            continue
        objectives.setdefault(cells[0].strip(), cells[4].strip())
    return objectives


def render(rows: List[Dict[str, object]]) -> str:
    lines = [
        '"""Adversary-AI technique registry, generated from the canonical document.',
        "",
        "DO NOT EDIT THIS FILE BY HAND. It is written by",
        "`tools/sync_taxonomy.py` from",
        "`operational/adversary-ai-taxonomy-and-threat-model.md`, which is",
        "authoritative for the identity and the behaviour of every technique.",
        "Run the tool after any change to the document.",
        "",
        "The countermeasure bindings carried here are the document's indicative",
        "category-level set. The technique-level bindings are held by",
        "`reference/ai-attack-technique-library.md`.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "TECHNIQUES_DATA: tuple[dict, ...] = (",
    ]
    for row in rows:
        lines.append("    {")
        for key, value in row.items():
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
        rows = extract_rows(text)
    except ParseError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    identifiers = [r["identifier"] for r in rows]
    if len(set(identifiers)) != len(identifiers):
        print("error: duplicate technique identifiers in the document", file=sys.stderr)
        return 2

    # Every technique must belong to a category the document itself defines.
    # A technique in an undefined category produces a registry the code cannot
    # import, and the failure would surface at import time rather than at
    # generation time.
    defined_categories = set(
        re.findall(r"^\|\s*\*\*(AAT-\d{1,2})\*\*\s*\|", text, re.M)
    )
    undefined = sorted(
        {i.rsplit(".", 1)[0] for i in identifiers} - defined_categories
    )
    if undefined:
        print(
            "error: the document defines techniques in categories it does not "
            "define: " + ", ".join(undefined),
            file=sys.stderr,
        )
        return 2

    if not LIBRARY.exists():
        print(
            f"error: the technique library is not found at {LIBRARY}; the library "
            "is canonical for the detection objectives and the registry cannot "
            "be written without it",
            file=sys.stderr,
        )
        return 2
    library_text = LIBRARY.read_text(encoding="utf-8")
    objectives = extract_library_objectives(library_text)
    missing = [i for i in identifiers if i not in objectives]
    if missing:
        print(
            "error: the technique library carries no detection objective for: "
            + ", ".join(missing),
            file=sys.stderr,
        )
        return 2
    for row in rows:
        row["detection_objective"] = objectives[str(row["identifier"])]

    rendered = render(rows)

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
    print(f"wrote {TARGET} ({len(rows)} techniques)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
