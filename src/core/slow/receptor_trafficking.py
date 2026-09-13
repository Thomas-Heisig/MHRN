"""Subsynaptic receptor availability that modulates transmission, not weight."""
from __future__ import annotations

from dataclasses import asdict, dataclass

from ..biophysical_contracts import ModelProvenance, ModelTimescale


@dataclass(frozen=True, slots=True)
class ReceptorTraffickingConfig:
    enabled: bool = False
    insertion_rate: float = 0.02
    removal_rate: float = 0.01
    baseline_availability: float = 1.0

    def __post_init__(self) -> None:
        if self.insertion_rate < 0.0 or self.removal_rate < 0.0:
            raise ValueError("rates must be >= 0")
        if not 0.0 <= self.baseline_availability <= 1.0:
            raise ValueError("baseline_availability must be in [0, 1]")


@dataclass(slots=True)
class ReceptorTraffickingState:
    availability: float = 1.0


@dataclass(slots=True)
class ReceptorTrafficking:
    config: ReceptorTraffickingConfig = ReceptorTraffickingConfig()

    @property
    def provenance_tag(self) -> ModelProvenance:
        return ModelProvenance(
            model_id="receptor-trafficking-v1",
            version="mhrn-experimental-1",
            timescale=ModelTimescale.PLASTICITY,
            enabled=self.config.enabled,
            parameters=asdict(self.config),
        )

    def plasticity_update(
        self,
        state: ReceptorTraffickingState,
        *,
        insertion_signal: float,
        removal_signal: float,
    ) -> float:
        if not self.config.enabled:
            return state.availability
        delta = (
            self.config.insertion_rate * max(0.0, insertion_signal)
            - self.config.removal_rate * max(0.0, removal_signal)
        )
        state.availability = min(1.0, max(0.0, state.availability + delta))
        return state.availability

    @staticmethod
    def transmission(weight: float, state: ReceptorTraffickingState) -> float:
        return weight * state.availability


__all__ = [
    "ReceptorTrafficking",
    "ReceptorTraffickingConfig",
    "ReceptorTraffickingState",
]
