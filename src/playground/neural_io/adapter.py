"""Framework-neutral peripheral adapter for Playground neural I/O."""

from __future__ import annotations

from dataclasses import dataclass

from src.embodiment.models import JSONValue
from src.embodiment.neural_symbiosis import NetworkAreaAdapter


@dataclass(slots=True)
class PlaygroundIOAreaAdapter:
    """Identity reference area satisfying NetworkAreaAdapter.

    It deliberately has no access to MHRN core state. Encoding into spikes is
    performed later by the explicit neural I/O codec plane.
    """

    area_id: str = "playground.io.reference"
    architecture: str = "Playground Neural I/O Reference Adapter"

    def process(self, payload: JSONValue, tick: int) -> JSONValue:
        if tick < 0:
            raise ValueError("tick must be non-negative")
        return payload


def adapter_contract_check() -> bool:
    """Return whether the reference adapter satisfies the runtime Protocol."""

    return isinstance(PlaygroundIOAreaAdapter(), NetworkAreaAdapter)
