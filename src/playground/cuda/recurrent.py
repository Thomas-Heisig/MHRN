"""Compatibility re-export for Wave-4 recurrent CUDA reference."""

from src.acceleration.cuda.driver import CudaDriver
from src.acceleration.cuda.errors import CudaDriverError
from src.acceleration.cuda.memory import DeviceAllocation
from src.acceleration.cuda.nvrtc import compile_cuda_source
from src.acceleration.cuda.recurrent import (
    RecurrentInputs,
    cpu_recurrent_reference,
    execute_recurrent,
    recurrent_fixture,
    recurrent_parity,
    validate_recurrent_inputs,
)
from src.acceleration.cuda.recurrent import backend as canonical_backend

__all__ = [
    "CudaDriver",
    "CudaDriverError",
    "DeviceAllocation",
    "RecurrentInputs",
    "canonical_backend",
    "compile_cuda_source",
    "cpu_recurrent_reference",
    "execute_recurrent",
    "recurrent_fixture",
    "recurrent_parity",
    "validate_recurrent_inputs",
]
