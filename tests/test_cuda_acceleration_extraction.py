"""Wave-4 CUDA infrastructure extraction contracts."""

from __future__ import annotations

from pathlib import Path

from src.acceleration.cuda import (
    CudaDriver,
    CudaDriverError,
    CudaRuntimeUnavailable,
    DeviceAllocation,
    compile_cuda_source,
    cooperative_capacity,
    validate_cuda_block_size,
)
from src.playground.cuda import nvrtc as playground_nvrtc
from src.playground.cuda import runtime as playground_runtime


def test_playground_cuda_infrastructure_uses_canonical_objects() -> None:
    assert playground_runtime.CudaDriver is CudaDriver
    assert playground_runtime.CudaDriverError is CudaDriverError
    assert playground_runtime.CudaRuntimeUnavailable is CudaRuntimeUnavailable
    assert playground_runtime.DeviceAllocation is DeviceAllocation
    assert playground_nvrtc.compile_cuda_source is compile_cuda_source


def test_canonical_acceleration_package_has_no_playground_dependency() -> None:
    root = Path(__file__).resolve().parents[1] / "src" / "acceleration" / "cuda"
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "src.playground" not in text
        assert "from src.playground" not in text


def test_cooperative_preflight_contract_is_preserved() -> None:
    result = cooperative_capacity(
        n_neurons=129,
        block_size=64,
        multiprocessor_count=28,
        active_blocks_per_sm=2,
    )
    assert result.required_blocks == 3
    assert result.resident_block_capacity == 56
    assert result.launch_fits is True
    assert validate_cuda_block_size(128) == 128
