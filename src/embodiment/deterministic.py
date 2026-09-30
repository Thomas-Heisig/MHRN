"""Deterministic environment used for the first Alpha.7 loop proof."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .environment import EnvironmentAdapter
from .models import ActionCommand, EnvironmentKind, EnvironmentObservation, JSONValue


@dataclass(slots=True)
class DeterministicTargetEnvironment(EnvironmentAdapter):
    """One-dimensional target task with deterministic seeded reset."""

    target: int = 3
    position: int = 0
    tick: int = 0

    @property
    def environment_id(self) -> str:
        return "deterministic-target-v1"

    @property
    def kind(self) -> EnvironmentKind:
        return EnvironmentKind.SIMULATED

    def reset(self, seed: int | None = None) -> EnvironmentObservation:
        self.position = 0 if seed is None else seed % 2
        self.tick = 0
        return self._observation(0.0)

    def step(self, action: ActionCommand) -> EnvironmentObservation:
        self.tick += 1
        if action.action == "right":
            self.position += 1
        elif action.action == "left":
            self.position -= 1
        reward = 1.0 if self.position == self.target else 0.0
        return self._observation(reward)

    def _observation(self, reward: float) -> EnvironmentObservation:
        return EnvironmentObservation(
            tick=self.tick,
            state={"position": self.position, "target": self.target},
            reward=reward,
            terminated=self.position == self.target,
        )

    def snapshot_state(self) -> dict[str, JSONValue]:
        """Return the complete continuation state used by frozen-world replay."""

        return {
            "target": self.target,
            "position": self.position,
            "tick": self.tick,
        }

    def restore_state(self, state: Mapping[str, JSONValue]) -> None:
        """Restore a previously frozen deterministic world state."""

        required = ("target", "position", "tick")
        if set(state) != set(required):
            raise ValueError("deterministic world state must contain target/position/tick")
        values: list[int] = []
        for field in required:
            value = state[field]
            if type(value) is not int:
                raise ValueError(f"{field} must be an integer")
            values.append(value)
        target, position, tick = values
        if tick < 0:
            raise ValueError("tick must be >= 0")
        self.target = target
        self.position = position
        self.tick = tick

    def rng_fingerprint(self) -> str:
        """This environment has no runtime RNG after explicit state restore."""

        return "deterministic-target:no-runtime-rng:v1"
