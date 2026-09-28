"""GPU PAN health/hyperstate in the Builder's existing CUDA context."""

from __future__ import annotations

import ctypes
import math
from collections.abc import Sequence
from typing import Any

from ..pan.runtime import PANRuntime, PANState
from .runtime import CudaDriver, CudaDriverError, DeviceAllocation, DriverModule

STATE_FIELDS = (
    "pan_health",
    "pan_amplitude",
    "pan_energy",
    "pan_activity_ema",
    "pan_consolidation",
    "pan_information_proxy",
)


class PANStateStepper:
    """Fixed population buffers; topology, feedback and lifecycle bookkeeping stay host-owned."""

    def __init__(
        self, driver: CudaDriver, loaded: DriverModule, runtime: PANRuntime
    ) -> None:
        self.driver, self.loaded, self.runtime = driver, loaded, runtime
        self.n, self.dimensions = runtime.n_neurons, runtime.dimensions
        self.host: dict[str, Any] = {}
        self.device: dict[str, DeviceAllocation] = {}
        self.ticks = 0
        if not 1 <= self.n <= 1024 or not 5 <= self.dimensions <= 32:
            raise ValueError("unsupported CUDA PAN shape")
        try:
            for name, count, kind in (
                ("voltage", self.n, ctypes.c_double),
                ("threshold", self.n, ctypes.c_double),
                ("position", self.n, ctypes.c_double),
                ("coupling", self.n, ctypes.c_double),
                ("spikes", self.n, ctypes.c_uint32),
                ("alive", self.n, ctypes.c_uint32),
                ("state", 6 * self.n, ctypes.c_double),
                ("vectors", self.n * self.dimensions, ctypes.c_double),
            ):
                self.host[name] = (kind * count)()
                self.device[name] = driver.alloc_device(ctypes.sizeof(self.host[name]))
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

    def update(
        self,
        *,
        tick: int,
        dt_ms: float,
        states: Sequence[PANState],
        spiked_neurons: Sequence[int],
        plasticity_active: bool,
    ) -> None:
        runtime = self.runtime
        if type(tick) is not int or not 0 <= tick < 2**32 - 1 or len(states) != self.n:
            raise ValueError("CUDA PAN tick/shape invalid")
        if (
            not math.isfinite(dt_ms)
            or not 0 < dt_ms <= 5
            or any(
                not math.isfinite(x)
                for x in (runtime.health_decay, runtime.apoptosis_threshold)
            )
        ):
            raise ValueError("CUDA PAN parameters must be finite and bounded")
        if any(type(i) is not int or not 0 <= i < self.n for i in spiked_neurons):
            raise ValueError("CUDA PAN spike index invalid")
        spiked = set(spiked_neurons)
        self.host["voltage"][:] = [float(s.get("v", -65.0)) for s in states]
        self.host["threshold"][:] = [
            float(s.get("pan_threshold", -50.0)) for s in states
        ]
        self.host["position"][:] = [
            runtime.position_projection(i) for i in range(self.n)
        ]
        self.host["coupling"][:] = [
            max(0.0, min(1.0, runtime.degree[i] / max(self.n - 1, 1)))
            for i in range(self.n)
        ]
        self.host["spikes"][:] = [int(i in spiked) for i in range(self.n)]
        before = [bool(s.get("pan_alive", True)) for s in states]
        self.host["alive"][:] = [int(x) for x in before]
        self.host["state"][:] = [float(s[k]) for s in states for k in STATE_FIELDS]
        vectors = [list(s["pan_x_hd"]) for s in states]
        if any(len(v) != self.dimensions for v in vectors):
            raise ValueError("CUDA PAN hypervector shape invalid")
        self.host["vectors"][:] = [float(x) for v in vectors for x in v]
        for name, values in self.host.items():
            if any(not math.isfinite(x) for x in values):
                raise ValueError("CUDA PAN input must be finite")
        for name in self.host:
            self.driver.copy_host_to_device(self.device[name], self.host[name])
        args: list[object] = [
            ctypes.c_uint32(self.n),
            ctypes.c_uint32(self.dimensions),
            ctypes.c_uint32(tick),
            ctypes.c_uint32(bool(plasticity_active)),
            ctypes.c_double(dt_ms),
            ctypes.c_double(runtime.health_decay),
            ctypes.c_double(runtime.apoptosis_threshold),
        ]
        args.extend(ctypes.c_uint64(self.device[name].ptr) for name in self.host)
        self.driver.launch_kernel(
            self.loaded,
            grid=((self.n + 127) // 128, 1, 1),
            block=(128, 1, 1),
            arguments=args,
        )
        self.driver.synchronize()
        for name in ("alive", "state", "vectors"):
            self.driver.copy_device_to_host(self.host[name], self.device[name])
        if any(
            not math.isfinite(x)
            for name in ("state", "vectors")
            for x in self.host[name]
        ) or any(x not in (0, 1) for x in self.host["alive"]):
            raise ValueError("CUDA PAN output must be finite with binary alive flags")
        for i, s in enumerate(states):
            for j, k in enumerate(STATE_FIELDS):
                s[k] = self.host["state"][6 * i + j]
            s["pan_x_hd"] = list(
                self.host["vectors"][i * self.dimensions : (i + 1) * self.dimensions]
            )
            s["pan_alive"] = bool(self.host["alive"][i])
            if before[i] and not s["pan_alive"]:
                runtime.apoptosis_events.append(
                    {"tick": tick, "neuron_id": i, "health": s["pan_health"]}
                )
        runtime.population_vector = [
            sum(float(s["pan_x_hd"][d]) for s in states) / self.n
            for d in range(self.dimensions)
        ]
        runtime.feedback_history.append(list(runtime.population_vector))
        keep = max(2, runtime.feedback_delay + 2)
        if len(runtime.feedback_history) > keep:
            runtime.feedback_history = runtime.feedback_history[-keep:]
        self.ticks += 1
