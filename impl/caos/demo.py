"""A synthetic estate for demonstration and for the exercise harness.

Everything in this module is fictional. The estate, the adversary, the
signals, and the card are invented to exercise the framework's machinery. No
real organisation, product, service, or incident is represented, and no
detail here should be read as a description of a real deployment.
"""

from __future__ import annotations

from datetime import timedelta

from .ledger import Ledger
from .models import (
    Claim,
    OperationCard,
    Signal,
    ThreatAssessment,
    utc_now,
)
from .roe import EvaluationContext
from .watchfloor import Posture, Watchfloor
from typing import List
from .vocab import AutonomyClass, ClaimLabel, CollateralClass, Reversibility, ROEProfile, SourceTier

__all__ = ["build_demo", "DEMO_CARD_ID"]


DEMO_CARD_ID = "OC-2026-014"


def build_demo() -> Watchfloor:
    """Construct a Watchfloor populated with a synthetic estate."""
    now = utc_now()
    horizon = now + timedelta(days=2)

    ledger = Ledger()
    ledger.append(
        "posture.set",
        {
            "posture": "Observe",
            "ea_reference": "EA-2026-004",
            "established": now.isoformat(),
            "rationale": (
                "baseline posture pending attribution; the advisory note is "
                "conditional on the operator confirming the observation"
            ),
        },
    )
    ledger.append(
        "signal.ingested",
        {
            "signal_id": "SIM-0001",
            "source": "tool-broker.trace",
            "summary": "tool-call sequence departs from the declared workflow",
            "fidelity": "high",
        },
        subject="agent:reporting-service",
        actor="role:collector",
        card_ref=DEMO_CARD_ID,
    )

    assessment = ThreatAssessment(
        likelihood=0.6,
        impact=3,
        autonomy_factor=1,
        velocity=1,
        attribution_confidence=0.55,
        attribution_basis=(
            "behavioural signature overlap only; no infrastructure overlap and no "
            "operator-level correlation, so this is class attribution and not "
            "identity attribution"
        ),
        likelihood_reason=(
            "the sequence departs from the declared workflow but is consistent "
            "with a legitimate configuration change that has not been recorded"
        ),
        impact_reason=(
            "the affected service would degrade, but no function of record would be lost"
        ),
        autonomy_reason=(
            "the agent retries without a human turn, but a human approves each "
            "retention; this is human-supervised automation"
        ),
        velocity_reason="repeated, but not yet adaptive between attempts",
        classification="AAT-1",
        techniques=("AAT-1.1", "AAT-1.2", "AAT-6.1"),
        alternative_explanations=(
            "an unrecorded configuration change to the workflow",
            "a seasonal batch job that was not documented",
        ),
    )

    card = OperationCard(
        card_id=DEMO_CARD_ID,
        title="Unattributed tool-call anomaly on the reporting service",
        owner="operator-1",
        created_at=now,
        objective=(
            "determine whether the observed tool-call sequence is an adversary "
            "operation or an unrecorded internal change, and reduce the risk "
            "that the reporting service is degraded by either"
        ),
        hypothesis=(
            "the sequence is an unrecorded internal configuration change rather "
            "than an adversary operation"
        ),
        disconfirming_observation=(
            "a tool-call pattern that recurs with no corresponding internal "
            "change record and no operator attribution"
        ),
        ea_reference="EA-2026-004",
        profile=ROEProfile.R0_OBSERVE,
        collateral_ceiling=CollateralClass.C0,
        autonomy_ceiling=AutonomyClass.AC1_ASSISTED,
        approver_roles=frozenset({"operator", "team_lead"}),
        expires_at=horizon,
        authorised_targets=("estate:reporting-service",),
        excluded_targets=(
            "all infrastructure not owned by the operator",
            "all third-party hosted services without specific authorisation",
            "any model, model artefact, or model provider",
        ),
        third_party_authorised=False,
        third_party_assessment="",
        required_reversibility=Reversibility.REVERSED,
        threat=assessment,
        classification="AAT-1",
        techniques=("AAT-1.1", "AAT-1.2", "AAT-6.1"),
        selected_counters=(),
        rejected_counters=(),
        min_countermeasure_confidence=0.30,
        autonomy_budget=0,
        autonomy_consumed=0,
        abort_conditions=(
            "the reporting service degrades below its declared service floor",
            "the sequence is confirmed as an internal change and the card is closed",
            "the engagement authority expires",
        ),
        abort_owner="operator-1",
        abort_mechanism="single-key abort on the Watchfloor; reverts posture to Observe",
        deconfliction_passed=True,
        risk_of_inaction=(
            "if the sequence is adversarial and no action is taken, the reporting "
            "service may be degraded during the next business cycle"
        ),
        residual_risk_before=assessment.effective_threat,
        residual_risk_after=assessment.effective_threat * (1 - 0.10),
        expected_effectiveness=0.10,
        effectiveness_confidence=0.45,
        claims=(
            Claim(
                text=(
                    "the observed tool-call sequence has no corresponding "
                    "configuration-change record"
                ),
                label=ClaimLabel.FACT,
                tier=SourceTier.ST1,
                confidence=0.85,
                provenance="tool-broker trace, retained for 30 days",
            ),
            Claim(
                text=(
                    "the behaviour is consistent with class AAT-1 automation; "
                    "identity attribution is not supported by the present evidence"
                ),
                label=ClaimLabel.INTERPRETATION,
                tier=SourceTier.ST2,
                confidence=0.55,
                provenance="analyst assessment against the taxonomy",
            ),
            Claim(
                text=(
                    "a behavioural baseline for this service would have raised the "
                    "signal earlier than the sequence detector did"
                ),
                label=ClaimLabel.HYPOTHESIS,
                tier=SourceTier.ST4,
                confidence=0.30,
                provenance="coverage assessment; not yet tested",
                derivation_penalty=0.10,
            ),
        ),
        rationale=(
            "the present evidence supports class attribution but not identity "
            "attribution, so the selected countermeasure is one that does not "
            "depend on the contested claim"
        ),
        alternatives_considered=(
            "OCC-24 bounded sandbox engagement — rejected: requires profile R2 and "
            "a legal contact, and the evidence does not yet support it",
            "OCC-34 credential invalidation — rejected: requires identity attribution "
            "at 0.85, which the present evidence does not reach",
            "OCC-28 decoy target deployment — rejected: requires profile R3, and a "
            "decoy against a possibly-internal change would be a disclosure risk",
        ),
        dissent="",
        contingency=(
            "if the baseline detector confirms the sequence is adversarial, "
            "reassess attribution and raise an escalation request for profile R2"
        ),
        contingency_recorded_at=now,
        revision=1,
    )

    signals: List[Signal] = [
        Signal(
            signal_id="SIM-0001",
            observed_at=now - timedelta(minutes=42),
            source="tool-broker.trace",
            fidelity="high",
            integrity="trustworthy",
            description=(
                "tool-call sequence departs from the declared workflow: the agent "
                "retries a failing call without a human turn between attempts"
            ),
            indicators=("retry-without-turn", "undeclared-tool"),
            category="AAT-1",
            technique="AAT-1.2",
        ),
        Signal(
            signal_id="SIM-0002",
            observed_at=now - timedelta(minutes=39),
            source="model-gateway.log",
            fidelity="medium",
            integrity="trustworthy",
            description=(
                "request rate for the service rose above the principal's declared "
                "range over a 15-minute window"
            ),
            indicators=("rate-above-baseline",),
            category="AAT-6",
            technique="AAT-6.1",
        ),
        Signal(
            signal_id="SIM-0003",
            observed_at=now - timedelta(minutes=31),
            source="egress-proxy.log",
            fidelity="high",
            integrity="degraded",
            description=(
                "proxy telemetry is delayed and partially unavailable; the absence "
                "of an egress finding is not evidence of no egress"
            ),
            indicators=("telemetry-degraded",),
            category="AAT-9",
            technique=None,
        ),
        Signal(
            signal_id="SIM-0004",
            observed_at=now - timedelta(minutes=12),
            source="agent-runtime.trace",
            fidelity="high",
            integrity="trustworthy",
            description=(
                "the agent decomposed the reporting task into constituent steps "
                "that no human specified"
            ),
            indicators=("undeclared-decomposition",),
            category="AAT-1",
            technique="AAT-1.1",
        ),
    ]

    posture = Posture(
        profile=ROEProfile.R0_OBSERVE,
        ea_reference="EA-2026-004",
        expires_at=horizon,
        rationale=(
            "baseline posture pending attribution; the posture is raised only by a "
            "recorded escalation decision, never by the arrival of a signal"
        ),
    )

    context = EvaluationContext(
        deconfliction_passed=True,
        class_confidence=0.55,
        external_authority_confirmed=False,
        now=now,
        policy_version="1.0",
    )

    return Watchfloor(
        ledger=ledger,
        cards=[card],
        signals=signals,
        posture=posture,
        context=context,
    )
