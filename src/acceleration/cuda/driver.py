"""Canonical CUDA Driver API wrapper.

This module owns device/context/module/memory/launch mechanics only. It has no
Playground, PAN, Gate-IR or scientific semantics.
"""

from __future__ import annotations

import ctypes
import math
import os
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from .errors import CudaDriverError, CudaRuntimeUnavailable
from .memory import DeviceAllocation
from .preflight import CooperativePreflight, validate_cuda_block_size

# CUDA Driver API attribute IDs from cuda.h.
_CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT = 16
_CU_DEVICE_ATTRIBUTE_COOPERATIVE_LAUNCH = 95

@dataclass(frozen=True, slots=True)
class DriverModule:
    """Opaque handles returned by CUDA Driver API loading."""

    context: ctypes.c_void_p
    module: ctypes.c_void_p
    function: ctypes.c_void_p
    device_ordinal: int

class CudaDriver:
    """Minimal ctypes wrapper for CUDA-1 loading, memory and kernel launch."""

    def __init__(self, library: str | None = None) -> None:
        candidates = (
            [library]
            if library
            else (["nvcuda.dll"] if os.name == "nt" else ["libcuda.so.1", "libcuda.so"])
        )
        loader = (
            getattr(ctypes, "WinDLL", ctypes.CDLL) if os.name == "nt" else ctypes.CDLL
        )
        last_error: OSError | None = None
        for candidate in candidates:
            try:
                self._lib = loader(candidate)
                break
            except OSError as exc:
                last_error = exc
        else:
            names = ", ".join(candidates)
            raise CudaRuntimeUnavailable(
                f"CUDA driver library not available; tried: {names}"
            ) from last_error
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
        lib.cuMemAlloc_v2.argtypes = [
            ctypes.POINTER(ctypes.c_uint64),
            ctypes.c_size_t,
        ]
        lib.cuMemAlloc_v2.restype = ctypes.c_int
        lib.cuMemFree_v2.argtypes = [ctypes.c_uint64]
        lib.cuMemFree_v2.restype = ctypes.c_int
        lib.cuMemGetInfo_v2.argtypes = [
            ctypes.POINTER(ctypes.c_size_t),
            ctypes.POINTER(ctypes.c_size_t),
        ]
        lib.cuMemGetInfo_v2.restype = ctypes.c_int
        lib.cuMemcpyHtoD_v2.argtypes = [
            ctypes.c_uint64,
            ctypes.c_void_p,
            ctypes.c_size_t,
        ]
        lib.cuMemcpyHtoD_v2.restype = ctypes.c_int
        lib.cuMemcpyDtoH_v2.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint64,
            ctypes.c_size_t,
        ]
        lib.cuMemcpyDtoH_v2.restype = ctypes.c_int
        lib.cuLaunchKernel.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.POINTER(ctypes.c_void_p),
        ]
        lib.cuLaunchKernel.restype = ctypes.c_int
        lib.cuCtxSynchronize.argtypes = []
        lib.cuCtxSynchronize.restype = ctypes.c_int

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

    def alloc_device(self, size_bytes: int) -> DeviceAllocation:
        """Allocate device memory owned by the current CUDA context."""

        if size_bytes <= 0:
            raise ValueError("size_bytes must be positive")
        ptr = ctypes.c_uint64()
        self._check(
            self._lib.cuMemAlloc_v2(ctypes.byref(ptr), size_bytes),
            "cuMemAlloc_v2",
        )
        return DeviceAllocation(ptr=int(ptr.value), size_bytes=size_bytes)

    def free_device(self, allocation: DeviceAllocation) -> None:
        """Release one device allocation."""

        if allocation.ptr:
            self._check(
                self._lib.cuMemFree_v2(ctypes.c_uint64(allocation.ptr)),
                "cuMemFree_v2",
            )

    def memory_info(self) -> tuple[int, int]:
        """Return free and total bytes for the current CUDA context."""

        free_bytes = ctypes.c_size_t()
        total_bytes = ctypes.c_size_t()
        self._check(
            self._lib.cuMemGetInfo_v2(
                ctypes.byref(free_bytes),
                ctypes.byref(total_bytes),
            ),
            "cuMemGetInfo_v2",
        )
        return int(free_bytes.value), int(total_bytes.value)

    def copy_host_to_device(
        self,
        allocation: DeviceAllocation,
        source: ctypes.Array[Any],
        *,
        size_bytes: int | None = None,
    ) -> None:
        """Copy a ctypes-backed host buffer to device memory."""

        count = allocation.size_bytes if size_bytes is None else size_bytes
        host_bytes = ctypes.sizeof(source)
        if count < 0 or count > allocation.size_bytes:
            raise ValueError("host-to-device copy exceeds device allocation")
        if count > host_bytes:
            raise ValueError(
                f"host-to-device copy exceeds host buffer: {count} > {host_bytes}"
            )
        self._check(
            self._lib.cuMemcpyHtoD_v2(
                ctypes.c_uint64(allocation.ptr),
                ctypes.cast(source, ctypes.c_void_p),
                count,
            ),
            "cuMemcpyHtoD_v2",
        )

    def copy_device_to_host(
        self,
        destination: ctypes.Array[Any],
        allocation: DeviceAllocation,
        *,
        size_bytes: int | None = None,
    ) -> None:
        """Copy device memory into a ctypes-backed host buffer."""

        count = allocation.size_bytes if size_bytes is None else size_bytes
        host_bytes = ctypes.sizeof(destination)
        if count < 0 or count > allocation.size_bytes:
            raise ValueError("device-to-host copy exceeds device allocation")
        if count > host_bytes:
            raise ValueError(
                f"device-to-host copy exceeds host buffer: {count} > {host_bytes}"
            )
        self._check(
            self._lib.cuMemcpyDtoH_v2(
                ctypes.cast(destination, ctypes.c_void_p),
                ctypes.c_uint64(allocation.ptr),
                count,
            ),
            "cuMemcpyDtoH_v2",
        )

    def launch_kernel(
        self,
        loaded: DriverModule,
        *,
        grid: tuple[int, int, int],
        block: tuple[int, int, int],
        arguments: Sequence[object],
        dynamic_shared_bytes: int = 0,
    ) -> None:
        """Launch a loaded kernel with CUDA Driver API argument packing."""

        if min(*grid, *block) <= 0:
            raise ValueError("grid and block dimensions must be positive")
        storage = list(arguments)
        kernel_params = (ctypes.c_void_p * len(storage))()
        for index, argument in enumerate(storage):
            kernel_params[index] = ctypes.cast(
                ctypes.byref(argument), ctypes.c_void_p  # type: ignore[arg-type]
            )
        self._check(
            self._lib.cuLaunchKernel(
                loaded.function,
                grid[0],
                grid[1],
                grid[2],
                block[0],
                block[1],
                block[2],
                dynamic_shared_bytes,
                None,
                kernel_params,
                None,
            ),
            "cuLaunchKernel",
        )

    def synchronize(self) -> None:
        """Synchronize the current CUDA context."""

        self._check(self._lib.cuCtxSynchronize(), "cuCtxSynchronize")

    def launch_cooperative(
        self,
        loaded: DriverModule,
        *,
        n_neurons: int,
        block_size: int,
        arguments: Sequence[object],
    ) -> CooperativePreflight:
        """Launch a resident 1D grid only after checking actual kernel occupancy."""
        preflight = self.cooperative_preflight(
            loaded, n_neurons=n_neurons, block_size=block_size
        )
        if n_neurons < 1 or not preflight.launch_fits:
            raise ValueError(
                "cooperative grid exceeds the device/kernel resident capacity"
            )
        launch = self._lib.cuLaunchCooperativeKernel
        launch.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_void_p),
        ]
        launch.restype = ctypes.c_int
        storage = list(arguments)
        parameters = (ctypes.c_void_p * len(storage))()
        for index, argument in enumerate(storage):
            parameters[index] = ctypes.cast(
                ctypes.byref(argument), ctypes.c_void_p  # type: ignore[arg-type]
            )
        self._check(
            launch(
                loaded.function,
                preflight.required_blocks,
                1,
                1,
                block_size,
                1,
                1,
                0,
                None,
                parameters,
            ),
            "cuLaunchCooperativeKernel",
        )
        return preflight

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

    def kernel(self, loaded: DriverModule, name: str) -> DriverModule:
        """Borrow another function in the same owned module/context; do not unload it separately."""
        if not name or not name.isascii() or not name.replace("_", "").isalnum():
            raise ValueError("invalid CUDA kernel symbol")
        function = ctypes.c_void_p()
        self._check(
            self._lib.cuModuleGetFunction(
                ctypes.byref(function), loaded.module, name.encode("ascii")
            ),
            "cuModuleGetFunction",
        )
        return DriverModule(
            loaded.context, loaded.module, function, loaded.device_ordinal
        )

    def unload(self, loaded: DriverModule) -> None:
        module_error: CudaDriverError | None = None
        if loaded.module.value:
            try:
                self._check(
                    self._lib.cuModuleUnload(loaded.module),
                    "cuModuleUnload",
                )
            except CudaDriverError as exc:
                module_error = exc
        if loaded.context.value:
            try:
                self._check(
                    self._lib.cuCtxDestroy_v2(loaded.context),
                    "cuCtxDestroy_v2",
                )
            except CudaDriverError:
                if module_error is None:
                    raise
        if module_error is not None:
            raise module_error

    def cooperative_preflight(
        self,
        loaded: DriverModule,
        *,
        n_neurons: int,
        block_size: int = 128,
        dynamic_shared_bytes: int = 0,
    ) -> CooperativePreflight:
        """Calculate whether the full cooperative grid can be resident."""

        validate_cuda_block_size(block_size)
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
