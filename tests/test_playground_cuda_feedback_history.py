"""Resident feedback history obeys the CPU retention window and source transforms."""

from __future__ import annotations

import math
import os
from copy import deepcopy

import pytest

from src.playground.cuda.builder_parity import run_builder_parity
from src.playground.cuda.membrane import cuda_membrane_session
from src.playground.cuda.pan_state import PANStateStepper
from src.playground.cuda.runtime import DeviceAllocation
from src.playground.pan.runtime import PANRuntime
from src.playground.registry.neuron_models import get_neuron_model


def runtime():
    return PANRuntime(
        n_neurons=3,
        dimensions=32,
        seed=42,
        feedback_gain=0.5,
        health_decay=0.0,
        apoptosis_threshold=0.1,
        closed_loop=True,
        coordinates=[[0.0]] * 3,
        degree=[1] * 3,
        feedback_delay=64,
    )


@pytest.mark.parametrize("bad", ["shape", "finite", "delay"])
def test_invalid_initial_feedback_never_transfers_and_cleans(bad):
    class Driver:
        def __init__(self):
            self.allocated, self.freed = [], []

        def kernel(self, loaded, name):
            return loaded

        def alloc_device(self, size):
            value = DeviceAllocation(len(self.allocated) + 1, size)
            self.allocated.append(value)
            return value

        def free_device(self, value):
            self.freed.append(value)

        def copy_host_to_device(self, *args):
            raise AssertionError("invalid feedback reached transfer")

    pan = runtime()
    if bad == "shape":
        pan.feedback_history = [[0.0]]
    elif bad == "finite":
        pan.population_vector[0] = float("nan")
    else:
        pan.feedback_delay = True
    driver = Driver()
    with pytest.raises(ValueError, match=bad):
        PANStateStepper(driver, object(), pan)
    assert driver.freed == list(reversed(driver.allocated))


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
def test_feedback_ring_wrap_retention_and_external_edits(tmp_path, monkeypatch):
    monkeypatch.setenv("TMP", str(tmp_path))
    cpu, gpu = runtime(), runtime()
    states = [{"v": -65.0} for _ in range(3)]
    cpu.initialize(states)
    for state in states:
        state["pan_alive"] = False
    other = deepcopy(states)
    model = get_neuron_model("pan_adex_5d")
    with cuda_membrane_session(
        model.name, [model.parameters] * 3, 1.0, pan_runtime=gpu
    ) as stepper:
        copies = []
        original_copy = stepper.driver.copy_host_to_device
        population = stepper.pan.reduction_device["population"].ptr
        history = stepper.pan.reduction_device["history"].ptr

        def record_copy(allocation, values, **kwargs):
            if allocation.ptr in (population, history):
                copies.append(allocation.ptr)
            return original_copy(allocation, values, **kwargs)

        monkeypatch.setattr(stepper.driver, "copy_host_to_device", record_copy)
        for tick in range(155):
            for pan in (cpu, gpu):
                pan.feedback_delay = 0 if 80 <= tick < 85 else 64
                pan.feedback_source = ("population", "layer", "subset", "hypervector")[
                    tick % 4
                ]
            expected = cpu.feedback_currents()
            assert stepper.pan.feedback_currents() == pytest.approx(
                expected, abs=1e-12, rel=0
            )
            if tick < 65 or 85 <= tick < 148:
                assert expected == [0.0] * 3
            for neuron, (a, b) in enumerate(zip(states, other)):
                values = [math.sin(tick * 0.1 + d + neuron) for d in range(32)]
                a["pan_x_hd"], b["pan_x_hd"] = list(values), list(values)
            options = dict(
                tick=tick, dt_ms=1.0, spiked_neurons=[], plasticity_active=False
            )
            cpu.update(states=states, **options)
            stepper.pan.update(states=other, **options)
            assert cpu.population_vector == gpu.population_vector
            assert cpu.feedback_history == gpu.feedback_history
        assert stepper.pan.source_calls == 155
        assert copies == []

        for pan in (cpu, gpu):
            pan.feedback_delay = 0
            pan.population_vector[0] += 0.2
            pan.feedback_history[-1][0] += 0.3
        assert stepper.pan.feedback_currents() == pytest.approx(
            cpu.feedback_currents(), abs=1e-12, rel=0
        )
        assert copies == [population, history]
        before = list(copies)
        for delay in (True, -1, 65, 0.5):
            gpu.feedback_delay = delay
            with pytest.raises(ValueError, match="delay"):
                stepper.pan.feedback_currents()
        gpu.feedback_delay = 0
        gpu.feedback_history[-1].pop()
        with pytest.raises(ValueError, match="shape"):
            stepper.pan.feedback_currents()
        gpu.feedback_history[-1].append(float("nan"))
        with pytest.raises(ValueError, match="finite"):
            stepper.pan.feedback_currents()
        assert copies == before


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
def test_builder_delayed_hypervector_feedback(tmp_path, monkeypatch):
    monkeypatch.setenv("TMP", str(tmp_path))
    result = run_builder_parity(
        {
            "closed_loop_preset": "pan_cuda_hybrid",
            "n_neurons": 32,
            "edge_budget": 64,
            "ticks": 256,
            "pan_feedback_delay": 64,
            "pan_feedback_source": "hypervector",
        }
    )
    assert result["passed"], result
    assert result["gpu_pan_source_calls"] == 256
