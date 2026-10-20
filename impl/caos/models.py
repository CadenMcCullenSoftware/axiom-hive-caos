"""Core data model for CAOS.

The dataclasses here mirror the artefacts defined in the documentation set: the
Operation Card, the Claim, the Signal, the Threat Assessment, the
Countermeasure, the Decision Record, and the Admissibility Failure.

Validation is deliberately explicit and shallow. The framework's position is
that the policy engine, not a data model, is the enforcement point; these
objects refuse to hold nonsense, and the policy engine refuses to let nonsense
through. Where a rule belongs to the operator's judgement rather than to the
data, it is not encoded here.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, FrozenSet, List, Mapping, Optional, Sequence, Tuple

from .vocab import (
    AttributionDependency,
    AutonomyClass,
    ClaimLabel,
    CMClass,
    CollateralClass,
    CountermeasureStatus,
    DirectionOfEffect,
    IntegrityState,
    Reversibility,
    ROEProfile,
    SourceTier,
    VerificationStatus,
)

#: The floor below which a countermeasure class may not be used. The
#: catalogue's class minimums, which the entries' own minimum profiles may
#: raise but not lower.
CLASS_PROFILE_FLOOR: Mapping[CMClass, ROEProfile] = {
    CMClass.CM_A: ROEProfile.R0_OBSERVE,
    CMClass.CM_B: ROEProfile.R0_OBSERVE,
    CMClass.CM_C: ROEProfile.R1_SHIELD,
    CMClass.CM_D: ROEProfile.R1_SHIELD,
    CMClass.CM_E: ROEProfile.R3_DECEIVE,
    CMClass.CM_F: ROEProfile.R1_SHIELD,
    CMClass.CM_G: ROEProfile.R1_SHIELD,
}

__all__ = [
    "Claim",
    "Signal",
    "ThreatAssessment",
    "Countermeasure",
    "AutonomyGrant",
    "OperationCard",
    "DecisionRecord",
    "AdmissibilityFailure",
    "utc_now",
    "canonical_json",
    "digest_of",
]


def utc_now() -> datetime:
    """Return the current time as an aware UTC datetime."""
    return datetime.now(timezone.utc)


#: The canonical JSON form is defined once, in `caos.canonical`, and every
#: digest in the system is computed over it. See that module for the rules.
from .canonical import canonical_json  # noqa: E402


@dataclass(frozen=True)
class Claim:
    """A labelled, tiered, confidence-bearing statement.

    A claim without a label and a tier is not displayed as a claim, per the
    evidence discipline in the conduct standard.
    """

    text: str
    label: ClaimLabel
    tier: SourceTier
    confidence: float
    provenance: str
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    derived_from: Tuple[str, ...] = ()
    derivation_penalty: float = 0.0

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("a claim requires text")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence out of range: {self.confidence}")
        if not 0.0 <= self.derivation_penalty <= 1.0:
            raise ValueError(
                f"derivation penalty out of range: {self.derivation_penalty}"
            )

    def propagated_confidence(self, input_confidences: Sequence[float]) -> float:
        """Return this claim's confidence after propagation from its inputs.

        The derived confidence is the weakest input's confidence, reduced by
        the declared derivation penalty. A claim with no inputs is returned
        unchanged.
        """
        if not input_confidences:
            return self.confidence
        return min(input_confidences) * (1.0 - self.derivation_penalty)


@dataclass(frozen=True)
class Signal:
    """An observation from a sensor.

    ``integrity`` is the state of the source, not of the observation. A
    degraded source may still have produced a true observation, so the two
    are recorded separately.
    """

    signal_id: str
    observed_at: datetime
    source: str
    fidelity: str
    integrity: str
    description: str
    indicators: Tuple[str, ...] = ()
    category: Optional[str] = None
    technique: Optional[str] = None
    personal_data_present: bool = False

    def __post_init__(self) -> None:
        if not self.signal_id:
            raise ValueError("a signal requires an identifier")
        if not self.description:
            raise ValueError("a signal requires a description")

    @property
    def integrity_state(self) -> IntegrityState:
        """The source's integrity state, resolved against the five-state vocabulary.

        A source whose state the vocabulary does not carry is treated as
        tampered-suspect, because a state the system cannot interpret is not a
        state it may treat as sound.
        """
        try:
            return IntegrityState(self.integrity.lower())
        except ValueError:
            return IntegrityState.TAMPERED_SUSPECT

    @property
    def usable(self) -> bool:
        """Whether this signal may support a classification.

        A missing or tampered-suspect source does not produce a negative
        finding; it produces no finding.
        """
        return self.integrity_state.usable


@dataclass(frozen=True)
class ThreatAssessment:
    """The scored assessment of an adversary operation.

    Every component carries its own reasoning, so that a reviewer can dispute
    one component rather than the whole assessment.
    """

    likelihood: float
    impact: int
    autonomy_factor: int
    velocity: int
    attribution_confidence: float
    attribution_basis: str
    likelihood_reason: str = ""
    impact_reason: str = ""
    autonomy_reason: str = ""
    velocity_reason: str = ""
    classification: Optional[str] = None
    techniques: Tuple[str, ...] = ()
    alternative_explanations: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.likelihood <= 1.0:
            raise ValueError(f"likelihood out of range: {self.likelihood}")
        if not 0 <= self.impact <= 5:
            raise ValueError(f"impact out of range: {self.impact}")
        if not 0 <= self.autonomy_factor <= 2:
            raise ValueError(f"autonomy factor out of range: {self.autonomy_factor}")
        if not 0 <= self.velocity <= 2:
            raise ValueError(f"velocity out of range: {self.velocity}")
        if not 0.0 <= self.attribution_confidence <= 1.0:
            raise ValueError(
                f"attribution confidence out of range: {self.attribution_confidence}"
            )
        if not self.attribution_basis:
            raise ValueError("an assessment requires an attribution basis")

    @property
    def score(self) -> float:
        """S = L x I x A x V."""
        return (
            self.likelihood
            * self.impact
            * self.autonomy_factor
            * self.velocity
        )

    @property
    def effective_threat(self) -> float:
        """S_eff = S x c."""
        return self.score * self.attribution_confidence


@dataclass(frozen=True)
class Countermeasure:
    """A catalogue entry.

    The catalogue describes; it does not enable. Nothing in this class confers
    authority to act.
    """

    identifier: str
    name: str
    cm_class: CMClass
    summary: str
    direction: DirectionOfEffect
    collateral: CollateralClass
    reversibility: Reversibility
    autonomy: AutonomyClass
    min_profile: ROEProfile
    attribution_dependency: AttributionDependency
    techniques: FrozenSet[str]
    preconditions: Tuple[str, ...] = ()
    procedure: str = ""
    failure_modes: Tuple[str, ...] = ()
    side_effects: Tuple[str, ...] = ()
    detection_objective: str = ""
    intelligence_yield: str = ""
    operator_burden: str = ""
    degradation_behaviour: str = ""
    evidence_produced: str = ""
    residual_reduction: float = 0.0
    effectiveness_confidence: float = 0.0
    status: CountermeasureStatus = CountermeasureStatus.ACTIVE
    autonomy_units: int = 1
    targets: Tuple[str, ...] = ()
    touches_third_party: bool = False
    affects_shared_environment: bool = False
    targets_humans: bool = False
    weaponises_model: bool = False
    non_weaponisation_declared: bool = True
    read_only: bool = False

    def __post_init__(self) -> None:
        if not self.identifier.startswith("OCC-"):
            raise ValueError(f"countermeasure identifier malformed: {self.identifier}")
        if not 0.0 <= self.residual_reduction <= 1.0:
            raise ValueError("residual reduction out of range")
        if not 0.0 <= self.effectiveness_confidence <= 1.0:
            raise ValueError("effectiveness confidence out of range")
        if self.targets_humans:
            raise ValueError(
                "a countermeasure whose object is a human being is outside the "
                "boundary of the framework and must not be catalogued"
            )
        if self.weaponises_model:
            raise ValueError(
                "a countermeasure that attacks a model is outside the boundary "
                "of the framework and must not be catalogued"
            )
        if self.autonomy is AutonomyClass.AC4_AUTONOMOUS and (
            self.collateral is not CollateralClass.C0 or not self.read_only
        ):
            raise ValueError(
                "autonomous execution is permitted only for read-only action at "
                "collateral class C0"
            )
        if not self.techniques:
            raise ValueError(
                "a countermeasure must bind at least one adversary technique; "
                "an unbound entry cannot be matched to anything and cannot be "
                "audited"
            )
        if self.min_profile.value < CLASS_PROFILE_FLOOR[self.cm_class].value:
            raise ValueError(
                f"the countermeasure's minimum profile {self.min_profile.label} is "
                f"below the floor for its class {self.cm_class.value}, which is "
                f"{CLASS_PROFILE_FLOOR[self.cm_class].label}"
            )
        # The third-party flag is denormalised from the direction of effect,
        # and a denormalised field that the model does not constrain is a
        # bypass: an outward action with the flag cleared would escape the
        # third-party exclusion entirely. The two must agree.
        outward = self.direction in (
            DirectionOfEffect.ADVERSARY_SYSTEM,
            DirectionOfEffect.ADVERSARY_INFRASTRUCTURE,
        )
        if self.touches_third_party != outward:
            raise ValueError(
                f"the third-party flag and the direction of effect disagree: "
                f"direction {self.direction.value} implies touches_third_party="
                f"{outward}, and the entry declares {self.touches_third_party}"
            )

@dataclass
class AutonomyGrant:
    """The autonomy envelope granted to a running countermeasure."""

    granted_at: datetime
    expires_at: datetime
    budget_units: int
    envelope: FrozenSet[str]
    on_call: str
    reversion_trigger: str

    def __post_init__(self) -> None:
        if self.expires_at <= self.granted_at:
            raise ValueError("an autonomy grant must expire after it is granted")
        if self.budget_units < 0:
            raise ValueError("autonomy budget cannot be negative")
        if not self.on_call:
            raise ValueError("an autonomy grant requires a named on-call operator")
        if not self.reversion_trigger:
            raise ValueError("an autonomy grant requires a reversion trigger")

    def expired(self, now: Optional[datetime] = None) -> bool:
        return (now or utc_now()) >= self.expires_at

    def remaining(self, consumed: int) -> int:
        return max(0, self.budget_units - consumed)


@dataclass
class OperationCard:
    """The atomic unit of authorised work.

    A card is a document, a data structure, and a legal instrument at once. It
    is the only thing that authorises a dispatch, and the control plane will
    not accept a dispatch without one.
    """

    card_id: str
    title: str
    owner: str
    created_at: datetime
    objective: str
    hypothesis: str
    disconfirming_observation: str
    ea_reference: str
    profile: ROEProfile
    collateral_ceiling: CollateralClass
    autonomy_ceiling: AutonomyClass
    approver_roles: FrozenSet[str]
    expires_at: datetime
    authorised_targets: Tuple[str, ...]
    excluded_targets: Tuple[str, ...]
    third_party_authorised: bool = False
    third_party_assessment: str = ""
    required_reversibility: Reversibility = Reversibility.REVERSED
    threat: Optional[ThreatAssessment] = None
    classification: Optional[str] = None
    techniques: Tuple[str, ...] = ()
    selected_counters: Tuple[str, ...] = ()
    rejected_counters: Tuple[str, ...] = ()
    min_countermeasure_confidence: float = 0.5
    autonomy_budget: int = 0
    autonomy_consumed: int = 0
    #: The declared envelope, expiry, and reversion trigger. The card's
    #: autonomy is granted under a named on-call operator and reverts on a
    #: stated condition; without those, the grant is not a grant.
    autonomy_envelope: Tuple[str, ...] = ()
    autonomy_expires_at: Optional[datetime] = None
    autonomy_on_call: str = ""
    autonomy_reversion_trigger: str = ""
    abort_conditions: Tuple[str, ...] = ()
    abort_owner: str = ""
    abort_mechanism: str = ""
    deconfliction_passed: bool = False
    deconfliction_attestation: str = ""
    deconfliction_map_current: bool = True
    risk_of_inaction: str = ""
    residual_risk_before: float = 0.0
    residual_risk_after: float = 0.0
    expected_effectiveness: float = 0.0
    #: The confidence in the expected effectiveness. The residual risk is
    #: reported as a band where this is low, because a residual risk stated
    #: without a confidence in the effectiveness behind it is not a number
    #: the operator may rely upon.
    effectiveness_confidence: float = 0.0
    per_target_authorisations: Tuple[str, ...] = ()
    irreversibility_argument: str = ""
    indirect_effect_attestation: str = ""
    non_weaponisation_attestation: str = ""
    claims: Tuple[Claim, ...] = ()
    rationale: str = ""
    alternatives_considered: Tuple[str, ...] = ()
    dissent: str = ""
    contingency: str = ""
    contingency_recorded_at: Optional[datetime] = None
    revision: int = 1

    # -- lifecycle -------------------------------------------------------

    def expired(self, now: Optional[datetime] = None) -> bool:
        return (now or utc_now()) >= self.expires_at

    def remaining_budget(self) -> int:
        return max(0, self.autonomy_budget - self.autonomy_consumed)

    def autonomy_grant(self) -> AutonomyGrant:
        """Return the card's autonomy grant, validated.

        The grant is what the card's autonomy budget, envelope, expiry, and
        reversion trigger amount to. Constructing it validates them: an
        expiry that has passed, a negative budget, an unnamed on-call
        operator, or an empty reversion trigger is refused here rather than
        being discovered during an operation.
        """
        return AutonomyGrant(
            granted_at=self.created_at,
            expires_at=self.autonomy_expires_at or self.expires_at,
            budget_units=self.autonomy_budget,
            envelope=frozenset(self.autonomy_envelope),
            on_call=self.autonomy_on_call,
            reversion_trigger=self.autonomy_reversion_trigger,
        )

    def required_approvals(self) -> FrozenSet[str]:
        """Roles that must authorise this card, per profile and collateral class."""
        from .vocab import required_approvals

        return required_approvals(self.profile, self.collateral_ceiling)

    def approval_gap(self) -> FrozenSet[str]:
        """Roles required for approval that the card does not carry."""
        return self.required_approvals() - set(self.approver_roles)

    # -- completion rules ------------------------------------------------

    #: Fields that must carry content before a card may be armed. This is
    #: the complete set: `completion_defects` checks these and nothing else,
    #: so a consumer that validates against this tuple accepts exactly the
    #: cards the engine accepts.
    MANDATORY_FIELDS: Tuple[str, ...] = (
        "objective",
        "hypothesis",
        "disconfirming_observation",
        "ea_reference",
        "authorised_targets",
        "excluded_targets",
        "risk_of_inaction",
        "alternatives_considered",
        "abort_conditions",
        "abort_owner",
        "abort_mechanism",
        "rationale",
        "contingency",
    )

    def completion_defects(self) -> List[str]:
        """Return the list of blocking defects on the card.

        A card with any defect cannot be armed. A field that does not apply
        must be marked ``n/a`` with a reason; it must not be left empty.
        """
        defects: List[str] = []
        for name in self.MANDATORY_FIELDS:
            value = getattr(self, name)
            if isinstance(value, str):
                if not value.strip():
                    defects.append(f"mandatory field '{name}' is empty")
            elif not value:
                defects.append(f"mandatory field '{name}' is empty")
        if self.threat is None:
            defects.append("mandatory field 'threat' is empty")
        if self.expected_effectiveness > 0.0 and self.effectiveness_confidence <= 0.0:
            defects.append(
                "the expected effectiveness is stated with no confidence in it; "
                "the residual risk it leaves cannot be relied upon as a point "
                "value"
            )
        if self.autonomy_budget and not self.autonomy_on_call.strip():
            defects.append(
                "the autonomy block is incomplete: an autonomy budget with no "
                "named on-call operator is not a grant"
            )
        if self.autonomy_budget and not self.autonomy_reversion_trigger.strip():
            defects.append(
                "the autonomy block is incomplete: an autonomy budget with no "
                "reversion trigger is not a grant"
            )
        unknown = self.unknown_techniques()
        if unknown:
            defects.append(
                "technique references not in the taxonomy registry: "
                + ", ".join(unknown)
            )
        if self.contingency.strip() and self.contingency_recorded_at is None:
            defects.append(
                "the pre-registered contingency carries no timestamp; a "
                "contingency written after the action would otherwise satisfy "
                "the field"
            )
        return defects

    def unknown_techniques(self) -> List[str]:
        """Return the card's technique references that the registry does not carry.

        A card that cites a technique identifier the registry does not hold
        cannot be checked against detection coverage, cannot be bound to a
        countermeasure, and cannot be audited. The reference is a defect, not
        a note.
        """
        from .taxonomy import TECHNIQUE_INDEX

        return [t for t in self.techniques if t not in TECHNIQUE_INDEX]

    def armed(self) -> bool:
        return not self.completion_defects()


@dataclass(frozen=True)
class AdmissibilityFailure:
    """A single failed admissibility condition, reported informatively."""

    condition: str
    title: str
    detail: str
    margin: str = ""
    remedy: str = ""

    def as_dict(self) -> Dict[str, str]:
        return {
            "condition": self.condition,
            "title": self.title,
            "detail": self.detail,
            "margin": self.margin,
            "remedy": self.remedy,
        }


@dataclass(frozen=True)
class DecisionRecord:
    """A reconstructible record of a decision.

    The sufficiency criterion is external: another reviewer must be able to
    reconstruct how the decision was reached from this record alone.
    """

    record_id: str
    card_id: str
    timestamp: datetime
    decision_point: str
    known_at_the_time: Tuple[str, ...]
    options_considered: Tuple[str, ...]
    grounds_for_rejection: Tuple[str, ...]
    choice: str
    authority_relied_on: str
    confidence_at_the_time: float
    residual_risk: float
    risk_of_inaction: str
    pre_registered_contingency: str
    contingency_recorded_at: str = ""
    dissent: str = ""
    outcome: str = ""
    actor: str = ""

    def as_payload(self) -> Dict[str, Any]:
        """Return the record as a JSON-safe payload for the Ledger."""
        return {
            "record_id": self.record_id,
            "card_id": self.card_id,
            "timestamp": self.timestamp.isoformat(),
            "decision_point": self.decision_point,
            "known_at_the_time": list(self.known_at_the_time),
            "options_considered": list(self.options_considered),
            "grounds_for_rejection": list(self.grounds_for_rejection),
            "choice": self.choice,
            "authority_relied_on": self.authority_relied_on,
            "confidence_at_the_time": self.confidence_at_the_time,
            "residual_risk": self.residual_risk,
            "risk_of_inaction": self.risk_of_inaction,
            "pre_registered_contingency": self.pre_registered_contingency,
            "contingency_recorded_at": self.contingency_recorded_at,
            "dissent": self.dissent,
            "outcome": self.outcome,
            "actor": self.actor,
        }
