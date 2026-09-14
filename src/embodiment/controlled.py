"""Fail-closed authorization and safety boundary for embodiment I/O."""

from __future__ import annotations

from dataclasses import dataclass, field

from .actuator import ActuatorAdapter
from .audit import ActionAuditTrail
from .connections import ConnectionDescriptor
from .environment import EnvironmentAdapter
from .loop_contract import DispatchBudget, valid_tick
from .models import (
    ActionCommand,
    ActionReceipt,
    ActuatorResult,
    EmbodimentMetrics,
    EnvironmentObservation,
    SensorFrame,
)
from .sensor import SensorAdapter


@dataclass(slots=True)
class ControlledSensorAdapter:
    """Fail-closed authorization boundary for sensor sampling."""

    sensor: SensorAdapter
    descriptor: ConnectionDescriptor

    def sample(self, tick: int) -> SensorFrame | None:
        if (
            not valid_tick(tick)
            or self.sensor.sensor_id != self.descriptor.connection_id
            or not self.descriptor.available
            or not self.descriptor.authorized
            or not self.descriptor.active
            or not self.sensor.active
        ):
            return None
        if self.sensor.modality not in self.descriptor.modalities:
            return None
        frame = self.sensor.sample(tick)
        if (
            frame.tick != tick
            or not valid_tick(frame.tick)
            or frame.sensor_id != self.sensor.sensor_id
            or frame.modality != self.sensor.modality
        ):
            return None
        return frame


@dataclass(slots=True)
class ControlledEmbodimentAgent:
    """Execute only authorized, capable and rate-limited external actions.

    Dispatch is serialized by the owning runtime. An attempted dispatch consumes
    budget even on rejection or failure. Unknown effects latch the emergency stop;
    neither software retry nor reset is permission to clear that stop.
    """

    environment: EnvironmentAdapter
    actuator: ActuatorAdapter
    descriptor: ConnectionDescriptor
    audit: ActionAuditTrail = field(default_factory=ActionAuditTrail)
    max_actions_per_tick: int = 1
    require_human_override: bool = False
    _emergency_stopped: bool = False
    episode: int = 0
    episode_reward: float = 0.0
    last_observation: EnvironmentObservation | None = None
    last_action: ActionCommand | None = None
    _approved_override_ticks: set[int] = field(default_factory=set[int])
    last_receipt: ActionReceipt | None = None
    _command_sequence: int = 0
    max_pending_overrides: int = 128
    _dispatch_budget: DispatchBudget = field(default_factory=DispatchBudget, init=False)

    def __post_init__(self) -> None:
        self._dispatch_budget.denial(0, self.max_actions_per_tick)
        if (
            type(self.max_pending_overrides) is not int
            or self.max_pending_overrides <= 0
        ):
            raise ValueError("max_pending_overrides must be a positive integer")

    def reset(self, seed: int | None = None) -> EnvironmentObservation:
        observation = self.environment.reset(seed)
        self.episode += 1
        self.episode_reward = 0.0
        self.last_action = None
        self.last_receipt = None
        self.last_observation = observation
        self._dispatch_budget.reset()
        self._approved_override_ticks.clear()
        return observation

    def emergency_stop(self) -> None:
        self._emergency_stopped = True

    def clear_emergency_stop(self, *, human_approved: bool) -> None:
        if not human_approved:
            raise PermissionError("human approval is required to clear emergency stop")
        self._emergency_stopped = False

    def approve_override(self, tick: int, *, human_approved: bool) -> None:
        if not human_approved:
            raise PermissionError("human approval is required for override")
        if not valid_tick(tick):
            raise ValueError("override tick must be a non-negative integer")
        if self._dispatch_budget.tick is not None and tick < self._dispatch_budget.tick:
            raise ValueError("cannot approve an expired override tick")
        if (
            tick not in self._approved_override_ticks
            and len(self._approved_override_ticks) >= self.max_pending_overrides
        ):
            raise ValueError("pending override capacity exceeded")
        self._approved_override_ticks.add(tick)

    def step(self, command: ActionCommand) -> EnvironmentObservation | None:
        self._command_sequence += 1
        command_id = f"{self.descriptor.connection_id}:{self._command_sequence}"
        result, reason = self._authorize(command)
        if result is not None:
            self.last_receipt = ActionReceipt(
                command_id,
                False,
                False,
                False,
                True,
                error=reason,
                effect_observed=False,
            )
            self.audit.append(
                self.descriptor.connection_id,
                command,
                result,
                accepted=False,
                reason=reason,
            )
            return None
        self._dispatch_budget.reserve(command.tick, self.max_actions_per_tick)
        self._approved_override_ticks = {
            tick for tick in self._approved_override_ticks if tick >= command.tick
        }
        accepted = False
        phase = "actuator_error"
        try:
            actuator_result = self.actuator.apply(command)
            accepted = actuator_result.accepted
            self.last_receipt = ActionReceipt(
                command_id,
                accepted,
                True,
                False,
                not accepted,
                error=None if accepted else actuator_result.message,
                effect_observed=None if accepted else False,
            )
            phase = "audit_error"
            self.audit.append(
                self.descriptor.connection_id,
                command,
                actuator_result,
                accepted=accepted,
                reason="accepted" if accepted else actuator_result.message,
            )
            if not accepted:
                return None
            phase = "feedback_error"
            observation = self.environment.step(command)
            self.last_receipt = ActionReceipt(
                command_id,
                True,
                True,
                True,
                False,
                latency=max(0, observation.tick - command.tick),
                effect_observed=True,
            )
            self.last_action = command
            self.last_observation = observation
            self.episode_reward += observation.reward
            return observation
        except Exception as error:
            self.emergency_stop()
            reason = f"{phase}:{type(error).__name__}"
            self.last_receipt = ActionReceipt(
                command_id,
                accepted,
                True,
                False,
                True,
                error=reason,
                effect_observed=None,
            )
            if phase != "audit_error":
                self.audit.append(
                    self.descriptor.connection_id,
                    command,
                    ActuatorResult(False, reason),
                    accepted=False,
                    reason=reason,
                )
            raise

    def metrics(self) -> EmbodimentMetrics:
        """Expose only feedback returned by the controlled environment."""
        observation = self.last_observation
        return EmbodimentMetrics(
            environment_kind=self.environment.kind.value,
            active_actuators=1 if self.actuator.active else 0,
            episode=self.episode,
            episode_reward=self.episode_reward,
            last_reward=0.0 if observation is None else observation.reward,
            last_action="" if self.last_action is None else self.last_action.action,
            last_observation_state=None if observation is None else observation.state,
            last_observation_tick=None if observation is None else observation.tick,
            last_observation_terminated=(
                None if observation is None else observation.terminated
            ),
            last_observation_truncated=(
                None if observation is None else observation.truncated
            ),
        )

    def _authorize(self, command: ActionCommand) -> tuple[ActuatorResult | None, str]:
        if self._emergency_stopped:
            return ActuatorResult(False, "emergency stop active"), "emergency_stop"
        if (
            command.actuator_id != self.descriptor.connection_id
            or command.actuator_id != self.actuator.actuator_id
        ):
            return ActuatorResult(False, "actuator target mismatch"), "target_mismatch"
        if not self.descriptor.available or not self.descriptor.authorized:
            return ActuatorResult(False, "actuator is not authorized"), "unauthorized"
        if not self.descriptor.active or not self.actuator.active:
            return ActuatorResult(False, "actuator is inactive"), "inactive"
        if command.action not in self.descriptor.capabilities:
            return (
                ActuatorResult(False, "capability is not granted"),
                "capability_denied",
            )
        reason = self._dispatch_budget.denial(command.tick, self.max_actions_per_tick)
        if reason is not None:
            return ActuatorResult(False, reason), reason
        if (
            self.require_human_override
            and command.tick not in self._approved_override_ticks
        ):
            return ActuatorResult(False, "human override required"), "override_required"
        return None, ""
