"""Bounded stimulus generators for playground sessions."""

from __future__ import annotations

import math
import random
from collections.abc import Callable

Stimulus = Callable[[int], list[float]]
Factory = Callable[[int, float, float, float, int], Stimulus]


def none_stimulus(
    n: int, _current: float, _rate: float, _dt: float, _seed: int
) -> Stimulus:
    def sample(_tick: int) -> list[float]:
        return [0.0 for _ in range(n)]

    return sample


def deterministic(
    n: int, current: float, _rate: float, _dt: float, _seed: int
) -> Stimulus:
    driven = max(1, n // 12)

    def sample(tick: int) -> list[float]:
        on = (tick % 40) < 12
        return [current if on and i < driven else 0.0 for i in range(n)]

    return sample


def poisson(
    n: int, current: float, rate_hz: float, dt_ms: float, seed: int
) -> Stimulus:
    rng = random.Random(seed ^ 0x504F4953)
    probability = min(1.0, max(0.0, rate_hz * dt_ms / 1000.0))

    def sample(_tick: int) -> list[float]:
        return [current if rng.random() < probability else 0.0 for _ in range(n)]

    return sample


def ramp(n: int, current: float, _rate: float, _dt: float, _seed: int) -> Stimulus:
    def sample(tick: int) -> list[float]:
        scale = min(1.0, (tick % 128) / 127.0)
        return [current * scale for _ in range(n)]

    return sample


def oscillatory(
    n: int, current: float, rate_hz: float, dt_ms: float, _seed: int
) -> Stimulus:
    frequency = max(0.1, rate_hz)

    def sample(tick: int) -> list[float]:
        phase = 2.0 * math.pi * frequency * (tick * dt_ms / 1000.0)
        value = current * (0.5 + 0.5 * math.sin(phase))
        return [value for _ in range(n)]

    return sample


def channel_ab(
    n: int, current: float, _rate: float, _dt: float, _seed: int
) -> Stimulus:
    midpoint = max(1, n // 2)

    def sample(tick: int) -> list[float]:
        phase = tick % 80
        values = [0.0 for _ in range(n)]
        if 5 <= phase < 15:
            for i in range(min(midpoint, max(1, n // 8))):
                values[i] = current
        if 25 <= phase < 35:
            start = midpoint
            for i in range(start, min(n, start + max(1, n // 8))):
                values[i] = current
        return values

    return sample


STIMULUS_REGISTRY: dict[str, Factory] = {
    "none": none_stimulus,
    "deterministic": deterministic,
    "poisson": poisson,
    "ramp": ramp,
    "oscillatory": oscillatory,
    "channel_ab": channel_ab,
}


def build_stimulus(
    name: str, n: int, current: float, rate_hz: float, dt_ms: float, seed: int
) -> Stimulus:
    try:
        factory = STIMULUS_REGISTRY[name]
    except KeyError as exc:
        raise ValueError(f"unknown playground stimulus: {name}") from exc
    return factory(n, current, rate_hz, dt_ms, seed)
