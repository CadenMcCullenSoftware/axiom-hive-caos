"""Tests for the consistency of the set's two binding instruments.

The technique library records technique-level bindings: "this countermeasure is
a candidate response to this specific technique". The countermeasure catalogue
records category-level bindings: "this countermeasure addresses this category".

The two are instruments at different granularity, and the library's is the
finer. A binding that names a countermeasure whose catalogue entry does not
list the technique's category is not a contradiction; it is a finer claim. The
aggregate is large enough to be worth measuring, and this module holds the
measurement so that it is reproducible rather than a claim in prose.

The measurement is recorded at `reference/ai-attack-technique-library.md` §20.5.
The baseline below is the figure as at 2026-10-20. When the catalogue's
category-level sets are reconciled against the library's technique-level sets,
the baseline falls and this test's upper bound should be lowered with it. The
test fails if the divergence grows, which is the direction that matters: a
growing divergence means the two documents are drifting apart.
"""

from __future__ import annotations

import pathlib
import re
import unittest
from typing import Dict, List

from caos.countermeasures import CATALOGUE
from caos.taxonomy import TECHNIQUES

LIBRARY = pathlib.Path(__file__).resolve().parents[1].parent / "reference" / "ai-attack-technique-library.md"

#: The measured divergence as recorded in the library at §20.5.
#:
#: 234 technique-level bindings. At the library's version 1.1, 104 of them
#: named a countermeasure whose catalogue entry omitted the technique's
#: category, because the catalogue's category-level lists were under-inclusive.
#: The catalogue was reconciled against the library's technique-level set on
#: 2026-10-20 — the library's set being the finer instrument, and the
#: direction of the reconciliation being to bring the catalogue up to it
#: rather than to narrow the library down to it. The divergence is now zero.
#:
#: The bound is held rather than asserted: it may fall further, and it must
#: not rise, because a rise would mean the two documents are drifting apart.
RECORDED_BINDINGS = 234
RECORDED_DIVERGENCE = 0
RECORDED_CATALOGUE_PAIRS = 162
RECORDED_CATALOGUE_ONLY_PAIRS = 38


def _split_row(line: str) -> List[str]:
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [cell.strip() for cell in inner.split("|")]


def library_bindings() -> Dict[str, List[str]]:
    """Return the technique-level bindings recorded in the technique library.

    The library is a document, not a code dependency. Where it is absent the
    measurement cannot be taken, and the measurement is skipped rather than
    failed: a missing document is not a divergence between two documents.
    """
    if not LIBRARY.exists():
        return {}
    text = LIBRARY.read_text(encoding="utf-8")
    bindings: Dict[str, List[str]] = {}
    for line in text.splitlines():
        cells = _split_row(line)
        if len(cells) == 9 and re.fullmatch(r"AAT-\d{1,2}\.\d{1,2}", cells[0]):
            bindings.setdefault(cells[0], re.findall(r"OCC-\d\d", cells[5]))
    return bindings


class BindingConsistencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bindings = library_bindings()
        self.catalogue = {c.identifier: c for c in CATALOGUE}
        if not self.bindings:
            self.skipTest(
                "the technique library is not present, so the divergence "
                "between the two instruments cannot be measured"
            )

    def test_the_library_carries_an_entry_for_every_technique(self) -> None:
        known = {t.identifier for t in TECHNIQUES}
        self.assertEqual(set(self.bindings), known)

    def test_every_binding_resolves_to_a_catalogue_entry(self) -> None:
        for technique_id, occurrences in self.bindings.items():
            for occurrence in occurrences:
                self.assertIn(
                    occurrence,
                    self.catalogue,
                    f"{technique_id} names a countermeasure not in the catalogue",
                )

    def test_every_technique_carries_at_least_one_binding(self) -> None:
        for technique in TECHNIQUES:
            self.assertTrue(
                self.bindings.get(technique.identifier),
                f"{technique.identifier} carries no countermeasure binding",
            )

    def test_the_binding_count_has_not_changed_without_the_record_being_updated(self) -> None:
        total = sum(len(v) for v in self.bindings.values())
        self.assertEqual(total, RECORDED_BINDINGS)

    def test_the_divergence_has_not_grown(self) -> None:
        """The two binding sets are reconciled, and must stay reconciled.

        At the library's version 1.1 the divergence was 104: the catalogue's
        category-level lists were under-inclusive, and the library's
        technique-level set was the finer and more complete instrument. The
        catalogue was reconciled against it. The divergence may fall further;
        it must not rise, because a rise would mean the two documents are
        drifting apart.
        """
        divergence = 0
        for technique in TECHNIQUES:
            for occurrence in self.bindings.get(technique.identifier, []):
                if technique.category not in self.catalogue[occurrence].techniques:
                    divergence += 1
        self.assertLessEqual(
            divergence,
            RECORDED_DIVERGENCE,
            "the technique-level and category-level binding sets have drifted "
            "further apart than the measurement recorded at the library's §20.5; "
            "update the recorded measurement and the catalogue's AAT binding "
            "column together",
        )

    def test_the_catalogue_pair_counts_have_not_changed_silently(self) -> None:
        pairs = {
            (c.identifier, category)
            for c in CATALOGUE
            for category in c.techniques
        }
        used = {
            (occurrence, technique.category)
            for technique in TECHNIQUES
            for occurrence in self.bindings.get(technique.identifier, [])
        }
        self.assertEqual(len(pairs), RECORDED_CATALOGUE_PAIRS)
        self.assertEqual(
            len(pairs - used),
            RECORDED_CATALOGUE_ONLY_PAIRS,
            "the catalogue's category-level pairs have changed; the recorded "
            "measurement at the library's §20.5 needs updating with it",
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
