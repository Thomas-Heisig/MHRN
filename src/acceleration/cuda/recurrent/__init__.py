"""Canonical bounded recurrent CUDA package."""

from .backend import (
    RecurrentInputs,
    cpu_recurrent_reference,
    execute_recurrent,
    recurrent_fixture,
    recurrent_parity,
    validate_recurrent_inputs,
)
from .config import SUPPORTED_MODELS, CudaReferenceModelProfile
from .reference import CPUReferenceBackend
from .state import recurrent_inputs_from_mapping, recurrent_inputs_to_mapping

__all__ = [
    "CPUReferenceBackend",
    "CudaReferenceModelProfile",
    "RecurrentInputs",
    "SUPPORTED_MODELS",
    "cpu_recurrent_reference",
    "execute_recurrent",
    "recurrent_fixture",
    "recurrent_inputs_from_mapping",
    "recurrent_inputs_to_mapping",
    "recurrent_parity",
    "validate_recurrent_inputs",
]
