"""Playground reference implementation of the MHRN Gateway Neural Interface.

This package is non-canonical PLAYGROUND infrastructure. It mirrors the
postulated MHRN boundary/codec/projection/readout separation without creating
scientific DATA or EVID.
"""

from .adapter import PlaygroundIOAreaAdapter, adapter_contract_check
from .codecs import (
    CODEC_CATALOG,
    DECODER_CATALOG,
    DEFAULT_SYMBOL_VOCABULARY,
)
from .contracts import (
    BoundaryFrame,
    CodecContract,
    DecodeResult,
    InterfacePhase,
    NeuralRole,
    PopulationLayout,
    SpikeEvent,
    SpikeFrame,
)
from .interface import NeuralIOInterface

__all__ = [
    "BoundaryFrame",
    "PlaygroundIOAreaAdapter",
    "adapter_contract_check",
    "CODEC_CATALOG",
    "CodecContract",
    "DECODER_CATALOG",
    "DEFAULT_SYMBOL_VOCABULARY",
    "DecodeResult",
    "InterfacePhase",
    "NeuralIOInterface",
    "NeuralRole",
    "PopulationLayout",
    "SpikeEvent",
    "SpikeFrame",
]
