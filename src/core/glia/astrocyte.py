"""Astrocyte sidecar: slow calcium/glutamate-homeostasis modulation only."""
from __future__ import annotations

from dataclasses import asdict, dataclass

from ..biophysical_contracts import ModelProvenance, ModelTimescale


@dataclass(frozen=True, slots=True)
class AstrocyteConfig:
    enabled: bool = False
    calcium_decay: float = 0.98
    uptake_rate: float = 0.05
    modulation_gain: float = 0.1

    def __post_init__(self) -> None:
        if not 0.0 <= self.calcium_decay <= 1.0:
            raise ValueError("calcium_decay must be in [0, 1]")
        if self.uptake_rate < 0.0 or self.modulation_gain < 0.0:
            raise ValueError("rates must be >= 0")


@dataclass(slots=True)
class AstrocyteField:
    config: AstrocyteConfig = AstrocyteConfig()
    calcium: float = 0.0
    extracellular_glutamate: float = 0.0

    @property
    def provenance_tag(self) -> ModelProvenance:
        return ModelProvenance(
            model_id="astrocyte-field-v1",
            version="mhrn-experimental-1",
            timescale=ModelTimescale.PLASTICITY,
            enabled=self.config.enabled,
            parameters=asdict(self.config),
        )

    def plasticity_update(self, synaptic_activity: float) -> float:
        if not self.config.enabled:
            return 1.0
        self.calcium = self.calcium * self.config.calcium_decay + max(0.0, synaptic_activity)
        self.extracellular_glutamate = max(
            0.0,
            self.extracellular_glutamate
            + max(0.0, synaptic_activity)
            - self.config.uptake_rate,
        )
        return 1.0 / (1.0 + self.config.modulation_gain * self.extracellular_glutamate)


__all__ = ["AstrocyteConfig", "AstrocyteField"]
