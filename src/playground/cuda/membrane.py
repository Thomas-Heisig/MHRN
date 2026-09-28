"""Optional GPU membrane execution inside the real host PAN closed loop."""

from __future__ import annotations

import ctypes
import math
import tempfile
from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from ..pan.runtime import PANRuntime
from .builder_synapses import BuilderSynapseStepper
from .delay_queue import DeviceDelayQueue
from .nvrtc import compile_cuda_source
from .pan_state import PANStateStepper
from .recurrent import PARAMETER_NAMES, SUPPORTED_MODELS
from .runtime import CudaDriver, CudaDriverError, DeviceAllocation, DriverModule


class MembraneStepper:
    """Reuse one module, context and allocation set for all Builder ticks."""

    def __init__(
        self,
        driver: CudaDriver,
        loaded: DriverModule,
        model: str,
        parameters: Sequence[Mapping[str, float]],
        dt_ms: float,
    ) -> None:
        self.driver, self.loaded = driver, loaded
        self.n = len(parameters)
        self.model, self.dt_ms = model, dt_ms
        self.device: dict[str, DeviceAllocation] = {}
        self.host: dict[str, Any] = {}
        self.ticks = 0
        self.pan: PANStateStepper | None = None
        self.synapses: BuilderSynapseStepper | None = None
        self.delay_queue: DeviceDelayQueue | None = None
        row = [
            p.get(name, 1.0 if name in {"resistance", "delta_t", "tau_w_ms"} else 0.0)
            for p in parameters
            for name in PARAMETER_NAMES
        ]
        if (
            model not in SUPPORTED_MODELS
            or not 1 <= self.n <= 1024
            or not math.isfinite(dt_ms)
            or not 0 < dt_ms <= 5
            or any(not math.isfinite(x) for x in row)
        ):
            raise ValueError("unsupported or non-finite CUDA membrane configuration")
        for offset in range(0, len(row), 10):
            if min(row[offset + 2], row[offset + 3], row[offset + 4]) <= 0:
                raise ValueError("CUDA membrane time constants must be positive")
        try:
            for name, kind, values in (
                ("parameters", ctypes.c_double, row),
                ("currents", ctypes.c_double, [0.0] * self.n),
                ("active", ctypes.c_uint32, [0] * self.n),
                ("voltage", ctypes.c_double, [0.0] * self.n),
                ("adaptation", ctypes.c_double, [0.0] * self.n),
                ("spikes", ctypes.c_uint32, [0] * self.n),
            ):
                array: Any = kind * len(values)
                self.host[name] = array(*values)
                self.device[name] = driver.alloc_device(ctypes.sizeof(self.host[name]))
                driver.copy_host_to_device(self.device[name], self.host[name])
        except BaseException:
            self.close()
            raise

    def close(self) -> None:
        for allocation in reversed(list(self.device.values())):
            try:
                self.driver.free_device(allocation)
            except CudaDriverError:
                pass
        self.device.clear()

    def step(
        self, states: list[dict[str, Any]], currents: list[float], active: list[int]
    ) -> list[int]:
        if len(states) != self.n or len(currents) != self.n or len(active) != self.n:
            raise ValueError("CUDA membrane vector shape mismatch")
        for name, values in (
            ("currents", currents),
            ("voltage", [float(s["v"]) for s in states]),
            ("adaptation", [float(s.get("w", 0.0)) for s in states]),
        ):
            if any(not math.isfinite(x) for x in values):
                raise ValueError("CUDA membrane state/current must be finite")
            self.host[name][:] = values
        if any(type(value) is not int or value not in (0, 1) for value in active):
            raise ValueError("CUDA membrane active mask must be binary integers")
        self.host["active"][:] = active
        for name in ("currents", "active", "voltage", "adaptation"):
            self.driver.copy_host_to_device(self.device[name], self.host[name])
        arguments: list[object] = [
            ctypes.c_uint32(self.n),
            ctypes.c_uint32(self.model != "lif"),
            ctypes.c_double(self.dt_ms),
        ]
        arguments.extend(ctypes.c_uint64(self.device[name].ptr) for name in self.host)
        self.driver.launch_kernel(
            self.loaded,
            grid=((self.n + 127) // 128, 1, 1),
            block=(128, 1, 1),
            arguments=arguments,
        )
        self.driver.synchronize()
        for name in ("voltage", "adaptation", "spikes"):
            self.driver.copy_device_to_host(self.host[name], self.device[name])
        if any(
            not math.isfinite(x)
            for name in ("voltage", "adaptation")
            for x in self.host[name]
        ):
            raise ValueError("CUDA membrane produced non-finite state")
        for i, state in enumerate(states):
            state["v"] = self.host["voltage"][i]
            if self.model != "lif":
                state["w"] = self.host["adaptation"][i]
        self.ticks += 1
        return [i for i, spike in enumerate(self.host["spikes"]) if spike]


@contextmanager
def cuda_membrane_session(
    model: str,
    parameters: Sequence[Mapping[str, float]],
    dt_ms: float,
    *,
    pan_runtime: PANRuntime | None = None,
) -> Generator[MembraneStepper]:
    source = Path(__file__).with_name("membrane.cu").read_text(encoding="utf-8")
    if pan_runtime is not None:
        source += "\n" + Path(__file__).with_name("pan_state.cu").read_text(
            encoding="utf-8"
        )
    if pan_runtime is not None:
        source += "\n" + Path(__file__).with_name("builder_synapses.cu").read_text(
            encoding="utf-8"
        )
    if pan_runtime is not None:
        source += "\n" + Path(__file__).with_name("delay_queue.cu").read_text(
            encoding="utf-8"
        )
    ptx = compile_cuda_source(source, target_sm="sm_86")
    with tempfile.TemporaryDirectory(prefix="mhrn-membrane-") as directory:
        path = Path(directory) / "membrane.ptx"
        path.write_text(ptx, encoding="utf-8")
        driver = CudaDriver()
        loaded = driver.load_cubin(path, kernel_name="pan_membrane_step")
        try:
            stepper = MembraneStepper(driver, loaded, model, parameters, dt_ms)
            try:
                if pan_runtime is not None:
                    stepper.pan = PANStateStepper(
                        driver, driver.kernel(loaded, "pan_state_step"), pan_runtime
                    )
                    stepper.synapses = BuilderSynapseStepper(
                        driver, loaded, min(20000, max(1, stepper.n * (stepper.n - 1)))
                    )
                    stepper.delay_queue = DeviceDelayQueue(
                        driver,
                        loaded,
                        stepper.n,
                        min(20000, max(1, stepper.n * (stepper.n - 1))),
                    )
                yield stepper
            finally:
                try:
                    try:
                        try:
                            if stepper.delay_queue is not None:
                                stepper.delay_queue.close()
                        finally:
                            if stepper.synapses is not None:
                                stepper.synapses.close()
                    finally:
                        if stepper.pan is not None:
                            stepper.pan.close()
                finally:
                    stepper.close()
        finally:
            driver.unload(loaded)
