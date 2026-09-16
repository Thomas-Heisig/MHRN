"""Stage-0 model conformance v2: local transition equivalence and LIF refractory mapping.

The v1 long free-running Izhikevich trajectory is retained as a scientific
negative. V2 tests the actual membrane transition contract without allowing
sub-nanoscopic floating-point differences to amplify chaotically across hundreds
of recurrent state updates. Free-running spike robustness remains a distinct
secondary outcome.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

from src.core.neuron import NeuronConfig, NeuronModel, create_neuron
from src.core.neuron_models import apply_spike_reset, integrate_membrane

OUT = Path("stage0-conformance-v2.json")
SEEDS = (20001, 20002, 20003)


def _native_transition(
    v: float, u: float, current: float
) -> tuple[float, float, bool, float, float]:
    cfg = NeuronConfig.isolated_reference(model=NeuronModel.IZHIKEVICH)
    nv, nu = integrate_membrane(
        NeuronModel.IZHIKEVICH,
        v=v,
        u=u,
        input_current=current,
        dt_ms=cfg.dt_ms,
        a=cfg.a,
        b=cfg.b,
        lif_resting_potential=cfg.lif_resting_potential,
        lif_tau_m_ms=cfg.lif_tau_m_ms,
        lif_resistance=cfg.lif_resistance,
    )
    spiked = nv >= cfg.izhikevich_threshold
    pv, pu = (
        apply_spike_reset(
            NeuronModel.IZHIKEVICH,
            v=nv,
            u=nu,
            c=cfg.c,
            d=cfg.d,
            lif_reset=cfg.lif_reset,
        )
        if spiked
        else (nv, nu)
    )
    return nv, nu, spiked, pv, pu


def _brian_transition(
    v: float, u: float, current: float
) -> tuple[float, float, bool, float, float]:
    import brian2 as brian

    brian.start_scope()
    brian.prefs.codegen.target = "numpy"
    group = brian.NeuronGroup(
        1,
        "v : 1\nu : 1\nI : 1",
        threshold="v >= 30",
        reset="v = -65; u += 8",
        dt=brian.ms,
    )
    group.v = v
    group.u = u
    group.I = current
    update = group.run_regularly(
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
    net = brian.Network(group, update, pre, post, spikes)
    net.run(1 * brian.ms)
    return (
        float(pre.v[0][-1]),
        float(pre.u[0][-1]),
        len(spikes.i) == 1,
        float(post.v[0][-1]),
        float(post.u[0][-1]),
    )


def _sample_states(seed: int, count: int = 64) -> list[tuple[float, float, float]]:
    rng = random.Random(seed)
    states: list[tuple[float, float, float]] = [
        (-65.0, -13.0, 0.0),
        (-65.0, -13.0, 10.0),
        (-65.0, -13.0, 50.0),
        (-40.0, -10.0, 20.0),
        (25.0, -5.0, 20.0),
        (29.9, -5.0, 20.0),
    ]
    while len(states) < count:
        states.append(
            (rng.uniform(-80, 29.9), rng.uniform(-25, 20), rng.uniform(-10, 80))
        )
    return states


def _izh_local(seed: int) -> dict[str, Any]:
    max_pre_v = max_pre_u = max_post_v = max_post_u = 0.0
    spike_equal = True
    first_failure = None
    for index, (v, u, current) in enumerate(_sample_states(seed)):
        native = _native_transition(v, u, current)
        brian = _brian_transition(v, u, current)
        errors = (
            abs(native[0] - brian[0]),
            abs(native[1] - brian[1]),
            abs(native[3] - brian[3]),
            abs(native[4] - brian[4]),
        )
        max_pre_v = max(max_pre_v, errors[0])
        max_pre_u = max(max_pre_u, errors[1])
        max_post_v = max(max_post_v, errors[2])
        max_post_u = max(max_post_u, errors[3])
        equal = native[2] == brian[2]
        spike_equal = spike_equal and equal
        if first_failure is None and (max(errors) > 1e-8 or not equal):
            first_failure = {
                "sample": index,
                "initial": {"v": v, "u": u, "current": current},
                "native": native,
                "brian2": brian,
                "errors": errors,
            }
    return {
        "seed": seed,
        "samples": len(_sample_states(seed)),
        "max_abs_pre_reset_v_error": max_pre_v,
        "max_abs_pre_reset_u_error": max_pre_u,
        "max_abs_post_reset_v_error": max_post_v,
        "max_abs_post_reset_u_error": max_post_u,
        "spike_decisions_equal": spike_equal,
        "conformance_within_1e_8": spike_equal
        and max(max_pre_v, max_pre_u, max_post_v, max_post_u) <= 1e-8,
        "first_failure": first_failure,
    }


def _lif_native(
    currents: list[list[float]], refractory_ticks: int
) -> tuple[list[list[float]], list[tuple[int, int]]]:
    cfg = NeuronConfig.isolated_reference(
        model=NeuronModel.LEAKY_INTEGRATE_AND_FIRE, refractory_ticks=refractory_ticks
    )
    cells = [create_neuron(i, config=cfg) for i in range(5)]
    states: list[list[float]] = []
    spikes: list[tuple[int, int]] = []
    for tick, row in enumerate(currents):
        for i, (cell, current) in enumerate(zip(cells, row)):
            if cell.step(current, tick):
                spikes.append((tick, i))
        states.append([cell.v for cell in cells])
    return states, spikes


def _lif_brian(
    currents: list[list[float]], refractory_ms: int
) -> tuple[list[list[float]], list[tuple[int, int]]]:
    import brian2 as brian
    import numpy as np

    brian.start_scope()
    brian.prefs.codegen.target = "numpy"
    stimulus = brian.TimedArray(np.asarray(currents), dt=brian.ms)
    kwargs: dict[str, Any] = {}
    equation = "dv/dt = ((-65 - v) + stimulus(t, i)) / (20*ms) : 1"
    if refractory_ms > 0:
        equation += " (unless refractory)"
        kwargs["refractory"] = refractory_ms * brian.ms
    group = brian.NeuronGroup(
        5,
        equation,
        threshold="v >= -50",
        reset="v = -65",
        method="euler",
        dt=brian.ms,
        namespace={"stimulus": stimulus},
        **kwargs,
    )
    group.v = -65
    states = brian.StateMonitor(group, "v", record=True, when="end")
    spikes = brian.SpikeMonitor(group)
    net = brian.Network(group, states, spikes)
    net.run(len(currents) * brian.ms)
    return states.v.T.tolist(), [
        (int(round(float(t / brian.ms))), int(i)) for t, i in zip(spikes.t, spikes.i)
    ]


def _max_abs(left: list[list[float]], right: list[list[float]]) -> float:
    return max(abs(a - b) for x, y in zip(left, right) for a, b in zip(x, y))


def _lif_mapping(seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    currents = [
        [2.0, 5.0, 10.0, 20.0, rng.choice((0.0, 10.0, 50.0))] for _ in range(1000)
    ]
    out: list[dict[str, Any]] = []
    for native_ticks in (0, 1, 2, 3):
        nv, ns = _lif_native(currents, native_ticks)
        for brian_ms in range(0, 6):
            bv, bs = _lif_brian(currents, brian_ms)
            out.append(
                {
                    "seed": seed,
                    "native_refractory_ticks": native_ticks,
                    "brian2_refractory_ms": brian_ms,
                    "spike_events_equal": ns == bs,
                    "max_abs_v_error": _max_abs(nv, bv),
                    "native_spike_count": len(ns),
                    "brian2_spike_count": len(bs),
                }
            )
    return out


def main() -> None:
    izh = [_izh_local(seed) for seed in SEEDS]
    lif = [row for seed in SEEDS for row in _lif_mapping(seed)]
    exact_mappings = [
        row
        for row in lif
        if row["spike_events_equal"] and row["max_abs_v_error"] <= 1e-8
    ]
    payload = {
        "status": "diagnostic_only_not_evidence",
        "protocol_candidate": "single_neuron_conformance_v2",
        "izhikevich_local_transition": izh,
        "izhikevich_all_seeds_pass": all(row["conformance_within_1e_8"] for row in izh),
        "lif_refractory_mapping_sweep": lif,
        "lif_exact_mappings": exact_mappings,
        "interpretation": {
            "v1_long_trajectory": "retained negative; free-running nonlinear divergence is not used as a local transition-equivalence test",
            "v2_primary": "one-step pre/post-reset state and spike-decision equivalence",
            "lif_primary_default": "refractory_ticks=0 is part of the canonical alternative-model conformance; nonzero refractory is an optional extension with separately mapped semantics",
        },
    }
    OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(OUT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
