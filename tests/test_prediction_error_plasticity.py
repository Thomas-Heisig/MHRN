from __future__ import annotations

import math
import random
from typing import Any, cast

import pytest

from src.core.network import NeuralNetwork, StepResult
from src.learning.learning_engine import LearningEngine
from src.learning.prediction_error import (
    PredictionErrorPlasticity,
    PredictionErrorPlasticityConfig,
    PredictionErrorPlasticityError,
    PredictionErrorSignal,
)
from tests.conftest import base_config


def _config(*, reward_enabled: bool = False) -> dict[str, Any]:
    config: dict[str, Any] = cast(dict[str, Any], base_config())
    config["stdp"] = {
        "enabled": False,
        "a_plus": 0.1,
        "a_minus": 0.12,
        "tau_plus": 20.0,
        "tau_minus": 20.0,
        "min_weight": 0.0,
        "max_weight": 1.0,
    }
    config["eligibility"] = {"enabled": True, "tau_ticks": 200.0}
    config["reward"] = {
        "enabled": reward_enabled,
        "learning_rate": 0.5,
        "delay_ticks": 0,
        "clamp_weights": True,
        "reset_trace_after_reward": False,
        "trace_epsilon": 1.0e-12,
    }
    return config


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


def _engine(*, reward_enabled: bool = False) -> tuple[LearningEngine, int, int]:
    config = _config(reward_enabled=reward_enabled)
    network = NeuralNetwork(config, random.Random(17))  # type: ignore[arg-type]
    pre_id = network.add_neuron((1, 1, 1, 1, 1))
    post_id = network.add_neuron((1, 1, 1, 1, 2))
    network.connect(pre_id, post_id, 0.5, 1)
    engine = LearningEngine(network, config)  # type: ignore[arg-type]
    engine.update(_result(0, pre_id))
    engine.update(_result(10, post_id))
    return engine, pre_id, post_id


def test_prediction_error_signal_rejects_invalid_values() -> None:
    with pytest.raises(PredictionErrorPlasticityError):
        PredictionErrorSignal(float("nan"), 1)
    with pytest.raises(PredictionErrorPlasticityError):
        PredictionErrorSignal(1.0, -1)


def test_disabled_prediction_error_path_does_not_change_weight() -> None:
    engine, pre_id, _ = _engine()
    plasticity = PredictionErrorPlasticity(
        engine, PredictionErrorPlasticityConfig(enabled=False, learning_rate=0.2)
    )

    changed = plasticity.apply(PredictionErrorSignal(1.0, 10))

    assert changed == 0
    assert engine.network.synapses[pre_id][0].weight == pytest.approx(0.5)
    assert plasticity.stats.signals_received == 1
    assert plasticity.stats.signals_applied == 0


def test_positive_prediction_error_modulates_positive_eligibility() -> None:
    engine, pre_id, post_id = _engine()
    eligibility = 0.1 * math.exp(-10.0 / 20.0)
    plasticity = PredictionErrorPlasticity(
        engine, PredictionErrorPlasticityConfig(enabled=True, learning_rate=0.2)
    )

    changed = plasticity.apply(PredictionErrorSignal(0.5, 10))

    assert changed == 1
    assert engine.get_eligibility(pre_id, post_id, 10) == pytest.approx(eligibility)
    assert engine.network.synapses[pre_id][0].weight == pytest.approx(
        0.5 + 0.2 * 0.5 * eligibility
    )


def test_prediction_error_does_not_increment_reward_statistics() -> None:
    engine, _, _ = _engine(reward_enabled=True)
    before = engine.stats
    plasticity = PredictionErrorPlasticity(
        engine, PredictionErrorPlasticityConfig(enabled=True, learning_rate=0.1)
    )

    plasticity.apply(PredictionErrorSignal(1.0, 10))
    after = engine.stats

    assert after.rewards_received == before.rewards_received == 0
    assert after.rewards_applied == before.rewards_applied == 0
    assert after.reward_weight_updates == before.reward_weight_updates == 0
    assert plasticity.stats.signals_applied == 1
    assert plasticity.stats.weight_updates == 1


def test_prediction_error_requires_eligibility_but_not_reward() -> None:
    config = _config(reward_enabled=False)
    config["eligibility"]["enabled"] = False
    network = NeuralNetwork(config, random.Random(19))  # type: ignore[arg-type]
    engine = LearningEngine(network, config)  # type: ignore[arg-type]

    with pytest.raises(PredictionErrorPlasticityError, match="requires eligibility"):
        PredictionErrorPlasticity(engine)
