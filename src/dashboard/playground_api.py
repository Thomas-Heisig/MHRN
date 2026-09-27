"""Dashboard adapter for the isolated non-canonical Playground."""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Mapping

from src.playground import service

_MAX_CONCURRENT_RUNS = 2
_RUNS_PER_MINUTE = 20
_RUN_WINDOW_SECONDS = 60.0

_RUN_SEMAPHORE = threading.BoundedSemaphore(_MAX_CONCURRENT_RUNS)
_RATE_LOCK = threading.Lock()
_RECENT_RUNS: deque[float] = deque()


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


def get_playground(path: str) -> dict[str, object] | None:
    if path == "/api/playground/catalog":
        return service.catalog()
    if path == "/api/playground/sessions":
        return service.sessions()
    if path.startswith("/api/playground/sessions/"):
        session_id = path[len("/api/playground/sessions/") :]
        return service.replay(session_id)
    return None


def post_playground(
    path: str, payload: Mapping[str, object]
) -> dict[str, object] | None:
    if path in {"/api/playground/run", "/api/playground/robustness"}:
        return _bounded_run(path, payload)
    return None
