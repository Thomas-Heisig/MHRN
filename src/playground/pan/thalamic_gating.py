"""Functional thalamic-style gating for the isolated PAN Playground.

This is a control/gating abstraction, not a biological thalamus model.
"""

from __future__ import annotations

from collections.abc import Sequence


class ThalamicGating:
    """Apply bounded relay/attention/inhibition gains to external current."""

    def __init__(
        self,
        *,
        n_neurons: int,
        relay_threshold: float = 0.0,
        attention_gain: float = 1.15,
        inhibition_gain: float = 0.35,
    ) -> None:
        if n_neurons < 1:
            raise ValueError("n_neurons must be positive")
        if not 0.0 <= relay_threshold <= 1.0:
            raise ValueError("relay_threshold must be between 0 and 1")
        if not 0.0 <= attention_gain <= 4.0:
            raise ValueError("attention_gain must be between 0 and 4")
        if not 0.0 <= inhibition_gain <= 1.0:
            raise ValueError("inhibition_gain must be between 0 and 1")
        self.n_neurons = n_neurons
        self.relay_threshold = relay_threshold
        self.attention_gain = attention_gain
        self.inhibition_gain = inhibition_gain
        self.activity_ema = 0.0
        self.gated_ticks = 0
        self.relay_ticks = 0

    def apply(
        self,
        currents: Sequence[float],
        previous_spikes: Sequence[int],
    ) -> list[float]:
        if len(currents) != self.n_neurons:
            raise ValueError("current vector size mismatch")
        instant = len(previous_spikes) / self.n_neurons
        self.activity_ema = 0.9 * self.activity_ema + 0.1 * instant
        if self.activity_ema >= self.relay_threshold:
            self.relay_ticks += 1
            gain = self.attention_gain
        else:
            self.gated_ticks += 1
            gain = self.inhibition_gain
        return [float(value) * gain for value in currents]

    def summary(self) -> dict[str, object]:
        return {
            "classification": "PLAYGROUND_THALAMIC_GATING",
            "scientific_evidence": False,
            "biological_equivalence_claim": False,
            "mode": "FUNCTIONAL_GATE_REFERENCE",
            "relay_threshold": self.relay_threshold,
            "attention_gain": self.attention_gain,
            "inhibition_gain": self.inhibition_gain,
            "activity_ema": self.activity_ema,
            "relay_ticks": self.relay_ticks,
            "gated_ticks": self.gated_ticks,
        }
