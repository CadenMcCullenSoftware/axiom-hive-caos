"""The proving ground: an adversary simulator for exercise and validation.

The proving ground exists to test the decision and the interlock, not the
tools. It simulates an adversary AI operating against a synthetic estate, and
it produces signals that the operator's detection content is evaluated
against. It never touches a real system; this module has no network access,
no execution of adversary code, and no contact with any non-simulated target.

Scenarios are seeded and reproducible, so that an exercise can be re-run
exactly and a detection result can be compared between runs.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, FrozenSet, List, Mapping, Optional, Sequence, Set, Tuple

from .models import Signal, utc_now

__all__ = [
    "Archetype",
    "Scenario",
    "SimulatedAdversary",
    "run_scenario",
    "evaluate_detection",
    "ExerciseReport",
    "score_exercise",
]


class Archetype(str, Enum):
    """The adversary archetypes the proving ground can simulate."""

    SCRIPT_OPPORTUNIST = "script opportunist"
    AUTOMATION_SCALER = "automation scaler"
    ADAPTIVE_RECON = "adaptive reconnaissance agent"
    SOCIAL_SWARM = "social-engineering swarm"
    SUPPLY_CHAIN_PLANTER = "supply-chain planter"
    MODEL_POISONER = "model-poisoning operator"
    MULTI_AGENT_SWARM = "multi-agent swarm"
    PERSISTENT_IMPLANT = "persistent implant operator"


#: Techniques each archetype tends to use, with the likelihood of each.
#: The mapping is a model of behaviour, not a claim about any real actor.
ARCHETYPE_TECHNIQUES: Mapping[Archetype, Mapping[str, float]] = {
    Archetype.SCRIPT_OPPORTUNIST: {
        "AAT-4.2": 0.8,
        "AAT-4.1": 0.6,
        "AAT-6.1": 0.5,
        "AAT-6.3": 0.4,
    },
    Archetype.AUTOMATION_SCALER: {
        "AAT-6.1": 0.9,
        "AAT-6.4": 0.6,
        "AAT-6.6": 0.5,
        "AAT-4.2": 0.5,
    },
    Archetype.ADAPTIVE_RECON: {
        "AAT-4.1": 0.7,
        "AAT-4.3": 0.6,
        "AAT-4.4": 0.6,
        "AAT-1.3": 0.5,
        "AAT-5.3": 0.4,
    },
    Archetype.SOCIAL_SWARM: {
        "AAT-3.1": 0.9,
        "AAT-3.2": 0.7,
        "AAT-3.4": 0.6,
        "AAT-3.5": 0.5,
        "AAT-2.4": 0.4,
    },
    Archetype.SUPPLY_CHAIN_PLANTER: {
        "AAT-7.4": 0.8,
        "AAT-7.2": 0.6,
        "AAT-7.1": 0.5,
        "AAT-5.5": 0.5,
        "AAT-7.6": 0.4,
    },
    Archetype.MODEL_POISONER: {
        "AAT-7.1": 0.8,
        "AAT-7.2": 0.7,
        "AAT-7.3": 0.6,
        "AAT-7.5": 0.5,
        "AAT-6.2": 0.4,
    },
    Archetype.MULTI_AGENT_SWARM: {
        "AAT-8.1": 0.9,
        "AAT-8.2": 0.6,
        "AAT-8.5": 0.5,
        "AAT-1.3": 0.6,
        "AAT-1.1": 0.5,
    },
    Archetype.PERSISTENT_IMPLANT: {
        "AAT-5.5": 0.8,
        "AAT-5.6": 0.6,
        "AAT-5.1": 0.6,
        "AAT-5.2": 0.5,
        "AAT-9.1": 0.5,
    },
}


#: The detection objectives the simulated estate is instrumented for. A
#: technique absent from this set is a detection gap, and the exercise report
#: says so.
DEFAULT_DETECTED: FrozenSet[str] = frozenset(
    {
        "AAT-1.1",
        "AAT-1.2",
        "AAT-2.1",
        "AAT-2.3",
        "AAT-3.1",
        "AAT-4.1",
        "AAT-4.2",
        "AAT-4.3",
        "AAT-6.1",
        "AAT-6.3",
        "AAT-7.4",
        "AAT-8.1",
        "AAT-9.1",
    }
)


@dataclass(frozen=True)
class Scenario:
    """The parameters of one simulated exercise."""

    name: str
    archetype: Archetype
    steps: int = 12
    seed: int = 20261020
    start: Optional[datetime] = None
    detected: FrozenSet[str] = DEFAULT_DETECTED
    notes: str = ""

    def __post_init__(self) -> None:
        if self.steps < 1:
            raise ValueError("a scenario requires at least one step")


class SimulatedAdversary:
    """A simulated adversary AI.

    This class models an adversary's observable behaviour for the purpose of
    exercising detection content and operator judgement. It performs no
    exploitation, contacts no external system, and produces no working
    attack capability. Its output is a set of synthetic signals.
    """

    def __init__(self, scenario: Scenario) -> None:
        self.scenario = scenario
        self._random = random.Random(scenario.seed)
        self._pool: List[str] = []
        for technique, weight in ARCHETYPE_TECHNIQUES[scenario.archetype].items():
            self._pool.extend([technique] * max(1, int(weight * 10)))

    def next_technique(self) -> str:
        """Return the next technique this adversary would attempt."""
        if not self._pool:
            return "AAT-1.1"
        return self._random.choice(self._pool)

    def signal(self, index: int, technique_id: str, start: datetime) -> Signal:
        """Produce a synthetic signal for one simulated step."""
        from .taxonomy import technique as get_technique

        tech = get_technique(technique_id)
        description = (
            f"simulated {self.scenario.archetype.value} behaviour: "
            + (tech.description if tech else "unregistered technique")
        )
        source = self._random.choice(
            [
                "model-gateway.log",
                "tool-broker.trace",
                "agent-runtime.trace",
                "egress-proxy.log",
                "identity-provider.log",
            ]
        )
        fidelity = self._random.choice(["high", "medium", "high", "medium"])
        integrity = self._random.choice(
            ["trustworthy", "trustworthy", "trustworthy", "degraded"]
        )
        return Signal(
            signal_id=f"SIM-{self.scenario.seed}-{index:03d}",
            observed_at=start + timedelta(minutes=index * 7),
            source=source,
            fidelity=fidelity,
            integrity=integrity,
            description=description,
            indicators=(f"sim-indicator-{index}",),
            category=technique_id.split(".")[0],
            technique=technique_id,
            personal_data_present=self._random.random() < 0.2,
        )


def run_scenario(scenario: Scenario) -> List[Signal]:
    """Run a scenario and return the synthetic signals it produced."""
    start = scenario.start or utc_now()
    adversary = SimulatedAdversary(scenario)
    return [
        adversary.signal(index, adversary.next_technique(), start)
        for index in range(scenario.steps)
    ]


@dataclass
class ExerciseReport:
    """The outcome of one exercise run."""

    scenario: str
    archetype: str
    signals: int
    techniques_exercised: Set[str]
    techniques_detected: Set[str]
    techniques_missed: Set[str]
    coverage_percentage: float
    personalised_data_signals: int
    findings: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, object]:
        return {
            "scenario": self.scenario,
            "archetype": self.archetype,
            "signals": self.signals,
            "techniques_exercised": sorted(self.techniques_exercised),
            "techniques_detected": sorted(self.techniques_detected),
            "techniques_missed": sorted(self.techniques_missed),
            "coverage_percentage": self.coverage_percentage,
            "personalised_data_signals": self.personalised_data_signals,
            "findings": self.findings,
        }


def evaluate_detection(
    signals: Sequence[Signal],
    detected: FrozenSet[str],
    *,
    scenario: str = "",
    archetype: str = "",
) -> ExerciseReport:
    """Assess detection coverage against a set of signals.

    A technique that was exercised and not detected is a coverage gap. A
    technique that was never exercised is untested, which is a different and
    weaker statement.
    """
    exercised = {s.technique for s in signals if s.technique}
    detected_seen = exercised & set(detected)
    missed = exercised - set(detected)
    coverage = (len(detected_seen) / len(exercised) * 100.0) if exercised else 0.0
    findings: List[str] = []
    if missed:
        findings.append(
            "detection gaps against exercised techniques: "
            + ", ".join(sorted(missed))
        )
    if not exercised:
        findings.append("no techniques were exercised; the run produced no coverage evidence")
    degraded = [s.signal_id for s in signals if s.integrity == "degraded"]
    if degraded:
        findings.append(
            f"{len(degraded)} signal(s) arrived from a degraded source; these are "
            "not a negative finding"
        )
    personal = [s.signal_id for s in signals if s.personal_data_present]
    if personal:
        findings.append(
            f"{len(personal)} signal(s) contain personal data; the data-protection "
            "handling rules apply to the retained copies"
        )
    return ExerciseReport(
        scenario=scenario,
        archetype=archetype,
        signals=len(signals),
        techniques_exercised=exercised,
        techniques_detected=detected_seen,
        techniques_missed=missed,
        coverage_percentage=coverage,
        personalised_data_signals=len(personal),
        findings=findings,
    )


#: The exercise rubric. The dimensions are what the exercise is judged on.
RUBRIC: Tuple[Tuple[str, str, int], ...] = (
    (
        "decision quality",
        "the chosen action is defensible from the information available at the time",
        4,
    ),
    (
        "escalation discipline",
        "the operator escalated where the profile ceiling required it, and did not "
        "where it did not",
        3,
    ),
    (
        "attribution reasoning",
        "the operator distinguished class attribution from identity attribution, "
        "and said so",
        3,
    ),
    (
        "inquiry scope",
        "the operator did not probe beyond the authorised target set",
        3,
    ),
    (
        "use of deception",
        "the operator preferred shaping to disruption where shaping was adequate, "
        "and said why",
        2,
    ),
    (
        "inquiry of the third party",
        "the operator asked who else depended on the affected infrastructure",
        2,
    ),
    (
        "abort readiness",
        "the operator could state the abort conditions without reference to the card",
        2,
    ),
    (
        "recording",
        "the decision log would let a reviewer reconstruct the decision",
        1,
    ),
)


def score_exercise(
    observations: Mapping[str, int], *, maximum: Optional[int] = None
) -> Dict[str, object]:
    """Score an exercise against the rubric.

    ``observations`` maps a rubric dimension to the points awarded, from zero
    to the dimension's weight. The result is a percentage and a per-dimension
    breakdown, so that the exercise identifies which dimension to work on
    rather than only producing a number.
    """
    total = maximum if maximum is not None else sum(w for _, _, w in RUBRIC)
    if total <= 0:
        raise ValueError("the exercise maximum must be positive")
    awarded = 0
    breakdown: List[Dict[str, object]] = []
    for dimension, description, weight in RUBRIC:
        points = observations.get(dimension, 0)
        points = max(0, min(points, weight))
        awarded += points
        breakdown.append(
            {
                "dimension": dimension,
                "description": description,
                "maximum": weight,
                "awarded": points,
            }
        )
    if awarded > total:
        raise ValueError(
            f"the awarded score ({awarded}) exceeds the maximum ({total}); a "
            "percentage above 100 is not a score"
        )
    return {
        "awarded": awarded,
        "maximum": total,
        "percentage": (awarded / total * 100.0) if total else 0.0,
        "breakdown": breakdown,
        "note": (
            "the score measures the exercise, not the operator's competence; a low "
            "score is a finding about the framework's support, the scenario, or the "
            "individual, and the debrief decides which"
        ),
    }
