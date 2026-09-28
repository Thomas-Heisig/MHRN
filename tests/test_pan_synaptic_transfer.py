"""Synaptic transfer must change only explicit compatible network state."""

from copy import deepcopy
from dataclasses import replace

import pytest

from src.playground.builder.session import PlaygroundSession
from src.playground.models import PlaygroundConfig
from src.playground.pan.synaptic_checkpoint import SynapticCheckpoint
from src.playground.pan.transfer import run_synaptic_transfer


def payload(**overrides: object) -> dict[str, object]:
    return {
        "closed_loop_preset": "pan_full_balanced",
        "n_neurons": 32,
        "edge_budget": 64,
        "ticks": 256,
        "behavior_episode_ticks": 8,
        "persist": False,
        **overrides,
    }


def test_frozen_pretraining_is_identical_to_fresh_initialization() -> None:
    result = run_synaptic_transfer(payload(transfer_pretrain_plasticity=False))
    assert result["changed_pretraining_weights"] == 0
    trained, fresh = result["conditions"]
    assert trained["full_spike_digest"] == fresh["full_spike_digest"]
    assert trained["decoding_curve"] == fresh["decoding_curve"]
    assert result["neural_transfer_claim"] is False
    assert result["pretraining_configuration"]["target_cue_channel"] == 0
    assert result["novel_configuration"]["target_cue_channel"] == 4


def test_plastic_pretraining_exports_real_changed_weights() -> None:
    result = run_synaptic_transfer(payload())
    assert result["changed_pretraining_weights"] > 0
    checkpoint = SynapticCheckpoint.from_mapping(result["transferred_state"])
    assert result["conditions"][0]["initial_synaptic_digest"] == checkpoint.digest()
    assert all(
        "policy_feedback_confound" in row
        for row in result["conditions"][0]["decoding_curve"]
    )
    assert "policy" in result["reset_state"]


def test_incompatible_and_nonfinite_checkpoints_fail_closed() -> None:
    config = PlaygroundConfig.from_mapping(payload(growth_enabled=False))
    result = PlaygroundSession(config, capture_research_state=True).run()
    raw = result["research_state"]["synapses"]
    for index, value in [(2, float("nan")), (3, True)]:
        bad = deepcopy(raw)
        bad["edges"][0][index] = value
        with pytest.raises(ValueError):
            SynapticCheckpoint.from_mapping(bad)
    checkpoint = SynapticCheckpoint.from_mapping(raw)
    with pytest.raises(ValueError, match="topology mismatch"):
        PlaygroundSession(
            config, initial_synapses=replace(checkpoint, edges=checkpoint.edges[:-1])
        ).run()
    with pytest.raises(ValueError, match="population mismatch"):
        PlaygroundSession(
            config, initial_synapses=replace(checkpoint, n_neurons=64)
        ).run()


def test_transfer_requires_disjoint_input_banks() -> None:
    with pytest.raises(ValueError, match="disjoint"):
        run_synaptic_transfer(payload(action_space_size=8))
