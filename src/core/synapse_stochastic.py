"""Seeded quantal-release synapse variant built on one coherent STP model."""
from __future__ import annotations

import random
from dataclasses import asdict, dataclass
from typing import Any

from .biophysical_contracts import ModelProvenance, ModelTimescale


@dataclass(frozen=True, slots=True)
class QuantalSynapseConfig:
    enabled: bool = False
    seed: int = 0
    release_sites: int = 4
    release_probability: float = 0.25
    quantal_size: float = 0.05
    facilitation_u: float = 0.2
    tau_recovery_ticks: float = 800.0
    tau_facilitation_ticks: float = 50.0

    def __post_init__(self) -> None:
        if self.release_sites < 1:
            raise ValueError("release_sites must be >= 1")
        if not 0.0 <= self.release_probability <= 1.0:
            raise ValueError("release_probability must be in [0, 1]")
        if self.quantal_size < 0.0:
            raise ValueError("quantal_size must be >= 0")
        if self.tau_recovery_ticks <= 0.0 or self.tau_facilitation_ticks <= 0.0:
            raise ValueError("time constants must be > 0")


@dataclass(slots=True)
class QuantalSTPSynapse:
    target_id: int
    weight: float
    delay: int
    config: QuantalSynapseConfig
    available_fraction: float = 1.0
    facilitation: float = 0.0
    last_tick: int = 0
    release_count: int = 0

    def __post_init__(self) -> None:
        if self.delay < 1:
            raise ValueError("delay must be >= 1")
        self._rng = random.Random(self.config.seed)

    @property
    def provenance_tag(self) -> ModelProvenance:
        return ModelProvenance(
            model_id="quantal-tsodyks-markram-v1",
            version="mhrn-experimental-1",
            timescale=ModelTimescale.TICK,
            enabled=self.config.enabled,
            parameters=asdict(self.config),
            seed=self.config.seed,
        )

    def _recover(self, tick: int) -> None:
        elapsed = max(0, tick - self.last_tick)
        if elapsed == 0:
            return
        self.available_fraction += (
            1.0 - self.available_fraction
        ) * min(1.0, elapsed / self.config.tau_recovery_ticks)
        self.facilitation *= max(
            0.0, 1.0 - elapsed / self.config.tau_facilitation_ticks
        )
        self.available_fraction = min(1.0, max(0.0, self.available_fraction))
        self.facilitation = min(1.0, max(0.0, self.facilitation))

    def release(self, tick: int) -> float:
        if not self.config.enabled:
            return 0.0
        self._recover(tick)
        effective_p = min(
            1.0,
            self.config.release_probability
            * (1.0 + self.facilitation)
            * self.available_fraction,
        )
        quanta = sum(
            1 for _ in range(self.config.release_sites) if self._rng.random() < effective_p
        )
        used_fraction = quanta / self.config.release_sites
        self.available_fraction = max(0.0, self.available_fraction - used_fraction)
        self.facilitation = min(1.0, self.facilitation + self.config.facilitation_u)
        self.last_tick = tick
        self.release_count += quanta
        return self.weight * self.config.quantal_size * quanta

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "target_id": self.target_id,
            "weight": self.weight,
            "delay": self.delay,
            "available_fraction": self.available_fraction,
            "facilitation": self.facilitation,
            "last_tick": self.last_tick,
            "release_count": self.release_count,
            "provenance": self.provenance_tag.to_dict(),
        }


__all__ = ["QuantalSTPSynapse", "QuantalSynapseConfig"]
