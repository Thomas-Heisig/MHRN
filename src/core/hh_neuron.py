"""Deterministic Hodgkin-Huxley style neuron variant.

This is an alternative neuron body with explicit gating state. It is not mixed
into the canonical :class:`src.core.neuron.Neuron` dataclass.
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from .biophysical_contracts import ModelProvenance, ModelTimescale


def _vtrap(x: float, y: float) -> float:
    if abs(x / y) < 1e-6:
        return y * (1.0 - x / (2.0 * y))
    return x / (math.exp(x / y) - 1.0)


@dataclass(frozen=True, slots=True)
class HHConfig:
    enabled: bool = False
    dt_ms: float = 0.025
    capacitance: float = 1.0
    g_na: float = 120.0
    g_k: float = 36.0
    g_ca: float = 0.0
    g_leak: float = 0.3
    e_na: float = 50.0
    e_k: float = -77.0
    e_ca: float = 120.0
    e_leak: float = -54.387
    spike_threshold_mv: float = 0.0
    enable_na: bool = True
    enable_k: bool = True
    enable_ca: bool = False

    def __post_init__(self) -> None:
        if self.dt_ms <= 0.0:
            raise ValueError("dt_ms must be > 0")
        if self.capacitance <= 0.0:
            raise ValueError("capacitance must be > 0")


@dataclass(slots=True)
class HodgkinHuxleyNeuron:
    neuron_id: int
    config: HHConfig = HHConfig()
    v: float = -65.0
    m: float = 0.0529
    h: float = 0.5961
    n: float = 0.3177
    ca_gate: float = 0.0
    spike_counter: int = 0
    last_spike_tick: int = -1
    _was_above_threshold: bool = False

    @property
    def provenance_tag(self) -> ModelProvenance:
        return ModelProvenance(
            model_id="hodgkin-huxley-na-k-ca-v1",
            version="mhrn-experimental-1",
            timescale=ModelTimescale.TICK,
            enabled=self.config.enabled,
            parameters=asdict(self.config),
        )

    def _rates(self) -> tuple[float, float, float, float, float, float]:
        v = self.v
        alpha_m = 0.1 * _vtrap(-(v + 40.0), 10.0)
        beta_m = 4.0 * math.exp(-(v + 65.0) / 18.0)
        alpha_h = 0.07 * math.exp(-(v + 65.0) / 20.0)
        beta_h = 1.0 / (math.exp(-(v + 35.0) / 10.0) + 1.0)
        alpha_n = 0.01 * _vtrap(-(v + 55.0), 10.0)
        beta_n = 0.125 * math.exp(-(v + 65.0) / 80.0)
        return alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n

    def step(self, input_current: float, tick: int) -> bool:
        if not self.config.enabled:
            return False
        dt = self.config.dt_ms
        am, bm, ah, bh, an, bn = self._rates()
        self.m += dt * (am * (1.0 - self.m) - bm * self.m)
        self.h += dt * (ah * (1.0 - self.h) - bh * self.h)
        self.n += dt * (an * (1.0 - self.n) - bn * self.n)
        self.m = min(1.0, max(0.0, self.m))
        self.h = min(1.0, max(0.0, self.h))
        self.n = min(1.0, max(0.0, self.n))

        i_na = 0.0
        if self.config.enable_na:
            i_na = self.config.g_na * (self.m**3) * self.h * (self.v - self.config.e_na)
        i_k = 0.0
        if self.config.enable_k:
            i_k = self.config.g_k * (self.n**4) * (self.v - self.config.e_k)
        i_ca = 0.0
        if self.config.enable_ca:
            self.ca_gate += dt * ((1.0 / (1.0 + math.exp(-(self.v + 20.0) / 6.5))) - self.ca_gate) / 5.0
            self.ca_gate = min(1.0, max(0.0, self.ca_gate))
            i_ca = self.config.g_ca * (self.ca_gate**2) * (self.v - self.config.e_ca)
        i_leak = self.config.g_leak * (self.v - self.config.e_leak)
        dv = (input_current - i_na - i_k - i_ca - i_leak) / self.config.capacitance
        self.v += dt * dv

        above = self.v >= self.config.spike_threshold_mv
        spiked = above and not self._was_above_threshold
        self._was_above_threshold = above
        if spiked:
            self.spike_counter += 1
            self.last_spike_tick = tick
        return spiked

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "neuron_id": self.neuron_id,
            "v": self.v,
            "m": self.m,
            "h": self.h,
            "n": self.n,
            "ca_gate": self.ca_gate,
            "spike_counter": self.spike_counter,
            "last_spike_tick": self.last_spike_tick,
            "config": asdict(self.config),
            "provenance": self.provenance_tag.to_dict(),
        }


__all__ = ["HHConfig", "HodgkinHuxleyNeuron"]
