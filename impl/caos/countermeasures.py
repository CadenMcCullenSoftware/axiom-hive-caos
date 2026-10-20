"""The countermeasure catalogue: OCC-01 to OCC-43.

The catalogue describes; it does not enable. Nothing in this module confers
authority to act. Every entry declares its collateral class, reversibility,
autonomy class, minimum ROE profile, and attribution dependency, because those
fields are what the admissibility engine evaluates.

The entry data is not written here. It is generated from
``operational/countermeasure-catalogue.md``, which is authoritative, by
``tools/sync_catalogue.py``. This module converts that data into the
executable model and derives the operational attributes the engine reads.

The residual-risk reduction figures are the midpoints of the bands stated in
the document, at the design-intent evidence basis the document records. They
are estimates, not measurements, and no figure in the catalogue has been
calibrated against outcome data.
"""

from __future__ import annotations

from typing import List, Mapping, Optional, Tuple

from .catalogue_data import CATALOGUE_REDUCED, CATALOGUE_VERSION
from .models import Countermeasure
from .vocab import (
    AttributionDependency,
    AutonomyClass,
    CMClass,
    CollateralClass,
    CountermeasureStatus,
    DirectionOfEffect,
    Reversibility,
    ROEProfile,
)

__all__ = [
    "CATALOGUE",
    "CATALOGUE_INDEX",
    "CATALOGUE_VERSION",
    "get",
    "by_class",
    "for_techniques",
    "autonomy_units_for",
]


#: The nominal cost, in system-executed steps, that an autonomy class draws
#: against a card's autonomy budget. AC-0 and AC-1 draw nothing: a human
#: performs or approves every step, so there is no system-executed action to
#: budget.
_AUTONOMY_UNITS: Mapping[AutonomyClass, int] = {
    AutonomyClass.AC0_MANUAL: 0,
    AutonomyClass.AC1_ASSISTED: 0,
    AutonomyClass.AC2_SUPERVISED: 1,
    AutonomyClass.AC3_DELEGATED: 3,
    AutonomyClass.AC4_AUTONOMOUS: 2,
}


def autonomy_units_for(autonomy: AutonomyClass) -> int:
    """Return the nominal autonomy cost of an autonomy class."""
    return _AUTONOMY_UNITS[autonomy]


def _build(record: Mapping[str, object]) -> Countermeasure:
    direction = DirectionOfEffect[str(record["direction"])]
    return Countermeasure(
        identifier=str(record["identifier"]),
        name=str(record["name"]),
        cm_class=CMClass[str(record["cm_class"])],
        summary=str(record["summary"]),
        direction=direction,
        collateral=CollateralClass[str(record["collateral"])],
        reversibility=Reversibility[str(record["reversibility"])],
        autonomy=AutonomyClass[str(record["autonomy"])],
        min_profile=ROEProfile[str(record["min_profile"])],
        attribution_dependency=AttributionDependency[
            str(record["attribution_dependency"])
        ],
        techniques=frozenset(record["techniques"]),  # type: ignore[arg-type]
        preconditions=(str(record["preconditions"]),),
        procedure=str(record["procedure"]),
        failure_modes=(str(record["failure_modes"]),),
        side_effects=(str(record["side_effects"]),),
        detection_objective=str(record["detection_objective"]),
        intelligence_yield=str(record["intelligence_yield"]),
        operator_burden=str(record["operator_burden"]),
        degradation_behaviour=str(record["degradation"]),
        evidence_produced=str(record["evidence"]),
        residual_reduction=float(record["residual_reduction"]),  # type: ignore[arg-type]
        effectiveness_confidence=float(record["effectiveness_confidence"]),  # type: ignore[arg-type]
        status=CountermeasureStatus[str(record["status"])],
        autonomy_units=autonomy_units_for(AutonomyClass[str(record["autonomy"])]),
        touches_third_party=direction
        in (DirectionOfEffect.ADVERSARY_SYSTEM, DirectionOfEffect.ADVERSARY_INFRASTRUCTURE),
        affects_shared_environment=direction is DirectionOfEffect.ADVERSARY_BEHAVIOUR,
        read_only=AutonomyClass[str(record["autonomy"])] is AutonomyClass.AC4_AUTONOMOUS,
    )


CATALOGUE: Tuple[Countermeasure, ...] = tuple(
    _build(record) for record in CATALOGUE_REDUCED
)

CATALOGUE_INDEX: Mapping[str, Countermeasure] = {c.identifier: c for c in CATALOGUE}


def get(identifier: str) -> Optional[Countermeasure]:
    """Return a countermeasure by identifier, or ``None`` if it is not catalogued."""
    return CATALOGUE_INDEX.get(identifier)


def by_class(cm_class: CMClass) -> List[Countermeasure]:
    """Return every countermeasure in a class, in identifier order."""
    return [c for c in CATALOGUE if c.cm_class is cm_class]


def for_techniques(technique_ids: "frozenset[str] | set[str]") -> List[Countermeasure]:
    """Return every countermeasure bound to at least one of the given techniques.

    A technique identifier may be a full technique (``AAT-2.1``) or a
    category (``AAT-2``); both are accepted, and a full technique also matches
    the countermeasures bound to its category.
    """
    wanted = set(technique_ids)
    categories = {t.split(".")[0] for t in wanted}
    matched: List[Countermeasure] = []
    for cm in CATALOGUE:
        if cm.techniques & wanted:
            matched.append(cm)
            continue
        if cm.techniques & categories:
            matched.append(cm)
    return matched
