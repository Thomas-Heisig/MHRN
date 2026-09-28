"""CUDA-1.4 bounded recurrent membrane reference, with explicit FP64 state.

This implements static synapses and LIF/AdEx membrane dynamics. PAN hyperstate,
plasticity and a live environment are deliberately not silently approximated.
"""

from __future__ import annotations

import ctypes
import math
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..registry.neuron_models import get_neuron_model
from .nvrtc import compile_cuda_source
from .runtime import (
    CudaDriver,
    CudaDriverError,
    DeviceAllocation,
    max_abs_error,
    validate_cuda_block_size,
)

PARAMETER_NAMES = (
    "v_rest",
    "v_t",
    "delta_t",
    "tau_m_ms",
    "tau_w_ms",
    "a",
    "b",
    "threshold",
    "reset",
    "resistance",
)
SUPPORTED_MODELS = {"lif", "adex", "pan_adex_5d"}


@dataclass(frozen=True)
class RecurrentInputs:
    n_neurons: int
    ticks: int
    offsets: tuple[int, ...]
    sources: tuple[int, ...]
    delays: tuple[int, ...]
    weights: tuple[float, ...]
    external: tuple[float, ...]
    voltage: tuple[float, ...]
    adaptation: tuple[float, ...]
    model: str = "lif"
    dt_ms: float = 1.0


def _bounded_integer(value: object, lower: int, upper: int) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, int)
        and lower <= value <= upper
    )


def _bounded_number(value: object) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, (int, float))
        and math.isfinite(value)
        and abs(value) <= 1e6
    )


def validate_recurrent_inputs(inputs: RecurrentInputs) -> None:
    for name, value, upper in (
        ("n_neurons", inputs.n_neurons, 4096),
        ("ticks", inputs.ticks, 2000),
    ):
        if not _bounded_integer(value, 1, upper):
            raise ValueError(f"{name} must be an integer in [1,{upper}]")
    n, ticks = inputs.n_neurons, inputs.ticks
    if n * ticks > 4_000_000:
        raise ValueError("state history exceeds bounded reference capacity")
    if inputs.model not in SUPPORTED_MODELS:
        raise ValueError("unsupported recurrent membrane model")
    if (
        isinstance(inputs.dt_ms, bool)
        or not math.isfinite(inputs.dt_ms)
        or not 0 < inputs.dt_ms <= 1
    ):
        raise ValueError("dt_ms must be finite in (0,1]")
    edges = len(inputs.sources)
    if edges > 65536 or len(inputs.offsets) != n + 1:
        raise ValueError("invalid incoming CSR shape")
    for values, upper in (
        (inputs.offsets, edges),
        (inputs.sources, n - 1),
        (inputs.delays, 64),
    ):
        if any(not _bounded_integer(x, 0, upper) for x in values):
            raise ValueError("invalid CSR integer/index/delay")
    if (
        inputs.offsets[0] != 0
        or inputs.offsets[-1] != edges
        or any(a > b for a, b in zip(inputs.offsets, inputs.offsets[1:]))
    ):
        raise ValueError("incoming CSR offsets must be monotone and span all edges")
    if len(inputs.delays) != edges or any(x < 1 for x in inputs.delays):
        raise ValueError("each edge requires a delay in [1,64]")
    for name, numbers, length in (
        ("weights", inputs.weights, edges),
        ("external", inputs.external, n * ticks),
        ("voltage", inputs.voltage, n),
        ("adaptation", inputs.adaptation, n),
    ):
        if len(numbers) != length or any(not _bounded_number(x) for x in numbers):
            raise ValueError(
                f"{name} has an invalid shape or non-finite/out-of-range values"
            )


def cpu_recurrent_reference(inputs: RecurrentInputs) -> dict[str, object]:
    """Use the existing Python neuron model as an independent scalar oracle."""
    validate_recurrent_inputs(inputs)
    model = get_neuron_model(inputs.model)
    states = [{"v": v, "w": w} for v, w in zip(inputs.voltage, inputs.adaptation)]
    n = inputs.n_neurons
    spikes: list[int] = []
    voltage: list[float] = []
    adaptation: list[float] = []
    for tick in range(inputs.ticks):
        for neuron in range(n):
            current = inputs.external[tick * n + neuron]
            for edge in range(inputs.offsets[neuron], inputs.offsets[neuron + 1]):
                previous = tick - inputs.delays[edge]
                if previous >= 0:
                    current += (
                        inputs.weights[edge]
                        * spikes[previous * n + inputs.sources[edge]]
                    )
            spike = model.step(states[neuron], current, inputs.dt_ms, model.parameters)
            spikes.append(int(spike))
            voltage.append(float(states[neuron]["v"]))
            adaptation.append(float(states[neuron]["w"]))
    return {"voltage": voltage, "adaptation": adaptation, "spikes": spikes}


def execute_recurrent(
    inputs: RecurrentInputs,
    *,
    block_size: int = 64,
    target_sm: str = "sm_86",
    output_dir: Path | None = None,
) -> dict[str, object]:
    validate_recurrent_inputs(inputs)
    validate_cuda_block_size(block_size)
    if output_dir is None:
        with tempfile.TemporaryDirectory(prefix="mhrn-recurrent-") as directory:
            return execute_recurrent(
                inputs,
                block_size=block_size,
                target_sm=target_sm,
                output_dir=Path(directory),
            )
    output_dir.mkdir(parents=True, exist_ok=True)
    ptx = compile_cuda_source(
        Path(__file__).with_name("recurrent.cu").read_text(), target_sm=target_sm
    )
    artifact = output_dir / "recurrent.ptx"
    artifact.write_text(ptx, encoding="utf-8")
    driver = CudaDriver()
    loaded = driver.load_cubin(artifact, kernel_name="pan_recurrent_kernel")
    allocations: list[DeviceAllocation] = []
    try:
        n, count = inputs.n_neurons, inputs.n_neurons * inputs.ticks
        ring_size = max(inputs.delays, default=1) + 1
        params = get_neuron_model(inputs.model).parameters
        parameter_row = [
            params.get(
                name, 1.0 if name in {"resistance", "tau_w_ms", "delta_t"} else 0.0
            )
            for name in PARAMETER_NAMES
        ]
        uint, double = ctypes.c_uint32, ctypes.c_double
        host: dict[str, Any] = {}
        for name, kind, values in (
            ("offsets", uint, inputs.offsets),
            ("sources", uint, inputs.sources),
            ("delays", uint, inputs.delays),
            ("weights", double, inputs.weights),
            ("external", double, inputs.external),
            ("parameters", double, parameter_row * n),
            ("voltage", double, inputs.voltage),
            ("adaptation", double, inputs.adaptation),
            ("ring", uint, [0] * (ring_size * n)),
            ("voltage_history", double, [0.0] * count),
            ("adaptation_history", double, [0.0] * count),
            ("spikes", uint, [0] * count),
        ):
            # CUDA does not accept a zero-byte allocation for an empty graph.
            array_type: Any = kind * max(1, len(values))
            host[name] = array_type(*values)
        device: dict[str, DeviceAllocation] = {}
        for name, buffer in host.items():
            allocation = driver.alloc_device(ctypes.sizeof(buffer))
            allocations.append(allocation)
            device[name] = allocation
            driver.copy_host_to_device(allocation, buffer)
        arguments: list[object] = [
            uint(n),
            uint(inputs.ticks),
            uint(ring_size),
            uint(inputs.model != "lif"),
            double(inputs.dt_ms),
        ]
        arguments.extend(ctypes.c_uint64(device[name].ptr) for name in host)
        preflight = driver.launch_cooperative(
            loaded, n_neurons=n, block_size=block_size, arguments=arguments
        )
        driver.synchronize()
        outputs: dict[str, object] = {}
        for name, key in (
            ("voltage_history", "voltage"),
            ("adaptation_history", "adaptation"),
            ("spikes", "spikes"),
        ):
            driver.copy_device_to_host(host[name], device[name])
            outputs[key] = list(host[name])
        return {
            "classification": "PLAYGROUND_CUDA14_RECURRENT_REFERENCE",
            "scientific_evidence": False,
            "execution_status": "GPU_KERNEL_EXECUTED",
            "state_dtype": "float64",
            "comparison_scope": "STATIC_SYNAPSES_AND_MEMBRANE_ONLY",
            "full_pan_backend": False,
            "preflight": preflight.to_mapping(),
            "ticks": inputs.ticks,
            "outputs": outputs,
        }
    finally:
        try:
            for allocation in reversed(allocations):
                try:
                    driver.free_device(allocation)
                except CudaDriverError:
                    pass
        finally:
            driver.unload(loaded)


def recurrent_parity(
    reference: dict[str, Any], candidate: dict[str, Any], *, tolerance: float = 1e-4
) -> dict[str, object]:
    if isinstance(tolerance, bool) or not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and non-negative")
    try:
        errors = {
            name: max_abs_error(reference.get(name, []), candidate.get(name, []))
            for name in ("voltage", "adaptation")
        }
    except (ValueError, TypeError, OverflowError) as exc:
        return {
            "passed": False,
            "failure_reason": str(exc),
            "scientific_evidence": False,
        }
    spikes = reference.get("spikes", [])
    other = candidate.get("spikes", [])
    exact = (
        bool(spikes)
        and len(spikes)
        == len(other)
        == len(reference["voltage"])
        == len(reference["adaptation"])
        and all(a in (0, 1) and b in (0, 1) and a == b for a, b in zip(spikes, other))
    )
    return {
        "passed": exact
        and all(math.isfinite(x) and x <= tolerance for x in errors.values()),
        "D1_spikes_exact": exact,
        "D2_max_abs_error": errors,
        "scientific_evidence": False,
        "scope": "MEMBRANE_AND_STATIC_SYNAPSES",
    }


def recurrent_fixture(
    *, n_neurons: int = 129, ticks: int = 100, model: str = "pan_adex_5d"
) -> RecurrentInputs:
    """Nontrivial cross-block ring graph used by CLI, HTTP and hardware checks."""
    if not _bounded_integer(n_neurons, 1, 4096):
        raise ValueError("n_neurons must be in [1,4096]")
    if not _bounded_integer(ticks, 1, 2000) or n_neurons * ticks > 4_000_000:
        raise ValueError("ticks or history exceeds diagnostic capacity")
    n = n_neurons
    inputs = RecurrentInputs(
        n,
        ticks,
        tuple(range(n + 1)),
        tuple((i - 65) % n for i in range(n)),
        tuple(1 + i % 7 for i in range(n)),
        (2.0,) * n,
        tuple(40.0 + (i % 5) * 2 for _ in range(ticks) for i in range(n)),
        (-65.0,) * n,
        (0.0,) * n,
        model=model,
    )
    validate_recurrent_inputs(inputs)
    return inputs
