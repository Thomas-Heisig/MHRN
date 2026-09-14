"""Typed observation errors; raw units are never silently called accuracy."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, TypeGuard


def is_number(value: object) -> TypeGuard[int | float]:
    """Booleans are categorical even though Python makes bool an int subtype."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


@dataclass(frozen=True, slots=True)
class PredictionErrors:
    """Per-field errors and coverage, separate from reward and spike mismatch."""

    numeric_absolute: dict[str, float]
    categorical_mismatch: dict[str, float]
    missing_fields: tuple[str, ...]
    unsupported_fields: tuple[str, ...]
    target_fields: int

    @property
    def coverage(self) -> float | None:
        compared = len(self.numeric_absolute) + len(self.categorical_mismatch)
        return compared / self.target_fields if self.target_fields else None

    @property
    def legacy_mean_error(self) -> float | None:
        """Compatibility telemetry only: mixed units, not a scientific score."""
        values = [*self.numeric_absolute.values(), *self.categorical_mismatch.values()]
        return sum(values) / len(values) if values else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "numeric_absolute": dict(self.numeric_absolute),
            "categorical_mismatch": dict(self.categorical_mismatch),
            "missing_fields": list(self.missing_fields),
            "unsupported_fields": list(self.unsupported_fields),
            "target_fields": self.target_fields,
            "coverage": self.coverage,
            "legacy_mean_error": self.legacy_mean_error,
            "metric_kind": "environment_prediction_error",
            "aggregate_kind": "legacy_mixed_units_not_accuracy",
        }


def compare_prediction(
    predicted: Mapping[str, Any] | None, actual: Mapping[str, Any] | None
) -> PredictionErrors:
    """Compare actual targets without treating missing or invalid values as zero."""
    numeric: dict[str, float] = {}
    categorical: dict[str, float] = {}
    missing: list[str] = []
    unsupported: list[str] = []
    if actual is None:
        return PredictionErrors(numeric, categorical, (), (), 0)
    for key, observed in actual.items():
        if not (observed is None or isinstance(observed, (str, bool)) or is_number(observed)):
            unsupported.append(key)
            continue
        if is_number(observed) and not math.isfinite(observed):
            raise ValueError("actual numeric state must be finite")
        if predicted is None or key not in predicted:
            missing.append(key)
            continue
        expected = predicted[key]
        if is_number(expected) and is_number(observed):
            difference = abs(float(expected) - float(observed))
            if not math.isfinite(difference):
                raise ValueError("prediction error must be finite")
            numeric[key] = difference
        elif expected is None or isinstance(expected, (str, bool)) or is_number(expected):
            if is_number(expected) and not math.isfinite(expected):
                raise ValueError("predicted numeric state must be finite")
            categorical[key] = 0.0 if type(expected) is type(observed) and expected == observed else 1.0
        else:
            missing.append(key)
    return PredictionErrors(
        numeric, categorical, tuple(sorted(missing)), tuple(sorted(unsupported)),
        len(actual) - len(unsupported),
    )
