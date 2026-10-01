"""Draft canonical state contract for PAN hyperstate integration.

This module defines the backend-neutral state surface and the current
Playground reference coefficients without promoting PAN to a canonical
scientific mechanism. The contract is deliberately marked DRAFT until
RQ-PAN-SEM-001 is reviewed and frozen.

Canonical MHRN modules may import this module. It must never import
src.playground.
"""

from __future__ import annotations

import math
from collections.abc import MutableMapping, Sequence
from dataclasses import dataclass
from typing import cast

PAN_CONTRACT_ID = "mhrn-pan-hyperstate-v0.1-draft"
PAN_CONTRACT_STATUS = "DRAFT_NOT_FROZEN"

PAN_STATE_FIELDS: tuple[str, ...] = (
    "pan_health",
    "pan_amplitude",
    "pan_energy",
    "pan_activity_ema",
    "pan_consolidation",
    "pan_alive",
    "pan_information_proxy",
    "pan_x_hd",
    "pan_neuron_id",
)

PAN_UPDATE_ORDER: tuple[str, ...] = (
    "activity_ema",
    "energy",
    "information_proxy",
    "stress_and_health",
    "consolidation",
    "amplitude",
    "hyperstate_vector",
    "apoptosis_eligibility",
    "population_reduction",
    "feedback_history",
)


@dataclass(frozen=True, slots=True)
class PANFormulaParameters:
    """Versioned coefficients used by the current exploratory PAN reference.

    These values describe existing engineering semantics. Their presence here
    does not validate biological meaning, PAN scientific validity or GPU
    equivalence.
    """

    activity_decay: float = 0.97
    activity_spike_gain: float = 0.03
    energy_recovery: float = 0.015
    energy_spike_cost: float = 0.035
    target_activity: float = 0.02
    energy_stress_floor: float = 0.35
    information_bits_scale: float = 8.0
    health_stress_loss: float = 0.0015
    health_recovery_gain: float = 0.0005
    consolidation_decay: float = 0.995
    consolidation_spike_gain: float = 0.005
    amplitude_floor: float = 0.2
    amplitude_health_gain: float = 0.8
    excitability_scale_mv: float = 5.0
    neuromodulation_period_ticks: int = 64

    def __post_init__(self) -> None:
        unit_interval = {
            "activity_decay": self.activity_decay,
            "target_activity": self.target_activity,
            "energy_stress_floor": self.energy_stress_floor,
            "consolidation_decay": self.consolidation_decay,
            "amplitude_floor": self.amplitude_floor,
        }
        for name, value in unit_interval.items():
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be finite and within [0,1]")

        non_negative = {
            "activity_spike_gain": self.activity_spike_gain,
            "energy_recovery": self.energy_recovery,
            "energy_spike_cost": self.energy_spike_cost,
            "health_stress_loss": self.health_stress_loss,
            "health_recovery_gain": self.health_recovery_gain,
            "consolidation_spike_gain": self.consolidation_spike_gain,
            "amplitude_health_gain": self.amplitude_health_gain,
        }
        for name, value in non_negative.items():
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and >= 0")

        if (
            not math.isfinite(self.information_bits_scale)
            or self.information_bits_scale <= 0.0
        ):
            raise ValueError("information_bits_scale must be finite and > 0")
        if (
            not math.isfinite(self.excitability_scale_mv)
            or self.excitability_scale_mv <= 0.0
        ):
            raise ValueError("excitability_scale_mv must be finite and > 0")
        if self.neuromodulation_period_ticks < 1:
            raise ValueError("neuromodulation_period_ticks must be >= 1")


def initialize_pan_state_mapping(
    state: MutableMapping[str, object],
    *,
    neuron_id: int,
    dimensions: int,
) -> None:
    """Initialize the exact state surface used by the current reference."""

    if neuron_id < 0:
        raise ValueError("neuron_id must be >= 0")
    if not 5 <= dimensions <= 32:
        raise ValueError("PAN dimensions must be between 5 and 32")

    state["pan_health"] = 1.0
    state["pan_amplitude"] = 1.0
    state["pan_energy"] = 1.0
    state["pan_activity_ema"] = 0.01
    state["pan_consolidation"] = 0.0
    state["pan_alive"] = True
    state["pan_information_proxy"] = 0.0
    state["pan_x_hd"] = [0.0 for _ in range(dimensions)]
    state["pan_neuron_id"] = neuron_id


def _finite_number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def validate_pan_state_mapping(
    state: MutableMapping[str, object],
    *,
    dimensions: int,
) -> None:
    """Validate continuation-critical PAN state fail-closed."""

    if not 5 <= dimensions <= 32:
        raise ValueError("PAN dimensions must be between 5 and 32")

    for name in (
        "pan_health",
        "pan_amplitude",
        "pan_energy",
        "pan_activity_ema",
        "pan_consolidation",
        "pan_information_proxy",
    ):
        value = _finite_number(state.get(name), name)
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be within [0,1]")

    if not isinstance(state.get("pan_alive"), bool):
        raise ValueError("pan_alive must be boolean")

    neuron_id = state.get("pan_neuron_id")
    if isinstance(neuron_id, bool) or not isinstance(neuron_id, int) or neuron_id < 0:
        raise ValueError("pan_neuron_id must be an integer >= 0")

    vector_value = state.get("pan_x_hd")
    if not isinstance(vector_value, Sequence) or isinstance(
        vector_value, (str, bytes, bytearray)
    ):
        raise ValueError("pan_x_hd must be a numeric sequence")
    vector = cast(Sequence[object], vector_value)
    if len(vector) != dimensions:
        raise ValueError("pan_x_hd dimension mismatch")
    for index, component in enumerate(vector):
        _finite_number(component, f"pan_x_hd[{index}]")


def pan_contract_check() -> bool:
    """Self-check the draft contract without executing Playground logic."""

    state: dict[str, object] = {}
    initialize_pan_state_mapping(state, neuron_id=0, dimensions=5)
    validate_pan_state_mapping(state, dimensions=5)
    return tuple(state.keys()) == PAN_STATE_FIELDS and len(PAN_UPDATE_ORDER) == len(
        set(PAN_UPDATE_ORDER)
    )


__all__ = [
    "PAN_CONTRACT_ID",
    "PAN_CONTRACT_STATUS",
    "PAN_STATE_FIELDS",
    "PAN_UPDATE_ORDER",
    "PANFormulaParameters",
    "initialize_pan_state_mapping",
    "pan_contract_check",
    "validate_pan_state_mapping",
]
