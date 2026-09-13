"""Microglia sidecar: slow structural surveillance and pruning proposals."""
from __future__ import annotations

from dataclasses import asdict, dataclass

from ..biophysical_contracts import ModelProvenance, ModelTimescale


@dataclass(frozen=True, slots=True)
class MicrogliaConfig:
    enabled: bool = False
    prune_confidence_threshold: float = 0.1
    inflammation_threshold: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.prune_confidence_threshold <= 1.0:
            raise ValueError("prune_confidence_threshold must be in [0, 1]")
        if self.inflammation_threshold < 0.0:
            raise ValueError("inflammation_threshold must be >= 0")


@dataclass(frozen=True, slots=True)
class MicrogliaProposal:
    action: str
    pre_id: int
    post_id: int
    reason: str


@dataclass(slots=True)
class MicrogliaField:
    config: MicrogliaConfig = MicrogliaConfig()
    inflammatory_state: float = 0.0

    @property
    def provenance_tag(self) -> ModelProvenance:
        return ModelProvenance(
            model_id="microglia-structural-v1",
            version="mhrn-experimental-1",
            timescale=ModelTimescale.DEVELOPMENT,
            enabled=self.config.enabled,
            parameters=asdict(self.config),
        )

    def develop(
        self,
        pre_id: int,
        post_id: int,
        *,
        confidence: float,
        damage_signal: float = 0.0,
    ) -> MicrogliaProposal | None:
        if not self.config.enabled:
            return None
        self.inflammatory_state = max(0.0, 0.99 * self.inflammatory_state + damage_signal)
        if confidence < self.config.prune_confidence_threshold:
            return MicrogliaProposal("prune", pre_id, post_id, "low-confidence")
        if self.inflammatory_state >= self.config.inflammation_threshold:
            return MicrogliaProposal("prune", pre_id, post_id, "damage-response")
        return None


__all__ = ["MicrogliaConfig", "MicrogliaField", "MicrogliaProposal"]
