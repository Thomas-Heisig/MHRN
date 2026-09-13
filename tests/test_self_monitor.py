from __future__ import annotations

import random
from typing import Any, cast

from src.core.network import NeuralNetwork
from src.research.self_monitor import SelfMonitor
from tests.conftest import base_config


def _network() -> NeuralNetwork:
    cfg = cast(dict[str, Any], base_config())
    net = NeuralNetwork(cfg, random.Random(7))  # type: ignore[arg-type]
    first = net.add_neuron((1, 1, 1, 1, 1))
    second = net.add_neuron((1, 1, 1, 1, 2))
    net.neurons[first].spike_counter = 3
    net.neurons[first].firing_rate_estimate = 2.5
    net.neurons[first].energy = 0.8
    net.neurons[first].threshold_adaptation = 0.2
    net.neurons[first].pre_trace = 0.4
    net.neurons[first].post_trace = 0.6
    net.neurons[first].model_switch_count = 1
    net.neurons[second].firing_rate_estimate = 0.5
    net.neurons[second].energy = 1.0
    return net


def test_self_monitor_observes_without_mutating_network_state() -> None:
    net = _network()
    before = {
        identifier: neuron.to_dict() for identifier, neuron in net.neurons.items()
    }
    monitor = SelfMonitor(max_history=4)

    snapshot = monitor.observe(net, tick=11)

    after = {identifier: neuron.to_dict() for identifier, neuron in net.neurons.items()}
    assert after == before
    assert snapshot.tick == 11
    assert snapshot.neuron_count == 2
    assert snapshot.active_neurons == 1
    assert snapshot.total_spikes == 3
    assert snapshot.mean_firing_rate == 1.5
    assert snapshot.mean_energy == 0.9
    assert snapshot.model_switch_count == 1


def test_self_monitor_history_is_bounded_and_immutable_from_callers() -> None:
    net = _network()
    monitor = SelfMonitor(max_history=2)

    monitor.observe(net, tick=1)
    monitor.observe(net, tick=2)
    monitor.observe(net, tick=3)

    assert [item.tick for item in monitor.history] == [2, 3]
    assert isinstance(monitor.history, tuple)


def test_self_monitor_supports_empty_network() -> None:
    cfg = cast(dict[str, Any], base_config())
    net = NeuralNetwork(cfg, random.Random(1))  # type: ignore[arg-type]
    snapshot = SelfMonitor().observe(net, tick=0)

    assert snapshot.neuron_count == 0
    assert snapshot.active_neurons == 0
    assert snapshot.mean_firing_rate == 0.0
