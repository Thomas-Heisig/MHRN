"""Slow tag-to-capture consolidation with an explicit finite capture window."""
from __future__ import annotations

from dataclasses import asdict, dataclass

from ..biophysical_contracts import ModelProvenance, ModelTimescale


@dataclass(frozen=True, slots=True)
class ProteinSynthesisConfig:
    enabled: bool = False
    capture_window_ticks: int = 3_600_000
    synthesis_threshold: float = 0.5
    consolidation_rate: float = 0.05

    def __post_init__(self) -> None:
        if self.capture_window_ticks < 1:
            raise ValueError("capture_window_ticks must be >= 1")
        if not 0.0 <= self.synthesis_threshold <= 1.0:
            raise ValueError("synthesis_threshold must be in [0, 1]")
        if not 0.0 <= self.consolidation_rate <= 1.0:
            raise ValueError("consolidation_rate must be in [0, 1]")


@dataclass(slots=True)
class TagCaptureState:
    tagged_tick: int | None = None
    tag_strength: float = 0.0
    protein_pool: float = 0.0
    consolidation: float = 0.0


@dataclass(slots=True)
class SlowConsolidation:
    config: ProteinSynthesisConfig = ProteinSynthesisConfig()

    @property
    def provenance_tag(self) -> ModelProvenance:
        return ModelProvenance(
            model_id="protein-tag-capture-v1",
            version="mhrn-experimental-1",
            timescale=ModelTimescale.CONSOLIDATION,
            enabled=self.config.enabled,
            parameters=asdict(self.config),
        )

    def tag(self, state: TagCaptureState, *, tick: int, strength: float) -> None:
        state.tagged_tick = tick
        state.tag_strength = min(1.0, max(0.0, strength))

    def consolidate(
        self,
        state: TagCaptureState,
        *,
        tick: int,
        synthesis_signal: float,
    ) -> float:
        if not self.config.enabled or state.tagged_tick is None:
            return state.consolidation
        age = tick - state.tagged_tick
        if age < 0 or age > self.config.capture_window_ticks:
            state.tag_strength = 0.0
            state.tagged_tick = None
            return state.consolidation
        if synthesis_signal >= self.config.synthesis_threshold:
            state.protein_pool = min(1.0, state.protein_pool + synthesis_signal)
        captured = min(state.tag_strength, state.protein_pool)
        if captured > 0.0:
            delta = self.config.consolidation_rate * captured
            state.consolidation = min(1.0, state.consolidation + delta)
            state.protein_pool = max(0.0, state.protein_pool - delta)
        return state.consolidation


__all__ = ["ProteinSynthesisConfig", "SlowConsolidation", "TagCaptureState"]
