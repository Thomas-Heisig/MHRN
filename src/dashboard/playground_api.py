"""Dashboard adapter for the isolated non-canonical Playground."""

from __future__ import annotations

import shutil
import threading
import time
from collections import deque
from collections.abc import Callable, Mapping
from typing import cast

from src.playground import service
from src.playground.cuda import (
    CompileBundle,
    CudaDriver,
    CudaDriverError,
    CudaRuntimeUnavailable,
    GateLaunchInputs,
    compile_mapping,
    cpu_gate_reference,
    execute_gate_bundle,
    gate_execution_parity_summary,
    preflight_bundle,
    validate_cuda_block_size,
)
from src.playground.models import PlaygroundConfig
from src.playground.night_run import NightRunManager
from src.playground.pan import PANEmbodiedSandboxSession, PANSessionDaemon

_MAX_CONCURRENT_RUNS = 2
_RUNS_PER_MINUTE = 20
_RUN_WINDOW_SECONDS = 60.0

_RUN_SEMAPHORE = threading.BoundedSemaphore(_MAX_CONCURRENT_RUNS)
_RATE_LOCK = threading.Lock()
_RECENT_RUNS: deque[float] = deque()


def _payload_int(
    payload: Mapping[str, object],
    name: str,
    default: int,
) -> int:
    value = payload.get(name, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    converted = int(value)
    if float(value) != float(converted):
        raise ValueError(f"{name} must be an integer")
    return converted


def _payload_float(
    payload: Mapping[str, object],
    name: str,
    default: float,
) -> float:
    value = payload.get(name, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    return float(value)


def _payload_text(
    payload: Mapping[str, object],
    name: str,
    default: str,
) -> str:
    value = payload.get(name, default)
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    return value


def _numeric_list(value: object, name: str) -> list[float]:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")
    items = cast(list[object], value)
    result: list[float] = []
    for item in items:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise ValueError(f"{name} entries must be numeric")
        result.append(float(item))
    return result


_LIVE_DAEMON = PANSessionDaemon()
_LIVE_SANDBOXES: dict[str, PANEmbodiedSandboxSession] = {}
_LIVE_LOCK = threading.RLock()
_NIGHT_RUN = NightRunManager()


class PlaygroundRateLimitError(RuntimeError):
    """Raised when the bounded Playground API rate is exceeded."""


class PlaygroundBusyError(RuntimeError):
    """Raised when all bounded Playground worker slots are occupied."""


def _reserve_rate_slot() -> None:
    now = time.monotonic()
    with _RATE_LOCK:
        cutoff = now - _RUN_WINDOW_SECONDS
        while _RECENT_RUNS and _RECENT_RUNS[0] < cutoff:
            _RECENT_RUNS.popleft()
        if len(_RECENT_RUNS) >= _RUNS_PER_MINUTE:
            raise PlaygroundRateLimitError(
                "Playground run rate exceeded; retry after the current minute window."
            )
        _RECENT_RUNS.append(now)


def _bounded_operation(
    operation: Callable[[], dict[str, object]],
) -> dict[str, object]:
    _reserve_rate_slot()
    if not _RUN_SEMAPHORE.acquire(blocking=False):
        raise PlaygroundBusyError(
            "Playground is busy; at most two simulation requests run concurrently."
        )
    try:
        return operation()
    finally:
        _RUN_SEMAPHORE.release()


def _bounded_run(path: str, payload: Mapping[str, object]) -> dict[str, object]:
    def operation() -> dict[str, object]:
        if path == "/api/playground/run":
            return service.run(payload)
        if path == "/api/playground/robustness":
            return service.robustness(payload)
        raise ValueError(f"unknown Playground POST route: {path}")

    return _bounded_operation(operation)


def _live_parts(path: str) -> list[str]:
    prefix = "/api/playground/live/"
    if not path.startswith(prefix):
        return []
    return [part for part in path[len(prefix) :].split("/") if part]


def _cuda_runtime_status() -> dict[str, object]:
    ptxas_path = shutil.which("ptxas")
    driver_available = False
    driver_error: str | None = None
    try:
        driver = CudaDriver()
        driver.initialize()
        driver_available = True
    except (CudaRuntimeUnavailable, CudaDriverError, OSError) as exc:
        driver_error = str(exc)

    return {
        "classification": "PLAYGROUND_CUDA_DIAGNOSTICS_STATUS",
        "scientific_evidence": False,
        "canonical_cuda_backend": False,
        "target_default": "sm_86",
        "ptxas_available": ptxas_path is not None,
        "ptxas_path": ptxas_path,
        "cuda_driver_available": driver_available,
        "cuda_driver_error": driver_error,
        "stages": {
            "CUDA-1.0": "PTXAS_LOAD_PREFLIGHT_IMPLEMENTED",
            "CUDA-1.1": "DETERMINISM_FREEZE_PARITY_CONTRACT_IMPLEMENTED",
            "CUDA-1.2": "LAUNCH_ABI_BUFFER_VALIDATION_IMPLEMENTED",
            "CUDA-1.3": "CPU_GATE_REFERENCE_D2_IMPLEMENTED_HARDWARE_VERIFICATION_REQUIRED",
            "CUDA-1.4": "PENDING_10_100_TICK_STATE_DELAYS_MULTIBLOCK",
            "CUDA-1.5": "PENDING_PLASTICITY_STDP",
            "CUDA-1.6": "PENDING_CLOSED_LOOP_SANDBOX_GPU",
        },
        "application_cpu": {
            "sandbox_physics": True,
            "sensorics": True,
            "actuation": True,
            "posture_analysis": True,
            "reward_triggers": True,
            "closed_loop": True,
        },
        "gpu_porting": {
            "gate_single_tick": True,
            "membrane_state_100_ticks": False,
            "adaptation_state": False,
            "refractory_state": False,
            "synapses": False,
            "delays": False,
            "plasticity": False,
            "sandbox_physics": False,
        },
        "verification": {
            "cpu_gate_reference": True,
            "single_tick_d2_endpoint": True,
            "rng_action_path_endpoint": True,
            "raw_rng_value_parity": True,
            "memory_leak_instrumentation": True,
        },
    }


def _diagnostic_inputs(
    bundle: CompileBundle,
    *,
    n_neurons: int,
    seed: int,
    epsilon: float,
) -> GateLaunchInputs:
    manifest = bundle.manifest
    raw_abi = manifest.get("kernel_abi")
    if not isinstance(raw_abi, Mapping):
        raise ValueError("compile bundle is missing kernel_abi")
    abi = cast(Mapping[str, object], raw_abi)
    input_channels = _payload_int(abi, "input_channels", 8)
    action_count = _payload_int(abi, "action_space_size", 4)
    pan_dimensions = _payload_int(abi, "pan_dimensions", 5)
    full_mask = (1 << input_channels) - 1 if input_channels < 64 else 0xFFFFFFFFFFFFFFFF
    logits: list[float] = []
    for neuron in range(n_neurons):
        preferred = neuron % action_count
        for action in range(action_count):
            logits.append(1.0 if action == preferred else 0.05 * (action + 1))
    return GateLaunchInputs.from_sequences(
        input_current=[1.0 + 0.125 * (index % 7) for index in range(n_neurons)],
        channel_masks=[full_mask] * n_neurons,
        amplitudes=[1.0 + 0.05 * channel for channel in range(input_channels)],
        reward_ring=[0.5, -0.25, 0.75, 0.0],
        action_map=[
            0.1 * (action + 1) * (channel + 1)
            for action in range(action_count)
            for channel in range(input_channels)
        ],
        feedback_matrix=[
            0.01 * (1 + ((neuron + dimension) % 5))
            for neuron in range(n_neurons)
            for dimension in range(pan_dimensions)
        ],
        population=[0.1 * (dimension + 1) for dimension in range(pan_dimensions)],
        logits=logits,
        tick=3,
        target_index=min(2, action_count - 1),
        previous_action=min(1, action_count - 1),
        seed=seed,
        epsilon=epsilon,
    )


def _cuda_config_payload(payload: Mapping[str, object]) -> dict[str, object]:
    excluded = {
        "target_sm",
        "ptx_version",
        "n_neurons",
        "block_size",
        "device_ordinal",
        "reference_commit",
        "rng_samples",
    }
    return {key: value for key, value in payload.items() if key not in excluded}


def _cuda_preflight(payload: Mapping[str, object]) -> dict[str, object]:
    target_sm = _payload_text(payload, "target_sm", "sm_86")
    ptx_version = _payload_text(payload, "ptx_version", "7.1")
    n_neurons = _payload_int(payload, "n_neurons", 256)
    block_size = validate_cuda_block_size(_payload_int(payload, "block_size", 64))
    device_ordinal = _payload_int(payload, "device_ordinal", 0)
    if not 1 <= n_neurons <= 12_288:
        raise ValueError("n_neurons must be in [1, 12288]")
    bundle = compile_mapping(
        _cuda_config_payload(payload),
        target_sm=target_sm,
        ptx_version=ptx_version,
    )
    return preflight_bundle(
        bundle,
        n_neurons=n_neurons,
        block_size=block_size,
        device_ordinal=device_ordinal,
    )


def _cuda_smoke(payload: Mapping[str, object]) -> dict[str, object]:
    target_sm = _payload_text(payload, "target_sm", "sm_86")
    ptx_version = _payload_text(payload, "ptx_version", "7.1")
    n_neurons = _payload_int(payload, "n_neurons", 64)
    block_size = validate_cuda_block_size(_payload_int(payload, "block_size", 64))
    device_ordinal = _payload_int(payload, "device_ordinal", 0)
    reference_commit = _payload_text(payload, "reference_commit", "")
    if not 1 <= n_neurons <= 4096:
        raise ValueError("n_neurons must be in [1, 4096] for hardware smoke")
    bundle = compile_mapping(
        _cuda_config_payload(payload),
        target_sm=target_sm,
        ptx_version=ptx_version,
    )
    inputs = _diagnostic_inputs(
        bundle,
        n_neurons=n_neurons,
        seed=12345,
        epsilon=0.0,
    )
    reference = cpu_gate_reference(bundle, inputs)
    first = execute_gate_bundle(
        bundle,
        inputs,
        block_size=block_size,
        device_ordinal=device_ordinal,
    )
    second = execute_gate_bundle(
        bundle,
        inputs,
        block_size=block_size,
        device_ordinal=device_ordinal,
    )
    first_parity = gate_execution_parity_summary(
        reference,
        first,
        tolerance=1.0e-5,
        reference_commit=reference_commit,
    )
    second_parity = gate_execution_parity_summary(
        reference,
        second,
        tolerance=1.0e-5,
        reference_commit=reference_commit,
    )
    deterministic = first.get("outputs") == second.get("outputs")
    return {
        "classification": "PLAYGROUND_CUDA1_3_HARDWARE_SMOKE",
        "scientific_evidence": False,
        "canonical_cuda_backend": False,
        "reference": reference,
        "first": first,
        "second": second,
        "parity": first_parity,
        "second_parity": second_parity,
        "gpu_repeat_exact": deterministic,
        "passed": bool(first_parity["passed"])
        and bool(second_parity["passed"])
        and deterministic,
        "cleanup_contract": {
            "device_allocations_released_in_finally": True,
            "driver_module_unloaded": True,
            "memory_leak_instrumented": True,
            "first_memory": first.get("memory"),
            "second_memory": second.get("memory"),
        },
    }


def _cuda_rng_parity(payload: Mapping[str, object]) -> dict[str, object]:
    target_sm = _payload_text(payload, "target_sm", "sm_86")
    ptx_version = _payload_text(payload, "ptx_version", "7.1")
    samples = _payload_int(payload, "rng_samples", 1000)
    block_size = validate_cuda_block_size(_payload_int(payload, "block_size", 64))
    device_ordinal = _payload_int(payload, "device_ordinal", 0)
    if not 1 <= samples <= 4096:
        raise ValueError("rng_samples must be in [1, 4096]")
    bundle = compile_mapping(
        _cuda_config_payload(payload),
        target_sm=target_sm,
        ptx_version=ptx_version,
    )
    inputs = _diagnostic_inputs(
        bundle,
        n_neurons=samples,
        seed=12345,
        epsilon=1.0,
    )
    reference = cpu_gate_reference(bundle, inputs)
    candidate = execute_gate_bundle(
        bundle,
        inputs,
        block_size=block_size,
        device_ordinal=device_ordinal,
    )
    reference_outputs = cast(Mapping[str, object], reference["outputs"])
    candidate_outputs = cast(Mapping[str, object], candidate["outputs"])
    reference_actions = cast(list[int], reference_outputs["action"])
    candidate_actions = cast(list[int], candidate_outputs["action"])
    actions_exact = reference_actions == candidate_actions
    return {
        "classification": "PLAYGROUND_CUDA_RNG_ACTION_PATH_PARITY",
        "scientific_evidence": False,
        "samples": samples,
        "seed": 12345,
        "tick": inputs.tick,
        "epsilon": 1.0,
        "actions_exact": actions_exact,
        "passed": actions_exact,
        "first_reference_actions": reference_actions[:20],
        "first_cuda_actions": candidate_actions[:20],
        "scope": "HASH_EPSILON_GREEDY_ACTION_PATH_UINT24_TO_F32_HALF_OPEN",
    }


def get_playground(path: str) -> dict[str, object] | None:
    if path == "/api/playground/catalog":
        return service.catalog()
    if path == "/api/playground/sessions":
        return service.sessions()
    if path.startswith("/api/playground/sessions/"):
        session_id = path[len("/api/playground/sessions/") :]
        return service.replay(session_id)
    if path == "/api/playground/night":
        return _NIGHT_RUN.status()
    if path == "/api/playground/cuda/status":
        return _cuda_runtime_status()
    if path == "/api/playground/live":
        return {
            "class": "PLAYGROUND_LIVE_SESSIONS",
            "scientific_evidence": False,
            "sessions": _LIVE_DAEMON.list(),
        }
    parts = _live_parts(path)
    if len(parts) == 1:
        return {"session_id": parts[0], **_LIVE_DAEMON.get(parts[0]).snapshot()}
    return None


def post_playground(
    path: str, payload: Mapping[str, object]
) -> dict[str, object] | None:
    if path in {"/api/playground/run", "/api/playground/robustness"}:
        return _bounded_run(path, payload)

    if path == "/api/playground/determinism":
        return service.determinism(payload)

    if path == "/api/playground/cuda/compile":
        target_sm = _payload_text(payload, "target_sm", "sm_86")
        ptx_version = _payload_text(payload, "ptx_version", "7.1")
        config_payload = dict(payload)
        config_payload.pop("target_sm", None)
        config_payload.pop("ptx_version", None)
        return compile_mapping(
            config_payload,
            target_sm=target_sm,
            ptx_version=ptx_version,
        ).to_mapping()

    if path == "/api/playground/cuda/preflight":
        return _bounded_operation(lambda: _cuda_preflight(payload))

    if path == "/api/playground/cuda/smoke":
        return _bounded_operation(lambda: _cuda_smoke(payload))

    if path == "/api/playground/cuda/rng-parity":
        return _bounded_operation(lambda: _cuda_rng_parity(payload))

    if path == "/api/playground/night/start":
        return _NIGHT_RUN.start(
            hours=_payload_float(payload, "hours", 8.0),
            max_episodes=_payload_int(payload, "max_episodes", 10_000),
            checkpoint_seconds=_payload_float(payload, "checkpoint_seconds", 600.0),
            seed=_payload_int(payload, "seed", 12345),
        )
    if path == "/api/playground/night/stop":
        return _NIGHT_RUN.stop()

    if path == "/api/playground/live/stop-all":
        with _LIVE_LOCK:
            _LIVE_SANDBOXES.clear()
        return _LIVE_DAEMON.stop_all()

    if path == "/api/playground/live/create":
        config_payload = dict(payload)
        config_payload.setdefault("neuron_model", "pan_adex_5d")
        config_payload.setdefault("pan_enabled", True)
        config_payload.setdefault("thalamic_relay_threshold", 0.0)
        config_payload.setdefault("pan_bias_current", 10.0)
        config_payload.setdefault("behavior_target_mode", "cycle")
        config = PlaygroundConfig.from_mapping(config_payload)
        session_id = _LIVE_DAEMON.create(config)
        with _LIVE_LOCK:
            _LIVE_SANDBOXES[session_id] = PANEmbodiedSandboxSession(
                _LIVE_DAEMON.get(session_id)
            )
        return {
            "class": "PLAYGROUND_LIVE_SESSION",
            "scientific_evidence": False,
            "session_id": session_id,
            "state": _LIVE_DAEMON.get(session_id).snapshot(),
        }

    parts = _live_parts(path)
    if len(parts) >= 2:
        session_id, action = parts[0], parts[1]
        session = _LIVE_DAEMON.get(session_id)
        if action == "step":
            ticks = _payload_int(payload, "ticks", 32)
            return {"session_id": session_id, **session.step(ticks)}
        if action == "input":
            values = _numeric_list(payload.get("values", []), "values")
            duration = _payload_int(payload, "duration_ticks", 16)
            gain = _payload_float(payload, "gain", 25.0)
            session.inject_vector(values, duration_ticks=duration, gain=gain)
            return {"session_id": session_id, "accepted": True}
        if action == "strategy":
            context = _payload_text(payload, "context", "default")
            options = _payload_int(payload, "action_count", 4)
            chosen = session.choose_strategy(context, options)
            return {
                "session_id": session_id,
                "classification": "PLAYGROUND_META_STRATEGY",
                "scientific_evidence": False,
                "context": context,
                "action": chosen,
                "action_count": options,
            }
        if action == "reward":
            context = _payload_text(payload, "context", "default")
            chosen = _payload_int(payload, "action", 0)
            action_count = _payload_int(payload, "action_count", 4)
            reward = _payload_float(payload, "reward", 0.0)
            return {
                "session_id": session_id,
                **session.apply_strategy_reward(
                    context=context,
                    action=chosen,
                    reward=reward,
                    action_count=action_count,
                ),
            }
        if action == "sandbox":
            with _LIVE_LOCK:
                sandbox = _LIVE_SANDBOXES.get(session_id)
                if sandbox is None:
                    sandbox = PANEmbodiedSandboxSession(session)
                    _LIVE_SANDBOXES[session_id] = sandbox
            ticks = _payload_int(payload, "ticks", 1)
            return {"session_id": session_id, **sandbox.step(ticks)}
        if action == "stop":
            with _LIVE_LOCK:
                _LIVE_SANDBOXES.pop(session_id, None)
            return {"session_id": session_id, **_LIVE_DAEMON.stop(session_id)}
    return None
