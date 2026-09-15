from __future__ import annotations

from dataclasses import dataclass

import pytest

from src.embodiment import (
    ActionCommand,
    ActuatorResult,
    ConnectionDescriptor,
    ConnectionKind,
    ConnectionStatus,
    ControlledEmbodimentAgent,
    DeterministicTargetEnvironment,
    RelationshipClass,
    SystemSensorAdapter,
)
from src.embodiment.models import EnvironmentObservation, SensorFrame
from src.experience import ExperienceEngine
from src.memory.neural_episodic import (
    NeuralEpisodicMemory,
    NeuralEpisodicMemoryError,
    spike_ids_from_result,
)


def _frame(tick: int, *, sensor_id: str = "sensor", modality: str = "vision") -> SensorFrame:
    return SensorFrame(sensor_id, tick, modality, {"cue": tick})


def _observation(tick: int, label: str) -> EnvironmentObservation:
    return EnvironmentObservation(tick, {"label": label})


def test_partial_cue_recalls_matching_neural_episode_before_distractor() -> None:
    memory = NeuralEpisodicMemory(run_id="run", capacity=8)
    memory.reset_episode("episode-a")
    target = memory.record(
        {"spike_ids": (1, 2, 3, 4)}, _frame(1), _observation(1, "target")
    )
    memory.reset_episode("episode-b")
    memory.record(
        {"spike_ids": (8, 9, 10)}, _frame(2), _observation(2, "distractor")
    )

    matches = memory.recall((1, 2), sensor_id="sensor", modality="vision")

    assert target is not None
    assert matches[0].episode == target
    assert matches[0].cue_coverage == 1.0
    assert matches[0].score == pytest.approx(2.0 * 2 / 6)


def test_context_filter_prevents_cross_sensor_recall() -> None:
    memory = NeuralEpisodicMemory(run_id="run")
    memory.record({"spike_ids": (1, 2)}, _frame(1, sensor_id="camera-a"), None)
    memory.record({"spike_ids": (1, 2)}, _frame(2, sensor_id="camera-b"), None)

    matches = memory.recall((1,), sensor_id="camera-b", modality="vision")

    assert len(matches) == 1
    assert matches[0].episode.sensor_id == "camera-b"


def test_capacity_retention_and_restore_are_deterministic() -> None:
    memory = NeuralEpisodicMemory(run_id="run", capacity=2, retention_ticks=3)
    for tick in (1, 2, 5):
        memory.record({"spike_ids": (tick,)}, _frame(tick), _observation(tick, str(tick)))

    assert [item.tick for item in memory.episodes] == [5]
    restored = NeuralEpisodicMemory.from_state_dict(memory.state_dict())
    assert restored.state_dict() == memory.state_dict()
    assert restored.recall((5,))[0].episode.tick == 5


def test_corrupted_state_and_invalid_spike_ids_fail_closed() -> None:
    memory = NeuralEpisodicMemory(run_id="run")
    memory.record({"spike_ids": (1, 2)}, _frame(1), None)
    state = memory.state_dict()
    state["run_id"] = "tampered"

    with pytest.raises(NeuralEpisodicMemoryError, match="integrity"):
        NeuralEpisodicMemory.from_state_dict(state)
    with pytest.raises(NeuralEpisodicMemoryError, match="non-negative"):
        spike_ids_from_result({"spike_ids": (1, -1)})
    with pytest.raises(NeuralEpisodicMemoryError, match="non-negative"):
        spike_ids_from_result({"spike_ids": (True,)})


@dataclass
class _Actuator:
    actuator_id: str = "target-actuator"
    active: bool = True

    def apply(self, command: ActionCommand) -> ActuatorResult:
        return ActuatorResult(True, command.action)


@dataclass
class _Network:
    def inject_current_batch(self, currents: dict[int, float]) -> None:
        del currents

    def step(self) -> dict[str, tuple[int, ...]]:
        return {"spike_ids": (3, 7), "output_spike_ids": (7,)}


def _agent() -> ControlledEmbodimentAgent:
    descriptor = ConnectionDescriptor(
        connection_id="target-actuator",
        name="Target actuator",
        kind=ConnectionKind.ACTUATOR,
        relationship=RelationshipClass.CONTROLLABLE,
        status=ConnectionStatus.CONNECTED,
        capabilities=("right",),
        available=True,
        authorized=True,
        active=True,
    )
    agent = ControlledEmbodimentAgent(
        DeterministicTargetEnvironment(), _Actuator(), descriptor
    )
    agent.reset(seed=42)
    return agent


def test_experience_engine_binds_actual_network_pattern_to_episode() -> None:
    neural_memory = NeuralEpisodicMemory(run_id="run")
    engine = ExperienceEngine(
        sensor=SystemSensorAdapter(lambda tick: {"cue": "A"}),
        network=_Network(),
        encoder=lambda frame: {0: 1.0},
        decoder=lambda result, frame: ActionCommand(
            "target-actuator", frame.tick, "right"
        ),
        embodiment=_agent(),
        neural_memory=neural_memory,
    )

    engine.reset(seed=42)
    step = engine.step(1)

    assert step.observation is not None
    assert len(neural_memory.episodes) == 1
    assert neural_memory.episodes[0].spike_ids == (3, 7)
    assert neural_memory.episodes[0].episode_id == "episode-2"
    assert neural_memory.episodes[0].actual_state == step.observation.state
