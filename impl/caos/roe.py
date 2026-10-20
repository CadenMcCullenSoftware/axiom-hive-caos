"""The admissibility engine: the enforcement surface of the authorisation model.

This module implements the admissibility algebra, conditions AD-1 to AD-12.
AD-13 is the reporting rule that makes a refusal informative, and it is
implemented as a property of the result rather than as a further condition.

The engine is server-side and authoritative. It is not advisory. It fails
closed: a request it cannot evaluate is a request it refuses. A refusal is a
successful control and is never treated as a failure of the system.

Each condition is marked as machine-checkable, human-checkable, or hybrid, so
that a reviewer can see which part of the model is doing the work and which
part depends on a person.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Sequence, Tuple

from .models import AdmissibilityFailure, Countermeasure, OperationCard, utc_now
from .vocab import (
    CLASS_CONFIDENCE_FLOOR,
    AttributionDependency,
    AutonomyClass,
    CollateralClass,
    CountermeasureStatus,
    DirectionOfEffect,
    Reversibility,
    attribution_threshold,
)

__all__ = [
    "EvaluationContext",
    "CheckResult",
    "AdmissibilityResult",
    "evaluate",
    "evaluate_all",
    "card_is_armable",
    "CONDITION_TITLES",
    "CONDITION_NATURE",
]


@dataclass(frozen=True)
class EvaluationContext:
    """State the engine needs that is not carried on the card itself.

    Every field defaults to the value that refuses. The engine fails closed,
    and a field that silently defaults to the permissive value is a
    fail-open path: a countermeasure that depends on a class-level
    attribution would otherwise be admitted on the strength of a confidence
    nobody recorded. The defaults are therefore zero or false, and a caller
    that has an attribution assessment must say so.
    """

    deconfliction_passed: bool = False
    class_confidence: float = 0.0
    external_authority_confirmed: bool = False
    now: Optional[datetime] = None
    policy_version: str = "1.0"

    def moment(self) -> datetime:
        return self.now or utc_now()


@dataclass(frozen=True)
class CheckResult:
    """The outcome of one admissibility condition."""

    condition: str
    title: str
    nature: str
    passed: bool
    detail: str
    margin: str = ""
    remedy: str = ""


@dataclass(frozen=True)
class AdmissibilityResult:
    """The full outcome of evaluating one countermeasure against one card."""

    countermeasure_id: str
    countermeasure_name: str
    admissible: bool
    checks: Tuple[CheckResult, ...]
    evaluated_at: datetime
    policy_version: str

    @property
    def failures(self) -> List[AdmissibilityFailure]:
        """The failed conditions, reported informatively."""
        return [
            AdmissibilityFailure(
                condition=c.condition,
                title=c.title,
                detail=c.detail,
                margin=c.margin,
                remedy=c.remedy,
            )
            for c in self.checks
            if not c.passed
        ]

    @property
    def blocking_summary(self) -> str:
        """A one-line summary of why the countermeasure was refused."""
        if self.admissible:
            return "admissible"
        parts = [f"{f.condition} ({f.margin})" for f in self.failures if f.margin]
        if not parts:
            parts = [f.condition for f in self.failures]
        return f"{self.countermeasure_id}: " + "; ".join(parts)


#: Short title of each admissibility condition.
CONDITION_TITLES: Dict[str, str] = {
    "AD-1": "Profile class and floor",
    "AD-2": "Collateral class ceiling",
    "AD-3": "Reversibility floor",
    "AD-4": "Target containment",
    "AD-5": "Third-party exclusion",
    "AD-6": "Human beings not the object",
    "AD-7": "Autonomy class ceiling",
    "AD-8": "Countermeasure confidence floor",
    "AD-9": "Attribution dependency satisfied",
    "AD-10": "Deconfliction passed",
    "AD-11": "Autonomy budget available",
    "AD-12": "Non-weaponisation",
}

#: Whether each condition is determined by declared state, by a human
#: judgement, or by both. The classification is the framework's statement
#: about how much of the algebra is mechanical, and it is not a statement
#: that the whole algebra is automatic.
CONDITION_NATURE: Dict[str, str] = {
    "AD-1": "machine",
    "AD-2": "machine",
    "AD-3": "hybrid",
    "AD-4": "machine",
    "AD-5": "human",
    "AD-6": "hybrid",
    "AD-7": "machine",
    "AD-8": "machine",
    "AD-9": "machine",
    "AD-10": "hybrid",
    "AD-11": "machine",
    "AD-12": "hybrid",
}

#: AAT categories whose techniques operate on people. Where a card declares
#: one of these, the operator must record that the countermeasure's effect on
#: people is indirect, because the prohibition is on targeting people as the
#: object of a countermeasure, not on affecting them.
HUMAN_FACING_CATEGORIES = frozenset({"AAT-3"})

#: The scope prefix a countermeasure's target set must be covered by.
_SCOPE_PREFIX: Dict[DirectionOfEffect, str] = {
    DirectionOfEffect.OWN_ESTATE: "estate",
    DirectionOfEffect.ADVERSARY_BEHAVIOUR: "estate",
    DirectionOfEffect.ADVERSARY_SYSTEM: "adversary",
    DirectionOfEffect.ADVERSARY_INFRASTRUCTURE: "adversary",
    DirectionOfEffect.NONE: "estate",
}


def _targets_with_prefix(card: OperationCard, prefix: str) -> List[str]:
    return [t for t in card.authorised_targets if t.startswith(prefix + ":")]


def card_is_armable(card: OperationCard, now: Optional[datetime] = None) -> List[str]:
    """Return the reasons a card cannot be armed, if any.

    An expired card, a card with blocking completion defects, or a card whose
    required approvals are not all present cannot carry a dispatch.
    """
    reasons: List[str] = []
    if card.expired(now):
        reasons.append(
            f"card expired at {card.expires_at.isoformat()}; an expired card "
            "authorises nothing"
        )
    reasons.extend(card.completion_defects())
    gap = card.approval_gap()
    if gap:
        reasons.append(
            "required approvals not present on the card: " + ", ".join(sorted(gap))
        )
    return reasons


def _check_ad1(card: OperationCard, cm: Countermeasure) -> CheckResult:
    permitted = card.profile.permitted_classes
    class_ok = cm.cm_class in permitted
    floor_ok = card.profile.value >= cm.min_profile.value
    detail = (
        f"countermeasure class {cm.cm_class.value} is "
        f"{'permitted' if class_ok else 'not permitted'} at profile "
        f"{card.profile.label} (permitted: "
        f"{', '.join(sorted(c.value for c in permitted))}); "
        f"countermeasure minimum profile is {cm.min_profile.label}, card profile "
        f"is {card.profile.label}"
    )
    margin = ""
    remedy = ""
    if not floor_ok:
        margin = (
            f"countermeasure requires profile {cm.min_profile.label}; card is at "
            f"{card.profile.label}"
        )
        remedy = "escalate the profile, or select a countermeasure with a lower floor"
    elif not class_ok:
        margin = f"class {cm.cm_class.value} is outside the profile's permitted set"
        remedy = (
            f"escalate to a profile that permits {cm.cm_class.value}, or select a "
            "countermeasure in a permitted class"
        )
    return CheckResult(
        "AD-1",
        CONDITION_TITLES["AD-1"],
        CONDITION_NATURE["AD-1"],
        class_ok and floor_ok,
        detail,
        margin,
        remedy,
    )


def _check_ad2(card: OperationCard, cm: Countermeasure) -> CheckResult:
    over_card = cm.collateral.value - card.collateral_ceiling.value
    over_profile = cm.collateral.value - card.profile.max_collateral.value
    over = max(over_card, over_profile)
    ceiling = min(card.collateral_ceiling, card.profile.max_collateral)
    detail = (
        f"countermeasure collateral class {cm.collateral.name} against effective "
        f"ceiling {ceiling.name} (card ceiling {card.collateral_ceiling.name}, "
        f"profile ceiling {card.profile.max_collateral.name})"
    )
    margin = f"exceeds ceiling by {over} class{'es' if over != 1 else ''}" if over > 0 else ""
    remedy = (
        "raise the collateral ceiling by amending the engagement authorisation, "
        "or select a lower-class countermeasure"
        if over > 0
        else ""
    )
    return CheckResult(
        "AD-2",
        CONDITION_TITLES["AD-2"],
        CONDITION_NATURE["AD-2"],
        over <= 0,
        detail,
        margin,
        remedy,
    )


def _check_ad3(card: OperationCard, cm: Countermeasure) -> CheckResult:
    ok = cm.reversibility.value >= card.required_reversibility.value
    argument_required = cm.reversibility in (Reversibility.LOW, Reversibility.NONE)
    argument_present = bool(card.irreversibility_argument.strip())
    if argument_required and not argument_present:
        ok = False
    detail = (
        f"countermeasure reversibility {cm.reversibility.name} against required "
        f"floor {card.required_reversibility.name}"
    )
    if argument_required:
        detail += (
            "; the reversibility is Low or None, so the ROE-7 irreversibility "
            f"argument is required and is "
            f"{'recorded' if argument_present else 'not recorded'}"
        )
    margin = ""
    remedy = ""
    if not ok and argument_required and not argument_present:
        margin = (
            f"reversibility {cm.reversibility.name} requires an irreversibility "
            "argument on the card"
        )
        remedy = (
            "record on the card which elements are irreversible and why no "
            "reversible countermeasure achieves an acceptable reduction in "
            "residual risk, and have the approver confirm the argument"
        )
    elif not ok:
        margin = (
            f"reversibility {cm.reversibility.name} is below the required "
            f"{card.required_reversibility.name}"
        )
        remedy = (
            "record on the card why a reversible countermeasure is insufficient, "
            "and lower the reversibility floor by decision of the approver"
        )
    return CheckResult(
        "AD-3",
        CONDITION_TITLES["AD-3"],
        CONDITION_NATURE["AD-3"],
        ok,
        detail,
        margin,
        remedy,
    )


def _check_ad4(card: OperationCard, cm: Countermeasure) -> CheckResult:
    # Two limbs, because the catalogue entries declare a direction of effect
    # and most do not name specific targets. Where the entry names its
    # targets, the test is set containment: every named target must be on the
    # card. Where it does not, the test is that the card's authorised scope
    # covers the entry's direction of effect.
    if cm.targets:
        outside = [t for t in cm.targets if t not in set(card.authorised_targets)]
        ok = not outside
        detail = (
            f"countermeasure names {len(cm.targets)} specific target(s); "
            f"{len(cm.targets) - len(outside)} of them are on the card's "
            f"authorised target set"
        )
        margin = (
            "" if ok else "targets outside the card's authorised set: "
            + ", ".join(outside)
        )
        remedy = (
            ""
            if ok
            else "add the named targets to the card's authorised target set, or "
            "select a countermeasure whose targets are within it"
        )
        return CheckResult(
            "AD-4",
            CONDITION_TITLES["AD-4"],
            CONDITION_NATURE["AD-4"],
            ok,
            detail,
            margin,
            remedy,
        )

    prefix = _SCOPE_PREFIX[cm.direction]
    covering = _targets_with_prefix(card, prefix)
    ok = bool(covering)
    detail = (
        f"countermeasure direction of effect is {cm.direction.value}; required "
        f"target scope prefix '{prefix}:' is covered by "
        f"{len(covering)} authorised target(s)"
    )
    margin = "" if ok else f"no authorised target with prefix '{prefix}:'"
    remedy = (
        ""
        if ok
        else f"add a specific '{prefix}:' target to the card's authorised target set, "
        "or select a countermeasure with a different direction of effect"
    )
    return CheckResult(
        "AD-4",
        CONDITION_TITLES["AD-4"],
        CONDITION_NATURE["AD-4"],
        ok,
        detail,
        margin,
        remedy,
    )


def _check_ad5(card: OperationCard, cm: Countermeasure) -> CheckResult:
    if not cm.touches_third_party and not cm.affects_shared_environment:
        return CheckResult(
            "AD-5",
            CONDITION_TITLES["AD-5"],
            CONDITION_NATURE["AD-5"],
            True,
            "countermeasure has no third-party effect and does not act in a "
            "shared environment",
        )

    if cm.affects_shared_environment and not cm.touches_third_party:
        # The effect lands in the operator's own environment, which may be
        # shared with third parties. The shared-tenancy answer is required;
        # a per-target third-party authorisation is not, because no system the
        # operator does not control is modified.
        recorded = bool(card.third_party_assessment.strip())
        return CheckResult(
            "AD-5",
            CONDITION_TITLES["AD-5"],
            CONDITION_NATURE["AD-5"],
            recorded,
            "countermeasure acts on the adversary's behaviour in the operator's "
            f"own environment; shared-tenancy assessment "
            f"{'recorded' if recorded else 'not recorded'}",
            "" if recorded else "shared-tenancy assessment not recorded",
            "" if recorded else "record on the card who else depends on the "
            "environment the countermeasure acts in",
        )

    if cm.collateral is CollateralClass.C0:
        # A countermeasure at C0 has, by the definition of C0, no effect on
        # any party outside the operator's own estate. The third-party
        # exclusion does not bite, and requiring an authorisation that could
        # not lawfully be granted would be theatre.
        return CheckResult(
            "AD-5",
            CONDITION_TITLES["AD-5"],
            CONDITION_NATURE["AD-5"],
            True,
            "countermeasure acts outward but at collateral class C0, which by "
            "definition has no effect on any party outside the operator's "
            "own estate",
        )

    authorised = card.third_party_authorised
    assessment = bool(card.third_party_assessment.strip())
    named = _targets_with_prefix(card, "third-party") or _targets_with_prefix(
        card, "adversary"
    )
    per_target = [target for target in named if target in set(card.per_target_authorisations)]
    withheld = cm.status is CountermeasureStatus.WITHHELD
    ok = (
        authorised
        and assessment
        and bool(named)
        and bool(per_target)
        and not withheld
    )
    detail = (
        f"countermeasure affects a third party; card third-party authorisation "
        f"{'present' if authorised else 'absent'}; shared-tenancy assessment "
        f"{'recorded' if assessment else 'not recorded'}; named third-party or "
        f"adversary target {('present: ' + ', '.join(named)) if named else 'absent'}; "
        f"per-target written authorisation "
        f"{('present: ' + ', '.join(per_target)) if per_target else 'absent'}"
    )
    if withheld:
        detail += "; the countermeasure's status is Withheld pending a determination"
    margin = ""
    remedy = ""
    if not ok:
        missing = []
        if not authorised:
            missing.append("third-party authorisation")
        if not assessment:
            missing.append("shared-tenancy assessment")
        if not named:
            missing.append("named third-party or adversary target")
        if named and not per_target:
            missing.append("per-target written authorisation")
        if withheld:
            missing.append("withheld determination")
        margin = "missing " + ", ".join(missing)
        remedy = (
            "obtain specific per-target authorisation, record who else depends on "
            "the affected infrastructure, and name the target on the card"
        )
    return CheckResult(
        "AD-5",
        CONDITION_TITLES["AD-5"],
        CONDITION_NATURE["AD-5"],
        ok,
        detail,
        margin,
        remedy,
    )


def _check_ad6(card: OperationCard, cm: Countermeasure) -> CheckResult:
    if cm.targets_humans:
        return CheckResult(
            "AD-6",
            CONDITION_TITLES["AD-6"],
            CONDITION_NATURE["AD-6"],
            False,
            "the countermeasure's declared object class is human",
            "not satisfiable by adjustment; the countermeasure must be withdrawn",
            "no countermeasure may target human beings as its object (CON-4)",
        )
    human_facing = any(
        technique.split(".")[0] in HUMAN_FACING_CATEGORIES
        for technique in card.techniques
    )
    attested = bool(card.indirect_effect_attestation.strip())
    ok = (not human_facing) or attested
    detail = (
        "the countermeasure's declared object class is not human"
        + (
            f"; the card declares techniques that operate on people, so the "
            f"operator's indirect-effect attestation is "
            f"{'recorded' if attested else 'not recorded'}"
            if human_facing
            else ""
        )
    )
    return CheckResult(
        "AD-6",
        CONDITION_TITLES["AD-6"],
        CONDITION_NATURE["AD-6"],
        ok,
        detail,
        "" if ok else "indirect-effect attestation not recorded",
        "" if ok else "record that the countermeasure's effect on people is "
        "indirect, or withdraw the countermeasure",
    )


def _check_ad7(card: OperationCard, cm: Countermeasure) -> CheckResult:
    if cm.autonomy is AutonomyClass.AC4_AUTONOMOUS:
        ok = (
            cm.read_only
            and cm.collateral is CollateralClass.C0
            and card.profile.permits_read_only_autonomy
            and card.autonomy_ceiling.value >= AutonomyClass.AC4_AUTONOMOUS.value
        )
        detail = (
            "autonomous execution is permitted only for read-only action at "
            f"collateral class C0; countermeasure read_only={cm.read_only}, "
            f"collateral={cm.collateral.name}, profile={card.profile.label}, "
            f"card autonomy ceiling={card.autonomy_ceiling.name}"
        )
        margin = "" if ok else "read-only autonomous execution conditions not met"
        remedy = (
            ""
            if ok
            else "reduce the autonomy class, or obtain a card at a profile that "
            "permits read-only autonomous execution"
        )
        return CheckResult(
            "AD-7",
            CONDITION_TITLES["AD-7"],
            CONDITION_NATURE["AD-7"],
            ok,
            detail,
            margin,
            remedy,
        )
    ok = (
        cm.autonomy.value <= card.autonomy_ceiling.value
        and cm.autonomy.value <= card.profile.max_autonomy.value
    )
    detail = (
        f"countermeasure autonomy {cm.autonomy.name} against card ceiling "
        f"{card.autonomy_ceiling.name} and profile ceiling "
        f"{card.profile.max_autonomy.name}"
    )
    margin = ""
    remedy = ""
    if not ok:
        margin = (
            f"autonomy {cm.autonomy.name} exceeds "
            + (
                f"card ceiling {card.autonomy_ceiling.name}"
                if cm.autonomy.value > card.autonomy_ceiling.value
                else f"profile ceiling {card.profile.max_autonomy.name}"
            )
        )
        remedy = "reduce the autonomy class, or raise the card's autonomy ceiling"
    return CheckResult(
        "AD-7",
        CONDITION_TITLES["AD-7"],
        CONDITION_NATURE["AD-7"],
        ok,
        detail,
        margin,
        remedy,
    )


def _check_ad8(card: OperationCard, cm: Countermeasure) -> CheckResult:
    ok = cm.effectiveness_confidence >= card.min_countermeasure_confidence
    detail = (
        f"countermeasure effectiveness confidence {cm.effectiveness_confidence:.2f} "
        f"against card floor {card.min_countermeasure_confidence:.2f}"
    )
    margin = (
        ""
        if ok
        else f"short by {card.min_countermeasure_confidence - cm.effectiveness_confidence:.2f}"
    )
    remedy = (
        ""
        if ok
        else "do not act on a countermeasure whose expected effect you do not "
        "believe in; lower the card's floor by decision, or select another"
    )
    return CheckResult(
        "AD-8",
        CONDITION_TITLES["AD-8"],
        CONDITION_NATURE["AD-8"],
        ok,
        detail,
        margin,
        remedy,
    )


def _check_ad9(
    card: OperationCard, cm: Countermeasure, context: EvaluationContext
) -> CheckResult:
    dependency = cm.attribution_dependency
    threshold = attribution_threshold(cm.collateral)
    if dependency is AttributionDependency.NONE:
        return CheckResult(
            "AD-9",
            CONDITION_TITLES["AD-9"],
            CONDITION_NATURE["AD-9"],
            True,
            "countermeasure does not depend on attribution",
        )
    if dependency is AttributionDependency.EXTERNAL:
        ok = context.external_authority_confirmed
        return CheckResult(
            "AD-9",
            CONDITION_TITLES["AD-9"],
            CONDITION_NATURE["AD-9"],
            ok,
            "countermeasure depends on an external authority's determination; "
            f"external authority {'confirmed' if ok else 'not confirmed'}",
            "" if ok else "external determination not on file",
            "" if ok else "obtain the external determination and record it against the card",
        )
    if dependency is AttributionDependency.IDENTITY:
        confidence = (
            card.threat.attribution_confidence if card.threat is not None else 0.0
        )
        source = "card attribution confidence"
        ok = confidence >= threshold
    else:
        # A countermeasure evaluated on class confidence is not governed by
        # the `INT-3` table, which scales with the collateral class and
        # governs identity attribution. It has its own floor, which does not
        # scale, because it acts on the estate rather than on a party.
        confidence = context.class_confidence
        source = "class confidence"
        threshold = CLASS_CONFIDENCE_FLOOR
        ok = confidence >= threshold
    detail = (
        f"countermeasure depends on {dependency.value} attribution; {source} "
        f"{confidence:.2f} against threshold {threshold:.2f} for collateral class "
        f"{cm.collateral.name}"
    )
    margin = "" if ok else f"short by {threshold - confidence:.2f}"
    remedy = (
        ""
        if ok
        else "prefer a countermeasure that does not depend on the contested "
        "attribution, or improve the attribution before acting"
    )
    return CheckResult(
        "AD-9",
        CONDITION_TITLES["AD-9"],
        CONDITION_NATURE["AD-9"],
        ok,
        detail,
        margin,
        remedy,
    )


def _check_ad10(
    card: OperationCard, cm: Countermeasure, context: EvaluationContext
) -> CheckResult:
    passed = context.deconfliction_passed or card.deconfliction_passed
    map_current = card.deconfliction_map_current
    attested = bool(card.deconfliction_attestation.strip())
    ok = passed and (map_current or attested)
    detail = (
        f"deconfliction against live legitimate operations "
        f"{'passed' if passed else 'not confirmed'}; the deconfliction map is "
        f"{'current' if map_current else 'degraded'}; the operator's "
        f"attestation is {'recorded' if attested else 'not recorded'}"
    )
    margin = ""
    remedy = ""
    if not passed:
        margin = "deconfliction not confirmed"
        remedy = (
            "run the deconfliction check against live operations and record the "
            "result"
        )
    elif not ok:
        margin = "deconfliction map degraded and no attestation recorded"
        remedy = (
            "re-run the deconfliction check against a current map, or record the "
            "operator's attestation that the conflict has been assessed"
        )
    return CheckResult(
        "AD-10",
        CONDITION_TITLES["AD-10"],
        CONDITION_NATURE["AD-10"],
        ok,
        detail,
        margin,
        remedy,
    )


def _check_ad11(card: OperationCard, cm: Countermeasure) -> CheckResult:
    remaining = card.remaining_budget()
    if cm.autonomy < AutonomyClass.AC2_SUPERVISED:
        # The autonomy budget bounds actions the system executes. At AC-0 and
        # AC-1 a human performs or approves every step, so no budget is drawn.
        return CheckResult(
            "AD-11",
            CONDITION_TITLES["AD-11"],
            CONDITION_NATURE["AD-11"],
            True,
            f"countermeasure autonomy {cm.autonomy.name} draws no autonomy budget; "
            "the budget bounds actions the system executes",
        )
    ok = cm.autonomy_units <= remaining
    detail = (
        f"countermeasure consumes {cm.autonomy_units} autonomy unit(s); card "
        f"budget {card.autonomy_budget}, consumed {card.autonomy_consumed}, "
        f"remaining {remaining}"
    )
    margin = "" if ok else f"short by {cm.autonomy_units - remaining} unit(s)"
    remedy = "" if ok else "raise the card's autonomy budget, or select a lower-cost countermeasure"
    return CheckResult(
        "AD-11",
        CONDITION_TITLES["AD-11"],
        CONDITION_NATURE["AD-11"],
        ok,
        detail,
        margin,
        remedy,
    )


def _check_ad12(card: OperationCard, cm: Countermeasure) -> CheckResult:
    if cm.weaponises_model:
        return CheckResult(
            "AD-12",
            CONDITION_TITLES["AD-12"],
            CONDITION_NATURE["AD-12"],
            False,
            "the countermeasure's declared effect is to degrade the adversary's model",
            "not applicable; the condition is binary",
            "no countermeasure may weaponise a model (CON-6); the countermeasure "
            "must be withdrawn",
        )
    declared = cm.non_weaponisation_declared
    attested = bool(card.non_weaponisation_attestation.strip())
    ok = declared or attested
    detail = (
        "the catalogue's declaration of conformity with the non-weaponisation "
        f"boundary is {'present' if declared else 'absent'}; the operator's "
        f"attestation is {'recorded' if attested else 'not recorded'}"
    )
    return CheckResult(
        "AD-12",
        CONDITION_TITLES["AD-12"],
        CONDITION_NATURE["AD-12"],
        ok,
        detail,
        "" if ok else "no declaration of conformity and no operator attestation",
        "" if ok else "the operator must attest the boundary analysis, including "
        "that no uninvolved third party is harmed, or the countermeasure must be "
        "withdrawn",
    )


def evaluate(
    card: OperationCard,
    cm: Countermeasure,
    context: Optional[EvaluationContext] = None,
) -> AdmissibilityResult:
    """Evaluate one countermeasure against one card.

    All twelve conditions must hold. There is no aggregation, no averaging,
    and no judgement call inside the engine. A single failure makes the
    countermeasure inadmissible.
    """
    context = context or EvaluationContext()
    checks: List[CheckResult] = [
        _check_ad1(card, cm),
        _check_ad2(card, cm),
        _check_ad3(card, cm),
        _check_ad4(card, cm),
        _check_ad5(card, cm),
        _check_ad6(card, cm),
        _check_ad7(card, cm),
        _check_ad8(card, cm),
        _check_ad9(card, cm, context),
        _check_ad10(card, cm, context),
        _check_ad11(card, cm),
        _check_ad12(card, cm),
    ]

    # Preconditions. A card that cannot be armed carries no dispatch, and a
    # countermeasure that is withheld or retired is not available at any
    # profile, under any envelope, at any collateral class.
    blocking = card_is_armable(card, context.moment())
    if blocking:
        checks.append(
            CheckResult(
                "G-3",
                "Card is armable",
                "machine",
                False,
                "card cannot be armed: " + "; ".join(blocking),
                "card is not armable",
                "complete the card, obtain the required approvals, and confirm it "
                "has not expired",
            )
        )
    if cm.status is not CountermeasureStatus.ACTIVE and (
        cm.status is not CountermeasureStatus.CONDITIONAL
    ):
        checks.append(
            CheckResult(
                "PRE",
                "Countermeasure is available",
                "machine",
                False,
                f"the countermeasure's status is {cm.status.value}; a withheld or "
                "retired countermeasure is not available",
                f"status is {cm.status.value}",
                "select a countermeasure whose status is active or conditional; "
                "a withheld or retired entry is retained in the catalogue so "
                "that historical cards remain interpretable, and is not usable",
            )
        )

    return AdmissibilityResult(
        countermeasure_id=cm.identifier,
        countermeasure_name=cm.name,
        admissible=all(c.passed for c in checks),
        checks=tuple(checks),
        evaluated_at=context.moment(),
        policy_version=context.policy_version,
    )


def evaluate_all(
    card: OperationCard,
    countermeasures: Sequence[Countermeasure],
    context: Optional[EvaluationContext] = None,
) -> List[AdmissibilityResult]:
    """Evaluate a set of countermeasures against one card."""
    context = context or EvaluationContext()
    return [evaluate(card, cm, context) for cm in countermeasures]
