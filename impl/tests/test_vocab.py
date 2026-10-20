"""Tests for the controlled vocabulary."""

from __future__ import annotations

import unittest

from caos.vocab import (
    APPROVAL_DEPTHS,
    ATTRIBUTION_THRESHOLDS,
    CMClass,
    CollateralClass,
    Reversibility,
    ROEProfile,
    attribution_threshold,
    required_approvals,
)


class CollateralClassTests(unittest.TestCase):
    def test_exposure_normalisation_is_fixed(self) -> None:
        self.assertEqual(CollateralClass.C0.exposure, 0.00)
        self.assertEqual(CollateralClass.C1.exposure, 0.25)
        self.assertEqual(CollateralClass.C2.exposure, 0.60)
        self.assertEqual(CollateralClass.C3.exposure, 1.00)

    def test_exposure_is_monotonic(self) -> None:
        exposures = [c.exposure for c in CollateralClass]
        self.assertEqual(exposures, sorted(exposures))


class AttributionThresholdTests(unittest.TestCase):
    def test_thresholds_rise_with_consequence(self) -> None:
        thresholds = [attribution_threshold(c) for c in CollateralClass]
        self.assertEqual(thresholds, sorted(thresholds))
        self.assertEqual(thresholds, [0.50, 0.70, 0.85, 0.95])

    def test_threshold_table_matches_documentation(self) -> None:
        self.assertEqual(ATTRIBUTION_THRESHOLDS[CollateralClass.C2], 0.85)


class ApprovalDepthTests(unittest.TestCase):
    def test_more_demanding_of_profile_and_collateral_prevails(self) -> None:
        # A high collateral class demands more than a low profile.
        required = required_approvals(ROEProfile.R0_OBSERVE, CollateralClass.C2)
        self.assertIn("director", required)
        self.assertIn("legal_contact", required)

    def test_higher_profile_demands_more_than_low_collateral(self) -> None:
        required = required_approvals(ROEProfile.R4_DISRUPT, CollateralClass.C0)
        self.assertIn("director", required)
        self.assertIn("asset_owner", required)
        self.assertNotIn("executive", required)

    def test_every_profile_has_a_depth(self) -> None:
        for profile in ROEProfile:
            self.assertTrue(APPROVAL_DEPTHS[profile])


class ProfileTests(unittest.TestCase):
    def test_collateral_ceilings_are_ordered(self) -> None:
        ceilings = [p.max_collateral.value for p in ROEProfile]
        self.assertEqual(ceilings, sorted(ceilings))

    def test_disrupt_permits_the_disrupt_class(self) -> None:
        self.assertIn(CMClass.CM_F, ROEProfile.R4_DISRUPT.permitted_classes)

    def test_observe_permits_detection_and_hardening_only(self) -> None:
        self.assertEqual(
            ROEProfile.R0_OBSERVE.permitted_classes,
            frozenset({CMClass.CM_A, CMClass.CM_B}),
        )

    def test_deception_is_not_available_below_r3(self) -> None:
        self.assertNotIn(CMClass.CM_E, ROEProfile.R2_TRAP.permitted_classes)
        self.assertIn(CMClass.CM_E, ROEProfile.R3_DECEIVE.permitted_classes)

    def test_observation_is_available_from_r1(self) -> None:
        self.assertIn(CMClass.CM_D, ROEProfile.R1_SHIELD.permitted_classes)
        self.assertIn(CMClass.CM_D, ROEProfile.R2_TRAP.permitted_classes)

    def test_read_only_autonomy_is_not_permitted_at_observe(self) -> None:
        self.assertFalse(ROEProfile.R0_OBSERVE.permits_read_only_autonomy)
        self.assertTrue(ROEProfile.R1_SHIELD.permits_read_only_autonomy)


class ReversibilityTests(unittest.TestCase):
    def test_ordering_puts_reversible_above_none(self) -> None:
        self.assertGreater(Reversibility.REVERSIBLE.value, Reversibility.NONE.value)
        self.assertGreater(Reversibility.REVERSED.value, Reversibility.LOW.value)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
