"""Backend-neutral execution contract for canonical MHRN runtimes."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


def _assert_json_serializable(value: object, *, field: str) -> None:
    try:
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be canonical JSON-serializable") from exc


@dataclass(frozen=True, slots=True)
class BackendCapabilities:
    """Declared execution features and bounded limits of one backend."""

    supports_recurrent: bool
    supports_plasticity: bool
    supports_pan_hyperstate: bool
    supports_structural_plasticity: bool
    max_neurons: int
    max_ticks: int
    deterministic: bool

    def __post_init__(self) -> None:
        if self.max_neurons < 1:
            raise ValueError("max_neurons must be >= 1")
        if self.max_ticks < 1:
            raise ValueError("max_ticks must be >= 1")


@dataclass(frozen=True, slots=True)
class BackendState:
    """Backend-neutral continuation state.

    The payload must be data-only and canonical-JSON serializable. Opaque
    device pointers, CUDA handles and process-local object identities are
    forbidden.
    """

    tick: int
    payload: Mapping[str, object]
    state_digest: str

    def __post_init__(self) -> None:
        if self.tick < 0:
            raise ValueError("tick must be >= 0")
        if not self.state_digest:
            raise ValueError("state_digest must not be empty")
        _assert_json_serializable(dict(self.payload), field="payload")


@dataclass(frozen=True, slots=True)
class StepResult:
    """One canonical backend step result."""

    tick: int
    spikes: tuple[int, ...]
    state_digest: str
    metrics: Mapping[str, object]

    def __post_init__(self) -> None:
        if self.tick < 0:
            raise ValueError("tick must be >= 0")
        if not self.state_digest:
            raise ValueError("state_digest must not be empty")
        if any(spike < 0 for spike in self.spikes):
            raise ValueError("spike neuron ids must be >= 0")
        _assert_json_serializable(dict(self.metrics), field="metrics")


@dataclass(frozen=True, slots=True)
class RunResult:
    """Bounded backend run result."""

    ticks_requested: int
    steps: tuple[StepResult, ...]
    final_state: BackendState
    execution_fingerprint: str

    def __post_init__(self) -> None:
        if self.ticks_requested < 1:
            raise ValueError("ticks_requested must be >= 1")
        if len(self.steps) > self.ticks_requested:
            raise ValueError("steps cannot exceed ticks_requested")
        if not self.execution_fingerprint:
            raise ValueError("execution_fingerprint must not be empty")


@runtime_checkable
class ExecutionBackend(Protocol):
    """Backend-neutral execution surface consumed by MHRN runtime control."""

    def initialize(self, config: Mapping[str, object], seed: int) -> None:
        """Initialize from a data-only configuration and deterministic seed."""

    def step(self, tick: int) -> StepResult:
        """Advance exactly one canonical tick."""

    def run(self, ticks: int) -> RunResult:
        """Advance a bounded number of ticks."""

    def snapshot(self) -> BackendState:
        """Capture backend-neutral continuation state."""

    def restore(self, state: BackendState) -> None:
        """Restore a previously captured backend-neutral state."""

    def capabilities(self) -> BackendCapabilities:
        """Return declared capabilities and bounded limits."""
