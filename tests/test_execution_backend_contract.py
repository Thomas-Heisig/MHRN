"""Canonical ExecutionBackend contract tests."""

from __future__ import annotations

from collections.abc import Mapping

import pytest

from src.runtime.backend import (
    BackendCapabilities,
    BackendState,
    ExecutionBackend,
    RunResult,
    StepResult,
)


class FakeBackend:
    def __init__(self) -> None:
        self.tick = 0

    def initialize(self, config: Mapping[str, object], seed: int) -> None:
        assert seed >= 0
        assert isinstance(config, Mapping)
        self.tick = 0

    def step(self, tick: int) -> StepResult:
        self.tick = tick + 1
        return StepResult(
            self.tick,
            (),
            f"state-{self.tick}",
            {"tick": self.tick},
        )

    def run(self, ticks: int) -> RunResult:
        steps = tuple(self.step(self.tick) for _ in range(ticks))
        return RunResult(ticks, steps, self.snapshot(), "f" * 64)

    def snapshot(self) -> BackendState:
        return BackendState(self.tick, {"tick": self.tick}, f"state-{self.tick}")

    def restore(self, state: BackendState) -> None:
        self.tick = state.tick

    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            supports_recurrent=True,
            supports_plasticity=False,
            supports_pan_hyperstate=False,
            supports_structural_plasticity=False,
            max_neurons=1024,
            max_ticks=2000,
            deterministic=True,
        )


def test_fake_backend_satisfies_runtime_protocol() -> None:
    backend = FakeBackend()
    assert isinstance(backend, ExecutionBackend)
    backend.initialize({"model": "lif"}, 12345)
    result = backend.run(2)
    assert result.final_state.tick == 2
    backend.restore(BackendState(1, {"tick": 1}, "state-1"))
    assert backend.snapshot().tick == 1


def test_backend_state_rejects_opaque_non_serializable_payload() -> None:
    with pytest.raises(ValueError, match="canonical JSON-serializable"):
        BackendState(0, {"bad": object()}, "digest")
