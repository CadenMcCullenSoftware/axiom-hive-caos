"""Tests for the admissibility engine.

Each of the twelve conditions is tested twice: once failing, once passing.
The engine is the enforcement surface of the authorisation model, so a
condition that is not exercised is a condition that is not enforced.
"""

from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import timedelta

from caos.countermeasures import get as get_cm
from caos.models import OperationCard, ThreatAssessment, utc_now
from caos.roe import (
    CONDITION_NATURE,
    CONDITION_TITLES,
    EvaluationContext,
    card_is_armable,
    evaluate,
)
from caos.vocab import (
    AttributionDependency,
    AutonomyClass,
    CollateralClass,
    Reversibility,
    ROEProfile,
)


def make_card(**overrides) -> OperationCard:
    now = utc_now()
    assessment = ThreatAssessment(
        likelihood=0.6,
        impact=3,
        autonomy_factor=1,
        velocity=1,
        attribution_confidence=0.9,
        attribution_basis="identity attribution at the issuer's records",
    )
    defaults = dict(
        card_id="OC-TEST-001",
        title="test card",
        owner="operator-1",
        created_at=now,
        objective="test objective",
        hypothesis="test hypothesis",
        disconfirming_observation="test disconfirming observation",
        ea_reference="EA-TEST",
        profile=ROEProfile.R2_TRAP,
        collateral_ceiling=CollateralClass.C1,
        autonomy_ceiling=AutonomyClass.AC2_SUPERVISED,
        approver_roles=frozenset({"duty_manager", "legal_contact", "team_lead"}),
        expires_at=now + timedelta(days=1),
        authorised_targets=("estate:test-service", "adversary:principal-1"),
        excluded_targets=("all third-party infrastructure without authorisation",),
        threat=assessment,
        classification="AAT-1",
        techniques=("AAT-1.1",),
        abort_conditions=("service degradation",),
        abort_owner="operator-1",
        abort_mechanism="single-key abort",
        deconfliction_passed=True,
        risk_of_inaction="the service may degrade",
        rationale="test rationale",
        alternatives_considered=("OCC-01",),
        contingency="abort on service degradation",
        contingency_recorded_at=now,
    )
    defaults.update(overrides)
    return OperationCard(**defaults)


def condition(result, identifier: str):
    for check in result.checks:
        if check.condition == identifier:
            return check
    raise AssertionError(f"condition {identifier} was not evaluated")


class AD1ProfileClassTests(unittest.TestCase):
    def test_class_outside_the_profile_is_refused(self) -> None:
        card = make_card(profile=ROEProfile.R0_OBSERVE)
        cm = get_cm("OCC-24")  # CM-D Observe, not permitted at R0
        result = evaluate(card, cm)
        self.assertFalse(result.admissible)
        self.assertFalse(condition(result, "AD-1").passed)
        self.assertIn("OCC-24", result.blocking_summary)

    def test_class_inside_the_profile_passes(self) -> None:
        card = make_card(profile=ROEProfile.R2_TRAP)
        cm = get_cm("OCC-24")
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-1").passed)

    def test_countermeasure_floor_above_the_card_profile_is_refused(self) -> None:
        card = make_card(profile=ROEProfile.R0_OBSERVE)
        cm = get_cm("OCC-34")  # minimum profile R4
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-1").passed)
        self.assertIn("requires profile", condition(result, "AD-1").margin)


class AD2CollateralTests(unittest.TestCase):
    def test_collateral_above_the_ceiling_is_refused(self) -> None:
        card = make_card(collateral_ceiling=CollateralClass.C0)
        cm = get_cm("OCC-24")  # C1
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-2").passed)
        self.assertIn("exceeds ceiling", condition(result, "AD-2").margin)

    def test_collateral_above_the_profile_ceiling_is_refused(self) -> None:
        card = make_card(
            profile=ROEProfile.R1_SHIELD, collateral_ceiling=CollateralClass.C2
        )
        cm = get_cm("OCC-24")  # C1, permitted at R2, not at R1
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-2").passed)

    def test_collateral_within_the_ceiling_passes(self) -> None:
        card = make_card(collateral_ceiling=CollateralClass.C1)
        cm = get_cm("OCC-24")
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-2").passed)


class AD3ReversibilityTests(unittest.TestCase):
    def test_reversibility_below_the_floor_is_refused(self) -> None:
        card = make_card(
            required_reversibility=Reversibility.REVERSIBLE,
            profile=ROEProfile.R1_SHIELD,
        )
        cm = get_cm("OCC-21")  # REVERSED
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-3").passed)

    def test_reversibility_at_or_above_the_floor_passes(self) -> None:
        card = make_card(required_reversibility=Reversibility.REVERSED)
        cm = get_cm("OCC-01")
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-3").passed)


class AD4TargetContainmentTests(unittest.TestCase):
    def test_missing_scope_is_refused(self) -> None:
        card = make_card(authorised_targets=("estate:test-service",))
        cm = get_cm("OCC-24")  # direction: adversary behaviour in own environment
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-4").passed)

    def test_adversary_direction_needs_an_adversary_target(self) -> None:
        card = make_card(authorised_targets=("estate:test-service",))
        cm = get_cm("OCC-34")  # direction: adversary system
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-4").passed)
        self.assertIn("adversary:", condition(result, "AD-4").margin)


class AD4SetContainmentTests(unittest.TestCase):
    def test_a_named_target_outside_the_card_is_refused(self) -> None:
        card = make_card(authorised_targets=("estate:test-service",))
        cm = replace(get_cm("OCC-01"), targets=("estate:other-service",))
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-4").passed)
        self.assertIn("estate:other-service", condition(result, "AD-4").margin)

    def test_a_named_target_on_the_card_passes(self) -> None:
        card = make_card(authorised_targets=("estate:test-service",))
        cm = replace(get_cm("OCC-01"), targets=("estate:test-service",))
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-4").passed)

    def test_an_entry_without_named_targets_falls_back_to_the_scope_test(self) -> None:
        card = make_card(authorised_targets=("estate:test-service",))
        cm = get_cm("OCC-01")
        self.assertEqual(cm.targets, ())
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-4").passed)


class AD5ThirdPartyTests(unittest.TestCase):
    def test_third_party_effect_without_authorisation_is_refused(self) -> None:
        card = make_card(
            profile=ROEProfile.R4_DISRUPT,
            collateral_ceiling=CollateralClass.C2,
            approver_roles=frozenset(
                {"director", "legal_contact", "asset_owner", "team_lead"}
            ),
            authorised_targets=("estate:test-service", "adversary:principal-1"),
        )
        cm = get_cm("OCC-34")  # outward, C2
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-5").passed)
        self.assertIn("third-party authorisation", condition(result, "AD-5").margin)

    def test_missing_tenancy_assessment_is_refused(self) -> None:
        card = make_card(
            third_party_authorised=True,
            third_party_assessment="",
            authorised_targets=("estate:test-service", "adversary:principal-1"),
        )
        cm = get_cm("OCC-24")  # acts on the adversary's behaviour in own environment
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-5").passed)
        self.assertIn("shared-tenancy assessment", condition(result, "AD-5").margin)

    def test_own_estate_countermeasure_passes(self) -> None:
        card = make_card()
        cm = get_cm("OCC-01")  # own estate, no third-party effect
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-5").passed)

    def test_a_c0_outward_countermeasure_needs_no_third_party_authorisation(self) -> None:
        card = make_card(
            profile=ROEProfile.R1_SHIELD,
            third_party_authorised=False,
            third_party_assessment="",
        )
        cm = get_cm("OCC-37")  # outward, but C0: no effect outside the estate
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-5").passed)


class AD6HumanBeingsTests(unittest.TestCase):
    def test_a_countermeasure_targeting_people_cannot_be_constructed(self) -> None:
        cm = get_cm("OCC-01")
        with self.assertRaises(ValueError):
            replace(cm, targets_humans=True)

    def test_condition_passes_for_a_catalogued_countermeasure(self) -> None:
        card = make_card()
        result = evaluate(card, get_cm("OCC-01"))
        self.assertTrue(condition(result, "AD-6").passed)


class AD7AutonomyTests(unittest.TestCase):
    def test_autonomy_above_the_card_ceiling_is_refused(self) -> None:
        card = make_card(autonomy_ceiling=AutonomyClass.AC1_ASSISTED)
        cm = get_cm("OCC-24")  # AC3
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-7").passed)

    def test_autonomy_above_the_profile_ceiling_is_refused(self) -> None:
        card = make_card(
            profile=ROEProfile.R0_OBSERVE,
            autonomy_ceiling=AutonomyClass.AC2_SUPERVISED,
        )
        cm = get_cm("OCC-05")  # AC-2, but R0 permits AC-1 only
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-7").passed)

    def test_autonomous_execution_is_refused_at_a_raised_ceiling(self) -> None:
        card = make_card(
            profile=ROEProfile.R1_SHIELD,
            autonomy_ceiling=AutonomyClass.AC4_AUTONOMOUS,
        )
        cm = get_cm("OCC-26")  # AC0, read-only
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-7").passed)

    def test_autonomous_execution_needs_a_raised_ceiling(self) -> None:
        card = make_card(
            profile=ROEProfile.R1_SHIELD,
            autonomy_ceiling=AutonomyClass.AC2_SUPERVISED,
        )
        cm = get_cm("OCC-27")  # AC-4, read-only
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-7").passed)

    def test_non_read_only_autonomous_execution_cannot_be_constructed(self) -> None:
        cm = get_cm("OCC-26")
        with self.assertRaises(ValueError):
            replace(cm, autonomy=AutonomyClass.AC4_AUTONOMOUS, read_only=False)


class AD8ConfidenceTests(unittest.TestCase):
    def test_confidence_below_the_floor_is_refused(self) -> None:
        card = make_card(min_countermeasure_confidence=0.9)
        cm = get_cm("OCC-24")  # effectiveness confidence 0.50
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-8").passed)
        self.assertIn("short by", condition(result, "AD-8").margin)

    def test_confidence_at_or_above_the_floor_passes(self) -> None:
        card = make_card(min_countermeasure_confidence=0.30)
        cm = get_cm("OCC-02")
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-8").passed)

    def test_very_low_confidence_entries_fail_a_higher_floor(self) -> None:
        card = make_card(min_countermeasure_confidence=0.30)
        cm = get_cm("OCC-24")  # band confidence: very low
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-8").passed)


class AD9AttributionTests(unittest.TestCase):
    def test_identity_dependent_action_below_the_threshold_is_refused(self) -> None:
        card = make_card(
            threat=ThreatAssessment(
                likelihood=0.6,
                impact=3,
                autonomy_factor=1,
                velocity=1,
                attribution_confidence=0.5,
                attribution_basis="class attribution only",
            )
        )
        cm = get_cm("OCC-34")  # identity dependency, C2, threshold 0.85
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-9").passed)
        self.assertIn("short by", condition(result, "AD-9").margin)

    def test_identity_dependent_action_above_the_threshold_passes(self) -> None:
        card = make_card()
        cm = get_cm("OCC-34")
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-9").passed)

    def test_identity_independent_action_passes_at_low_confidence(self) -> None:
        card = make_card(
            threat=ThreatAssessment(
                likelihood=0.6,
                impact=3,
                autonomy_factor=1,
                velocity=1,
                attribution_confidence=0.2,
                attribution_basis="no attribution basis established",
            )
        )
        cm = get_cm("OCC-01")  # attribution dependency: none
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-9").passed)

    def test_external_dependency_requires_the_external_determination(self) -> None:
        card = make_card()
        cm = replace(
            get_cm("OCC-01"),
            attribution_dependency=AttributionDependency.EXTERNAL,
        )
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-9").passed)
        result2 = evaluate(
            card, cm, EvaluationContext(external_authority_confirmed=True)
        )
        self.assertTrue(condition(result2, "AD-9").passed)


class AD10DeconflictionTests(unittest.TestCase):
    def test_failed_deconfliction_is_refused(self) -> None:
        card = make_card(deconfliction_passed=False)
        result = evaluate(card, get_cm("OCC-01"))
        self.assertFalse(condition(result, "AD-10").passed)

    def test_passed_deconfliction_passes(self) -> None:
        card = make_card(deconfliction_passed=True)
        result = evaluate(card, get_cm("OCC-01"))
        self.assertTrue(condition(result, "AD-10").passed)


class AD11BudgetTests(unittest.TestCase):
    def test_insufficient_budget_is_refused(self) -> None:
        card = make_card(autonomy_budget=1, autonomy_consumed=1)
        cm = get_cm("OCC-24")  # 5 units
        result = evaluate(card, cm)
        self.assertFalse(condition(result, "AD-11").passed)
        self.assertIn("short by", condition(result, "AD-11").margin)

    def test_sufficient_budget_passes(self) -> None:
        card = make_card(autonomy_budget=5, autonomy_consumed=0)
        cm = get_cm("OCC-24")
        result = evaluate(card, cm)
        self.assertTrue(condition(result, "AD-11").passed)


class AD12NonWeaponisationTests(unittest.TestCase):
    def test_a_weaponising_countermeasure_cannot_be_constructed(self) -> None:
        cm = get_cm("OCC-01")
        with self.assertRaises(ValueError):
            replace(cm, weaponises_model=True)

    def test_condition_passes_for_a_catalogued_countermeasure(self) -> None:
        result = evaluate(make_card(), get_cm("OCC-01"))
        self.assertTrue(condition(result, "AD-12").passed)


class InformativeFailureTests(unittest.TestCase):
    def test_rejection_states_the_condition_and_the_margin(self) -> None:
        card = make_card(collateral_ceiling=CollateralClass.C0)
        result = evaluate(card, get_cm("OCC-24"))
        self.assertFalse(result.admissible)
        failures = result.failures
        self.assertTrue(failures)
        for failure in failures:
            self.assertTrue(failure.condition)
            self.assertTrue(failure.detail)
            self.assertTrue(failure.remedy, "a rejection must be actionable")

    def test_every_condition_is_titled_and_classified(self) -> None:
        for identifier in CONDITION_TITLES:
            self.assertIn(identifier, CONDITION_NATURE)
            self.assertTrue(CONDITION_TITLES[identifier])


class CardArmabilityTests(unittest.TestCase):
    def test_expired_card_is_not_armable(self) -> None:
        card = make_card(expires_at=utc_now() - timedelta(seconds=1))
        reasons = card_is_armable(card)
        self.assertTrue(any("expired" in r for r in reasons))

    def test_incomplete_card_is_not_armable(self) -> None:
        card = make_card(rationale="")
        reasons = card_is_armable(card)
        self.assertTrue(any("rationale" in r for r in reasons))

    def test_missing_risk_of_inaction_is_a_defect(self) -> None:
        card = make_card(risk_of_inaction="")
        self.assertTrue(
            any("risk_of_inaction" in d for d in card.completion_defects())
        )

    def test_missing_alternatives_is_a_defect(self) -> None:
        card = make_card(alternatives_considered=())
        self.assertTrue(
            any("alternatives_considered" in d for d in card.completion_defects())
        )

    def test_missing_excluded_targets_is_a_defect(self) -> None:
        card = make_card(excluded_targets=())
        self.assertTrue(
            any("excluded_targets" in d for d in card.completion_defects())
        )

    def test_missing_approvals_blocks_arming(self) -> None:
        card = make_card(approver_roles=frozenset({"operator"}))
        reasons = card_is_armable(card)
        self.assertTrue(any("approvals" in r for r in reasons))

    def test_incomplete_card_refuses_every_countermeasure(self) -> None:
        card = make_card(rationale="")
        result = evaluate(card, get_cm("OCC-01"))
        self.assertFalse(result.admissible)
        self.assertFalse(condition(result, "G-3").passed)

    def test_an_unregistered_technique_reference_is_a_defect(self) -> None:
        card = make_card(techniques=("AAT-99.9",))
        self.assertTrue(any("AAT-99.9" in d for d in card.completion_defects()))

    def test_a_registered_technique_reference_is_not_a_defect(self) -> None:
        card = make_card(techniques=("AAT-1.1",))
        self.assertEqual(card.unknown_techniques(), [])

    def test_a_contingency_without_a_timestamp_is_a_defect(self) -> None:
        card = make_card(contingency="abort on degradation")
        card.contingency_recorded_at = None
        self.assertTrue(
            any("timestamp" in d for d in card.completion_defects())
        )

    def test_a_timestamped_contingency_is_not_a_defect(self) -> None:
        card = make_card(contingency="abort on degradation")
        card.contingency_recorded_at = utc_now()
        self.assertFalse(any("timestamp" in d for d in card.completion_defects()))

    def test_complete_card_is_armable(self) -> None:
        card = make_card()
        self.assertEqual(card.completion_defects(), [])


class FailClosedTests(unittest.TestCase):
    def test_engine_never_raises_on_a_permitted_countermeasure(self) -> None:
        card = make_card()
        for identifier in ("OCC-01", "OCC-24", "OCC-34", "OCC-05"):
            result = evaluate(card, get_cm(identifier))
            self.assertIsInstance(result.admissible, bool)
            self.assertEqual(
            {c.condition for c in result.checks}, {f"AD-{i}" for i in range(1, 13)}
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
