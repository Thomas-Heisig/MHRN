"""Fail-closed regression tests for the Playground CUDA-1.3 boundary."""

from __future__ import annotations

import ctypes
from dataclasses import replace

import pytest

from src.dashboard import playground_api
from src.playground.cuda import (
    CudaDriver,
    CudaDriverError,
    DeviceAllocation,
    DriverModule,
    GateLaunchInputs,
    compile_mapping,
    cpu_gate_reference,
    gate_execution_parity_summary,
    hash_to_uniform_f32,
    smoke_gate_launch_inputs,
    validate_cuda_block_size,
    validate_gate_launch_inputs,
)


def _bundle_and_inputs() -> tuple[object, GateLaunchInputs]:
    bundle = compile_mapping({"closed_loop_preset": "minimal_closed_loop"})
    return bundle, smoke_gate_launch_inputs(bundle, n_neurons=2, seed=12345)


@pytest.mark.parametrize("poison", [float("nan"), float("inf"), float("-inf")])
def test_d2_parity_fails_closed_on_nonfinite_candidate(poison: float) -> None:
    summary = gate_execution_parity_summary(
        {"outputs": {"current": [1.0, 2.0], "action": [0, 1]}},
        {"outputs": {"current": [1.0, poison], "action": [0, 1]}},
    )
    assert summary["passed"] is False
    assert summary["current_max_abs_error"] is None
    assert "NaN/Inf" in str(summary["failure_reason"])


def test_d2_parity_fails_closed_on_empty_or_mismatched_evidence() -> None:
    empty = gate_execution_parity_summary(
        {"outputs": {"current": [], "action": []}},
        {"outputs": {"current": [], "action": []}},
    )
    length = gate_execution_parity_summary(
        {"outputs": {"current": [1.0], "action": [0]}},
        {"outputs": {"current": [1.0, 2.0], "action": [0]}},
    )
    missing_action = gate_execution_parity_summary(
        {"outputs": {"current": [1.0], "action": []}},
        {"outputs": {"current": [1.0], "action": []}},
    )
    assert empty["passed"] is False
    assert length["passed"] is False
    assert missing_action["passed"] is False


@pytest.mark.parametrize("poison", [float("nan"), float("inf"), float("-inf"), 1.0e100])
def test_abi_rejects_nonfinite_or_out_of_float32_range(poison: float) -> None:
    bundle, good = _bundle_and_inputs()
    broken = replace(good, input_current=(poison, good.input_current[1]))
    with pytest.raises(ValueError):
        validate_gate_launch_inputs(bundle, broken)


@pytest.mark.parametrize("tick", [2**32, -1, 1.5, True])
def test_abi_rejects_invalid_tick_before_uint32_packing(tick: object) -> None:
    bundle, good = _bundle_and_inputs()
    broken = replace(good, tick=tick)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="tick"):
        validate_gate_launch_inputs(bundle, broken)


@pytest.mark.parametrize("mask", [-1, 2**64, 1.5, True])
def test_abi_rejects_invalid_channel_mask_before_bit_operations(mask: object) -> None:
    bundle, good = _bundle_and_inputs()
    broken = replace(
        good,
        channel_masks=(mask, good.channel_masks[1]),  # type: ignore[arg-type]
    )
    with pytest.raises(ValueError, match="channel_masks"):
        validate_gate_launch_inputs(bundle, broken)


def test_from_sequences_does_not_hide_invalid_scalar_types() -> None:
    bundle = compile_mapping({"closed_loop_preset": "minimal_closed_loop"})
    good = smoke_gate_launch_inputs(bundle, n_neurons=1)
    broken = GateLaunchInputs.from_sequences(
        input_current=good.input_current,
        channel_masks=good.channel_masks,
        amplitudes=good.amplitudes,
        reward_ring=good.reward_ring,
        action_map=good.action_map,
        feedback_matrix=good.feedback_matrix,
        population=good.population,
        logits=good.logits,
        tick=1.5,  # type: ignore[arg-type]
    )
    with pytest.raises(ValueError, match="tick"):
        validate_gate_launch_inputs(bundle, broken)


class _CopyLib:
    def __init__(self) -> None:
        self.called = False

    def cuMemcpyHtoD_v2(self, *_args: object) -> int:
        self.called = True
        return 0

    def cuMemcpyDtoH_v2(self, *_args: object) -> int:
        self.called = True
        return 0


def _driver_with_lib(lib: object) -> CudaDriver:
    driver = object.__new__(CudaDriver)
    driver._lib = lib  # type: ignore[attr-defined]
    return driver


def test_h2d_rejects_host_buffer_smaller_than_requested_copy() -> None:
    lib = _CopyLib()
    driver = _driver_with_lib(lib)
    host = (ctypes.c_uint32 * 1)(1)
    allocation = DeviceAllocation(ptr=1, size_bytes=16)
    with pytest.raises(ValueError, match="host buffer"):
        driver.copy_host_to_device(allocation, host)
    assert lib.called is False


def test_d2h_rejects_host_buffer_smaller_than_requested_copy() -> None:
    lib = _CopyLib()
    driver = _driver_with_lib(lib)
    host = (ctypes.c_uint32 * 1)()
    allocation = DeviceAllocation(ptr=1, size_bytes=16)
    with pytest.raises(ValueError, match="host buffer"):
        driver.copy_device_to_host(host, allocation)
    assert lib.called is False


class _CleanupLib:
    def __init__(self) -> None:
        self.context_destroyed = False

    def cuModuleUnload(self, _module: object) -> int:
        return 999

    def cuCtxDestroy_v2(self, _context: object) -> int:
        self.context_destroyed = True
        return 0


def test_unload_attempts_context_cleanup_after_module_unload_failure() -> None:
    lib = _CleanupLib()
    driver = _driver_with_lib(lib)
    loaded = DriverModule(
        context=ctypes.c_void_p(1),
        module=ctypes.c_void_p(2),
        function=ctypes.c_void_p(3),
        device_ordinal=0,
    )
    with pytest.raises(CudaDriverError, match="cuModuleUnload"):
        driver.unload(loaded)
    assert lib.context_destroyed is True


@pytest.mark.parametrize("bits", [0, 1, 2**31, 2**32 - 2, 2**32 - 1])
def test_rng_mapping_is_always_half_open(bits: int) -> None:
    uniform = hash_to_uniform_f32(bits)
    assert 0.0 <= uniform < 1.0


def test_rng_max_hash_still_explores_at_epsilon_one() -> None:
    bundle = compile_mapping(
        {
            "closed_loop_preset": "minimal_closed_loop",
            "pan_feedback_gain": 0.0,
        }
    )
    good = smoke_gate_launch_inputs(bundle, n_neurons=1, seed=4050964655)
    inputs = replace(good, logits=(10.0, 0.0, 0.0, 0.0), epsilon=1.0)
    result = cpu_gate_reference(bundle, inputs)
    assert result["outputs"]["action"] == [3]


def test_generated_rng_uses_uint24_to_float32_half_open_mapping() -> None:
    bundle = compile_mapping({"closed_loop_preset": "minimal_closed_loop"})
    assert "shr.u32 %r22, %r20, 8;" in bundle.ptx
    assert "mul.f32 %f7, %f7, 0f33800000;" in bundle.ptx
    assert "cvt.rn.f32.u32 %f7, %r20;" not in bundle.ptx
    assert "random_bits >> 8" in bundle.cuda_source
    assert "5.960464477539063e-8f" in bundle.cuda_source


@pytest.mark.parametrize("block_size", [0, 31, 33, 2048, True])
def test_cuda_block_size_validation_rejects_illegal_shapes(block_size: object) -> None:
    with pytest.raises(ValueError, match="block_size"):
        validate_cuda_block_size(block_size)  # type: ignore[arg-type]


@pytest.mark.parametrize("block_size", [32, 64, 128, 256, 512, 1024])
def test_cuda_block_size_validation_accepts_legal_warp_multiples(
    block_size: int,
) -> None:
    assert validate_cuda_block_size(block_size) == block_size


def test_smoke_route_rejects_2048_threads_before_gpu_access() -> None:
    with pytest.raises(ValueError, match="block_size"):
        playground_api.post_playground(
            "/api/playground/cuda/smoke",
            {"block_size": 2048},
        )


class _BusySemaphore:
    def acquire(self, *, blocking: bool) -> bool:
        assert blocking is False
        return False

    def release(self) -> None:
        raise AssertionError("release must not run when acquire failed")


@pytest.mark.parametrize(
    "path",
    [
        "/api/playground/cuda/preflight",
        "/api/playground/cuda/smoke",
        "/api/playground/cuda/rng-parity",
    ],
)
def test_cuda_diagnostics_share_two_worker_limit(
    monkeypatch: pytest.MonkeyPatch,
    path: str,
) -> None:
    monkeypatch.setattr(playground_api, "_reserve_rate_slot", lambda: None)
    monkeypatch.setattr(playground_api, "_RUN_SEMAPHORE", _BusySemaphore())
    with pytest.raises(playground_api.PlaygroundBusyError):
        playground_api.post_playground(path, {})
