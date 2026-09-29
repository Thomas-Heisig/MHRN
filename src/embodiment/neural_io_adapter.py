"""Framework-neutral neural-I/O area adapter for MHRN embodiment gateways."""

from __future__ import annotations

from dataclasses import dataclass

from .models import JSONValue
from .neural_symbiosis import NetworkAreaAdapter


@dataclass(slots=True)
class NeuralIOAreaAdapter:
    """Minimal deterministic area satisfying :class:`NetworkAreaAdapter`.

    The adapter is deliberately state-free and has no direct access to MHRN
    neural-core state. Neural encoding/decoding remains a separate codec plane.
    """

    area_id: str = "mhrn.neural_io.reference"
    architecture: str = "MHRN Neural I/O Reference Adapter"

    def process(self, payload: JSONValue, tick: int) -> JSONValue:
        if tick < 0:
            raise ValueError("tick must be non-negative")
        return payload


def neural_io_adapter_contract_check() -> bool:
    """Return whether the canonical adapter satisfies the gateway Protocol."""

    adapter: NetworkAreaAdapter = NeuralIOAreaAdapter()
    return (
        callable(adapter.process)
        and bool(adapter.area_id)
        and bool(adapter.architecture)
    )


__all__ = ["NeuralIOAreaAdapter", "neural_io_adapter_contract_check"]
