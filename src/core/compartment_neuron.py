"""Experimental multi-compartment neuron variant with separable NMDA plateau axis."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .biophysical_contracts import (
    DendriticNonlinearity,
    ModelProvenance,
    ModelTimescale,
    NeuronStructure,
)


@dataclass(frozen=True, slots=True)
class CompartmentConfig:
    enabled: bool = False
    structure: NeuronStructure = NeuronStructure.MULTI_COMPARTMENT
    compartments: int = 3
    dt_ms: float = 1.0
    soma_tau_ms: float = 20.0
    dendrite_tau_ms: float = 40.0
    coupling: float = 0.08
    resting_potential: float = -65.0
    spike_threshold: float = -50.0
    reset_potential: float = -65.0
    dendritic_nonlinearity: DendriticNonlinearity = DendriticNonlinearity.LINEAR
    nmda_plateau_threshold: float = -35.0
    nmda_plateau_gain: float = 4.0
    enable_nmda_plateau: bool = False

    def __post_init__(self) -> None:
        if self.structure is not NeuronStructure.MULTI_COMPARTMENT:
            raise ValueError("CompartmentNeuron requires MULTI_COMPARTMENT structure")
        if self.compartments < 2:
            raise ValueError("compartments must be >= 2")
        if self.dt_ms <= 0.0:
            raise ValueError("dt_ms must be > 0")


@dataclass(slots=True)
class CompartmentNeuron:
    neuron_id: int
    config: CompartmentConfig = CompartmentConfig()
    soma_v: float = -65.0
    spike_counter: int = 0
    last_spike_tick: int = -1
    dendrite_v: list[float] = field(default_factory=list[float])

    def __post_init__(self) -> None:
        expected = self.config.compartments - 1
        if not self.dendrite_v:
            self.dendrite_v = [self.config.resting_potential] * expected
        elif len(self.dendrite_v) != expected:
            raise ValueError("dendrite_v must match configured compartments")

    @property
    def provenance_tag(self) -> ModelProvenance:
        payload = asdict(self.config)
        payload["structure"] = self.config.structure.value
        payload["dendritic_nonlinearity"] = self.config.dendritic_nonlinearity.value
        return ModelProvenance(
            model_id="multi-compartment-v1",
            version="mhrn-experimental-1",
            timescale=ModelTimescale.TICK,
            enabled=self.config.enabled,
            parameters=payload,
        )

    def step(
        self,
        soma_current: float,
        dendritic_currents: tuple[float, ...],
        tick: int,
    ) -> bool:
        if not self.config.enabled:
            return False
        if len(dendritic_currents) != len(self.dendrite_v):
            raise ValueError("dendritic_currents must match configured dendrites")
        dt = self.config.dt_ms
        old = list(self.dendrite_v)
        for index, current in enumerate(dendritic_currents):
            v = old[index]
            neighbour = self.soma_v if index == 0 else old[index - 1]
            coupling = self.config.coupling * (neighbour - v)
            plateau = 0.0
            if (
                self.config.enable_nmda_plateau
                and self.config.dendritic_nonlinearity
                is DendriticNonlinearity.NMDA_PLATEAU
                and v >= self.config.nmda_plateau_threshold
            ):
                plateau = self.config.nmda_plateau_gain
            dv = (
                (self.config.resting_potential - v) + current + coupling + plateau
            ) * (dt / self.config.dendrite_tau_ms)
            self.dendrite_v[index] = v + dv
        dendritic_drive = sum(
            self.config.coupling * (value - self.soma_v) for value in self.dendrite_v
        )
        self.soma_v += (
            (self.config.resting_potential - self.soma_v)
            + soma_current
            + dendritic_drive
        ) * (dt / self.config.soma_tau_ms)
        spiked = self.soma_v >= self.config.spike_threshold
        if spiked:
            self.soma_v = self.config.reset_potential
            self.spike_counter += 1
            self.last_spike_tick = tick
        return spiked

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "neuron_id": self.neuron_id,
            "soma_v": self.soma_v,
            "dendrite_v": list(self.dendrite_v),
            "spike_counter": self.spike_counter,
            "last_spike_tick": self.last_spike_tick,
            "provenance": self.provenance_tag.to_dict(),
        }


__all__ = ["CompartmentConfig", "CompartmentNeuron"]
