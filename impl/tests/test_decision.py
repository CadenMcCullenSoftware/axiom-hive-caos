"""Tests for the selection algorithm."""

from __future__ import annotations

import unittest
from datetime import timedelta

from caos.countermeasures import get
from caos.decision import (
    counterfactuals,
    dispatch,
    filter_admissible,
    generate_candidates,
    rank_candidates,
    select,
)
from caos.ledger import Ledger
from caos.models import OperationCard, ThreatAssessment, utc_now
from caos.vocab import AutonomyClass, CollateralClass, ROEProfile


def make_card(**overrides) -> OperationCard:
    now = utc_now()
    defaults = dict(
        card_id="OC-TEST-002",
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
        contingency="abort on degradation",
        contingency_recorded_at=now,
        min_countermeasure_confidence=0.30,
        autonomy_on_call="operator-1",
        autonomy_reversion_trigger="revert on loss of telemetry",
    )
    defaults.update(overrides)
    return OperationCard(**defaults)


class CandidateGenerationTests(unittest.TestCase):
    def test_candidates_come_from_the_declared_technique_bindings(self) -> None:
        card = make_card(techniques=("AAT-2.1",))
        candidates = generate_candidates(card)
        self.assertTrue(candidates)
        self.assertIn("OCC-05", {c.identifier for c in candidates})

    def test_operator_proposals_are_included(self) -> None:
        card = make_card(techniques=("AAT-1.1",))
        candidates = generate_candidates(card, extra=["OCC-05"])
        self.assertIn("OCC-05", {c.identifier for c in candidates})

    def test_unknown_extras_are_ignored(self) -> None:
        card = make_card()
        candidates = generate_candidates(card, extra=["OCC-999"])
        self.assertNotIn("OCC-999", {c.identifier for c in candidates})


class FilteringTests(unittest.TestCase):
    def test_rejections_are_retained_with_reasons(self) -> None:
        card = make_card(techniques=("AAT-1.1", "AAT-7.1"))
        candidates = generate_candidates(card)
        admissible, rejected = filter_admissible(card, candidates)
        self.assertTrue(rejected)
        for candidate in rejected:
            self.assertFalse(candidate.admissible)
            self.assertTrue(candidate.result.failures)
            for failure in candidate.result.failures:
                self.assertTrue(failure.detail)
                self.assertTrue(failure.remedy)

    def test_no_candidate_is_lost_between_generation_and_filtering(self) -> None:
        card = make_card(techniques=("AAT-1.1", "AAT-7.1"))
        candidates = generate_candidates(card)
        admissible, rejected = filter_admissible(card, candidates)
        self.assertEqual(len(admissible) + len(rejected), len(candidates))

    def test_a_card_that_cannot_be_armed_admits_nothing(self) -> None:
        card = make_card(rationale="")
        candidates = generate_candidates(card)
        admissible, _rejected = filter_admissible(card, candidates)
        self.assertEqual(admissible, [])


class RankingTests(unittest.TestCase):
    def test_candidates_are_ranked_by_descending_priority(self) -> None:
        card = make_card(techniques=("AAT-1.1", "AAT-2.1", "AAT-7.1"))
        candidates = generate_candidates(card)
        admissible, _rejected = filter_admissible(card, candidates)
        ranked = rank_candidates(admissible)
        priorities = [c.priority for c in ranked]
        self.assertEqual(priorities, sorted(priorities, reverse=True))

    def test_ranking_breaks_ties_on_the_identifier(self) -> None:
        card = make_card(techniques=("AAT-1.1",))
        candidates = generate_candidates(card)
        admissible, _rejected = filter_admissible(card, candidates)
        ranked = rank_candidates(admissible)
        for first, second in zip(ranked, ranked[1:]):
            self.assertGreaterEqual(first.priority, second.priority)
            if first.priority == second.priority:
                self.assertLess(first.identifier, second.identifier)


class SelectionTests(unittest.TestCase):
    def test_selection_produces_a_reconstructible_record(self) -> None:
        card = make_card(techniques=("AAT-1.1",))
        candidates = generate_candidates(card)
        admissible, _rejected = filter_admissible(card, candidates)
        chosen = rank_candidates(admissible)[0]
        record = select(
            card,
            chosen,
            alternatives=tuple(c.identifier for c in admissible),
            actor="operator-1",
        )
        self.assertTrue(record.known_at_the_time)
        self.assertIn(chosen.identifier, record.choice)
        self.assertTrue(record.authority_relied_on)
        self.assertTrue(record.pre_registered_contingency)
        self.assertTrue(record.risk_of_inaction)
        self.assertEqual(record.actor, "operator-1")

    def test_the_record_states_the_threat_components(self) -> None:
        card = make_card(techniques=("AAT-1.1",))
        candidates = generate_candidates(card)
        admissible, _rejected = filter_admissible(card, candidates)
        record = select(card, rank_candidates(admissible)[0])
        joined = " ".join(record.known_at_the_time)
        self.assertIn("threat score", joined)
        self.assertIn("attribution confidence", joined)

    def test_the_record_is_json_serialisable(self) -> None:
        card = make_card(techniques=("AAT-1.1",))
        candidates = generate_candidates(card)
        admissible, _rejected = filter_admissible(card, candidates)
        record = select(card, rank_candidates(admissible)[0])
        payload = record.as_payload()
        self.assertIsInstance(payload["timestamp"], str)
        self.assertIsInstance(payload["options_considered"], list)


class DispatchTests(unittest.TestCase):
    def _admissible(self, card):
        candidates = generate_candidates(card)
        admissible, _rejected = filter_admissible(card, candidates)
        return rank_candidates(admissible)[0]

    def test_a_dispatch_debits_the_autonomy_budget(self) -> None:
        card = make_card(
            techniques=("AAT-1.1",),
            autonomy_budget=3,
            autonomy_on_call="operator-1",
            autonomy_reversion_trigger="revert on loss of telemetry",
            autonomy_consumed=0,
        )
        ledger = Ledger()
        candidate = self._admissible(card)
        result = dispatch(card, candidate.countermeasure, ledger)
        self.assertTrue(result.dispatched)
        self.assertEqual(card.autonomy_consumed, result.units_spent)
        self.assertEqual(card.remaining_budget(), 3 - result.units_spent)

    def test_a_refused_dispatch_spends_nothing(self) -> None:
        card = make_card(
            techniques=("AAT-1.1",),
            autonomy_budget=3,
            autonomy_consumed=0,
            min_countermeasure_confidence=0.95,
        )
        ledger = Ledger()
        from caos.countermeasures import get

        result = dispatch(card, get("OCC-24"), ledger)
        self.assertFalse(result.dispatched)
        self.assertEqual(result.units_spent, 0)
        self.assertEqual(card.autonomy_consumed, 0)
        self.assertTrue(result.failures)

    def test_a_refusal_is_recorded_in_the_ledger(self) -> None:
        card = make_card(
            techniques=("AAT-1.1",),
            min_countermeasure_confidence=0.95,
        )
        ledger = Ledger()
        from caos.countermeasures import get

        dispatch(card, get("OCC-24"), ledger)
        refusals = ledger.of_kind("dispatch.refused")
        self.assertEqual(len(refusals), 1)
        self.assertEqual(refusals[0].payload["outcome"], "refuse")

    def test_a_dispatch_is_recorded_in_the_ledger(self) -> None:
        card = make_card(techniques=("AAT-1.1",), autonomy_budget=3)
        ledger = Ledger()
        candidate = self._admissible(card)
        dispatch(card, candidate.countermeasure, ledger)
        issued = ledger.of_kind("dispatch.issued")
        self.assertEqual(len(issued), 1)
        self.assertEqual(issued[0].card_id, card.card_id)


class CounterfactualTests(unittest.TestCase):
    def test_the_do_nothing_option_is_included(self) -> None:
        card = make_card(techniques=("AAT-1.1",))
        candidates = generate_candidates(card)
        admissible, rejected = filter_admissible(card, candidates)
        options = counterfactuals(card, admissible + rejected)
        labels = [o.label for o in options]
        self.assertIn("do nothing", labels)

    def test_options_are_ordered_by_residual_risk(self) -> None:
        card = make_card(techniques=("AAT-1.1",))
        candidates = generate_candidates(card)
        admissible, rejected = filter_admissible(card, candidates)
        options = counterfactuals(card, admissible + rejected)
        risks = [o.residual_risk for o in options]
        self.assertEqual(risks, sorted(risks))

    def test_inadmissible_options_are_marked_in_the_note(self) -> None:
        card = make_card(techniques=("AAT-1.1", "AAT-7.1"))
        candidates = generate_candidates(card)
        admissible, rejected = filter_admissible(card, candidates)
        options = counterfactuals(card, admissible + rejected)
        notes = [o.note for o in options if o.note.startswith("not admissible")]
        self.assertTrue(notes)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
