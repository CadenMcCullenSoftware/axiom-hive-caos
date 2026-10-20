"""The emergency console: a synthetic drill of the containment path.

The emergency path — the case where the operator's own AI deployment turns
against the operator's device, credentials, or data — is specified at
`operational/emergency-shutdown-and-containment-protocol.md` and implemented
in `caos/emergency.py`. This module renders it as a console surface and runs a
drill against a synthetic estate, so that the operator can see what the
containment path does before they need it.

Everything here is synthetic. The drill never touches a real system.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, Tuple
from .emergency import (
    ACTIONS,
    PROHIBITED_OPERATIONS,
    CheckResult,
    EmergencyCard,
    EmergencyContext,
    EmergencyController,
    EmergencyLevel,
    InventoryEntry,
    PaceEnvelope,
    ProtocolRefusal,
    ProtectedControlSet,
    SeverityIndicators,
    TargetPosture,
    collateral_checks,
    classify_level,
    preflight,
    utc_now,
)


__all__ = ["build_drill", "run_drill", "show_catalogue", "Drill"]


RULE = "-" * 78


@dataclass
class Drill:
    """A synthetic emergency, ready to be declared and exercised."""

    card: EmergencyCard
    context: EmergencyContext
    pace: PaceEnvelope
    indicators: SeverityIndicators

    @property
    def derived_level(self) -> EmergencyLevel:
        return classify_level(self.indicators)


def build_drill() -> Drill:
    """Construct a synthetic emergency on a fictional deployment."""
    now = utc_now()
    principal = "agent:assistant-session-01"
    boundary = frozenset({"session:assistant-session-01", "key:integration-key-01"})

    # The protected control set is the operator's own command path: the
    # break-glass identity and the session it commands with. A containment
    # action that touches either would lock the operator out of their own
    # estate, which is the one failure the emergency path exists to prevent.
    protected = ProtectedControlSet(
        identities=frozenset({"identity:operator-break-glass"}),
        sessions=frozenset({"session:operator-console"}),
        surfaces=frozenset({"surface:operator-console"}),
        verified_at=now,
    )

    inventory: Dict[str, InventoryEntry] = {
        "session:assistant-session-01": InventoryEntry(
            identifier="session:assistant-session-01",
            owner="agent:assistant-session-01",
            instance_scoped=True,
            protected=False,
        ),
        "key:integration-key-01": InventoryEntry(
            identifier="key:integration-key-01",
            owner="agent:assistant-session-01",
            instance_scoped=True,
            protected=False,
        ),
    }

    context = EmergencyContext(
        posture=TargetPosture.P_C,
        deployment_principal=principal,
        blast_boundary=boundary,
        shared_tenancy=True,
        operator_break_glass_working=True,
        operator_credential_exposed=True,
        evidence_captured=True,
        recovery_card_open=True,
        authorisation_source="out_of_band_human",
        reversible_alternatives_tried=("EA-A-01", "EA-A-02"),
        less_reversible_action=False,
        blast_preview_shown=True,
        safety_capability_at_stake=False,
        safety_alternative_confirmed=True,
        command_authority_holder="operator-1",
        command_authority_intact=True,
        inventory=inventory,
        protected_controls=protected,
    )

    card = EmergencyCard(
        incident_id="INC-EXAMPLE-0001",
        operator="operator-1",
        target_principal=principal,
        posture=TargetPosture.P_C,
        blast_boundary=boundary,
        context=context,
        protected_controls=protected,
        command_authority_holder="operator-1",
        break_glass_tested=True,
        break_glass_passed=True,
        break_glass_tested_at=now,
        break_glass_tested_by="operator-1",
        # The standard card's authorisation. The drill's card is armable, or
        # it could not carry a dispatch, and a demonstration of a card that
        # cannot exist teaches the wrong thing about the control.
        ea_reference="EA-EXAMPLE-0001",
        objective=(
            "contain the compromised deployment without breaking the operator's own "
            "access or affecting a shared tenant"
        ),
        hypothesis=(
            "the deployment's capability is reachable through its own session and its "
            "own credentials, and nothing beyond"
        ),
        disconfirming_observation=(
            "the capability survives the termination of the session, which would mean "
            "it is held somewhere the containment does not reach"
        ),
        excluded_targets=(
            "every other tenant of the shared service",
            "the provider's own service surface",
        ),
        risk_of_inaction=(
            "the compromised deployment retains access to the operator's data and to "
            "the shared tenant's service"
        ),
        alternatives_considered=(
            "wait for the provider's fraud review, which takes days",
            "restore from the operator's own backup, which restores the foothold",
        ),
        abort_conditions=(
            "the operator's break-glass access stops working",
            "the shared tenant's service becomes unavailable",
        ),
        abort_owner="operator-1",
        abort_mechanism="single-key abort on the emergency console",
        contingency=(
            "restore the operator's session from the break-glass path and escalate to "
            "the alternate holder"
        ),
        contingency_recorded_at=now,
        deconfliction_passed=True,
        third_party_assessment=(
            "the affected service is shared with another tenant, which depends on it "
            "for its own operations; the containment is confined to the operator's "
            "own deployment identity"
        ),
        approver_roles=frozenset({"team_lead"}),
        non_weaponisation_attestation=(
            "no model is attacked, and no uninvolved third party is harmed"
        ),
        third_party_authorised=False,
        approved_by="operator-1",
    )

    pace = PaceEnvelope(
        reference="PACE-EXAMPLE-0001",
        issued_to=frozenset({"operator-1"}),
        issued_at=now,
        expires_at=now + timedelta(days=30),
    )

    indicators = SeverityIndicators(
        indicator_only=False,
        unauthorised_action=True,
        data_left_boundary=False,
        credentials_exposed=False,
        persistence_established=False,
        persistence_attempted=False,
        control_plane_tampered=False,
        operator_manipulation=False,
        containment_failed=False,
    )

    return Drill(card=card, context=context, pace=pace, indicators=indicators)


def show_catalogue() -> str:
    """Render the emergency action catalogue and the hard prohibitions."""
    lines = [RULE, "EMERGENCY ACTION CATALOGUE", RULE]
    lines.append("")
    lines.append("actions")
    for action in sorted(ACTIONS, key=lambda a: a.identifier):
        lines.append(
            f"  {action.identifier:<10} tier {action.tier}  {action.collateral.name:<4} "
            f"{action.reversibility.name:<12} {'PACE' if action.in_pace else '    '}  "
            f"{action.name}"
        )
    lines.append("")
    lines.append("hard prohibitions — never available at any level")
    for prohibition in PROHIBITED_OPERATIONS:
        lines.append(f"  - {prohibition}")
    lines.append(RULE)
    return "\n".join(lines)


def run_drill() -> str:
    """Run the synthetic drill and render what the containment path does."""
    drill = build_drill()
    lines = [RULE, "EMERGENCY DRILL — synthetic estate", RULE]
    lines.append(
        f"incident   : {drill.card.incident_id} "
        f"(a fictional deployment; nothing here touches a real system)"
    )
    lines.append(f"posture    : {drill.card.posture.value}")
    lines.append(f"principal  : {drill.card.target_principal}")
    lines.append(f"blast      : {', '.join(sorted(drill.card.blast_boundary))}")
    lines.append(
        f"derived level: {drill.derived_level.label} — the level the evidence "
        "indicates, before any operator judgement"
    )
    lines.append("")

    controller = EmergencyController(card=drill.card, pace=drill.pace)
    try:
        controller.declare(drill.derived_level, "operator-1", drill.indicators)
        lines.append(
            f"declared   : {drill.card.state.value} at level {drill.card.level.label}"
        )
    except ProtocolRefusal as refusal:
        lines.append(f"declaration refused: {refusal.rule} — {refusal.detail}")

    lines.append("")
    lines.append("zero-collateral pre-dispatch checks")
    checks: Tuple[CheckResult, ...] = preflight(
        "session:assistant-session-01",
        drill.context.inventory,
        "agent:assistant-session-01",
        drill.context.protected_controls,
    )
    for check in checks:
        marker = "pass" if check.passed else "FAIL"
        lines.append(f"  {check.identifier:<6} {marker}  {check.name}")
        if not check.passed:
            lines.append(f"           {check.reason}")
    lines.append("")

    lines.append("containment action admissibility against the declared context")
    for action in sorted(ACTIONS, key=lambda a: a.identifier)[:6]:
        action_checks = collateral_checks(
            action, drill.context, target="session:assistant-session-01"
        )
        failed = [c for c in action_checks if not c.passed]
        state = "permitted" if not failed else "refused"
        lines.append(f"  {action.identifier:<10} {state}")
        for check in failed:
            lines.append(f"             {check.identifier}: {check.reason}")
    lines.append("")
    lines.append(
        "the checks fail closed: a check that cannot be evaluated because its "
        "input is unavailable is reported as failed, not as passed"
    )
    lines.append(RULE)
    return "\n".join(lines)
