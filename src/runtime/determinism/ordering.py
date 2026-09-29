"""Deterministic ordering contracts shared by execution backends."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")


def ordered_by_identity(
    values: Iterable[T],
    *,
    key: Callable[[T], tuple[int, ...]],
) -> tuple[T, ...]:
    """Return a stable canonical ordering defined by logical identities."""

    return tuple(sorted(values, key=key))


def spike_update_order(source_id: int, target_id: int) -> tuple[str, str]:
    """Return the canonical same-tick pre/post update order."""

    if source_id < 0 or target_id < 0:
        raise ValueError("neuron ids must be >= 0")
    return ("pre", "post") if source_id <= target_id else ("post", "pre")
