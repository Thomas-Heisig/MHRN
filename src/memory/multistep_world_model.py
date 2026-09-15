"""Bounded action-conditioned multistep transition baseline.

The model learns exact discrete transition contexts ``state + action -> next_state``
and can roll them forward over an explicit action sequence. It is deliberately a
statistical reference model, not a neural world model and not accepted evidence
for planning or counterfactual reasoning.
"""

from __future__ import annotations

import copy
import json
from collections import Counter
from dataclasses import dataclass
from typing import Any, Sequence


class MultistepWorldModelError(ValueError):
    """Raised for malformed transition data or rollout requests."""


def _canonical(value: object) -> str:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise MultistepWorldModelError(
            "state and action values must be finite JSON"
        ) from error


def _state(value: object, name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise MultistepWorldModelError(f"{name} must be a string-keyed object")
    _canonical(value)
    return copy.deepcopy(value)


@dataclass(frozen=True, slots=True)
class StateAction:
    """Explicit action label and JSON payload for one transition step."""

    action: str
    payload: dict[str, Any]

    def __post_init__(self) -> None:
        if not self.action.strip():
            raise MultistepWorldModelError("action must be non-empty")
        _state(self.payload, "action payload")

    def to_dict(self) -> dict[str, Any]:
        return {"action": self.action, "payload": copy.deepcopy(self.payload)}


@dataclass(frozen=True, slots=True)
class RolloutStep:
    step: int
    action: StateAction
    predicted_state: dict[str, Any] | None
    support: int
    uncertainty: float


@dataclass(frozen=True, slots=True)
class RolloutResult:
    initial_state: dict[str, Any]
    steps: tuple[RolloutStep, ...]
    terminated_early: bool

    @property
    def final_state(self) -> dict[str, Any] | None:
        if not self.steps:
            return copy.deepcopy(self.initial_state)
        return copy.deepcopy(self.steps[-1].predicted_state)


class ActionConditionedWorldModel:
    """Bounded exact-context transition counts with deterministic rollouts."""

    model_version = 1

    def __init__(self, *, max_contexts: int = 512) -> None:
        if type(max_contexts) is not int or max_contexts <= 0:
            raise MultistepWorldModelError("max_contexts must be a positive integer")
        self.max_contexts = max_contexts
        self._contexts: dict[str, Counter[str]] = {}

    @staticmethod
    def _context(state: dict[str, Any], action: StateAction) -> str:
        return _canonical({"state": state, "action": action.to_dict()})

    def update(
        self,
        state: dict[str, Any],
        action: StateAction,
        next_state: dict[str, Any],
    ) -> None:
        current = _state(state, "state")
        following = _state(next_state, "next_state")
        key = self._context(current, action)
        label = _canonical(following)
        if key not in self._contexts and len(self._contexts) >= self.max_contexts:
            del self._contexts[next(iter(self._contexts))]
        self._contexts.setdefault(key, Counter[str]())[label] += 1

    def predict(
        self, state: dict[str, Any], action: StateAction
    ) -> tuple[dict[str, Any] | None, int, float]:
        current = _state(state, "state")
        counts = self._contexts.get(self._context(current, action))
        if not counts:
            return None, 0, 1.0
        label = min(counts, key=lambda item: (-counts[item], item))
        support = counts[label]
        total = sum(counts.values())
        return json.loads(label), support, 1.0 - support / total

    def rollout(
        self,
        initial_state: dict[str, Any],
        actions: Sequence[StateAction],
        *,
        max_steps: int = 32,
    ) -> RolloutResult:
        if type(max_steps) is not int or max_steps <= 0:
            raise MultistepWorldModelError("max_steps must be a positive integer")
        if len(actions) > max_steps:
            raise MultistepWorldModelError("action sequence exceeds rollout budget")
        initial = _state(initial_state, "initial_state")
        current = initial
        steps: list[RolloutStep] = []
        terminated = False
        for index, action in enumerate(actions, start=1):
            predicted, support, uncertainty = self.predict(current, action)
            steps.append(RolloutStep(index, action, predicted, support, uncertainty))
            if predicted is None:
                terminated = True
                break
            current = predicted
        return RolloutResult(initial, tuple(steps), terminated)

    def counterfactual(
        self,
        state: dict[str, Any],
        actions: Sequence[StateAction],
    ) -> dict[str, dict[str, Any] | None]:
        """Compare one-step alternatives without claiming causal intervention."""

        result: dict[str, dict[str, Any] | None] = {}
        for action in actions:
            key = _canonical(action.to_dict())
            predicted, _, _ = self.predict(state, action)
            result[key] = predicted
        return result

    def state_dict(self) -> dict[str, Any]:
        return {
            "model_version": self.model_version,
            "max_contexts": self.max_contexts,
            "context_order": list(self._contexts),
            "contexts": {
                key: dict(sorted(values.items()))
                for key, values in self._contexts.items()
            },
            "scientific_status": "statistical_multistep_reference_not_neural_evidence",
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> "ActionConditionedWorldModel":
        if state.get("model_version") != cls.model_version:
            raise MultistepWorldModelError("unsupported multistep world-model version")
        try:
            model = cls(max_contexts=state["max_contexts"])
            contexts = state["contexts"]
            order = state["context_order"]
            if not isinstance(contexts, dict) or not isinstance(order, list):
                raise MultistepWorldModelError("invalid contexts or context order")
            if len(order) != len(contexts) or set(order) != set(contexts):
                raise MultistepWorldModelError("context order does not match contexts")
            if len(order) > model.max_contexts:
                raise MultistepWorldModelError("stored contexts exceed capacity")
            for key in order:
                if not isinstance(key, str) or not isinstance(contexts[key], dict):
                    raise MultistepWorldModelError("invalid transition context")
                counts: Counter[str] = Counter()
                for label, count in contexts[key].items():
                    if (
                        not isinstance(label, str)
                        or type(count) is not int
                        or count <= 0
                    ):
                        raise MultistepWorldModelError("invalid transition count")
                    decoded = json.loads(label)
                    if _canonical(_state(decoded, "stored next_state")) != label:
                        raise MultistepWorldModelError(
                            "non-canonical stored next_state"
                        )
                    counts[label] = count
                if not counts:
                    raise MultistepWorldModelError(
                        "transition context may not be empty"
                    )
                model._contexts[key] = counts
            return model
        except (KeyError, TypeError, json.JSONDecodeError) as error:
            if isinstance(error, MultistepWorldModelError):
                raise
            raise MultistepWorldModelError(
                "malformed multistep world-model state"
            ) from error


__all__ = [
    "ActionConditionedWorldModel",
    "MultistepWorldModelError",
    "RolloutResult",
    "RolloutStep",
    "StateAction",
]
