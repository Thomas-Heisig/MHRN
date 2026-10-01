"""Validated synaptic-only transfer state; not a resumable full-network checkpoint."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast


@dataclass(frozen=True)
class SynapticCheckpoint:
    n_neurons: int
    neuron_model: str
    edges: tuple[tuple[int, int, float, int], ...]

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> "SynapticCheckpoint":
        if payload.get("schema") != "PAN_SYNAPTIC_TRANSFER_V1":
            raise ValueError("unsupported synaptic checkpoint schema")
        n, model, raw = (
            payload.get("n_neurons"),
            payload.get("neuron_model"),
            payload.get("edges"),
        )
        if (
            type(n) is not int
            or not 2 <= n <= 1024
            or not isinstance(model, str)
            or not isinstance(raw, list)
        ):
            raise ValueError("invalid synaptic checkpoint header")
        rows = cast(list[object], raw)
        if len(rows) > 20_000:
            raise ValueError("synaptic checkpoint exceeds edge capacity")
        edges: list[tuple[int, int, float, int]] = []
        for raw_row in rows:
            if not isinstance(raw_row, list) or len(cast(list[object], raw_row)) != 4:
                raise ValueError("invalid synaptic checkpoint row")
            source, target, weight, delay = cast(list[object], raw_row)
            if (
                type(source) is not int
                or type(target) is not int
                or type(delay) is not int
                or isinstance(weight, bool)
                or not isinstance(weight, (int, float))
            ):
                raise ValueError("invalid synaptic checkpoint types")
            edges.append((source, target, float(weight), delay))
        checkpoint = cls(n, model, tuple(edges))
        checkpoint.validate(
            n_neurons=n,
            neuron_model=model,
            expected_edges={(s, t) for s, t, _, _ in edges},
        )
        return checkpoint

    def validate(
        self, *, n_neurons: int, neuron_model: str, expected_edges: set[tuple[int, int]]
    ) -> None:
        if self.n_neurons != n_neurons or self.neuron_model != neuron_model:
            raise ValueError("synaptic checkpoint model/population mismatch")
        seen: set[tuple[int, int]] = set()
        for source, target, weight, delay in self.edges:
            if (
                type(source) is not int
                or type(target) is not int
                or not 0 <= source < n_neurons
                or not 0 <= target < n_neurons
                or type(delay) is not int
                or not 1 <= delay <= 64
                or isinstance(weight, bool)
                or not math.isfinite(weight)
                or not 0 <= weight <= 100
            ):
                raise ValueError("invalid synaptic checkpoint entry")
            if (source, target) in seen:
                raise ValueError("duplicate synaptic checkpoint edge")
            seen.add((source, target))
        if seen != expected_edges:
            raise ValueError("synaptic checkpoint topology mismatch")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": "PAN_SYNAPTIC_TRANSFER_V1",
            "n_neurons": self.n_neurons,
            "neuron_model": self.neuron_model,
            "edges": [list(edge) for edge in self.edges],
            "scope": "WEIGHTS_AND_DELAYS_ONLY_NEURON_AND_POLICY_STATE_RESET",
        }

    def digest(self) -> str:
        return hashlib.sha256(
            json.dumps(self.to_dict(), sort_keys=True, allow_nan=False).encode()
        ).hexdigest()
