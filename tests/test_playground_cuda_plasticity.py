"""Analytic synaptic rules and physical GPU plasticity parity."""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path

import pytest

from src.playground.cuda.recurrent import (
    RecurrentInputs,
    cpu_recurrent_reference,
    execute_recurrent,
    recurrent_fixture,
    recurrent_parity,
    validate_recurrent_inputs,
)
from src.playground.cuda.synapses import SynapseConfig, SynapseState, release_uniform


def pair_state(**overrides: object) -> SynapseState:
    inputs = RecurrentInputs(
        2, 20, (0, 0, 1), (0,), (7,), (2.0,), (0.0,) * 40, (-65.0,) * 2, (0.0,) * 2
    )
    config = replace(
        SynapseConfig(stp=False, reward_modulated=False, weight_decay=0), **overrides
    )
    return SynapseState(inputs, config)


def test_causal_pair_potentiates_and_anticausal_pair_depresses() -> None:
    causal = pair_state()
    causal.update(0, [1, 0], 0)
    causal.update(1, [0, 1], 0)
    assert causal.weights[0] == pytest.approx(2.1)
    anticausal = pair_state()
    anticausal.update(0, [0, 1], 0)
    anticausal.update(1, [1, 0], 0)
    assert anticausal.weights[0] == pytest.approx(1.92)


def test_emitted_weight_is_frozen_until_delayed_delivery() -> None:
    state = pair_state()
    state.update(0, [1, 0], 0)
    state.weights[0] = 15.0
    assert state.edge_current(6, 0) == 0.0
    assert state.edge_current(7, 0) == 2.0


def test_stp_resources_deplete_and_recover() -> None:
    state = pair_state(stp=True)
    state.update(0, [1, 0], 0)
    assert state.available[0] == pytest.approx(0.745)
    state.update(1, [0, 0], 0)
    assert state.available[0] == pytest.approx(0.77)


def test_reward_modulation_is_signed_and_expires_outside_credit_window() -> None:
    positive = pair_state(stdp=False, reward_modulated=True, credit_window=1)
    negative = pair_state(stdp=False, reward_modulated=True, credit_window=1)
    for state in (positive, negative):
        state.update(0, [0, 1], 0)
    positive.update(1, [0, 0], 1)
    negative.update(1, [0, 0], -1)
    assert positive.weights[0] > 2.0 > negative.weights[0]
    before = positive.weights[0]
    positive.update(2, [0, 0], 1)
    assert positive.weights[0] == before


def test_release_rng_half_open_and_reproducible() -> None:
    for seed in (0, 12345, 0xFFFFFFFF):
        values = [release_uniform(seed, 2000, edge) for edge in range(1000)]
        assert all(0 <= value < 1 for value in values)
        assert len(set(values)) > 990
        assert values == [release_uniform(seed, 2000, edge) for edge in range(1000)]


@pytest.mark.parametrize(
    "config",
    [
        SynapseConfig(seed=True),
        SynapseConfig(weight_max=float("nan")),
        SynapseConfig(eligibility_tau=0),
        SynapseConfig(credit_window=-1),
    ],
)
def test_plasticity_configuration_fails_closed(config: SynapseConfig) -> None:
    with pytest.raises(ValueError):
        validate_recurrent_inputs(
            replace(recurrent_fixture(ticks=1), synapses=config, rewards=(0.0,))
        )


def test_plasticity_requires_complete_finite_rewards_and_parity_state() -> None:
    inputs = replace(recurrent_fixture(ticks=1), synapses=SynapseConfig())
    with pytest.raises(ValueError):
        validate_recurrent_inputs(inputs)
    with pytest.raises(ValueError):
        validate_recurrent_inputs(replace(inputs, rewards=(float("inf"),)))
    result = cpu_recurrent_reference(replace(inputs, rewards=(0.0,)))
    missing = {key: value for key, value in result.items() if key != "eligibility"}
    assert not recurrent_parity(result, missing)["passed"]


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
@pytest.mark.parametrize("ticks", [10, 100, 1000, 2000])
@pytest.mark.parametrize("reward_sign", [-1.0, 0.0, 1.0])
def test_physical_stp_stdp_trace_and_weight_parity(
    ticks: int, reward_sign: float, tmp_path: Path
) -> None:
    inputs = replace(
        recurrent_fixture(ticks=ticks),
        synapses=SynapseConfig(),
        rewards=tuple(reward_sign if tick % 32 == 0 else 0.0 for tick in range(ticks)),
    )
    reference = cpu_recurrent_reference(inputs)
    result = execute_recurrent(inputs, output_dir=tmp_path)
    assert recurrent_parity(reference, result["outputs"])["passed"]
    assert all(0 <= weight <= 20 for weight in result["outputs"]["weights"])
    if ticks >= 100:
        assert sum(reference["spikes"]) > 0
        assert reference["weights"] != list(inputs.weights)
