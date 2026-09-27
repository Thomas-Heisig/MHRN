"""Composable topology builder for exploratory Playground use."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from ..models import Topology
from ..registry.topology_generators import build_topology


def _as_int(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{label} must be an integer")
    return value


@dataclass(slots=True)
class TopologyBuilder:
    """Fluent builder for one bounded exploratory topology."""

    n: int
    seed: int = 12345
    dimensions: int = 5
    layers: list[dict[str, object]] = field(default_factory=list)
    connections: list[dict[str, object]] = field(default_factory=list)

    def add_layer(
        self, name: str, dim: int, n: int, **options: object
    ) -> "TopologyBuilder":
        self.layers.append({"name": name, "dim": dim, "n": n, **options})
        return self

    def connect(
        self,
        source: str,
        target: str,
        rule: str = "random",
        budget: int = 128,
    ) -> "TopologyBuilder":
        self.connections.append(
            {"source": source, "target": target, "rule": rule, "budget": budget}
        )
        return self

    def build(self) -> Topology:
        if not 1 <= self.dimensions <= 32:
            raise ValueError("builder dimensions must be between 1 and 32")
        if not self.layers:
            topology_name = "mhrn_5d" if self.dimensions == 5 else "generic_nd"
            return build_topology(
                topology_name,
                self.n,
                max(self.n, self.n * 4),
                self.seed,
                dimensions=self.dimensions,
            )
        if sum(_as_int(layer["n"], "layer n") for layer in self.layers) != self.n:
            raise ValueError("layer neuron counts must sum to builder n")
        rng = random.Random(self.seed)
        coordinates: list[tuple[float, ...]] = []
        offsets: dict[str, tuple[int, int]] = {}
        cursor = 0
        for layer_index, layer in enumerate(self.layers):
            count = _as_int(layer["n"], "layer n")
            dim = _as_int(layer["dim"], "layer dim")
            offsets[str(layer["name"])] = (cursor, cursor + count)
            for local in range(count):
                point = [0.0 for _ in range(max(dim, self.dimensions))]
                point[0] = local / max(count - 1, 1)
                if len(point) > 1:
                    point[1] = layer_index / max(len(self.layers) - 1, 1)
                coordinates.append(tuple(point[: self.dimensions]))
            cursor += count
        edges: set[tuple[int, int]] = set()
        for spec in self.connections:
            source_lo, source_hi = offsets[str(spec["source"])]
            target_lo, target_hi = offsets[str(spec["target"])]
            budget = _as_int(spec["budget"], "connection budget")
            target_size = len(edges) + budget
            attempts = 0
            while len(edges) < target_size and attempts < budget * 50:
                attempts += 1
                source = rng.randrange(source_lo, source_hi)
                target = rng.randrange(target_lo, target_hi)
                if source != target:
                    edges.add((source, target))
        return Topology(
            "composed",
            self.dimensions,
            tuple(sorted(edges)),
            tuple(coordinates),
            {
                "layers": self.layers,
                "connections": self.connections,
                "seed": self.seed,
                "geometry_class": "composed_nd",
            },
        )
