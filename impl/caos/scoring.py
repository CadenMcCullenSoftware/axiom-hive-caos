"""The scoring and confidence model.

Every number produced here is decomposed on screen. The model exists to make
a decision under uncertainty legible and contestable, not to make the
decision, and it never authorises anything.

A score orders the queue. A card, the evidence, and a named human authorise
the action.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

from .models import ThreatAssessment
from .vocab import CollateralClass

__all__ = [
    "DERIVATION_PENALTIES",
    "threat_score",
    "effective_threat",
    "residual_risk",
    "risk_adjusted_priority",
    "propagate_confidence",
    "derivation_penalty",
    "score_breakdown",
    "residual_risk_after",
    "band_for_likelihood",
    "band_for_impact",
    "compare_options",
]


#: Penalty applied to a derived claim, by the kind of derivation.
#: The penalty is a declared judgement, not a measurement. It is stated
#: explicitly so that a reviewer can dispute it.
DERIVATION_PENALTIES: Mapping[str, float] = {
    "direct observation": 0.00,
    "single-step inference": 0.05,
    "multi-step inference": 0.10,
    "inference across a telemetry gap": 0.15,
    "inference from an unclassified input": 0.20,
}


def derivation_penalty(kind: str) -> float:
    """Return the declared derivation penalty for a kind of derivation."""
    if kind not in DERIVATION_PENALTIES:
        raise KeyError(
            f"unknown derivation kind '{kind}'; declare the penalty explicitly "
            "rather than defaulting to a value that is not recorded"
        )
    return DERIVATION_PENALTIES[kind]


def threat_score(assessment: ThreatAssessment) -> float:
    """Return S = L x I x A x V, the threat score in the range 0 to 20."""
    return assessment.score


def effective_threat(score: float, attribution_confidence: float) -> float:
    """Return S_eff = S x c, the quantity the escalation ladder is applied to."""
    return score * attribution_confidence


def residual_risk(effective: float, expected_effectiveness: float) -> float:
    """Return R = S_eff x (1 - e), the risk carried forward after mitigation."""
    if not 0.0 <= expected_effectiveness <= 1.0:
        raise ValueError("expected effectiveness out of range")
    return effective * (1.0 - expected_effectiveness)


def residual_risk_after(
    assessment: ThreatAssessment, expected_effectiveness: float
) -> float:
    """Return the residual risk for a threat assessment and a mitigation level."""
    return residual_risk(assessment.effective_threat, expected_effectiveness)


def risk_adjusted_priority(
    effective: float, effectiveness_confidence: float, collateral: CollateralClass
) -> float:
    """Return P = (S_eff / 20) x q x (1 - r), a ranking value.

    P is a ranking only. It is never an authorisation, and a low value never
    prevents a different countermeasure from being chosen.
    """
    if not 0.0 <= effectiveness_confidence <= 1.0:
        raise ValueError("effectiveness confidence out of range")
    exposure = collateral.exposure
    return (effective / 20.0) * effectiveness_confidence * (1.0 - exposure)


def propagate_confidence(
    input_confidences: Sequence[float], penalty: float = 0.0
) -> float:
    """Return the confidence of a derived claim.

    A derived claim cannot be more confident than its least confident input,
    less the declared derivation penalty. The operation is subtractive, not
    multiplicative: ``c_derived = c_weakest - penalty``, floored at zero.

    The subtractive form is the one the decision-support model states, and it
    is the more conservative of the two. A leaf at 0.95 with a penalty of 0.10
    yields 0.85, which is the class minimum for a C2 countermeasure; the
    multiplicative form would yield 0.855, and the difference is large enough
    to change an admissibility outcome.
    """
    if not input_confidences:
        raise ValueError("a derived claim requires at least one input")
    if not 0.0 <= penalty <= 1.0:
        raise ValueError("derivation penalty out of range")
    for confidence in input_confidences:
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(f"input confidence out of range: {confidence}")
    return max(0.0, min(input_confidences) - penalty)


def score_breakdown(assessment: ThreatAssessment) -> List[Dict[str, object]]:
    """Return the score with each component exposed for contestation.

    A reviewer who disputes the score should be able to say which component
    they dispute. This function is what makes that possible.
    """
    return [
        {
            "component": "likelihood",
            "value": assessment.likelihood,
            "range": "0.0 - 1.0",
            "reason": assessment.likelihood_reason,
            "contestable": True,
        },
        {
            "component": "impact",
            "value": assessment.impact,
            "range": "0 - 5",
            "reason": assessment.impact_reason,
            "contestable": True,
        },
        {
            "component": "autonomy factor",
            "value": assessment.autonomy_factor,
            "range": "0 - 2",
            "reason": assessment.autonomy_reason,
            "contestable": True,
        },
        {
            "component": "velocity",
            "value": assessment.velocity,
            "range": "0 - 2",
            "reason": assessment.velocity_reason,
            "contestable": True,
        },
        {
            "component": "attribution confidence",
            "value": assessment.attribution_confidence,
            "range": "0.0 - 1.0",
            "reason": assessment.attribution_basis,
            "contestable": True,
        },
    ]


_LIKELIHOOD_BANDS: Tuple[Tuple[float, float, str], ...] = (
    (0.0, 0.09, "no evidence of an attack; ordinary or explained activity"),
    (0.10, 0.39, "possible; the pattern is consistent with benign activity"),
    (0.40, 0.69, "probable; attack behaviour is the more likely reading"),
    (0.70, 0.89, "highly likely; attack behaviour is the only reading that fits"),
    (0.90, 1.0, "observed; malicious intent is directly evidenced"),
)

_IMPACT_BANDS: Tuple[Tuple[int, int, str], ...] = (
    (0, 0, "no consequence to the estate"),
    (1, 1, "nuisance; an operator's time is consumed"),
    (2, 2, "exposure of data whose loss is material to a party"),
    (3, 3, "degradation of a service the estate depends on"),
    (4, 4, "material loss, or compromise of a system of record"),
    (5, 5, "loss of a critical function, or an effect on safety"),
)


def band_for_likelihood(value: float) -> str:
    """Return the evidential band description for a likelihood value."""
    for low, high, description in _LIKELIHOOD_BANDS:
        if low <= value <= high:
            return description
    return "outside the defined bands"


def band_for_impact(value: int) -> str:
    """Return the consequence description for an impact value."""
    for low, high, description in _IMPACT_BANDS:
        if low <= value <= high:
            return description
    return "outside the defined scale"


@dataclass(frozen=True)
class Option:
    """One option in a counterfactual comparison."""

    label: str
    residual_risk: float
    collateral: CollateralClass
    priority: float
    note: str = ""
    #: The residual risk's band, as (low, high). Equal to the point value
    #: where the confidence in the countermeasure's effectiveness is firm.
    band: Tuple[float, float] = (0.0, 0.0)
    #: Whether the countermeasure's effectiveness is an unconfirmed claim,
    #: and the residual risk it carries is therefore not a commitment.
    unconfirmed_effectiveness: bool = False

    @property
    def has_band(self) -> bool:
        return self.band[0] != self.band[1]


#: Below this confidence in a countermeasure's effectiveness, the residual
#: risk is reported as a band rather than a point value.
BAND_CONFIDENCE_THRESHOLD = 0.60


def residual_band(
    effective: float, effectiveness: float, effectiveness_confidence: float
) -> Tuple[float, float]:
    """Return the band the residual risk lies in.

    The residual risk is `R = S_eff x (1 - e)`. Where the confidence in `e`
    is below the band threshold, the figure is reported as a range rather
    than a point: the low end takes the whole of `e`'s uncertainty against
    the estimate, and the high end takes none of it.

    The band is a statement about the estimate's precision, not about the
    risk. It widens as confidence falls and collapses to a point when
    confidence is firm.
    """
    residual = residual_risk(effective, effectiveness)
    if effectiveness_confidence >= BAND_CONFIDENCE_THRESHOLD:
        return (residual, residual)
    uncertainty = 1.0 - effectiveness_confidence
    return (max(0.0, residual * (1.0 - uncertainty)), residual)


def is_effectiveness_unconfirmed(
    effectiveness: float, effectiveness_confidence: float
) -> bool:
    """Whether the countermeasure's effectiveness is an unconfirmed claim.

    A countermeasure whose effectiveness is asserted at `e >= 0.70` but
    whose confidence in that assertion is below 0.50 is not a commitment:
    the residual risk it leaves is not a number the operator may rely upon,
    and it must be marked as such wherever it is displayed.
    """
    return effectiveness >= 0.70 and effectiveness_confidence < 0.50


def compare_options(options: Sequence[Option]) -> List[Option]:
    """Return the options ordered by residual risk, lowest first.

    The comparison exists so that the operator sees the shape of the decision
    space rather than a single recommendation. Ordering by residual risk alone
    would ignore collateral, so the collateral class is carried on each option
    and the ranking is by residual risk with the priority value available for
    a second ordering.
    """
    return sorted(options, key=lambda o: (o.residual_risk, -o.priority))
