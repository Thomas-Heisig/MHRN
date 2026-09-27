"""Neuron-model registry used only by exploratory playground sessions.

The registry deliberately exposes model families as neutral building blocks.
No entry is recommended or promoted by this module.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

State = dict[str, Any]
StepFunction = Callable[[State, float, float, Mapping[str, float]], bool]
StateFactory = Callable[[Mapping[str, float]], State]


@dataclass(frozen=True, slots=True)
class NeuronModelSpec:
    name: str
    label: str
    family: str
    parameters: Mapping[str, float]
    compatible_dimensions: tuple[int, ...] | None
    state_factory: StateFactory
    step: StepFunction
    experimental: bool = False
    note: str = ""

    def supports_dimensions(self, dimensions: int) -> bool:
        return (
            self.compatible_dimensions is None
            or dimensions in self.compatible_dimensions
        )

    def descriptor(self) -> dict[str, object]:
        return {
            "name": self.name,
            "label": self.label,
            "family": self.family,
            "parameters": dict(self.parameters),
            "compatible_dimensions": (
                "any"
                if self.compatible_dimensions is None
                else list(self.compatible_dimensions)
            ),
            "experimental": self.experimental,
            "note": self.note,
        }


def _izh_state(params: Mapping[str, float]) -> State:
    v = params.get("v0", -65.0)
    return {"v": v, "u": params["b"] * v}


def _izh_step(
    state: State, current: float, dt_ms: float, params: Mapping[str, float]
) -> bool:
    v = float(state["v"])
    u = float(state["u"])
    half = dt_ms / 2.0
    for _ in range(2):
        v += half * (0.04 * v * v + 5.0 * v + 140.0 - u + current)
    u += dt_ms * params["a"] * (params["b"] * v - u)
    spiked = v >= params.get("threshold", 30.0)
    if spiked:
        v = params["c"]
        u += params["d"]
    state["v"] = v
    state["u"] = u
    return spiked


def _lif_state(params: Mapping[str, float]) -> State:
    return {"v": params["v_rest"]}


def _lif_step(
    state: State, current: float, dt_ms: float, params: Mapping[str, float]
) -> bool:
    v = float(state["v"])
    tau = max(params["tau_m_ms"], 1e-6)
    v += dt_ms * (
        (params["v_rest"] - v + params.get("resistance", 1.0) * current) / tau
    )
    spiked = v >= params["threshold"]
    state["v"] = params["reset"] if spiked else v
    return spiked


def _adex_state(params: Mapping[str, float]) -> State:
    return {"v": params["v_rest"], "w": 0.0}


def _adex_step(
    state: State, current: float, dt_ms: float, params: Mapping[str, float]
) -> bool:
    v = float(state["v"])
    w = float(state["w"])
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


def _vtrap(x: float, scale: float) -> float:
    if abs(x / scale) < 1e-6:
        return scale * (1.0 - x / (2.0 * scale))
    return x / (math.exp(x / scale) - 1.0)


def _hh_rates(v: float) -> tuple[float, float, float, float, float, float]:
    alpha_m = 0.1 * _vtrap(-(v + 40.0), 10.0)
    beta_m = 4.0 * math.exp(-(v + 65.0) / 18.0)
    alpha_h = 0.07 * math.exp(-(v + 65.0) / 20.0)
    beta_h = 1.0 / (math.exp(-(v + 35.0) / 10.0) + 1.0)
    alpha_n = 0.01 * _vtrap(-(v + 55.0), 10.0)
    beta_n = 0.125 * math.exp(-(v + 65.0) / 80.0)
    return alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n


def _hh_state(params: Mapping[str, float]) -> State:
    v = params["v_rest"]
    am, bm, ah, bh, an, bn = _hh_rates(v)
    return {
        "v": v,
        "m": am / (am + bm),
        "h": ah / (ah + bh),
        "n": an / (an + bn),
        "ca_gate": 0.0,
        "prev_v": v,
    }


def _hh_step(
    state: State, current: float, dt_ms: float, params: Mapping[str, float]
) -> bool:
    v = float(state["v"])
    m = float(state["m"])
    h = float(state["h"])
    n = float(state["n"])
    ca_gate = float(state["ca_gate"])
    start_v = v
    spiked = False
    substeps = max(1, math.ceil(dt_ms / 0.025))
    dt = dt_ms / substeps
    for _ in range(substeps):
        v = min(80.0, max(-120.0, v))
        am, bm, ah, bh, an, bn = _hh_rates(v)
        m += dt * (am * (1.0 - m) - bm * m)
        h += dt * (ah * (1.0 - h) - bh * h)
        n += dt * (an * (1.0 - n) - bn * n)
        m = min(1.0, max(0.0, m))
        h = min(1.0, max(0.0, h))
        n = min(1.0, max(0.0, n))
        ca_gate += (
            dt
            * ((1.0 / (1.0 + math.exp(-(v + 20.0) / 6.5))) - ca_gate)
            / max(params["tau_ca_ms"], 1e-6)
        )
        ca_gate = min(1.0, max(0.0, ca_gate))
        i_na = params["g_na"] * (m**3) * h * (v - params["e_na"])
        i_k = params["g_k"] * (n**4) * (v - params["e_k"])
        i_ca = params["g_ca"] * (ca_gate**2) * (v - params["e_ca"])
        i_l = params["g_l"] * (v - params["e_l"])
        previous = v
        v += dt * (current - i_na - i_k - i_ca - i_l) / params["c_m"]
        if previous < params["threshold"] <= v:
            spiked = True
    state.update(
        {
            "v": v,
            "m": m,
            "h": h,
            "n": n,
            "ca_gate": ca_gate,
            "prev_v": start_v,
        }
    )
    return spiked


def _compartment_state(params: Mapping[str, float]) -> State:
    compartments = max(2, int(params["compartments"]))
    rest = params["v_rest"]
    return {
        "v": rest,
        "soma_v": rest,
        "dendrite_v": [rest for _ in range(compartments - 1)],
    }


def _compartment_step(
    state: State, current: float, dt_ms: float, params: Mapping[str, float]
) -> bool:
    soma = float(state["soma_v"])
    dendrites = [float(value) for value in state["dendrite_v"]]
    old = list(dendrites)
    for index, value in enumerate(old):
        neighbour = soma if index == 0 else old[index - 1]
        coupling = params["coupling"] * (neighbour - value)
        plateau = 0.0
        if params.get("nmda_enabled", 0.0) > 0.5 and value >= params["nmda_threshold"]:
            plateau = params["nmda_gain"]
        local_current = current if index == 0 else current * 0.35
        dendrites[index] = value + (
            (params["v_rest"] - value) + local_current + coupling + plateau
        ) * (dt_ms / params["dendrite_tau_ms"])
    dendritic_drive = sum(params["coupling"] * (value - soma) for value in dendrites)
    soma += ((params["v_rest"] - soma) + current + dendritic_drive) * (
        dt_ms / params["soma_tau_ms"]
    )
    spiked = soma >= params["threshold"]
    if spiked:
        soma = params["reset"]
    state["v"] = soma
    state["soma_v"] = soma
    state["dendrite_v"] = dendrites
    return spiked


def _izh(
    name: str,
    label: str,
    a: float,
    b: float,
    c: float,
    d: float,
    *,
    experimental: bool = False,
) -> NeuronModelSpec:
    return NeuronModelSpec(
        name=name,
        label=label,
        family="Izhikevich",
        parameters={
            "a": a,
            "b": b,
            "c": c,
            "d": d,
            "v0": -65.0,
            "threshold": 30.0,
        },
        compatible_dimensions=None,
        state_factory=_izh_state,
        step=_izh_step,
        experimental=experimental,
    )


NEURON_MODELS: dict[str, NeuronModelSpec] = {
    "izhikevich_rs": _izh(
        "izhikevich_rs", "Izhikevich · Regular Spiking", 0.02, 0.2, -65.0, 8.0
    ),
    "izhikevich_fs": _izh(
        "izhikevich_fs", "Izhikevich · Fast Spiking", 0.1, 0.2, -65.0, 2.0
    ),
    "izhikevich_ib": _izh(
        "izhikevich_ib",
        "Izhikevich · Intrinsically Bursting",
        0.02,
        0.2,
        -55.0,
        4.0,
    ),
    "izhikevich_chattering": _izh(
        "izhikevich_chattering",
        "Izhikevich · Chattering",
        0.02,
        0.2,
        -50.0,
        2.0,
    ),
    "izhikevich_lts": _izh(
        "izhikevich_lts",
        "Izhikevich · Low Threshold Spiking",
        0.02,
        0.25,
        -65.0,
        2.0,
    ),
    "izhikevich_resonator": _izh(
        "izhikevich_resonator",
        "Izhikevich · Resonator",
        0.1,
        0.26,
        -65.0,
        2.0,
    ),
    "izhikevich_sensory": _izh(
        "izhikevich_sensory",
        "Izhikevich · Sensory",
        0.02,
        0.2,
        -65.0,
        8.0,
    ),
    "izhikevich_motor": _izh(
        "izhikevich_motor",
        "Izhikevich · Motor",
        0.02,
        0.2,
        -65.0,
        8.0,
    ),
    "lif": NeuronModelSpec(
        "lif",
        "Leaky Integrate-and-Fire",
        "Point neuron",
        {
            "v_rest": -65.0,
            "threshold": -50.0,
            "reset": -65.0,
            "tau_m_ms": 20.0,
            "resistance": 1.0,
        },
        None,
        _lif_state,
        _lif_step,
    ),
    "adex": NeuronModelSpec(
        "adex",
        "Adaptive Exponential",
        "Point neuron",
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
        },
        None,
        _adex_state,
        _adex_step,
        experimental=True,
    ),
    "pan_adex_5d": NeuronModelSpec(
        "pan_adex_5d",
        "PAN · AdEx + hyperstate",
        "PAN exploratory",
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
        },
        None,
        _adex_state,
        _adex_step,
        experimental=True,
        note=(
            "AdEx membrane dynamics plus Playground PAN health/hyperstate layer. "
            "Exploratory only; no scientific evidence claim."
        ),
    ),
    "hodgkin_huxley_na_k_ca": NeuronModelSpec(
        "hodgkin_huxley_na_k_ca",
        "Hodgkin-Huxley · Na/K/Ca",
        "Conductance-based",
        {
            "v_rest": -65.0,
            "c_m": 1.0,
            "g_na": 120.0,
            "g_k": 36.0,
            "g_ca": 0.4,
            "g_l": 0.3,
            "e_na": 50.0,
            "e_k": -77.0,
            "e_ca": 120.0,
            "e_l": -54.387,
            "tau_ca_ms": 5.0,
            "threshold": 0.0,
        },
        None,
        _hh_state,
        _hh_step,
        experimental=True,
        note="Exploratory Na/K/Ca conductance model; no 5D advantage claim.",
    ),
    "multi_compartment_linear": NeuronModelSpec(
        "multi_compartment_linear",
        "Multi-compartment · linear dendrites",
        "Multi-compartment",
        {
            "compartments": 3.0,
            "v_rest": -65.0,
            "threshold": -50.0,
            "reset": -65.0,
            "soma_tau_ms": 20.0,
            "dendrite_tau_ms": 40.0,
            "coupling": 0.08,
            "nmda_enabled": 0.0,
            "nmda_threshold": -35.0,
            "nmda_gain": 4.0,
        },
        None,
        _compartment_state,
        _compartment_step,
        experimental=True,
    ),
    "multi_compartment_nmda": NeuronModelSpec(
        "multi_compartment_nmda",
        "Multi-compartment · NMDA plateau",
        "Multi-compartment",
        {
            "compartments": 3.0,
            "v_rest": -65.0,
            "threshold": -50.0,
            "reset": -65.0,
            "soma_tau_ms": 20.0,
            "dendrite_tau_ms": 40.0,
            "coupling": 0.08,
            "nmda_enabled": 1.0,
            "nmda_threshold": -35.0,
            "nmda_gain": 4.0,
        },
        None,
        _compartment_state,
        _compartment_step,
        experimental=True,
        note="NMDA plateau is an exploratory building block, not a validation claim.",
    ),
}


def get_neuron_model(name: str) -> NeuronModelSpec:
    try:
        return NEURON_MODELS[name]
    except KeyError as exc:
        raise ValueError(f"unknown playground neuron model: {name}") from exc
