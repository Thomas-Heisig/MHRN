"""Contracts shared by experimental biophysical model variants.

These types make model selection, ablation and timescale ownership explicit.
They intentionally do not mutate the canonical point-neuron or synapse schemas.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any, Protocol


class NeuronStructure(StrEnum):
    POINT = "point"
    MULTI_COMPARTMENT = "multi_compartment"


class DendriticNonlinearity(StrEnum):
    LINEAR = "linear"
    NMDA_PLATEAU = "nmda_plateau"


class ModelTimescale(StrEnum):
    TICK = "tick"
    PLASTICITY = "plasticity"
    CONSOLIDATION = "consolidation"
    DEVELOPMENT = "development"


@dataclass(frozen=True, slots=True)
class ModelProvenance:
    model_id: str
    version: str
    timescale: ModelTimescale
    enabled: bool
    parameters: dict[str, Any]
    seed: int | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["timescale"] = self.timescale.value
        return data


class TickMechanism(Protocol):
    def step(self, *args: Any, **kwargs: Any) -> Any: ...


class PlasticityMechanism(Protocol):
    def plasticity_update(self, *args: Any, **kwargs: Any) -> Any: ...


class ConsolidationMechanism(Protocol):
    def consolidate(self, *args: Any, **kwargs: Any) -> Any: ...


class DevelopmentMechanism(Protocol):
    def develop(self, *args: Any, **kwargs: Any) -> Any: ...


__all__ = [
    "ConsolidationMechanism",
    "DendriticNonlinearity",
    "DevelopmentMechanism",
    "ModelProvenance",
    "ModelTimescale",
    "NeuronStructure",
    "PlasticityMechanism",
    "TickMechanism",
]
