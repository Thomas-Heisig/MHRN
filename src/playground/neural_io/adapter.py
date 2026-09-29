"""Playground adapter backed by the canonical MHRN neural-I/O adapter."""

from __future__ import annotations

from dataclasses import dataclass

from src.embodiment.neural_io_adapter import NeuralIOAreaAdapter
from src.embodiment.neural_symbiosis import NetworkAreaAdapter


@dataclass(slots=True)
class PlaygroundIOAreaAdapter(NeuralIOAreaAdapter):
    """Playground identity wrapper around the canonical area adapter."""

    area_id: str = "playground.io.reference"
    architecture: str = "Playground Neural I/O Reference Adapter"


def adapter_contract_check() -> bool:
    """Return whether the Playground wrapper satisfies the runtime Protocol."""

    return isinstance(PlaygroundIOAreaAdapter(), NetworkAreaAdapter)


__all__ = ["PlaygroundIOAreaAdapter", "adapter_contract_check"]
