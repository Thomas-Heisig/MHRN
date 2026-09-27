"""Minimal deterministic embodied sandbox for PAN live sessions."""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(slots=True)
class Joint:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    mass: float = 1.0


class _LiveSessionLike(Protocol):
    def inject_vector(self, values: list[float], *, duration_ticks: int, gain: float) -> None: ...
    def step(self, ticks: int = 32) -> dict[str, object]: ...


@dataclass(slots=True)
class StickFigureSandbox:
    """Simple point-mass/spring body with four muscle controls."""

    joints: dict[str, Joint] = field(default_factory=dict)
    muscles: dict[str, float] = field(default_factory=dict)
    echo: deque[list[float]] = field(default_factory=lambda: deque(maxlen=10))
    springs: list[tuple[str, str, float, float]] = field(
        init=False,
        default_factory=list,
    )
    tick: int = 0

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
        forces = {name: [0.0, -9.81 * joint.mass] for name, joint in self.joints.items()}
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
            if joint.y < 0.0:
                joint.y = 0.0
                if joint.vy < 0.0:
                    joint.vy = 0.0
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



class PANEmbodiedSandboxSession:
    """Couple a persistent PAN live session to the stick-figure environment."""

    def __init__(self, live_session: _LiveSessionLike) -> None:
        self.live_session = live_session
        self.world = StickFigureSandbox()
        self.last_frame: dict[str, object] | None = None

    def step(self, ticks: int = 1) -> dict[str, object]:
        if ticks < 1 or ticks > 512:
            raise ValueError("sandbox ticks must be between 1 and 512")
        frames: list[dict[str, object]] = []
        pan_result: dict[str, object] = {}
        for _ in range(ticks):
            receptors = self.world.receptors()
            audio = 0.0
            echo_values: list[float] = []
            if self.last_frame is not None:
                raw_audio = self.last_frame.get("audio")
                if isinstance(raw_audio, dict):
                    raw_level = raw_audio.get("level", 0.0)
                    if isinstance(raw_level, (int, float)):
                        audio = float(raw_level)
                raw_echo = self.last_frame.get("echo")
                if isinstance(raw_echo, list):
                    echo_values = [
                        float(value)
                        for value in raw_echo
                        if isinstance(value, (int, float))
                    ]
            combined = list(receptors) + [audio] + echo_values
            self.live_session.inject_vector(combined, duration_ticks=1, gain=25.0)
            pan_result = self.live_session.step(1)
            actions = pan_result.get("actions", [])
            action = int(actions[-1]) if isinstance(actions, list) and actions else None
            self.world.apply_action(action)
            frame = self.world.step()
            frame["pan_action"] = action
            frames.append(frame)
            self.last_frame = frame

        return {
            "classification": "PLAYGROUND_PAN_EMBODIED_SANDBOX",
            "scientific_evidence": False,
            "ticks": ticks,
            "world": self.last_frame,
            "pan": pan_result,
            "frames": frames[-32:],
            "learning_claim": "EXPLORATORY_REFERENCE_ONLY",
        }
