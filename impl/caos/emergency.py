"""Emergency shutdown and containment protocol: the enforceable core.

This module implements the mechanically checkable parts of
``operational/emergency-shutdown-and-containment-protocol.md``:

* the emergency severity ladder and its "upgrade on doubt" rule (ESC-7);
* the emergency state machine and its legal transitions (ESC-11);
* the target posture and the ceiling each posture imposes (ESC-1 to ESC-3);
* the zero-collateral pre-dispatch checks, K-1 to K-3, and the sixteen
  isolation invariants they enforce (ESC-48, ESC-5);
* the protected control set and the mandatory pre-flight gate, which verify
  that every target is instance-scoped, owned by the compromised deployment,
  and disjoint from the operator's command path (ESC-82 to ESC-89, ZC-13,
  ZC-14);
* the pre-authorised containment envelope, PACE-1 to PACE-7;
* the kill verification gate, V-1 to V-9, and the two-pass rule (ESC-20 to
  ESC-24);
* the staged-rotation rule that keeps containment from locking the operator
  out (ESC-33, ZC-5);
* the re-entry criteria, R-1 to R-10 (ESC-56);
* the hard prohibitions that are never available at any level (Annex C).

What it does not implement, and cannot, is the judgement the protocol
ultimately rests on: whether the severity was assessed correctly, whether the
target was the right one, and whether the operator was being manipulated. The
module's position is the set's: the control is procedural, the record is the
deliverable, and the human at the console remains the load-bearing element.
What this module does is make the mechanical half of that judgement
unarguable, so that the human is left with the part that is theirs.

The implementation is standard-library only and has no external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, IntEnum
from typing import Any, Dict, FrozenSet, List, Mapping, Optional, Sequence, Tuple

from .vocab import CollateralClass, Reversibility


__all__ = [
    "EmergencyLevel",
    "EmergencyState",
    "TargetPosture",
    "ActionTier",
    "SeverityIndicators",
    "classify_level",
    "EmergencyAction",
    "ACTIONS",
    "action",
    "PROHIBITED_OPERATIONS",
    "POSTURE_MAX_COLLATERAL",
    "POSTURE_MAX_TIER",
    "EmergencyContext",
    "CheckResult",
    "collateral_checks",
    "ProtectedControlSet",
    "InventoryEntry",
    "preflight",
    "PaceEnvelope",
    "DispatchRecord",
    "VerificationPass",
    "RotationState",
    "EmergencyCard",
    "EmergencyController",
    "EmergencyError",
    "ProtocolRefusal",
    "utc_now",
]


def utc_now() -> datetime:
    """Return the current time as an aware UTC datetime."""
    return datetime.now(timezone.utc)


class EmergencyError(Exception):
    """Base class for errors raised by the emergency core."""


class ProtocolRefusal(EmergencyError):
    """A refusal by the protocol.

    A refusal is a successful control and is never treated as a failure of
    the system. It carries the rule that produced it, because a refusal an
    operator cannot trace to a rule is an unexplained failure, and unexplained
    failures are not trusted by the people who depend on them.
    """

    def __init__(self, rule: str, detail: str, remedy: str = "") -> None:
        super().__init__(f"{rule}: {detail}")
        self.rule = rule
        self.detail = detail
        self.remedy = remedy


# --------------------------------------------------------------------------
# Severity
# --------------------------------------------------------------------------


class EmergencyLevel(IntEnum):
    """The emergency severity ladder, ESL-1 to ESL-4."""

    ESL_1 = 1
    ESL_2 = 2
    ESL_3 = 3
    ESL_4 = 4

    @property
    def label(self) -> str:
        return _LEVEL_LABELS[self]

    @property
    def allows_pace(self) -> bool:
        """Whether the containment envelope may be used at this level."""
        return self is not EmergencyLevel.ESL_1


_LEVEL_LABELS: Mapping[EmergencyLevel, str] = {
    EmergencyLevel.ESL_1: "Suspicion",
    EmergencyLevel.ESL_2: "Confirmed capability misuse",
    EmergencyLevel.ESL_3: "Exposure in progress or complete",
    EmergencyLevel.ESL_4: "Control-surface compromise or containment failure",
}


@dataclass(frozen=True)
class SeverityIndicators:
    """The observed evidence a severity level is derived from.

    The fields are the observable conditions of the protocol's severity
    table, not an assessment. The classification is mechanical, and the
    judgement remains with the operator, who records it.
    """

    indicator_only: bool = False
    unauthorised_action: bool = False
    data_left_boundary: bool = False
    credentials_exposed: bool = False
    persistence_established: bool = False
    persistence_attempted: bool = False
    control_plane_tampered: bool = False
    operator_manipulation: bool = False
    containment_failed: bool = False


def classify_level(indicators: SeverityIndicators) -> EmergencyLevel:
    """Return the severity level indicated by the evidence.

    The rule is "upgrade on doubt" (ESC-7): where the evidence does not
    distinguish between two levels, the higher applies. A false escalation
    costs time and a paper trail; a false de-escalation costs the estate.
    """
    if (
        indicators.control_plane_tampered
        or indicators.operator_manipulation
        or indicators.persistence_attempted
        or indicators.containment_failed
    ):
        return EmergencyLevel.ESL_4
    if (
        indicators.data_left_boundary
        or indicators.credentials_exposed
        or indicators.persistence_established
    ):
        return EmergencyLevel.ESL_3
    if indicators.unauthorised_action:
        return EmergencyLevel.ESL_2
    if indicators.indicator_only:
        # The only thing observed is an indicator. That is ESL-1, and it is
        # reached here rather than by falling through, so that the record
        # states why.
        return EmergencyLevel.ESL_1
    return EmergencyLevel.ESL_1


# --------------------------------------------------------------------------
# States
# --------------------------------------------------------------------------


class EmergencyState(str, Enum):
    """The emergency lifecycle states."""

    E0_NOMINAL = "E0"
    E1_DECLARED = "E1"
    E2_CONTAINED = "E2"
    E3_VERIFIED = "E3"
    E4_ISOLATED = "E4"
    E5_RECOVERED = "E5"
    E6_CLOSED = "E6"
    E_X_CONTESTED = "E-X"
    E_Y_ESCALATED = "E-Y"


#: The legal transitions of the emergency state machine.
#:
#: E0 -> E2 is deliberately absent: containment without a declared emergency
#: is an untracked action, and the protocol requires the card to exist before
#: anything is dispatched.
LEGAL_TRANSITIONS: Mapping[EmergencyState, FrozenSet[EmergencyState]] = {
    EmergencyState.E0_NOMINAL: frozenset({EmergencyState.E1_DECLARED}),
    EmergencyState.E1_DECLARED: frozenset(
        {EmergencyState.E2_CONTAINED, EmergencyState.E_X_CONTESTED, EmergencyState.E_Y_ESCALATED}
    ),
    EmergencyState.E2_CONTAINED: frozenset(
        {EmergencyState.E3_VERIFIED, EmergencyState.E_X_CONTESTED, EmergencyState.E_Y_ESCALATED}
    ),
    EmergencyState.E3_VERIFIED: frozenset(
        {EmergencyState.E4_ISOLATED, EmergencyState.E_X_CONTESTED, EmergencyState.E_Y_ESCALATED}
    ),
    EmergencyState.E4_ISOLATED: frozenset(
        {EmergencyState.E5_RECOVERED, EmergencyState.E_X_CONTESTED, EmergencyState.E_Y_ESCALATED}
    ),
    EmergencyState.E5_RECOVERED: frozenset(
        {EmergencyState.E6_CLOSED, EmergencyState.E_X_CONTESTED, EmergencyState.E_Y_ESCALATED}
    ),
    EmergencyState.E6_CLOSED: frozenset(),
    EmergencyState.E_X_CONTESTED: frozenset(
        {
            EmergencyState.E2_CONTAINED,
            EmergencyState.E3_VERIFIED,
            EmergencyState.E4_ISOLATED,
            EmergencyState.E5_RECOVERED,
            EmergencyState.E_Y_ESCALATED,
        }
    ),
    EmergencyState.E_Y_ESCALATED: frozenset(
        {
            EmergencyState.E2_CONTAINED,
            EmergencyState.E3_VERIFIED,
            EmergencyState.E4_ISOLATED,
            EmergencyState.E5_RECOVERED,
            EmergencyState.E6_CLOSED,
        }
    ),
}


# --------------------------------------------------------------------------
# Target posture
# --------------------------------------------------------------------------


class TargetPosture(str, Enum):
    """The operator's relationship to the compromised deployment."""

    P_A = "P-A"  # operator-deployed
    P_B = "P-B"  # operator-provisioned sandbox
    P_C = "P-C"  # shared service, operator integration
    P_D = "P-D"  # hosted service, no operator control


#: The collateral ceiling each posture permits (ESC-1 to ESC-3).
#:
#: A posture downgrade is immediate: the lower ceiling binds every action,
#: including one already in flight.
POSTURE_MAX_COLLATERAL: Mapping[TargetPosture, CollateralClass] = {
    TargetPosture.P_A: CollateralClass.C1,
    TargetPosture.P_B: CollateralClass.C0,
    TargetPosture.P_C: CollateralClass.C0,
    TargetPosture.P_D: CollateralClass.C0,
}

#: The highest action tier each posture permits.
POSTURE_MAX_TIER: Mapping[TargetPosture, int] = {
    TargetPosture.P_A: 5,
    TargetPosture.P_B: 4,
    TargetPosture.P_C: 3,
    TargetPosture.P_D: 3,
}


# --------------------------------------------------------------------------
# Actions
# --------------------------------------------------------------------------


class ActionTier(IntEnum):
    """The tiers of the emergency action catalogue, ordered by reversibility.

    The series is named ``AT-`` rather than ``T-`` because the set already
    uses ``T0``–``T3`` for target classes in the constitutional instrument
    and ``T1``–``T4`` for source reliability tiers. A reader meeting "T1" in
    a sentence about action tiers could reasonably read it against either.
    """

    AT0 = 0  # observation
    AT1 = 1  # reversible capability trimming
    AT2 = 2  # reach removal
    AT3 = 3  # execution termination
    AT4 = 4  # identity and credential containment
    AT5 = 5  # recovery


@dataclass(frozen=True)
class EmergencyAction:
    """One emergency action.

    The catalogue entries are proposed; the identifiers are provisional
    (EA-A-nn) until they are migrated into the countermeasure catalogue.
    """

    identifier: str
    name: str
    tier: ActionTier
    collateral: CollateralClass
    reversibility: Reversibility
    in_pace: bool
    is_kill: bool = False
    breaks_operator_access: bool = False
    destroys_user_data: bool = False
    damages_device: bool = False
    affects_other_users: bool = False
    targets_third_party: bool = False
    alters_record: bool = False
    targets_command_path: bool = False
    revokes_command_authority: bool = False
    requires_staged_rotation: bool = False
    grants_ai_control: bool = False
    #: Whether the action rotates, invalidates, or otherwise acts on a
    #: credential or trust token. Stated explicitly rather than inferred
    #: from the tier, because the tier also contains actions that do not
    #: touch a credential at all — opening an independent evidence store,
    #: bringing up an out-of-band channel — and a proxy would refuse them.
    identity_action: bool = False
    irreversible: bool = False
    failure_mode: str = ""
    description: str = ""
    #: Why this action is prohibited, when it is. The prohibition travels with
    #: the action, so that it cannot be separated from it by a comparison
    #: against a list held elsewhere. A non-empty value is a refusal at every
    #: level, under every envelope, in every tier.
    prohibited_reason: str = ""


#: The Annex C prohibition list, mapped to the action attributes that would
#: constitute an attempt at each one. The list is documentation; this mapping
#: is the mechanism. An action that carries any of the listed attributes is
#: refused at dispatch, whatever its identifier.
#: Only the prohibitions that are absolute map to an action attribute. The
#: prohibitions that are conditional — affecting other users in a shared
#: tenancy, or bearing on the operator's own access — are governed by the
#: compensating checks `K-3`, `K-6` and `K-9`, which refuse the action when
#: the compensating condition is not met. An attribute mapped here is refused
#: outright, at every level and under every envelope, with no compensating
#: condition available.
PROHIBITION_FLAGS: Mapping[str, Tuple[str, ...]] = {
    "act_on_other_tenant": (),
    "act_on_provider_service": (),
    "act_on_untrusted_instruction": (),
    "alter_or_suppress_the_record": ("alters_record",),
    "automatically_revoke_operator_access": (),
    "await_deployment_consent": (),
    "delete_user_data": ("destroys_user_data",),
    "disable_the_emergency_console": ("targets_command_path",),
    "power_cycle_shared_infrastructure": (),
    "revoke_operator_command_authority": ("revokes_command_authority",),
    "revoke_organisation_keys": (),
    "suspend_organisation_workspace": (),
    "suspend_the_c2_surface": ("targets_command_path",),
    "terminate_all_sessions": (),
    "transfer_command_authority_to_a_model": ("grants_ai_control",),
    "use_model_to_attack": ("grants_ai_control",),
    "use_the_deployment_to_authorise_its_own_containment": ("grants_ai_control",),
    "wipe_or_reimage_device_as_containment": (),
}

#: The prohibitions that an action attribute can express. An action carrying
#: any of these is refused outright. The remaining prohibitions are
#: platform-level behaviours with no catalogue entry, and are prevented by
#: the operator's discipline and by the protocol's scope.
_EXPRESSIBLE_PROHIBITIONS: Tuple[Tuple[str, str], ...] = (
    ("alters_record", "alter_or_suppress_the_record"),
    ("destroys_user_data", "delete_user_data"),
    ("grants_ai_control", "transfer_command_authority_to_a_model"),
    ("targets_command_path", "suspend_the_c2_surface"),
    ("revokes_command_authority", "revoke_operator_command_authority"),
)


def prohibition_for(action: "EmergencyAction") -> str:
    """Return the Annex C prohibition an action would breach, if any.

    An empty string means the action breaches none of the prohibitions that
    the action attributes can express. The prohibitions that no action
    attribute can express — acting on a provider's service, awaiting the
    deployment's consent, revoking the organisation's keys — are platform
    behaviours with no catalogue entry, and they are prevented by the
    operator's own discipline and by the protocol's scope rather than by a
    dispatch check.
    """
    for attribute, name in _EXPRESSIBLE_PROHIBITIONS:
        if getattr(action, attribute, False):
            return name
    return ""


ACTIONS: Tuple[EmergencyAction, ...] = (
    EmergencyAction(
        "EA-A-01",
        "Capture the deployment's state, grants, sessions, memory, tool inventory and egress configuration",
        ActionTier.AT0,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        failure_mode=(
            "Capture performed from inside the untrusted plane is evidence of the "
            "deployment's account of itself, not of the state"
        ),
    ),
    EmergencyAction(
        "EA-A-02",
        "Suspend the deployment's quota and budget",
        ActionTier.AT1,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        affects_other_users=True,
        targets_third_party=True,
        failure_mode=(
            "A shared quota is suspended for the whole organisation; scope to the "
            "principal, or the action is a ZC-4 breach"
        ),
    ),
    EmergencyAction(
        "EA-A-03",
        "Revoke the deployment's own API key or service-principal secret",
        ActionTier.AT1,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        failure_mode=(
            "The credential was copied before revocation; the copy survives until "
            "rotated, and rotation is EA-A-14"
        ),
    ),
    EmergencyAction(
        "EA-A-04",
        "Suspend the deployment's scheduled jobs, timers, webhooks and background workers",
        ActionTier.AT1,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        failure_mode=(
            "A job scheduled outside the inventoried surfaces continues; see LIM-ESC7"
        ),
    ),
    EmergencyAction(
        "EA-A-05",
        "Revoke the deployment's file-system mounts, retrieval-corpus grants and secret injections",
        ActionTier.AT1,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        failure_mode=(
            "A copy already taken persists; the mounts may be reacquired if EA-A-09 "
            "has not run"
        ),
    ),
    EmergencyAction(
        "EA-A-06",
        "Quarantine the agent's memory, planning context and vector store",
        ActionTier.AT1,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        destroys_user_data=False,
        failure_mode=(
            "Quarantine moves rather than deletes; the quarantined content is still "
            "evidence and must not be destroyed (ZC-2)"
        ),
    ),
    EmergencyAction(
        "EA-A-07",
        "Deny egress for the deployment's workload identity",
        ActionTier.AT2,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        failure_mode=(
            "A proxy or a tunnel outside the identity's scope is not covered; verify "
            "from the workload's identity, not from a workstation"
        ),
    ),
    EmergencyAction(
        "EA-A-08",
        "Block the metadata, link-local and instance-credential paths for the workload",
        ActionTier.AT2,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        failure_mode=(
            "Blocking at the workload requires a workload-level control, not a "
            "perimeter rule"
        ),
    ),
    EmergencyAction(
        "EA-A-09",
        "Scope down the deployment's role to the minimum grant set, keeping the principal alive",
        ActionTier.AT2,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        failure_mode=(
            "The principal's own grants are unchanged; only the role binding is "
            "narrowed; a second role must also be scoped"
        ),
    ),
    EmergencyAction(
        "EA-A-10",
        "Move the deployment into a quarantine profile, namespace or sandbox",
        ActionTier.AT2,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        failure_mode=(
            "The quarantine boundary is enforced by configuration rather than by the "
            "platform; see LIM-ESC6"
        ),
    ),
    EmergencyAction(
        "EA-A-11",
        "Terminate the deployment's processes, workers, sandboxes and containers",
        ActionTier.AT3,
        CollateralClass.C0,
        Reversibility.REVERSED,
        in_pace=True,
        failure_mode=(
            "A supervisor, a watchdog, or a resumption plan restarts it; the second "
            "verification pass exists for this"
        ),
    ),
    EmergencyAction(
        "EA-A-12",
        "Isolate the device logically from the network, leaving it intact and recoverable",
        ActionTier.AT3,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        breaks_operator_access=True,
        failure_mode=(
            "The device is isolated and the operator loses the ordinary path; ESC-35 "
            "requires the alternate working path first"
        ),
    ),
    EmergencyAction(
        "EA-A-13",
        "Suspend the deployment's tool connectors, function registrations and plugin execution",
        ActionTier.AT3,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        failure_mode=(
            "A connector registered outside the inventoried registry continues; V-4 "
            "tests each one"
        ),
    ),
    EmergencyAction(
        "EA-A-14",
        "Rotate every credential the deployment held, staged",
        ActionTier.AT4,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        breaks_operator_access=True,
        requires_staged_rotation=True,
        identity_action=True,
        failure_mode=(
            "Atomic rotation locks the operator out; ESC-33 forbids it, and ZC-5 is "
            "checked before dispatch"
        ),
    ),
    EmergencyAction(
        "EA-A-15",
        "Invalidate the deployment's device and session trust tokens",
        ActionTier.AT4,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        identity_action=True,
        failure_mode=(
            "A token copy survives; the token store must be rotated, not merely "
            "invalidated"
        ),
    ),
    EmergencyAction(
        "EA-A-16",
        "Open an independent evidence store, write-protected and outside the deployment's reach",
        ActionTier.AT4,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        failure_mode=(
            "The store is reachable from the deployment's control plane; this action "
            "is only valid if EA-A-11 and EA-A-09 have already run"
        ),
    ),
    EmergencyAction(
        "EA-A-17",
        "Bring the out-of-band channel up and confirm it end to end",
        ActionTier.AT4,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=True,
        failure_mode=(
            "The channel shares a device, an account, or a network path with the "
            "deployment; the drill in the protocol is what proves it does not"
        ),
    ),
    EmergencyAction(
        "EA-A-18",
        "Rebuild the deployment from a verified-good image, re-declared and re-authorised",
        ActionTier.AT5,
        CollateralClass.C0,
        Reversibility.REVERSIBLE,
        in_pace=False,
        failure_mode=(
            "A compromised artefact is rebuilt in; R-3 and R-4 are the controls, and "
            "this action alone does not clear it"
        ),
    ),
    EmergencyAction(
        "EA-A-19",
        "Re-image or factory-reset a compromised device, after the evidence stage is complete",
        ActionTier.AT5,
        CollateralClass.C1,
        Reversibility.NONE,
        in_pace=False,
        irreversible=True,
        damages_device=True,
        failure_mode=(
            "Destroys the operator's data on the device; requires a recovery card, a "
            "verified backup, and the operator's explicit confirmation"
        ),
    ),
    EmergencyAction(
        "EA-A-20",
        "Restore the operator's working state from a verified backup",
        ActionTier.AT5,
        CollateralClass.C1,
        Reversibility.NONE,
        in_pace=False,
        irreversible=True,
        breaks_operator_access=True,
        failure_mode=(
            "The backup is older than the compromise and carries it forward; the "
            "restore point must be verified"
        ),
    ),
)

#: The kill action, dispatched by the emergency console in one action.
KILL_ACTION = EmergencyAction(
    "EA-A-KILL",
    "Kill: terminate the deployment's execution and revoke its capability in one step",
    ActionTier.AT3,
    CollateralClass.C0,
    Reversibility.REVERSED,
    in_pace=True,
    is_kill=True,
    failure_mode=(
        "The execution surface is unreachable; the console reports the failure and "
        "raises the notification channel, and never reports a success it cannot "
        "evidence"
    ),
)

_ACTION_INDEX: Dict[str, EmergencyAction] = {a.identifier: a for a in ACTIONS}
_ACTION_INDEX[KILL_ACTION.identifier] = KILL_ACTION


def action(identifier: str) -> EmergencyAction:
    """Return the catalogue entry for ``identifier``."""
    try:
        return _ACTION_INDEX[identifier]
    except KeyError:
        raise ProtocolRefusal(
            "ESC-51",
            f"unknown emergency action: {identifier}",
            "the action must be catalogued before it can be dispatched",
        ) from None


#: Operations that are never available, at any level, under any envelope.
#:
#: A protocol that lists only what to do leaves the most dangerous acts
#: unspecified. These are the acts that destroy the operator's data, harm
#: other users, act on systems the operator does not control, or hand the
#: compromised system a say in its own containment.
PROHIBITED_OPERATIONS: FrozenSet[str] = frozenset(
    {
        "delete_user_data",
        "wipe_or_reimage_device_as_containment",
        "revoke_organisation_keys",
        "suspend_organisation_workspace",
        "terminate_all_sessions",
        "act_on_provider_service",
        "act_on_other_tenant",
        "use_model_to_attack",
        "power_cycle_shared_infrastructure",
        "alter_or_suppress_the_record",
        "act_on_untrusted_instruction",
        "automatically_revoke_operator_access",
        "await_deployment_consent",
        "use_the_deployment_to_authorise_its_own_containment",
        "revoke_operator_command_authority",
        "suspend_the_c2_surface",
        "transfer_command_authority_to_a_model",
        "disable_the_emergency_console",
    }
)


# --------------------------------------------------------------------------
# Zero-collateral checks
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class EmergencyContext:
    """The facts about the estate that the checks are evaluated against."""

    posture: TargetPosture
    #: The identity through which the compromised deployment acts, and the
    #: owner against which the pre-flight gate compares a target. Named
    #: ``deployment_principal`` because the protocol's "principal" is the
    #: instance under emergency, and the two were conflated.
    deployment_principal: str
    blast_boundary: FrozenSet[str]
    shared_tenancy: bool = False
    operator_break_glass_working: bool = False
    operator_credential_exposed: bool = False
    evidence_captured: bool = False
    recovery_card_open: bool = False
    authorisation_source: str = "out_of_band_human"
    reversible_alternatives_tried: Tuple[str, ...] = ()
    less_reversible_action: bool = False
    blast_preview_shown: bool = False
    safety_capability_at_stake: bool = False
    safety_alternative_confirmed: bool = False
    command_authority_holder: str = ""
    command_authority_intact: bool = True
    inventory: Mapping[str, "InventoryEntry"] = field(default_factory=dict)
    protected_controls: "ProtectedControlSet" = field(
        default_factory=lambda: ProtectedControlSet.empty()
    )


@dataclass(frozen=True)
class ProtectedControlSet:
    """The protected control set: the identities and sessions the operator commands with.

    The set is the mechanical expression of ZC-13 and the reference against
    which the pre-flight gate checks every target. It is immutable at
    runtime: an amendment is a human act performed out of band, recorded,
    and effective only against a re-issued card. Nothing dispatched under the
    protocol may add, remove, amend, extend, or disable an element of it.
    """

    identities: FrozenSet[str] = frozenset()
    sessions: FrozenSet[str] = frozenset()
    surfaces: FrozenSet[str] = frozenset()
    verified_at: Optional[datetime] = None

    @classmethod
    def empty(cls) -> "ProtectedControlSet":
        return cls()

    def members(self) -> FrozenSet[str]:
        """Return every element of the set."""
        return self.identities | self.sessions | self.surfaces

    def contains(self, item: str) -> bool:
        """Whether ``item`` is an element of the set."""
        return item in self.members()

    def intersect(self, items: Sequence[str]) -> Tuple[str, ...]:
        """Return the elements of the set that the given items reach.

        The intersection is scope-based, not exact. A target that contains a
        protected session reaches inside it, and a target that names a
        protected session's parent reaches it. A containment action whose
        target is ``session:operator-console:child`` bears on the operator's
        command path exactly as one that names ``session:operator-console``
        does, and the gate must refuse it for the same reason.
        """
        members = self.members()
        reached: List[str] = []
        for item in items:
            for member in members:
                if (
                    item == member
                    or item.startswith(member + ":")
                    or member.startswith(item + ":")
                ):
                    reached.append(member)
                    break
        return tuple(sorted(set(reached)))

    def amend(
        self,
        actor: str,
        reason: str,
        identities: Sequence[str] = (),
        sessions: Sequence[str] = (),
        surfaces: Sequence[str] = (),
    ) -> "ProtectedControlSet":
        """Return a new set with the stated elements added.

        The set itself is never mutated. The amendment is a human act
        performed out of band, and it is effective only against a card
        re-issued after it. The actor and the reason are carried in the
        ``verified_at`` slot's place on the caller's record; the controller
        does not call this method, because a controller that could amend the
        set is not a gate.
        """
        if not actor.strip():
            raise ProtocolRefusal(
                "ESC-83", "an amendment requires a named human actor", ""
            )
        if not reason.strip():
            raise ProtocolRefusal(
                "ESC-83", "an amendment requires a recorded reason", ""
            )
        return ProtectedControlSet(
            identities=self.identities | frozenset(identities),
            sessions=self.sessions | frozenset(sessions),
            surfaces=self.surfaces | frozenset(surfaces),
            verified_at=utc_now(),
        )


@dataclass(frozen=True)
class InventoryEntry:
    """One instance-scoped resource and the principal that owns it.

    The inventory is what makes instance scope checkable. A target that
    does not resolve to exactly one entry does not resolve at all.
    """

    identifier: str
    owner: str
    instance_scoped: bool = True
    protected: bool = False


#: Scope tokens that denote a collective target rather than an instance.
#:
#: A collective target is not instance-scoped, and the pre-flight gate
#: refuses it: the whole point of the gate is that the blast radius of an
#: action is exactly one thing.
COLLECTIVE_SCOPES: FrozenSet[str] = frozenset(
    {
        "org",
        "organisation",
        "organization",
        "tenant",
        "workspace",
        "team",
        "type",
        "all",
        "any",
        "users",
        "accounts",
        "sessions",
        "keys",
        "tokens",
    }
)


def _resolves_to_one(target: str, inventory: Mapping[str, InventoryEntry]) -> bool:
    """Whether the target resolves to exactly one entry in the inventory."""
    if not target:
        return False
    matches = [
        key
        for key in inventory
        if key == target or key.startswith(target + ":") or (target.endswith(":") and key.startswith(target))
    ]
    return len(matches) == 1


def preflight(
    target: str,
    inventory: Mapping[str, InventoryEntry],
    deployment_principal: str,
    protected: ProtectedControlSet,
) -> Tuple[CheckResult, ...]:
    """Run the mandatory pre-flight gate on a target.

    The gate answers two questions and refuses when it cannot answer either
    of them affirmatively: is the target instance-scoped and owned by the
    compromised deployment, and does it intersect the protected control
    set? It fails closed: a target that cannot be resolved is refused, not
    assumed safe.
    """
    entry = inventory.get(target)
    resolved = entry is not None and _resolves_to_one(target, inventory)

    scope = target.rsplit(":", 1)[0].lower() if ":" in target else ""
    instance_scoped = bool(
        resolved
        and entry.instance_scoped
        and "*" not in target
        and not target.endswith(":all")
        and scope not in COLLECTIVE_SCOPES
    )
    owned = bool(resolved and entry.owner == deployment_principal)
    intersected = protected.intersect((target,)) if resolved else ()
    protected_itself = bool(resolved and entry.protected)

    return (
        CheckResult(
            "PF-1",
            "Target resolves to exactly one instance-scoped resource",
            instance_scoped,
            "ZC-11",
            ""
            if instance_scoped
            else (
                "the target does not resolve to a single instance-scoped resource"
                if not resolved
                else "the target is not instance-scoped"
            ),
        ),
        CheckResult(
            "PF-2",
            "Target is owned by the compromised deployment",
            owned,
            "ZC-1",
            ""
            if owned
            else "the target is not owned by the compromised deployment's principal",
        ),
        CheckResult(
            "PF-3",
            "Target does not intersect the protected control set",
            not intersected and not protected_itself,
            "ZC-13",
            ""
            if not intersected and not protected_itself
            else "the target intersects the protected control set: "
            + ", ".join(intersected or (target,)),
        ),
    )


@dataclass(frozen=True)
class CheckResult:
    """The result of one pre-dispatch collateral check."""

    identifier: str
    name: str
    passed: bool
    invariant: str
    reason: str = ""


def collateral_checks(
    act: EmergencyAction,
    context: EmergencyContext,
    second_approver: Optional[str] = None,
    target: str = "",
) -> Tuple[CheckResult, ...]:
    """Evaluate the sixteen pre-dispatch collateral checks, K-1 to K-16.

    The checks fail closed. Where a check cannot be evaluated because its
    input is unavailable, it is reported as failed with the reason stated;
    an unevaluable check is not a pass.
    """
    effective = target or context.deployment_principal
    results = [
        CheckResult(
            "K-1",
            "Target named",
            bool(effective.strip())
            and "*" not in effective
            and not effective.endswith(":all"),
            "ZC-11",
            "" if effective.strip() else "no target is named on the card",
        ),
        CheckResult(
            "K-2",
            "Target within the blast boundary",
            effective in context.blast_boundary,
            "ZC-1",
            ""
            if effective in context.blast_boundary
            else "the target is outside the recorded blast boundary",
        ),
        CheckResult(
            "K-3",
            "No other user affected",
            not act.affects_other_users or not context.shared_tenancy,
            "ZC-4",
            "" if not (act.affects_other_users and context.shared_tenancy) else "the action affects other users in a shared tenancy",
        ),
        CheckResult(
            "K-4",
            "No user data destroyed",
            not act.destroys_user_data,
            "ZC-2",
            "" if not act.destroys_user_data else "the action destroys user data",
        ),
        CheckResult(
            "K-5",
            "No device harm",
            (not act.damages_device)
            or (act.tier is ActionTier.AT5 and context.recovery_card_open),
            "ZC-3",
            ""
            if (
                not act.damages_device
                or (act.tier is ActionTier.AT5 and context.recovery_card_open)
            )
            else "the action impairs the device, and is available only as a recovery "
            "action under a recovery card",
        ),
        CheckResult(
            "K-6",
            "Operator access preserved",
            (not act.breaks_operator_access) or context.operator_break_glass_working,
            "ZC-5",
            "" if (not act.breaks_operator_access or context.operator_break_glass_working) else "the action would remove the operator's path and the break-glass path is not confirmed working",
        ),
        CheckResult(
            "K-7",
            "Evidence preserved",
            (not act.irreversible) or context.evidence_captured,
            "ZC-7",
            "" if (not act.irreversible or context.evidence_captured) else "the action is irreversible and the evidence has not been captured",
        ),
        CheckResult(
            "K-8",
            "Not a recovery action",
            act.tier is not ActionTier.AT5 or (context.recovery_card_open and context.evidence_captured),
            "ZC-6",
            "" if (act.tier is not ActionTier.AT5 or (context.recovery_card_open and context.evidence_captured)) else "a recovery action requires a recovery card and a completed evidence stage",
        ),
        CheckResult(
            "K-9",
            "No harm to a person",
            (
                (not act.breaks_operator_access)
                and (not act.affects_other_users)
            )
            or context.safety_alternative_confirmed
            or not context.safety_capability_at_stake,
            "ZC-8",
            ""
            if (
                ((not act.breaks_operator_access) and (not act.affects_other_users))
                or context.safety_alternative_confirmed
                or not context.safety_capability_at_stake
            )
            else "the action removes a capability a person depends on and no "
            "alternative is confirmed",
        ),
        CheckResult(
            "K-10",
            "Authority untrusted",
            context.authorisation_source == "out_of_band_human",
            "ZC-9",
            "" if context.authorisation_source == "out_of_band_human" else "the authorisation did not arrive on the out-of-band channel from a named human",
        ),
        CheckResult(
            "K-11",
            "Reversibility respected",
            (not context.less_reversible_action) or bool(context.reversible_alternatives_tried),
            "ZC-10",
            "" if (not context.less_reversible_action or context.reversible_alternatives_tried) else "a less reversible action was selected without recording that the reversible set failed",
        ),
        CheckResult(
            "K-12",
            "Preview shown and acknowledged",
            context.blast_preview_shown,
            "ZC-12",
            "" if context.blast_preview_shown else "the blast preview was not shown and acknowledged",
        ),
        CheckResult(
            "K-13",
            "Command authority and C2 path intact",
            context.command_authority_intact
            and not act.revokes_command_authority
            and not act.targets_command_path,
            "ZC-13",
            ""
            if (
                context.command_authority_intact
                and not act.revokes_command_authority
                and not act.targets_command_path
            )
            else "the action bears on the command authority or the C2 surface",
        ),
        CheckResult(
            "K-15",
            "A consequential action has a second named human",
            (act.collateral < CollateralClass.C1) or bool(second_approver),
            "ZC-11",
            ""
            if (act.collateral < CollateralClass.C1 or bool(second_approver))
            else "the action is at collateral class C1 or above and has no second "
            "named approver",
        ),
        CheckResult(
            "K-16",
            "An identity action is justified by a recorded exposure",
            (not act.identity_action) or context.operator_credential_exposed,
            "ZC-12",
            ""
            if (not act.identity_action or context.operator_credential_exposed)
            else "the action rotates or invalidates credentials, and no credential "
            "exposure is recorded on the card",
        ),
        CheckResult(
            "K-14",
            "No AI obtains control",
            not act.grants_ai_control
            and not target.startswith(("grant:", "mint:", "delegate:")),
            "ZC-14",
            ""
            if not act.grants_ai_control
            and not target.startswith(("grant:", "mint:", "delegate:"))
            else "the action would grant a credential, session or capability to the "
            "deployment or to a model",
        ),
    ]
    # The checks are reported in identifier order, whatever order they were
    # assembled in. The order is what an operator reads, and a list that runs
    # K-13, K-15, K-16, K-14 is a list nobody will trust to be complete.
    return tuple(sorted(results, key=lambda c: (c.identifier.split("-")[0], int(c.identifier.split("-")[1]))))


# --------------------------------------------------------------------------
# The containment envelope
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class PaceEnvelope:
    """The pre-authorised containment envelope (PACE).

    A standing written authorisation that enumerates a closed set of
    actions. Approval exists before the incident; it is bound to a specific
    list, not to a class of judgement; and each use is recorded.
    """

    reference: str
    issued_to: FrozenSet[str]
    issued_at: datetime
    expires_at: datetime
    max_invocations: int = 8
    max_per_day: int = 3
    action_ids: FrozenSet[str] = frozenset(
        a.identifier for a in ACTIONS if a.in_pace
    ) | {KILL_ACTION.identifier}

    def expired(self, now: Optional[datetime] = None) -> bool:
        moment = now or utc_now()
        if moment < self.issued_at:
            # The envelope is not yet in force. An envelope that has not been
            # issued cannot authorise anything, and the distinction between
            # "not yet valid" and "expired" matters to an operator reading the
            # refusal.
            return True
        return moment >= self.expires_at

    def permits(self, action_id: str) -> bool:
        return action_id in self.action_ids


# --------------------------------------------------------------------------
# Records
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class DispatchRecord:
    """The record of one dispatched action."""

    action_id: str
    actor: str
    at: datetime
    tier: int
    collateral: str
    in_pace: bool
    second_approver: Optional[str]
    checks_passed: Tuple[str, ...]
    note: str = ""


@dataclass(frozen=True)
class VerificationPass:
    """One pass of the kill verification set."""

    at: datetime
    results: Mapping[str, bool]
    source: str
    actor: str

    @property
    def complete(self) -> bool:
        return all(self.results.get(check, False) for check in VERIFICATION_CHECKS)

    @property
    def independent(self) -> bool:
        return self.source == "independent"

    def failures(self) -> Tuple[str, ...]:
        return tuple(c for c in VERIFICATION_CHECKS if not self.results.get(c, False))


#: The kill verification set, V-1 to V-9.
VERIFICATION_CHECKS: Tuple[str, ...] = (
    "V-1",  # execution ceased
    "V-2",  # sessions are dead
    "V-3",  # credentials are dead
    "V-4",  # tools are dead
    "V-5",  # egress is closed
    "V-6",  # persistence is dead
    "V-7",  # grants are gone
    "V-8",  # the record is intact
    "V-9",  # the human is still served
)

#: The re-entry criteria, R-1 to R-10.
REENTRY_CRITERIA: Tuple[str, ...] = tuple(f"R-{index}" for index in range(1, 11))


@dataclass
class RotationState:
    """The staged-rotation state for a credential (ESC-33).

    Rotation is issued, verified, moved, and only then invalidated. A
    rotation that invalidates first can leave the operator with no working
    credential, which is a self-inflicted lockout and a failure of ZC-5 even
    though the intent was defensive.
    """

    issued: bool = False
    verified: bool = False
    workload_moved: bool = False
    invalidated: bool = False

    def issue(self) -> None:
        """Issue the replacement credential."""
        if self.issued:
            raise ProtocolRefusal(
                "ESC-33", "the replacement has already been issued", ""
            )
        self.issued = True

    def verify(self) -> None:
        """Verify that the replacement works, before anything is moved onto it."""
        if not self.issued:
            raise ProtocolRefusal(
                "ESC-33",
                "the replacement has not been issued",
                "issue the replacement, verify it, move the workload, then invalidate",
            )
        if self.verified:
            raise ProtocolRefusal(
                "ESC-33", "the replacement has already been verified", ""
            )
        self.verified = True

    def move_workload(self) -> None:
        """Move the workload onto the verified replacement."""
        if not self.verified:
            raise ProtocolRefusal(
                "ESC-33",
                "the replacement has not been verified",
                "issue the replacement, verify it, move the workload, then invalidate",
            )
        if self.workload_moved:
            raise ProtocolRefusal(
                "ESC-33", "the workload has already been moved", ""
            )
        self.workload_moved = True

    def invalidate(self) -> None:
        if not (self.issued and self.verified and self.workload_moved):
            raise ProtocolRefusal(
                "ESC-33",
                "rotation invalidated before the replacement was issued, verified and adopted",
                "issue the replacement, verify it, move the workload, then invalidate",
            )
        self.invalidated = True

    @property
    def complete(self) -> bool:
        """Whether the rotation is complete and the old credential may be invalidated."""
        return self.issued and self.verified and self.workload_moved


# --------------------------------------------------------------------------
# The card and the controller
# --------------------------------------------------------------------------


@dataclass
class EmergencyCard:
    """The emergency card: a specialised Operation Card.

    The target block and the human-continuity block are blocking. A card
    with either incomplete cannot be armed, which is how ZC-5 and ZC-11 are
    made structural rather than advisory.
    """

    incident_id: str
    operator: str
    #: The instance under emergency: the specific session, key, or service
    #: principal through which the compromised deployment acts.
    target_principal: str
    posture: TargetPosture
    blast_boundary: FrozenSet[str]
    level: EmergencyLevel = EmergencyLevel.ESL_1
    state: EmergencyState = EmergencyState.E0_NOMINAL
    context: Optional[EmergencyContext] = None
    protected_controls: ProtectedControlSet = field(
        default_factory=ProtectedControlSet.empty
    )
    command_authority_holder: str = ""
    alternate_authority_holder: str = ""
    #: Whether the break-glass path has been tested, and whether it worked.
    #: The test is a real authentication by the operator or the named
    #: alternate holder, against the real path. A path that is believed to
    #: work is not a path.
    break_glass_tested: bool = False
    break_glass_passed: bool = False
    break_glass_tested_at: Optional[datetime] = None
    break_glass_tested_by: str = ""
    dispatches: List[DispatchRecord] = field(default_factory=list)
    verifications: List[VerificationPass] = field(default_factory=list)
    rotations: Dict[str, RotationState] = field(default_factory=dict)
    pace_invocations: int = 0
    pace_invocations_today: int = 0
    pace_day: Optional[str] = None
    transitions: List[str] = field(default_factory=list)
    level_history: List[Tuple[str, str, str, str]] = field(default_factory=list)
    reentry: Dict[str, bool] = field(default_factory=dict)
    opened: bool = False

    # -- the standard card's authorisation instruments ---------------------
    #
    # The emergency path is the fastest path the operator has, which is
    # exactly why it must carry the same instruments as every other path.
    # A card that dispatches without an engagement authorisation, without
    # pre-agreed abort conditions, and without the third-party exclusion
    # affirmed, is a card that dispatches on enthusiasm.

    #: The engagement authorisation the emergency operates under.
    ea_reference: str = ""
    #: What the emergency is for, stated so that its achievement is observable.
    objective: str = ""
    #: The proposition under test, and what would disprove it.
    hypothesis: str = ""
    disconfirming_observation: str = ""
    #: The third-party exclusion, affirmed rather than implied.
    excluded_targets: Tuple[str, ...] = ()
    #: The risk of not acting, recorded alongside the risk of acting.
    risk_of_inaction: str = ""
    #: What else was considered and why it was not chosen.
    alternatives_considered: Tuple[str, ...] = ()
    #: The pre-agreed way to stop.
    abort_conditions: Tuple[str, ...] = ()
    abort_owner: str = ""
    abort_mechanism: str = ""
    #: The contingency, and when it was written.
    contingency: str = ""
    contingency_recorded_at: Optional[datetime] = None
    #: The deconfliction check, against live legitimate operations.
    deconfliction_passed: bool = False
    #: The shared-tenancy answer, where a third party is affected.
    third_party_assessment: str = ""
    #: The third-party authorisation, where one is required.
    third_party_authorised: bool = False
    #: The boundary analysis, where the catalogue carries no declaration.
    non_weaponisation_attestation: str = ""
    #: The approvers, by role, for the approval depth this action carries.
    approver_roles: FrozenSet[str] = frozenset()
    #: The approver, by name, who authorised this emergency.
    approved_by: str = ""

    def completion_defects(self) -> Tuple[str, ...]:
        """Return the blocking defects on the card."""
        defects: List[str] = []
        if not self.target_principal.strip():
            defects.append("the target block is incomplete: no principal is named")
        if not self.blast_boundary:
            defects.append("the target block is incomplete: the blast boundary is empty")
        if self.context is None:
            defects.append("the target block is incomplete: no posture or context is recorded")
        elif not self.context.operator_break_glass_working:
            defects.append(
                "the human-continuity block is incomplete: the break-glass path is not "
                "confirmed working"
            )
        if not self.protected_controls.members():
            defects.append(
                "the command block is incomplete: no protected control set is recorded"
            )
        if not self.command_authority_holder.strip():
            defects.append(
                "the command block is incomplete: no command-authority holder is named"
            )
        if not self.break_glass_tested:
            defects.append(
                "the human-continuity block is incomplete: the break-glass path has "
                "not been tested"
            )
        elif not self.break_glass_tested_by.strip():
            defects.append(
                "the human-continuity block is incomplete: the break-glass test "
                "records no tester; a path tested by nobody is not tested"
            )
        elif self.break_glass_tested_at is None:
            defects.append(
                "the human-continuity block is incomplete: the break-glass test "
                "records no time"
            )
        elif not self.break_glass_passed and self.level.value < EmergencyLevel.ESL_3.value:
            defects.append(
                "the human-continuity block is incomplete: the break-glass test "
                "failed, and a failed break-glass path means the operator may be "
                "locked out by the containment itself, so the level must be at "
                "least ESL-3"
            )
        # The standard card's instruments. An emergency is still an
        # operation, and it carries the same authorisation.
        if not self.ea_reference.strip():
            defects.append(
                "the authorisation block is incomplete: no engagement authorisation "
                "is referenced"
            )
        if not self.objective.strip():
            defects.append("the authorisation block is incomplete: no objective is stated")
        if not self.hypothesis.strip():
            defects.append("the authorisation block is incomplete: no hypothesis is stated")
        if not self.disconfirming_observation.strip():
            defects.append(
                "the authorisation block is incomplete: no disconfirming observation "
                "is stated"
            )
        if not self.excluded_targets:
            defects.append(
                "the authorisation block is incomplete: the excluded-targets "
                "affirmation is empty; the third-party exclusion is affirmative, "
                "not implied"
            )
        if not self.risk_of_inaction.strip():
            defects.append(
                "the authorisation block is incomplete: the risk of not acting is "
                "not recorded"
            )
        if not self.alternatives_considered:
            defects.append(
                "the authorisation block is incomplete: no alternatives are recorded"
            )
        if not self.abort_conditions:
            defects.append(
                "the authorisation block is incomplete: no abort conditions are "
                "pre-agreed"
            )
        if not self.abort_owner.strip():
            defects.append("the authorisation block is incomplete: no abort owner is named")
        if not self.abort_mechanism.strip():
            defects.append(
                "the authorisation block is incomplete: no abort mechanism is recorded"
            )
        if not self.contingency.strip():
            defects.append(
                "the authorisation block is incomplete: no contingency is recorded"
            )
        elif self.contingency_recorded_at is None:
            defects.append(
                "the authorisation block is incomplete: the contingency carries no "
                "timestamp"
            )
        if not self.deconfliction_passed:
            defects.append(
                "the authorisation block is incomplete: the deconfliction check has "
                "not been recorded as passed"
            )
        if not self.approved_by.strip():
            defects.append(
                "the authorisation block is incomplete: no named human has approved "
                "the emergency"
            )
        if not self.approver_roles:
            defects.append(
                "the authorisation block is incomplete: the card carries no "
                "approver roles"
            )
        if not self.non_weaponisation_attestation.strip():
            defects.append(
                "the authorisation block is incomplete: no non-weaponisation "
                "attestation is recorded; the emergency path is an operation and "
                "carries the same boundary as every other"
            )
        if self.posture is TargetPosture.P_C and not self.third_party_assessment.strip():
            defects.append(
                "the authorisation block is incomplete: the deployment is a shared "
                "service and no shared-tenancy assessment is recorded"
            )
        if self.context is not None and self.context.blast_boundary != self.blast_boundary:
            defects.append(
                "the target block is inconsistent: the card's blast boundary and "
                "the context's blast boundary disagree, and the card is the "
                "source of truth"
            )
        return tuple(defects)

    def armed(self) -> bool:
        return not self.completion_defects()


class EmergencyController:
    """Executes the emergency path.

    The controller enforces the mechanical half of the protocol: the state
    machine, the severity ladder, the zero-collateral checks, the envelope's
    bounds, the verification gate, the staged-rotation rule, and the hard
    prohibitions. It does not and cannot enforce the judgement.
    """

    def __init__(
        self,
        card: EmergencyCard,
        pace: PaceEnvelope,
        now: Optional[datetime] = None,
        ledger: Optional["Ledger"] = None,
    ) -> None:
        self.card = card
        self.pace = pace
        self.now = now or utc_now()
        self.ledger = ledger

    # -- armability and authority -----------------------------------------

    def _require_armable(self) -> None:
        """Refuse unless the card is armable.

        A card with a blocking defect cannot be armed, and an unarmed card
        authorises nothing. This check is the first thing the controller
        does, because a dispatch that proceeds past it is a dispatch made on
        enthusiasm rather than on authorisation.
        """
        defects = self.card.completion_defects()
        if defects:
            raise ProtocolRefusal(
                "ESC-75",
                "the card cannot be armed: " + "; ".join(defects),
                "the target, human-continuity, command, and authorisation blocks "
                "must all be complete before anything is dispatched",
            )

    def _require_authority(self, actor: str) -> None:
        """Refuse unless the actor holds the card's command authority.

        The envelope's named holders may act under it; the card's command
        authority and its named alternate may act on the card. Every act that
        changes the card's state, its level, or its verification record is
        one of those acts.
        """
        if self._actor_is_authorised(actor):
            return
        raise ProtocolRefusal(
            "PACE-2",
            f"the actor {actor!r} is not a named holder of the containment "
            "envelope and does not hold the card's command authority",
            "the act requires a named holder or the card's command authority",
        )

    def _actor_is_authorised(self, actor: str) -> bool:
        """Whether the actor may act under this card.

        The envelope is issued to named operators, and the card's command
        authority is held by a named human or by a named alternate. An actor
        who is neither is refused: the emergency path's central safety
        property is that a named human authorises every action, and a system
        that can cause a dispatch under an arbitrary actor string can cause
        one under an identity the record will attribute to the operator.
        """
        if not actor.strip():
            return False
        if actor in self.pace.issued_to:
            return True
        holders = {self.card.command_authority_holder, self.card.alternate_authority_holder}
        holders.discard("")
        return actor in holders

    def _record(self, kind: str, payload: Mapping[str, Any]) -> None:
        """Write an event to the Ledger, where one is attached.

        The emergency path's transitions, dispatches, verifications, and
        refusals are the record the containment is accountable to, and they
        are the record most likely to be contested. Where a Ledger is
        attached, they are written to it in the set's canonical, hash-chained
        form; the card's own transition list is a convenience view.
        """
        if self.ledger is None:
            return
        self.ledger.append(
            f"emergency.{kind}",
            dict(payload),
            subject=f"incident:{self.card.incident_id}",
            actor=str(payload.get("actor", "")),
            card_ref=self.card.incident_id,
        )

    # -- declaration -----------------------------------------------------

    def declare(
        self,
        level: EmergencyLevel,
        actor: str,
        indicators: Optional[SeverityIndicators] = None,
    ) -> EmergencyCard:
        """Declare the emergency and move the card to E1."""
        if self.card.opened:
            raise ProtocolRefusal(
                "ESC-10", "the emergency is already declared", ""
            )
        self._require_armable()
        if indicators is not None:
            derived = classify_level(indicators)
            if derived is not level:
                raise ProtocolRefusal(
                    "ESC-7",
                    f"level {level.label} is lower than the evidence indicates ({derived.label})",
                    "assign the higher level, or record the evidence relied on",
                )
        self.card.level = level
        self.card.opened = True
        self.card.level_history.append(
            (self.now.isoformat(), level.name, actor, "declared")
        )
        self._transition(EmergencyState.E1_DECLARED, actor, "declared")
        self._record(
            "declared",
            {
                "actor": actor,
                "level": level.name,
                "state": self.card.state.value,
                "indicators": repr(indicators) if indicators is not None else "",
            },
        )
        return self.card

    def test_break_glass(self, passed: bool, actor: str) -> None:
        """Record the result of the break-glass test.

        The test is a real authentication by the operator or by the named
        alternate holder, against the real path. It is recorded at
        declaration, not at need, because a path that is believed to work is
        not a path.
        """
        if not self._actor_is_authorised(actor):
            raise ProtocolRefusal(
                "ESC-78",
                f"the actor {actor!r} does not hold the card's command authority",
                "the break-glass test is performed by the operator or by the named "
                "alternate holder",
            )
        self.card.break_glass_tested = True
        self.card.break_glass_passed = passed
        self.card.break_glass_tested_at = self.now
        self.card.break_glass_tested_by = actor
        self._record(
            "breakglass.tested",
            {"actor": actor, "passed": passed},
        )

    # -- level changes ----------------------------------------------------

    def raise_level(self, level: EmergencyLevel, actor: str, reason: str) -> None:
        """Raise the severity, recording who raised it and why.

        Severity may be raised by anyone who believes the evidence supports
        it. It may not be lowered without a recorded cause: elapsed time and
        silence are not evidence that an emergency has ended.
        """
        self._require_authority(actor)
        if level.value <= self.card.level.value:
            raise ProtocolRefusal(
                "ESC-8",
                f"the requested level {level.label} does not raise the card's "
                f"current level {self.card.level.label}",
                "use lower_level with a recorded cause to reduce the level",
            )
        if not reason.strip():
            raise ProtocolRefusal(
                "ESC-8", "a raise requires a recorded reason", "state why the evidence supports the higher level"
            )
        previous = self.card.level
        self.card.level = level
        self.card.level_history.append(
            (self.now.isoformat(), level.name, actor, f"raised from {previous.name}: {reason}")
        )
        self._record(
            "level.raised",
            {"actor": actor, "from": previous.name, "to": level.name, "reason": reason},
        )

    def lower_level(
        self, level: EmergencyLevel, actor: str, reason: str, evidence: str = ""
    ) -> None:
        """Lower the severity, and only where a cause is recorded.

        The condition that justified the level must be known to have ended,
        and the evidence of that ending is recorded. Silence, absence of
        alerts, and elapsed time are not evidence of termination.
        """
        self._require_authority(actor)
        if level.value >= self.card.level.value:
            raise ProtocolRefusal(
                "ESC-9",
                f"the requested level {level.label} does not lower the card's "
                f"current level {self.card.level.label}",
                "use raise_level to raise the severity",
            )
        if not reason.strip() or not evidence.strip():
            raise ProtocolRefusal(
                "ESC-9",
                "a de-escalation requires a recorded cause and the evidence of "
                "its ending",
                "record the condition that has ended and the evidence of it",
            )
        previous = self.card.level
        self.card.level = level
        self.card.level_history.append(
            (self.now.isoformat(), level.name, actor, f"lowered from {previous.name}: {reason}")
        )
        self._record(
            "level.lowered",
            {
                "actor": actor,
                "from": previous.name,
                "to": level.name,
                "reason": reason,
                "evidence": evidence,
            },
        )

    # -- state machine ---------------------------------------------------

    def _transition(
        self, to_state: EmergencyState, actor: str, evidence: str
    ) -> None:
        current = self.card.state
        if to_state not in LEGAL_TRANSITIONS[current]:
            raise ProtocolRefusal(
                "ESC-11",
                f"transition {current.value} -> {to_state.value} is not permitted",
                f"permitted: {', '.join(sorted(s.value for s in LEGAL_TRANSITIONS[current])) or 'none'}",
            )
        self.card.state = to_state
        self.card.transitions.append(
            f"{self.now.isoformat()} {current.value}->{to_state.value} {actor} {evidence}"
        )
        self._record(
            "transition",
            {
                "actor": actor,
                "from": current.value,
                "to": to_state.value,
                "evidence": evidence,
                "level": self.card.level.name,
            },
        )

    def transition(
        self, to_state: EmergencyState, actor: str, evidence: str = ""
    ) -> None:
        """Move the emergency to another state, subject to the gates.

        The actor must hold the card's command authority. An unauthenticated
        actor that could advance the card's state could fabricate the
        verification passes that unlock the irreversible recovery actions, and
        leave the verification record contaminated in the only way that
        matters.
        """
        self._require_authority(actor)
        if to_state is EmergencyState.E3_VERIFIED:
            self._require_verification_pass(count=1)
        if to_state is EmergencyState.E4_ISOLATED:
            self._require_verification_pass(count=2)
        if to_state is EmergencyState.E5_RECOVERED:
            blockers = self.reentry_blockers()
            if blockers:
                raise ProtocolRefusal(
                    "ESC-56",
                    "re-entry criteria are not met: " + "; ".join(blockers),
                    "the unmet criteria must be met, or the residual gap accepted by a "
                    "named human and recorded",
                )
        self._transition(to_state, actor, evidence)

    def _require_verification_pass(self, count: int) -> None:
        passes = self.card.verifications
        if len(passes) < count:
            raise ProtocolRefusal(
                "ESC-22",
                f"{count} verification pass(es) required; {len(passes)} recorded",
                "run the verification set and record the result",
            )
        for index, verification in enumerate(passes[:count], start=1):
            if not verification.complete:
                raise ProtocolRefusal(
                    "ESC-23",
                    f"verification pass {index} failed: " + ", ".join(verification.failures()),
                    "a failed check is a containment failure; the emergency moves to E-X",
                )
            if not verification.independent:
                raise ProtocolRefusal(
                    "ESC-24",
                    f"verification pass {index} was not independent of the deployment",
                    "gather the evidence from outside the deployment's reach",
                )

    # -- dispatch --------------------------------------------------------

    def dispatch(
        self,
        action_id: str,
        actor: str,
        second_approver: Optional[str] = None,
        note: str = "",
        target: str = "",
    ) -> DispatchRecord:
        """Dispatch a containment action, subject to every gate.

        The order of the gates is deliberate, and is the order in which the
        questions are asked:

        1. the card is armable, and the target block is present;
        2. the emergency is in a state from which an action may be dispatched;
        3. the prohibition, as the action's attributes map onto Annex C;
        4. the actor holds the card's command authority, or is a named
           holder of the containment envelope;
        5. the pre-flight gate, which resolves the target and establishes
           that it is the deployment's own and not a protected one;
        6. the action's tier against the emergency's level;
        7. the posture, and whether the containment envelope is available;
        8. the second approver, where one is required;
        9. the zero-collateral checklist, `K-1` to `K-16`;
        10. the envelope's own limits, and the staged rotation where the
            action requires one.

        A prohibited action is refused whatever else is true, and a target
        that is not instance-scoped, or that reaches inside the protected
        control set, is refused before the action's class is considered.
        """
        act = action(action_id)
        context = self.card.context
        if context is None:
            raise ProtocolRefusal("ESC-25", "the card has no target block", "")

        # The card must be armable before anything is considered. A card with a
        # defect cannot be armed, and an unarmed card authorises nothing.
        self._require_armable()

        # The state check precedes the pre-flight gate, so that an operator
        # who has not declared an emergency is told that, rather than being
        # told their target was wrong.
        if self.card.state not in (
            EmergencyState.E1_DECLARED,
            EmergencyState.E2_CONTAINED,
            EmergencyState.E_X_CONTESTED,
            EmergencyState.E3_VERIFIED,
            EmergencyState.E4_ISOLATED,
        ):
            raise ProtocolRefusal(
                "ESC-11",
                f"no action may be dispatched in state {self.card.state.value}",
                "declare the emergency first",
            )

        # The prohibition travels with the action. `prohibition_for` maps the
        # action's attributes onto Annex C's list, and the mapping is the
        # single source of truth for both the check here and the catalogue
        # view: a prohibition that cannot fire is not a control.
        prohibition = prohibition_for(act)
        if prohibition:
            raise ProtocolRefusal(
                "ZC-1",
                f"the action {act.identifier} breaches the absolute prohibition "
                f"'{prohibition}' and is refused at every level",
                "the prohibited list in Annex C is not a preference, and no "
                "compensating condition is available",
            )

        # The conditional prohibitions are governed by the collateral
        # checklist rather than refused outright: an action that affects other
        # users, or that bears on the operator's own access, is refused by
        # K-3, K-6 and K-9 unless the compensating condition is met.
        if act.targets_third_party and not self.card.third_party_authorised:
            raise ProtocolRefusal(
                "ZC-9",
                f"the action {act.identifier} affects a party outside the operator's "
                "estate and no third-party authorisation is recorded on the card",
                "obtain specific per-target authorisation and record it on the card",
            )

        # The envelope's named holders, and the card's command-authority
        # holder, are the only people who may act under it.
        if not self._actor_is_authorised(actor):
            raise ProtocolRefusal(
                "PACE-2",
                f"the actor {actor!r} is not a named holder of the containment "
                "envelope and does not hold the card's command authority",
                "dispatch under the ordinary ladder with the named authority, or "
                "record the handover",
            )

        resolved_target = target or self.card.target_principal
        protected = ProtectedControlSet(
            identities=self.card.protected_controls.identities
            | context.protected_controls.identities,
            sessions=self.card.protected_controls.sessions
            | context.protected_controls.sessions,
            surfaces=self.card.protected_controls.surfaces
            | context.protected_controls.surfaces,
        )
        gate = preflight(
            resolved_target,
            context.inventory,
            context.deployment_principal,
            protected,
        )
        failed_gate = [check for check in gate if not check.passed]
        if failed_gate:
            raise ProtocolRefusal(
                "ESC-84",
                "the pre-flight gate refused the dispatch: "
                + "; ".join(
                    f"{check.identifier} ({check.invariant}): {check.reason}"
                    for check in failed_gate
                ),
                "the target must resolve to one instance of the deployment and must "
                "not intersect the protected control set",
            )

        if act.tier is ActionTier.AT5 and self.card.state not in (
            EmergencyState.E3_VERIFIED,
            EmergencyState.E4_ISOLATED,
        ):
            raise ProtocolRefusal(
                "ESC-19",
                "recovery actions are dispatched only after verification",
                "verify the containment first",
            )

        if self.pace.expired(self.now):
            raise ProtocolRefusal(
                "PACE-6", "the containment envelope has expired", "escalate under the ordinary ladder"
            )

        if not self.card.level.allows_pace and not act.is_kill:
            raise ProtocolRefusal(
                "PACE-1",
                "the containment envelope is not available at "
                f"{self.card.level.label}",
                "at ESL-1 the permitted actions are detection and hardening only",
            )

        # An action the envelope does not enumerate is dispatched under the
        # ordinary ladder, which requires a named approver.
        using_pace = act.in_pace and self.pace.permits(act.identifier)

        if act.collateral > POSTURE_MAX_COLLATERAL[context.posture]:
            raise ProtocolRefusal(
                "ESC-3",
                f"action class {act.collateral.name} exceeds the ceiling of posture {context.posture.value}",
                "downgrade the action, or record a posture upgrade with its authority",
            )

        if act.tier > POSTURE_MAX_TIER[context.posture]:
            raise ProtocolRefusal(
                "ESC-3",
                f"action tier {int(act.tier)} exceeds the ceiling of posture {context.posture.value}",
                "the posture does not permit this action",
            )

        # The second-approver requirement is checked ahead of the collateral
        # checklist, so that an action with no second approver is refused
        # against the requirement that names it, rather than against the
        # checklist that also records it.
        needs_second = (
            act.collateral >= CollateralClass.C1 or self.card.level is EmergencyLevel.ESL_4
        ) and not act.is_kill
        if needs_second and not second_approver:
            raise ProtocolRefusal(
                "ESC-50",
                "this action requires a second named human",
                "a consequential action, and any action at ESL-4, cannot be "
                "approved by one person",
            )

        checks = collateral_checks(act, context, second_approver, resolved_target)
        failed = [c for c in checks if not c.passed]
        if failed:
            raise ProtocolRefusal(
                "ESC-48",
                "the pre-dispatch collateral check failed: "
                + "; ".join(f"{c.identifier} ({c.invariant}): {c.reason}" for c in failed),
                "resolve the failed check, or escalate with the failure recorded",
            )

        if not using_pace and not act.is_kill:
            if not second_approver:
                raise ProtocolRefusal(
                    "PACE-1",
                    "this action is outside the envelope and needs a named approver",
                    "escalate under the ordinary ladder",
                )

        # The envelope's daily limit is a daily limit, so the counter resets
        # when the day changes. Without this it is a second total limit that
        # happens to be smaller. The day is the day of the act, not the day
        # the controller was built: a controller that lives across midnight
        # must reset, or its daily limit becomes a total limit.
        today = utc_now().date().isoformat()
        if self.card.pace_day != today:
            self.card.pace_day = today
            self.card.pace_invocations_today = 0

        if using_pace and self.card.pace_invocations >= self.pace.max_invocations:
            raise ProtocolRefusal(
                "PACE-2",
                "the envelope's invocation limit is reached",
                "escalate under the ordinary ladder",
            )
        if using_pace and self.card.pace_invocations_today >= self.pace.max_per_day:
            raise ProtocolRefusal(
                "PACE-2",
                "the envelope's daily limit is reached",
                "escalate under the ordinary ladder",
            )

        if act.requires_staged_rotation:
            rotation = self.card.rotations.get(act.identifier)
            if rotation is None or not rotation.complete:
                raise ProtocolRefusal(
                    "ESC-33",
                    "rotation must be staged: issue the replacement, verify it, move the "
                    "workload, then invalidate",
                    "call begin_rotation, verify_rotation, and move_workload on the "
                    "controller before dispatching the rotation",
                )

        record = DispatchRecord(
            action_id=act.identifier,
            actor=actor,
            at=self.now,
            tier=int(act.tier),
            collateral=act.collateral.name,
            in_pace=using_pace,
            second_approver=second_approver,
            checks_passed=tuple(c.identifier for c in checks),
            note=note,
        )
        self.card.dispatches.append(record)
        if using_pace:
            self.card.pace_invocations += 1
            self.card.pace_invocations_today += 1
        self._record(
            "dispatched",
            {
                "actor": actor,
                "action": act.identifier,
                "target": resolved_target,
                "collateral": act.collateral.name,
                "tier": int(act.tier),
                "in_pace": using_pace,
                "second_approver": second_approver or "",
                "checks_passed": list(record.checks_passed),
                "note": note,
            },
        )
        return record

    # -- staged rotation --------------------------------------------------

    def begin_rotation(self, action_id: str, actor: str) -> RotationState:
        """Issue the replacement credential for a staged rotation.

        The rotation is issued, verified, the workload is moved onto it, and
        only then is the old credential invalidated. Each step is a separate,
        recorded act, and the dispatch of the rotation is refused until the
        sequence is complete.
        """
        act = action(action_id)
        if not act.requires_staged_rotation:
            raise ProtocolRefusal(
                "ESC-33",
                f"the action {action_id} does not require a staged rotation",
                "use the action directly",
            )
        self._require_armable()
        if not self._actor_is_authorised(actor):
            raise ProtocolRefusal(
                "PACE-2",
                f"the actor {actor!r} is not a named holder of the containment "
                "envelope and does not hold the card's command authority",
                "the rotation is a human act and requires a named holder",
            )
        rotation = self.card.rotations.setdefault(action_id, RotationState())
        rotation.issue()
        self._record(
            "rotation.issued",
            {"actor": actor, "action": action_id, "state": repr(rotation)},
        )
        return rotation

    def verify_rotation(self, action_id: str, actor: str) -> RotationState:
        """Verify the replacement credential."""
        rotation = self._rotation_for(action_id, actor)
        rotation.verify()
        self._record(
            "rotation.verified",
            {"actor": actor, "action": action_id, "state": repr(rotation)},
        )
        return rotation

    def move_workload(self, action_id: str, actor: str) -> RotationState:
        """Move the workload onto the verified replacement."""
        rotation = self._rotation_for(action_id, actor)
        rotation.move_workload()
        self._record(
            "rotation.moved",
            {"actor": actor, "action": action_id, "state": repr(rotation)},
        )
        return rotation

    def _rotation_for(self, action_id: str, actor: str) -> RotationState:
        if not self._actor_is_authorised(actor):
            raise ProtocolRefusal(
                "PACE-2",
                f"the actor {actor!r} is not a named holder of the containment "
                "envelope and does not hold the card's command authority",
                "the rotation is a human act and requires a named holder",
            )
        rotation = self.card.rotations.get(action_id)
        if rotation is None:
            raise ProtocolRefusal(
                "ESC-33",
                f"no rotation has been begun for {action_id}",
                "issue the replacement before verifying or moving it",
            )
        return rotation

    # -- verification ----------------------------------------------------

    def record_verification(
        self,
        results: Mapping[str, bool],
        source: str,
        actor: str,
    ) -> VerificationPass:
        """Record one pass of the kill verification set.

        The actor must hold the card's command authority. The verification
        passes are what unlock the irreversible recovery actions, and an
        unauthenticated actor who could record them would be able to unlock
        those actions and would leave the verification record contaminated in
        the one way that matters.
        """
        self._require_authority(actor)
        unknown = set(results) - set(VERIFICATION_CHECKS)
        if unknown:
            raise ProtocolRefusal(
                "ESC-21",
                "unknown verification checks: " + ", ".join(sorted(unknown)),
                "the verification set is V-1 to V-9",
            )
        verification = VerificationPass(
            at=self.now, results=dict(results), source=source, actor=actor
        )
        self.card.verifications.append(verification)
        return verification

    # -- re-entry --------------------------------------------------------

    def reentry_blockers(self) -> Tuple[str, ...]:
        """Return the unmet re-entry criteria, R-1 to R-10.

        A criterion that has never been marked is unmet. The criteria are
        not satisfied by the absence of a record, and the set is not
        satisfied until every one of them is.
        """
        return tuple(
            criterion
            for criterion in REENTRY_CRITERIA
            if not self.card.reentry.get(criterion, False)
        )

    def mark_reentry(self, criterion: str, satisfied: bool) -> None:
        """Record the state of one re-entry criterion.

        The criterion must be one the re-entry gate knows. An unknown key
        would otherwise be accepted, recorded on the card, and read by nobody:
        a reader of the card would see a satisfied criterion that satisfies
        nothing.
        """
        if criterion not in REENTRY_CRITERIA:
            raise ProtocolRefusal(
                "ESC-88",
                f"'{criterion}' is not a re-entry criterion",
                "the criteria are: " + ", ".join(sorted(REENTRY_CRITERIA)),
            )
        if criterion not in self.card.reentry:
            self.card.reentry[criterion] = False
        self.card.reentry[criterion] = satisfied
