"""Deterministic interleaved event/continuous scheduler for Playground PAN."""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Sequence


@dataclass(order=True, slots=True)
class ScheduledEvent:
    """One logical event ordered by simulation time."""

    time_ms: float
    sequence: int
    kind: str = field(compare=False)
    neuron_id: int | None = field(default=None, compare=False)
    payload: dict[str, object] = field(default_factory=dict, compare=False)

    def descriptor(self) -> dict[str, object]:
        return {
            "time_ms": self.time_ms,
            "kind": self.kind,
            "neuron_id": self.neuron_id,
            "payload": dict(self.payload),
        }


class DualModeScheduler:
    """Reference dual scheduler with deterministic sync barriers.

    The existing Playground tick loop remains the continuous engine. Events are
    queued between barriers and drained in deterministic time/sequence order.
    """

    def __init__(
        self,
        *,
        dt_ms: float,
        base_hz: float,
        event_batch_ms: float,
    ) -> None:
        if dt_ms <= 0.0 or base_hz <= 0.0 or event_batch_ms <= 0.0:
            raise ValueError("dual scheduler intervals must be positive")
        self.dt_ms = dt_ms
        self.base_hz = base_hz
        self.event_batch_ms = event_batch_ms
        self.batch_ticks = max(1, round(event_batch_ms / dt_ms))
        self._queue: list[ScheduledEvent] = []
        self._sequence = 0
        self.continuous_steps = 0
        self.events_processed = 0
        self.sync_barriers = 0
        self.max_queue_depth = 0

    def begin_continuous_step(self) -> None:
        self.continuous_steps += 1

    def push(
        self,
        *,
        time_ms: float,
        kind: str,
        neuron_id: int | None = None,
        payload: dict[str, object] | None = None,
    ) -> None:
        self._sequence += 1
        heapq.heappush(
            self._queue,
            ScheduledEvent(
                time_ms=time_ms,
                sequence=self._sequence,
                kind=kind,
                neuron_id=neuron_id,
                payload={} if payload is None else dict(payload),
            ),
        )
        self.max_queue_depth = max(self.max_queue_depth, len(self._queue))

    def observe_spikes(self, tick: int, neuron_ids: Sequence[int]) -> None:
        time_ms = (tick + 1) * self.dt_ms
        for neuron_id in neuron_ids:
            self.push(time_ms=time_ms, kind="SPIKE", neuron_id=int(neuron_id))

    def sync_due(self, tick: int) -> bool:
        return (tick + 1) % self.batch_ticks == 0

    def drain_barrier(self, tick: int) -> list[dict[str, object]]:
        """Drain events up to the current barrier time."""

        end_ms = (tick + 1) * self.dt_ms
        drained: list[dict[str, object]] = []
        while self._queue and self._queue[0].time_ms <= end_ms:
            drained.append(heapq.heappop(self._queue).descriptor())
        self.events_processed += len(drained)
        self.sync_barriers += 1
        return drained

    def finalize(self, final_tick: int) -> list[dict[str, object]]:
        if not self._queue:
            return []
        return self.drain_barrier(final_tick)

    def summary(self) -> dict[str, object]:
        return {
            "classification": "PLAYGROUND_DUAL_CLOCK",
            "scientific_evidence": False,
            "mode": "dual",
            "execution_semantics": "DETERMINISTIC_INTERLEAVED_REFERENCE",
            "base_hz": self.base_hz,
            "continuous_dt_ms": self.dt_ms,
            "event_batch_ms": self.event_batch_ms,
            "batch_ticks": self.batch_ticks,
            "continuous_steps": self.continuous_steps,
            "events_processed": self.events_processed,
            "sync_barriers": self.sync_barriers,
            "max_queue_depth": self.max_queue_depth,
            "queued_events": len(self._queue),
        }
