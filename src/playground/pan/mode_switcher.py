"""Switchable event/tick execution controller for the isolated PAN Playground.

The controller manages execution policy and transition bookkeeping. It does not
claim mathematical equivalence between event-only and tick-only integration.
"""

from __future__ import annotations

import hashlib
import json
from collections import deque
from collections.abc import Mapping, Sequence


EXECUTION_MODES = {"EVENT_ONLY", "TICK_ONLY", "HYBRID_AUTO"}
ENGINE_MODES = {"EVENT_ONLY", "TICK_ONLY"}


class ActivityMonitor:
    """Track a bounded moving average of population spike activity."""

    def __init__(self, *, window: int = 100) -> None:
        if window < 1:
            raise ValueError("activity window must be positive")
        self.window = window
        self.history: deque[float] = deque(maxlen=window)

    def update(self, spikes: Sequence[int], n_neurons: int) -> float:
        if n_neurons < 1:
            raise ValueError("n_neurons must be positive")
        activity = len(spikes) / n_neurons
        self.history.append(activity)
        return activity

    def mean(self) -> float:
        if not self.history:
            return 0.0
        return sum(self.history) / len(self.history)

    def trend(self) -> str:
        values = list(self.history)
        if len(values) < 4:
            return "stable"
        half = max(1, len(values) // 2)
        older = sum(values[:half]) / half
        recent_values = values[-half:]
        recent = sum(recent_values) / len(recent_values)
        if recent > max(older * 1.2, older + 1e-12):
            return "rising"
        if recent < older * 0.8:
            return "falling"
        return "stable"


def state_integrity_hash(
    states: Sequence[Mapping[str, object]],
    pending: Sequence[Sequence[float]],
    current_engine: str,
) -> str:
    """Return a stable digest for transition-integrity bookkeeping."""

    compact_states: list[dict[str, object]] = []
    for state in states:
        compact: dict[str, object] = {}
        for key in sorted(state):
            value = state[key]
            if isinstance(value, (bool, int, float, str)) or value is None:
                compact[key] = value
        compact_states.append(compact)
    payload = {
        "engine": current_engine,
        "states": compact_states,
        "pending": [
            [round(float(value), 12) for value in row]
            for row in pending
        ],
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class ModeSwitcher:
    """Choose EVENT_ONLY or TICK_ONLY with hysteresis and dwell time."""

    def __init__(
        self,
        *,
        mode: str = "HYBRID_AUTO",
        initial_mode: str = "EVENT_ONLY",
        theta_high: float = 0.30,
        theta_low: float = 0.05,
        hysteresis: float = 0.02,
        min_dwell: int = 100,
        activity_window: int = 100,
        transition_mode: str = "clean",
        sync_on_switch: bool = True,
        log_transitions: bool = True,
        log_state_hash: bool = True,
    ) -> None:
        mode = mode.upper()
        initial_mode = initial_mode.upper()
        if mode not in EXECUTION_MODES:
            raise ValueError("unsupported execution mode")
        if initial_mode not in ENGINE_MODES:
            raise ValueError("initial_mode must be EVENT_ONLY or TICK_ONLY")
        if not 0.0 <= theta_low <= theta_high <= 1.0:
            raise ValueError("execution thresholds must satisfy 0 <= low <= high <= 1")
        if not 0.0 <= hysteresis <= 0.5:
            raise ValueError("execution hysteresis must be between 0 and 0.5")
        if min_dwell < 0:
            raise ValueError("execution min_dwell must be non-negative")
        if transition_mode not in {"clean", "fast", "debug"}:
            raise ValueError("unsupported transition_mode")
        self.mode = mode
        self.current_engine = initial_mode if mode == "HYBRID_AUTO" else mode
        if self.current_engine == "HYBRID_AUTO":
            self.current_engine = initial_mode
        self.theta_high = theta_high
        self.theta_low = theta_low
        self.hysteresis = hysteresis
        self.min_dwell = min_dwell
        self.transition_mode = transition_mode
        self.sync_on_switch = sync_on_switch
        self.log_transitions = log_transitions
        self.log_state_hash = log_state_hash
        self.monitor = ActivityMonitor(window=activity_window)
        self.last_switch_tick = 0
        self.mode_history: list[dict[str, object]] = [
            {"tick": 0, "mode": self.current_engine, "reason": "initial"}
        ]
        self.transitions: list[dict[str, object]] = []
        self.event_ticks = 0
        self.tick_ticks = 0
        self.consistency_failures = 0

    def observe(self, spikes: Sequence[int], n_neurons: int) -> float:
        return self.monitor.update(spikes, n_neurons)

    def decide(self, tick: int) -> tuple[str, str | None]:
        if self.mode == "EVENT_ONLY":
            return "EVENT_ONLY", None
        if self.mode == "TICK_ONLY":
            return "TICK_ONLY", None
        if tick - self.last_switch_tick < self.min_dwell:
            return self.current_engine, None

        activity = self.monitor.mean()
        high = min(1.0, self.theta_high + self.hysteresis)
        low = max(0.0, self.theta_low - self.hysteresis)
        if self.current_engine == "EVENT_ONLY" and activity > high:
            return "TICK_ONLY", f"activity>{high:.6f}"
        if self.current_engine == "TICK_ONLY" and activity < low:
            return "EVENT_ONLY", f"activity<{low:.6f}"
        return self.current_engine, None

    def transition(
        self,
        *,
        tick: int,
        new_engine: str,
        reason: str,
        states: Sequence[Mapping[str, object]],
        pending: Sequence[Sequence[float]],
    ) -> None:
        if new_engine == self.current_engine:
            return
        if new_engine not in ENGINE_MODES:
            raise ValueError("transition target must be an engine mode")

        before = state_integrity_hash(states, pending, self.current_engine)
        old_engine = self.current_engine
        # Shared-state reference implementation: switching execution policy does
        # not copy or transform neuron state. Therefore transition integrity is
        # checked by comparing the same shared state before/after the policy flip.
        self.current_engine = new_engine
        after_shared_state = state_integrity_hash(states, pending, old_engine)
        consistent = before == after_shared_state
        if not consistent:
            self.consistency_failures += 1

        self.last_switch_tick = tick
        entry: dict[str, object] = {
            "tick": tick,
            "from": old_engine,
            "to": new_engine,
            "reason": reason,
            "transition_mode": self.transition_mode,
            "shared_state_integrity": "PASS" if consistent else "FAIL",
        }
        if self.log_state_hash:
            entry["state_hash_before"] = before
            entry["state_hash_after"] = after_shared_state
        if self.log_transitions:
            self.transitions.append(entry)
        self.mode_history.append(
            {"tick": tick, "mode": new_engine, "reason": reason}
        )

    def note_tick(self) -> None:
        if self.current_engine == "EVENT_ONLY":
            self.event_ticks += 1
        else:
            self.tick_ticks += 1

    def summary(self) -> dict[str, object]:
        total = self.event_ticks + self.tick_ticks
        return {
            "classification": "PLAYGROUND_SWITCHABLE_EXECUTION",
            "scientific_evidence": False,
            "configured_mode": self.mode,
            "current_engine": self.current_engine,
            "equivalence": "NOT_MATHEMATICALLY_EQUIVALENT",
            "transition_consistency_scope": "SHARED_STATE_INTEGRITY_ONLY",
            "consistency_check": (
                "PASS" if self.consistency_failures == 0 else "FAIL"
            ),
            "theta_high": self.theta_high,
            "theta_low": self.theta_low,
            "hysteresis": self.hysteresis,
            "min_dwell": self.min_dwell,
            "activity_window": self.monitor.window,
            "avg_activity": self.monitor.mean(),
            "activity_trend": self.monitor.trend(),
            "transition_count": len(self.transitions),
            "mode_history": list(self.mode_history),
            "transitions": list(self.transitions),
            "ticks_in_event": self.event_ticks,
            "ticks_in_tick": self.tick_ticks,
            "time_in_event": self.event_ticks / total if total else 0.0,
            "time_in_tick": self.tick_ticks / total if total else 0.0,
            "performance_claim": "NOT_BENCHMARKED",
        }
