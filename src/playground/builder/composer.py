"""Composition helpers for multi-layer exploratory playground networks."""

from __future__ import annotations

from dataclasses import dataclass, field

from ..models import Topology
from .network_builder import TopologyBuilder


@dataclass(slots=True)
class PlaygroundComposer:
    """Compose named neuron layers into one neutral playground topology."""

    n_neurons: int
    seed: int = 12345
    dimensions: int = 5
    _builder: TopologyBuilder = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._builder = TopologyBuilder(
            n=self.n_neurons,
            seed=self.seed,
            dimensions=self.dimensions,
        )

    def add_layer(
        self, name: str, *, dim: int, n: int, **options: object
    ) -> "PlaygroundComposer":
        self._builder.add_layer(name, dim=dim, n=n, **options)
        return self

    def connect(
        self,
        source: str,
        target: str,
        *,
        rule: str = "random",
        budget: int = 128,
    ) -> "PlaygroundComposer":
        self._builder.connect(source, target, rule=rule, budget=budget)
        return self

    def build(self) -> Topology:
        return self._builder.build()
