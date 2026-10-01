"""Compatibility re-export for neural-I/O codecs promoted into MHRN.

Canonical codec/decoder implementations live in
:mod:`src.embodiment.neural_io_codecs`. Existing Playground callers import
the same function and catalog objects, preserving the Playground -> MHRN
dependency direction.
"""

from src.embodiment.neural_io_codecs import (
    CODEC_CATALOG,
    DECODER_CATALOG,
    DEFAULT_SYMBOL_VOCABULARY,
    decode_output,
    encode_input,
)

__all__ = [
    "CODEC_CATALOG",
    "DECODER_CATALOG",
    "DEFAULT_SYMBOL_VOCABULARY",
    "decode_output",
    "encode_input",
]
