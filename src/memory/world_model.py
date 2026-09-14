"""Observation-only reference predictor with typed, deterministic persistence.

This is a bounded-context statistical baseline, not neural semantic memory or a
multistep world model. Support-based uncertainty is a heuristic, not calibration.
"""

from __future__ import annotations

import copy
import json
import math
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from src.embodiment.models import ActionCommand, EnvironmentObservation, SensorFrame

from .prediction_metrics import compare_prediction, is_number


@dataclass(frozen=True, slots=True)
class WorldPrediction:
    predicted_state: dict[str, Any] | None
    uncertainty: float
    source: str
    target_tick: int


@dataclass(slots=True)
class _TransitionStats:
    count: int = 0
    numeric_sum: dict[str, float] = field(default_factory=dict[str, float])
    numeric_count: dict[str, int] = field(default_factory=dict[str, int])
    categorical: dict[str, Counter[str]] = field(default_factory=dict[str, Counter[str]])


def _positive_int(value: Any, name: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _category(value: Any) -> str:
    if value is not None and not isinstance(value, (str, bool)):
        raise ValueError("categorical state must be a string, bool or null")
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"))


class TransitionWorldModel:
    """Bounded context FIFO; inference is read-only and restore preserves order."""

    model_version = 2

    def __init__(self, *, max_contexts: int = 128) -> None:
        self.max_contexts = _positive_int(max_contexts, "max_contexts")
        self._contexts: dict[str, _TransitionStats] = {}

    @staticmethod
    def _context(frame: SensorFrame, action: ActionCommand | None) -> str:
        value = {
            "sensor_id": frame.sensor_id,
            "modality": frame.modality,
            "payload": frame.payload,
            "actuator_id": None if action is None else action.actuator_id,
            "action": None if action is None else action.action,
            "action_payload": None if action is None else action.payload,
        }
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)

    def predict(
        self, frame: SensorFrame, action: ActionCommand | None, *, target_tick: int,
        persistence_state: dict[str, Any] | None,
    ) -> WorldPrediction:
        stats = self._contexts.get(self._context(frame, action))
        if stats is None:
            return WorldPrediction(copy.deepcopy(persistence_state), 1.0, "persistence_reference", target_tick)
        predicted: dict[str, Any] = {
            name: total / stats.numeric_count[name]
            for name, total in stats.numeric_sum.items()
        }
        for name, values in stats.categorical.items():
            label = min(values, key=lambda item: (-values[item], item))
            predicted[name] = json.loads(label)
        return WorldPrediction(predicted, 1.0 / (1.0 + stats.count), "adaptive_transition", target_tick)

    def update(
        self, frame: SensorFrame, action: ActionCommand | None,
        observation: EnvironmentObservation,
    ) -> None:
        key = self._context(frame, action)
        candidate = copy.deepcopy(self._contexts.get(key, _TransitionStats()))
        for name, value in observation.state.items():
            if not isinstance(name, str):
                raise ValueError("state field names must be strings")
            if is_number(value):
                if name in candidate.categorical:
                    raise ValueError("state field changed from categorical to numeric")
                total = candidate.numeric_sum.get(name, 0.0) + float(value)
                if not math.isfinite(total):
                    raise ValueError("numeric state and accumulated sum must be finite")
                candidate.numeric_sum[name] = total
                candidate.numeric_count[name] = candidate.numeric_count.get(name, 0) + 1
            elif value is None or isinstance(value, (str, bool)):
                if name in candidate.numeric_sum:
                    raise ValueError("state field changed from numeric to categorical")
                bucket = candidate.categorical.setdefault(name, Counter[str]())
                bucket[_category(value)] += 1
        candidate.count += 1
        if key not in self._contexts and len(self._contexts) >= self.max_contexts:
            del self._contexts[next(iter(self._contexts))]
        self._contexts[key] = candidate

    @staticmethod
    def error(predicted: dict[str, Any] | None, actual: dict[str, Any] | None) -> float | None:
        """Legacy mixed-unit compatibility value; use error_components in studies."""
        return compare_prediction(predicted, actual).legacy_mean_error

    @staticmethod
    def error_components(predicted: dict[str, Any] | None, actual: dict[str, Any] | None) -> dict[str, Any]:
        return compare_prediction(predicted, actual).to_dict()

    def state_dict(self) -> dict[str, Any]:
        return {
            "model_version": self.model_version,
            "max_contexts": self.max_contexts,
            "context_order": list(self._contexts),
            "uncertainty_kind": "support_heuristic_not_calibrated",
            "contexts": {
                key: {
                    "count": stats.count,
                    "numeric_sum": dict(stats.numeric_sum),
                    "numeric_count": dict(stats.numeric_count),
                    "categorical": {name: dict(values) for name, values in stats.categorical.items()},
                }
                for key, stats in self._contexts.items()
            },
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> "TransitionWorldModel":
        if state.get("model_version") != cls.model_version:
            raise ValueError("unsupported world model version; legacy v1 needs a replay-based rebuild because category types and FIFO order were not preserved")
        try:
            model = cls(max_contexts=state["max_contexts"])
            contexts = state["contexts"]
            order = state["context_order"]
            if not isinstance(contexts, dict) or not isinstance(order, list):
                raise ValueError("world model contexts and order have invalid types")
            if not all(isinstance(key, str) for key in order):
                raise ValueError("context order must contain string keys")
            if len(order) != len(contexts) or set(order) != set(contexts) or len(order) > model.max_contexts:
                raise ValueError("context order or capacity is invalid")
            for key in order:
                item = contexts[key]
                stats = _TransitionStats(count=_positive_int(item["count"], "count"))
                sums, counts, categories = item["numeric_sum"], item["numeric_count"], item["categorical"]
                if not all(isinstance(value, dict) for value in (sums, counts, categories)):
                    raise ValueError("invalid transition statistics")
                if set(sums) != set(counts) or set(sums) & set(categories):
                    raise ValueError("inconsistent transition fields")
                for name, value in sums.items():
                    if not isinstance(name, str) or not is_number(value) or not math.isfinite(value):
                        raise ValueError("invalid numeric sum")
                    count = _positive_int(counts[name], "field count")
                    if count > stats.count:
                        raise ValueError("field count exceeds observation count")
                    stats.numeric_sum[name] = float(value)
                    stats.numeric_count[name] = count
                for name, values in categories.items():
                    if not isinstance(name, str) or not isinstance(values, dict) or not values:
                        raise ValueError("invalid categorical statistics")
                    bucket: Counter[str] = Counter()
                    for label, value in values.items():
                        if not isinstance(label, str) or _category(json.loads(label)) != label:
                            raise ValueError("invalid typed category")
                        bucket[label] = _positive_int(value, "category count")
                    if sum(bucket.values()) > stats.count:
                        raise ValueError("category count exceeds observation count")
                    stats.categorical[name] = bucket
                model._contexts[key] = stats
            return model
        except (KeyError, TypeError, AttributeError) as error:
            raise ValueError("malformed world model state") from error
