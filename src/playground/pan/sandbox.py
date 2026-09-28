"""Minimal deterministic embodied sandbox for PAN live sessions."""

from __future__ import annotations

import hashlib
import json
import math
from collections import deque
from dataclasses import dataclass, field
from typing import Protocol, cast


@dataclass(slots=True)
class Joint:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    mass: float = 1.0


Spring = tuple[str, str, float, float]


def _empty_joints() -> dict[str, Joint]:
    return {}


def _empty_muscles() -> dict[str, float]:
    return {}


def _empty_springs() -> list[Spring]:
    return []


class PostureAnalyzer:
    """Compute a bounded posture score for the exploratory stick figure."""

    def __init__(self, config: object) -> None:
        self.config = config
        self.previous_score: float | None = None

    def compute(self, figure: "StickFigureSandbox") -> float:
        neck = figure.joints["neck"]
        hip = figure.joints["hip"]
        tilt = math.atan2(neck.x - hip.x, max(1e-6, neck.y - hip.y))
        upright = max(
            0.0,
            1.0
            - abs(tilt)
            / max(float(getattr(self.config, "posture_tilt_max", 1.0)), 1e-6),
        )
        height = max(
            0.0,
            min(
                1.0,
                hip.y
                / max(float(getattr(self.config, "posture_target_height", 1.0)), 1e-6),
            ),
        )
        speed = math.hypot(hip.vx, hip.vy)
        stability = max(
            0.0,
            1.0
            - speed
            / max(float(getattr(self.config, "posture_velocity_max", 5.0)), 1e-6),
        )
        symmetry = max(
            0.0, 1.0 - abs(figure.joints["foot_l"].y - figure.joints["foot_r"].y) / 0.5
        )
        weights = (
            float(getattr(self.config, "posture_weight_upright", 0.4)),
            float(getattr(self.config, "posture_weight_height", 0.3)),
            float(getattr(self.config, "posture_weight_stability", 0.2)),
            float(getattr(self.config, "posture_weight_symmetry", 0.1)),
        )
        total = sum(weights) or 1.0
        score = max(
            0.0,
            min(
                1.0,
                (
                    weights[0] * upright
                    + weights[1] * height
                    + weights[2] * stability
                    + weights[3] * symmetry
                )
                / total,
            ),
        )
        self.previous_score = score
        return score


class RewardTrigger:
    """Turn posture trajectories into continuous reward and discrete events."""

    def __init__(self, config: object) -> None:
        self.config = config
        self.good_counter = 0
        self.was_low = False

    def evaluate(
        self, score: float, previous_score: float | None
    ) -> tuple[float, list[str]]:
        reward = (score - 0.5) * float(
            getattr(self.config, "reward_continuous_alpha", 0.1)
        )
        events: list[str] = []
        if score > float(getattr(self.config, "trigger_good_score", 0.85)):
            self.good_counter += 1
            if self.good_counter == int(
                getattr(self.config, "trigger_good_duration", 10)
            ):
                reward += float(getattr(self.config, "trigger_good_reward", 1.0))
                events.append("GOOD_POSTURE")
        else:
            self.good_counter = 0
        if previous_score is not None and score - previous_score < float(
            getattr(self.config, "trigger_falling_rate", -0.05)
        ):
            reward += float(getattr(self.config, "trigger_falling_reward", -1.0))
            events.append("FALLING")
        if score < float(getattr(self.config, "trigger_warning_score", 0.4)):
            reward += float(getattr(self.config, "trigger_warning_reward", -0.3))
            self.was_low = True
            events.append("WARNING")
        if self.was_low and score > 0.6:
            reward += float(getattr(self.config, "trigger_recovery_bonus", 2.0))
            self.was_low = False
            events.append("RECOVERED")
        if score < float(getattr(self.config, "trigger_collapse_score", 0.1)):
            reward += float(getattr(self.config, "trigger_collapse_reward", -5.0))
            events.append("COLLAPSED")
        return reward, events


class _LiveSessionLike(Protocol):
    @property
    def config(self) -> object: ...

    def inject_vector(
        self, values: list[float], *, duration_ticks: int, gain: float
    ) -> None: ...
    def step(self, ticks: int = 32) -> dict[str, object]: ...


@dataclass(slots=True)
class StickFigureSandbox:
    """Simple point-mass/spring body with four muscle controls."""

    joints: dict[str, Joint] = field(default_factory=_empty_joints)
    muscles: dict[str, float] = field(default_factory=_empty_muscles)
    echo: deque[list[float]] = field(default_factory=lambda: deque(maxlen=10))
    springs: list[Spring] = field(default_factory=_empty_springs, init=False)
    tick: int = 0
    world_x_min: float = -2.0
    world_x_max: float = 2.0
    ground_friction: float = 0.3

    def reset_to_initial_pose(self) -> None:
        initial = {
            "head": (0.0, 1.8),
            "neck": (0.0, 1.5),
            "shoulder_l": (-0.3, 1.4),
            "shoulder_r": (0.3, 1.4),
            "hip": (0.0, 1.0),
            "knee_l": (-0.15, 0.5),
            "knee_r": (0.15, 0.5),
            "foot_l": (-0.15, 0.0),
            "foot_r": (0.15, 0.0),
        }
        for name, (x, y) in initial.items():
            joint = self.joints[name]
            joint.x, joint.y, joint.vx, joint.vy = x, y, 0.0, 0.0
        self.muscles = {key: 0.0 for key in self.muscles}
        self.echo.clear()
        self.tick = 0

    def __post_init__(self) -> None:
        if not self.joints:
            self.joints = {
                "head": Joint(0.0, 1.8, mass=5.0),
                "neck": Joint(0.0, 1.5, mass=3.0),
                "shoulder_l": Joint(-0.3, 1.4, mass=2.0),
                "shoulder_r": Joint(0.3, 1.4, mass=2.0),
                "hip": Joint(0.0, 1.0, mass=5.0),
                "knee_l": Joint(-0.15, 0.5, mass=2.0),
                "knee_r": Joint(0.15, 0.5, mass=2.0),
                "foot_l": Joint(-0.15, 0.0, mass=1.0),
                "foot_r": Joint(0.15, 0.0, mass=1.0),
            }
        if not self.muscles:
            self.muscles = {
                "hip_l": 0.0,
                "hip_r": 0.0,
                "knee_l": 0.0,
                "knee_r": 0.0,
            }
        self.springs = [
            ("head", "neck", 0.3, 50.0),
            ("neck", "hip", 0.5, 100.0),
            ("neck", "shoulder_l", 0.3, 80.0),
            ("neck", "shoulder_r", 0.3, 80.0),
            ("hip", "knee_l", 0.5, 100.0),
            ("hip", "knee_r", 0.5, 100.0),
            ("knee_l", "foot_l", 0.5, 100.0),
            ("knee_r", "foot_r", 0.5, 100.0),
        ]

    def _angle(self, a: str, b: str) -> float:
        left, right = self.joints[a], self.joints[b]
        return math.atan2(right.y - left.y, right.x - left.x)

    def receptors(self) -> list[float]:
        hip = self.joints["hip"]
        neck = self.joints["neck"]
        values = [
            self._angle("hip", "knee_l") / math.pi,
            self._angle("hip", "knee_r") / math.pi,
            self._angle("knee_l", "foot_l") / math.pi,
            self._angle("knee_r", "foot_r") / math.pi,
            1.0 if self.joints["foot_l"].y <= 0.01 else 0.0,
            1.0 if self.joints["foot_r"].y <= 0.01 else 0.0,
            max(0.0, min(1.0, hip.y / 2.0)),
            max(-1.0, min(1.0, hip.vx / 2.0)),
            math.atan2(neck.x - hip.x, max(1e-6, neck.y - hip.y)) / math.pi,
        ]
        return values

    def apply_action(self, action: int | None) -> None:
        for key in self.muscles:
            self.muscles[key] *= 0.85
        if action is None:
            return
        keys = ["hip_l", "hip_r", "knee_l", "knee_r"]
        self.muscles[keys[action % 4]] = 1.0

    def step(self, dt: float = 0.01) -> dict[str, object]:
        forces = {
            name: [0.0, -9.81 * joint.mass] for name, joint in self.joints.items()
        }
        for a, b, rest, stiffness in self.springs:
            ja, jb = self.joints[a], self.joints[b]
            dx, dy = jb.x - ja.x, jb.y - ja.y
            dist = max(1e-6, math.hypot(dx, dy))
            magnitude = stiffness * (dist - rest) / dist
            fx, fy = magnitude * dx, magnitude * dy
            forces[a][0] += fx
            forces[a][1] += fy
            forces[b][0] -= fx
            forces[b][1] -= fy

        # Four bounded actuator forces. These are engineering controls, not
        # anatomical muscle models.
        forces["knee_l"][0] += 20.0 * self.muscles["hip_l"]
        forces["knee_r"][0] += 20.0 * self.muscles["hip_r"]
        forces["foot_l"][1] += 15.0 * self.muscles["knee_l"]
        forces["foot_r"][1] += 15.0 * self.muscles["knee_r"]

        contacts = 0
        for name, joint in self.joints.items():
            joint.vx += forces[name][0] / joint.mass * dt
            joint.vy += forces[name][1] / joint.mass * dt
            joint.vx *= 0.995
            joint.vy *= 0.995
            joint.x += joint.vx * dt
            joint.y += joint.vy * dt
            joint.x = max(self.world_x_min, min(self.world_x_max, joint.x))
            if joint.x in (self.world_x_min, self.world_x_max):
                joint.vx = 0.0
            if joint.y < 0.0:
                joint.y = 0.0
                if joint.vy < 0.0:
                    joint.vy = 0.0
                joint.vx *= max(0.0, 1.0 - self.ground_friction)
                contacts += 1

        self.tick += 1
        hip = self.joints["hip"]
        audio_level = min(1.0, abs(hip.vx) * 0.2 + contacts * 0.05)
        visual = [
            max(-1.0, min(1.0, hip.x / 2.0)),
            max(0.0, min(1.0, hip.y / 2.0)),
            max(-1.0, min(1.0, hip.vx / 2.0)),
        ]
        self.echo.append(visual)
        delayed = self.echo[0] if len(self.echo) == self.echo.maxlen else [0.0] * 3
        return {
            "classification": "PLAYGROUND_STICK_FIGURE_SANDBOX",
            "scientific_evidence": False,
            "tick": self.tick,
            "receptors": self.receptors(),
            "muscles": dict(self.muscles),
            "audio": {
                "mode": "SYNTHETIC_ACTIVITY_PROXY",
                "level": audio_level,
                "fft_status": "NOT_IMPLEMENTED_REFERENCE_SANDBOX",
            },
            "visual": visual,
            "echo": [value * 0.3 for value in delayed],
            "joints": {
                name: {
                    "x": joint.x,
                    "y": joint.y,
                    "vx": joint.vx,
                    "vy": joint.vy,
                }
                for name, joint in self.joints.items()
            },
            "llm": {
                "status": "EXISTING_GATEWAY_INTERFACE_REQUIRED",
                "direct_ollama_http_created": False,
            },
        }


class EmbodiedEnvironment:
    """Shared deterministic world used by batch and live PAN execution."""

    def __init__(self, config: object) -> None:
        self.config = config
        self.world = StickFigureSandbox()
        self.last_frame: dict[str, object] | None = None
        self.posture = PostureAnalyzer(config)
        self.reward_trigger = RewardTrigger(config)
        self.episode_tick = 0
        self.total_ticks = 0
        self.trajectory_digest = hashlib.sha256()
        self.terminals = 0
        self.reward_total = 0.0
        self.last_reward = 0.0
        self.reward_vector: list[float] = []
        self.frames: deque[dict[str, object]] = deque(maxlen=128)

    def sensor_vector(self) -> list[float]:
        receptors = self.world.receptors()
        audio = 0.0
        echo_values: list[float] = []
        if self.last_frame is not None:
            raw_audio = self.last_frame.get("audio")
            if isinstance(raw_audio, dict):
                raw_level: object = cast(dict[str, object], raw_audio).get(
                    "level", 0.0
                )
                if isinstance(raw_level, (int, float)):
                    audio = float(raw_level)
            raw_echo = self.last_frame.get("echo")
            if isinstance(raw_echo, list):
                echo_values_raw = cast(list[object], raw_echo)
                echo_values = [
                    float(value)
                    for value in echo_values_raw
                    if isinstance(value, (int, float))
                ]
        combined = list(receptors) + [audio] + echo_values
        return combined

    def advance(
        self, action: int | None, *, dt_seconds: float = 0.01
    ) -> dict[str, object]:
        self.world.apply_action(action)
        frame = self.world.step(dt=dt_seconds)
        frame["pan_action"] = action
        previous_score = self.posture.previous_score
        posture_score = self.posture.compute(self.world)
        config = self.config
        if bool(getattr(config, "posture_reward_enabled", False)):
            reward, reward_events = self.reward_trigger.evaluate(
                posture_score, previous_score
            )
        else:
            reward, reward_events = 0.0, []
        reward_vector = [
            0.0
            for _ in range(
                max(
                    int(getattr(config, "input_channels", 1)),
                    int(getattr(config, "posture_score_channel", 2)) + 1,
                    int(getattr(config, "reward_event_channel", 3)) + 1,
                )
            )
        ]
        if bool(getattr(config, "posture_reward_enabled", False)):
            reward_vector[int(getattr(config, "posture_score_channel", 2))] = (
                posture_score * float(getattr(config, "posture_current_scale", 25.0))
            )
            reward_vector[int(getattr(config, "reward_event_channel", 3))] = (
                reward * float(getattr(config, "reward_event_scale", 25.0))
            )
            self.reward_vector = reward_vector
        self.episode_tick += 1
        terminal = None
        if bool(getattr(config, "episode_termination_enabled", True)):
            if (
                posture_score < float(getattr(config, "trigger_collapse_score", 0.1))
                or self.world.joints["hip"].y < 0.3
            ):
                terminal = "COLLAPSED"
            elif abs(self.world.joints["hip"].x) > 1.9:
                terminal = "OUT_OF_BOUNDS"
            elif self.episode_tick >= int(getattr(config, "episode_max_ticks", 256)):
                terminal = "TIMEOUT"
        frame["posture_score"] = posture_score
        frame["reward"] = reward
        frame["reward_events"] = reward_events
        frame["terminal"] = terminal
        self.trajectory_digest.update(
            json.dumps(frame, sort_keys=True, allow_nan=False).encode("utf-8")
        )
        self.frames.append(frame)
        self.total_ticks += 1
        self.reward_total += reward
        self.last_reward = reward
        if terminal:
            self.terminals += 1
        self.last_frame = frame
        if terminal and bool(getattr(config, "episode_reset_on_collapse", True)):
            self.world.reset_to_initial_pose()
            self.posture.previous_score = None
            self.reward_trigger.good_counter = 0
            self.reward_trigger.was_low = False
            self.episode_tick = 0
        return frame

    def summary(self) -> dict[str, object]:
        return {
            "classification": "PLAYGROUND_PAN_EMBODIED_SANDBOX",
            "backend": "CPU_REFERENCE",
            "scientific_evidence": False,
            "ticks": self.total_ticks,
            "full_trajectory_digest": self.trajectory_digest.hexdigest(),
            "terminals": self.terminals,
            "reward_total": self.reward_total,
            "world": self.last_frame,
            "frames": list(self.frames),
            "learning_claim": "EXPLORATORY_REFERENCE_ONLY",
        }


class PANEmbodiedSandboxSession(EmbodiedEnvironment):
    """Couple a persistent PAN live session to the shared environment."""

    def __init__(self, live_session: _LiveSessionLike) -> None:
        super().__init__(live_session.config)
        self.live_session = live_session

    def step(self, ticks: int = 1) -> dict[str, object]:
        if ticks < 1 or ticks > 512:
            raise ValueError("sandbox ticks must be between 1 and 512")
        frames: list[dict[str, object]] = []
        pan_result: dict[str, object] = {}
        for _ in range(ticks):
            self.live_session.inject_vector(
                self.sensor_vector(), duration_ticks=1, gain=25.0
            )
            pan_result = self.live_session.step(1)
            actions = pan_result.get("actions", [])
            action = None
            if isinstance(actions, list) and actions:
                raw_action = cast(list[object], actions)[-1]
                if isinstance(raw_action, (int, float)):
                    action = int(raw_action)
            frame = self.advance(action)
            frames.append(frame)
            if self.reward_vector:
                self.live_session.inject_vector(
                    self.reward_vector, duration_ticks=1, gain=1.0
                )

        return {
            "classification": "PLAYGROUND_PAN_EMBODIED_SANDBOX",
            "scientific_evidence": False,
            "ticks": ticks,
            "world": self.last_frame,
            "pan": pan_result,
            "frames": frames[-32:],
            "learning_claim": "EXPLORATORY_REFERENCE_ONLY",
            "posture_score": (
                self.last_frame.get("posture_score", 0.0) if self.last_frame else 0.0
            ),
            "reward": self.last_frame.get("reward", 0.0) if self.last_frame else 0.0,
            "reward_events": (
                self.last_frame.get("reward_events", []) if self.last_frame else []
            ),
            "terminal": self.last_frame.get("terminal") if self.last_frame else None,
        }
