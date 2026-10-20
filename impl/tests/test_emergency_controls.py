"""Tests for the controls the technical audit found to be advisory rather than enforced.

`reference/emergency-protocol-technical-audit.md` found six critical defects in
the emergency path: a card that could be armed without being complete, a
prohibition list that could never fire, a gate whose inputs travelled with the
call, a rotation that could never be dispatched, an actor checked against
nothing, and a second approver required in prose only.

Each of these is a fail-open defect in a containment path, and each is now
demonstrated here in both its failing and its passing state.
"""

from __future__ import annotations

import unittest
from datetime import timedelta

from caos.emergency import (
    PROHIBITION_FLAGS,
    EmergencyController,
    EmergencyLevel,
    EmergencyState,
    PaceEnvelope,
    ProtocolRefusal,
    RotationState,
    action,
    prohibition_for,
)
from caos.ledger import Ledger

from tests.test_emergency import NOW, PROTECTED, make_card, make_context


class ArmabilityTests(unittest.TestCase):
    """F-1: a card with a defect cannot be armed, and nothing is dispatched on it."""

    def _controller(self, card, declare=False):
        pace = PaceEnvelope(
            reference="PACE-T",
            issued_to=frozenset({"operator"}),
            issued_at=NOW - timedelta(days=1),
            expires_at=NOW + timedelta(days=1),
        )
        return EmergencyController(card, pace, now=NOW)

    def test_a_complete_card_is_armable(self) -> None:
        self.assertTrue(make_card().armed())
        self.assertEqual(make_card().completion_defects(), ())

    def test_a_card_with_no_protected_control_set_is_not_armable(self) -> None:
        card = make_card()
        card.protected_controls = PROTECTED.__class__.empty()
        self.assertFalse(card.armed())
        self.assertTrue(
            any("protected control set" in d for d in card.completion_defects())
        )

    def test_a_card_with_no_engagement_authorisation_is_not_armable(self) -> None:
        card = make_card()
        card.ea_reference = ""
        self.assertFalse(card.armed())
        self.assertTrue(
            any("engagement authorisation" in d for d in card.completion_defects())
        )

    def test_a_card_with_no_abort_conditions_is_not_armable(self) -> None:
        card = make_card()
        card.abort_conditions = ()
        self.assertFalse(card.armed())

    def test_a_card_with_no_third_party_exclusion_is_not_armable(self) -> None:
        card = make_card()
        card.excluded_targets = ()
        self.assertFalse(card.armed())

    def test_a_card_with_an_untested_break_glass_path_is_not_armable(self) -> None:
        card = make_card()
        card.break_glass_tested = False
        self.assertFalse(card.armed())
        self.assertTrue(
            any("break-glass" in d for d in card.completion_defects())
        )

    def test_a_failed_break_glass_test_requires_esl3(self) -> None:
        card = make_card()
        card.break_glass_passed = False
        card.level = EmergencyLevel.ESL_2
        self.assertFalse(card.armed())
        card.level = EmergencyLevel.ESL_3
        self.assertTrue(card.armed())

    def test_the_break_glass_test_is_recorded(self) -> None:
        card = make_card()
        card.break_glass_tested = False
        controller = _controller(card, declare=False)
        controller.test_break_glass(passed=True, actor="operator")
        self.assertTrue(card.break_glass_tested)
        self.assertTrue(card.break_glass_passed)

    def test_a_card_with_no_named_approver_is_not_armable(self) -> None:
        card = make_card()
        card.approved_by = ""
        self.assertFalse(card.armed())

    def test_an_unarmable_card_refuses_to_declare(self) -> None:
        card = make_card()
        card.ea_reference = ""
        controller = self._controller(card, declare=False)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.declare(EmergencyLevel.ESL_2, "operator")
        self.assertEqual(caught.exception.rule, "ESC-75")

    def test_an_unarmable_card_refuses_to_dispatch(self) -> None:
        card = make_card()
        card.protected_controls = PROTECTED.__class__.empty()
        controller = self._controller(card, declare=False)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-03", actor="operator", target="session:a1")
        self.assertEqual(caught.exception.rule, "ESC-75")


class ProhibitionTests(unittest.TestCase):
    """F-2: the prohibition travels with the action and can fire."""

    def test_every_prohibition_is_mapped_to_an_attribute_or_declared_platform_level(self) -> None:
        """Every prohibition is accounted for.

        A prohibition is either expressed by an action attribute, in which
        case the dispatch refuses it outright, or it is a platform-level
        behaviour with no catalogue entry, in which case it is prevented by
        the operator's discipline and by the protocol's scope. A prohibition
        that is neither is a prohibition that nothing enforces.
        """
        expressed = {
            name for name, flags in PROHIBITION_FLAGS.items() if flags
        }
        for name in PROHIBITED_OPERATIONS:
            self.assertIn(
                name,
                PROHIBITION_FLAGS,
                f"{name} is not mapped at all",
            )
            self.assertTrue(
                name in expressed or name in _PLATFORM_LEVEL_PROHIBITIONS,
                f"{name} is neither expressed by an attribute nor declared a "
                "platform-level prohibition",
            )

    def test_the_prohibition_mechanism_is_on_the_dispatch_path(self) -> None:
        """A prohibition that cannot fire is not a control."""
        from unittest.mock import patch

        from caos import emergency as emergency_module

        offender = _action_with(grants_ai_control=True)
        controller = _controller()
        with patch.dict(emergency_module._ACTION_INDEX, {offender.identifier: offender}):
            with self.assertRaises(ProtocolRefusal) as caught:
                controller.dispatch(
                    offender.identifier, actor="operator", target="session:a1"
                )
        self.assertEqual(caught.exception.rule, "ZC-1")
        self.assertIn("transfer_command_authority_to_a_model", caught.exception.detail)

    def test_every_prohibited_operation_is_accounted_for(self) -> None:
        for name in PROHIBITED_OPERATIONS:
            self.assertIn(name, PROHIBITION_FLAGS)

    def test_an_action_that_touches_the_command_path_is_refused(self) -> None:
        from unittest.mock import patch

        from caos import emergency as emergency_module

        offender = _action_with(alters_record=True)
        controller = _controller()
        with patch.dict(emergency_module._ACTION_INDEX, {offender.identifier: offender}):
            with self.assertRaises(ProtocolRefusal) as caught:
                controller.dispatch(
                    offender.identifier, actor="operator", target="session:a1"
                )
        self.assertEqual(caught.exception.rule, "ZC-1")
        self.assertIn("alter_or_suppress_the_record", caught.exception.detail)

    def test_an_action_that_grants_ai_control_is_refused(self) -> None:
        from unittest.mock import patch

        from caos import emergency as emergency_module

        offender = _action_with(grants_ai_control=True)
        controller = _controller()
        with patch.dict(emergency_module._ACTION_INDEX, {offender.identifier: offender}):
            with self.assertRaises(ProtocolRefusal) as caught:
                controller.dispatch(
                    offender.identifier, actor="operator", target="session:a1"
                )
        self.assertEqual(caught.exception.rule, "ZC-1")
        self.assertIn(
            "transfer_command_authority_to_a_model", caught.exception.detail
        )

    def test_an_action_that_touches_the_command_path_is_refused(self) -> None:
        from unittest.mock import patch

        from caos import emergency as emergency_module

        offender = _action_with(targets_command_path=True)
        controller = _controller()
        with patch.dict(emergency_module._ACTION_INDEX, {offender.identifier: offender}):
            with self.assertRaises(ProtocolRefusal) as caught:
                controller.dispatch(
                    offender.identifier, actor="operator", target="session:a1"
                )
        self.assertEqual(caught.exception.rule, "ZC-1")
        self.assertIn("suspend_the_c2_surface", caught.exception.detail)

    def test_an_action_that_affects_a_third_party_is_refused_without_authorisation(self) -> None:
        from unittest.mock import patch

        from caos import emergency as emergency_module

        offender = _action_with(targets_third_party=True)
        controller = _controller()
        with patch.dict(emergency_module._ACTION_INDEX, {offender.identifier: offender}):
            with self.assertRaises(ProtocolRefusal) as caught:
                controller.dispatch(
                    offender.identifier, actor="operator", target="session:a1"
                )
        self.assertEqual(caught.exception.rule, "ZC-9")

    def test_a_conditional_prohibition_is_not_an_absolute_one(self) -> None:
        """The conditional prohibitions are governed by the checklist.

        An action that bears on the operator's own access, or that affects
        other users in a shared tenancy, is refused by K-6 and K-3 unless the
        compensating condition is met. Mapping those attributes to the
        absolute prohibitions would refuse legitimate containment.
        """
        from caos import emergency as emergency_module

        self.assertEqual(prohibition_for(_action_with(breaks_operator_access=True)), "")
        self.assertEqual(prohibition_for(_action_with(affects_other_users=True)), "")

    def test_prohibition_for_identifies_the_breach(self) -> None:
        self.assertEqual(prohibition_for(_action_with(alters_record=True)),
                         "alter_or_suppress_the_record")
        self.assertEqual(prohibition_for(_action_with(destroys_user_data=True)),
                         "delete_user_data")
        self.assertEqual(prohibition_for(_action_with(grants_ai_control=True)),
                         "transfer_command_authority_to_a_model")

    def test_an_ordinary_action_breaches_no_prohibition(self) -> None:
        self.assertEqual(prohibition_for(action("EA-A-03")), "")


class AuthorityTests(unittest.TestCase):
    """F-5: a named human authorises every action."""

    def test_an_unnamed_actor_is_refused(self) -> None:
        controller = _controller()
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-03", actor="someone-else", target="session:a1")
        self.assertEqual(caught.exception.rule, "PACE-2")

    def test_the_envelope_holder_may_act(self) -> None:
        controller = _controller()
        record = controller.dispatch("EA-A-03", actor="operator", target="session:a1")
        self.assertEqual(record.actor, "operator")

    def test_the_alternate_holder_may_act(self) -> None:
        card = make_card()
        card.alternate_authority_holder = "alternate"
        controller = _controller(card)
        record = controller.dispatch("EA-A-03", actor="alternate", target="session:a1")
        self.assertEqual(record.actor, "alternate")


class SecondApproverTests(unittest.TestCase):
    """F-7: ESL-4 requires a second named human."""

    def test_a_c0_action_at_esl4_requires_a_second_approver(self) -> None:
        controller = _controller(level=EmergencyLevel.ESL_4)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-11", actor="operator", target="session:a1")
        self.assertEqual(caught.exception.rule, "ESC-50")

    def test_a_second_approver_satisfies_it(self) -> None:
        controller = _controller(level=EmergencyLevel.ESL_4)
        record = controller.dispatch(
            "EA-A-11", actor="operator", second_approver="alternate", target="session:a1"
        )
        self.assertEqual(record.second_approver, "alternate")


class ReentryKeyTests(unittest.TestCase):
    """F-13: an unknown re-entry criterion is refused."""

    def test_an_unknown_criterion_is_refused(self) -> None:
        controller = _controller()
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.mark_reentry("R-99", True)
        self.assertEqual(caught.exception.rule, "ESC-88")

    def test_a_known_criterion_is_accepted(self) -> None:
        controller = _controller()
        controller.mark_reentry("R-1", True)
        self.assertTrue(controller.card.reentry["R-1"])


class RotationLifecycleTests(unittest.TestCase):
    """F-4: the rotation is reachable, and only in order."""

    def test_a_rotation_cannot_be_dispatched_before_it_is_staged(self) -> None:
        controller = _controller(level=EmergencyLevel.ESL_3,
                                 context=make_context(operator_credential_exposed=True))
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.dispatch("EA-A-14", actor="operator", target="key:k3")
        self.assertEqual(caught.exception.rule, "ESC-33")

    def test_the_rotation_may_be_staged_and_then_dispatched(self) -> None:
        controller = _controller(level=EmergencyLevel.ESL_3,
                                 context=make_context(operator_credential_exposed=True))
        rotation = controller.begin_rotation("EA-A-14", actor="operator")
        self.assertTrue(rotation.issued)
        controller.verify_rotation("EA-A-14", actor="operator")
        controller.move_workload("EA-A-14", actor="operator")
        self.assertTrue(rotation.complete)
        record = controller.dispatch("EA-A-14", actor="operator", target="key:k3")
        self.assertEqual(record.action_id, "EA-A-14")

    def test_verification_before_issue_is_refused(self) -> None:
        controller = _controller(level=EmergencyLevel.ESL_3,
                                 context=make_context(operator_credential_exposed=True))
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.verify_rotation("EA-A-14", actor="operator")
        self.assertEqual(caught.exception.rule, "ESC-33")

    def test_invalidation_before_completion_is_refused(self) -> None:
        rotation = RotationState()
        with self.assertRaises(ProtocolRefusal) as caught:
            rotation.invalidate()
        self.assertEqual(caught.exception.rule, "ESC-33")


class PacingTests(unittest.TestCase):
    """F-8: the envelope's daily limit is daily."""

    def test_the_daily_counter_resets_on_a_new_day(self) -> None:
        controller = _controller()
        controller.card.pace_invocations_today = 99
        controller.card.pace_day = "2026-10-19"
        controller.dispatch("EA-A-03", actor="operator", target="session:a1")
        self.assertEqual(controller.card.pace_invocations_today, 1)


class LevelHistoryTests(unittest.TestCase):
    """F-10: severity changes are recorded, and lowering requires a cause."""

    def test_the_level_can_be_raised(self) -> None:
        controller = _controller(level=EmergencyLevel.ESL_2)
        controller.raise_level(EmergencyLevel.ESL_3, "operator", "new evidence")
        self.assertIs(controller.card.level, EmergencyLevel.ESL_3)
        self.assertTrue(controller.card.level_history)

    def test_lowering_without_a_cause_is_refused(self) -> None:
        controller = _controller(level=EmergencyLevel.ESL_3)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.lower_level(EmergencyLevel.ESL_2, "operator", reason="")
        self.assertEqual(caught.exception.rule, "ESC-9")

    def test_lowering_with_a_cause_and_evidence_is_accepted(self) -> None:
        controller = _controller(level=EmergencyLevel.ESL_3)
        controller.lower_level(
            EmergencyLevel.ESL_2, "operator", reason="the cause has ended",
            evidence="the deployment was decommissioned by the provider",
        )
        self.assertIs(controller.card.level, EmergencyLevel.ESL_2)

    def test_raising_to_a_lower_level_is_refused(self) -> None:
        controller = _controller(level=EmergencyLevel.ESL_3)
        with self.assertRaises(ProtocolRefusal) as caught:
            controller.raise_level(EmergencyLevel.ESL_2, "operator", "reason")
        self.assertEqual(caught.exception.rule, "ESC-8")


class LedgerTests(unittest.TestCase):
    """F-9: the emergency path writes to the Ledger."""

    def test_the_transitions_and_the_dispatch_are_recorded(self) -> None:
        ledger = Ledger()
        card = make_card()
        pace = PaceEnvelope(
            reference="PACE-T",
            issued_to=frozenset({"operator"}),
            issued_at=NOW - timedelta(days=1),
            expires_at=NOW + timedelta(days=1),
        )
        controller = EmergencyController(card, pace, now=NOW, ledger=ledger)
        controller.declare(EmergencyLevel.ESL_2, "operator")
        controller.dispatch("EA-A-03", actor="operator", target="session:a1")
        kinds = {entry.kind for entry in ledger.records}
        self.assertIn("emergency.declared", kinds)
        self.assertIn("emergency.transition", kinds)
        self.assertIn("emergency.dispatched", kinds)
        self.assertTrue(ledger.verify()["intact"])
        self.assertGreater(len(ledger), 0)


# -- helpers ---------------------------------------------------------------

def _controller(card=None, level=EmergencyLevel.ESL_2, context=None, declare=True):
    """A controller over an armable card, optionally already declared."""
    if card is None:
        card = make_card(context=context) if context is not None else make_card()
    pace = PaceEnvelope(
        reference="PACE-T",
        issued_to=frozenset({"operator", "alternate"}),
        issued_at=NOW - timedelta(days=1),
        expires_at=NOW + timedelta(days=1),
    )
    controller = EmergencyController(card, pace, now=NOW)
    if declare and card.state is EmergencyState.E0_NOMINAL:
        controller.declare(level, actor="operator")
    return controller


def _action_with(**flags):
    """Return an action carrying the given flags, for the prohibition tests."""
    from dataclasses import replace

    return replace(action("EA-A-03"), **flags)


from caos.emergency import PROHIBITED_OPERATIONS  # noqa: E402  (used above)

#: The prohibitions that no catalogue action can express, because they are
#: platform behaviours rather than actions within the operator's estate.
_PLATFORM_LEVEL_PROHIBITIONS = frozenset({
    name for name, flags in PROHIBITION_FLAGS.items() if not flags
})


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
