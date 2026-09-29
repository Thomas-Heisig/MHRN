"""Canonical parity, fingerprint and determinism contracts."""

from __future__ import annotations

import math

import pytest

from src.runtime.determinism import (
    delivery_tick,
    release_uniform,
    ring_size_for_max_delay,
    ring_slot,
    spike_update_order,
)
from src.verification.parity import (
    config_fingerprint,
    default_parity_contract,
    exact_spike_parity,
    execution_fingerprint,
    max_abs_error,
)


def test_execution_fingerprint_is_stable_and_seed_sensitive() -> None:
    config_a = {"ticks": 100, "model": "lif", "nested": {"b": 2, "a": 1}}
    config_b = {"nested": {"a": 1, "b": 2}, "model": "lif", "ticks": 100}
    config_hash_a = config_fingerprint(config_a)
    config_hash_b = config_fingerprint(config_b)
    assert config_hash_a == config_hash_b

    first = execution_fingerprint(
        seed=7,
        config_hash=config_hash_a,
        backend_name="cpu",
        backend_version="1",
        ticks=100,
    )
    second = execution_fingerprint(
        seed=7,
        config_hash=config_hash_b,
        backend_name="cpu",
        backend_version="1",
        ticks=100,
    )
    changed = execution_fingerprint(
        seed=8,
        config_hash=config_hash_b,
        backend_name="cpu",
        backend_version="1",
        ticks=100,
    )
    assert first == second
    assert first != changed


def test_d1_and_d2_fail_closed_on_empty_or_non_finite_evidence() -> None:
    assert exact_spike_parity([], []).passed is False
    with pytest.raises(ValueError, match="NaN/Inf"):
        max_abs_error([1.0, 2.0], [1.0, math.nan])


def test_counter_rng_matches_playground_compatibility_export() -> None:
    from src.playground.cuda.synapses import release_uniform as playground_uniform

    assert playground_uniform is release_uniform
    for edge in range(64):
        assert release_uniform(12345, 2000, edge) == playground_uniform(
            12345,
            2000,
            edge,
        )


def test_delay_and_same_tick_order_contracts_match_existing_ring_semantics() -> None:
    ring_size = ring_size_for_max_delay(64)
    assert ring_size == 65
    assert delivery_tick(0, 64) == 64
    assert ring_slot(64, ring_size) == 64
    assert ring_slot(65, ring_size) == 0
    assert spike_update_order(1, 2) == ("pre", "post")
    assert spike_update_order(2, 1) == ("post", "pre")


def test_default_contract_preserves_cuda_1_numeric_thresholds() -> None:
    classes = default_parity_contract().to_mapping()["classes"]
    assert isinstance(classes, dict)
    d1 = classes["D1"]
    d2 = classes["D2"]
    d3 = classes["D3"]
    assert isinstance(d1, dict)
    assert isinstance(d2, dict)
    assert isinstance(d3, dict)
    assert d1["allowed_spike_mismatches"] == 0
    assert d2["voltage_max_abs_error"] == 1.0e-4
    assert d2["weight_max_abs_error"] == 1.0e-4
    assert d3["spike_count_relative_error"] == 0.005
    assert d3["success_fraction_abs_error"] == 0.02
