"""CUDA-1 runtime helpers for the Playground PAN gate compiler.

The runtime is deliberately optional: importing it requires neither a CUDA
toolkit nor a GPU. PTX assembly requires `ptxas`; driver loading and occupancy
preflight require a CUDA driver. Scientific promotion remains disabled.
"""

from __future__ import annotations

import ctypes
import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.verification.parity import (
    default_parity_contract,
    exact_spike_parity,
    metric_behavior_parity,
)
from src.verification.parity import (
    max_abs_error as canonical_max_abs_error,
)

from src.acceleration.cuda import (
    CooperativePreflight as CooperativePreflight,
    CudaDriver as CudaDriver,
    CudaDriverError as CudaDriverError,
    CudaRuntimeUnavailable as CudaRuntimeUnavailable,
    DeviceAllocation as DeviceAllocation,
    DriverModule as DriverModule,
    PtxasReport as PtxasReport,
    assemble_ptx as assemble_ptx,
    cooperative_capacity as cooperative_capacity,
    parse_ptxas_verbose as parse_ptxas_verbose,
    validate_cuda_block_size as validate_cuda_block_size,
)

from .pan_compiler import CompileBundle


@dataclass(frozen=True, slots=True)
class GateLaunchInputs:
    """Host-side ABI payload for one pan_gate_kernel launch."""

    input_current: tuple[float, ...]
    channel_masks: tuple[int, ...]
    amplitudes: tuple[float, ...]
    reward_ring: tuple[float, ...]
    action_map: tuple[float, ...]
    feedback_matrix: tuple[float, ...]
    population: tuple[float, ...]
    logits: tuple[float, ...]
    tick: int = 0
    target_index: int = 0
    previous_action: int = 0
    seed: int = 0
    epsilon: float = 0.0

    @classmethod
    def from_sequences(
        cls,
        *,
        input_current: Sequence[float],
        channel_masks: Sequence[int],
        amplitudes: Sequence[float],
        reward_ring: Sequence[float],
        action_map: Sequence[float],
        feedback_matrix: Sequence[float],
        population: Sequence[float],
        logits: Sequence[float],
        tick: int = 0,
        target_index: int = 0,
        previous_action: int = 0,
        seed: int = 0,
        epsilon: float = 0.0,
    ) -> "GateLaunchInputs":
        return cls(
            input_current=tuple(input_current),
            channel_masks=tuple(channel_masks),
            amplitudes=tuple(amplitudes),
            reward_ring=tuple(reward_ring),
            action_map=tuple(action_map),
            feedback_matrix=tuple(feedback_matrix),
            population=tuple(population),
            logits=tuple(logits),
            tick=tick,
            target_index=target_index,
            previous_action=previous_action,
            seed=seed,
            epsilon=epsilon,
        )


def assemble_bundle(
    bundle: CompileBundle,
    *,
    output_dir: Path | None = None,
    ptxas: str = "ptxas",
) -> PtxasReport:
    """Assemble one compiler bundle using its declared target architecture."""

    target = str(bundle.manifest.get("target_sm", "sm_86"))
    return assemble_ptx(
        bundle.ptx,
        target_sm=target,
        output_dir=output_dir,
        ptxas=ptxas,
    )


def preflight_bundle(
    bundle: CompileBundle,
    *,
    n_neurons: int,
    block_size: int = 128,
    dynamic_shared_bytes: int = 0,
    output_dir: Path | None = None,
    ptxas: str = "ptxas",
    driver_library: str | None = None,
    device_ordinal: int = 0,
) -> dict[str, object]:
    """Assemble, load and occupancy-check one generated kernel.

    This is a technical preflight only. It does not execute the kernel and does
    not establish CPU/CUDA semantic equivalence.
    """

    report = assemble_bundle(bundle, output_dir=output_dir, ptxas=ptxas)
    driver = CudaDriver(driver_library)
    loaded = driver.load_cubin(
        report.cubin_path,
        device_ordinal=device_ordinal,
    )
    try:
        cooperative = driver.cooperative_preflight(
            loaded,
            n_neurons=n_neurons,
            block_size=block_size,
            dynamic_shared_bytes=dynamic_shared_bytes,
        )
    finally:
        driver.unload(loaded)
    return {
        "classification": "PLAYGROUND_CUDA1_PREFLIGHT",
        "scientific_evidence": False,
        "execution_status": "ASSEMBLED_LOADED_NOT_EXECUTED",
        "ptxas": report.to_mapping(),
        "cooperative": cooperative.to_mapping(),
        "ready_for_cooperative_launch": cooperative.launch_fits,
        "full_snn_parity_verified": False,
    }


_FLOAT32_MAX = 3.4028234663852886e38
_UINT32_MAX = 0xFFFFFFFF
_UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def _numeric_int(value: object, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be an integer")
    converted = int(value)
    if float(value) != float(converted):
        raise ValueError(f"{field} must be an integer")
    return converted


def _numeric_float(value: object, *, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be numeric")
    converted = float(value)
    if not math.isfinite(converted):
        raise ValueError(f"{field} must be finite")
    if abs(converted) > _FLOAT32_MAX:
        raise ValueError(f"{field} exceeds float32 range")
    return converted


def hash_to_uniform_f32(random_bits: int) -> float:
    """Map a uint32 hash into the exactly representable float32 interval [0, 1)."""

    if isinstance(random_bits, bool) or not isinstance(random_bits, int):
        raise ValueError("random_bits must be an integer")
    if not 0 <= random_bits <= _UINT32_MAX:
        raise ValueError("random_bits must fit unsigned 32-bit")
    mantissa = random_bits >> 8
    return _f32(float(mantissa) * (2.0**-24))


def _kernel_abi(bundle: CompileBundle) -> Mapping[str, object]:
    abi = bundle.manifest.get("kernel_abi")
    if not isinstance(abi, Mapping):
        raise ValueError("compile bundle is missing kernel_abi metadata")
    return abi


def validate_gate_launch_inputs(
    bundle: CompileBundle,
    inputs: GateLaunchInputs,
) -> dict[str, int]:
    """Validate host buffers against the compiler-declared PTX ABI."""

    abi = _kernel_abi(bundle)
    try:
        input_channels = _numeric_int(
            abi["input_channels"], field="kernel_abi.input_channels"
        )
        action_count = _numeric_int(
            abi["action_space_size"], field="kernel_abi.action_space_size"
        )
        pan_dimensions = _numeric_int(
            abi["pan_dimensions"], field="kernel_abi.pan_dimensions"
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("kernel_abi dimensions are invalid") from exc

    n_neurons = len(inputs.input_current)
    if n_neurons <= 0:
        raise ValueError("input_current must contain at least one neuron")
    expected_lengths = {
        "channel_masks": n_neurons,
        "amplitudes": input_channels,
        "action_map": action_count * input_channels,
        "feedback_matrix": n_neurons * pan_dimensions,
        "population": pan_dimensions,
        "logits": n_neurons * action_count,
    }
    actual_lengths = {
        "channel_masks": len(inputs.channel_masks),
        "amplitudes": len(inputs.amplitudes),
        "action_map": len(inputs.action_map),
        "feedback_matrix": len(inputs.feedback_matrix),
        "population": len(inputs.population),
        "logits": len(inputs.logits),
    }
    for name, expected in expected_lengths.items():
        actual = actual_lengths[name]
        if actual != expected:
            raise ValueError(f"{name} length {actual} != expected {expected}")
    if not inputs.reward_ring:
        raise ValueError("reward_ring must contain at least one value")

    float_vectors = {
        "input_current": inputs.input_current,
        "amplitudes": inputs.amplitudes,
        "reward_ring": inputs.reward_ring,
        "action_map": inputs.action_map,
        "feedback_matrix": inputs.feedback_matrix,
        "population": inputs.population,
        "logits": inputs.logits,
    }
    for name, values in float_vectors.items():
        for index, value in enumerate(values):
            _numeric_float(value, field=f"{name}[{index}]")

    for index, mask in enumerate(inputs.channel_masks):
        if isinstance(mask, bool) or not isinstance(mask, int):
            raise ValueError(f"channel_masks[{index}] must be an integer")
        if not 0 <= mask <= _UINT64_MAX:
            raise ValueError(f"channel_masks[{index}] must fit unsigned 64-bit")

    for field, value in (
        ("tick", inputs.tick),
        ("target_index", inputs.target_index),
        ("previous_action", inputs.previous_action),
        ("seed", inputs.seed),
    ):
        checked = _numeric_int(value, field=field)
        if not 0 <= checked <= _UINT32_MAX:
            raise ValueError(f"{field} must fit unsigned 32-bit")

    if not 0 <= inputs.target_index < action_count:
        raise ValueError("target_index is outside action space")
    if not 0 <= inputs.previous_action < action_count:
        raise ValueError("previous_action is outside action space")

    epsilon = _numeric_float(inputs.epsilon, field="epsilon")
    if not 0.0 <= epsilon <= 1.0:
        raise ValueError("epsilon must be in [0, 1]")
    return {
        "n_neurons": n_neurons,
        "input_channels": input_channels,
        "action_count": action_count,
        "pan_dimensions": pan_dimensions,
    }


def smoke_gate_launch_inputs(
    bundle: CompileBundle,
    *,
    n_neurons: int,
    seed: int = 0,
) -> GateLaunchInputs:
    """Build deterministic bounded buffers for a first single-tick GPU smoke run."""

    if n_neurons <= 0:
        raise ValueError("n_neurons must be positive")
    abi = _kernel_abi(bundle)
    input_channels = _numeric_int(
        abi["input_channels"], field="kernel_abi.input_channels"
    )
    action_count = _numeric_int(
        abi["action_space_size"], field="kernel_abi.action_space_size"
    )
    pan_dimensions = _numeric_int(
        abi["pan_dimensions"], field="kernel_abi.pan_dimensions"
    )
    full_mask = (1 << input_channels) - 1 if input_channels < 64 else 0xFFFFFFFFFFFFFFFF
    return GateLaunchInputs(
        input_current=tuple(0.0 for _ in range(n_neurons)),
        channel_masks=tuple(full_mask for _ in range(n_neurons)),
        amplitudes=tuple(1.0 for _ in range(input_channels)),
        reward_ring=(0.0,),
        action_map=tuple(0.0 for _ in range(action_count * input_channels)),
        feedback_matrix=tuple(0.0 for _ in range(n_neurons * pan_dimensions)),
        population=tuple(0.0 for _ in range(pan_dimensions)),
        logits=tuple(0.0 for _ in range(n_neurons * action_count)),
        seed=seed,
        epsilon=0.0,
    )


def _f32(value: float) -> float:
    """Round a scalar through IEEE-754 binary32 like the PTX ABI."""

    return float(ctypes.c_float(float(value)).value)


def _gate_params(
    bundle: CompileBundle,
    *,
    stage: str,
    label: str,
) -> Mapping[str, object] | None:
    for raw_gate in bundle.gate_ir:
        if raw_gate.get("stage") == stage and raw_gate.get("label") == label:
            params = raw_gate.get("params")
            if isinstance(params, Mapping):
                return params
            return {}
    return None


def _gate_labels(bundle: CompileBundle, stage: str) -> set[str]:
    return {
        str(raw_gate.get("label"))
        for raw_gate in bundle.gate_ir
        if raw_gate.get("stage") == stage
    }


def cpu_gate_reference(
    bundle: CompileBundle,
    inputs: GateLaunchInputs,
) -> dict[str, object]:
    """Execute the current single-tick PTX gate ABI as a CPU reference.

    The function deliberately mirrors only the values observable from the
    current `pan_gate_kernel`: output current and selected action. Internal
    B/C4 scratch values that do not reach those outputs are not promoted to
    parity claims.
    """

    shape = validate_gate_launch_inputs(bundle, inputs)
    n_neurons = shape["n_neurons"]
    input_channels = shape["input_channels"]
    action_count = shape["action_count"]
    pan_dimensions = shape["pan_dimensions"]

    a2_labels = _gate_labels(bundle, "A2")
    a3_labels = _gate_labels(bundle, "A3")
    a4_labels = _gate_labels(bundle, "A4")
    c1_labels = _gate_labels(bundle, "C1")

    reward_delay_params = _gate_params(bundle, stage="A3", label="reward_delay")
    reward_magnitude_params = _gate_params(bundle, stage="A3", label="reward_magnitude")
    reward_select_params = _gate_params(
        bundle, stage="A3", label="reward_channel_select"
    )
    coupling_params = _gate_params(bundle, stage="A4", label="action_coupling")
    feedback_dot_params = _gate_params(bundle, stage="C1", label="pan_feedback_dot")
    feedback_gain_params = _gate_params(bundle, stage="C1", label="pan_feedback_gain")
    feedback_threshold_params = _gate_params(
        bundle, stage="C2", label="pan_feedback_threshold"
    )
    feedback_saturation_params = _gate_params(
        bundle, stage="C2", label="pan_feedback_saturation"
    )

    output_current: list[float] = []
    output_action: list[int] = []

    for gid in range(n_neurons):
        mask = int(inputs.channel_masks[gid])
        source_current = _f32(inputs.input_current[gid])
        current = _f32(0.0)

        for channel in range(input_channels):
            if mask & (1 << channel):
                product = _f32(source_current * _f32(inputs.amplitudes[channel]))
                current = _f32(current + product)

        for action in range(action_count):
            label = f"target_match_{action}"
            if label not in a2_labels:
                continue
            params = _gate_params(bundle, stage="A2", label=label) or {}
            channel = _numeric_int(
                params.get("channel", action % input_channels),
                field="A2.target_match.channel",
            )
            if inputs.target_index == action and mask & (1 << channel):
                cue_params = (
                    _gate_params(
                        bundle,
                        stage="A2",
                        label=f"target_cue_{action}",
                    )
                    or {}
                )
                cue_current = _numeric_float(
                    cue_params.get("current", 0.0),
                    field="A2.target_cue.current",
                )
                current = _f32(current + _f32(cue_current))

        if "reward_channel_select" in a3_labels:
            delay = _numeric_int(
                (reward_delay_params or {}).get("delay_ticks", 0),
                field="A3.reward_delay.delay_ticks",
            )
            reward_value = 0.0
            if inputs.tick >= delay:
                reward_index = (inputs.tick - delay) % len(inputs.reward_ring)
                reward_value = _f32(inputs.reward_ring[reward_index])
            magnitude = _numeric_float(
                (reward_magnitude_params or {}).get("magnitude", 1.0),
                field="A3.reward_magnitude.magnitude",
            )
            reward_value = _f32(reward_value * _f32(magnitude))
            reward_channel = _numeric_int(
                (reward_select_params or {}).get("channel", 0),
                field="A3.reward_channel_select.channel",
            )
            if mask & (1 << reward_channel):
                current = _f32(current + reward_value)

        if "action_coupling" in a4_labels:
            map_index = inputs.previous_action * input_channels + gid % input_channels
            action_value = _f32(inputs.action_map[map_index])
            strength = _numeric_float(
                (coupling_params or {}).get("strength", 1.0),
                field="A4.action_coupling.strength",
            )
            current = _f32(current + _f32(action_value * _f32(strength)))

        if "pan_feedback_dot" in c1_labels:
            dimensions = _numeric_int(
                (feedback_dot_params or {}).get("dimensions", pan_dimensions),
                field="C1.pan_feedback_dot.dimensions",
            )
            feedback = _f32(0.0)
            base = gid * pan_dimensions
            for dim in range(dimensions):
                contribution = _f32(
                    _f32(inputs.feedback_matrix[base + dim])
                    * _f32(inputs.population[dim])
                )
                feedback = _f32(feedback + contribution)

            if "pan_feedback_tanh" in c1_labels:
                feedback = _f32(math.tanh(feedback))
            elif "pan_feedback_sign" in c1_labels:
                feedback = _f32(1.0 if feedback > 0.0 else -1.0)
            elif "pan_feedback_clip" in c1_labels:
                feedback = _f32(max(-1.0, min(1.0, feedback)))

            gain = _numeric_float(
                (feedback_gain_params or {}).get("gain", 1.0),
                field="C1.pan_feedback_gain.gain",
            )
            feedback = _f32(feedback * _f32(gain))
            threshold = _numeric_float(
                (feedback_threshold_params or {}).get("threshold", 0.0),
                field="C2.pan_feedback_threshold.threshold",
            )
            if abs(feedback) < threshold:
                feedback = _f32(0.0)
            saturation = _numeric_float(
                (feedback_saturation_params or {}).get("saturation", float("inf")),
                field="C2.pan_feedback_saturation.saturation",
            )
            feedback = _f32(max(-saturation, min(saturation, feedback)))
            current = _f32(current + feedback)

        logits_offset = gid * action_count
        best_action = 0
        best_value = _f32(inputs.logits[logits_offset])
        for candidate in range(1, action_count):
            value = _f32(inputs.logits[logits_offset + candidate])
            if value > best_value:
                best_value = value
                best_action = candidate

        random_bits = ((gid ^ inputs.seed ^ inputs.tick) * 2654435761) & 0xFFFFFFFF
        uniform = hash_to_uniform_f32(random_bits)
        if uniform < _f32(inputs.epsilon):
            best_action = random_bits % action_count

        output_current.append(current)
        output_action.append(best_action)

    return {
        "classification": "PLAYGROUND_CPU_GATE_ABI_REFERENCE",
        "scientific_evidence": False,
        "execution_status": "CPU_REFERENCE_EXECUTED",
        "comparison_scope": "GATE_OUTPUT_ONLY_NOT_FULL_SNN",
        "outputs": {
            "current": output_current,
            "action": output_action,
        },
    }


def gate_execution_parity_summary(
    reference: Mapping[str, object],
    candidate: Mapping[str, object],
    *,
    tolerance: float = 1.0e-4,
    reference_commit: str = "",
) -> dict[str, object]:
    """Compare CPU/CUDA gate outputs and fail closed on invalid evidence."""

    base = {
        "classification": "PLAYGROUND_CUDA_GATE_EXECUTION_PARITY",
        "scientific_evidence": False,
        "parity_class": "D2",
        "comparison_scope": "GATE_OUTPUT_ONLY_NOT_FULL_SNN",
        "reference_source": "CPU_GATE_ABI_REFERENCE",
        "reference_frozen_at": reference_commit or "UNSPECIFIED",
        "current_tolerance": tolerance,
        "full_snn_parity_verified": False,
    }

    def fail(reason: str) -> dict[str, object]:
        return {
            **base,
            "current_max_abs_error": None,
            "actions_exact": False,
            "failure_reason": reason,
            "passed": False,
        }

    reference_outputs = reference.get("outputs")
    candidate_outputs = candidate.get("outputs")
    if not isinstance(reference_outputs, Mapping) or not isinstance(
        candidate_outputs, Mapping
    ):
        return fail("gate execution results must contain outputs mappings")

    reference_current = reference_outputs.get("current")
    candidate_current = candidate_outputs.get("current")
    reference_action = reference_outputs.get("action")
    candidate_action = candidate_outputs.get("action")
    for name, value in (
        ("reference current", reference_current),
        ("candidate current", candidate_current),
        ("reference action", reference_action),
        ("candidate action", candidate_action),
    ):
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
            return fail(f"{name} output must be a sequence")

    assert isinstance(reference_current, Sequence)
    assert isinstance(candidate_current, Sequence)
    assert isinstance(reference_action, Sequence)
    assert isinstance(candidate_action, Sequence)

    if len(reference_current) != len(candidate_current):
        return fail("current output length mismatch")
    if len(reference_action) != len(candidate_action):
        return fail("action output length mismatch")
    if not reference_current or not reference_action:
        return fail("parity outputs must not be empty")
    if len(reference_current) != len(reference_action):
        return fail("current/action output length mismatch")

    try:
        reference_current_f = [float(value) for value in reference_current]
        candidate_current_f = [float(value) for value in candidate_current]
    except (TypeError, ValueError):
        return fail("current outputs must be numeric")
    if not all(math.isfinite(value) for value in reference_current_f):
        return fail("reference current contains NaN/Inf")
    if not all(math.isfinite(value) for value in candidate_current_f):
        return fail("candidate current contains NaN/Inf")

    if any(
        isinstance(value, bool) or not isinstance(value, int)
        for value in reference_action
    ):
        return fail("reference actions must be integers")
    if any(
        isinstance(value, bool) or not isinstance(value, int)
        for value in candidate_action
    ):
        return fail("candidate actions must be integers")

    current_error = max_abs_error(reference_current_f, candidate_current_f)
    actions_exact = list(reference_action) == list(candidate_action)
    return {
        **base,
        "current_max_abs_error": current_error,
        "actions_exact": actions_exact,
        "failure_reason": None,
        "passed": current_error <= tolerance and actions_exact,
    }


def _f32_buffer(values: Sequence[float]) -> ctypes.Array[Any]:
    array_type = ctypes.c_float * len(values)
    return array_type(*(float(value) for value in values))


def _u64_buffer(values: Sequence[int]) -> ctypes.Array[Any]:
    array_type = ctypes.c_uint64 * len(values)
    return array_type(*(int(value) for value in values))


def execute_gate_bundle(
    bundle: CompileBundle,
    inputs: GateLaunchInputs,
    *,
    block_size: int = 64,
    output_dir: Path | None = None,
    ptxas: str = "ptxas",
    driver_library: str | None = None,
    device_ordinal: int = 0,
) -> dict[str, object]:
    """Assemble, load and execute one single-tick Playground gate kernel.

    This is CUDA-1.2 engineering execution only. The emitted PTX gate kernel
    computes bounded gate current/action outputs; it is not yet the canonical
    MHRN SNN backend and does not establish full neuron/synapse parity.
    """

    validate_cuda_block_size(block_size)
    shape = validate_gate_launch_inputs(bundle, inputs)
    report = assemble_bundle(bundle, output_dir=output_dir, ptxas=ptxas)
    driver = CudaDriver(driver_library)
    loaded = driver.load_cubin(
        report.cubin_path,
        kernel_name=str(_kernel_abi(bundle).get("entry", "pan_gate_kernel")),
        device_ordinal=device_ordinal,
    )
    allocations: list[DeviceAllocation] = []
    try:
        memory_before_free, memory_total = driver.memory_info()
        host_buffers = {
            "input": _f32_buffer(inputs.input_current),
            "channel_masks": _u64_buffer(inputs.channel_masks),
            "amplitudes": _f32_buffer(inputs.amplitudes),
            "reward_ring": _f32_buffer(inputs.reward_ring),
            "action_map": _f32_buffer(inputs.action_map),
            "feedback_matrix": _f32_buffer(inputs.feedback_matrix),
            "population": _f32_buffer(inputs.population),
            "logits": _f32_buffer(inputs.logits),
        }
        sizes = {
            "input": len(inputs.input_current) * ctypes.sizeof(ctypes.c_float),
            "channel_masks": len(inputs.channel_masks) * ctypes.sizeof(ctypes.c_uint64),
            "amplitudes": len(inputs.amplitudes) * ctypes.sizeof(ctypes.c_float),
            "reward_ring": len(inputs.reward_ring) * ctypes.sizeof(ctypes.c_float),
            "action_map": len(inputs.action_map) * ctypes.sizeof(ctypes.c_float),
            "feedback_matrix": len(inputs.feedback_matrix)
            * ctypes.sizeof(ctypes.c_float),
            "population": len(inputs.population) * ctypes.sizeof(ctypes.c_float),
            "logits": len(inputs.logits) * ctypes.sizeof(ctypes.c_float),
        }
        device: dict[str, DeviceAllocation] = {}
        for name in (
            "input",
            "channel_masks",
            "amplitudes",
            "reward_ring",
            "action_map",
            "feedback_matrix",
            "population",
            "logits",
        ):
            allocation = driver.alloc_device(sizes[name])
            allocations.append(allocation)
            device[name] = allocation
            driver.copy_host_to_device(allocation, host_buffers[name])

        out_current = driver.alloc_device(
            shape["n_neurons"] * ctypes.sizeof(ctypes.c_float)
        )
        out_action = driver.alloc_device(
            shape["n_neurons"] * ctypes.sizeof(ctypes.c_uint32)
        )
        allocations.extend([out_current, out_action])

        arguments: list[object] = [
            ctypes.c_uint64(device["input"].ptr),
            ctypes.c_uint64(device["channel_masks"].ptr),
            ctypes.c_uint64(device["amplitudes"].ptr),
            ctypes.c_uint64(device["reward_ring"].ptr),
            ctypes.c_uint64(device["action_map"].ptr),
            ctypes.c_uint64(device["feedback_matrix"].ptr),
            ctypes.c_uint64(device["population"].ptr),
            ctypes.c_uint64(device["logits"].ptr),
            ctypes.c_uint64(out_current.ptr),
            ctypes.c_uint64(out_action.ptr),
            ctypes.c_uint32(shape["n_neurons"]),
            ctypes.c_uint32(inputs.tick),
            ctypes.c_uint32(len(inputs.reward_ring)),
            ctypes.c_uint32(inputs.target_index),
            ctypes.c_uint32(inputs.previous_action),
            ctypes.c_uint32(inputs.seed),
            ctypes.c_float(inputs.epsilon),
        ]
        grid_x = math.ceil(shape["n_neurons"] / block_size)
        driver.launch_kernel(
            loaded,
            grid=(grid_x, 1, 1),
            block=(block_size, 1, 1),
            arguments=arguments,
        )
        driver.synchronize()

        host_current_type = ctypes.c_float * shape["n_neurons"]
        host_action_type = ctypes.c_uint32 * shape["n_neurons"]
        host_current = host_current_type()
        host_action = host_action_type()
        driver.copy_device_to_host(host_current, out_current)
        driver.copy_device_to_host(host_action, out_action)

        result: dict[str, object] = {
            "classification": "PLAYGROUND_CUDA1_SINGLE_TICK_EXECUTION",
            "scientific_evidence": False,
            "execution_status": "GPU_KERNEL_EXECUTED",
            "kernel": str(_kernel_abi(bundle).get("entry", "pan_gate_kernel")),
            "device_ordinal": device_ordinal,
            "launch": {
                "grid": [grid_x, 1, 1],
                "block": [block_size, 1, 1],
                "n_neurons": shape["n_neurons"],
                "tick": inputs.tick,
            },
            "outputs": {
                "current": [float(value) for value in host_current],
                "action": [int(value) for value in host_action],
            },
            "ptxas": report.to_mapping(),
            "comparison_scope": "GATE_OUTPUT_ONLY_NOT_FULL_SNN",
            "full_snn_parity_verified": False,
            "canonical_cuda_backend": False,
        }
        while allocations:
            allocation = allocations[-1]
            driver.free_device(allocation)
            allocations.pop()
        memory_after_free, memory_total_after = driver.memory_info()
        result["memory"] = {
            "free_before_bytes": memory_before_free,
            "free_after_bytes": memory_after_free,
            "total_before_bytes": memory_total,
            "total_after_bytes": memory_total_after,
            "free_delta_bytes": memory_after_free - memory_before_free,
            "allocations_released": True,
        }
        return result
    finally:
        for allocation in reversed(allocations):
            try:
                driver.free_device(allocation)
            except CudaDriverError:
                pass
        driver.unload(loaded)


def parity_contract() -> dict[str, object]:
    """Return the canonical parity criteria with Playground compatibility metadata."""

    canonical = default_parity_contract().to_mapping()
    raw_classes = canonical["classes"]
    if not isinstance(raw_classes, dict):
        raise RuntimeError("canonical parity classes are invalid")
    classes = {
        key: dict(value) if isinstance(value, Mapping) else {}
        for key, value in raw_classes.items()
    }
    classes["D1"].update(
        {
            "name": "exact_event_parity",
            "spike_train": "BIT_IDENTICAL_NEURON_ID_TICK",
            "target_stage": "LATER_STRICT_TARGET",
        }
    )
    classes["D2"].update(
        {
            "name": "numerical_state_parity",
            "target_stage": "CUDA_1_PRIMARY_TARGET",
        }
    )
    classes["D3"].update(
        {
            "name": "behavioral_metric_parity",
            "target_stage": "CLOSED_LOOP_AND_PLASTICITY",
        }
    )
    return {
        "classification": "PLAYGROUND_CUDA_PARITY_CONTRACT",
        "scientific_evidence": False,
        "reference_source": "CPU_PYTHON_PLAYGROUND",
        "contract_version": canonical["version"],
        "classes": classes,
        "freeze_modes": {
            "actions": (
                "Replay the CPU reference action sequence; do not select new actions."
            ),
            "rewards": (
                "Replay the CPU reference reward sequence; do not recompute environment "
                "reward."
            ),
        },
    }


def _deterministic_projection(result: Mapping[str, object]) -> dict[str, object]:
    """Extract only replay-relevant CPU state from a Playground result."""

    monitors = result.get("monitors")
    metrics = result.get("metrics")
    topology = result.get("topology")
    closed_loop = result.get("closed_loop")
    behavioral = result.get("behavioral_learning")

    monitor_map = monitors if isinstance(monitors, Mapping) else {}
    metric_map = metrics if isinstance(metrics, Mapping) else {}
    topology_map = topology if isinstance(topology, Mapping) else {}
    loop_map = closed_loop if isinstance(closed_loop, Mapping) else {}
    behavior_map = behavioral if isinstance(behavioral, Mapping) else {}

    return {
        "config": result.get("config"),
        "model": result.get("model"),
        "topology": {
            "name": topology_map.get("name"),
            "dimensions": topology_map.get("dimensions"),
            "neuron_count": topology_map.get("neuron_count"),
            "edge_count": topology_map.get("edge_count"),
            "coordinates": topology_map.get("coordinates"),
            "edges": topology_map.get("edges"),
        },
        "metrics": {
            "total_spikes": metric_map.get("total_spikes"),
            "mean_rate_hz": metric_map.get("mean_rate_hz"),
            "active_neurons": metric_map.get("active_neurons"),
            "active_fraction": metric_map.get("active_fraction"),
            "weight_mean": metric_map.get("weight_mean"),
            "weight_min": metric_map.get("weight_min"),
            "weight_max": metric_map.get("weight_max"),
            "delay_mean_ticks": metric_map.get("delay_mean_ticks"),
        },
        "monitors": {
            "spikes": monitor_map.get("spikes"),
            "rates_hz": monitor_map.get("rates_hz"),
            "tick_spike_counts": monitor_map.get("tick_spike_counts"),
            "state_samples": monitor_map.get("state_samples"),
        },
        "readout": result.get("readout"),
        "closed_loop": {
            "action_history": loop_map.get("action_history"),
            "target_history": loop_map.get("target_history"),
            "reward_history": loop_map.get("reward_history"),
            "successes": loop_map.get("successes"),
            "success_fraction": loop_map.get("success_fraction"),
        },
        "behavioral_learning": {
            "policy": behavior_map.get("policy"),
            "activity": behavior_map.get("activity"),
            "action_history": behavior_map.get("action_history"),
            "target_history": behavior_map.get("target_history"),
            "reward_history": behavior_map.get("reward_history"),
            "policy_updates": behavior_map.get("policy_updates"),
            "external_reward_updates": behavior_map.get("external_reward_updates"),
            "success_fraction": behavior_map.get("success_fraction"),
        },
        "pan": result.get("pan"),
        "execution": result.get("execution"),
    }


def cpu_determinism_fingerprint(result: Mapping[str, object]) -> str:
    """Hash a canonical CPU replay projection, excluding timestamps/runtime."""

    payload = json.dumps(
        _deterministic_projection(result),
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def cpu_determinism_summary(
    first: Mapping[str, object],
    second: Mapping[str, object],
) -> dict[str, object]:
    """Check exact replay determinism of two same-seed CPU Playground runs."""

    first_projection = _deterministic_projection(first)
    second_projection = _deterministic_projection(second)
    first_hash = cpu_determinism_fingerprint(first)
    second_hash = cpu_determinism_fingerprint(second)

    first_monitors = first_projection["monitors"]
    second_monitors = second_projection["monitors"]
    assert isinstance(first_monitors, Mapping)
    assert isinstance(second_monitors, Mapping)

    spike_train_exact = first_monitors.get("spikes") == second_monitors.get("spikes")
    return {
        "classification": "PLAYGROUND_CPU_DETERMINISM",
        "scientific_evidence": False,
        "reference_role": "CUDA_1_CPU_REFERENCE",
        "same_seed_required": True,
        "wall_clock_excluded": True,
        "session_identity_excluded": True,
        "spike_train_exact": spike_train_exact,
        "fingerprint_first": first_hash,
        "fingerprint_second": second_hash,
        "projection_exact": first_projection == second_projection,
        "passed": spike_train_exact and first_hash == second_hash,
    }


def exact_spike_parity_summary(
    reference: Sequence[object],
    candidate: Sequence[object],
    *,
    reference_commit: str = "",
) -> dict[str, object]:
    """Compatibility wrapper around canonical D1 exact event parity."""

    result = exact_spike_parity(reference, candidate, require_non_empty=False)
    return {
        "classification": "PLAYGROUND_CUDA_SPIKE_PARITY",
        "scientific_evidence": False,
        "parity_class": "D1",
        "reference_source": "CPU_PYTHON_PLAYGROUND",
        "reference_frozen_at": reference_commit or "UNSPECIFIED",
        "allowed_spike_mismatches": result.details["allowed_spike_mismatches"],
        "spike_mismatches": result.details["spike_mismatches"],
        "passed": result.passed,
    }


def behavioral_parity_summary(
    *,
    reference_spike_count: int,
    candidate_spike_count: int,
    reference_success_fraction: float,
    candidate_success_fraction: float,
    reference_commit: str = "",
) -> dict[str, object]:
    """Compatibility wrapper around canonical D3 metric parity."""

    result = metric_behavior_parity(
        reference_spike_count=reference_spike_count,
        candidate_spike_count=candidate_spike_count,
        reference_success_fraction=reference_success_fraction,
        candidate_success_fraction=candidate_success_fraction,
    )
    return {
        "classification": "PLAYGROUND_CUDA_BEHAVIORAL_PARITY",
        "scientific_evidence": False,
        "parity_class": "D3",
        "reference_source": "CPU_PYTHON_PLAYGROUND",
        "reference_frozen_at": reference_commit or "UNSPECIFIED",
        **dict(result.details),
        "passed": result.passed,
    }


def max_abs_error(reference: Sequence[float], candidate: Sequence[float]) -> float:
    """Compatibility wrapper around canonical fail-closed D2 comparison."""

    return canonical_max_abs_error(reference, candidate)


def gate_parity_summary(
    reference: Sequence[float],
    candidate: Sequence[float],
    *,
    tolerance: float = 1.0e-4,
    reference_commit: str = "",
) -> dict[str, object]:
    """Summarize D2 gate parity without claiming full SNN equivalence."""

    failure_reason: str | None = None
    error: float | None
    try:
        error = max_abs_error(reference, candidate)
    except ValueError as exc:
        error = None
        failure_reason = str(exc)
    return {
        "classification": "PLAYGROUND_CUDA_GATE_PARITY",
        "scientific_evidence": False,
        "comparison_scope": "GATE_OUTPUT_ONLY_NOT_FULL_SNN",
        "parity_class": "D2",
        "gates_compared": ["A1", "A2", "A3", "A4", "B1", "C1", "C2", "D1"],
        "gates_not_compared": ["C4", "C2_FEEDBACK_TOPOLOGY_STATE"],
        "excluded_by_design": [
            "later_weight_updates",
            "full_recurrent_snn_state",
            "structural_growth",
        ],
        "reference_source": "CPU_PYTHON_PLAYGROUND",
        "reference_frozen_at": reference_commit or "UNSPECIFIED",
        "max_abs_error": error,
        "tolerance": tolerance,
        "failure_reason": failure_reason,
        "passed": (failure_reason is None and error is not None and error <= tolerance),
    }
