"""Backend-neutral PAN parity contract for Wave-5B preflight.

This module defines only comparison semantics. It does not execute CUDA,
freeze PAN semantics, authorize Wave 5B, or create scientific DATA/EVID.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import cast

from src.homeostasis.pan_contract import (
    PAN_CONTRACT_ID,
    PAN_STATE_FIELDS,
    validate_pan_state_mapping,
)

PAN_PARITY_CONTRACT_ID = "mhrn-pan-parity-v0.1-draft"
PAN_PARITY_CONTRACT_STATUS = "DRAFT_PREFLIGHT"

PAN_EXACT_FIELDS: tuple[str, ...] = ("pan_alive", "pan_neuron_id")
PAN_NUMERIC_FIELDS: tuple[str, ...] = tuple(
    field for field in PAN_STATE_FIELDS if field not in {*PAN_EXACT_FIELDS, "pan_x_hd"}
)


@dataclass(frozen=True, slots=True)
class PANParityThresholds:
    """Engineering tolerances for the prospective canonical PAN parity gate."""

    abs_tolerance: float = 1e-12
    require_d3c_exact: bool = True

    def __post_init__(self) -> None:
        if not math.isfinite(self.abs_tolerance) or self.abs_tolerance <= 0.0:
            raise ValueError("abs_tolerance must be finite and > 0")


@dataclass(frozen=True, slots=True)
class PANParityResult:
    """One fail-closed PAN D2 comparison result."""

    passed: bool
    max_abs_error: float
    exact_fields_match: bool
    compared_neurons: int
    compared_dimensions: int
    tolerance: float

    def to_mapping(self) -> dict[str, object]:
        return {
            "classification": "PAN_BACKEND_ENGINEERING_PARITY",
            "scientific_evidence": False,
            "pan_contract_id": PAN_CONTRACT_ID,
            "parity_contract_id": PAN_PARITY_CONTRACT_ID,
            "parity_contract_status": PAN_PARITY_CONTRACT_STATUS,
            **asdict(self),
        }


def _numeric_sequence(value: object, *, name: str) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValueError(f"{name} must be a numeric sequence")
    return cast(Sequence[object], value)


def _finite_number(value: object, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def compare_pan_state_mappings(
    reference: Sequence[Mapping[str, object]],
    candidate: Sequence[Mapping[str, object]],
    *,
    dimensions: int,
    thresholds: PANParityThresholds | None = None,
) -> PANParityResult:
    """Compare continuation-critical PAN state without backend-specific imports."""

    limits = thresholds or PANParityThresholds()
    if len(reference) != len(candidate) or not reference:
        raise ValueError("PAN parity requires equal non-empty state populations")

    max_error = 0.0
    exact = True
    for neuron_index, (reference_state, candidate_state) in enumerate(
        zip(reference, candidate)
    ):
        ref = dict(reference_state)
        got = dict(candidate_state)
        validate_pan_state_mapping(ref, dimensions=dimensions)
        validate_pan_state_mapping(got, dimensions=dimensions)

        for field in PAN_EXACT_FIELDS:
            if ref[field] != got[field]:
                exact = False

        for field in PAN_NUMERIC_FIELDS:
            left = _finite_number(ref[field], name=f"reference[{neuron_index}].{field}")
            right = _finite_number(
                got[field], name=f"candidate[{neuron_index}].{field}"
            )
            max_error = max(max_error, abs(left - right))

        left_vector = _numeric_sequence(
            ref["pan_x_hd"], name=f"reference[{neuron_index}].pan_x_hd"
        )
        right_vector = _numeric_sequence(
            got["pan_x_hd"], name=f"candidate[{neuron_index}].pan_x_hd"
        )
        if len(left_vector) != dimensions or len(right_vector) != dimensions:
            raise ValueError("PAN parity hypervector dimension mismatch")
        for dimension_index, (left_raw, right_raw) in enumerate(
            zip(left_vector, right_vector)
        ):
            left = _finite_number(
                left_raw,
                name=(f"reference[{neuron_index}].pan_x_hd[{dimension_index}]"),
            )
            right = _finite_number(
                right_raw,
                name=(f"candidate[{neuron_index}].pan_x_hd[{dimension_index}]"),
            )
            max_error = max(max_error, abs(left - right))

    return PANParityResult(
        passed=exact and max_error <= limits.abs_tolerance,
        max_abs_error=max_error,
        exact_fields_match=exact,
        compared_neurons=len(reference),
        compared_dimensions=dimensions,
        tolerance=limits.abs_tolerance,
    )


def pan_parity_contract_check() -> bool:
    """Self-check the pure comparison contract without executing a backend."""

    state = {
        "pan_health": 1.0,
        "pan_amplitude": 1.0,
        "pan_energy": 1.0,
        "pan_activity_ema": 0.01,
        "pan_consolidation": 0.0,
        "pan_alive": True,
        "pan_information_proxy": 0.0,
        "pan_x_hd": [0.0] * 5,
        "pan_neuron_id": 0,
    }
    result = compare_pan_state_mappings([state], [dict(state)], dimensions=5)
    return result.passed and result.max_abs_error == 0.0


__all__ = [
    "PAN_EXACT_FIELDS",
    "PAN_NUMERIC_FIELDS",
    "PAN_PARITY_CONTRACT_ID",
    "PAN_PARITY_CONTRACT_STATUS",
    "PANParityResult",
    "PANParityThresholds",
    "compare_pan_state_mappings",
    "pan_parity_contract_check",
]
