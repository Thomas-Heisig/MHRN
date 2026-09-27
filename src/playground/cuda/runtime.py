"""CUDA-1 runtime helpers for the Playground PAN gate compiler.

The runtime is deliberately optional: importing it requires neither a CUDA
toolkit nor a GPU. PTX assembly requires `ptxas`; driver loading and occupancy
preflight require a CUDA driver. Scientific promotion remains disabled.
"""

from __future__ import annotations

import copy
import ctypes
import hashlib
import json
import math
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from collections.abc import Mapping, Sequence
from pathlib import Path

from .pan_compiler import CompileBundle


class CudaRuntimeUnavailable(RuntimeError):
    """Raised when an optional CUDA-1 dependency is not available."""


class CudaDriverError(RuntimeError):
    """Raised when a CUDA Driver API call fails."""


@dataclass(frozen=True, slots=True)
class PtxasReport:
    """Measured resource report emitted by ptxas."""

    target_sm: str
    registers: int | None
    shared_bytes: int | None
    constant_bytes: int | None
    stack_bytes: int | None
    spill_store_bytes: int | None
    spill_load_bytes: int | None
    cubin_path: Path
    verbose_output: str

    def to_mapping(self) -> dict[str, object]:
        return {
            "target_sm": self.target_sm,
            "registers": self.registers,
            "shared_bytes": self.shared_bytes,
            "constant_bytes": self.constant_bytes,
            "stack_bytes": self.stack_bytes,
            "spill_store_bytes": self.spill_store_bytes,
            "spill_load_bytes": self.spill_load_bytes,
            "cubin_path": str(self.cubin_path),
            "verbose_output": self.verbose_output,
        }


@dataclass(frozen=True, slots=True)
class CooperativePreflight:
    """Host/device limits required for a cooperative persistent launch."""

    cooperative_launch: bool
    multiprocessor_count: int
    active_blocks_per_sm: int
    block_size: int
    required_blocks: int
    resident_block_capacity: int
    launch_fits: bool
    n_neurons: int

    def to_mapping(self) -> dict[str, object]:
        return {
            "cooperative_launch": self.cooperative_launch,
            "multiprocessor_count": self.multiprocessor_count,
            "active_blocks_per_sm": self.active_blocks_per_sm,
            "block_size": self.block_size,
            "required_blocks": self.required_blocks,
            "resident_block_capacity": self.resident_block_capacity,
            "launch_fits": self.launch_fits,
            "n_neurons": self.n_neurons,
        }


@dataclass(frozen=True, slots=True)
class DriverModule:
    """Opaque handles returned by CUDA Driver API loading."""

    context: ctypes.c_void_p
    module: ctypes.c_void_p
    function: ctypes.c_void_p
    device_ordinal: int


_REGISTER_RE = re.compile(r"Used\s+(\d+)\s+registers")
_SMEM_RE = re.compile(r"(\d+)\s+bytes smem")
_CMEM_RE = re.compile(r"(\d+)\s+bytes cmem\[\d+\]")
_STACK_RE = re.compile(r"(\d+)\s+bytes stack frame")
_SPILL_STORE_RE = re.compile(r"(\d+)\s+bytes spill stores")
_SPILL_LOAD_RE = re.compile(r"(\d+)\s+bytes spill loads")


def _first_int(pattern: re.Pattern[str], text: str) -> int | None:
    match = pattern.search(text)
    return int(match.group(1)) if match else None


def parse_ptxas_verbose(
    verbose_output: str,
    *,
    target_sm: str,
    cubin_path: Path,
) -> PtxasReport:
    """Parse stable resource fields from ptxas verbose diagnostics."""

    constant_values = [int(value) for value in _CMEM_RE.findall(verbose_output)]
    return PtxasReport(
        target_sm=target_sm,
        registers=_first_int(_REGISTER_RE, verbose_output),
        shared_bytes=_first_int(_SMEM_RE, verbose_output),
        constant_bytes=sum(constant_values) if constant_values else None,
        stack_bytes=_first_int(_STACK_RE, verbose_output),
        spill_store_bytes=_first_int(_SPILL_STORE_RE, verbose_output),
        spill_load_bytes=_first_int(_SPILL_LOAD_RE, verbose_output),
        cubin_path=cubin_path,
        verbose_output=verbose_output,
    )


def assemble_ptx(
    ptx_source: str,
    *,
    target_sm: str = "sm_86",
    output_dir: Path | None = None,
    ptxas: str = "ptxas",
) -> PtxasReport:
    """Assemble generated PTX and return measured ptxas resources."""

    executable = shutil.which(ptxas)
    if executable is None:
        raise CudaRuntimeUnavailable(f"{ptxas} is not available on PATH")

    root = output_dir or Path(tempfile.mkdtemp(prefix="mhrn-ptxas-"))
    root.mkdir(parents=True, exist_ok=True)
    ptx_path = root / "pan_gate_kernel.ptx"
    cubin_path = root / "pan_gate_kernel.cubin"
    ptx_path.write_text(ptx_source, encoding="utf-8")

    process = subprocess.run(
        [
            executable,
            "--verbose",
            f"--gpu-name={target_sm}",
            str(ptx_path),
            "--output-file",
            str(cubin_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    verbose = "\n".join(part for part in (process.stdout, process.stderr) if part)
    if process.returncode != 0:
        raise CudaDriverError(
            "ptxas rejected generated PTX " f"(exit={process.returncode}):\n{verbose}"
        )
    return parse_ptxas_verbose(
        verbose,
        target_sm=target_sm,
        cubin_path=cubin_path,
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


# CUDA Driver API attribute IDs from cuda.h.
_CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT = 16
_CU_DEVICE_ATTRIBUTE_COOPERATIVE_LAUNCH = 95


class CudaDriver:
    """Minimal ctypes wrapper for CUDA-1 loading and occupancy preflight."""

    def __init__(self, library: str = "libcuda.so.1") -> None:
        try:
            self._lib = ctypes.CDLL(library)
        except OSError as exc:
            raise CudaRuntimeUnavailable(
                f"CUDA driver library not available: {library}"
            ) from exc
        self._bind()

    def _bind(self) -> None:
        lib = self._lib
        lib.cuInit.argtypes = [ctypes.c_uint]
        lib.cuInit.restype = ctypes.c_int
        lib.cuDeviceGet.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        lib.cuDeviceGet.restype = ctypes.c_int
        lib.cuDeviceGetAttribute.argtypes = [
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_int,
            ctypes.c_int,
        ]
        lib.cuDeviceGetAttribute.restype = ctypes.c_int
        lib.cuCtxCreate_v2.argtypes = [
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.c_uint,
            ctypes.c_int,
        ]
        lib.cuCtxCreate_v2.restype = ctypes.c_int
        lib.cuCtxDestroy_v2.argtypes = [ctypes.c_void_p]
        lib.cuCtxDestroy_v2.restype = ctypes.c_int
        lib.cuModuleLoad.argtypes = [
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.c_char_p,
        ]
        lib.cuModuleLoad.restype = ctypes.c_int
        lib.cuModuleUnload.argtypes = [ctypes.c_void_p]
        lib.cuModuleUnload.restype = ctypes.c_int
        lib.cuModuleGetFunction.argtypes = [
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.c_void_p,
            ctypes.c_char_p,
        ]
        lib.cuModuleGetFunction.restype = ctypes.c_int
        lib.cuOccupancyMaxActiveBlocksPerMultiprocessor.argtypes = [
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_size_t,
        ]
        lib.cuOccupancyMaxActiveBlocksPerMultiprocessor.restype = ctypes.c_int

    @staticmethod
    def _check(code: int, call: str) -> None:
        if code != 0:
            raise CudaDriverError(f"{call} failed with CUDA error code {code}")

    def initialize(self) -> None:
        self._check(self._lib.cuInit(0), "cuInit")

    def _device(self, ordinal: int) -> int:
        device = ctypes.c_int()
        self._check(
            self._lib.cuDeviceGet(ctypes.byref(device), ordinal),
            "cuDeviceGet",
        )
        return int(device.value)

    def device_attribute(self, ordinal: int, attribute: int) -> int:
        device = self._device(ordinal)
        value = ctypes.c_int()
        self._check(
            self._lib.cuDeviceGetAttribute(
                ctypes.byref(value),
                attribute,
                device,
            ),
            "cuDeviceGetAttribute",
        )
        return int(value.value)

    def load_cubin(
        self,
        cubin_path: Path,
        *,
        kernel_name: str = "pan_gate_kernel",
        device_ordinal: int = 0,
    ) -> DriverModule:
        """Load a ptxas-generated cubin and resolve one kernel symbol."""

        self.initialize()
        device = self._device(device_ordinal)
        context = ctypes.c_void_p()
        self._check(
            self._lib.cuCtxCreate_v2(ctypes.byref(context), 0, device),
            "cuCtxCreate_v2",
        )
        module = ctypes.c_void_p()
        try:
            self._check(
                self._lib.cuModuleLoad(
                    ctypes.byref(module),
                    str(cubin_path).encode("utf-8"),
                ),
                "cuModuleLoad",
            )
            function = ctypes.c_void_p()
            self._check(
                self._lib.cuModuleGetFunction(
                    ctypes.byref(function),
                    module,
                    kernel_name.encode("ascii"),
                ),
                "cuModuleGetFunction",
            )
        except Exception:
            if module.value:
                self._lib.cuModuleUnload(module)
            self._lib.cuCtxDestroy_v2(context)
            raise
        return DriverModule(
            context=context,
            module=module,
            function=function,
            device_ordinal=device_ordinal,
        )

    def unload(self, loaded: DriverModule) -> None:
        if loaded.module.value:
            self._check(
                self._lib.cuModuleUnload(loaded.module),
                "cuModuleUnload",
            )
        if loaded.context.value:
            self._check(
                self._lib.cuCtxDestroy_v2(loaded.context),
                "cuCtxDestroy_v2",
            )

    def cooperative_preflight(
        self,
        loaded: DriverModule,
        *,
        n_neurons: int,
        block_size: int = 128,
        dynamic_shared_bytes: int = 0,
    ) -> CooperativePreflight:
        """Calculate whether the full cooperative grid can be resident."""

        if block_size <= 0:
            raise ValueError("block_size must be positive")
        cooperative = bool(
            self.device_attribute(
                loaded.device_ordinal,
                _CU_DEVICE_ATTRIBUTE_COOPERATIVE_LAUNCH,
            )
        )
        sms = self.device_attribute(
            loaded.device_ordinal,
            _CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT,
        )
        active = ctypes.c_int()
        self._check(
            self._lib.cuOccupancyMaxActiveBlocksPerMultiprocessor(
                ctypes.byref(active),
                loaded.function,
                block_size,
                dynamic_shared_bytes,
            ),
            "cuOccupancyMaxActiveBlocksPerMultiprocessor",
        )
        required = math.ceil(n_neurons / block_size)
        capacity = int(active.value) * sms
        return CooperativePreflight(
            cooperative_launch=cooperative,
            multiprocessor_count=sms,
            active_blocks_per_sm=int(active.value),
            block_size=block_size,
            required_blocks=required,
            resident_block_capacity=capacity,
            launch_fits=cooperative and required <= capacity,
            n_neurons=n_neurons,
        )


def preflight_bundle(
    bundle: CompileBundle,
    *,
    n_neurons: int,
    block_size: int = 128,
    dynamic_shared_bytes: int = 0,
    output_dir: Path | None = None,
    ptxas: str = "ptxas",
    driver_library: str = "libcuda.so.1",
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


def cooperative_capacity(
    *,
    n_neurons: int,
    block_size: int,
    multiprocessor_count: int,
    active_blocks_per_sm: int,
    cooperative_launch: bool = True,
) -> CooperativePreflight:
    """Pure helper used by CI to verify occupancy-bound grid logic."""

    if (
        min(
            n_neurons,
            block_size,
            multiprocessor_count,
            active_blocks_per_sm,
        )
        <= 0
    ):
        raise ValueError("cooperative capacity inputs must be positive")
    required = math.ceil(n_neurons / block_size)
    capacity = multiprocessor_count * active_blocks_per_sm
    return CooperativePreflight(
        cooperative_launch=cooperative_launch,
        multiprocessor_count=multiprocessor_count,
        active_blocks_per_sm=active_blocks_per_sm,
        block_size=block_size,
        required_blocks=required,
        resident_block_capacity=capacity,
        launch_fits=cooperative_launch and required <= capacity,
        n_neurons=n_neurons,
    )


PARITY_CONTRACT: dict[str, object] = {
    "classification": "PLAYGROUND_CUDA_PARITY_CONTRACT",
    "scientific_evidence": False,
    "reference_source": "CPU_PYTHON_PLAYGROUND",
    "classes": {
        "D1": {
            "name": "exact_event_parity",
            "spike_train": "BIT_IDENTICAL_NEURON_ID_TICK",
            "allowed_spike_mismatches": 0,
            "target_stage": "LATER_STRICT_TARGET",
        },
        "D2": {
            "name": "numerical_state_parity",
            "voltage_max_abs_error": 1.0e-4,
            "weight_max_abs_error": 1.0e-4,
            "target_stage": "CUDA_1_PRIMARY_TARGET",
        },
        "D3": {
            "name": "behavioral_metric_parity",
            "spike_count_relative_error": 0.005,
            "success_fraction_abs_error": 0.02,
            "target_stage": "CLOSED_LOOP_AND_PLASTICITY",
        },
    },
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


def parity_contract() -> dict[str, object]:
    """Return an isolated copy of the CUDA-1 parity criteria."""

    return copy.deepcopy(PARITY_CONTRACT)


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

    spike_train_exact = (
        first_monitors.get("spikes") == second_monitors.get("spikes")
    )
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
    """Evaluate D1 exact spike-event parity."""

    mismatches = 0
    for index in range(max(len(reference), len(candidate))):
        left = reference[index] if index < len(reference) else None
        right = candidate[index] if index < len(candidate) else None
        if left != right:
            mismatches += 1
    return {
        "classification": "PLAYGROUND_CUDA_SPIKE_PARITY",
        "scientific_evidence": False,
        "parity_class": "D1",
        "reference_source": "CPU_PYTHON_PLAYGROUND",
        "reference_frozen_at": reference_commit or "UNSPECIFIED",
        "allowed_spike_mismatches": 0,
        "spike_mismatches": mismatches,
        "passed": mismatches == 0,
    }


def behavioral_parity_summary(
    *,
    reference_spike_count: int,
    candidate_spike_count: int,
    reference_success_fraction: float,
    candidate_success_fraction: float,
    reference_commit: str = "",
) -> dict[str, object]:
    """Evaluate the bounded D3 behavioral parity criteria."""

    denominator = max(abs(reference_spike_count), 1)
    spike_count_relative_error = (
        abs(candidate_spike_count - reference_spike_count) / denominator
    )
    success_fraction_abs_error = abs(
        candidate_success_fraction - reference_success_fraction
    )
    spike_limit = 0.005
    success_limit = 0.02
    return {
        "classification": "PLAYGROUND_CUDA_BEHAVIORAL_PARITY",
        "scientific_evidence": False,
        "parity_class": "D3",
        "reference_source": "CPU_PYTHON_PLAYGROUND",
        "reference_frozen_at": reference_commit or "UNSPECIFIED",
        "spike_count_relative_error": spike_count_relative_error,
        "spike_count_relative_error_limit": spike_limit,
        "success_fraction_abs_error": success_fraction_abs_error,
        "success_fraction_abs_error_limit": success_limit,
        "passed": (
            spike_count_relative_error <= spike_limit + 1.0e-12
            and success_fraction_abs_error <= success_limit + 1.0e-12
        ),
    }


def max_abs_error(reference: Sequence[float], candidate: Sequence[float]) -> float:
    """Return the maximum absolute error for a gate-parity vector."""

    if len(reference) != len(candidate):
        raise ValueError("parity vectors must have the same length")
    if not reference:
        return 0.0
    return max(
        abs(float(left) - float(right)) for left, right in zip(reference, candidate)
    )


def gate_parity_summary(
    reference: Sequence[float],
    candidate: Sequence[float],
    *,
    tolerance: float = 1.0e-4,
    reference_commit: str = "",
) -> dict[str, object]:
    """Summarize D2 gate parity without claiming full SNN equivalence."""

    error = max_abs_error(reference, candidate)
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
        "passed": error <= tolerance,
    }
