"""Exercise the existing observational temporal-memory contract directly."""

from math import inf, nan

import pytest

from src.research.temporal import (
    TemporalComparator,
    TemporalStateFrame,
    TemporalStateMemory,
)


def test_reference_horizon_and_capacity_do_not_rewind_state() -> None:
    memory = TemporalStateMemory(horizons={"fast": 2, "slow": 5}, capacity=3)
    for tick in range(5):
        memory.append(
            TemporalStateFrame.from_mapping(tick, str(tick), {"activity": float(tick)})
        )
    assert len(memory) == 3
    assert memory.reference(5, "fast").tick == 3
    assert memory.reference(5, "slow") is None
    assert memory.reference(0, "fast") is None
    with pytest.raises(KeyError):
        memory.reference(5, "missing")
    assert len(memory) == 3


def test_temporal_comparison_preserves_missing_reference_and_real_zero() -> None:
    frame = TemporalStateFrame.from_mapping(2, "a", {"z": 4.0, "a": 0.0})
    comparator = TemporalComparator()
    unknown = comparator.compare(frame, None, horizon="slow").to_dict()
    assert unknown["discrepancy"] is None
    assert unknown["digest_changed"] is None
    same = comparator.compare(frame, frame, horizon="fast")
    assert same.discrepancy == 0.0
    assert same.digest_changed is False
    after = TemporalStateFrame.from_mapping(3, "b", {"a": 2.0, "z": 6.0})
    changed = comparator.compare(after, frame, horizon="fast")
    assert changed.discrepancy == 2.0
    assert changed.changed_metrics == ("a", "z")
    assert changed.digest_changed is True
    assert frame.metric_map() == {"a": 0.0, "z": 4.0}


@pytest.mark.parametrize("value", [inf, -inf, nan])
def test_nonfinite_temporal_metrics_are_rejected(value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        TemporalStateFrame.from_mapping(0, "invalid", {"activity": value})


@pytest.mark.parametrize("kwargs", [{"capacity": 0}, {"horizons": {"fast": 0}}])
def test_invalid_temporal_memory_limits_are_rejected(kwargs) -> None:
    with pytest.raises(ValueError):
        TemporalStateMemory(**kwargs)
