"""Tests for the two synchronisers' failure paths.

The synchronisers are the mechanism that keeps the executable catalogue and
the executable technique registry in step with the canonical documents. A
failure that produces a silently degraded generated module is worse than no
mechanism at all, because the degradation is invisible until something
depends on the technique or the countermeasure that went missing.

Each test here corrupts a copy of the canonical document under a temporary
tree and asserts that the tool refuses it, writes nothing, and says what is
wrong.
"""

from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

IMPL = pathlib.Path(__file__).resolve().parents[1]
SET = IMPL.parent

CATALOGUE = SET / "operational" / "countermeasure-catalogue.md"
TAXONOMY = SET / "operational" / "adversary-ai-taxonomy-and-threat-model.md"
LIBRARY = SET / "reference" / "ai-attack-technique-library.md"


def _tree(tmp: pathlib.Path) -> pathlib.Path:
    """Build a throwaway tree with the tools, the code, and the documents."""
    (tmp / "impl").mkdir(parents=True, exist_ok=True)
    shutil.copytree(IMPL / "tools", tmp / "impl" / "tools")
    shutil.copytree(IMPL / "caos", tmp / "impl" / "caos")
    (tmp / "operational").mkdir(exist_ok=True)
    (tmp / "reference").mkdir(exist_ok=True)
    shutil.copy(CATALOGUE, tmp / "operational" / CATALOGUE.name)
    shutil.copy(TAXONOMY, tmp / "operational" / TAXONOMY.name)
    shutil.copy(LIBRARY, tmp / "reference" / LIBRARY.name)
    return tmp


def _run(tree: pathlib.Path, tool: str):
    return subprocess.run(
        [sys.executable, str(tree / "impl" / "tools" / tool)],
        capture_output=True,
        text=True,
        cwd=str(tree),
    )


class SyncCatalogueTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tree = _tree(pathlib.Path(self._tmp.name))
        self.document = self.tree / "operational" / CATALOGUE.name
        self.original = self.document.read_text(encoding="utf-8")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _generated(self) -> str:
        return (self.tree / "impl" / "caos" / "catalogue_data.py").read_text(
            encoding="utf-8"
        )

    def test_a_clean_document_writes_the_module(self) -> None:
        result = _run(self.tree, "sync_catalogue.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("43 entries", result.stdout)

    def test_a_duplicate_identifier_is_refused(self) -> None:
        self.document.write_text(
            self.original.replace("#### OCC-02 — ", "#### OCC-01 — ", 1),
            encoding="utf-8",
        )
        before = self._generated()
        result = _run(self.tree, "sync_catalogue.py")
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate countermeasure identifiers", result.stderr)
        self.assertEqual(self._generated(), before, "the module was written")

    def test_a_missing_entry_is_refused(self) -> None:
        self.document.write_text(
            self.original.replace("#### OCC-02 — ", "#### OCC-99 — ", 1),
            encoding="utf-8",
        )
        before = self._generated()
        result = _run(self.tree, "sync_catalogue.py")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self._generated(), before, "the module was written")

    def test_a_malformed_table_row_is_refused(self) -> None:
        self.document.write_text(
            self.original.replace(
                "| Class | CM-A Detect |", "| Class | CM-A Detect |", 1
            ).replace(
                "| Reversibility | Reversible |", "| Reversibility |", 1
            ),
            encoding="utf-8",
        )
        before = self._generated()
        result = _run(self.tree, "sync_catalogue.py")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self._generated(), before, "the module was written")


class SyncTaxonomyTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tree = _tree(pathlib.Path(self._tmp.name))
        self.document = self.tree / "operational" / TAXONOMY.name
        self.library = self.tree / "reference" / LIBRARY.name
        self.original = self.document.read_text(encoding="utf-8")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _generated(self) -> str:
        return (self.tree / "impl" / "caos" / "taxonomy_data.py").read_text(
            encoding="utf-8"
        )

    def test_a_clean_document_writes_the_module(self) -> None:
        result = _run(self.tree, "sync_taxonomy.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("techniques", result.stdout)

    def test_a_technique_row_that_cannot_be_read_is_refused(self) -> None:
        self.document.write_text(
            self.original.replace("| **AAT-1.1** |", "| AAT-1.1 |", 1),
            encoding="utf-8",
        )
        before = self._generated()
        result = _run(self.tree, "sync_taxonomy.py")
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot be read", result.stderr)
        self.assertEqual(self._generated(), before, "the module was written")

    def test_a_missing_library_is_refused(self) -> None:
        self.library.unlink()
        before = self._generated()
        result = _run(self.tree, "sync_taxonomy.py")
        self.assertEqual(result.returncode, 2)
        self.assertIn("technique library is not found", result.stderr)
        self.assertEqual(self._generated(), before, "the module was written")

    def test_a_technique_in_an_undefined_category_is_refused(self) -> None:
        self.document.write_text(
            self.original.replace("| **AAT-1.1** |", "| **AAT-11.1** |", 1),
            encoding="utf-8",
        )
        before = self._generated()
        result = _run(self.tree, "sync_taxonomy.py")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self._generated(), before, "the module was written")

    def test_a_duplicate_identifier_is_refused(self) -> None:
        self.document.write_text(
            self.original.replace("| **AAT-1.2** |", "| **AAT-1.1** |", 1),
            encoding="utf-8",
        )
        before = self._generated()
        result = _run(self.tree, "sync_taxonomy.py")
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate", result.stderr)
        self.assertEqual(self._generated(), before, "the module was written")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
