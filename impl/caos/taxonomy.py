"""The adversary-AI taxonomy (AAT) registry.

The taxonomy is behaviour-centred: it describes what an adversary does, because
behaviour is what sensors can observe and because capabilities are shared
across actors in a way that intent is not. A category that cannot be evidenced
from telemetry is not a category; it is a hypothesis.

`operational/adversary-ai-taxonomy-and-threat-model.md` §5 is canonical for
the identity and the behaviour of every technique, and the technique data here
is generated from it by `tools/sync_taxonomy.py`. The technique library at
`reference/ai-attack-technique-library.md` is canonical for the per-technique
indicators, detection methods, technique-level countermeasure bindings, and
external-mapping verification status.

No external framework's technique identifiers are asserted here. The internal
AAT identifiers are canonical for this system; the external identifiers are
aids to interoperability, are recorded in the library with a verification
status and a date, and are not reproduced in code where an unverified
identifier would become an unverified claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Mapping, Optional, Tuple

from .taxonomy_data import TECHNIQUES_DATA
from .vocab import CMClass

__all__ = [
    "Technique",
    "CATEGORIES",
    "TECHNIQUES",
    "TECHNIQUE_INDEX",
    "category_of",
    "techniques_for_category",
    "technique",
    "categories_for_countermeasure_class",
    "coverage_report",
    "identity_dependent_techniques",
]


@dataclass(frozen=True)
class Technique:
    """One adversary technique."""

    identifier: str
    name: str
    category: str
    description: str
    artefacts: str
    detection_objective: str
    countermeasure_bindings: FrozenSet[str]
    attribution_note: str
    mttd: str


#: The ten behaviour categories, as stated in the taxonomy document §4.
CATEGORIES: Mapping[str, Mapping[str, str]] = {
    "AAT-1": {
        "name": "Autonomy and Planning",
        "scope": (
            "Task decomposition, autonomous retry, recursive delegation, planning "
            "persistence, multi-step goal pursuit"
        ),
        "dominant_detection_signal": "Shape of the tool-call sequence: fan-out, join structure, retry curvature, nested run identifiers",
        "dominant_countermeasure_class": "Containment, with Disrupt where reach must be cut",
    },
    "AAT-2": {
        "name": "Manipulation and Deception",
        "scope": (
            "Direct and indirect prompt injection, tool-output poisoning, false "
            "authority and identity claims, instruction-hierarchy violation, "
            "context corruption"
        ),
        "dominant_detection_signal": "Instruction-like text crossing a trust boundary; imperative content in data fields; divergence between the model context and the authoritative transcript",
        "dominant_countermeasure_class": "Harden",
    },
    "AAT-3": {
        "name": "Social and Cognitive",
        "scope": (
            "Automated persuasion, persona consistency over time, adaptive "
            "rapport, pretextual social engineering, synthetic organisational voice"
        ),
        "dominant_detection_signal": "Stylistic and structural regularity across messages that have no human history; uniform variance profile",
        "dominant_countermeasure_class": "Harden, with Deceive where the channel can be shaped",
    },
    "AAT-4": {
        "name": "Exploitation and Discovery",
        "scope": (
            "Automated vulnerability discovery, campaign-scale fuzzing, "
            "credential harvesting, configuration and secret discovery, "
            "exploit chaining"
        ),
        "dominant_detection_signal": "Request sequences that walk an inventory or mutate parameters; reads outside the task scope; access to secret-bearing paths",
        "dominant_countermeasure_class": "Harden, with Detect as the entry control",
    },
    "AAT-5": {
        "name": "Evasion and Persistence",
        "scope": (
            "Log tampering, anti-forensic behaviour, sandbox and detector "
            "evasion, model-fingerprint suppression, long-horizon presence, "
            "account persistence"
        ),
        "dominant_detection_signal": "Gaps and anomalies in the audit chain; behavioural divergence between equivalent environments; parameter variance against stable content",
        "dominant_countermeasure_class": "Detect, with Contain",
    },
    "AAT-6": {
        "name": "Resource and Denial",
        "scope": (
            "Automation scaling, inference-cost exhaustion, credential stuffing, "
            "adaptive denial of service, resource pre-emption"
        ),
        "dominant_detection_signal": "Quota, rate, and cost telemetry diverging from the principal's declared envelope",
        "dominant_countermeasure_class": "Contain, with Disrupt where the entitlement must be withdrawn",
    },
    "AAT-7": {
        "name": "Supply Chain and Model",
        "scope": (
            "Model poisoning, backdoored adapters and fine-tunes, "
            "retrieval-corpus poisoning, tool and plugin supply chain, "
            "embedding manipulation"
        ),
        "dominant_detection_signal": "Artefact digests, index change logs, and dependency manifests",
        "dominant_countermeasure_class": "Harden, with Recover",
    },
    "AAT-8": {
        "name": "Multi-Agent Coordination",
        "scope": (
            "Agent swarms, delegation-chain abuse, coordinator compromise, "
            "inter-agent trust exploitation, conflicting-goal propagation"
        ),
        "dominant_detection_signal": "Orchestration graphs, delegation lineage, and trust-graph edges",
        "dominant_countermeasure_class": "Contain, with Harden",
    },
    "AAT-9": {
        "name": "Exfiltration and Covert Channels",
        "scope": (
            "Staged exfiltration, encoding and compression, DNS and timing "
            "channels, covert storage, egress abuse"
        ),
        "dominant_detection_signal": "Egress and proxy telemetry, and the aggregation of individually small transfers",
        "dominant_countermeasure_class": "Contain",
    },
    "AAT-10": {
        "name": "Decision Manipulation",
        "scope": (
            "Goal substitution, incremental scope creep, specification gaming, "
            "reward-hacking of the surrounding loop, operator decision influence"
        ),
        "dominant_detection_signal": "Divergence between the recorded objective and the executed plan",
        "dominant_countermeasure_class": "Deceive, with Contain",
    },
}

#: The techniques whose indicative bindings include a countermeasure acting on
#: the adversary's own systems, per the taxonomy document §5.12. These are the
#: techniques that cannot be answered without identifying the adversary.
_IDENTITY_DEPENDENT: FrozenSet[str] = frozenset(
    {
        "AAT-4.6", "AAT-4.8", "AAT-5.6", "AAT-6.1", "AAT-6.2",
        "AAT-6.3", "AAT-6.4", "AAT-6.5", "AAT-6.6", "AAT-9.7",
    }
)

#: The category-level expected time to detect, taken from the taxonomy
#: document's per-category detection notes. It is a category-level judgement
#: about detectability, not a per-technique measurement, and it is recorded
#: as such so that no reader mistakes it for a measured figure.
_MTTD_BY_CATEGORY: Mapping[str, str] = {
    "AAT-1": "medium",
    "AAT-2": "medium",
    "AAT-3": "high",
    "AAT-4": "low",
    "AAT-5": "high",
    "AAT-6": "low",
    "AAT-7": "high",
    "AAT-8": "medium",
    "AAT-9": "high",
    "AAT-10": "high",
}


def _build(record: Mapping[str, object]) -> Technique:
    identifier = str(record["identifier"])
    category = identifier.split(".")[0]
    identity_dependent = identifier in _IDENTITY_DEPENDENT
    return Technique(
        identifier=identifier,
        name=str(record["name"]),
        category=category,
        description=str(record["description"]),
        artefacts=str(record["artefacts"]),
        detection_objective=str(record.get("detection_objective") or record["artefacts"]),
        countermeasure_bindings=frozenset(record["countermeasure_bindings"]),  # type: ignore[arg-type]
        attribution_note=(
            "the technique's indicative bindings include a countermeasure acting "
            "on the adversary's own systems, so acting on it requires identity "
            "attribution and per-target authorisation"
            if identity_dependent
            else "answerable from the operator's own estate without identifying "
            "the adversary"
        ),
        mttd=_MTTD_BY_CATEGORY[category],
    )


TECHNIQUES: Tuple[Technique, ...] = tuple(_build(record) for record in TECHNIQUES_DATA)

TECHNIQUE_INDEX: Mapping[str, Technique] = {t.identifier: t for t in TECHNIQUES}


def category_of(technique_id: str) -> str:
    """Return the category identifier a technique belongs to."""
    return technique_id.split(".")[0]


def techniques_for_category(category: str) -> List[Technique]:
    """Return every technique in a category, in identifier order."""
    return [t for t in TECHNIQUES if t.category == category]


def technique(technique_id: str) -> Optional[Technique]:
    """Return a technique by identifier, or ``None`` if it is not registered."""
    return TECHNIQUE_INDEX.get(technique_id)


def identity_dependent_techniques() -> FrozenSet[str]:
    """Return the techniques that cannot be answered without identifying the adversary."""
    return _IDENTITY_DEPENDENT


def categories_for_countermeasure_class(cm_class: CMClass) -> FrozenSet[str]:
    """Return the AAT categories a countermeasure class addresses.

    The mapping is derived from the catalogue's own bindings rather than
    declared here, because a declared mapping and the catalogue's bindings
    drift apart, and when they do the join between "this technique" and
    "what addresses it" misleads.
    """
    from .countermeasures import CATALOGUE

    return frozenset(
        category
        for cm in CATALOGUE
        if cm.cm_class is cm_class
        for category in cm.techniques
    )


def coverage_report(
    detected: FrozenSet[str], *, include_untested: bool = True
) -> List[Dict[str, str]]:
    """Assess detection coverage of the taxonomy.

    ``detected`` is the set of technique identifiers for which a detection
    objective is satisfied and exercised. Techniques with no coverage are
    returned with status ``uncovered``; techniques whose detection objective
    exists but has not been exercised are returned with status ``untested``.

    Coverage is an input to residual risk, not a documentation entry.
    """
    report: List[Dict[str, str]] = []
    for tech in TECHNIQUES:
        if tech.identifier in detected:
            status = "covered"
        elif include_untested:
            status = "untested"
        else:
            status = "uncovered"
        report.append(
            {
                "technique": tech.identifier,
                "name": tech.name,
                "category": tech.category,
                "status": status,
                "mttd": tech.mttd,
                "detection_objective": tech.detection_objective,
            }
        )
    return report
