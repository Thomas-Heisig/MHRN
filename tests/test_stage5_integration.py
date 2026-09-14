"""Stage-5 fault controls using real loop code and deterministic test adapters.

These are integration regressions, not SNN performance or biological evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

import pytest

from src.embodiment.connections import (
    ConnectionDescriptor,
    ConnectionKind,
    ConnectionStatus,
    RelationshipClass,
)
from src.embodiment.controlled import ControlledEmbodimentAgent, ControlledSensorAdapter
from src.embodiment.deterministic import DeterministicTargetEnvironment
from src.embodiment.models import ActionCommand, ActuatorResult, SensorFrame
from src.experience.engine import ExperienceEngine


@dataclass
class TestActuator:
    __test__ = False
    actuator_id: str = "target-actuator"
    active: bool = True
    mode: str = "accept"
    calls: int = 0

    def apply(self, command: ActionCommand) -> ActuatorResult:
        self.calls += 1
        if self.mode == "raise":
            raise OSError("actuator feedback unavailable")
        return ActuatorResult(self.mode == "accept", command.action)


@dataclass
class TestSensor:
    __test__ = False
    sensor_id: str = "target-sensor"
    modality: str = "position"
    active: bool = True
    offset: int = 0
    returned_id: str | None = None
    returned_modality: str | None = None

    def sample(self, tick: int) -> SensorFrame:
        return SensorFrame(
            self.returned_id or self.sensor_id,
            tick + self.offset,
            self.returned_modality or self.modality,
            {"signal": 1.0},
        )


@dataclass
class TestNetwork:
    __test__ = False
    fail: bool = False
    injected: list[dict[int, float]] = field(default_factory=list)

    def inject_current_batch(self, currents: dict[int, float]) -> None:
        self.injected.append(currents)

    def step(self) -> dict[str, tuple[int, ...]]:
        if self.fail:
            raise RuntimeError("network failure")
        return {"output_spike_ids": (1,)}


def agent_and_actuator(**kwargs: Any) -> tuple[ControlledEmbodimentAgent, TestActuator]:
    actuator = TestActuator()
    descriptor = ConnectionDescriptor(
        connection_id="target-actuator",
        name="Stage-5 deterministic actuator",
        kind=ConnectionKind.ACTUATOR,
        relationship=RelationshipClass.CONTROLLABLE,
        status=ConnectionStatus.CONNECTED,
        capabilities=("left", "right"),
        available=True,
        authorized=True,
        active=True,
    )
    agent = ControlledEmbodimentAgent(
        DeterministicTargetEnvironment(), actuator, descriptor, **kwargs
    )
    agent.reset(seed=42)
    return agent, actuator


def engine_and_actuator() -> tuple[ExperienceEngine, TestActuator]:
    agent, actuator = agent_and_actuator()
    return (
        ExperienceEngine(
            sensor=TestSensor(),
            network=TestNetwork(),
            encoder=lambda frame: {0: 1.0},
            decoder=lambda result, frame: ActionCommand(
                "target-actuator", frame.tick, "right"
            ),
            embodiment=agent,
        ),
        actuator,
    )


def test_wrong_target_is_denied_even_without_hub():
    agent, actuator = agent_and_actuator()
    assert agent.step(ActionCommand("another-device", 1, "right")) is None
    assert actuator.calls == 0
    assert agent.last_receipt.error == "target_mismatch"
    assert agent.audit.verify()


def test_descriptor_cannot_authorize_another_adapter():
    agent, actuator = agent_and_actuator()
    actuator.actuator_id = "another-device"
    assert agent.step(ActionCommand("target-actuator", 1, "right")) is None
    assert actuator.calls == 0


def test_rejected_dispatch_still_uses_budget():
    agent, actuator = agent_and_actuator()
    actuator.mode = "reject"
    assert agent.step(ActionCommand("target-actuator", 1, "right")) is None
    assert agent.step(ActionCommand("target-actuator", 1, "right")) is None
    assert actuator.calls == 1
    assert agent.last_receipt.error == "rate_limited"
    actuator.mode = "accept"
    assert agent.step(ActionCommand("target-actuator", 2, "right")) is not None


def test_old_tick_cannot_reopen_an_expired_dispatch_window():
    agent, actuator = agent_and_actuator()
    agent.step(ActionCommand("target-actuator", 10, "right"))
    assert agent.step(ActionCommand("target-actuator", 1, "right")) is None
    assert agent.last_receipt.error == "stale_tick"
    assert actuator.calls == 1


def test_actuator_exception_latches_stop_and_preserves_unknown_effect():
    agent, actuator = agent_and_actuator()
    actuator.mode = "raise"
    with pytest.raises(OSError):
        agent.step(ActionCommand("target-actuator", 1, "right"))
    assert agent.last_receipt.failed is True
    assert agent.last_receipt.effect_observed is None
    assert agent.last_receipt.error == "actuator_error:OSError"
    assert agent.audit.verify()
    assert agent.step(ActionCommand("target-actuator", 2, "right")) is None
    assert agent.last_receipt.error == "emergency_stop"
    agent.clear_emergency_stop(human_approved=True)
    assert agent.step(ActionCommand("target-actuator", 1, "right")) is None
    assert agent.last_receipt.error == "rate_limited"
    assert actuator.calls == 1


def test_feedback_exception_does_not_fabricate_reward_or_known_effect(monkeypatch):
    agent, actuator = agent_and_actuator()
    original = agent.last_observation

    def fail(self, command):
        raise OSError("environment feedback unavailable")

    monkeypatch.setattr(DeterministicTargetEnvironment, "step", fail)
    with pytest.raises(OSError):
        agent.step(ActionCommand("target-actuator", 1, "right"))
    assert actuator.calls == 1
    assert agent.last_receipt.accepted is True
    assert agent.last_receipt.completed is False
    assert agent.last_receipt.effect_observed is None
    assert agent.last_observation is original
    assert agent.episode_reward == 0.0


def test_reset_expires_overrides_and_budget_but_not_emergency_stop():
    agent, actuator = agent_and_actuator(require_human_override=True)
    agent.approve_override(1, human_approved=True)
    agent.step(ActionCommand("target-actuator", 1, "right"))
    agent.approve_override(2, human_approved=True)
    agent.emergency_stop()
    agent.reset(seed=42)
    assert agent.step(ActionCommand("target-actuator", 1, "right")) is None
    assert agent.last_receipt.error == "emergency_stop"
    agent.clear_emergency_stop(human_approved=True)
    assert agent.step(ActionCommand("target-actuator", 2, "right")) is None
    assert agent.last_receipt.error == "override_required"
    agent.approve_override(1, human_approved=True)
    assert agent.step(ActionCommand("target-actuator", 1, "right")) is not None
    assert actuator.calls == 2


def test_pending_override_storage_is_bounded():
    agent, _ = agent_and_actuator(max_pending_overrides=2)
    agent.approve_override(1, human_approved=True)
    agent.approve_override(2, human_approved=True)
    agent.approve_override(2, human_approved=True)
    with pytest.raises(ValueError, match="capacity"):
        agent.approve_override(3, human_approved=True)
    agent.step(ActionCommand("target-actuator", 2, "right"))
    agent.approve_override(3, human_approved=True)
    with pytest.raises(ValueError, match="expired"):
        agent.approve_override(1, human_approved=True)


@pytest.mark.parametrize(
    "options",
    [{"offset": -1}, {"returned_id": "foreign"}, {"returned_modality": "audio"}],
)
def test_sensor_boundary_rejects_stale_or_misidentified_frames(options):
    sensor = TestSensor(**options)
    agent, _ = agent_and_actuator()
    descriptor = replace(
        agent.descriptor,
        connection_id=sensor.sensor_id,
        kind=ConnectionKind.SENSOR,
        relationship=RelationshipClass.PERCEIVABLE,
        modalities=(sensor.modality,),
    )
    assert ControlledSensorAdapter(sensor, descriptor).sample(4) is None


def test_engine_rejects_stale_frame_before_current_injection():
    engine, actuator = engine_and_actuator()
    engine.sensor.offset = -1
    with pytest.raises(ValueError, match="identity or tick"):
        engine.prepare(3)
    assert engine.network.injected == []
    assert actuator.calls == 0
    with pytest.raises(RuntimeError, match="increase"):
        engine.prepare(3)


@pytest.mark.parametrize(
    "currents",
    [{0: float("nan")}, {0: float("inf")}, {-1: 1.0}, {True: 1.0}, {0: True}],
)
def test_invalid_encoder_currents_never_reach_network(currents):
    engine, actuator = engine_and_actuator()
    engine.encoder = lambda frame: currents
    with pytest.raises(ValueError, match="currents"):
        engine.prepare(1)
    assert engine.network.injected == []
    assert actuator.calls == 0


def test_prepare_and_complete_are_single_consumption():
    engine, actuator = engine_and_actuator()
    engine.prepare(1)
    with pytest.raises(RuntimeError, match="pending"):
        engine.prepare(2)
    engine.complete(1, {})
    with pytest.raises(RuntimeError, match="matching"):
        engine.complete(1, {})
    assert len(engine.network.injected) == 1
    assert actuator.calls == 1


def test_action_from_another_tick_is_not_dispatched():
    engine, actuator = engine_and_actuator()
    engine.decoder = lambda result, frame: ActionCommand("target-actuator", 99, "right")
    with pytest.raises(ValueError, match="action tick"):
        engine.step(1)
    assert actuator.calls == 0


def test_memory_failure_after_actuation_cannot_replay_action():
    class FailingObserver:
        def predict(self, frame, action, tick):
            return None

        def complete(self, *args):
            raise OSError("memory persistence failed")

    engine, actuator = engine_and_actuator()
    engine.memory = FailingObserver()
    with pytest.raises(OSError, match="persistence"):
        engine.step(1)
    with pytest.raises(RuntimeError, match="matching"):
        engine.complete(1, {})
    with pytest.raises(RuntimeError, match="increase"):
        engine.prepare(1)
    assert actuator.calls == 1


def test_network_failure_aborts_pending_cycle():
    engine, actuator = engine_and_actuator()
    engine.network.fail = True
    with pytest.raises(RuntimeError, match="network failure"):
        engine.step(1)
    with pytest.raises(RuntimeError, match="matching"):
        engine.complete(1, {})
    assert actuator.calls == 0
    engine.network.fail = False
    engine.step(2)
    assert actuator.calls == 1
