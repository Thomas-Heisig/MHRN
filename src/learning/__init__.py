"""Learning and plasticity for MHRN.

This package provides:
- Pair-based STDP (isolated and production variants)
- Reward-modulated plasticity
- Independent prediction-error modulation
- Eligibility traces
- Learning engine for network integration
- Guarded learning-preparation contracts
"""

from .eligibility import EligibilityTrace, create_eligibility_trace
from .learning_engine import LearningEngine, LearningParameters, LearningStats
from .prediction_error import (
    PredictionErrorPlasticity,
    PredictionErrorPlasticityConfig,
    PredictionErrorPlasticityError,
    PredictionErrorPlasticityStats,
    PredictionErrorSignal,
)
from .preparation import (
    LearningDataPartition,
    LearningObjective,
    LearningPlanOrigin,
    LearningPreparationGuard,
    LearningPreparationProposal,
    LearningPreparationService,
    LearningSourceRef,
    PreparedLearningPlan,
)
from .reward import RewardSignal, create_reward
from .stdp_plugin import STDPParameters, STDPSynapse, create_stdp_synapse

__all__ = [
    # STDP
    "STDPParameters",
    "STDPSynapse",
    "create_stdp_synapse",
    # Reward
    "RewardSignal",
    "create_reward",
    # Prediction Error
    "PredictionErrorPlasticity",
    "PredictionErrorPlasticityConfig",
    "PredictionErrorPlasticityError",
    "PredictionErrorPlasticityStats",
    "PredictionErrorSignal",
    # Learning Engine
    "LearningEngine",
    "LearningParameters",
    "LearningStats",
    # Eligibility
    "EligibilityTrace",
    "create_eligibility_trace",
    # Learning Preparation
    "LearningDataPartition",
    "LearningObjective",
    "LearningPlanOrigin",
    "LearningPreparationGuard",
    "LearningPreparationProposal",
    "LearningPreparationService",
    "LearningSourceRef",
    "PreparedLearningPlan",
]
