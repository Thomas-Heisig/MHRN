"""Compatibility re-export for neural-I/O contracts promoted into MHRN.

The canonical definitions live in :mod:`src.embodiment.neural_io_contracts`.
Playground code intentionally imports the same class objects so existing
sessions/codecs remain connected while MHRN no longer depends on Playground.
"""

from src.embodiment.neural_io_contracts import (
    BoundaryFrame,
    CodecContract,
    DecodeResult,
    InterfacePhase,
    NeuralRole,
    PopulationLayout,
    SpikeEvent,
    SpikeFrame,
    canonical_payload_bytes,
    event_digest,
    readout_digest,
)

__all__ = [
    "BoundaryFrame",
    "CodecContract",
    "DecodeResult",
    "InterfacePhase",
    "NeuralRole",
    "PopulationLayout",
    "SpikeEvent",
    "SpikeFrame",
    "canonical_payload_bytes",
    "event_digest",
    "readout_digest",
]
