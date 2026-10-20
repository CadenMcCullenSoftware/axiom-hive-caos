"""Tests for the branches the code review found untested.

The review named eleven branches that the code exercised but no test
demonstrated. Each of them is a place where a regression would be silent, and
each is demonstrated here in its failing state or its constrained state.
"""

from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import timedelta

from caos.countermeasures import get
from caos.decision import dispatch
from caos.emergency import EmergencyContext, EmergencyController, EmergencyLevel, EmergencyState, InventoryEntry, PaceEnvelope, ProtocolRefusal
from caos.ledger import Ledger
from caos.models import OperationCard, ThreatAssessment, utc_now
from caos.proving_ground import score_exercise
from caos.roe import evaluate
from caos.vocab import (
    AutonomyClass,
    CollateralClass,
    CountermeasureStatus,
    ROEProfile,
)

NOW = utc_now()


class CountermeasureInvariantTests(unittest.TestCase):
    """The constructor refuses values that violate the framework's invariants."""

    def test_an_unbound_countermeasure_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            replace(get("OCC-01"), techniques=frozenset())

    def test_a_third_party_flag_that_contradicts_the_direction_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            replace(get("OCC-34"), touches_third_party=False)

    def test_a_profile_below_the_class_floor_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            replace(get("OCC-19"), min_profile=ROEProfile.R0_OBSERVE)

    def test_a_withheld_countermeasure_is_constructible(self) -> None:
        """Withheld and retired are legitimate states of a catalogue entry.

        They are refused at the point of use, not at the point of
        construction: a withdrawn entry stays in the catalogue so that
        historical cards remain interpretable.
        """
        cm = replace(get("OCC-01"), status=CountermeasureStatus.WITHHELD)
        self.assertIs(cm.status, CountermeasureStatus.WITHHELD)

    def test_a_withheld_countermeasure_that_is_not_outward_is_refused(self) -> None:
        """The finding that a withheld inward countermeasure was admissible."""
        cm = replace(get("OCC-01"), status=CountermeasureStatus.WITHHELD)
        card = _card()
        result = evaluate(card, cm)
        self.assertFalse(result.admissible)
        self.assertTrue(any(f.condition == "PRE" for f in result.failures))

    def test_a_retired_countermeasure_is_refused(self) -> None:
        cm = replace(get("OCC-01"), status=CountermeasureStatus.RETIRED)
        result = evaluate(_card(), cm)
        self.assertFalse(result.admissible)


class AdmissibleSetTests(unittest.TestCase):
    """The evaluated condition set is exactly the one the model declares."""

    def test_the_evaluated_condition_set_is_exact(self) -> None:
        result = evaluate(_card(), get("OCC-01"))
        evaluated = {c.condition for c in result.checks}
        self.assertEqual(evaluated, {f"AD-{i}" for i in range(1, 13)})

    def test_an_unarmable_card_adds_the_armability_check(self) -> None:
        card = _card(rationale="")
        result = evaluate(card, get("OCC-01"))
        evaluated = {c.condition for c in result.checks}
        self.assertEqual(evaluated, {f"AD-{i}" for i in range(1, 13)} | {"G-3"})

    def test_admissible_is_the_conjunction_of_the_checks(self) -> None:
        for cm in (get("OCC-01"), get("OCC-24"), get("OCC-34")):
            result = evaluate(_card(), cm)
            self.assertEqual(
                result.admissible, all(c.passed for c in result.checks)
            )

    def test_no_condition_is_evaluated_twice(self) -> None:
        result = evaluate(_card(), get("OCC-01"))
        identifiers = [c.condition for c in result.checks]
        self.assertEqual(len(identifiers), len(set(identifiers)))


class ProtectedScopeTests(unittest.TestCase):
    """A target that reaches inside a protected session is refused."""

    def test_a_target_containing_a_protected_session_is_refused(self) -> None:
        protected = _protected()
        from caos.emergency import TargetPosture

        context = EmergencyContext(
            posture=TargetPosture.P_A,
            deployment_principal="agent:app",
            operator_break_glass_working=True,
            blast_boundary=frozenset({"session:operator-console:child"}),
            inventory={
                "session:operator-console:child": InventoryEntry(
                    identifier="session:operator-console:child",
                    owner="agent:app",
                    instance_scoped=True,
                    protected=False,
                )
            },
            protected_controls=protected,
        )
        controller = _emergency_controller(context=context, protected=protected)
        controller.declare(EmergencyLevel.ESL_2, "operator-1")
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-03", actor="operator-1", target="session:operator-console:child")
        self.assertEqual(caught.exception.rule, "ESC-84")

    def test_the_protected_session_itself_is_refused(self) -> None:
        protected = _protected()
        from caos.emergency import TargetPosture

        context = EmergencyContext(
            posture=TargetPosture.P_A,
            deployment_principal="agent:app",
            operator_break_glass_working=True,
            blast_boundary=frozenset({"session:operator-console"}),
            inventory={
                "session:operator-console": InventoryEntry(
                    identifier="session:operator-console",
                    owner="agent:app",
                    instance_scoped=True,
                    protected=False,
                )
            },
            protected_controls=protected,
        )
        controller = _emergency_controller(context=context, protected=protected)
        controller.declare(EmergencyLevel.ESL_2, "operator-1")
        with self.assertRaises(ProtocolRefusal):
            controller.dispatch("EA-A-03", actor="operator-1", target="session:operator-console")


class AuthorityOnStatePathsTests(unittest.TestCase):
    """The verification, transition and level paths require an authority."""

    def setUp(self) -> None:
        self.controller = _emergency_controller()
        self.controller.declare(EmergencyLevel.ESL_2, "operator-1")

    def test_an_unauthorised_verification_is_refused(self) -> None:
        with self.assertRaises(ProtocolRefusal) as caught:
            self.controller.record_verification({"V-1": True}, "independent", "attacker")
        self.assertEqual(caught.exception.rule, "PACE-2")

    def test_an_unauthorised_transition_is_refused(self) -> None:
        with self.assertRaises(ProtocolRefusal) as caught:
            self.controller.transition(EmergencyState.E2_CONTAINED, "attacker")
        self.assertEqual(caught.exception.rule, "PACE-2")

    def test_an_unauthorised_raise_is_refused(self) -> None:
        with self.assertRaises(ProtocolRefusal) as caught:
            self.controller.raise_level(EmergencyLevel.ESL_3, "attacker", "reason")
        self.assertEqual(caught.exception.rule, "PACE-2")

    def test_an_unauthorised_lowering_is_refused(self) -> None:
        with self.assertRaises(ProtocolRefusal) as caught:
            self.controller.lower_level(
                EmergencyLevel.ESL_1, "attacker", "reason", "evidence"
            )
        self.assertEqual(caught.exception.rule, "PACE-2")


class VerificationTests(unittest.TestCase):
    """The kill verification set: complete, twice, and from an independent source."""

    def setUp(self) -> None:
        self.controller = _emergency_controller()
        self.controller.declare(EmergencyLevel.ESL_2, "operator-1")

    def test_a_verification_pass_must_cover_every_check(self) -> None:
        """A pass that omits a check is not a pass.

        The omission is caught when the pass is recorded, by refusing an
        unknown check, and when it is relied upon, because a pass that does
        not cover every check is not complete.
        """
        from caos.emergency import VERIFICATION_CHECKS

        partial = {check: True for check in VERIFICATION_CHECKS[:-1]}
        verification = self.controller.record_verification(
            partial, "independent", "operator-1"
        )
        self.assertFalse(verification.complete)
        self.assertIn(VERIFICATION_CHECKS[-1], verification.failures())
        with self.assertRaises(ProtocolRefusal) as caught:
            self.controller.transition(EmergencyState.E3_VERIFIED, "operator-1")
        self.assertEqual(caught.exception.rule, "ESC-23")

    def test_an_unknown_verification_check_is_refused(self) -> None:
        with self.assertRaises(ProtocolRefusal) as caught:
            self.controller.record_verification(
                {"V-99": True}, "independent", "operator-1"
            )
        self.assertEqual(caught.exception.rule, "ESC-21")

    def test_a_second_pass_is_refused_until_the_first_is_recorded(self) -> None:
        from caos.emergency import VERIFICATION_CHECKS

        complete = {check: True for check in VERIFICATION_CHECKS}
        self.controller.record_verification(complete, "independent", "operator-1")
        with self.assertRaises(ProtocolRefusal) as caught:
            self.controller.transition(EmergencyState.E4_ISOLATED, "operator-1")
        self.assertEqual(caught.exception.rule, "ESC-22")

    def test_a_failed_check_is_a_containment_failure(self) -> None:
        from caos.emergency import VERIFICATION_CHECKS

        failed = {check: True for check in VERIFICATION_CHECKS}
        failed["V-3"] = False
        self.controller.record_verification(failed, "independent", "operator-1")
        with self.assertRaises(ProtocolRefusal) as caught:
            self.controller.transition(EmergencyState.E3_VERIFIED, "operator-1")
        self.assertEqual(caught.exception.rule, "ESC-23")

    def test_a_complete_pass_from_an_independent_source_is_accepted(self) -> None:
        from caos.emergency import VERIFICATION_CHECKS

        complete = {check: True for check in VERIFICATION_CHECKS}
        verification = self.controller.record_verification(
            complete, "independent", "operator-1"
        )
        self.assertTrue(verification.complete)
        self.assertTrue(verification.independent)


class LedgerFailureTests(unittest.TestCase):
    """A dispatch whose record cannot be written is a refusal, not a debit."""

    def test_the_budget_is_not_spent_when_the_ledger_cannot_be_written(self) -> None:
        card = _card()
        before = card.autonomy_consumed

        class Unwritable:
            def append(self, *args, **kwargs):
                raise OSError("the ledger could not be written")

        result = dispatch(card, get("OCC-01"), Unwritable())
        self.assertFalse(result.dispatched)
        self.assertIn("ledger", result.reason.lower())
        self.assertEqual(card.autonomy_consumed, before)

    def test_a_foreign_export_is_refused_with_a_statement(self) -> None:
        for bad in ([], "a string", {"records": "not a list"}, {"manifest": {}}):
            with self.assertRaises(ValueError):
                Ledger.from_export(bad)

    def test_an_export_with_a_foreign_format_is_refused(self) -> None:
        ledger = Ledger()
        ledger.append("signal.ingested", {"n": 1})
        exported = ledger.export()
        exported["format_version"] = "caos.ledger.export/99"
        with self.assertRaises(ValueError):
            Ledger.from_export(exported)

    def test_a_rewritten_chain_no_longer_matches_its_anchor(self) -> None:
        ledger = Ledger()
        ledger.append("signal.ingested", {"n": 1})
        ledger.anchor()
        exported = ledger.export()
        restored = Ledger.from_export(exported)
        self.assertTrue(restored.verify()["intact"])
        # A chain rewritten from the genesis no longer matches the anchor.
        rewritten = Ledger()
        rewritten.append("signal.ingested", {"n": 2})
        rewritten.anchor_head = ledger.anchor_head
        self.assertFalse(rewritten.verify()["intact"])


class AbortAttributionTests(unittest.TestCase):
    """An abort appears in the card's replay."""

    def test_the_abort_is_attributable_to_its_card(self) -> None:
        from caos.demo import build_demo

        floor = build_demo()
        floor.abort("OC-2026-014", "the service degraded")
        timeline = floor.ledger.replay("OC-2026-014")
        self.assertTrue(any(item["kind"] == "abort" for item in timeline))


class ExerciseScoringTests(unittest.TestCase):
    """The exercise score cannot exceed its maximum."""

    def test_a_maximum_below_the_awarded_score_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            score_exercise({"decision quality": 4}, maximum=1)

    def test_a_non_positive_maximum_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            score_exercise({}, maximum=0)


class BlastBoundaryTests(unittest.TestCase):
    """The card's blast boundary is the source of truth."""

    def test_a_card_whose_boundaries_disagree_is_not_armable(self) -> None:
        from caos.emergency import TargetPosture

        context = EmergencyContext(
            posture=TargetPosture.P_A,
            deployment_principal="agent:app",
            operator_break_glass_working=True,
            blast_boundary=frozenset({"session:a"}),
        )
        card = _emergency_card(context=context)
        card.blast_boundary = frozenset({"session:b"})
        defects = card.completion_defects()
        self.assertTrue(any("blast boundary" in d for d in defects))


# -- helpers ---------------------------------------------------------------

def _card(**overrides) -> OperationCard:
    defaults = dict(
        card_id="OC-T",
        title="t",
        owner="operator-1",
        created_at=NOW,
        objective="o",
        hypothesis="h",
        disconfirming_observation="d",
        ea_reference="EA-T",
        profile=ROEProfile.R2_TRAP,
        collateral_ceiling=CollateralClass.C1,
        autonomy_ceiling=AutonomyClass.AC2_SUPERVISED,
        approver_roles=frozenset({"duty_manager", "legal_contact", "team_lead"}),
        expires_at=NOW + timedelta(days=1),
        authorised_targets=("estate:test-service",),
        excluded_targets=("third-party infrastructure without authorisation",),
        threat=ThreatAssessment(
            likelihood=0.6, impact=3, autonomy_factor=1, velocity=1,
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
        rationale="why",
        alternatives_considered=("OCC-01",),
        contingency="abort on degradation",
        contingency_recorded_at=NOW,
        min_countermeasure_confidence=0.30,
        autonomy_budget=4,
        autonomy_on_call="operator-1",
        autonomy_reversion_trigger="revert on loss of telemetry",
    )
    defaults.update(overrides)
    return OperationCard(**defaults)


def _protected():
    from caos.emergency import ProtectedControlSet

    return ProtectedControlSet(
        identities=frozenset({"identity:operator-break-glass"}),
        sessions=frozenset({"session:operator-console"}),
        surfaces=frozenset({"surface:operator-console"}),
        verified_at=NOW,
    )


def _emergency_card(context=None, protected=None):
    from caos.emergency import EmergencyCard, TargetPosture

    boundary = (
        context.blast_boundary if context is not None else frozenset({"session:a"})
    )
    return EmergencyCard(
        incident_id="INC-T",
        operator="operator-1",
        target_principal="agent:app",
        posture=TargetPosture.P_A,
        blast_boundary=boundary,
        context=context,
        protected_controls=protected if protected is not None else _protected(),
        command_authority_holder="operator-1",
        break_glass_tested=True,
        break_glass_passed=True,
        break_glass_tested_at=NOW,
        break_glass_tested_by="operator-1",
        ea_reference="EA-T",
        objective="contain",
        hypothesis="the capability is reachable through its own session",
        disconfirming_observation="the capability survives",
        excluded_targets=("other tenants",),
        risk_of_inaction="the capability is retained",
        alternatives_considered=("wait",),
        abort_conditions=("the operator's access breaks",),
        abort_owner="operator-1",
        abort_mechanism="single-key abort",
        contingency="restore from the break-glass path",
        contingency_recorded_at=NOW,
        deconfliction_passed=True,
        third_party_assessment="a shared tenant depends on it",
        approver_roles=frozenset({"team_lead"}),
        non_weaponisation_attestation="no model is attacked",
        approved_by="operator-1",
    )


def _emergency_controller(context=None, protected=None):
    if context is None:
        from caos.emergency import TargetPosture

        context = EmergencyContext(
            posture=TargetPosture.P_A,
            deployment_principal="agent:app",
            operator_break_glass_working=True,
            blast_boundary=frozenset({"session:a"}),
            inventory={
                "session:a": InventoryEntry(
                    identifier="session:a",
                    owner="agent:app",
                    instance_scoped=True,
                    protected=False,
                )
            },
        )
    card = _emergency_card(context=context, protected=protected)
    pace = PaceEnvelope(
        reference="PACE-T",
        issued_to=frozenset({"operator-1"}),
        issued_at=NOW - timedelta(days=1),
        expires_at=NOW + timedelta(days=1),
    )
    return EmergencyController(card, pace, now=NOW)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
