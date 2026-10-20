"""Tests for the scoring and confidence model."""

from __future__ import annotations

import unittest

from caos.models import ThreatAssessment
from caos.scoring import (
    DERIVATION_PENALTIES,
    band_for_impact,
    band_for_likelihood,
    compare_options,
    derivation_penalty,
    effective_threat,
    propagate_confidence,
    residual_risk,
    risk_adjusted_priority,
    score_breakdown,
    threat_score,
)
from caos.vocab import CollateralClass


def assessment(**kwargs) -> ThreatAssessment:
    defaults = dict(
        likelihood=0.6,
        impact=3,
        autonomy_factor=1,
        velocity=1,
        attribution_confidence=0.5,
        attribution_basis="behavioural signature overlap",
    )
    defaults.update(kwargs)
    return ThreatAssessment(**defaults)


class ThreatScoreTests(unittest.TestCase):
    def test_score_is_the_product_of_its_components(self) -> None:
        a = assessment(likelihood=0.5, impact=4, autonomy_factor=2, velocity=2)
        self.assertAlmostEqual(threat_score(a), 0.5 * 4 * 2 * 2)

    def test_score_range_is_zero_to_twenty(self) -> None:
        low = assessment(likelihood=0.0, impact=0, autonomy_factor=0, velocity=0)
        high = assessment(likelihood=1.0, impact=5, autonomy_factor=2, velocity=2)
        self.assertEqual(threat_score(low), 0.0)
        self.assertEqual(threat_score(high), 20.0)

    def test_effective_threat_applies_attribution_confidence(self) -> None:
        a = assessment(likelihood=1.0, impact=5, autonomy_factor=2, velocity=2,
                       attribution_confidence=0.8)
        self.assertAlmostEqual(effective_threat(threat_score(a), 0.8), 16.0)

    def test_zero_attribution_gives_zero_effective_threat(self) -> None:
        a = assessment(attribution_confidence=0.0)
        self.assertEqual(a.effective_threat, 0.0)

    def test_velocity_is_visible_as_a_separate_component(self) -> None:
        rows = score_breakdown(assessment())
        components = [r["component"] for r in rows]
        self.assertIn("velocity", components)
        self.assertIn("attribution confidence", components)

    def test_bands_cover_the_defined_ranges(self) -> None:
        self.assertIn("attack behaviour", band_for_likelihood(0.8))
        self.assertIn("nuisance", band_for_impact(1))
        self.assertIn("critical function", band_for_impact(5))

    def test_out_of_range_components_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            assessment(impact=6)
        with self.assertRaises(ValueError):
            assessment(likelihood=1.5)


class ResidualRiskTests(unittest.TestCase):
    def test_residual_risk_reduces_with_effectiveness(self) -> None:
        self.assertAlmostEqual(residual_risk(10.0, 0.0), 10.0)
        self.assertAlmostEqual(residual_risk(10.0, 1.0), 0.0)
        self.assertAlmostEqual(residual_risk(10.0, 0.25), 7.5)

    def test_effectiveness_out_of_range_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            residual_risk(10.0, 1.5)


class PriorityTests(unittest.TestCase):
    def test_priority_discounts_collateral_exposure(self) -> None:
        c0 = risk_adjusted_priority(10.0, 0.8, CollateralClass.C0)
        c2 = risk_adjusted_priority(10.0, 0.8, CollateralClass.C2)
        self.assertGreater(c0, c2)

    def test_priority_is_zero_at_full_collateral(self) -> None:
        self.assertEqual(
            risk_adjusted_priority(10.0, 0.8, CollateralClass.C3), 0.0
        )

    def test_priority_scales_with_effective_threat(self) -> None:
        low = risk_adjusted_priority(2.0, 0.8, CollateralClass.C1)
        high = risk_adjusted_priority(18.0, 0.8, CollateralClass.C1)
        self.assertGreater(high, low)


class ConfidencePropagationTests(unittest.TestCase):
    def test_derived_confidence_is_the_weakest_input(self) -> None:
        self.assertAlmostEqual(propagate_confidence([0.9, 0.4, 0.7]), 0.4)

    def test_penalty_reduces_the_propagated_value(self) -> None:
        # The propagation is subtractive: c_derived = c_weakest - penalty.
        self.assertAlmostEqual(propagate_confidence([0.8], 0.10), 0.70)

    def test_propagation_never_returns_a_negative_confidence(self) -> None:
        self.assertEqual(propagate_confidence([0.05], 0.20), 0.0)

    def test_propagation_is_the_most_conservative_of_the_two_forms(self) -> None:
        # A leaf at 0.95 with a 0.10 penalty yields 0.85, which is the class
        # minimum for a C2 countermeasure.
        self.assertAlmostEqual(propagate_confidence([0.95], 0.10), 0.85)

    def test_derivation_penalties_are_declared(self) -> None:
        self.assertEqual(derivation_penalty("direct observation"), 0.00)
        self.assertEqual(derivation_penalty("multi-step inference"), 0.10)
        with self.assertRaises(KeyError):
            derivation_penalty("unstated derivation")

    def test_penalty_table_is_not_empty(self) -> None:
        self.assertTrue(DERIVATION_PENALTIES)


class OptionComparisonTests(unittest.TestCase):
    def test_options_are_ordered_by_residual_risk(self) -> None:
        from caos.scoring import Option

        options = [
            Option("high", 8.0, CollateralClass.C0, 0.1),
            Option("low", 2.0, CollateralClass.C1, 0.1),
            Option("middle", 5.0, CollateralClass.C0, 0.1),
        ]
        ordered = compare_options(options)
        self.assertEqual([o.label for o in ordered], ["low", "middle", "high"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
