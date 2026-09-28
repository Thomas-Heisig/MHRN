"""PAN GPU state parity and lifecycle/resource failures."""

from __future__ import annotations

import ctypes
import os
from copy import deepcopy

import pytest

from src.playground.cuda import membrane
from src.playground.cuda.builder_parity import run_builder_parity
from src.playground.cuda.pan_state import STATE_FIELDS
from src.playground.cuda.runtime import CudaDriverError, DeviceAllocation, DriverModule
from src.playground.models import PlaygroundConfig
from src.playground.pan.runtime import PANRuntime
from src.playground.registry.neuron_models import get_neuron_model


def runtime(n=129, dimensions=10, decay=0.0, threshold=0.2):
    return PANRuntime(
        n_neurons=n,
        dimensions=dimensions,
        seed=42,
        feedback_gain=1.0,
        health_decay=decay,
        apoptosis_threshold=threshold,
        closed_loop=True,
        coordinates=[[i / n, 0.5] for i in range(n)],
        degree=[i % 8 for i in range(n)],
    )


def test_cuda_pan_rejects_non_pan_models():
    with pytest.raises(ValueError, match="requires pan_adex_5d"):
        PlaygroundConfig.from_mapping(
            {"neuron_backend": "cuda_pan", "neuron_model": "lif"}
        )


@pytest.mark.parametrize(
    "failure", ["allocation", "copy", "launch", "synchronize", "nonfinite"]
)
def test_pan_shared_context_cleanup_and_validation(monkeypatch, failure, tmp_path):
    class Driver:
        def __init__(self):
            self.allocated = []
            self.freed = []
            self.unloads = 0

        def load_cubin(self, *a, **kw):
            return DriverModule(
                ctypes.c_void_p(1), ctypes.c_void_p(2), ctypes.c_void_p(3), 0
            )

        def kernel(self, loaded, name):
            return loaded

        def alloc_device(self, size):
            if failure == "allocation" and len(self.allocated) == 8:
                raise CudaDriverError("allocation")
            x = DeviceAllocation(len(self.allocated) + 1, size)
            self.allocated.append(x)
            return x

        def free_device(self, x):
            self.freed.append(x)

        def unload(self, x):
            self.unloads += 1

        def copy_host_to_device(self, *a):
            if failure == "copy" and len(self.allocated) > 6:
                raise CudaDriverError("copy")

        def launch_kernel(self, *a, **kw):
            if failure == "launch":
                raise CudaDriverError("launch")

        def synchronize(self):
            raise CudaDriverError("synchronize")

    driver = Driver()
    monkeypatch.setattr(membrane, "CudaDriver", lambda: driver)
    monkeypatch.setattr(membrane, "compile_cuda_source", lambda *a, **kw: "ptx")
    monkeypatch.setenv("TMP", str(tmp_path))
    pan = runtime(2)
    states = [{"v": -65.0} for _ in range(2)]
    pan.initialize(states)
    if failure == "nonfinite":
        states[0]["pan_energy"] = float("nan")
    model = get_neuron_model("pan_adex_5d")
    with pytest.raises((ValueError, CudaDriverError)):
        with membrane.cuda_membrane_session(
            model.name, [model.parameters] * 2, 1.0, pan_runtime=pan
        ) as stepper:
            stepper.pan.update(
                tick=0,
                dt_ms=1.0,
                states=states,
                spiked_neurons=[0],
                plasticity_active=True,
            )
    assert driver.unloads == 1
    assert driver.freed == list(reversed(driver.allocated))


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
@pytest.mark.parametrize("dimensions,decay", [(5, 0.0), (10, 80.0), (32, 0.0)])
def test_pan_gpu_state_and_apoptosis_match_cpu(
    dimensions, decay, tmp_path, monkeypatch
):
    monkeypatch.setenv("TMP", str(tmp_path))
    cpu = runtime(dimensions=dimensions, decay=decay)
    gpu = runtime(dimensions=dimensions, decay=decay)
    a = [{"v": -65.0 + (i % 20), "pan_threshold": -50.0} for i in range(cpu.n_neurons)]
    cpu.initialize(a)
    b = deepcopy(a)
    model = get_neuron_model("pan_adex_5d")
    with membrane.cuda_membrane_session(
        model.name, [model.parameters] * cpu.n_neurons, 1.0, pan_runtime=gpu
    ) as stepper:
        for tick in range(130):
            spikes = [i for i in range(cpu.n_neurons) if (i + tick) % 7 == 0]
            options = {
                "tick": tick,
                "dt_ms": 1.0,
                "spiked_neurons": spikes,
                "plasticity_active": tick % 2 == 0,
            }
            cpu.update(states=a, **options)
            stepper.pan.update(states=b, **options)
            for x, y in zip(a, b):
                assert x["pan_alive"] == y["pan_alive"]
                assert [x[k] for k in STATE_FIELDS] == pytest.approx(
                    [y[k] for k in STATE_FIELDS], abs=1e-12, rel=0
                )
                assert x["pan_x_hd"] == pytest.approx(y["pan_x_hd"], abs=1e-12, rel=0)
            assert cpu.population_vector == pytest.approx(
                gpu.population_vector, abs=1e-12, rel=0
            )
    assert [(e["tick"], e["neuron_id"]) for e in cpu.apoptosis_events] == [
        (e["tick"], e["neuron_id"]) for e in gpu.apoptosis_events
    ]
    assert bool(cpu.apoptosis_events) == bool(decay)


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
@pytest.mark.parametrize("seed", [12345, 42, 777])
def test_pan_state_real_builder_d3(seed, tmp_path, monkeypatch):
    monkeypatch.setenv("TMP", str(tmp_path))
    result = run_builder_parity(
        {
            "closed_loop_preset": "pan_full_balanced",
            "neuron_backend": "cuda_pan",
            "seed": seed,
        }
    )
    assert result["passed"], result
    assert result["D2_full_pan_state_max_error"] <= 1e-12
    assert result["D2_full_synaptic_weight_max_error"] <= 1e-12
    assert result["D3_full_body_trajectory_exact"]
    assert result["RNG_builder_state_exact"]
    assert result["D2_STP_eligibility_max_error"] <= 1e-12
    assert result["D2_pending_current_max_error"] <= 1e-12
    assert result["gpu_synaptic_emissions"] > 0
    assert result["gpu_synaptic_reward_calls"] > 0
    assert result["gpu_synaptic_plasticity_calls"] == 2000
    assert result["gpu_delay_consumed_ticks"] == 2000


def test_pan_parity_requires_full_finite_state_and_gpu_ticks():
    from src.playground.builder.session import PlaygroundSession
    from src.playground.cuda.builder_parity import compare_builder_runs

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
    gpu = deepcopy(cpu)
    gpu["execution"].update(
        neuron_backend="cuda_pan",
        gpu_membrane_ticks=128,
        gpu_pan_ticks=128,
        gpu_delay_consumed_ticks=128,
    )
    assert compare_builder_runs(cpu, gpu)["passed"]
    gpu["research_state"]["pan_states"][0]["pan_energy"] = float("nan")
    assert not compare_builder_runs(cpu, gpu)["passed"]
    gpu = deepcopy(cpu)
    gpu["execution"].update(
        neuron_backend="cuda_pan", gpu_membrane_ticks=128, gpu_pan_ticks=0
    )
    assert not compare_builder_runs(cpu, gpu)["passed"]
    del gpu["research_state"]
    assert not compare_builder_runs(cpu, gpu)["passed"]


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
def test_gpu_feedback_projection_all_modes(tmp_path, monkeypatch):
    import math

    monkeypatch.setenv("TMP", str(tmp_path))
    cpu = runtime(dimensions=32)
    gpu = runtime(dimensions=32)
    vector = [math.sin(i) * 0.8 for i in range(32)]
    for pan in (cpu, gpu):
        pan.population_vector = list(vector)
        pan.feedback_history = [
            [v * scale for v in vector] for scale in (0.2, 0.4, 0.7, 1.0)
        ]
        pan.feedback_gain = 7.0
        pan.feedback_threshold = 0.05
        pan.feedback_saturation = 0.7
    model = get_neuron_model("pan_adex_5d")
    with membrane.cuda_membrane_session(
        model.name, [model.parameters] * cpu.n_neurons, 1.0, pan_runtime=gpu
    ) as stepper:
        for source in ("population", "layer", "subset", "hypervector"):
            for target in ("all", "layer", "random_subset"):
                for nonlinearity in ("linear", "tanh", "sign", "clip"):
                    for delay in (0, 2):
                        for pan in (cpu, gpu):
                            pan.feedback_source = source
                            pan.feedback_target = target
                            pan.feedback_nonlinearity = nonlinearity
                            pan.feedback_delay = delay
                        assert cpu.feedback_currents() == pytest.approx(
                            stepper.pan.feedback_currents(), abs=1e-12, rel=0
                        )
        assert stepper.pan.feedback_calls == 96
        gpu.population_vector[0] = float("nan")
        gpu.feedback_delay = 0
        gpu.feedback_source = "population"
        with pytest.raises(ValueError, match="finite"):
            stepper.pan.feedback_currents()
        gpu.closed_loop = False
        assert stepper.pan.feedback_currents() == [0.0] * gpu.n_neurons
    assert cpu.feedback_samples == gpu.feedback_samples
    assert cpu.feedback_abs_total == pytest.approx(
        gpu.feedback_abs_total, abs=1e-10, rel=0
    )
