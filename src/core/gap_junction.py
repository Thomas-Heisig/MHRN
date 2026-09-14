"""Bidirectional ohmic coupling kept separate from directed chemical synapses."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .biophysical_contracts import ModelProvenance, ModelTimescale


@dataclass(frozen=True, slots=True)
class GapJunctionConfig:
    enabled: bool = False
    conductance: float = 0.01

    def __post_init__(self) -> None:
        if self.conductance < 0.0:
            raise ValueError("conductance must be >= 0")


@dataclass(slots=True)
class GapJunction:
    neuron_a: int
    neuron_b: int
    config: GapJunctionConfig = GapJunctionConfig()

    def __post_init__(self) -> None:
        if self.neuron_a == self.neuron_b:
            raise ValueError("gap junction endpoints must differ")

    @property
    def provenance_tag(self) -> ModelProvenance:
        return ModelProvenance(
            model_id="gap-junction-ohmic-v1",
            version="mhrn-experimental-1",
            timescale=ModelTimescale.TICK,
            enabled=self.config.enabled,
            parameters=asdict(self.config),
        )

    def currents(self, voltage_a: float, voltage_b: float) -> tuple[float, float]:
        if not self.config.enabled:
            return 0.0, 0.0
        current_a = self.config.conductance * (voltage_b - voltage_a)
        return current_a, -current_a


__all__ = ["GapJunction", "GapJunctionConfig"]
