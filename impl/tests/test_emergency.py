"""Tests for the emergency shutdown and containment protocol's enforceable core.

The tests exercise the mechanical half of the protocol: the severity ladder,
the state machine, the pre-flight gate, the protected control set, the
zero-collateral checks, the containment envelope, the verification gate, the
staged-rotation rule, and the hard prohibitions.

Run from the set root with:

    python3 -m unittest discover -s "AI C@ Op/impl/tests" -t "AI C@ Op/impl"
"""

from __future__ import annotations

import os
import sys
import unittest
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from caos.emergency import (  # noqa: E402
    ACTIONS,
    REENTRY_CRITERIA,
    EmergencyCard,
    EmergencyController,
    EmergencyLevel,
    EmergencyState,
    InventoryEntry,
    PaceEnvelope,
    ProtocolRefusal,
    ProtectedControlSet,
    RotationState,
    SeverityIndicators,
    TargetPosture,
    VERIFICATION_CHECKS,
    action,
    classify_level,
    collateral_checks,
    preflight,
)

PRINCIPAL = "grok-agent-01"

INVENTORY = {
    "session:a1": InventoryEntry("session:a1", PRINCIPAL),
    "session:b2": InventoryEntry("session:b2", PRINCIPAL),
    "key:k3": InventoryEntry("key:k3", PRINCIPAL),
    "container:c4": InventoryEntry("container:c4", PRINCIPAL),
    "console:emergency": InventoryEntry("console:emergency", "caos-platform", protected=True),
    "session:operator": InventoryEntry("session:operator", "operator", protected=True),
    "session:otheruser": InventoryEntry("session:otheruser", "another-principal"),
    "tenant:acme": InventoryEntry("tenant:acme", PRINCIPAL, instance_scoped=False),
}

PROTECTED = ProtectedControlSet(
    identities=frozenset({"operator-principal", "caos-platform"}),
    sessions=frozenset({"session:operator"}),
    surfaces=frozenset({"console:emergency", "ledger", "notification-path"}),
)

NOW = datetime(2026, 10, 20, 12, 0, 0, tzinfo=timezone.utc)


def make_context(**overrides):
    from caos.emergency import EmergencyContext

    base = dict(
        posture=TargetPosture.P_A,
        deployment_principal=PRINCIPAL,
        blast_boundary=frozenset({"session:a1", "session:b2", "key:k3", "container:c4"}),
        operator_break_glass_working=True,
        evidence_captured=True,
        blast_preview_shown=True,
        command_authority_holder="operator",
        command_authority_intact=True,
        inventory=INVENTORY,
        protected_controls=PROTECTED,
    )
    base.update(overrides)
    return EmergencyContext(**base)


def make_card(level=EmergencyLevel.ESL_2, context=None, protected=PROTECTED, holder="operator"):
    card = EmergencyCard(
        incident_id="INC-001",
        operator="operator",
        target_principal=PRINCIPAL,
        posture=TargetPosture.P_A,
        blast_boundary=frozenset({"session:a1", "session:b2", "key:k3", "container:c4"}),
        context=context if context is not None else make_context(),
        protected_controls=protected,
        command_authority_holder=holder,
        break_glass_tested=True,
        break_glass_passed=True,
        break_glass_tested_at=NOW,
        break_glass_tested_by=holder,
        # The standard card's authorisation instruments. The emergency path
        # is the fastest path the operator has, which is why it carries the
        # same instruments as every other path.
        ea_reference="EA-2026-004",
        objective="contain the compromised deployment without harming the operator",
        hypothesis="the deployment's capability is reachable through its own session",
        disconfirming_observation="the capability survives termination of the session",
        excluded_targets=("all other tenants", "the provider's service"),
        risk_of_inaction="the compromised deployment retains access to the operator's data",
        alternatives_considered=("wait for the provider", "restore from backup"),
        abort_conditions=("the operator's own access is broken",),
        abort_owner=holder,
        abort_mechanism="single-key abort on the emergency console",
        contingency="restore the operator's session from the break-glass path",
        contingency_recorded_at=NOW,
        deconfliction_passed=True,
        third_party_assessment="a shared tenant depends on the affected service",
        approver_roles=frozenset({"team_lead"}),
        non_weaponisation_attestation=(
            "no model is attacked, and no uninvolved third party is harmed"
        ),
        approved_by=holder,
    )
    return card


def make_controller(level=EmergencyLevel.ESL_2, context=None, protected=PROTECTED, holder="operator"):
    card = make_card(level=level, context=context, protected=protected, holder=holder)
    pace = PaceEnvelope(
        reference="PACE-2026-10",
        issued_to=frozenset({"operator", "alternate"}),
        issued_at=NOW - timedelta(days=1),
        expires_at=NOW + timedelta(days=30),
    )
    controller = EmergencyController(card, pace, now=NOW)
    controller.declare(level, actor="operator")
    return controller


def advance_to_verified(controller):
    """Take a controller to E3, where recovery actions may be dispatched."""
    results = {check: True for check in VERIFICATION_CHECKS}
    controller.transition(EmergencyState.E2_CONTAINED, actor="operator")
    controller.record_verification(results, source="independent", actor="operator")
    controller.transition(EmergencyState.E3_VERIFIED, actor="operator")
    return controller


class TestSeverityLadder(unittest.TestCase):
    def test_indicator_only_is_esl_1(self):
        self.assertEqual(
            classify_level(SeverityIndicators(indicator_only=True)),
            EmergencyLevel.ESL_1,
        )

    def test_unauthorised_action_is_esl_2(self):
        self.assertEqual(
            classify_level(SeverityIndicators(unauthorised_action=True)),
            EmergencyLevel.ESL_2,
        )

    def test_exposure_is_esl_3(self):
        for indicator in ("data_left_boundary", "credentials_exposed", "persistence_established"):
            with self.subTest(indicator=indicator):
                self.assertEqual(
                    classify_level(SeverityIndicators(**{indicator: True})),
                    EmergencyLevel.ESL_3,
                )

    def test_control_surface_and_manipulation_are_esl_4(self):
        for indicator in (
            "control_plane_tampered",
            "operator_manipulation",
            "persistence_attempted",
            "containment_failed",
        ):
            with self.subTest(indicator=indicator):
                self.assertEqual(
                    classify_level(SeverityIndicators(**{indicator: True})),
                    EmergencyLevel.ESL_4,
                )

    def test_escalating_evidence_dominates(self):
        self.assertEqual(
            classify_level(
                SeverityIndicators(unauthorised_action=True, data_left_boundary=True)
            ),
            EmergencyLevel.ESL_3,
        )

    def test_declaring_below_the_evidence_is_refused(self):
        controller = EmergencyController(
            make_card(), PaceEnvelope("P", frozenset({"operator"}), NOW, NOW + timedelta(days=1)), now=NOW
        )
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.declare(
                EmergencyLevel.ESL_2,
                actor="operator",
                indicators=SeverityIndicators(operator_manipulation=True),
            )
        self.assertEqual(caught.exception.rule, "ESC-7")


class TestStateMachine(unittest.TestCase):
    def test_declaration_moves_to_e1(self):
        controller = make_controller()
        self.assertEqual(controller.card.state, EmergencyState.E1_DECLARED)

    def test_e0_to_e2_is_not_a_permitted_shortcut(self):
        controller = EmergencyController(
            make_card(), PaceEnvelope("P", frozenset({"operator"}), NOW, NOW + timedelta(days=1)), now=NOW
        )
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.transition(EmergencyState.E2_CONTAINED, actor="operator")
        self.assertEqual(caught.exception.rule, "ESC-11")

    def test_e3_requires_a_verification_pass(self):
        controller = make_controller()
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.transition(EmergencyState.E3_VERIFIED, actor="operator")
        self.assertEqual(caught.exception.rule, "ESC-22")

    def test_e3_requires_a_complete_independent_pass(self):
        controller = make_controller()
        results = {check: True for check in VERIFICATION_CHECKS}
        results["V-6"] = False
        controller.record_verification(results, source="independent", actor="operator")
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.transition(EmergencyState.E3_VERIFIED, actor="operator")
        self.assertEqual(caught.exception.rule, "ESC-23")

    def test_a_non_independent_pass_does_not_count(self):
        controller = make_controller()
        results = {check: True for check in VERIFICATION_CHECKS}
        controller.record_verification(results, source="deployment", actor="operator")
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.transition(EmergencyState.E3_VERIFIED, actor="operator")
        self.assertEqual(caught.exception.rule, "ESC-24")

    def test_e4_requires_two_passes(self):
        controller = make_controller()
        results = {check: True for check in VERIFICATION_CHECKS}
        controller.transition(EmergencyState.E2_CONTAINED, actor="operator")
        controller.record_verification(results, source="independent", actor="operator")
        controller.transition(EmergencyState.E3_VERIFIED, actor="operator")
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.transition(EmergencyState.E4_ISOLATED, actor="operator")
        self.assertEqual(caught.exception.rule, "ESC-22")
        controller.record_verification(results, source="independent", actor="operator")
        controller.transition(EmergencyState.E4_ISOLATED, actor="operator")
        self.assertEqual(controller.card.state, EmergencyState.E4_ISOLATED)

    def test_recovery_requires_the_reentry_criteria(self):
        controller = make_controller()
        results = {check: True for check in VERIFICATION_CHECKS}
        controller.transition(EmergencyState.E2_CONTAINED, actor="operator")
        controller.record_verification(results, source="independent", actor="operator")
        controller.transition(EmergencyState.E3_VERIFIED, actor="operator")
        controller.record_verification(results, source="independent", actor="operator")
        controller.transition(EmergencyState.E4_ISOLATED, actor="operator")
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.transition(EmergencyState.E5_RECOVERED, actor="operator")
        self.assertEqual(caught.exception.rule, "ESC-56")
        self.assertIn("R-2", controller.reentry_blockers())
        for criterion in REENTRY_CRITERIA:
            controller.mark_reentry(criterion, True)
        self.assertEqual(controller.reentry_blockers(), ())
        controller.transition(EmergencyState.E5_RECOVERED, actor="operator")
        self.assertEqual(controller.card.state, EmergencyState.E5_RECOVERED)


class TestPreflightGate(unittest.TestCase):
    def test_instance_scoped_owned_target_passes(self):
        results = preflight("session:a1", INVENTORY, PRINCIPAL, PROTECTED)
        self.assertTrue(all(result.passed for result in results))

    def test_collective_target_is_refused(self):
        results = preflight("tenant:acme", INVENTORY, PRINCIPAL, PROTECTED)
        self.assertFalse(results[0].passed)
        self.assertEqual(results[0].identifier, "PF-1")

    def test_wildcard_target_is_refused(self):
        results = preflight("session:*", INVENTORY, PRINCIPAL, PROTECTED)
        self.assertFalse(results[0].passed)

    def test_target_owned_by_another_principal_is_refused(self):
        results = preflight("session:otheruser", INVENTORY, PRINCIPAL, PROTECTED)
        self.assertFalse(results[1].passed)
        self.assertEqual(results[1].identifier, "PF-2")

    def test_unresolvable_target_fails_closed(self):
        results = preflight("session:does-not-exist", INVENTORY, PRINCIPAL, PROTECTED)
        self.assertFalse(results[0].passed)

    def test_protected_target_is_refused(self):
        results = preflight("session:operator", INVENTORY, PRINCIPAL, PROTECTED)
        self.assertFalse(results[2].passed)
        self.assertEqual(results[2].identifier, "PF-3")

    def test_dispatch_to_a_protected_session_is_refused(self):
        controller = make_controller()
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-05", actor="operator", target="session:operator")
        self.assertEqual(caught.exception.rule, "ESC-84")

    def test_dispatch_to_the_console_is_refused(self):
        controller = make_controller()
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-11", actor="operator", target="console:emergency")
        self.assertEqual(caught.exception.rule, "ESC-84")

    def test_dispatch_to_a_collective_target_is_refused(self):
        controller = make_controller()
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-05", actor="operator", target="tenant:acme")
        self.assertEqual(caught.exception.rule, "ESC-84")

    def test_dispatch_to_another_users_session_is_refused(self):
        controller = make_controller()
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-03", actor="operator", target="session:otheruser")
        self.assertEqual(caught.exception.rule, "ESC-84")


class TestProtectedControlSet(unittest.TestCase):
    def test_card_cannot_be_armed_without_the_set(self):
        card = make_card(protected=ProtectedControlSet.empty())
        defects = card.completion_defects()
        self.assertTrue(any("protected control set" in defect for defect in defects))

    def test_card_cannot_be_armed_without_a_command_holder(self):
        card = make_card(holder="")
        defects = card.completion_defects()
        self.assertTrue(any("command-authority holder" in defect for defect in defects))

    def test_card_arms_when_the_command_block_is_present(self):
        card = make_card()
        self.assertTrue(card.armed())

    def test_the_set_is_not_mutated_by_amendment(self):
        amended = PROTECTED.amend(
            actor="operator", reason="new console instance", identities=("new-console",)
        )
        self.assertIn("new-console", amended.identities)
        self.assertNotIn("new-console", PROTECTED.identities)

    def test_amendment_requires_a_named_human_and_a_reason(self):
        with self.assertRaises(ProtocolRefusal):
            PROTECTED.amend(actor="", reason="something")
        with self.assertRaises(ProtocolRefusal):
            PROTECTED.amend(actor="operator", reason="")

    def test_intersection_names_the_element(self):
        self.assertEqual(
            PROTECTED.intersect(["session:operator", "session:a1"]),
            ("session:operator",),
        )


class TestNoAiObtainsControl(unittest.TestCase):
    def test_a_granting_action_is_refused(self):
        controller = make_controller()
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-03", actor="operator", target="grant:session")
        self.assertEqual(caught.exception.rule, "ESC-84")

    def test_a_minting_target_is_refused_by_the_checklist(self):
        act = action("EA-A-03")
        checks = collateral_checks(act, make_context(), target="mint:key:new")
        failed = [check for check in checks if not check.passed]
        self.assertTrue(any(check.identifier == "K-14" for check in failed))

    def test_no_catalogue_action_grants_control(self):
        for act in ACTIONS:
            with self.subTest(action=act.identifier):
                self.assertFalse(act.grants_ai_control)
                self.assertFalse(act.targets_command_path)
                self.assertFalse(act.revokes_command_authority)


class TestZeroCollateralChecks(unittest.TestCase):
    def test_shared_tenancy_action_is_refused(self):
        act = action("EA-A-02")
        checks = collateral_checks(act, make_context(shared_tenancy=True), target="key:k3")
        failed = [check for check in checks if not check.passed]
        self.assertTrue(any(check.identifier == "K-3" for check in failed))

    def test_operator_access_action_needs_a_working_break_glass(self):
        act = action("EA-A-12")
        checks = collateral_checks(act, make_context(operator_break_glass_working=False), target="session:a1")
        failed = [check for check in checks if not check.passed]
        self.assertTrue(any(check.identifier == "K-6" for check in failed))

    def test_irreversible_action_needs_captured_evidence(self):
        act = action("EA-A-19")
        checks = collateral_checks(act, make_context(evidence_captured=False), target="container:c4")
        failed = [check for check in checks if not check.passed]
        self.assertTrue(any(check.identifier == "K-7" for check in failed))

    def test_untrusted_authorisation_is_refused(self):
        act = action("EA-A-03")
        checks = collateral_checks(act, make_context(authorisation_source="deployment"), target="key:k3")
        failed = [check for check in checks if not check.passed]
        self.assertTrue(any(check.identifier == "K-10" for check in failed))

    def test_a_device_damaging_action_needs_a_recovery_card(self):
        act = action("EA-A-19")
        checks = collateral_checks(act, make_context(), target="container:c4")
        failed = [check for check in checks if not check.passed]
        self.assertTrue(any(check.identifier == "K-5" for check in failed))
        self.assertTrue(any(check.identifier == "K-8" for check in failed))
        checks = collateral_checks(
            act, make_context(recovery_card_open=True), target="container:c4"
        )
        failed = [check for check in checks if not check.passed]
        self.assertFalse(any(check.identifier == "K-5" for check in failed))
        self.assertFalse(any(check.identifier == "K-8" for check in failed))

    def test_a_clean_context_passes_every_check(self):
        act = action("EA-A-03")
        checks = collateral_checks(act, make_context(), target="key:k3")
        self.assertTrue(all(check.passed for check in checks))
        self.assertEqual(len(checks), 16)


class TestContainmentEnvelope(unittest.TestCase):
    def test_envelope_action_is_dispatchable_at_esl_2(self):
        controller = make_controller(EmergencyLevel.ESL_2)
        record = controller.dispatch("EA-A-03", actor="operator", target="key:k3")
        self.assertTrue(record.in_pace)

    def test_envelope_is_unavailable_at_esl_1(self):
        controller = make_controller(EmergencyLevel.ESL_1)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-03", actor="operator", target="key:k3")
        self.assertEqual(caught.exception.rule, "PACE-1")

    def test_expired_envelope_is_refused(self):
        card = make_card()
        pace = PaceEnvelope("P", frozenset({"operator"}), NOW - timedelta(days=2), NOW - timedelta(days=1))
        controller = EmergencyController(card, pace, now=NOW)
        controller.declare(EmergencyLevel.ESL_2, actor="operator")
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-03", actor="operator", target="key:k3")
        self.assertEqual(caught.exception.rule, "PACE-6")

    def test_invocation_limit_is_enforced(self):
        card = make_card()
        pace = PaceEnvelope(
            "P",
            frozenset({"operator"}),
            NOW - timedelta(days=1),
            NOW + timedelta(days=1),
            max_invocations=2,
        )
        controller = EmergencyController(card, pace, now=NOW)
        controller.declare(EmergencyLevel.ESL_2, actor="operator")
        controller.dispatch("EA-A-03", actor="operator", target="key:k3")
        controller.dispatch("EA-A-04", actor="operator", target="session:a1")
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-07", actor="operator", target="container:c4")
        self.assertEqual(caught.exception.rule, "PACE-2")

    def test_action_outside_the_envelope_needs_an_approver(self):
        context = make_context(recovery_card_open=True)
        controller = make_controller(EmergencyLevel.ESL_3, context=context)
        advance_to_verified(controller)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-19", actor="operator", target="container:c4")
        self.assertEqual(caught.exception.rule, "ESC-50")

    def test_an_authorised_recovery_action_dispatches_outside_the_envelope(self):
        context = make_context(recovery_card_open=True)
        controller = make_controller(EmergencyLevel.ESL_3, context=context)
        advance_to_verified(controller)
        record = controller.dispatch(
            "EA-A-19", actor="operator", second_approver="legal", target="container:c4"
        )
        self.assertFalse(record.in_pace)

    def test_recovery_actions_are_refused_before_verification(self):
        controller = make_controller(EmergencyLevel.ESL_3)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch(
                "EA-A-19", actor="operator", second_approver="legal", target="container:c4"
            )
        self.assertEqual(caught.exception.rule, "ESC-19")


class TestStagedRotation(unittest.TestCase):
    def test_invalidation_before_issue_is_refused(self):
        rotation = RotationState()
        with self.assertRaises(ProtocolRefusal) as caught:
            rotation.invalidate()
        self.assertEqual(caught.exception.rule, "ESC-33")

    def test_the_full_sequence_is_accepted(self):
        rotation = RotationState()
        rotation.issued = True
        rotation.verified = True
        rotation.workload_moved = True
        rotation.invalidate()
        self.assertTrue(rotation.invalidated)

    def test_rotation_action_requires_the_staged_state(self):
        # The rotation is an identity action, so the card must record that a
        # credential exposure is what the rotation is answering.
        context = make_context(operator_credential_exposed=True)
        controller = make_controller(EmergencyLevel.ESL_3, context=context)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-14", actor="operator", target="key:k3")
        self.assertEqual(caught.exception.rule, "ESC-33")

    def test_a_completed_rotation_may_be_dispatched(self):
        context = make_context(operator_credential_exposed=True)
        controller = make_controller(EmergencyLevel.ESL_3, context=context)
        controller.begin_rotation("EA-A-14", actor="operator")
        controller.verify_rotation("EA-A-14", actor="operator")
        controller.move_workload("EA-A-14", actor="operator")
        record = controller.dispatch("EA-A-14", actor="operator", target="key:k3")
        self.assertEqual(record.action_id, "EA-A-14")


class TestPostureCeilings(unittest.TestCase):
    def test_c1_action_is_refused_under_a_shared_service_posture(self):
        context = make_context(posture=TargetPosture.P_C)
        controller = make_controller(EmergencyLevel.ESL_3, context=context)
        advance_to_verified(controller)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch(
                "EA-A-19", actor="operator", second_approver="legal", target="container:c4"
            )
        self.assertEqual(caught.exception.rule, "ESC-3")

    def test_recovery_tier_is_refused_under_a_hosted_service_posture(self):
        context = make_context(posture=TargetPosture.P_D)
        controller = make_controller(EmergencyLevel.ESL_3, context=context)
        advance_to_verified(controller)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch(
                "EA-A-18", actor="operator", second_approver="legal", target="container:c4"
            )
        self.assertEqual(caught.exception.rule, "ESC-3")

    def test_a_downgraded_posture_binds_actions_already_in_flight(self):
        context = make_context(posture=TargetPosture.P_C)
        controller = make_controller(EmergencyLevel.ESL_3, context=context)
        advance_to_verified(controller)
        with self.assertRaises(ProtocolRefusal):
            controller.dispatch(
                "EA-A-19", actor="operator", second_approver="legal", target="container:c4"
            )
        upgraded = make_context(posture=TargetPosture.P_A, recovery_card_open=True)
        controller.card.context = upgraded
        record = controller.dispatch(
            "EA-A-19", actor="operator", second_approver="legal", target="container:c4"
        )
        self.assertFalse(record.in_pace)


class TestKillAction(unittest.TestCase):
    def test_the_kill_is_one_action_and_needs_no_second_approver(self):
        controller = make_controller(EmergencyLevel.ESL_4)
        record = controller.dispatch("EA-A-KILL", actor="operator", target="container:c4")
        self.assertTrue(record.in_pace)
        self.assertEqual(record.actor, "operator")

    def test_the_kill_is_refused_when_it_would_touch_the_command_path(self):
        controller = make_controller(EmergencyLevel.ESL_4)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-KILL", actor="operator", target="console:emergency")
        self.assertEqual(caught.exception.rule, "ESC-84")

    def test_the_kill_is_refused_before_the_emergency_is_declared(self):
        card = make_card()
        pace = PaceEnvelope("P", frozenset({"operator"}), NOW, NOW + timedelta(days=1))
        controller = EmergencyController(card, pace, now=NOW)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-KILL", actor="operator", target="container:c4")
        self.assertEqual(caught.exception.rule, "ESC-11")


class TestProhibitions(unittest.TestCase):
    def test_prohibited_operations_are_declared(self):
        from caos.emergency import PROHIBITED_OPERATIONS

        for operation in (
            "delete_user_data",
            "revoke_operator_command_authority",
            "suspend_the_c2_surface",
            "transfer_command_authority_to_a_model",
            "disable_the_emergency_console",
            "act_on_provider_service",
        ):
            with self.subTest(operation=operation):
                self.assertIn(operation, PROHIBITED_OPERATIONS)


if __name__ == "__main__":
    unittest.main()
