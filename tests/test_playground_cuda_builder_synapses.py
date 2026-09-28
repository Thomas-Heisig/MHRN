"""Builder CUDA emission preserves inhibitory algebra, STP and RNG consumption."""

from __future__ import annotations

import math
import os
from copy import deepcopy

import pytest

from src.playground.builder.session import PlaygroundSession
from src.playground.cuda.builder_parity import compare_builder_runs
from src.playground.cuda.membrane import cuda_membrane_session
from src.playground.models import PlaygroundConfig
from src.playground.pan.runtime import PANRuntime
from src.playground.registry.neuron_models import get_neuron_model


def test_d3_rejects_stp_rng_and_pending_event_drift():
    cpu = PlaygroundSession(
        PlaygroundConfig.from_mapping(
            {
                "closed_loop_preset": "pan_full_balanced",
                "n_neurons": 32,
                "edge_budget": 64,
                "ticks": 128,
                "persist": False,
            }
        ),
        capture_research_state=True,
    ).run()
    for field in ("release_resources", "eligibility", "pending_currents", "rng_state"):
        gpu = deepcopy(cpu)
        gpu["execution"].update(
            neuron_backend="cuda_pan", gpu_membrane_ticks=128, gpu_pan_ticks=128
        )
        if field == "rng_state":
            gpu["research_state"][field] = (0, (), None)
        elif field == "pending_currents":
            gpu["research_state"][field][0][0] += 0.1
        else:
            gpu["research_state"][field][0] += 0.1
        assert not compare_builder_runs(cpu, gpu)["passed"], field


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
@pytest.mark.parametrize("stp", [False, True])
def test_emission_inhibition_recovery_and_frozen_amplitude(stp, tmp_path, monkeypatch):
    monkeypatch.setenv("TMP", str(tmp_path))
    pan = PANRuntime(
        n_neurons=17,
        dimensions=5,
        seed=42,
        feedback_gain=0.1,
        health_decay=0.001,
        apoptosis_threshold=0.1,
        closed_loop=True,
        coordinates=[[0.0]] * 17,
        degree=[1] * 17,
    )
    model = get_neuron_model("pan_adex_5d")
    rows = [
        (
            float(i % 11),
            (i % 10) / 10,
            0.2 + 0.8 * ((i % 8) / 8),
            (i * 37 % 100) / 100,
            float(i % 2),
        )
        for i in range(129)
    ]
    threshold = min(0.95, 0.25 + 0.7 * 0.4)
    rows[:2] = [
        (2.0, 0.4, 1.0, threshold, 0.0),
        (2.0, 0.4, 1.0, math.nextafter(threshold, 0.0), 1.0),
    ]
    expected = []
    for weight, available, amplitude, draw, inhibitory in rows:
        value = weight
        if inhibitory:
            value = -abs(value) * 1.3 / 0.25
        value *= amplitude
        if stp:
            value *= 1.0 if draw < min(0.95, 0.25 + 0.7 * available) else 0.0
            available = max(0.1, available * 0.72)
        expected.append((value, available))
    with cuda_membrane_session(
        model.name, [model.parameters] * 17, 1.0, pan_runtime=pan
    ) as stepper:
        actual = stepper.synapses.emit(rows, stp=stp, gaba=1.3, ratio=0.25)
        assert actual == expected
        recovered = stepper.synapses.recover(
            [r[0] for r in rows],
            [r[1] for r in actual],
            stp=stp,
            decay=0.01,
            maximum=5.0,
        )
        assert recovered == [
            (min(5.0, max(0.0, r[0] * 0.99)), min(1.0, a[1] + 0.025) if stp else a[1])
            for r, a in zip(rows, actual)
        ]
        assert actual == expected
        for reward in (-1.0, 0.0, 1.0):
            for respect in (False, True):
                weights, eligibility, ages = (
                    [2.0, 50.0, 19.99],
                    [1.0, -2.0, 3.0],
                    [64, 65, 0],
                )
                result = stepper.synapses.reward(
                    weights,
                    eligibility,
                    ages,
                    scale=0.2,
                    reward=reward,
                    maximum=20.0,
                    window=64,
                    respect_window=respect,
                )
                assert result == [
                    (
                        w
                        if respect and age > 64
                        else min(20.0, max(0.0, w + 0.2 * e * reward))
                    )
                    for w, e, age in zip(weights, eligibility, ages)
                ]
        with pytest.raises(ValueError):
            stepper.synapses.reward(
                [1.0],
                [1.0],
                [0],
                scale=0.2,
                reward=float("nan"),
                maximum=20.0,
                window=64,
                respect_window=True,
            )
        with pytest.raises(ValueError):
            stepper.synapses.emit(
                [(1.0, 1.0, 1.0, 1.0, 0.0)], stp=True, gaba=1.0, ratio=1.0
            )
        with pytest.raises(ValueError):
            stepper.synapses.emit(
                [(float("nan"), 1.0, 1.0, 0.0, 0.0)], stp=True, gaba=1.0, ratio=1.0
            )
        with pytest.raises(ValueError):
            stepper.synapses.recover([1.0], [], stp=True, decay=0.0, maximum=5.0)


def test_cuda_preset_inherits_pan_with_explicit_backend():
    cpu = PlaygroundConfig.from_mapping({"closed_loop_preset": "pan_full_balanced"})
    gpu = PlaygroundConfig.from_mapping({"closed_loop_preset": "pan_cuda_hybrid"})
    assert cpu.neuron_backend == "cpu"
    assert gpu.neuron_backend == "cuda_pan"
    assert gpu.sandbox_enabled and gpu.neural_io_enabled and gpu.growth_enabled
    assert (cpu.n_neurons, cpu.edge_budget, cpu.weight) == (
        gpu.n_neurons,
        gpu.edge_budget,
        gpu.weight,
    )
