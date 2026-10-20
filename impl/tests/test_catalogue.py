"""Tests for the countermeasure catalogue and the taxonomy registry."""

from __future__ import annotations

import unittest

from caos.countermeasures import CATALOGUE, CATALOGUE_INDEX, by_class, for_techniques, get
from caos.taxonomy import (
    CATEGORIES,
    TECHNIQUES,
    TECHNIQUE_INDEX,
    category_of,
    coverage_report,
    technique,
)
from caos.vocab import (
    AttributionDependency,
    AutonomyClass,
    CMClass,
    CollateralClass,
    CountermeasureStatus,
    DirectionOfEffect,
    Reversibility,
    ROEProfile,
)


class CatalogueIntegrityTests(unittest.TestCase):
    def test_catalogue_holds_forty_three_entries(self) -> None:
        self.assertEqual(len(CATALOGUE), 43)

    def test_identifiers_are_unique_and_contiguous(self) -> None:
        identifiers = [c.identifier for c in CATALOGUE]
        self.assertEqual(len(set(identifiers)), len(identifiers))
        expected = [f"OCC-{i:02d}" for i in range(1, 44)]
        self.assertEqual(sorted(identifiers), expected)

    def test_class_grouping_is_contiguous(self) -> None:
        by_id = {c.identifier: c for c in CATALOGUE}
        for index in range(1, 8):
            self.assertIs(by_id[f"OCC-{index:02d}"].cm_class, CMClass.CM_A)
        for index in range(8, 17):
            self.assertIs(by_id[f"OCC-{index:02d}"].cm_class, CMClass.CM_B)
        for index in range(17, 24):
            self.assertIs(by_id[f"OCC-{index:02d}"].cm_class, CMClass.CM_C)
        for index in range(24, 28):
            self.assertIs(by_id[f"OCC-{index:02d}"].cm_class, CMClass.CM_D)
        for index in range(28, 34):
            self.assertIs(by_id[f"OCC-{index:02d}"].cm_class, CMClass.CM_E)
        for index in range(34, 40):
            self.assertIs(by_id[f"OCC-{index:02d}"].cm_class, CMClass.CM_F)
        for index in range(40, 44):
            self.assertIs(by_id[f"OCC-{index:02d}"].cm_class, CMClass.CM_G)

    def test_no_entry_targets_human_beings(self) -> None:
        for cm in CATALOGUE:
            self.assertFalse(cm.targets_humans)

    def test_no_entry_uses_a_model_as_a_weapon(self) -> None:
        for cm in CATALOGUE:
            self.assertFalse(cm.weaponises_model)

    def test_autonomous_entries_are_read_only_and_c0(self) -> None:
        for cm in CATALOGUE:
            if cm.autonomy is AutonomyClass.AC4_AUTONOMOUS:
                self.assertTrue(cm.read_only)
                self.assertIs(cm.collateral, CollateralClass.C0)

    def test_every_entry_declares_a_minimum_profile(self) -> None:
        for cm in CATALOGUE:
            self.assertIsInstance(cm.min_profile, ROEProfile)

    def test_every_entry_declares_its_direction(self) -> None:
        for cm in CATALOGUE:
            self.assertIsInstance(cm.direction, DirectionOfEffect)

    def test_every_entry_declares_a_reversibility(self) -> None:
        for cm in CATALOGUE:
            self.assertIsInstance(cm.reversibility, Reversibility)

    def test_every_entry_declares_an_attribution_dependency(self) -> None:
        for cm in CATALOGUE:
            self.assertIsInstance(cm.attribution_dependency, AttributionDependency)

    def test_every_entry_is_deliverable_or_marked(self) -> None:
        for cm in CATALOGUE:
            self.assertIn(
                cm.status,
                {
                    CountermeasureStatus.ACTIVE,
                    CountermeasureStatus.CONDITIONAL,
                    CountermeasureStatus.WITHHELD,
                },
            )

    def test_a_withheld_entry_remains_in_the_catalogue(self) -> None:
        withheld = [c for c in CATALOGUE if c.status is CountermeasureStatus.WITHHELD]
        self.assertTrue(withheld)
        for cm in withheld:
            self.assertIn(cm.identifier, CATALOGUE_INDEX)

    def test_residual_reduction_is_bounded_and_carries_confidence(self) -> None:
        for cm in CATALOGUE:
            self.assertGreaterEqual(cm.residual_reduction, 0.0)
            self.assertLessEqual(cm.residual_reduction, 1.0)
            self.assertGreater(cm.effectiveness_confidence, 0.0)
            self.assertLessEqual(cm.effectiveness_confidence, 1.0)

    def test_disruptive_entries_never_exceed_class_c2(self) -> None:
        for cm in by_class(CMClass.CM_F):
            self.assertLessEqual(cm.collateral.value, CollateralClass.C2.value)

    def test_outward_entries_above_c0_require_identity_attribution(self) -> None:
        for cm in CATALOGUE:
            if (
                cm.direction is DirectionOfEffect.ADVERSARY_SYSTEM
                and cm.collateral.value >= CollateralClass.C1.value
            ):
                self.assertIs(
                    cm.attribution_dependency, AttributionDependency.IDENTITY,
                    f"{cm.identifier} acts outward at {cm.collateral.name} and must "
                    "depend on identity attribution",
                )

    def test_an_outward_c0_entry_may_depend_on_class_attribution(self) -> None:
        cm = get("OCC-37")
        self.assertIs(cm.direction, DirectionOfEffect.ADVERSARY_SYSTEM)
        self.assertIs(cm.collateral, CollateralClass.C0)
        self.assertIs(cm.attribution_dependency, AttributionDependency.CLASS)

    def test_identity_free_entries_exist_in_the_catalogue(self) -> None:
        free = [
            cm
            for cm in CATALOGUE
            if cm.attribution_dependency is AttributionDependency.NONE
        ]
        self.assertGreaterEqual(len(free), 10)

    def test_get_returns_none_for_an_unknown_identifier(self) -> None:
        self.assertIsNone(get("OCC-999"))

    def test_for_techniques_accepts_categories_and_techniques(self) -> None:
        by_category = for_techniques({"AAT-2"})
        by_technique = for_techniques({"AAT-2.1"})
        self.assertTrue(by_category)
        self.assertTrue(by_technique)
        self.assertIn("OCC-05", {c.identifier for c in by_technique})


class TaxonomyIntegrityTests(unittest.TestCase):
    def test_ten_categories_are_defined(self) -> None:
        self.assertEqual(len(CATEGORIES), 10)
        for index in range(1, 11):
            self.assertIn(f"AAT-{index}", CATEGORIES)

    def test_every_technique_belongs_to_a_defined_category(self) -> None:
        for tech in TECHNIQUES:
            self.assertIn(tech.category, CATEGORIES)

    def test_technique_identifiers_are_unique(self) -> None:
        identifiers = [t.identifier for t in TECHNIQUES]
        self.assertEqual(len(set(identifiers)), len(identifiers))

    def test_every_category_carries_at_least_six_techniques(self) -> None:
        for index in range(1, 11):
            count = sum(1 for t in TECHNIQUES if t.category == f"AAT-{index}")
            self.assertGreaterEqual(count, 6, f"AAT-{index} has only {count}")

    def test_technique_bindings_resolve_to_the_catalogue(self) -> None:
        catalogue_ids = {c.identifier for c in CATALOGUE}
        for tech in TECHNIQUES:
            for binding in tech.countermeasure_bindings:
                self.assertIn(binding, catalogue_ids, f"{tech.identifier}: {binding}")

    def test_every_technique_states_its_attribution_note(self) -> None:
        for tech in TECHNIQUES:
            self.assertTrue(tech.attribution_note)
            self.assertTrue(tech.detection_objective)

    def test_category_of_derives_the_prefix(self) -> None:
        self.assertEqual(category_of("AAT-7.3"), "AAT-7")
        self.assertEqual(category_of("AAT-7"), "AAT-7")

    def test_unknown_technique_returns_none(self) -> None:
        self.assertIsNone(technique("AAT-99.9"))

    def test_coverage_report_distinguishes_covered_from_untested(self) -> None:
        report = coverage_report(frozenset({"AAT-1.1"}))
        by_id = {row["technique"]: row for row in report}
        self.assertEqual(by_id["AAT-1.1"]["status"], "covered")
        self.assertEqual(by_id["AAT-1.2"]["status"], "untested")
        self.assertEqual(len(report), len(TECHNIQUES))

    def test_technique_index_is_consistent(self) -> None:
        self.assertEqual(len(TECHNIQUE_INDEX), len(TECHNIQUES))
        for tech in TECHNIQUES:
            self.assertIs(TECHNIQUE_INDEX[tech.identifier], tech)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
