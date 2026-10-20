"""Controlled vocabulary for CAOS.

This module is the single source of truth for the enumerated vocabularies
defined in the CAOS documentation set: claim labels, source reliability tiers,
verification statuses, collateral risk classes, autonomy classes, rules-of-
engagement profiles, countermeasure classes, reversibility categories, and
attribution dependencies.

Every other module in the package imports from here. Nothing else may define
an enumeration of its own; doing so would create a second, divergent
vocabulary, which is the defect this set's conventions exist to prevent.

The implementation is standard-library only and has no external dependencies.
"""

from __future__ import annotations

from enum import Enum, IntEnum
from typing import FrozenSet, Mapping

__all__ = [
    "ClaimLabel",
    "SourceTier",
    "VerificationStatus",
    "CollateralClass",
    "AutonomyClass",
    "ROEProfile",
    "CMClass",
    "Reversibility",
    "AttributionDependency",
    "DirectionOfEffect",
    "CountermeasureStatus",
    "IntegrityState",
    "APPROVAL_DEPTHS",
    "COLLATERAL_APPROVALS",
    "ATTRIBUTION_THRESHOLDS",
    "attribution_threshold",
    "CLASS_CONFIDENCE_FLOOR",
    "required_approvals",
]


class ClaimLabel(str, Enum):
    """The five claim labels, inherited from the Axiom Hive evidence model."""

    FACT = "Fact"
    ESTIMATE = "Estimate"
    INTERPRETATION = "Interpretation"
    HYPOTHESIS = "Hypothesis"
    RECOMMENDATION = "Recommendation"


class SourceTier(IntEnum):
    """Source reliability tiers. Rank 1 is the highest.

    The members are named ``ST`` rather than ``T`` because the set uses
    ``T0`` to ``T3`` for target classes in the constitutional instrument.
    One token, one meaning, across the code and the documents.
    """

    ST1 = 1
    ST2 = 2
    ST3 = 3
    ST4 = 4


class VerificationStatus(str, Enum):
    """Verification status of a claim or of a claim about system behaviour."""

    VERIFIED_PRIMARY = "Verified (primary)"
    VERIFIED_SECONDARY = "Verified (secondary)"
    CORRECTED = "Corrected"
    UNVERIFIED = "Unverified"
    REQUIRES_CONFIRMATION = "Requires confirmation"


class CollateralClass(IntEnum):
    """Collateral risk classes. The class is determined by effect, not intent."""

    C0 = 0
    C1 = 1
    C2 = 2
    C3 = 3

    @property
    def exposure(self) -> float:
        """Normalised collateral exposure used by the risk-adjusted priority.

        The normalisation is fixed by the decision-support model so that the
        ranking is reproducible. It is a judgement, not a measurement, and the
        fact is recorded as such in the document's limitations.
        """
        return _COLLATERAL_EXPOSURE[self]


_COLLATERAL_EXPOSURE: Mapping[CollateralClass, float] = {
    CollateralClass.C0: 0.00,
    CollateralClass.C1: 0.25,
    CollateralClass.C2: 0.60,
    CollateralClass.C3: 1.00,
}


class AutonomyClass(IntEnum):
    """How a countermeasure executes, independent of how clever it is."""

    AC0_MANUAL = 0
    AC1_ASSISTED = 1
    AC2_SUPERVISED = 2
    AC3_DELEGATED = 3
    AC4_AUTONOMOUS = 4


class IntegrityState(str, Enum):
    """The state of a data source, not of the observation it carried.

    The vocabulary is the one the platform architecture specification §6.1
    fixes, and it is the vocabulary every document describing a degraded
    source should use.
    """

    TRUSTWORTHY = "trustworthy"
    DEGRADED = "degraded"
    STALE = "stale"
    MISSING = "missing"
    TAMPERED_SUSPECT = "tampered-suspect"

    @property
    def usable(self) -> bool:
        """Whether a source in this state may support a conclusion.

        A missing or tampered-suspect source produces no finding, and never a
        negative one: the absence of a signal is not evidence of the absence
        of the thing the signal would have carried.
        """
        return self in {
            IntegrityState.TRUSTWORTHY,
            IntegrityState.DEGRADED,
            IntegrityState.STALE,
        }


class CMClass(str, Enum):
    """The seven countermeasure classes."""

    CM_A = "Detect"
    CM_B = "Harden"
    CM_C = "Contain"
    CM_D = "Observe"
    CM_E = "Deceive"
    CM_F = "Disrupt"
    CM_G = "Recover"


class ROEProfile(IntEnum):
    """Rules-of-engagement profiles. Each is a hard ceiling."""

    R0_OBSERVE = 0
    R1_SHIELD = 1
    R2_TRAP = 2
    R3_DECEIVE = 3
    R4_DISRUPT = 4
    R5_NEUTRALISE = 5

    @property
    def label(self) -> str:
        return _ROE_LABELS[self]

    @property
    def max_collateral(self) -> CollateralClass:
        return _ROE_MAX_COLLATERAL[self]

    @property
    def max_autonomy(self) -> AutonomyClass:
        return _ROE_MAX_AUTONOMY[self]

    @property
    def permitted_classes(self) -> FrozenSet["CMClass"]:
        return _ROE_PERMITTED_CLASSES[self]

    @property
    def permits_read_only_autonomy(self) -> bool:
        """Whether read-only autonomous execution is permitted at this profile.

        Autonomous execution is prohibited for any action with a collateral
        class above C0. The only exception is read-only reconnaissance inside
        a declared boundary, which the framework permits from profile R1
        upward.
        """
        return self is not ROEProfile.R0_OBSERVE


_ROE_LABELS: Mapping[ROEProfile, str] = {
    ROEProfile.R0_OBSERVE: "Observe",
    ROEProfile.R1_SHIELD: "Shield",
    ROEProfile.R2_TRAP: "Trap",
    ROEProfile.R3_DECEIVE: "Deceive",
    ROEProfile.R4_DISRUPT: "Disrupt",
    ROEProfile.R5_NEUTRALISE: "Neutralise",
}

_ROE_MAX_COLLATERAL: Mapping[ROEProfile, CollateralClass] = {
    ROEProfile.R0_OBSERVE: CollateralClass.C0,
    ROEProfile.R1_SHIELD: CollateralClass.C0,
    ROEProfile.R2_TRAP: CollateralClass.C1,
    ROEProfile.R3_DECEIVE: CollateralClass.C1,
    ROEProfile.R4_DISRUPT: CollateralClass.C2,
    ROEProfile.R5_NEUTRALISE: CollateralClass.C3,
}

_ROE_MAX_AUTONOMY: Mapping[ROEProfile, AutonomyClass] = {
    ROEProfile.R0_OBSERVE: AutonomyClass.AC1_ASSISTED,
    ROEProfile.R1_SHIELD: AutonomyClass.AC2_SUPERVISED,
    ROEProfile.R2_TRAP: AutonomyClass.AC3_DELEGATED,
    ROEProfile.R3_DECEIVE: AutonomyClass.AC3_DELEGATED,
    ROEProfile.R4_DISRUPT: AutonomyClass.AC3_DELEGATED,
    ROEProfile.R5_NEUTRALISE: AutonomyClass.AC3_DELEGATED,
}

#: Which countermeasure classes are available at each profile.
#:
#: The class sets are the class minimums stated in the countermeasure
#: catalogue §4.1: CM-A and CM-B from R0, CM-C, CM-D, and CM-G from R1, CM-E
#: from R3, and CM-F from R1 where the effect is exerted at the operator's
#: own perimeter and from R4 otherwise. The class set is a coarse
#: availability rule; the binding constraint on any individual entry is its
#: own declared minimum profile, which the admissibility engine checks
#: separately.
_ROE_PERMITTED_CLASSES: Mapping[ROEProfile, FrozenSet["CMClass"]] = {
    ROEProfile.R0_OBSERVE: frozenset({CMClass.CM_A, CMClass.CM_B}),
    ROEProfile.R1_SHIELD: frozenset(
        {
            CMClass.CM_A,
            CMClass.CM_B,
            CMClass.CM_C,
            CMClass.CM_D,
            CMClass.CM_F,
            CMClass.CM_G,
        }
    ),
    ROEProfile.R2_TRAP: frozenset(
        {
            CMClass.CM_A,
            CMClass.CM_B,
            CMClass.CM_C,
            CMClass.CM_D,
            CMClass.CM_G,
        }
    ),
    ROEProfile.R3_DECEIVE: frozenset(
        {
            CMClass.CM_A,
            CMClass.CM_B,
            CMClass.CM_C,
            CMClass.CM_D,
            CMClass.CM_E,
            CMClass.CM_G,
        }
    ),
    ROEProfile.R4_DISRUPT: frozenset(
        {
            CMClass.CM_A,
            CMClass.CM_B,
            CMClass.CM_C,
            CMClass.CM_D,
            CMClass.CM_E,
            CMClass.CM_F,
            CMClass.CM_G,
        }
    ),
    ROEProfile.R5_NEUTRALISE: frozenset(
        {
            CMClass.CM_A,
            CMClass.CM_B,
            CMClass.CM_C,
            CMClass.CM_D,
            CMClass.CM_E,
            CMClass.CM_F,
            CMClass.CM_G,
        }
    ),
}


class Reversibility(IntEnum):
    """Reversibility of a countermeasure. Higher is more reversible.

    REVERSIBLE  the effect can be undone by an equivalent action
    REVERSED    the effect was undone as part of the countermeasure
    LOW         the effect can be partly undone, with delay and effort
    NONE        the effect cannot be undone
    """

    REVERSIBLE = 3
    REVERSED = 2
    LOW = 1
    NONE = 0


class AttributionDependency(str, Enum):
    """What an action depends on being able to attribute.

    NONE        the action does not depend on attribution at all
    BEHAVIOURAL the action depends on the adversary's behaviour being recognised
    CLASS       the action depends on knowing the class of activity, not the actor
    IDENTITY    the action must be directed at a specific identified principal
    EXTERNAL    the action depends on an external authority's determination
    """

    NONE = "none"
    BEHAVIOURAL = "behavioural"
    CLASS = "class"
    IDENTITY = "identity"
    EXTERNAL = "external"


class DirectionOfEffect(str, Enum):
    """Where the countermeasure's effect lands."""

    OWN_ESTATE = "own estate"
    ADVERSARY_BEHAVIOUR = "adversary behaviour in own environment"
    ADVERSARY_SYSTEM = "adversary system"
    ADVERSARY_INFRASTRUCTURE = "adversary infrastructure"
    NONE = "none; the effect is on the operator's knowledge alone"


class CountermeasureStatus(str, Enum):
    """Lifecycle status of a catalogue entry."""

    ACTIVE = "active"
    CONDITIONAL = "conditional"
    RETIRED = "retired"
    WITHHELD = "withheld"


#: Approval depth required by each rules-of-engagement profile.
APPROVAL_DEPTHS: Mapping[ROEProfile, FrozenSet[str]] = {
    ROEProfile.R0_OBSERVE: frozenset({"operator"}),
    ROEProfile.R1_SHIELD: frozenset({"team_lead"}),
    ROEProfile.R2_TRAP: frozenset({"duty_manager", "legal_contact"}),
    ROEProfile.R3_DECEIVE: frozenset({"duty_manager", "asset_owner"}),
    ROEProfile.R4_DISRUPT: frozenset({"director", "legal_contact", "asset_owner"}),
    ROEProfile.R5_NEUTRALISE: frozenset(
        {"executive", "legal_contact", "external_authority"}
    ),
}

#: Approval depth required by each collateral risk class.
COLLATERAL_APPROVALS: Mapping[CollateralClass, FrozenSet[str]] = {
    CollateralClass.C0: frozenset({"team_lead"}),
    CollateralClass.C1: frozenset({"duty_manager", "legal_contact"}),
    CollateralClass.C2: frozenset({"director", "legal_contact", "asset_owner"}),
    CollateralClass.C3: frozenset({"executive", "legal_contact", "external_authority"}),
}

#: The minimum confidence in a classification required of a countermeasure
#: whose attribution dependency is behavioural or class rather than identity.
#:
#: The `INT-3` table scales with the collateral class and governs *identity*
#: attribution. A countermeasure that is evaluated on class confidence alone
#: is not governed by that table: it acts on the estate, not on a party. It
#: does need a floor, or a classification nobody believes in would authorise
#: it, so the floor is stated separately and does not scale.
CLASS_CONFIDENCE_FLOOR: float = 0.50

#: Minimum attribution confidence required to act, by collateral class.
ATTRIBUTION_THRESHOLDS: Mapping[CollateralClass, float] = {
    CollateralClass.C0: 0.50,
    CollateralClass.C1: 0.70,
    CollateralClass.C2: 0.85,
    CollateralClass.C3: 0.95,
}

def attribution_threshold(collateral: CollateralClass) -> float:
    """Return the minimum attribution confidence required to act.

    A countermeasure whose collateral class is ``collateral`` may be used only
    where the card's attribution confidence is at least this value.
    """
    return ATTRIBUTION_THRESHOLDS[collateral]


def required_approvals(
    profile: ROEProfile, collateral: CollateralClass
) -> FrozenSet[str]:
    """Return the roles that must authorise an action.

    The profile and the collateral class each impose a depth, and the roles
    are the **union** of the two. Taking the more demanding set alone drops a
    requirement: an R0 card at collateral class C2 would then arm on a team
    lead's approval with no operator's approval at all, and the profile's own
    depth would never be enforced.
    """
    return APPROVAL_DEPTHS[profile] | COLLATERAL_APPROVALS[collateral]
