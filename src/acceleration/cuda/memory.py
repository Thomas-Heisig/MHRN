"""Canonical CUDA memory ownership contracts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeviceAllocation:
    """One owned CUDA device allocation."""

    ptr: int
    size_bytes: int
