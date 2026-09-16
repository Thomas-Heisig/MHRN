"""Regression coverage for firing-rate, plasticity-mode, and hook semantics."""

from __future__ import annotations

import logging
import random

import pytest

from src.core.network import Brain5DConfig, NeuralNetwork
from src.core.neuron import NeuronConfig, create_neuron
from src.core.neuron_models import NeuronModel
from src.core.synapse import Synapse, SynapseConfig


def test_firing_rate_estimate_is_hz_not_cumulative_spike_count() -> None:
    config = NeuronConfig(
        model=NeuronModel.LEAKY_INTEGRATE_AND_FIRE,
        lif_resting_potential=-65.0,
        lif_threshold=-64.0,
        lif_reset=-65.0,
        lif_tau_m_ms=20.0,
        lif_resistance=1.0,
        firing_rate_tau_ms=1000.0,
        enable_threshold_adaptation=False,
        enable_energy_dynamics=False,
        enable_traces=False,
        enable_homeostasis=False,
    )
    neuron = create_neuron(1, config=config)

    for tick in range(5000):
        current = 100.0 if tick % 100 == 0 else 0.0
        neuron.step(current, tick)

    assert neuron.spike_counter == 50
    assert 9.0 <= neuron.firing_rate_estimate <= 11.0


def test_firing_rate_tau_must_be_positive() -> None:
    with pytest.raises(ValueError, match="firing_rate_tau_ms"):
        NeuronConfig(firing_rate_tau_ms=0.0)


def test_triplet_mode_fails_fast_instead_of_silent_pair_stdp() -> None:
    synapse = Synapse(target_id=2, weight=0.5, delay=1)
    synapse.set_config(SynapseConfig(enable_triplet=True))

    with pytest.raises(NotImplementedError, match="Triplet-STDP"):
        synapse.record_pre_spike(1)
    assert synapse.last_pre_spike == -1

    with pytest.raises(NotImplementedError, match="Triplet-STDP"):
        synapse.compute_stdp_update(10.0)


def test_post_step_hook_exception_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    network = NeuralNetwork(Brain5DConfig(dimensions=(2, 2, 2, 2, 2)), random.Random(7))

    def broken_hook(_result: object) -> None:
        raise RuntimeError("hook boom")

    network.add_post_step_hook(broken_hook)
    with caplog.at_level(logging.ERROR, logger="src.core.network"):
        result = network.step()

    assert result.tick == 0
    assert "Post-step hook failed at tick 0" in caplog.text
    assert "hook boom" in caplog.text
