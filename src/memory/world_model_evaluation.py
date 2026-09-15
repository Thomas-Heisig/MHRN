"""Offline decision-benefit evaluation for Stage-6 world-model experiments.

The evaluator scores frozen multistep rollouts under matched candidate horizons.
It never dispatches actions and is not an actuation authority. Recommendations are
research outputs only and must not be interpreted as evidence of planning unless a
registered behavioural experiment supports that claim.
"""

from __future__ import annotations

import copy
import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from .multistep_world_model import (
    ActionConditionedWorldModel,
    RolloutResult,
    StateAction,
)


class WorldModelEvaluationError(ValueError):
    """Raised when an offline decision-benefit evaluation is invalid."""


@dataclass(frozen=True, slots=True)
class ActionSequenceCandidate:
    """Named, fixed-horizon action sequence evaluated without actuation."""

    label: str
    actions: tuple[StateAction, ...]

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise WorldModelEvaluationError("candidate label must be non-empty")
        if not self.actions:
            raise WorldModelEvaluationError("candidate actions must be non-empty")


@dataclass(frozen=True, slots=True)
class CandidateEvaluation:
    """Read-only evaluation result for one action-sequence candidate."""

    label: str
    rollout: RolloutResult
    eligible: bool
    score: float | None
    reason: str


@dataclass(frozen=True, slots=True)
class DecisionRecommendation:
    """Offline recommendation; never an actuator command or safety authorization."""

    selected_label: str | None
    evaluations: tuple[CandidateEvaluation, ...]
    scientific_status: str = "offline_reference_evaluator_not_actuation_authority"


TrajectoryScorer = Callable[[RolloutResult], float]


class OfflineDecisionEvaluator:
    """Compare matched candidate rollouts without mutating or actuating the model."""

    scientific_status = "offline_reference_evaluator_not_actuation_authority"

    def __init__(
        self,
        model: ActionConditionedWorldModel,
        scorer: TrajectoryScorer,
        *,
        max_steps: int = 32,
    ) -> None:
        if type(max_steps) is not int or max_steps <= 0:
            raise WorldModelEvaluationError("max_steps must be a positive integer")
        self.model = model
        self.scorer = scorer
        self.max_steps = max_steps

    def evaluate(
        self,
        initial_state: dict[str, Any],
        candidates: Sequence[ActionSequenceCandidate],
    ) -> DecisionRecommendation:
        """Score complete known rollouts under equal horizons and deterministic ties."""

        if not candidates:
            raise WorldModelEvaluationError("at least one candidate is required")
        labels = [candidate.label for candidate in candidates]
        if len(labels) != len(set(labels)):
            raise WorldModelEvaluationError("candidate labels must be unique")
        horizons = {len(candidate.actions) for candidate in candidates}
        if len(horizons) != 1:
            raise WorldModelEvaluationError("candidate horizons must be matched")
        horizon = next(iter(horizons))
        if horizon > self.max_steps:
            raise WorldModelEvaluationError(
                "candidate horizon exceeds evaluation budget"
            )

        before = copy.deepcopy(self.model.state_dict())
        evaluations: list[CandidateEvaluation] = []
        for candidate in candidates:
            rollout = self.model.rollout(
                initial_state,
                candidate.actions,
                max_steps=self.max_steps,
            )
            if rollout.terminated_early or rollout.final_state is None:
                evaluations.append(
                    CandidateEvaluation(
                        label=candidate.label,
                        rollout=rollout,
                        eligible=False,
                        score=None,
                        reason="unknown_transition",
                    )
                )
                continue
            score = self.scorer(rollout)
            if isinstance(score, bool) or not math.isfinite(score):
                raise WorldModelEvaluationError("trajectory score must be finite")
            evaluations.append(
                CandidateEvaluation(
                    label=candidate.label,
                    rollout=rollout,
                    eligible=True,
                    score=float(score),
                    reason="complete_rollout",
                )
            )

        if self.model.state_dict() != before:
            raise WorldModelEvaluationError(
                "offline evaluation mutated the world model"
            )

        eligible = [
            item for item in evaluations if item.eligible and item.score is not None
        ]
        eligible.sort(key=lambda item: (-item.score, item.label))
        selected = eligible[0].label if eligible else None
        return DecisionRecommendation(selected, tuple(evaluations))


__all__ = [
    "ActionSequenceCandidate",
    "CandidateEvaluation",
    "DecisionRecommendation",
    "OfflineDecisionEvaluator",
    "TrajectoryScorer",
    "WorldModelEvaluationError",
]
