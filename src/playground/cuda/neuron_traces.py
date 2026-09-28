"""Device-owned neuron traces with explicit pre-plasticity and post-emission phases."""

from __future__ import annotations

import ctypes
import math
from collections.abc import Sequence
from typing import Any

from .runtime import CudaDriver, CudaDriverError, DeviceAllocation, DriverModule


class DeviceNeuronTraces:
    def __init__(
        self, driver: CudaDriver, loaded: DriverModule, n_neurons: int
    ) -> None:
        if type(n_neurons) is not int or not 1 <= n_neurons <= 1024:
            raise ValueError("invalid CUDA neuron trace population")
        self.driver, self.n = driver, n_neurons
        self.kernel = driver.kernel(loaded, "pan_neuron_traces")
        self.device: dict[str, DeviceAllocation] = {}
        self.host: dict[str, Any] = {
            "spikes": (ctypes.c_uint32 * self.n)(),
            "traces": (ctypes.c_double * (2 * self.n))(),
            "last": (ctypes.c_int64 * self.n)(*([-10_000_000] * self.n)),
        }
        self.completed_ticks = 0
        self._awaiting_commit = False
        try:
            for name, values in self.host.items():
                self.device[name] = driver.alloc_device(ctypes.sizeof(values))
                driver.copy_host_to_device(self.device[name], values)
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

    def _validate_tick(self, tick: int, commit: bool) -> None:
        if (
            type(tick) is not int
            or not 0 <= tick < 2**32
            or tick != self.completed_ticks
            or commit != self._awaiting_commit
        ):
            raise ValueError("invalid CUDA trace tick/phase")

    def _execute(
        self, tick: int, commit: bool
    ) -> tuple[list[float], list[float], list[int]]:
        self.driver.launch_kernel(
            self.kernel,
            grid=((self.n + 127) // 128, 1, 1),
            block=(128, 1, 1),
            arguments=[
                ctypes.c_uint32(self.n),
                ctypes.c_uint32(commit),
                ctypes.c_uint32(tick),
                *(ctypes.c_uint64(self.device[name].ptr) for name in self.host),
            ],
        )
        self.driver.synchronize()
        for name in ("traces", "last"):
            self.driver.copy_device_to_host(self.host[name], self.device[name])
        values = list(self.host["traces"])
        if any(not math.isfinite(x) or x < 0 for x in values):
            raise ValueError("CUDA neuron traces must remain finite and nonnegative")
        return values[: self.n], values[self.n :], list(self.host["last"])

    def begin(self, tick: int) -> tuple[list[float], list[float], list[int]]:
        self._validate_tick(tick, False)
        result = self._execute(tick, False)
        self._awaiting_commit = True
        return result

    def commit(
        self, tick: int, spikes: Sequence[int]
    ) -> tuple[list[float], list[float], list[int]]:
        self._validate_tick(tick, True)
        if any(type(i) is not int or not 0 <= i < self.n for i in spikes):
            raise ValueError("invalid CUDA neuron trace spike index")
        selected = set(spikes)
        if len(selected) != len(spikes):
            raise ValueError("duplicate CUDA neuron trace spikes")
        self.host["spikes"][:] = [int(i in selected) for i in range(self.n)]
        self.driver.copy_host_to_device(self.device["spikes"], self.host["spikes"])
        result = self._execute(tick, True)
        self._awaiting_commit = False
        self.completed_ticks += 1
        return result
