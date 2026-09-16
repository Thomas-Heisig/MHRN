"""Diagnose Stage-0 reference-conformance phase semantics for Izhikevich and LIF.

This is exploratory DATA only. It explicitly records both the state immediately
before reset and the state after reset, so a scheduler-phase mismatch cannot be
mistaken for a membrane-model error. It also characterizes the optional LIF
refractory extension without changing its semantics.
"""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

from src.core.neuron import NeuronConfig, NeuronModel, create_neuron
from src.core.neuron_models import integrate_membrane

OUT = Path("stage0-phase-model-diagnostic.json")
SEEDS = (20001, 20002, 20003)
TICKS = 1000
CELLS = 5


def _currents(seed: int) -> list[list[float]]:
    rng = random.Random(seed)
    return [
        [2.0, 5.0, 10.0, 20.0, rng.choice((0.0, 10.0, 50.0))]
        for _ in range(TICKS)
    ]


def _max_abs(left: list[list[float]], right: list[list[float]]) -> float:
    return max(
        abs(a - b)
        for left_row, right_row in zip(left, right)
        for a, b in zip(left_row, right_row)
    )


def _first_state_mismatch(
    left: list[list[float]], right: list[list[float]], tolerance: float = 1e-10
) -> dict[str, Any] | None:
    for tick, (left_row, right_row) in enumerate(zip(left, right)):
        for cell, (a, b) in enumerate(zip(left_row, right_row)):
            if abs(a - b) > tolerance:
                return {
                    "tick": tick,
                    "cell": cell,
                    "native": a,
                    "brian2": b,
                    "abs_error": abs(a - b),
                }
    return None


def _first_spike_mismatch(
    native: list[tuple[int, int]], brian2_spikes: list[tuple[int, int]]
) -> dict[str, Any] | None:
    limit = max(len(native), len(brian2_spikes))
    for index in range(limit):
        a = native[index] if index < len(native) else None
        b = brian2_spikes[index] if index < len(brian2_spikes) else None
        if a != b:
            return {"index": index, "native": a, "brian2": b}
    return None


def _native_izh(currents: list[list[float]]) -> dict[str, Any]:
    config = NeuronConfig.isolated_reference(model=NeuronModel.IZHIKEVICH)
    neurons = [create_neuron(i, config=config) for i in range(CELLS)]
    pre_v: list[list[float]] = []
    pre_u: list[list[float]] = []
    post_v: list[list[float]] = []
    post_u: list[list[float]] = []
    spikes: list[tuple[int, int]] = []
    for tick, row in enumerate(currents):
        tick_pre_v: list[float] = []
        tick_pre_u: list[float] = []
        for neuron, current in zip(neurons, row):
            v, u = integrate_membrane(
                NeuronModel.IZHIKEVICH,
                v=neuron.v,
                u=neuron.u,
                input_current=current,
                dt_ms=config.dt_ms,
                a=neuron.a,
                b=neuron.b,
                lif_resting_potential=config.lif_resting_potential,
                lif_tau_m_ms=config.lif_tau_m_ms,
                lif_resistance=config.lif_resistance,
            )
            tick_pre_v.append(v)
            tick_pre_u.append(u)
        pre_v.append(tick_pre_v)
        pre_u.append(tick_pre_u)
        for index, (neuron, current) in enumerate(zip(neurons, row)):
            if neuron.step(current, tick + 1):
                spikes.append((tick, index))
        post_v.append([neuron.v for neuron in neurons])
        post_u.append([neuron.u for neuron in neurons])
    return {
        "pre_v": pre_v,
        "pre_u": pre_u,
        "post_v": post_v,
        "post_u": post_u,
        "spikes": spikes,
    }


def _brian2_izh(currents: list[list[float]]) -> dict[str, Any]:
    import brian2 as brian
    import numpy as np

    brian.start_scope()
    brian.prefs.codegen.target = "numpy"
    stimulus = brian.TimedArray(np.asarray(currents), dt=brian.ms)
    group = brian.NeuronGroup(
        CELLS,
        "v : 1\nu : 1\nI : 1",
        threshold="v >= 30",
        reset="v = -65; u += 8",
        dt=brian.ms,
        namespace={"stimulus": stimulus},
    )
    group.v = -65
    group.u = -13
    update = group.run_regularly(
        "I = stimulus(t, i)\n"
        "v += 0.5*(0.04*v*v + 5*v + 140 - u + I)\n"
        "v += 0.5*(0.04*v*v + 5*v + 140 - u + I)\n"
        "u += 0.02*(0.2*v - u)",
        dt=brian.ms,
        when="groups",
        order=0,
    )
    pre = brian.StateMonitor(group, ("v", "u"), record=True, when="thresholds", order=1)
    post = brian.StateMonitor(group, ("v", "u"), record=True, when="end")
    spikes = brian.SpikeMonitor(group)
    network = brian.Network(group, update, pre, post, spikes)
    network.run(TICKS * brian.ms)
    return {
        "pre_v": pre.v.T.tolist(),
        "pre_u": pre.u.T.tolist(),
        "post_v": post.v.T.tolist(),
        "post_u": post.u.T.tolist(),
        "spikes": [
            (int(round(float(t / brian.ms))), int(i)) for t, i in zip(spikes.t, spikes.i)
        ],
        "version": str(brian.__version__),
    }


def _native_lif(currents: list[list[float]], refractory_ticks: int) -> dict[str, Any]:
    config = NeuronConfig.isolated_reference(
        model=NeuronModel.LEAKY_INTEGRATE_AND_FIRE,
        refractory_ticks=refractory_ticks,
    )
    neurons = [create_neuron(i, config=config) for i in range(CELLS)]
    post_v: list[list[float]] = []
    spikes: list[tuple[int, int]] = []
    for tick, row in enumerate(currents):
        for index, (neuron, current) in enumerate(zip(neurons, row)):
            if neuron.step(current, tick):
                spikes.append((tick, index))
        post_v.append([neuron.v for neuron in neurons])
    return {"post_v": post_v, "spikes": spikes}


def _brian2_lif(currents: list[list[float]], refractory_ticks: int) -> dict[str, Any]:
    import brian2 as brian
    import numpy as np

    brian.start_scope()
    brian.prefs.codegen.target = "numpy"
    stimulus = brian.TimedArray(np.asarray(currents), dt=brian.ms)
    refractory = refractory_ticks * brian.ms if refractory_ticks else False
    group = brian.NeuronGroup(
        CELLS,
        "dv/dt = ((-65 - v) + stimulus(t, i)) / (20*ms) : 1 (unless refractory)",
        threshold="v >= -50",
        reset="v = -65",
        refractory=refractory,
        method="euler",
        dt=brian.ms,
        namespace={"stimulus": stimulus},
    )
    group.v = -65
    states = brian.StateMonitor(group, "v", record=True, when="end")
    spikes = brian.SpikeMonitor(group)
    network = brian.Network(group, states, spikes)
    network.run(TICKS * brian.ms)
    return {
        "post_v": states.v.T.tolist(),
        "spikes": [
            (int(round(float(t / brian.ms))), int(i)) for t, i in zip(spikes.t, spikes.i)
        ],
        "version": str(brian.__version__),
    }


def main() -> None:
    izh_runs: list[dict[str, Any]] = []
    lif_runs: list[dict[str, Any]] = []
    for seed in SEEDS:
        currents = _currents(seed)
        native = _native_izh(currents)
        brian = _brian2_izh(currents)
        izh_runs.append(
            {
                "seed": seed,
                "brian2_version": brian["version"],
                "pre_reset": {
                    "max_abs_v_error": _max_abs(native["pre_v"], brian["pre_v"]),
                    "max_abs_u_error": _max_abs(native["pre_u"], brian["pre_u"]),
                    "first_v_mismatch_gt_1e_10": _first_state_mismatch(native["pre_v"], brian["pre_v"]),
                    "first_u_mismatch_gt_1e_10": _first_state_mismatch(native["pre_u"], brian["pre_u"]),
                },
                "post_reset": {
                    "max_abs_v_error": _max_abs(native["post_v"], brian["post_v"]),
                    "max_abs_u_error": _max_abs(native["post_u"], brian["post_u"]),
                    "first_v_mismatch_gt_1e_10": _first_state_mismatch(native["post_v"], brian["post_v"]),
                    "first_u_mismatch_gt_1e_10": _first_state_mismatch(native["post_u"], brian["post_u"]),
                },
                "spike_events_equal": native["spikes"] == brian["spikes"],
                "first_spike_mismatch": _first_spike_mismatch(native["spikes"], brian["spikes"]),
                "native_spike_count": len(native["spikes"]),
                "brian2_spike_count": len(brian["spikes"]),
            }
        )
        for refractory_ticks in (0, 1, 2, 3):
            native_lif = _native_lif(currents, refractory_ticks)
            brian_lif = _brian2_lif(currents, refractory_ticks)
            lif_runs.append(
                {
                    "seed": seed,
                    "refractory_ticks": refractory_ticks,
                    "brian2_refractory_ms": float(refractory_ticks),
                    "max_abs_v_error": _max_abs(native_lif["post_v"], brian_lif["post_v"]),
                    "first_v_mismatch_gt_1e_10": _first_state_mismatch(native_lif["post_v"], brian_lif["post_v"]),
                    "spike_events_equal": native_lif["spikes"] == brian_lif["spikes"],
                    "first_spike_mismatch": _first_spike_mismatch(native_lif["spikes"], brian_lif["spikes"]),
                    "native_spike_count": len(native_lif["spikes"]),
                    "brian2_spike_count": len(brian_lif["spikes"]),
                }
            )
    payload = {
        "status": "diagnostic_only_not_evidence",
        "purpose": "resolve compare phase and model/refractory semantics before freezing v2",
        "compare_phases": ["pre_reset", "post_reset"],
        "izhikevich": izh_runs,
        "lif": lif_runs,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
