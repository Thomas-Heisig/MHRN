"""Experience Engine for controlled, single-consumption learning loops."""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from src.embodiment.controlled import ControlledEmbodimentAgent
from src.embodiment.loop_contract import CycleContract, valid_tick
from src.embodiment.models import ActionCommand, EnvironmentObservation, SensorFrame
from src.embodiment.sensor import SensorAdapter
from src.embodiment.task_outcome import TaskOutcome, TaskOutcomeVerifier
from src.learning.learning_engine import LearningEngine
from src.memory import MemoryWorldModel
from src.memory.neural_episodic import NeuralEpisodicMemory
from src.profiles import BehaviorProfile

Encoder = Callable[[SensorFrame], Mapping[int, float]]
Decoder = Callable[[Any, SensorFrame], ActionCommand | tuple[ActionCommand, ...] | None]


@dataclass(frozen=True, slots=True)
class ExperienceStep:
    """Immutable audit record for one perception-action-feedback cycle."""

    tick: int
    frame: SensorFrame
    action: ActionCommand | None
    observation: EnvironmentObservation | None
    reward: float
    outcome: TaskOutcome | None = None


@dataclass(slots=True)
class ExperienceEngine:
    """Connect a controlled sensor loop to the real learning engine.

    Rewards are accepted only from environment observations. No language
    model, configuration value, or decoder output can write a reward.
    A consumed cycle cannot be retried after a downstream observer fails.
    """

    sensor: SensorAdapter
    network: Any
    encoder: Encoder
    decoder: Decoder
    embodiment: ControlledEmbodimentAgent
    learning: LearningEngine | None = None
    outcome_verifier: TaskOutcomeVerifier = field(default_factory=TaskOutcomeVerifier)
    memory: MemoryWorldModel | None = None
    neural_memory: NeuralEpisodicMemory | None = None
    behavior_profile: BehaviorProfile | None = None
    last_step: ExperienceStep | None = None
    _pending_frame: SensorFrame | None = None
    _pending_prediction: Any = None
    _cycle: CycleContract = field(default_factory=CycleContract, init=False)

    def reset(self, seed: int | None = None) -> EnvironmentObservation:
        """Reset the environment and episode-local cycle state, not safety stops."""

        self._abort_cycle()
        observation = self.embodiment.reset(seed)
        self.last_step = None
        self._cycle.reset()
        episode_id = f"episode-{self.embodiment.episode}"
        if self.memory is not None:
            self.memory.reset_episode(episode_id)
        if self.neural_memory is not None:
            self.neural_memory.reset_episode(episode_id)
        return observation

    def _abort_cycle(self) -> None:
        self._cycle.abort()
        self._pending_frame = None
        self._pending_prediction = None

    def step(self, tick: int) -> ExperienceStep:
        """Run one complete sensor, network, action, feedback and reward step."""

        self.prepare(tick)
        try:
            result = self.network.step()
        except Exception:
            self._abort_cycle()
            raise
        return self.complete(tick, result)

    def prepare(self, tick: int) -> SensorFrame:
        """Validate and encode input before exactly one existing runtime tick."""

        self._cycle.begin(tick)
        try:
            if not self.sensor.active:
                raise RuntimeError("experience sensor is inactive")
            frame = self.sensor.sample(tick)
            if (
                not valid_tick(frame.tick)
                or frame.tick != tick
                or frame.sensor_id != self.sensor.sensor_id
                or frame.modality != self.sensor.modality
            ):
                raise ValueError("sensor frame identity or tick mismatch")
            currents = dict(self.encoder(frame))
            if any(
                type(neuron_id) is not int
                or neuron_id < 0
                or isinstance(value, bool)
                or not math.isfinite(value)
                for neuron_id, value in currents.items()
            ):
                raise ValueError(
                    "encoder currents must have valid IDs and finite values"
                )
            self.network.inject_current_batch(currents)
            self._pending_frame = frame
            return frame
        except Exception:
            self._abort_cycle()
            raise

    def complete(self, tick: int, result: Any) -> ExperienceStep:
        """Consume before side effects; late failures cannot replay an action."""

        self._cycle.consume(tick)
        frame = self._pending_frame
        self._pending_frame = None
        self._pending_prediction = None
        if frame is None or frame.tick != tick:
            raise RuntimeError("complete() requires a matching prepare() call")
        observation = None
        decoded = self.decoder(result, frame)
        if isinstance(decoded, tuple):
            action: ActionCommand | None = (
                self.behavior_profile.select_action(decoded, tick=tick)
                if self.behavior_profile is not None
                else (decoded[0] if decoded else None)
            )
        else:
            action = decoded
        if action is not None and (not valid_tick(action.tick) or action.tick != tick):
            raise ValueError("action tick must match the prepared cycle")
        prediction = (
            None if self.memory is None else self.memory.predict(frame, action, tick)
        )
        if action is not None:
            observation = self.embodiment.step(action)
        outcome = (
            TaskOutcome(False, False, 0.0, "no environment observation")
            if observation is None
            else self.outcome_verifier.verify(observation)
        )
        reward = outcome.reward
        if not math.isfinite(reward):
            raise ValueError("environment reward must be finite")
        if self.learning is not None and observation is not None:
            self.learning.set_reward(reward, tick)
        record = ExperienceStep(tick, frame, action, observation, reward, outcome)
        if self.memory is not None:
            self.memory.complete(frame, action, observation, tick, prediction)
        if self.neural_memory is not None:
            self.neural_memory.record(result, frame, observation)
        if self.behavior_profile is not None:
            self.behavior_profile.update(success=outcome.success, tick=tick)
        self.last_step = record
        return record

    def attach_runtime(self, runtime: Any) -> None:
        """Attach to a RuntimeController without taking ownership of ticks."""

        runtime.add_pre_hook(self.prepare)
        runtime.add_hook(self.complete)


__all__ = ["ExperienceEngine", "ExperienceStep"]
