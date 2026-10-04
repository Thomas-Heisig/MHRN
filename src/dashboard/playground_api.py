"""Dashboard adapter for the isolated non-canonical Playground."""

from __future__ import annotations

import csv
import hashlib
import hmac
import io
import json
import os
import re
import shutil
import subprocess
import threading
import time
import uuid
from collections import deque
from collections.abc import Callable, Mapping
from dataclasses import replace
from datetime import datetime, timezone
from http import HTTPStatus
from pathlib import Path
from typing import cast

from src.dashboard.verification import (
    SCIENTIFIC_PATHS,
    TEST_PATHS,
    current_git_head,
    inspect_source_tree,
)
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
from src.playground.cuda.builder_parity import run_builder_parity
from src.playground.cuda.recurrent import (
    cpu_recurrent_reference,
    execute_recurrent,
    recurrent_fixture,
    recurrent_parity,
)
from src.playground.cuda.synapses import SynapseConfig
from src.playground.integration import integration_catalog, transfer_element
from src.playground.models import PlaygroundConfig
from src.playground.night_run import NightRunManager
from src.playground.pan import PANEmbodiedSandboxSession, PANSessionDaemon
from src.playground.pan.cue_controls import run_cue_controls
from src.playground.pan.transfer import run_synaptic_transfer

_MAX_CONCURRENT_RUNS = 2
_RUNS_PER_MINUTE = 20
_RUN_WINDOW_SECONDS = 60.0
_CUDA_DIAGNOSTIC_ID = re.compile(r"[0-9a-f]{32}")
_CUDA_DIAGNOSTIC_MAX_BYTES = 8 * 1024 * 1024
_REPO_ROOT = Path(__file__).resolve().parents[2]
_CUDA_DIAGNOSTIC_URL_PREFIX = "/api/playground/cuda/diagnostics/"

_RUN_SEMAPHORE = threading.BoundedSemaphore(_MAX_CONCURRENT_RUNS)
_RATE_LOCK = threading.Lock()
_RECENT_RUNS: deque[float] = deque()


def _canonical_artifact_bytes(artifact: Mapping[str, object]) -> bytes:
    return json.dumps(
        artifact, sort_keys=True, ensure_ascii=True, separators=(",", ":")
    ).encode("utf-8")


def _write_cuda_diagnostic_artifact(
    repo_root: Path, artifact: Mapping[str, object]
) -> tuple[Path, str]:
    artifact_id = artifact.get("artifact_id")
    if not isinstance(artifact_id, str) or not _CUDA_DIAGNOSTIC_ID.fullmatch(
        artifact_id
    ):
        raise ValueError("CUDA diagnostic artifact ID is invalid")

    directory = repo_root / "artifacts" / "cuda_diagnostics"
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name != "nt":
        directory.chmod(0o700)
    record = dict(artifact)
    artifact_digest = hashlib.sha256(_canonical_artifact_bytes(record)).hexdigest()
    record["artifact_sha256"] = artifact_digest
    serialized = json.dumps(record, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    encoded = serialized.encode("utf-8")
    if len(encoded) > _CUDA_DIAGNOSTIC_MAX_BYTES:
        raise ValueError("CUDA diagnostic artifact exceeds the 8 MiB limit")

    destination = directory / f"{artifact_id}.json"
    temporary = directory / f".{artifact_id}.{uuid.uuid4().hex}.tmp"
    try:
        temporary.write_bytes(encoded)
        if os.name != "nt":
            temporary.chmod(0o600)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination, artifact_digest


def _load_cuda_diagnostic_artifact(
    repo_root: Path, artifact_id: str
) -> dict[str, object]:
    if not _CUDA_DIAGNOSTIC_ID.fullmatch(artifact_id):
        raise ValueError("CUDA diagnostic artifact ID is invalid")
    path = repo_root / "artifacts" / "cuda_diagnostics" / f"{artifact_id}.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("CUDA diagnostic artifact is malformed")
    record = dict(cast(dict[str, object], value))
    if record.get("artifact_id") != artifact_id:
        raise ValueError("CUDA diagnostic artifact is malformed")
    recorded_digest = record.pop("artifact_sha256", None)
    actual_digest = hashlib.sha256(_canonical_artifact_bytes(record)).hexdigest()
    if not isinstance(recorded_digest, str) or not hmac.compare_digest(
        recorded_digest, actual_digest
    ):
        raise ValueError("CUDA diagnostic artifact digest mismatch")
    record["artifact_sha256"] = recorded_digest
    return record


def _cuda_hardware_identity(device_ordinal: int) -> dict[str, object]:
    executable = shutil.which("nvidia-smi")
    if executable is None:
        return {
            "status": "unavailable",
            "source": "nvidia-smi",
            "device_ordinal": device_ordinal,
            "reason": "nvidia-smi_not_found",
        }
    try:
        completed = subprocess.run(
            [
                executable,
                "--query-gpu=index,name,uuid,pci.bus_id,driver_version",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            check=False,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {
            "status": "unavailable",
            "source": "nvidia-smi",
            "device_ordinal": device_ordinal,
            "reason": type(exc).__name__,
        }
    if completed.returncode != 0:
        return {
            "status": "unavailable",
            "source": "nvidia-smi",
            "device_ordinal": device_ordinal,
            "reason": "query_failed",
        }

    rows = [
        [value.strip() for value in row]
        for row in csv.reader(io.StringIO(completed.stdout), skipinitialspace=True)
        if row
    ]
    selector = os.environ.get("CUDA_VISIBLE_DEVICES")
    visible = selector.split(",") if selector is not None else None
    if visible is not None:
        if device_ordinal >= len(visible):
            return {
                "status": "unavailable",
                "source": "nvidia-smi",
                "device_ordinal": device_ordinal,
                "reason": "device_not_visible",
            }
        selected = visible[device_ordinal].strip()
        if selected.isdecimal():
            match = next((row for row in rows if row[0] == selected), None)
        elif selected.startswith("GPU-"):
            match = next(
                (row for row in rows if len(row) > 2 and row[2] == selected), None
            )
        else:
            match = None
    else:
        match = next((row for row in rows if row[0] == str(device_ordinal)), None)

    if match is None or len(match) < 5 or match[2] in {"", "N/A"}:
        return {
            "status": "unavailable",
            "source": "nvidia-smi",
            "device_ordinal": device_ordinal,
            "reason": "device_identity_unresolved",
        }
    return {
        "status": "captured",
        "source": "nvidia-smi",
        "device_ordinal": device_ordinal,
        "physical_index": match[0],
        "model": match[1],
        "device_uuid_sha256": hashlib.sha256(match[2].encode("utf-8")).hexdigest(),
        "pci_bus_id": match[3],
        "driver_version": match[4],
    }


def _working_tree_provenance(repo_root: Path) -> dict[str, object]:
    try:
        inspection = inspect_source_tree(repo_root)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return {
            "git_commit": current_git_head(repo_root),
            "working_tree_digest": None,
            "working_tree_digest_status": type(exc).__name__,
            "working_tree_digest_scope": [*SCIENTIFIC_PATHS, *TEST_PATHS],
        }
    dirty = bool(
        inspection.dirty_relevant_paths
        or inspection.untracked_relevant_paths
        or inspection.missing_relevant_paths
    )
    return {
        "git_commit": current_git_head(repo_root),
        "working_tree_digest": inspection.digest,
        "working_tree_digest_status": (
            "captured" if inspection.digest else "unavailable"
        ),
        "working_tree_state": (
            "unknown"
            if not inspection.git_available
            else "modified" if dirty else "clean"
        ),
        "working_tree_digest_scope": [*SCIENTIFIC_PATHS, *TEST_PATHS],
        "dirty_relevant_paths": list(inspection.dirty_relevant_paths),
        "untracked_relevant_paths": list(inspection.untracked_relevant_paths),
        "missing_relevant_paths": list(inspection.missing_relevant_paths),
    }


def _diagnostic_outcome(result: Mapping[str, object]) -> str:
    passed = result.get("passed")
    if isinstance(passed, bool):
        return "passed" if passed else "failed"
    parity = result.get("parity")
    if isinstance(parity, Mapping):
        parity_passed = cast(Mapping[str, object], parity).get("passed")
        if isinstance(parity_passed, bool):
            return "passed" if parity_passed else "failed"
    actions_exact = result.get("actions_exact")
    if isinstance(actions_exact, bool):
        return "passed" if actions_exact else "failed"
    return "not_evaluated"


def _diagnostic_http_status(exc: Exception) -> int:
    if isinstance(exc, (ValueError, TypeError, json.JSONDecodeError)):
        return HTTPStatus.BAD_REQUEST
    if isinstance(exc, FileNotFoundError):
        return HTTPStatus.NOT_FOUND
    if isinstance(exc, TimeoutError):
        return HTTPStatus.GATEWAY_TIMEOUT
    if isinstance(exc, RuntimeError):
        return HTTPStatus.SERVICE_UNAVAILABLE
    return HTTPStatus.INTERNAL_SERVER_ERROR


def _run_cuda_diagnostic(
    route: str,
    payload: Mapping[str, object],
    operation: Callable[[], dict[str, object]],
    *,
    repo_root: Path | None = None,
) -> dict[str, object]:
    root = repo_root or _REPO_ROOT
    started = datetime.now(timezone.utc)
    artifact_id = uuid.uuid4().hex
    ordinal = payload.get("device_ordinal", 0)
    device_ordinal = (
        ordinal
        if isinstance(ordinal, int) and not isinstance(ordinal, bool) and ordinal >= 0
        else 0
    )
    provenance = _working_tree_provenance(root)
    hardware = _cuda_hardware_identity(device_ordinal)
    try:
        result = operation()
    except Exception as exc:
        completed = datetime.now(timezone.utc)
        record: dict[str, object] = {
            "schema_version": "mhrn.cuda-diagnostic.v1",
            "artifact_id": artifact_id,
            "route": route,
            "execution_status": "failed",
            "outcome": "error",
            "started_at": started.isoformat(),
            "completed_at": completed.isoformat(),
            "duration_seconds": (completed - started).total_seconds(),
            "request_sha256": hashlib.sha256(
                _canonical_artifact_bytes(payload)
            ).hexdigest(),
            "provenance": provenance,
            "hardware_identity": hardware,
            "error_type": type(exc).__name__,
            "error": str(exc)[:1000],
            "scientific_evidence": False,
        }
        _attach_cuda_diagnostic_receipt(exc, root, record)
        raise

    completed = datetime.now(timezone.utc)
    record = {
        "schema_version": "mhrn.cuda-diagnostic.v1",
        "artifact_id": artifact_id,
        "route": route,
        "execution_status": "completed",
        "outcome": _diagnostic_outcome(result),
        "started_at": started.isoformat(),
        "completed_at": completed.isoformat(),
        "duration_seconds": (completed - started).total_seconds(),
        "request_sha256": hashlib.sha256(
            _canonical_artifact_bytes(payload)
        ).hexdigest(),
        "provenance": provenance,
        "hardware_identity": hardware,
        "result": result,
        "scientific_evidence": False,
    }
    receipt = _attach_cuda_diagnostic_receipt(None, root, record)
    response = dict(result)
    response["run_evidence"] = receipt
    return response


def _attach_cuda_diagnostic_receipt(
    error: Exception | None,
    repo_root: Path,
    record: dict[str, object],
) -> dict[str, object]:
    artifact_id = cast(str, record["artifact_id"])
    receipt: dict[str, object] = {
        "artifact_id": artifact_id,
        "artifact_url": f"/api/playground/cuda/diagnostics/{artifact_id}",
        "execution_status": record["execution_status"],
        "outcome": record["outcome"],
        "started_at": record["started_at"],
        "completed_at": record["completed_at"],
        "duration_seconds": record["duration_seconds"],
        "provenance": record["provenance"],
        "hardware_identity": record["hardware_identity"],
    }
    record["artifact_url"] = receipt["artifact_url"]
    try:
        _, artifact_digest = _write_cuda_diagnostic_artifact(repo_root, record)
    except (OSError, TypeError, ValueError) as exc:
        receipt["persistence_status"] = "failed"
        receipt["persistence_error"] = type(exc).__name__
        receipt["artifact_url"] = None
    else:
        receipt["persistence_status"] = "persisted"
        receipt["artifact_sha256"] = artifact_digest
    if error is not None:
        setattr(error, "run_evidence", receipt)
        setattr(error, "run_http_status", _diagnostic_http_status(error))
    return receipt


def _bounded_cuda_diagnostic(
    route: str,
    payload: Mapping[str, object],
    operation: Callable[[], dict[str, object]],
) -> dict[str, object]:
    return _bounded_operation(lambda: _run_cuda_diagnostic(route, payload, operation))


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
        "provenance": {
            "git_commit": current_git_head(Path(__file__).resolve().parents[2]),
            "source": "runtime_repository_head",
            "working_tree_state": "not_captured",
        },
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
            "CUDA-1.4": "BOUNDED_RECURRENT_FP64_REFERENCE_IMPLEMENTED",
            "CUDA-1.5": "BOUNDED_FROZEN_REWARD_PLASTICITY_REFERENCE_IMPLEMENTED",
            "CUDA-1.6": "HYBRID_BUILDER_MEMBRANE_AND_OPTIONAL_PAN_STATE_GPU_BODY_CPU_IMPLEMENTED",
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
            "membrane_state_100_ticks": True,
            "adaptation_state": True,
            "pan_health_energy_hyperstate": "OPTIONAL_CUDA_PAN_BUILDER",
            "pan_apoptosis_decision": "OPTIONAL_CUDA_PAN_BUILDER",
            "pan_feedback_projection": "OPTIONAL_CUDA_PAN_BUILDER",
            "refractory_state": False,
            "synapses": "BUILDER_GPU_EMISSION_PLASTICITY_REWARD_RESIDENT_QUEUE_HOST_TRACE",
            "builder_rng_semantics": "HOST_TRAVERSAL_STREAM_PRESERVED",
            "builder_inhibitory_emission": True,
            "delays": True,
            "builder_delay_queue": "DEVICE_RESIDENT_RING_65",
            "builder_neuron_traces": "DEVICE_RESIDENT_TWO_PHASE",
            "builder_pan_population": "CUDA_ORDERED_AXIS_REDUCTION",
            "plasticity": "BUILDER_PAIR_TRIPLET_ELIGIBILITY_MODULATION_AND_BOUNDED_REFERENCE",
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


def _cuda_recurrent_parity(payload: Mapping[str, object]) -> dict[str, object]:
    block_size = validate_cuda_block_size(_payload_int(payload, "block_size", 64))
    inputs = recurrent_fixture(
        n_neurons=_payload_int(payload, "n_neurons", 129),
        ticks=_payload_int(payload, "ticks", 100),
        model=_payload_text(payload, "model", "pan_adex_5d"),
    )
    plasticity = payload.get("plasticity", False)
    if not isinstance(plasticity, bool):
        raise ValueError("plasticity must be boolean")
    if plasticity:
        inputs = replace(
            inputs,
            synapses=SynapseConfig(),
            rewards=tuple(
                1.0 if tick % 32 == 0 else 0.0 for tick in range(inputs.ticks)
            ),
        )
    reference = cpu_recurrent_reference(inputs)
    candidate = execute_recurrent(
        inputs,
        block_size=block_size,
        target_sm=_payload_text(payload, "target_sm", "sm_86"),
    )
    return {
        "classification": (
            "PLAYGROUND_CUDA15_PLASTICITY_PARITY"
            if plasticity
            else "PLAYGROUND_CUDA14_RECURRENT_PARITY"
        ),
        "scientific_evidence": False,
        "model": inputs.model,
        "ticks": inputs.ticks,
        "state_dtype": candidate["state_dtype"],
        "preflight": candidate["preflight"],
        "parity": recurrent_parity(
            reference, cast(dict[str, object], candidate["outputs"])
        ),
        "scope": candidate["comparison_scope"],
        "full_pan_backend": False,
    }


def get_playground(path: str) -> dict[str, object] | None:
    if path == "/api/playground/catalog":
        return service.catalog()
    if path == "/api/playground/integration":
        return integration_catalog()
    if path == "/api/playground/sessions":
        return service.sessions()
    if path.startswith("/api/playground/sessions/"):
        session_id = path[len("/api/playground/sessions/") :]
        return service.replay(session_id)
    if path.startswith(_CUDA_DIAGNOSTIC_URL_PREFIX):
        artifact_id = path[len(_CUDA_DIAGNOSTIC_URL_PREFIX) :]
        if not _CUDA_DIAGNOSTIC_ID.fullmatch(artifact_id):
            return None
        try:
            return _load_cuda_diagnostic_artifact(_REPO_ROOT, artifact_id)
        except FileNotFoundError:
            return None
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

    if path == "/api/playground/integration/transfer":
        return transfer_element(payload)

    if path == "/api/playground/research/synaptic-transfer":
        return _bounded_cuda_diagnostic(
            path, payload, lambda: run_synaptic_transfer(payload)
        )

    if path == "/api/playground/research/cue-controls":
        return _bounded_cuda_diagnostic(
            path, payload, lambda: run_cue_controls(payload)
        )

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
        return _bounded_cuda_diagnostic(path, payload, lambda: _cuda_preflight(payload))

    if path == "/api/playground/cuda/smoke":
        return _bounded_cuda_diagnostic(path, payload, lambda: _cuda_smoke(payload))

    if path == "/api/playground/cuda/rng-parity":
        return _bounded_cuda_diagnostic(
            path, payload, lambda: _cuda_rng_parity(payload)
        )

    if path == "/api/playground/cuda/builder-parity":
        return _bounded_cuda_diagnostic(
            path, payload, lambda: run_builder_parity(payload)
        )

    if path == "/api/playground/cuda/recurrent-parity":
        return _bounded_cuda_diagnostic(
            path, payload, lambda: _cuda_recurrent_parity(payload)
        )

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
            include_topology = payload.get("include_topology", True) is not False
            return {
                "session_id": session_id,
                **session.step(ticks, include_topology=include_topology),
            }
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
