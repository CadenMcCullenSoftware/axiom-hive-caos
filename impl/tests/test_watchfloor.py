"""Tests for the Watchfloor console and the proving ground."""

from __future__ import annotations

import unittest

from caos.demo import DEMO_CARD_ID, build_demo
from caos.models import Signal, utc_now
from caos.proving_ground import (
    ARCHETYPE_TECHNIQUES,
    RUBRIC,
    Archetype,
    Scenario,
    evaluate_detection,
    run_scenario,
    score_exercise,
)
from caos.taxonomy import TECHNIQUES


class WatchboardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.floor = build_demo()

    def test_watchboard_renders(self) -> None:
        output = self.floor.watchboard()
        self.assertIn("WATCHBOARD", output)
        self.assertIn(DEMO_CARD_ID, output)

    def test_watchboard_states_the_posture(self) -> None:
        output = self.floor.watchboard()
        self.assertIn("Observe", output)
        self.assertIn("EA-2026-004", output)

    def test_unusable_sources_are_reported_as_not_a_negative_finding(self) -> None:
        output = self.floor.watchboard()
        self.assertIn("NOT a negative finding", output)

    def test_watchboard_reports_autonomy_utilisation(self) -> None:
        output = self.floor.watchboard()
        self.assertIn("autonomy utilisation", output)


class IntegrityStateTests(unittest.TestCase):
    def test_the_five_state_vocabulary_is_used(self) -> None:
        from caos.vocab import IntegrityState

        self.assertEqual(len(list(IntegrityState)), 5)

    def test_a_missing_source_is_not_usable(self) -> None:
        from caos.vocab import IntegrityState

        signal = Signal(
            signal_id="X", observed_at=utc_now(), source="s.log", fidelity="none",
            integrity="missing", description="the source did not report",
        )
        self.assertFalse(signal.usable)
        self.assertIs(signal.integrity_state, IntegrityState.MISSING)

    def test_a_stale_source_is_usable_but_impaired(self) -> None:
        from caos.vocab import IntegrityState

        signal = Signal(
            signal_id="X", observed_at=utc_now(), source="s.log", fidelity="low",
            integrity="stale", description="the source is reporting late",
        )
        self.assertTrue(signal.usable)
        self.assertIs(signal.integrity_state, IntegrityState.STALE)

    def test_an_uninterpretable_state_is_treated_as_tampered(self) -> None:
        from caos.vocab import IntegrityState

        signal = Signal(
            signal_id="X", observed_at=utc_now(), source="s.log", fidelity="unknown",
            integrity="who knows", description="an unrecognised integrity state",
        )
        self.assertFalse(signal.usable)
        self.assertIs(signal.integrity_state, IntegrityState.TAMPERED_SUSPECT)


class TriageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.floor = build_demo()

    def test_triage_renders_every_signal(self) -> None:
        output = self.floor.triage()
        for signal in self.floor.signals:
            self.assertIn(signal.signal_id, output)

    def test_degraded_sources_are_marked(self) -> None:
        output = self.floor.triage()
        self.assertIn("?", output)

    def test_unusable_sources_are_marked_distinctly(self) -> None:
        self.floor.signals.append(
            Signal(
                signal_id="SIM-9998",
                observed_at=utc_now(),
                source="missing.log",
                fidelity="none",
                integrity="missing",
                description="source did not report; absence is not a negative finding",
            )
        )
        output = self.floor.triage()
        self.assertIn("!", output)

    def test_personal_data_is_flagged(self) -> None:
        self.floor.signals.append(
            Signal(
                signal_id="SIM-9999",
                observed_at=utc_now(),
                source="synthetic.log",
                fidelity="high",
                integrity="trustworthy",
                description="synthetic signal carrying personal data",
                personal_data_present=True,
            )
        )
        output = self.floor.triage()
        self.assertIn("personal data present", output)


class CardViewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.floor = build_demo()

    def test_card_view_shows_the_threat_components(self) -> None:
        output = self.floor.show_card(DEMO_CARD_ID)
        self.assertIn("likelihood", output)
        self.assertIn("impact", output)
        self.assertIn("velocity", output)

    def test_card_view_shows_the_evidence_with_labels(self) -> None:
        output = self.floor.show_card(DEMO_CARD_ID)
        self.assertIn("[Fact]", output)
        self.assertIn("[Interpretation]", output)
        self.assertIn("[Hypothesis]", output)

    def test_card_view_shows_the_risk_of_inaction(self) -> None:
        output = self.floor.show_card(DEMO_CARD_ID)
        self.assertIn("risk of inaction", output)

    def test_card_view_reports_blocking_defects(self) -> None:
        card = self.floor.cards[DEMO_CARD_ID]
        card.rationale = ""
        output = self.floor.show_card(DEMO_CARD_ID)
        self.assertIn("BLOCKING DEFECTS", output)

    def test_unknown_card_raises(self) -> None:
        with self.assertRaises(KeyError):
            self.floor.show_card("OC-NOT-THERE")


class RoeGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.floor = build_demo()

    def test_gate_refuses_an_out_of_profile_countermeasure(self) -> None:
        output = self.floor.roe_gate(DEMO_CARD_ID, "OCC-34")
        self.assertIn("REFUSED", output)
        self.assertIn("AD-1", output)

    def test_gate_states_the_margin_of_exceedance(self) -> None:
        output = self.floor.roe_gate(DEMO_CARD_ID, "OCC-24")
        self.assertIn("margin", output.lower())

    def test_gate_lists_the_approvals_required(self) -> None:
        output = self.floor.roe_gate(DEMO_CARD_ID, "OCC-24")
        self.assertIn("approvals needed", output)

    def test_gate_reports_an_unknown_countermeasure(self) -> None:
        output = self.floor.roe_gate(DEMO_CARD_ID, "OCC-999")
        self.assertIn("no such countermeasure", output)


class CountermeasureConsoleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.floor = build_demo()

    def test_console_shows_candidates_and_rejections(self) -> None:
        output = self.floor.countermeasure_console(DEMO_CARD_ID)
        self.assertIn("COUNTERMEASURE CONSOLE", output)
        self.assertIn("rejected", output)

    def test_options_include_doing_nothing(self) -> None:
        output = self.floor.options(DEMO_CARD_ID)
        self.assertIn("do nothing", output)

    def test_autonomy_monitor_renders(self) -> None:
        output = self.floor.autonomy_monitor(DEMO_CARD_ID)
        self.assertIn("AUTONOMY MONITOR", output)


class AbortTests(unittest.TestCase):
    def setUp(self) -> None:
        self.floor = build_demo()

    def test_abort_records_the_reason_and_reverts_posture(self) -> None:
        output = self.floor.abort(DEMO_CARD_ID, "the service degraded")
        self.assertIn("ABORTED", output)
        self.assertIn("the service degraded", output)
        self.assertIn(DEMO_CARD_ID, self.floor.aborted)

    def test_abort_writes_to_the_ledger(self) -> None:
        self.floor.abort(DEMO_CARD_ID, "test reason")
        aborts = self.floor.ledger.of_kind("abort")
        self.assertEqual(len(aborts), 1)
        self.assertEqual(aborts[0].payload["reason"], "test reason")

    def test_abort_consumes_the_autonomy_budget(self) -> None:
        card = self.floor.cards[DEMO_CARD_ID]
        card.autonomy_budget = 4
        card.autonomy_consumed = 1
        self.floor.abort(DEMO_CARD_ID, "test")
        self.assertEqual(card.remaining_budget(), 0)


class ReplayAndAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.floor = build_demo()

    def test_replay_renders_recorded_entries(self) -> None:
        output = self.floor.replay(DEMO_CARD_ID)
        self.assertIn("REPLAY", output)

    def test_replay_of_an_unknown_card_is_honest(self) -> None:
        output = self.floor.replay("OC-NOT-THERE")
        self.assertIn("no recorded entries", output)

    def test_audit_reports_the_chain_and_its_limits(self) -> None:
        output = self.floor.audit()
        self.assertIn("LEDGER VERIFICATION", output)
        self.assertIn("does not establish", output)


class ProvingGroundTests(unittest.TestCase):
    def test_scenarios_are_reproducible(self) -> None:
        scenario = Scenario(
            name="t", archetype=Archetype.SOCIAL_SWARM, steps=10, seed=42
        )
        first = run_scenario(scenario)
        second = run_scenario(scenario)
        self.assertEqual([s.signal_id for s in first], [s.signal_id for s in second])
        self.assertEqual([s.technique for s in first], [s.technique for s in second])

    def test_a_scenario_produces_the_requested_number_of_signals(self) -> None:
        scenario = Scenario(name="t", archetype=Archetype.AUTOMATION_SCALER, steps=7)
        self.assertEqual(len(run_scenario(scenario)), 7)

    def test_every_archetype_maps_to_known_techniques(self) -> None:
        known = {t.identifier for t in TECHNIQUES}
        for archetype, techniques in ARCHETYPE_TECHNIQUES.items():
            for technique_id in techniques:
                self.assertIn(technique_id, known, f"{archetype}: {technique_id}")

    def test_detection_evaluation_reports_misses(self) -> None:
        scenario = Scenario(name="t", archetype=Archetype.SOCIAL_SWARM, steps=30)
        signals = run_scenario(scenario)
        report = evaluate_detection(signals, frozenset())
        self.assertTrue(report.techniques_missed)
        self.assertEqual(report.coverage_percentage, 0.0)

    def test_detection_evaluation_reports_full_coverage_when_covered(self) -> None:
        scenario = Scenario(name="t", archetype=Archetype.SOCIAL_SWARM, steps=30)
        signals = run_scenario(scenario)
        exercised = {s.technique for s in signals if s.technique}
        report = evaluate_detection(signals, frozenset(exercised))
        self.assertEqual(report.coverage_percentage, 100.0)

    def test_the_report_names_personal_data(self) -> None:
        scenario = Scenario(name="t", archetype=Archetype.SOCIAL_SWARM, steps=30)
        signals = run_scenario(scenario)
        report = evaluate_detection(signals, scenario.detected)
        self.assertTrue(
            any("personal data" in finding for finding in report.findings)
            or report.personalised_data_signals == 0
        )

    def test_scoring_produces_a_breakdown(self) -> None:
        result = score_exercise({"decision quality": 3, "escalation discipline": 1})
        self.assertEqual(len(result["breakdown"]), len(RUBRIC))
        self.assertLessEqual(result["awarded"], result["maximum"])

    def test_scoring_caps_a_dimension_at_its_weight(self) -> None:
        result = score_exercise({"decision quality": 99})
        decision = [d for d in result["breakdown"] if d["dimension"] == "decision quality"]
        self.assertEqual(decision[0]["awarded"], 4)

    def test_scoring_states_that_it_measures_the_exercise(self) -> None:
        result = score_exercise({})
        self.assertIn("not the operator's competence", result["note"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
