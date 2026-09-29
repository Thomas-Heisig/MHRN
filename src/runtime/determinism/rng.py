"""Schedule-independent counter RNG primitives."""

from __future__ import annotations


def release_uniform(seed: int, tick: int, edge: int) -> float:
    """Return deterministic U[0,1) from seed, tick and edge."""

    for name, value in (("seed", seed), ("tick", tick), ("edge", edge)):
        if type(value) is not int:
            raise TypeError(f"{name} must be int")
        if value < 0:
            raise ValueError(f"{name} must be >= 0")
    if seed > 0xFFFFFFFF:
        raise ValueError("seed must fit uint32")

    bits = (
        seed
        ^ ((tick * 0x9E3779B9) & 0xFFFFFFFF)
        ^ ((edge * 0x85EBCA6B) & 0xFFFFFFFF)
    ) & 0xFFFFFFFF
    bits ^= bits >> 16
    bits = (bits * 0x7FEB352D) & 0xFFFFFFFF
    bits ^= bits >> 15
    bits = (bits * 0x846CA68B) & 0xFFFFFFFF
    bits ^= bits >> 16
    return (bits >> 8) / 16777216.0
