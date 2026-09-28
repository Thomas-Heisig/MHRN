"""Executable contracts for the complete, exploratory PAN starting profile."""

import math

from src.playground import PlaygroundConfig
from src.playground.closed_loop import closed_loop_catalog
from src.playground.service import run


def test_pan_default_resolves_complete_separated_profile() -> None:
    config = PlaygroundConfig.from_mapping({"closed_loop_preset": "pan_full_balanced"})
    assert (config.n_neurons, config.edge_budget, config.ticks) == (256, 2048, 2000)
    assert config.neuron_model == "pan_adex_5d"
    assert config.synapse_model == "pan_stp_stdp"
    assert config.pan_enabled and config.pan_closed_loop
    assert config.growth_enabled and config.neural_io_enabled
    assert config.thalamic_gating_enabled and config.cortical_layers_enabled
    assert config.behavior_learning_enabled and config.sandbox_enabled
    assert config.action_loop_enabled and config.reward_signal_enabled
    channels = {
        config.target_cue_channel,
        config.reward_channel,
        config.posture_score_channel,
        config.reward_event_channel,
        config.reward_cue_channel,
        config.action_feedback_channel,
    }
    assert len(channels) == 6
    assert all(0 <= channel < config.input_channels for channel in channels)
    assert config.hardware_profile_name == "reference_cpu"
    assert not config.offload_enabled
    assert closed_loop_catalog()["scientific_evidence"] is False


def test_pan_default_runs_repeatably_with_explicit_small_overrides() -> None:
    payload = {
        "closed_loop_preset": "pan_full_balanced",
        "n_neurons": 32,
        "edge_budget": 64,
        "ticks": 64,
        "persist": False,
    }
    first = run(payload)
    second = run(payload)
    assert first["metrics"] == second["metrics"]
    assert first["metrics"]["total_spikes"] > 0
    assert first["metrics"]["weight_max"] <= 20.0
    assert all(math.isfinite(value) for value in first["metrics"].values())
