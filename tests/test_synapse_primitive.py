from __future__ import annotations

import random
from typing import Any, cast

import pytest

from src.core.network import NeuralNetwork, StepResult
from src.core.synapse import Synapse, SynapseConfig, create_synapse
from src.learning.learning_engine import LearningEngine
from tests.conftest import base_config


def test_directional_soft_bounds_block_ltp_at_max_and_ltd_at_min() -> None:
    at_max = Synapse(target_id=2, weight=1.0, delay=1, eligibility=1.0)
    at_min = Synapse(target_id=2, weight=0.0, delay=1, eligibility=1.0)

    assert at_max.compute_stdp_update(10.0) == 0.0
    assert at_min.compute_stdp_update(-10.0) == 0.0
    assert at_max.compute_stdp_update(-10.0) < 0.0
    assert at_min.compute_stdp_update(10.0) > 0.0


def test_custom_weight_range_remains_supported() -> None:
    config = SynapseConfig(w_min=0.0, w_max=2.0)
    synapse = create_synapse(target_id=2, weight=1.5, delay=1, config=config)

    assert synapse.weight == 1.5
    assert synapse.config == config
    assert synapse.compute_stdp_update(10.0) > 0.0


def test_spike_pair_accumulates_signed_reward_eligibility() -> None:
    ltp = Synapse(target_id=2, weight=0.5, delay=1)
    ltp.record_pre_spike(10)
    ltp.record_post_spike(20)
    assert ltp.eligibility > 0.0

    ltd = Synapse(target_id=2, weight=0.5, delay=1)
    ltd.record_post_spike(10)
    ltd.record_pre_spike(20)
    assert ltd.eligibility < 0.0


def test_reward_update_uses_signed_eligibility_and_soft_bounds() -> None:
    synapse = Synapse(target_id=2, weight=0.5, delay=1)
    synapse.record_pre_spike(1)
    synapse.record_post_spike(6)
    before = synapse.weight
    eligibility = synapse.eligibility

    delta = synapse.compute_reward_update(1.0)

    assert eligibility > 0.0
    assert delta > 0.0
    assert synapse.weight > before
    assert synapse.eligibility == 0.0


def test_reward_update_can_preserve_trace_when_configured() -> None:
    synapse = Synapse(target_id=2, weight=0.5, delay=1)
    synapse.set_config(SynapseConfig(reset_eligibility_after_reward=False))
    synapse.record_pre_spike(1)
    synapse.record_post_spike(4)
    trace = synapse.eligibility

    assert synapse.compute_reward_update(1.0) > 0.0
    assert synapse.eligibility == pytest.approx(trace)


def test_trace_decay_is_not_trapped_by_triplet_mode_switch() -> None:
    synapse = Synapse(target_id=2, weight=0.5, delay=1, pre_trace=1.0, post_trace=1.0)
    synapse.decay_traces()
    assert 0.0 < synapse.pre_trace < 1.0
    assert 0.0 < synapse.post_trace < 1.0


def test_roundtrip_preserves_complete_adaptive_state() -> None:
    synapse = Synapse(
        target_id=7,
        weight=0.42,
        delay=3,
        eligibility=-0.25,
        last_pre_spike=12,
        last_post_spike=9,
        pre_trace=0.3,
        post_trace=0.4,
        meta_state=0.6,
        update_count=11,
        created_tick=2,
    )
    synapse.set_config(
        SynapseConfig(
            w_min=0.1,
            w_max=0.9,
            reward_learning_rate=0.02,
            enable_triplet=True,
            enable_metaplasticity=True,
        )
    )
    synapse.disable()

    restored = Synapse.from_dict(synapse.to_dict())

    assert restored.to_dict() == synapse.to_dict()
    assert restored.is_enabled is False


def _learning_config() -> dict[str, Any]:
    cfg = cast(dict[str, Any], base_config())
    cfg["stdp"] = {
        "enabled": False,
        "a_plus": 0.1,
        "a_minus": 0.12,
        "tau_plus": 20.0,
        "tau_minus": 20.0,
        "min_weight": 0.0,
        "max_weight": 1.0,
    }
    cfg["eligibility"] = {"enabled": True, "tau_ticks": 200.0}
    cfg["reward"] = {
        "enabled": True,
        "learning_rate": 0.01,
        "delay_ticks": 0,
        "reset_trace_after_reward": False,
    }
    return cfg


def _result(tick: int, *spike_ids: int) -> StepResult:
    return StepResult(
        tick=tick,
        spike_ids=tuple(spike_ids),
        output_spike_ids=(),
        spikes_this_tick=len(spike_ids),
        total_spikes=len(spike_ids),
        delivered_events=0,
        queued_events=0,
        external_injection_count=0,
        external_total_current=0.0,
        synaptic_current_targets=0,
        mean_v=-65.0,
        min_v=-65.0,
        max_v=-65.0,
        mean_energy=1.0,
        core_step_ms=0.0,
    )


def test_learning_engine_keeps_eligibility_separate_from_primitive_field() -> None:
    cfg = _learning_config()
    net = NeuralNetwork(cfg, random.Random(123))  # type: ignore[arg-type]
    pre = net.add_neuron((1, 1, 1, 1, 1))
    post = net.add_neuron((1, 1, 1, 1, 2))
    net.connect(pre, post, 0.5, 1)
    primitive = net.synapses[pre][0]
    engine = LearningEngine(net, cfg)  # type: ignore[arg-type]

    engine.update(_result(0, pre))
    engine.update(_result(10, post))

    assert engine.get_eligibility(pre, post) > 0.0
    assert primitive.eligibility == 0.0
