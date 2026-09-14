"""Bounded, deterministic bookkeeping for serialized embodiment loops.

These guards track attempted software operations, not physical exactly-once
execution. They deliberately do not infer whether a failed actuator had an effect.
"""

from __future__ import annotations

from dataclasses import dataclass


def valid_tick(tick: int) -> bool:
    """Reject booleans, negative ticks and non-integer timestamps."""

    return type(tick) is int and tick >= 0


@dataclass(slots=True)
class CycleContract:
    """Allow one pending and at most one consumed cycle per increasing tick."""

    pending_tick: int | None = None
    last_attempted_tick: int | None = None

    def begin(self, tick: int) -> None:
        """Reserve a cycle before sampling or current injection has side effects."""

        if not valid_tick(tick):
            raise ValueError("experience tick must be a non-negative integer")
        if self.pending_tick is not None:
            raise RuntimeError("a prepared experience cycle is already pending")
        if self.last_attempted_tick is not None and tick <= self.last_attempted_tick:
            raise RuntimeError("experience ticks must increase within an episode")
        self.pending_tick = tick

    def consume(self, tick: int) -> None:
        """Consume before decoding, actuation or observers can raise exceptions."""

        if not valid_tick(tick) or self.pending_tick != tick:
            raise RuntimeError("complete() requires a matching prepare() call")
        self.last_attempted_tick = tick
        self.pending_tick = None

    def abort(self) -> None:
        """Discard a failed cycle without making its tick available for replay."""

        if self.pending_tick is not None:
            self.last_attempted_tick = self.pending_tick
        self.pending_tick = None

    def reset(self) -> None:
        """Begin a new explicit episode; this does not reset actuator safety."""

        self.pending_tick = None
        self.last_attempted_tick = None


@dataclass(slots=True)
class DispatchBudget:
    """Constant-space attempt budget for serialized, monotonic command ticks."""

    tick: int | None = None
    attempts: int = 0

    def denial(self, tick: int, limit: int) -> str | None:
        """Inspect admission without changing the budget."""

        if type(limit) is not int or limit <= 0:
            raise ValueError("dispatch limit must be a positive integer")
        if not valid_tick(tick):
            return "invalid_tick"
        if self.tick is not None and tick < self.tick:
            return "stale_tick"
        if tick == self.tick and self.attempts >= limit:
            return "rate_limited"
        return None

    def reserve(self, tick: int, limit: int) -> None:
        """Charge BEFORE external dispatch, including failures and rejections."""

        reason = self.denial(tick, limit)
        if reason is not None:
            raise RuntimeError(reason)
        if self.tick != tick:
            self.tick = tick
            self.attempts = 0
        self.attempts += 1

    def reset(self) -> None:
        """Reset episode-local ordering and attempts explicitly."""

        self.tick = None
        self.attempts = 0
