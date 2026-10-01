"""Frozen model profiles for the bounded CUDA recurrent reference.

These profiles preserve the hardware-tested CUDA-1.4/1.5 membrane semantics
without importing the exploratory Playground registry. They are engineering
compatibility profiles, not a new scientific neuron-model registry.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Final


@dataclass(frozen=True, slots=True)
class CudaReferenceModelProfile:
    name: str
    parameters: Mapping[str, float]
    family: str


_PROFILES: Final[dict[str, CudaReferenceModelProfile]] = {
    "lif": CudaReferenceModelProfile(
        "lif",
        MappingProxyType(
            {
                "v_rest": -65.0,
                "threshold": -50.0,
                "reset": -65.0,
                "tau_m_ms": 20.0,
                "resistance": 1.0,
            }
        ),
        "bounded-lif-reference",
    ),
    "adex": CudaReferenceModelProfile(
        "adex",
        MappingProxyType(
            {
                "v_rest": -65.0,
                "v_t": -50.0,
                "delta_t": 2.0,
                "tau_m_ms": 20.0,
                "tau_w_ms": 120.0,
                "a": 0.02,
                "b": 0.5,
                "threshold": 20.0,
                "reset": -58.0,
            }
        ),
        "bounded-adex-reference",
    ),
    "pan_adex_5d": CudaReferenceModelProfile(
        "pan_adex_5d",
        MappingProxyType(
            {
                "v_rest": -65.0,
                "v_t": -55.0,
                "delta_t": 2.0,
                "tau_m_ms": 20.0,
                "tau_w_ms": 120.0,
                "a": 0.02,
                "b": 0.5,
                "threshold": -20.0,
                "reset": -60.0,
            }
        ),
        "bounded-pan-adex-membrane-reference",
    ),
}

SUPPORTED_MODELS: Final[frozenset[str]] = frozenset(_PROFILES)


def cuda_reference_model_profile(name: str) -> CudaReferenceModelProfile:
    try:
        return _PROFILES[name]
    except KeyError as exc:
        raise ValueError(f"unsupported recurrent membrane model: {name}") from exc


def step_reference(
    profile: CudaReferenceModelProfile,
    state: dict[str, Any],
    current: float,
    dt_ms: float,
) -> bool:
    params = profile.parameters
    v = float(state["v"])
    if profile.name == "lif":
        tau = max(params["tau_m_ms"], 1e-6)
        v += dt_ms * (
            (params["v_rest"] - v + params.get("resistance", 1.0) * current) / tau
        )
        spiked = v >= params["threshold"]
        state["v"] = params["reset"] if spiked else v
        state["w"] = float(state.get("w", 0.0))
        return spiked

    w = float(state.get("w", 0.0))
    exponent = min(20.0, (v - params["v_t"]) / params["delta_t"])
    dv = (
        -(v - params["v_rest"]) + params["delta_t"] * math.exp(exponent) - w + current
    ) / params["tau_m_ms"]
    dw = (params["a"] * (v - params["v_rest"]) - w) / params["tau_w_ms"]
    v += dt_ms * dv
    w += dt_ms * dw
    spiked = v >= params["threshold"]
    if spiked:
        v = params["reset"]
        w += params["b"]
    state["v"] = v
    state["w"] = w
    return spiked
