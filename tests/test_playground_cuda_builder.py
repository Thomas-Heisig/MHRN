"""Actual Builder CUDA selection, resource cleanup and behavioral equivalence."""

import os
from copy import deepcopy
from pathlib import Path

import pytest

from src.playground import PlaygroundConfig
from src.playground.cuda.builder_parity import compare_builder_runs, run_builder_parity
from src.playground.service import run


def test_cuda_backend_rejects_unsupported_models() -> None:
    with pytest.raises(ValueError, match="supports"):
        PlaygroundConfig.from_mapping(
            {"neuron_backend": "cuda_membrane", "neuron_model": "izhikevich"}
        )


def test_cuda_failure_is_not_silently_replaced_by_cpu(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from src.playground.builder import session

    def unavailable(*args: object, **kwargs: object) -> None:
        raise RuntimeError("GPU unavailable")

    monkeypatch.setattr(session, "cuda_membrane_session", unavailable)
    with pytest.raises(RuntimeError, match="GPU unavailable"):
        run(
            {
                "closed_loop_preset": "pan_full_balanced",
                "neuron_backend": "cuda_membrane",
                "persist": False,
            }
        )


def test_builder_parity_rejects_cpu_only_and_nonfinite_results() -> None:
    cpu = run(
        {
            "closed_loop_preset": "pan_full_balanced",
            "n_neurons": 32,
            "edge_budget": 64,
            "ticks": 128,
            "persist": False,
        }
    )
    assert not compare_builder_runs(cpu, cpu)["passed"]
    fake = deepcopy(cpu)
    fake["execution"].update(neuron_backend="cuda_membrane", gpu_membrane_ticks=128)
    assert compare_builder_runs(cpu, fake)["passed"]
    fake["monitors"]["state_samples"][0]["v"][0] = float("nan")
    assert not compare_builder_runs(cpu, fake)["passed"]


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
@pytest.mark.parametrize("seed", [12345, 42, 777])
def test_full_pan_builder_hardware_d3(
    seed: int, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("TMP", str(tmp_path))
    result = run_builder_parity(
        {"closed_loop_preset": "pan_full_balanced", "seed": seed}
    )
    assert result["passed"], result
    assert result["gpu_membrane_ticks"] == 2000
    assert result["D3_full_body_trajectory_exact"]


@pytest.mark.parametrize("failure", ["copy", "launch", "synchronize"])
def test_membrane_context_cleans_allocations_on_failures(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, failure: str
) -> None:
    import ctypes

    from src.playground.cuda import membrane
    from src.playground.cuda.runtime import (
        CudaDriverError,
        DeviceAllocation,
        DriverModule,
    )
    from src.playground.registry.neuron_models import get_neuron_model

    class FakeDriver:
        def __init__(self) -> None:
            self.allocated = []
            self.freed = []
            self.unloaded = False

        def load_cubin(self, *args, **kwargs):
            return DriverModule(
                ctypes.c_void_p(1), ctypes.c_void_p(2), ctypes.c_void_p(3), 0
            )

        def alloc_device(self, size):
            allocation = DeviceAllocation(len(self.allocated) + 1, size)
            self.allocated.append(allocation)
            return allocation

        def copy_host_to_device(self, *args):
            if failure == "copy":
                raise CudaDriverError("copy failed")

        def launch_kernel(self, *args, **kwargs):
            if failure == "launch":
                raise CudaDriverError("launch failed")

        def synchronize(self):
            raise CudaDriverError("synchronize failed")

        def free_device(self, allocation):
            self.freed.append(allocation)

        def unload(self, loaded):
            self.unloaded = True

    driver = FakeDriver()
    monkeypatch.setattr(membrane, "CudaDriver", lambda: driver)
    monkeypatch.setattr(membrane, "compile_cuda_source", lambda *a, **kw: "ptx")
    monkeypatch.setenv("TMP", str(tmp_path))
    model = get_neuron_model("lif")
    with pytest.raises(CudaDriverError):
        with membrane.cuda_membrane_session("lif", [model.parameters], 1.0) as stepper:
            stepper.step([{"v": -65.0}], [1.0], [1])
    assert driver.unloaded
    assert driver.freed == list(reversed(driver.allocated))


def test_live_session_rejects_unsupported_cuda_selection() -> None:
    from src.playground.pan.live_session import PANLiveSession

    with pytest.raises(ValueError, match="live sessions require cpu"):
        PANLiveSession(
            PlaygroundConfig.from_mapping(
                {
                    "closed_loop_preset": "pan_full_balanced",
                    "neuron_backend": "cuda_membrane",
                }
            )
        )


def test_spike_digest_covers_events_beyond_display_limit() -> None:
    from src.playground.instruments.monitors import SpikeMonitor

    left, right = SpikeMonitor(), SpikeMonitor()
    for tick in range(10_001):
        left.record(tick, 0)
        right.record(tick, int(tick == 10_000))
    assert left.rows() == right.rows()
    assert left.digest() != right.digest()
