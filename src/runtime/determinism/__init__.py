"""Canonical deterministic runtime primitives."""

from .delay_queue_contract import (
    DelayEvent,
    DelayQueueSnapshot,
    delivery_tick,
    ring_size_for_max_delay,
    ring_slot,
)
from .ordering import ordered_by_identity, spike_update_order
from .rng import release_uniform

__all__ = [
    "DelayEvent",
    "DelayQueueSnapshot",
    "delivery_tick",
    "ordered_by_identity",
    "release_uniform",
    "ring_size_for_max_delay",
    "ring_slot",
    "spike_update_order",
]
