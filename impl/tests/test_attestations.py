"""Tests for the attestation fields the admissibility algebra depends on.

AD-3, AD-5, AD-6, AD-10 and AD-12 are hybrid or human conditions: the
machine can establish that the judgement was made and recorded, and it
cannot make the judgement. The attestation fields are where that judgement is
recorded, and each of them must have a specific, testable effect on
admissibility.

These are the tests the reference implementation's own audit identified as
missing, and they exist because an attestation that the engine consults but
nothing tests is an attestation that can silently stop being consulted.
"""

from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import timedelta

from caos.countermeasures import get
from caos.models import OperationCard, ThreatAssessment, utc_now
from caos.roe import CONDITION_NATURE, EvaluationContext, evaluate
from caos.vocab import (
    AutonomyClass,
    CollateralClass,
    Reversibility,
    ROEProfile,
)


def make_card(**overrides) -> OperationCard:
    now = utc_now()
    defaults = dict(
        card_id="OC-TEST-ATTEST",
        title="attestation card",
        owner="operator-1",
        created_at=now,
        objective="test objective",
        hypothesis="test hypothesis",
        disconfirming_observation="test disconfirming observation",
        ea_reference="EA-TEST",
        profile=ROEProfile.R1_SHIELD,
        collateral_ceiling=CollateralClass.C0,
        autonomy_ceiling=AutonomyClass.AC2_SUPERVISED,
        approver_roles=frozenset({"team_lead"}),
        expires_at=now + timedelta(days=1),
        authorised_targets=("estate:test-service",),
        excluded_targets=("third-party infrastructure without authorisation",),
        threat=ThreatAssessment(
            likelihood=0.6,
            impact=3,
            autonomy_factor=1,
            velocity=1,
            attribution_confidence=0.9,
            attribution_basis="identity attribution at the issuer",
        ),
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
        min_countermeasure_confidence=0.30,
        autonomy_budget=4,
        autonomy_on_call="operator-1",
        autonomy_reversion_trigger="revert on loss of telemetry",
        required_reversibility=Reversibility.REVERSED,
    )
    defaults.update(overrides)
    return OperationCard(**defaults)


def check(result, identifier: str):
    for c in result.checks:
        if c.condition == identifier:
            return c
    raise AssertionError(f"condition {identifier} was not evaluated")


class ClassificationTests(unittest.TestCase):
    def test_the_hybrid_and_human_conditions_are_classified_as_such(self) -> None:
        self.assertEqual(CONDITION_NATURE["AD-3"], "hybrid")
        self.assertEqual(CONDITION_NATURE["AD-6"], "hybrid")
        self.assertEqual(CONDITION_NATURE["AD-10"], "hybrid")
        self.assertEqual(CONDITION_NATURE["AD-12"], "hybrid")
        self.assertEqual(CONDITION_NATURE["AD-5"], "human")

    def test_the_remaining_conditions_are_machine(self) -> None:
        for condition in ("AD-1", "AD-2", "AD-4", "AD-7", "AD-8", "AD-9", "AD-11"):
            self.assertEqual(CONDITION_NATURE[condition], "machine")


class FailClosedDefaultTests(unittest.TestCase):
    """A context that records nothing must refuse, not permit."""

    def test_a_default_context_records_no_class_confidence(self) -> None:
        self.assertEqual(EvaluationContext().class_confidence, 0.0)

    def test_a_default_context_records_no_deconfliction_pass(self) -> None:
        self.assertFalse(EvaluationContext().deconfliction_passed)

    def test_a_default_context_confirms_no_external_authority(self) -> None:
        self.assertFalse(EvaluationContext().external_authority_confirmed)

    def test_a_class_dependent_countermeasure_is_refused_without_a_class_confidence(self) -> None:
        """OCC-37 declares a class attribution dependency.

        With the default context no class confidence has been recorded, and
        the condition must refuse rather than treat an unrecorded confidence
        as full confidence.
        """
        card = make_card(
            profile=ROEProfile.R1_SHIELD,
            authorised_targets=("estate:test-service", "adversary:acct-1"),
            third_party_authorised=True,
            third_party_assessment="a shared tenant depends on this service",
            per_target_authorisations=("adversary:acct-1",),
        )
        result = evaluate(card, get("OCC-37"), EvaluationContext())
        self.assertFalse(check(result, "AD-9").passed)
        self.assertIn("short by", check(result, "AD-9").margin)

    def test_a_class_dependent_countermeasure_passes_with_a_recorded_confidence(self) -> None:
        card = make_card(
            profile=ROEProfile.R1_SHIELD,
            authorised_targets=("estate:test-service", "adversary:acct-1"),
            third_party_authorised=True,
            third_party_assessment="a shared tenant depends on this service",
            per_target_authorisations=("adversary:acct-1",),
        )
        result = evaluate(
            card, get("OCC-37"), EvaluationContext(class_confidence=0.9)
        )
        self.assertTrue(check(result, "AD-9").passed)


class AD3IrreversibilityArgumentTests(unittest.TestCase):
    """A countermeasure with Low or None reversibility needs the argument."""

    def test_a_low_reversibility_countermeasure_needs_the_argument(self) -> None:
        card = make_card()
        result = evaluate(card, get("OCC-36"))  # reversibility NONE
        self.assertFalse(check(result, "AD-3").passed)
        self.assertIn("irreversibility argument", check(result, "AD-3").margin)

    def test_the_argument_satisfies_the_condition(self) -> None:
        # The card's reversibility floor is lowered to NONE so that the
        # argument limb is what is under test, not the floor.
        card = make_card(
            required_reversibility=Reversibility.NONE,
            irreversibility_argument="the elements are irreversible and the reversible alternative is insufficient",
        )
        result = evaluate(card, get("OCC-36"))
        self.assertTrue(check(result, "AD-3").passed)

    def test_a_reversible_countermeasure_does_not_need_the_argument(self) -> None:
        card = make_card()
        result = evaluate(card, get("OCC-01"))  # reversibility REVERSIBLE
        self.assertTrue(check(result, "AD-3").passed)


class AD5PerTargetAuthorisationTests(unittest.TestCase):
    """An outward action needs a specific per-target written authorisation."""

    def _outward_card(self, **overrides) -> OperationCard:
        defaults = dict(
            profile=ROEProfile.R4_DISRUPT,
            collateral_ceiling=CollateralClass.C2,
            approver_roles=frozenset(
                {"director", "legal_contact", "asset_owner", "team_lead"}
            ),
            authorised_targets=("estate:test-service", "adversary:acct-1"),
            third_party_authorised=True,
            third_party_assessment="a shared tenant depends on this service",
        )
        defaults.update(overrides)
        return make_card(**defaults)

    def test_an_outward_action_without_a_per_target_authorisation_is_refused(self) -> None:
        card = self._outward_card(per_target_authorisations=())
        result = evaluate(card, get("OCC-34"))
        self.assertFalse(check(result, "AD-5").passed)
        self.assertIn("per-target written authorisation", check(result, "AD-5").margin)

    def test_an_outward_action_with_a_per_target_authorisation_passes(self) -> None:
        card = self._outward_card(per_target_authorisations=("adversary:acct-1",))
        result = evaluate(card, get("OCC-34"))
        self.assertTrue(check(result, "AD-5").passed)

    def test_a_withheld_countermeasure_is_refused(self) -> None:
        card = self._outward_card(per_target_authorisations=("adversary:acct-1",))
        result = evaluate(card, get("OCC-38"))  # status: Withheld
        self.assertFalse(check(result, "AD-5").passed)
        self.assertIn("withheld determination", check(result, "AD-5").margin)

    def test_a_shared_environment_action_needs_the_tenancy_assessment(self) -> None:
        card = make_card(third_party_assessment="")
        result = evaluate(card, get("OCC-24"))  # inward/outward direction
        self.assertFalse(check(result, "AD-5").passed)
        self.assertIn("shared-tenancy assessment", check(result, "AD-5").margin)


class AD6IndirectEffectTests(unittest.TestCase):
    """A technique that operates on people requires the attestation."""

    def test_a_human_facing_technique_needs_the_attestation(self) -> None:
        card = make_card(techniques=("AAT-3.4",))
        result = evaluate(card, get("OCC-01"))
        self.assertFalse(check(result, "AD-6").passed)
        self.assertIn("indirect-effect attestation", check(result, "AD-6").margin)

    def test_the_attestation_satisfies_the_condition(self) -> None:
        card = make_card(
            techniques=("AAT-3.4",),
            indirect_effect_attestation="the effect on people is indirect; no person is the object",
        )
        result = evaluate(card, get("OCC-01"))
        self.assertTrue(check(result, "AD-6").passed)

    def test_a_card_without_a_human_facing_technique_needs_no_attestation(self) -> None:
        card = make_card(techniques=("AAT-1.1",))
        result = evaluate(card, get("OCC-01"))
        self.assertTrue(check(result, "AD-6").passed)


class AD10DeconflictionAttestationTests(unittest.TestCase):
    """A degraded deconfliction map needs the operator's attestation."""

    def test_a_degraded_map_needs_the_attestation(self) -> None:
        card = make_card(deconfliction_map_current=False)
        result = evaluate(card, get("OCC-01"))
        self.assertFalse(check(result, "AD-10").passed)
        self.assertIn("degraded", check(result, "AD-10").margin)

    def test_the_attestation_satisfies_the_condition(self) -> None:
        card = make_card(
            deconfliction_map_current=False,
            deconfliction_attestation="the conflict has been assessed against a current map",
        )
        result = evaluate(card, get("OCC-01"))
        self.assertTrue(check(result, "AD-10").passed)

    def test_a_current_map_needs_no_attestation(self) -> None:
        card = make_card(deconfliction_map_current=True)
        result = evaluate(card, get("OCC-01"))
        self.assertTrue(check(result, "AD-10").passed)

    def test_a_failed_deconfliction_is_refused_outright(self) -> None:
        card = make_card(
            deconfliction_passed=False,
            deconfliction_map_current=True,
            deconfliction_attestation="the conflict has been assessed",
        )
        result = evaluate(card, get("OCC-01"))
        self.assertFalse(check(result, "AD-10").passed)
        self.assertEqual(check(result, "AD-10").margin, "deconfliction not confirmed")


class AD12NonWeaponisationTests(unittest.TestCase):
    """The catalogue's declaration, or the operator's attestation."""

    def test_a_countermeasure_without_a_declaration_needs_the_attestation(self) -> None:
        cm = replace(get("OCC-01"), non_weaponisation_declared=False)
        card = make_card()
        result = evaluate(card, cm)
        self.assertFalse(check(result, "AD-12").passed)
        self.assertIn("no operator attestation", check(result, "AD-12").margin)

    def test_the_attestation_satisfies_the_condition(self) -> None:
        cm = replace(get("OCC-01"), non_weaponisation_declared=False)
        card = make_card(
            non_weaponisation_attestation="no uninvolved third party is harmed and no model is attacked"
        )
        result = evaluate(card, cm)
        self.assertTrue(check(result, "AD-12").passed)

    def test_the_catalogue_declaration_satisfies_the_condition(self) -> None:
        card = make_card()
        result = evaluate(card, get("OCC-01"))
        self.assertTrue(check(result, "AD-12").passed)

    def test_a_weaponising_countermeasure_cannot_be_constructed(self) -> None:
        with self.assertRaises(ValueError):
            replace(get("OCC-01"), weaponises_model=True)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
