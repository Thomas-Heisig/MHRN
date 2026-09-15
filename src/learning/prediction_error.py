"""Independent environment-prediction-error modulation for eligibility traces.

Prediction error is deliberately not routed through ``LearningEngine.set_reward``.
This module provides an experimental third-factor path that can be enabled and
ablated independently from external reward. It is a hypothesis probe, not a
claim that environment error is a biological reward signal.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .learning_engine import LearningEngine


class PredictionErrorPlasticityError(ValueError):
    """Raised for invalid prediction-error plasticity input."""


@dataclass(frozen=True, slots=True)
class PredictionErrorSignal:
    """Scalar environment prediction discrepancy at one runtime tick."""

    value: float
    tick: int
    source: str = "environment_prediction_error"

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not math.isfinite(self.value):
            raise PredictionErrorPlasticityError("prediction error must be finite")
        if type(self.tick) is not int or self.tick < 0:
            raise PredictionErrorPlasticityError(
                "prediction-error tick must be >= 0"
            )
        if not self.source.strip():
            raise PredictionErrorPlasticityError("prediction-error source is required")


@dataclass(frozen=True, slots=True)
class PredictionErrorPlasticityConfig:
    """Independent modulation parameters; reward configuration is not reused."""

    enabled: bool = False
    learning_rate: float = 0.01
    trace_epsilon: float = 1e-12
    clamp_weights: bool = True

    def __post_init__(self) -> None:
        if self.learning_rate < 0.0 or not math.isfinite(self.learning_rate):
            raise PredictionErrorPlasticityError(
                "learning_rate must be finite and >= 0"
            )
        if self.trace_epsilon < 0.0 or not math.isfinite(self.trace_epsilon):
            raise PredictionErrorPlasticityError(
                "trace_epsilon must be finite and >= 0"
            )


@dataclass(frozen=True, slots=True)
class PredictionErrorPlasticityStats:
    signals_received: int
    signals_applied: int
    weight_updates: int


class PredictionErrorPlasticity:
    """Apply prediction error to existing eligibility without invoking reward."""

    def __init__(
        self,
        learning: LearningEngine,
        config: PredictionErrorPlasticityConfig = PredictionErrorPlasticityConfig(),
    ) -> None:
        if not learning.params.eligibility_enabled:
            raise PredictionErrorPlasticityError(
                "prediction-error plasticity requires eligibility.enabled=true"
            )
        self.learning = learning
        self.config = config
        self._signals_received = 0
        self._signals_applied = 0
        self._weight_updates = 0

    @property
    def stats(self) -> PredictionErrorPlasticityStats:
        return PredictionErrorPlasticityStats(
            self._signals_received,
            self._signals_applied,
            self._weight_updates,
        )

    def apply(self, signal: PredictionErrorSignal) -> int:
        """Apply one PE signal to eligible synapses and return changed weights."""

        self._signals_received += 1
        if not self.config.enabled:
            return 0

        changed = 0
        network = self.learning.network
        for pre_id in sorted(network.synapses):
            for synapse in sorted(
                network.synapses[pre_id], key=lambda item: item.target_id
            ):
                eligibility = self.learning.get_eligibility(
                    pre_id, synapse.target_id, signal.tick
                )
                if abs(eligibility) <= self.config.trace_epsilon:
                    continue
                delta = self.config.learning_rate * signal.value * eligibility
                candidate = synapse.weight + delta
                if self.config.clamp_weights:
                    candidate = max(
                        self.learning.params.min_weight,
                        min(self.learning.params.max_weight, candidate),
                    )
                if candidate != synapse.weight:
                    synapse.weight = candidate
                    synapse.mark_dirty()
                    changed += 1
        self._signals_applied += 1
        self._weight_updates += changed
        return changed


__all__ = [
    "PredictionErrorPlasticity",
    "PredictionErrorPlasticityConfig",
    "PredictionErrorPlasticityError",
    "PredictionErrorPlasticityStats",
    "PredictionErrorSignal",
]
