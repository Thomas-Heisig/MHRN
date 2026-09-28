"""Actual Builder synaptic emission with host traversal RNG and arrival order."""

from __future__ import annotations

import ctypes
import math
from typing import Any

from .runtime import CudaDriver, CudaDriverError, DeviceAllocation, DriverModule


class BuilderSynapseStepper:
    """Reuse bounded buffers for emission and per-tick recovery/decay."""

    def __init__(self, driver: CudaDriver, loaded: DriverModule, capacity: int) -> None:
        if type(capacity) is not int or not 1 <= capacity <= 20000:
            raise ValueError("invalid CUDA synaptic capacity")
        self.driver, self.capacity = driver, capacity
        self.emit_kernel = driver.kernel(loaded, "pan_synaptic_emit")
        self.recover_kernel = driver.kernel(loaded, "pan_synaptic_recover")
        self.reward_kernel = driver.kernel(loaded, "pan_synaptic_reward")
        self.device: dict[str, DeviceAllocation] = {}
        self.host: dict[str, Any] = {
            "input": (ctypes.c_double * (5 * capacity))(),
            "output": (ctypes.c_double * (2 * capacity))(),
        }
        self.emitted_events = 0
        self.recovery_calls = 0
        self.reward_calls = 0
        try:
            for name in self.host:
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

    def _execute(
        self,
        rows: list[tuple[float, float, float, float, float]],
        *,
        stp: bool,
        first: float,
        second: float,
        kernel: DriverModule,
    ) -> list[tuple[float, float]]:
        count = len(rows)
        if (
            count > self.capacity
            or any(
                len(row) != 5 or any(not math.isfinite(x) for x in row) for row in rows
            )
            or not all(math.isfinite(x) for x in (first, second))
        ):
            raise ValueError("invalid CUDA synaptic shape/non-finite input")
        if not count:
            return []
        self.host["input"][: 5 * count] = [x for row in rows for x in row]
        self.driver.copy_host_to_device(
            self.device["input"], self.host["input"], size_bytes=5 * count * 8
        )
        args: list[object] = [
            ctypes.c_uint32(count),
            ctypes.c_uint32(bool(stp)),
            ctypes.c_double(first),
            ctypes.c_double(second),
            ctypes.c_uint64(self.device["input"].ptr),
            ctypes.c_uint64(self.device["output"].ptr),
        ]
        self.driver.launch_kernel(
            kernel, grid=((count + 127) // 128, 1, 1), block=(128, 1, 1), arguments=args
        )
        self.driver.synchronize()
        self.driver.copy_device_to_host(
            self.host["output"], self.device["output"], size_bytes=2 * count * 8
        )
        values = list(self.host["output"][: 2 * count])
        if any(not math.isfinite(x) for x in values):
            raise ValueError("non-finite CUDA synaptic output")
        return [(values[2 * i], values[2 * i + 1]) for i in range(count)]

    def emit(
        self,
        rows: list[tuple[float, float, float, float, float]],
        *,
        stp: bool,
        gaba: float,
        ratio: float,
    ) -> list[tuple[float, float]]:
        if (
            not math.isfinite(gaba)
            or gaba < 0
            or not math.isfinite(ratio)
            or ratio <= 0
        ):
            raise ValueError("invalid CUDA inhibitory scaling")
        for _weight, available, amplitude, draw, inhibitory in rows:
            if (
                not 0 <= available <= 1
                or not 0 <= amplitude <= 1
                or not 0 <= draw < 1
                or inhibitory not in (0, 1)
            ):
                raise ValueError("invalid CUDA STP/amplitude/RNG descriptor")
        result = self._execute(
            rows, stp=stp, first=gaba, second=ratio, kernel=self.emit_kernel
        )
        self.emitted_events += len(rows)
        return result

    def recover(
        self,
        weights: list[float],
        resources: list[float],
        *,
        stp: bool,
        decay: float,
        maximum: float,
    ) -> list[tuple[float, float]]:
        if (
            len(weights) != len(resources)
            or not 0 <= decay <= 1
            or not 0 < maximum <= 100
            or any(not 0 <= x <= 1 for x in resources)
        ):
            raise ValueError("invalid CUDA recovery/decay parameters")
        result = self._execute(
            [(w, r, 0.0, 0.0, 0.0) for w, r in zip(weights, resources)],
            stp=stp,
            first=decay,
            second=maximum,
            kernel=self.recover_kernel,
        )
        if result:
            self.recovery_calls += 1
        return result

    def reward(
        self,
        weights: list[float],
        eligibility: list[float],
        ages: list[int],
        *,
        scale: float,
        reward: float,
        maximum: float,
        window: int,
        respect_window: bool,
    ) -> list[float]:
        if (
            len(weights) != len(eligibility)
            or len(weights) != len(ages)
            or not 0 < maximum <= 100
            or type(window) is not int
            or window < 0
            or any(type(age) is not int for age in ages)
        ):
            raise ValueError("invalid CUDA live reward shape/window")
        rows = [
            (w, e, float(age), float(window), maximum)
            for w, e, age in zip(weights, eligibility, ages)
        ]
        values = self._execute(
            rows,
            stp=respect_window,
            first=scale,
            second=reward,
            kernel=self.reward_kernel,
        )
        if values:
            self.reward_calls += 1
        return [w for w, _ in values]
