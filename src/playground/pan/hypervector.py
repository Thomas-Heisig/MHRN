"""Hypervector operations for exploratory PAN state representations."""

from __future__ import annotations

import math
from collections.abc import Sequence

BASE_AXES: tuple[tuple[str, str, str, str], ...] = (
    (
        "intrinsic_time",
        "t",
        "Intrinsic simulation time; never wall-clock time.",
        "R+",
    ),
    (
        "excitability",
        "E",
        "Normalized membrane excitability proxy.",
        "[0,1]",
    ),
    (
        "plasticity",
        "P",
        "Current exploratory plasticity activity.",
        "[0,1]",
    ),
    (
        "information_proxy",
        "I*",
        "Local surprise proxy; not a validated PID quantity.",
        "[0,1]",
    ),
    (
        "health",
        "H",
        "Exploratory health / survival state.",
        "[0,1]",
    ),
    (
        "neuromodulation",
        "N",
        "Bounded exploratory neuromodulatory state.",
        "[0,1]",
    ),
    (
        "energy",
        "ATP*",
        "Normalized exploratory energy budget.",
        "[0,1]",
    ),
    (
        "embodied_position",
        "R",
        "Scalar projection of the assigned topology coordinate.",
        "[0,1]",
    ),
    (
        "consolidation",
        "C",
        "Activity-history consolidation proxy.",
        "[0,1]",
    ),
    (
        "network_coupling",
        "S",
        "Normalized local coupling / degree proxy.",
        "[0,1]",
    ),
)


def axis_schema(dimensions: int) -> list[dict[str, object]]:
    """Return neutral metadata for a PAN hyperstate with D >= 5."""

    if not 5 <= dimensions <= 32:
        raise ValueError("PAN hypervector dimensions must be between 5 and 32")
    axes: list[dict[str, object]] = []
    for index in range(dimensions):
        if index < len(BASE_AXES):
            name, symbol, meaning, value_range = BASE_AXES[index]
        else:
            name = f"latent_{index + 1}"
            symbol = f"L{index + 1}"
            meaning = "Unassigned exploratory latent axis."
            value_range = "R"
        axes.append(
            {
                "dimension": index + 1,
                "name": name,
                "symbol": symbol,
                "meaning": meaning,
                "range": value_range,
            }
        )
    return axes


def _same_width(a: Sequence[float], b: Sequence[float]) -> None:
    if len(a) != len(b):
        raise ValueError("hypervectors must have equal dimensions")


def bind(
    a: Sequence[float],
    b: Sequence[float],
    *,
    method: str = "hadamard",
) -> list[float]:
    """Bind two equal-width hypervectors without scientific interpretation."""

    _same_width(a, b)
    if method == "hadamard":
        return [float(left) * float(right) for left, right in zip(a, b)]
    if method == "circular_convolution":
        width = len(a)
        if width == 0:
            return []
        return [
            sum(
                float(a[index]) * float(b[(out - index) % width])
                for index in range(width)
            )
            for out in range(width)
        ]
    raise ValueError(f"unknown PAN binding method: {method}")


def bundle(vectors: Sequence[Sequence[float]]) -> list[float]:
    """Bundle hypervectors by the sign of their component-wise sum."""

    if not vectors:
        return []
    width = len(vectors[0])
    if any(len(vector) != width for vector in vectors):
        raise ValueError("all hypervectors must have equal dimensions")
    sums = [sum(float(vector[index]) for vector in vectors) for index in range(width)]
    return [0.0 if value == 0.0 else math.copysign(1.0, value) for value in sums]
