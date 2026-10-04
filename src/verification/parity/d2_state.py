"""D2 continuous-state parity with fail-closed numeric handling."""

from __future__ import annotations

import math
from collections.abc import Sequence

from .contract import ParityClass, ParityResult


def max_abs_error(reference: Sequence[float], candidate: Sequence[float]) -> float:
    if len(reference) != len(candidate):
        raise ValueError("parity vectors must have the same length")
    if not reference:
        raise ValueError("parity vectors must not be empty")
    left_values = [float(value) for value in reference]
    right_values = [float(value) for value in candidate]
    if not all(math.isfinite(value) for value in left_values):
        raise ValueError("reference parity vector contains NaN/Inf")
    if not all(math.isfinite(value) for value in right_values):
        raise ValueError("candidate parity vector contains NaN/Inf")
    return max(abs(left - right) for left, right in zip(left_values, right_values))


def state_vector_parity(
    reference: Sequence[float],
    candidate: Sequence[float],
    *,
    tolerance: float,
) -> ParityResult:
    try:
        if (
            isinstance(tolerance, bool)
            or not isinstance(tolerance, (int, float))
            or not math.isfinite(tolerance)
            or tolerance < 0.0
        ):
            raise ValueError("tolerance must be finite and non-negative")
        error = max_abs_error(reference, candidate)
    except ValueError as exc:
        return ParityResult(
            ParityClass.D2,
            passed=False,
            details={
                "max_abs_error": None,
                "tolerance": tolerance,
                "failure_reason": str(exc),
            },
        )
    return ParityResult(
        ParityClass.D2,
        passed=error <= tolerance,
        details={
            "max_abs_error": error,
            "tolerance": tolerance,
            "failure_reason": None,
        },
    )
