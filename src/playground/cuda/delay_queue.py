"""Resident bounded delay ring with ordered emissions and explicit snapshot/restore."""

from __future__ import annotations

import ctypes
import math
from collections.abc import Sequence
from typing import Any

from .runtime import CudaDriver, CudaDriverError, DeviceAllocation, DriverModule


def _is_number(value: object) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float))


class DeviceDelayQueue:
    def __init__(
        self, driver: CudaDriver, loaded: DriverModule, n_neurons: int, capacity: int
    ) -> None:
        if (
            type(n_neurons) is not int
            or not 1 <= n_neurons <= 1024
            or type(capacity) is not int
            or not 1 <= capacity <= 20000
        ):
            raise ValueError("invalid CUDA delay queue capacity")
        self.driver, self.n, self.capacity = driver, n_neurons, capacity
        self.consume_kernel = driver.kernel(loaded, "pan_delay_consume")
        self.enqueue_kernel = driver.kernel(loaded, "pan_delay_enqueue")
        self.device: dict[str, DeviceAllocation] = {}
        self.host: dict[str, Any] = {}
        self.consumed_ticks = 0
        self.enqueued_events = 0
        try:
            for name, count, kind in (
                ("queue", 65 * self.n, ctypes.c_double),
                ("currents", self.n, ctypes.c_double),
                ("targets", capacity, ctypes.c_uint32),
                ("delays", capacity, ctypes.c_uint32),
                ("amplitudes", capacity, ctypes.c_double),
                ("invalid", 1, ctypes.c_uint32),
            ):
                self.host[name] = (kind * count)()
                self.device[name] = driver.alloc_device(ctypes.sizeof(self.host[name]))
            driver.copy_host_to_device(self.device["queue"], self.host["queue"])
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

    @staticmethod
    def _tick(tick: int) -> None:
        if type(tick) is not int or not 0 <= tick < 2**32:
            raise ValueError("CUDA queue tick must be uint32")

    def consume(self, tick: int) -> list[float]:
        self._tick(tick)
        self.driver.launch_kernel(
            self.consume_kernel,
            grid=((self.n + 127) // 128, 1, 1),
            block=(128, 1, 1),
            arguments=[
                ctypes.c_uint32(self.n),
                ctypes.c_uint32(tick % 65),
                ctypes.c_uint64(self.device["queue"].ptr),
                ctypes.c_uint64(self.device["currents"].ptr),
            ],
        )
        self.driver.synchronize()
        self.driver.copy_device_to_host(self.host["currents"], self.device["currents"])
        values = list(self.host["currents"])
        if any(not math.isfinite(x) for x in values):
            raise ValueError("CUDA delay current is non-finite")
        self.consumed_ticks += 1
        return values

    def enqueue(self, tick: int, events: Sequence[tuple[int, int, float]]) -> None:
        self._tick(tick)
        count = len(events)
        if count > self.capacity or any(
            type(target) is not int
            or not 0 <= target < self.n
            or type(delay) is not int
            or not 1 <= delay <= 64
            or not _is_number(amplitude)
            or not math.isfinite(amplitude)
            for target, delay, amplitude in events
        ):
            raise ValueError("invalid CUDA delay event")
        if not count:
            return
        self.host["targets"][:count] = [e[0] for e in events]
        self.host["delays"][:count] = [e[1] for e in events]
        self.host["amplitudes"][:count] = [e[2] for e in events]
        self.host["invalid"][0] = 0
        for name, size in (
            ("targets", count * 4),
            ("delays", count * 4),
            ("amplitudes", count * 8),
            ("invalid", 4),
        ):
            self.driver.copy_host_to_device(
                self.device[name], self.host[name], size_bytes=size
            )
        args: list[object] = [
            ctypes.c_uint32(self.n),
            ctypes.c_uint32(count),
            ctypes.c_uint32(tick),
        ]
        args.extend(
            ctypes.c_uint64(self.device[name].ptr)
            for name in ("targets", "delays", "amplitudes", "queue", "invalid")
        )
        self.driver.launch_kernel(
            self.enqueue_kernel,
            grid=((self.n + 127) // 128, 1, 1),
            block=(128, 1, 1),
            arguments=args,
        )
        self.driver.synchronize()
        self.driver.copy_device_to_host(self.host["invalid"], self.device["invalid"])
        if self.host["invalid"][0]:
            raise ValueError("CUDA delay accumulation is non-finite")
        self.enqueued_events += count

    def snapshot(self) -> list[list[float]]:
        self.driver.copy_device_to_host(self.host["queue"], self.device["queue"])
        values = list(self.host["queue"])
        if any(not math.isfinite(x) for x in values):
            raise ValueError("CUDA queue snapshot is non-finite")
        return [values[i * self.n : (i + 1) * self.n] for i in range(65)]

    def restore(self, rows: Sequence[Sequence[float]]) -> None:
        if len(rows) != 65 or any(len(row) != self.n for row in rows):
            raise ValueError("CUDA queue snapshot shape mismatch")
        if any(not _is_number(x) for row in rows for x in row):
            raise ValueError("CUDA queue snapshot values must be numbers")
        values = [float(x) for row in rows for x in row]
        if any(not math.isfinite(x) for x in values):
            raise ValueError("CUDA queue snapshot is non-finite")
        self.host["queue"][:] = values
        self.driver.copy_host_to_device(self.device["queue"], self.host["queue"])
