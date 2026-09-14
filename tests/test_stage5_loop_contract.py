"""Deterministic unit checks; no SNN or biological-evidence claim."""

from __future__ import annotations

import random

import pytest

from src.embodiment.loop_contract import CycleContract, DispatchBudget, valid_tick


@pytest.mark.parametrize("tick", [-1, True, False, 1.5, "1", None])
def test_tick_contract_rejects_non_integer_or_negative_values(tick):
    assert not valid_tick(tick)
    with pytest.raises(ValueError):
        CycleContract().begin(tick)


def test_pending_cycle_cannot_be_overwritten_or_consumed_twice():
    guard = CycleContract()
    guard.begin(0)
    with pytest.raises(RuntimeError, match="pending"):
        guard.begin(1)
    with pytest.raises(RuntimeError, match="matching"):
        guard.consume(1)
    guard.consume(0)
    with pytest.raises(RuntimeError, match="matching"):
        guard.consume(0)
    with pytest.raises(RuntimeError, match="increase"):
        guard.begin(0)
    guard.begin(1)
    guard.consume(1)


def test_aborted_cycle_is_not_replayable_but_explicit_reset_allows_new_episode():
    guard = CycleContract()
    guard.begin(7)
    guard.abort()
    guard.abort()
    assert guard.pending_tick is None
    assert guard.last_attempted_tick == 7
    with pytest.raises(RuntimeError, match="increase"):
        guard.begin(7)
    guard.reset()
    guard.begin(0)
    guard.consume(0)


@pytest.mark.parametrize("limit", [0, -1, True, 1.5])
def test_dispatch_requires_positive_integer_budget(limit):
    with pytest.raises(ValueError):
        DispatchBudget().denial(0, limit)


def test_dispatch_attempts_are_consumed_before_success_is_known():
    budget = DispatchBudget()
    budget.reserve(4, 1)
    assert budget.denial(4, 1) == "rate_limited"
    assert budget.denial(3, 1) == "stale_tick"
    assert budget.denial(True, 1) == "invalid_tick"
    with pytest.raises(RuntimeError, match="rate_limited"):
        budget.reserve(4, 1)
    budget.reserve(5, 1)
    assert budget.attempts == 1
    budget.reset()
    budget.reserve(0, 1)


@pytest.mark.parametrize("seed", range(16))
def test_adversarial_command_stream_never_exceeds_per_tick_budget(seed):
    rng = random.Random(seed)
    budget = DispatchBudget()
    accepted: dict[int, int] = {}
    latest = -1
    for _ in range(1000):
        tick = rng.randrange(128)
        if budget.denial(tick, 3) is None:
            budget.reserve(tick, 3)
            assert tick >= latest
            latest = tick
            accepted[tick] = accepted.get(tick, 0) + 1
    assert all(count <= 3 for count in accepted.values())
    assert set(budget.__slots__) == {"tick", "attempts"}
