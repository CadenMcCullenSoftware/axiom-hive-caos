"""Package entry point for the CAOS reference implementation.

The package surface covers the decision-support core, the countermeasure
catalogue, the adversary taxonomy, the admissibility engine, the Ledger, the
Watchfloor, the proving ground, and the emergency shutdown and containment
path.

The implementation is standard-library only. It is the executable statement of
the decision-support model, the admissibility algebra, the ledger, the
Watchfloor, and the proving ground.
"""

from __future__ import annotations

from .countermeasures import CATALOGUE, get as get_countermeasure
from .decision import (
    Candidate,
    counterfactuals,
    filter_admissible,
    generate_candidates,
    rank_candidates,
    select,
)
from .emergency import (
    ACTIONS,
    PROHIBITED_OPERATIONS,
    EmergencyAction,
    EmergencyCard,
    EmergencyController,
    EmergencyLevel,
    EmergencyState,
    ProtocolRefusal,
)
from .ledger import GENESIS_DIGEST, Ledger, LedgerRecord
from .models import (
    AdmissibilityFailure,
    AutonomyGrant,
    Claim,
    Countermeasure,
    DecisionRecord,
    OperationCard,
    Signal,
    ThreatAssessment,
)
from .proving_ground import (
    Archetype,
    ExerciseReport,
    Scenario,
    evaluate_detection,
    run_scenario,
    score_exercise,
)
from .roe import (
    AdmissibilityResult,
    CheckResult,
    EvaluationContext,
    card_is_armable,
    evaluate,
    evaluate_all,
)
from .scoring import (
    effective_threat,
    propagate_confidence,
    residual_risk,
    risk_adjusted_priority,
    score_breakdown,
    threat_score,
)
from .taxonomy import CATEGORIES, TECHNIQUES, technique
from .vocab import (
    AttributionDependency,
    AutonomyClass,
    ClaimLabel,
    CMClass,
    CollateralClass,
    CountermeasureStatus,
    DirectionOfEffect,
    Reversibility,
    ROEProfile,
    SourceTier,
    VerificationStatus,
    attribution_threshold,
    required_approvals,
)
from .watchfloor import Posture, Watchfloor

from .version import PLATFORM_BUILD, __version__

__all__ = [
    "AdmissibilityFailure",
    "AdmissibilityResult",
    "Archetype",
    "AttributionDependency",
    "AutonomyClass",
    "AutonomyGrant",
    "CATEGORIES",
    "CATALOGUE",
    "CMClass",
    "Candidate",
    "CheckResult",
    "Claim",
    "ClaimLabel",
    "CollateralClass",
    "Countermeasure",
    "CountermeasureStatus",
    "DecisionRecord",
    "DirectionOfEffect",
    "EvaluationContext",
    "ExerciseReport",
    "GENESIS_DIGEST",
    "EmergencyState",
    "Ledger",
    "LedgerRecord",
    "OperationCard",
    "Posture",
    "ProtocolRefusal",
    "Reversibility",
    "ROEProfile",
    "Scenario",
    "Signal",
    "SourceTier",
    "TECHNIQUES",
    "ThreatAssessment",
    "VerificationStatus",
    "Watchfloor",
    "ACTIONS",
    "PROHIBITED_OPERATIONS",
    "EmergencyAction",
    "EmergencyCard",
    "EmergencyController",
    "attribution_threshold",
    "card_is_armable",
    "counterfactuals",
    "effective_threat",
    "evaluate",
    "evaluate_all",
    "evaluate_detection",
    "filter_admissible",
    "generate_candidates",
    "get_countermeasure",
    "propagate_confidence",
    "required_approvals",
    "residual_risk",
    "risk_adjusted_priority",
    "run_scenario",
    "score_breakdown",
    "score_exercise",
    "select",
    "threat_score",
    "technique",
    "__version__",
]
