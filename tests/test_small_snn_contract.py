"""Stage-1 contract for a deterministic small coupled SNN.

This verifies software mechanics only: sparse coupling, delayed event delivery,
causal spike propagation and deterministic replay. It is not biological
validation and it does not establish scaling beyond the tested small network.
"""

from __future__ import annotations

import random
from dataclasses import replace

from src.core.network import Brain5DConfig, NeuralNetwork, SimulationConfig, StepResult
from src.core.neuron import NeuronConfig
from src.core.synapse import SynapseConfig


def _chain() -> tuple[NeuralNetwork, tuple[int, int, int]]:
    config = Brain5DConfig(
        dimensions=(4, 4, 4, 4, 4),
        simulation=SimulationConfig(dt_ms=1.0, max_delay=4),
        neuron=NeuronConfig.isolated_reference(),
        # The strong reference transmission is explicit and isolated to this
        # software contract; production defaults remain unchanged.
        synapse=SynapseConfig(w_min=0.0, w_max=100.0),
    )
    network = NeuralNetwork(config, random.Random(17))
    a = network.add_neuron((1, 1, 1, 1, 1))
    b = network.add_neuron((1, 1, 1, 1, 2))
    c = network.add_neuron((1, 1, 1, 1, 3))
    network.connect(a, b, weight=100.0, delay=1)
    network.connect(b, c, weight=100.0, delay=2)
    return network, (a, b, c)


def _normalized(results: tuple[StepResult, ...]) -> tuple[StepResult, ...]:
    return tuple(replace(result, core_step_ms=0.0) for result in results)


def test_three_neuron_chain_propagates_spikes_at_declared_delays() -> None:
    network, (a, b, c) = _chain()
    network.neurons[a].v = 30.0

    results = tuple(network.step() for _ in range(4))

    assert results[0].spike_ids == (a,)
    assert results[0].queued_events == 1
    assert results[1].delivered_events == 1
    assert results[1].spike_ids == (b,)
    assert results[1].queued_events == 1
    assert results[2].delivered_events == 0
    assert results[2].spike_ids == ()
    assert results[3].delivered_events == 1
    assert results[3].spike_ids == (c,)
    assert results[3].queued_events == 0
    assert network.total_spikes == 3
    assert network.total_events_processed == 2


def test_small_snn_replay_is_deterministic() -> None:
    first, (first_a, _, _) = _chain()
    second, (second_a, _, _) = _chain()
    first.neurons[first_a].v = 30.0
    second.neurons[second_a].v = 30.0

    first_results = tuple(first.step() for _ in range(4))
    second_results = tuple(second.step() for _ in range(4))

    assert _normalized(first_results) == _normalized(second_results)
    assert first.to_dict() == second.to_dict()


def test_small_snn_batch_execution_matches_tick_execution() -> None:
    single, (single_a, _, _) = _chain()
    batch, (batch_a, _, _) = _chain()
    single.neurons[single_a].v = 30.0
    batch.neurons[batch_a].v = 30.0

    expected = tuple(single.step() for _ in range(4))
    actual = batch.step_batch(4)

    assert _normalized(expected) == _normalized(actual)
    assert single.to_dict() == batch.to_dict()


def test_small_snn_topology_is_sparse_and_explicit() -> None:
    network, (a, b, c) = _chain()

    assert network.neuron_count == 3
    assert network.synapse_count == 2
    assert network.in_degree[a] == 0
    assert network.in_degree[b] == 1
    assert network.in_degree[c] == 1
    assert [(s.target_id, s.weight, s.delay) for s in network.get_synapses(a)] == [
        (b, 100.0, 1)
    ]
    assert [(s.target_id, s.weight, s.delay) for s in network.get_synapses(b)] == [
        (c, 100.0, 2)
    ]
