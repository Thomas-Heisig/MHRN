"""Dashboard adapter for the isolated non-canonical Playground."""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Mapping
from typing import cast

from src.playground import service
from src.playground.models import PlaygroundConfig
from src.playground.pan import PANEmbodiedSandboxSession, PANSessionDaemon
from src.playground.night_run import NightRunManager

_MAX_CONCURRENT_RUNS = 2
_RUNS_PER_MINUTE = 20
_RUN_WINDOW_SECONDS = 60.0

_RUN_SEMAPHORE = threading.BoundedSemaphore(_MAX_CONCURRENT_RUNS)
_RATE_LOCK = threading.Lock()
_RECENT_RUNS: deque[float] = deque()


def _payload_int(
    payload: Mapping[str, object],
    name: str,
    default: int,
) -> int:
    value = payload.get(name, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    converted = int(value)
    if float(value) != float(converted):
        raise ValueError(f"{name} must be an integer")
    return converted


def _payload_float(
    payload: Mapping[str, object],
    name: str,
    default: float,
) -> float:
    value = payload.get(name, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    return float(value)


def _payload_text(
    payload: Mapping[str, object],
    name: str,
    default: str,
) -> str:
    value = payload.get(name, default)
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    return value


def _numeric_list(value: object, name: str) -> list[float]:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")
    items = cast(list[object], value)
    result: list[float] = []
    for item in items:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise ValueError(f"{name} entries must be numeric")
        result.append(float(item))
    return result


_LIVE_DAEMON = PANSessionDaemon()
_LIVE_SANDBOXES: dict[str, PANEmbodiedSandboxSession] = {}
_LIVE_LOCK = threading.RLock()
_NIGHT_RUN = NightRunManager()


class PlaygroundRateLimitError(RuntimeError):
    """Raised when the bounded Playground API rate is exceeded."""


class PlaygroundBusyError(RuntimeError):
    """Raised when all bounded Playground worker slots are occupied."""


def _reserve_rate_slot() -> None:
    now = time.monotonic()
    with _RATE_LOCK:
        cutoff = now - _RUN_WINDOW_SECONDS
        while _RECENT_RUNS and _RECENT_RUNS[0] < cutoff:
            _RECENT_RUNS.popleft()
        if len(_RECENT_RUNS) >= _RUNS_PER_MINUTE:
            raise PlaygroundRateLimitError(
                "Playground run rate exceeded; retry after the current minute window."
            )
        _RECENT_RUNS.append(now)


def _bounded_run(path: str, payload: Mapping[str, object]) -> dict[str, object]:
    _reserve_rate_slot()
    if not _RUN_SEMAPHORE.acquire(blocking=False):
        raise PlaygroundBusyError(
            "Playground is busy; at most two simulation requests run concurrently."
        )
    try:
        if path == "/api/playground/run":
            return service.run(payload)
        if path == "/api/playground/robustness":
            return service.robustness(payload)
        raise ValueError(f"unknown Playground POST route: {path}")
    finally:
        _RUN_SEMAPHORE.release()


def _live_parts(path: str) -> list[str]:
    prefix = "/api/playground/live/"
    if not path.startswith(prefix):
        return []
    return [part for part in path[len(prefix):].split("/") if part]


def get_playground(path: str) -> dict[str, object] | None:
    if path == "/api/playground/catalog":
        return service.catalog()
    if path == "/api/playground/sessions":
        return service.sessions()
    if path.startswith("/api/playground/sessions/"):
        session_id = path[len("/api/playground/sessions/") :]
        return service.replay(session_id)
    if path == "/api/playground/night":
        return _NIGHT_RUN.status()
    if path == "/api/playground/live":
        return {
            "class": "PLAYGROUND_LIVE_SESSIONS",
            "scientific_evidence": False,
            "sessions": _LIVE_DAEMON.list(),
        }
    parts = _live_parts(path)
    if len(parts) == 1:
        return {"session_id": parts[0], **_LIVE_DAEMON.get(parts[0]).snapshot()}
    return None


def post_playground(
    path: str, payload: Mapping[str, object]
) -> dict[str, object] | None:
    if path in {"/api/playground/run", "/api/playground/robustness"}:
        return _bounded_run(path, payload)

    if path == "/api/playground/night/start":
        return _NIGHT_RUN.start(
            hours=_payload_float(payload, "hours", 8.0),
            max_episodes=_payload_int(payload, "max_episodes", 10_000),
            checkpoint_seconds=_payload_float(payload, "checkpoint_seconds", 600.0),
            seed=_payload_int(payload, "seed", 12345),
        )
    if path == "/api/playground/night/stop":
        return _NIGHT_RUN.stop()

    if path == "/api/playground/live/create":
        config_payload = dict(payload)
        config_payload.setdefault("neuron_model", "pan_adex_5d")
        config_payload.setdefault("pan_enabled", True)
        config_payload.setdefault("thalamic_relay_threshold", 0.0)
        config_payload.setdefault("pan_bias_current", 15.0)
        config_payload.setdefault("behavior_target_mode", "cycle")
        config = PlaygroundConfig.from_mapping(config_payload)
        session_id = _LIVE_DAEMON.create(config)
        with _LIVE_LOCK:
            _LIVE_SANDBOXES[session_id] = PANEmbodiedSandboxSession(_LIVE_DAEMON.get(session_id))
        return {
            "class": "PLAYGROUND_LIVE_SESSION",
            "scientific_evidence": False,
            "session_id": session_id,
            "state": _LIVE_DAEMON.get(session_id).snapshot(),
        }

    parts = _live_parts(path)
    if len(parts) >= 2:
        session_id, action = parts[0], parts[1]
        session = _LIVE_DAEMON.get(session_id)
        if action == "step":
            ticks = _payload_int(payload, "ticks", 32)
            return {"session_id": session_id, **session.step(ticks)}
        if action == "input":
            values = _numeric_list(payload.get("values", []), "values")
            duration = _payload_int(payload, "duration_ticks", 16)
            gain = _payload_float(payload, "gain", 25.0)
            session.inject_vector(values, duration_ticks=duration, gain=gain)
            return {"session_id": session_id, "accepted": True}
        if action == "strategy":
            context = _payload_text(payload, "context", "default")
            options = _payload_int(payload, "action_count", 4)
            chosen = session.choose_strategy(context, options)
            return {
                "session_id": session_id,
                "classification": "PLAYGROUND_META_STRATEGY",
                "scientific_evidence": False,
                "context": context,
                "action": chosen,
                "action_count": options,
            }
        if action == "reward":
            context = _payload_text(payload, "context", "default")
            chosen = _payload_int(payload, "action", 0)
            action_count = _payload_int(payload, "action_count", 4)
            reward = _payload_float(payload, "reward", 0.0)
            return {
                "session_id": session_id,
                **session.apply_strategy_reward(
                    context=context,
                    action=chosen,
                    reward=reward,
                    action_count=action_count,
                ),
            }
        if action == "sandbox":
            with _LIVE_LOCK:
                sandbox = _LIVE_SANDBOXES.get(session_id)
                if sandbox is None:
                    sandbox = PANEmbodiedSandboxSession(session)
                    _LIVE_SANDBOXES[session_id] = sandbox
            ticks = _payload_int(payload, "ticks", 1)
            return {"session_id": session_id, **sandbox.step(ticks)}
        if action == "stop":
            with _LIVE_LOCK:
                _LIVE_SANDBOXES.pop(session_id, None)
            return {"session_id": session_id, **_LIVE_DAEMON.stop(session_id)}
    return None
