"""Backend-neutral delayed-event ring contract."""

from __future__ import annotations

from dataclasses import dataclass


def ring_size_for_max_delay(max_delay: int) -> int:
    if type(max_delay) is not int:
        raise TypeError("max_delay must be int")
    if max_delay < 1:
        raise ValueError("max_delay must be >= 1")
    return max_delay + 1


def ring_slot(tick: int, ring_size: int) -> int:
    if type(tick) is not int or type(ring_size) is not int:
        raise TypeError("tick and ring_size must be int")
    if tick < 0:
        raise ValueError("tick must be >= 0")
    if ring_size < 2:
        raise ValueError("ring_size must be >= 2")
    return tick % ring_size


def delivery_tick(send_tick: int, delay: int) -> int:
    if type(send_tick) is not int or type(delay) is not int:
        raise TypeError("send_tick and delay must be int")
    if send_tick < 0:
        raise ValueError("send_tick must be >= 0")
    if delay < 1:
        raise ValueError("delay must be >= 1")
    return send_tick + delay


@dataclass(frozen=True, slots=True)
class DelayEvent:
    """One immutable delayed emission."""

    source_id: int
    target_id: int
    amplitude: float
    delivery_tick: int

    def __post_init__(self) -> None:
        if self.source_id < 0 or self.target_id < 0:
            raise ValueError("logical ids must be >= 0")
        if self.delivery_tick < 0:
            raise ValueError("delivery_tick must be >= 0")


@dataclass(frozen=True, slots=True)
class DelayQueueSnapshot:
    """Immutable backend-neutral ring snapshot."""

    ring_size: int
    cursor_tick: int
    slots: tuple[tuple[DelayEvent, ...], ...]

    def __post_init__(self) -> None:
        if self.ring_size < 2:
            raise ValueError("ring_size must be >= 2")
        if self.cursor_tick < 0:
            raise ValueError("cursor_tick must be >= 0")
        if len(self.slots) != self.ring_size:
            raise ValueError("slots length must equal ring_size")
