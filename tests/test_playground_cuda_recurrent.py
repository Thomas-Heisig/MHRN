"""CPU contracts and opt-in physical GPU acceptance for CUDA-1.4."""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path

import pytest

from src.playground.cuda import recurrent
from src.playground.cuda.recurrent import (
    RecurrentInputs,
    cpu_recurrent_reference,
    execute_recurrent,
    recurrent_fixture,
    recurrent_parity,
    validate_recurrent_inputs,
)
from src.playground.cuda.runtime import CudaDriverError, DeviceAllocation


@pytest.mark.parametrize(
    "updates",
    [
        {"n_neurons": True},
        {"ticks": 1.5},
        {"ticks": 0},
        {"dt_ms": float("nan")},
        {"sources": (129,) * 129},
        {"offsets": (0,) * 130},
        {"delays": (0,) * 129},
        {"delays": (65,) * 129},
        {"weights": (float("inf"),) * 129},
        {"voltage": ()},
        {"model": "unknown"},
    ],
)
def test_recurrent_boundary_rejects_invalid_inputs(updates: dict[str, object]) -> None:
    with pytest.raises((ValueError, TypeError)):
        validate_recurrent_inputs(replace(recurrent_fixture(), **updates))


def test_delay_propagates_across_blocks_at_exact_tick() -> None:
    n = 65
    # Neuron zero spikes on tick zero; only neuron 64 receives its delayed edge.
    inputs = RecurrentInputs(
        n,
        12,
        (0,) * n + (1,),
        (0,),
        (7,),
        (400.0,),
        (0.0,) * (12 * n),
        (-49.0,) + (-65.0,) * (n - 1),
        (0.0,) * n,
    )
    result = cpu_recurrent_reference(inputs)
    spikes = result["spikes"]
    assert spikes[0] == 1
    assert [tick for tick in range(12) if spikes[tick * n + 64]] == [7]


@pytest.mark.parametrize("poison", [[], [float("nan")], [float("inf")], [0.0, 1.0]])
def test_recurrent_parity_fails_closed(poison: list[float]) -> None:
    reference = {"voltage": [0.0], "adaptation": [0.0], "spikes": [0]}
    assert not recurrent_parity(reference, {**reference, "voltage": poison})["passed"]


def test_recurrent_parity_rejects_spike_mismatch_and_empty_evidence() -> None:
    reference = {"voltage": [0.0], "adaptation": [0.0], "spikes": [0]}
    assert not recurrent_parity(reference, {**reference, "spikes": [1]})["passed"]
    assert not recurrent_parity({}, {})["passed"]


@pytest.mark.parametrize("failure", ["copy", "launch", "synchronize", "unload"])
def test_recurrent_failure_releases_every_allocation(
    failure: str, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    allocated = []
    freed = []
    unloaded = []

    class FakeDriver:
        def load_cubin(self, *args, **kwargs):
            return object()

        def alloc_device(self, size):
            allocation = DeviceAllocation(len(allocated) + 1, size)
            allocated.append(allocation)
            return allocation

        def copy_host_to_device(self, *args):
            if failure == "copy":
                raise CudaDriverError("copy failed")

        def launch_cooperative(self, *args, **kwargs):
            if failure == "launch":
                raise CudaDriverError("launch failed")
            return self

        def synchronize(self):
            if failure == "synchronize":
                raise CudaDriverError("synchronize failed")

        def copy_device_to_host(self, *args):
            pass

        def to_mapping(self):
            return {}

        def free_device(self, allocation):
            freed.append(allocation)
            if len(freed) == 1:
                raise CudaDriverError("free failed; continue cleanup")

        def unload(self, loaded):
            unloaded.append(loaded)
            if failure == "unload":
                raise CudaDriverError("unload failed")

    monkeypatch.setattr(recurrent, "CudaDriver", FakeDriver)
    monkeypatch.setattr(recurrent, "compile_cuda_source", lambda *args, **kwargs: "PTX")
    with pytest.raises(CudaDriverError, match=failure):
        execute_recurrent(recurrent_fixture(n_neurons=1, ticks=1), output_dir=tmp_path)
    assert freed == list(reversed(allocated))
    assert len(unloaded) == 1


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
@pytest.mark.parametrize("model", ["lif", "pan_adex_5d"])
@pytest.mark.parametrize("ticks", [10, 100, 1000, 2000])
def test_physical_multiblock_delay_parity(
    model: str, ticks: int, tmp_path: Path
) -> None:
    inputs = recurrent_fixture(model=model, ticks=ticks)
    reference = cpu_recurrent_reference(inputs)
    result = execute_recurrent(inputs, output_dir=tmp_path)
    assert result["preflight"]["required_blocks"] == 3
    assert recurrent_parity(reference, result["outputs"])["passed"]
    if ticks >= 100:
        assert sum(reference["spikes"]) > 0


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
@pytest.mark.parametrize("block_size", [32, 128, 256])
def test_physical_ring_wrap_and_partial_blocks(block_size: int, tmp_path: Path) -> None:
    inputs = replace(recurrent_fixture(ticks=150), delays=(64,) * 129)
    reference = cpu_recurrent_reference(inputs)
    result = execute_recurrent(inputs, block_size=block_size, output_dir=tmp_path)
    assert recurrent_parity(reference, result["outputs"])["passed"]
