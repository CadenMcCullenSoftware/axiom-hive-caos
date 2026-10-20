"""The countermeasure selection algorithm.

Six steps: generate candidates, filter on admissibility, rank, human selection,
authorise, and arm. The algorithm proposes; it does not decide. The operator
may select a lower-ranked countermeasure, and the card records that it was a
choice rather than a default.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Sequence, Tuple

from .countermeasures import CATALOGUE
from .models import (
    AdmissibilityFailure,
    Countermeasure,
    DecisionRecord,
    OperationCard,
)
from .roe import AdmissibilityResult, EvaluationContext, evaluate
from .scoring import (
    Option,
    compare_options,
    is_effectiveness_unconfirmed,
    residual_band,
    risk_adjusted_priority,
)
from .vocab import CollateralClass

if TYPE_CHECKING:  # pragma: no cover
    from .ledger import Ledger

__all__ = [
    "Candidate",
    "generate_candidates",
    "filter_admissible",
    "rank_candidates",
    "select",
    "counterfactuals",
    "DispatchResult",
    "dispatch",
]


@dataclass(frozen=True)
class Candidate:
    """A candidate countermeasure with its evaluation and ranking."""

    countermeasure: Countermeasure
    result: AdmissibilityResult
    priority: float

    @property
    def identifier(self) -> str:
        return self.countermeasure.identifier

    @property
    def admissible(self) -> bool:
        return self.result.admissible


def generate_candidates(
    card: OperationCard,
    *,
    extra: Sequence[str] = (),
    catalogue: Sequence[Countermeasure] = CATALOGUE,
) -> List[Countermeasure]:
    """Return every countermeasure bound to a technique the card declares.

    The operator may propose additional candidates explicitly; those are
    included whether or not the technique bindings match, because the
    operator's judgement is not subordinate to the catalogue's index.
    """
    index = {c.identifier: c for c in catalogue}
    bound = [
        c
        for c in catalogue
        if c.techniques & set(card.techniques)
        or c.techniques & {t.split(".")[0] for t in card.techniques}
    ]
    bound_ids = {c.identifier for c in bound}
    extras = [
        index[identifier]
        for identifier in extra
        if identifier in index and identifier not in bound_ids
    ]
    return list(bound) + list(extras)


def filter_admissible(
    card: OperationCard,
    candidates: Sequence[Countermeasure],
    context: Optional[EvaluationContext] = None,
) -> Tuple[List[Candidate], List[Candidate]]:
    """Split candidates into admissible and rejected sets.

    Every rejection is retained with its reason. A rejected countermeasure is
    a source of guidance, not a discarded entry.
    """
    context = context or EvaluationContext()
    admissible: List[Candidate] = []
    rejected: List[Candidate] = []
    effective = card.threat.effective_threat if card.threat else 0.0
    for cm in candidates:
        result = evaluate(card, cm, context)
        priority = risk_adjusted_priority(
            effective, cm.effectiveness_confidence, cm.collateral
        )
        candidate = Candidate(countermeasure=cm, result=result, priority=priority)
        if result.admissible:
            admissible.append(candidate)
        else:
            rejected.append(candidate)
    return admissible, rejected


def rank_candidates(candidates: Sequence[Candidate]) -> List[Candidate]:
    """Return candidates ordered by risk-adjusted priority, highest first."""
    return sorted(candidates, key=lambda c: (-c.priority, c.identifier))


def select(
    card: OperationCard,
    chosen: Candidate,
    *,
    alternatives: Sequence[str] = (),
    dissent: str = "",
    actor: str = "",
    context: Optional[EvaluationContext] = None,
) -> DecisionRecord:
    """Record the operator's selection as a reconstructible decision record.

    The record states what was known at the time, what was considered, what
    was chosen, the authority relied upon, and the pre-registered contingency.
    """
    context = context or EvaluationContext()
    effective = card.threat.effective_threat if card.threat else 0.0
    residual = effective * (1.0 - card.expected_effectiveness)
    known: List[str] = []
    if card.threat is not None:
        known.append(
            f"threat score {card.threat.score:.2f} (L={card.threat.likelihood} "
            f"I={card.threat.impact} A={card.threat.autonomy_factor} "
            f"V={card.threat.velocity})"
        )
        known.append(
            f"attribution confidence {card.threat.attribution_confidence:.2f} on the "
            f"basis of {card.threat.attribution_basis}"
        )
    known.append(f"card profile {card.profile.label} under {card.ea_reference}")
    known.append(
        f"card residual risk before {card.residual_risk_before:.2f}, after "
        f"{card.residual_risk_after:.2f}"
    )
    for claim in card.claims:
        known.append(f"[{claim.label.value}] {claim.text} (tier {claim.tier})")
    return DecisionRecord(
        record_id=f"DR-{card.card_id}-{card.revision}-{len(alternatives):03d}-{int(context.moment().timestamp())}",
        card_id=card.card_id,
        timestamp=context.moment(),
        decision_point="countermeasure selection",
        known_at_the_time=tuple(known),
        options_considered=tuple(alternatives),
        grounds_for_rejection=(
            "candidates rejected at the admissibility stage are recorded on the "
            "card with the specific condition and margin of failure"
        ),
        choice=(
            f"{chosen.identifier} — {chosen.countermeasure.name} "
            f"(priority {chosen.priority:.3f}, collateral "
            f"{chosen.countermeasure.collateral.name}, reversibility "
            f"{chosen.countermeasure.reversibility.name}, autonomy "
            f"{chosen.countermeasure.autonomy.name})"
        ),
        authority_relied_on=(
            f"engagement authorisation {card.ea_reference}; profile "
            f"{card.profile.label}; approvals {', '.join(sorted(card.approver_roles))}"
        ),
        confidence_at_the_time=(
            card.threat.attribution_confidence if card.threat else 0.0
        ),
        residual_risk=residual,
        risk_of_inaction=card.risk_of_inaction,
        pre_registered_contingency=card.contingency,
        contingency_recorded_at=(
            card.contingency_recorded_at.isoformat()
            if card.contingency_recorded_at
            else ""
        ),
        dissent=dissent,
        actor=actor or card.owner,
    )


def counterfactuals(
    card: OperationCard,
    candidates: Sequence[Candidate],
    *,
    include_inaction: bool = True,
) -> List[Option]:
    """Return the decision space as explicit computed alternatives.

    The operator should see the shape of the decision, not a single
    recommendation. The do-nothing option is included by default, because a
    card that only considers the risk of acting is incomplete.
    """
    effective = card.threat.effective_threat if card.threat else 0.0
    options: List[Option] = []
    for candidate in candidates:
        expected = candidate.countermeasure.residual_reduction
        confidence = candidate.countermeasure.effectiveness_confidence
        band = residual_band(effective, expected, confidence)
        options.append(
            Option(
                label=f"{candidate.identifier} — {candidate.countermeasure.name}",
                residual_risk=effective * (1.0 - expected),
                collateral=candidate.countermeasure.collateral,
                priority=candidate.priority,
                note=(
                    "admissible"
                    if candidate.admissible
                    else "not admissible: " + candidate.result.blocking_summary
                ),
                band=band,
                unconfirmed_effectiveness=is_effectiveness_unconfirmed(
                    expected, confidence
                ),
            )
        )
    if include_inaction:
        options.append(
            Option(
                label="do nothing",
                residual_risk=effective,
                collateral=CollateralClass.C0,
                priority=0.0,
                note=card.risk_of_inaction or "no risk of inaction recorded",
            )
        )
    return compare_options(options)


@dataclass(frozen=True)
class DispatchResult:
    """The outcome of a dispatch attempt."""

    dispatched: bool
    countermeasure_id: str
    reason: str
    units_spent: int
    remaining_budget: int
    failures: Tuple[AdmissibilityFailure, ...] = ()

    def as_payload(self) -> Dict[str, object]:
        return {
            "countermeasure": self.countermeasure_id,
            "dispatched": self.dispatched,
            "reason": self.reason,
            "units_spent": self.units_spent,
            "remaining_budget": self.remaining_budget,
            "failures": [f.as_dict() for f in self.failures],
        }


def dispatch(
    card: OperationCard,
    countermeasure: Countermeasure,
    ledger: "Ledger",
    *,
    context: Optional[EvaluationContext] = None,
    actor: str = "",
) -> DispatchResult:
    """Dispatch a countermeasure under a card, or refuse it.

    The admissibility algebra is re-evaluated at dispatch time, because both
    the card's state and the world may have changed since the selection. A
    countermeasure that was admissible at selection and is not admissible at
    dispatch is refused, and the refusal is recorded.

    A successful dispatch debits the card's autonomy budget by the
    countermeasure's autonomy cost. A refused dispatch spends nothing, because
    nothing was executed.
    """
    context = context or EvaluationContext()
    result = evaluate(card, countermeasure, context)
    if not result.admissible:
        ledger.append(
            "dispatch.refused",
            {
                "card_ref": card.card_id,
                "countermeasure": countermeasure.identifier,
                "outcome": "refuse",
                "failures": [f.as_dict() for f in result.failures],
            },
            subject=f"countermeasure:{countermeasure.identifier}",
            actor=actor or card.owner,
            card_ref=card.card_id,
        )
        return DispatchResult(
            dispatched=False,
            countermeasure_id=countermeasure.identifier,
            reason=result.blocking_summary,
            units_spent=0,
            remaining_budget=card.remaining_budget(),
            failures=tuple(result.failures),
        )

    units = countermeasure.autonomy_units
    # The record is written before the budget is debited. The Ledger's own
    # rule is that a failure to write is a failure to dispatch; debiting
    # first would spend the budget on an action that was never recorded, and
    # an unwritable ledger would surface as an unhandled error rather than as
    # a refusal.
    try:
        ledger.append(
            "dispatch.issued",
            {
                "card_ref": card.card_id,
                "countermeasure": countermeasure.identifier,
                "outcome": "permit",
                "autonomy_units": units,
                "remaining_budget": card.remaining_budget() - units,
                "collateral_class": countermeasure.collateral.name,
                "reversibility": countermeasure.reversibility.name,
            },
            subject=f"countermeasure:{countermeasure.identifier}",
            actor=actor or card.owner,
            card_ref=card.card_id,
        )
    except OSError as error:
        return DispatchResult(
            dispatched=False,
            countermeasure_id=countermeasure.identifier,
            reason=f"the ledger could not be written: {error}",
            units_spent=0,
            remaining_budget=card.remaining_budget(),
        )
    card.autonomy_consumed += units
    return DispatchResult(
        dispatched=True,
        countermeasure_id=countermeasure.identifier,
        reason="admissible at dispatch",
        units_spent=units,
        remaining_budget=card.remaining_budget(),
    )
