"""Topology and connectivity probes for playground results."""

from __future__ import annotations

from dataclasses import dataclass

from ..models import Topology


@dataclass(frozen=True, slots=True)
class ConnectivityProbe:
    topology: Topology

    def snapshot(self) -> dict[str, object]:
        n = len(self.topology.coordinates)
        in_degree = [0 for _ in range(n)]
        out_degree = [0 for _ in range(n)]
        for source, target in self.topology.edges:
            if 0 <= source < n and 0 <= target < n:
                out_degree[source] += 1
                in_degree[target] += 1
        return {
            "neuron_count": n,
            "edge_count": len(self.topology.edges),
            "dimensions": self.topology.dimensions,
            "in_degree": in_degree,
            "out_degree": out_degree,
            "mean_in_degree": sum(in_degree) / max(n, 1),
            "mean_out_degree": sum(out_degree) / max(n, 1),
            "max_in_degree": max(in_degree, default=0),
            "max_out_degree": max(out_degree, default=0),
        }
