"""Stage-2 contract for a stable deterministic recurrent SNN.

This is a software reference contract. It verifies explicit recurrent topology,
bounded spike/event propagation and long deterministic replay for one small
reference ring. It does not establish biological equivalence, arbitrary-network
stability, cognition, or scaling to the Stage-2 target range.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

from src.core.network import Brain5DConfig, NeuralNetwork, SimulationConfig, StepResult
from src.core.neuron import NeuronConfig
from src.core.synapse import SynapseConfig

ROOT = Path(__file__).resolve().parents[1]
LONG_RUN_TICKS = 20_000
REFERENCE_WEIGHT = 200.0


def _ring() -> tuple[NeuralNetwork, tuple[int, int, int, int]]:
    config = Brain5DConfig(
        dimensions=(4, 4, 4, 4, 4),
        simulation=SimulationConfig(dt_ms=1.0, max_delay=2, debug_invariants=True),
        neuron=NeuronConfig.isolated_reference(),
        # The strong reference transmission is isolated to this software
        # contract. Production synaptic bounds remain unchanged.
        synapse=SynapseConfig(w_min=0.0, w_max=REFERENCE_WEIGHT),
    )
    network = NeuralNetwork(config, random.Random(23))
    a = network.add_neuron((1, 1, 1, 1, 0))
    b = network.add_neuron((1, 1, 1, 1, 1))
    c = network.add_neuron((1, 1, 1, 1, 2))
    d = network.add_neuron((1, 1, 1, 1, 3))
    network.connect(a, b, weight=REFERENCE_WEIGHT, delay=1)
    network.connect(b, c, weight=REFERENCE_WEIGHT, delay=1)
    network.connect(c, d, weight=REFERENCE_WEIGHT, delay=1)
    network.connect(d, a, weight=REFERENCE_WEIGHT, delay=1)
    return network, (a, b, c, d)


def _prime(network: NeuralNetwork, first_id: int) -> None:
    network.neurons[first_id].v = 30.0


def _deterministic_projection(result: StepResult) -> tuple[object, ...]:
    """Return only deterministic StepResult fields, excluding wall-clock timing."""
    return (
        result.tick,
        result.spike_ids,
        result.output_spike_ids,
        result.spikes_this_tick,
        result.total_spikes,
        result.delivered_events,
        result.queued_events,
        result.external_injection_count,
        result.external_total_current,
        result.synaptic_current_targets,
        result.mean_v,
        result.min_v,
        result.max_v,
        result.mean_energy,
        result.total_synapses,
    )


def test_recurrent_reference_topology_is_an_explicit_closed_ring() -> None:
    network, ids = _ring()

    assert network.neuron_count == 4
    assert network.synapse_count == 4
    for index, source_id in enumerate(ids):
        target_id = ids[(index + 1) % len(ids)]
        assert network.in_degree[source_id] == 1
        assert [
            (syn.target_id, syn.weight, syn.delay)
            for syn in network.get_synapses(source_id)
        ] == [(target_id, REFERENCE_WEIGHT, 1)]


def test_recurrent_reference_remains_bounded_for_long_run() -> None:
    network, ids = _ring()
    _prime(network, ids[0])
    spike_counts = dict.fromkeys(ids, 0)
    max_queue = 0

    for tick in range(LONG_RUN_TICKS):
        result = network.step()
        expected_id = ids[tick % len(ids)]

        assert result.spike_ids == (expected_id,)
        assert result.spikes_this_tick == 1
        assert result.delivered_events == (0 if tick == 0 else 1)
        assert result.queued_events == 1
        assert math.isfinite(result.mean_v)
        assert math.isfinite(result.min_v)
        assert math.isfinite(result.max_v)
        assert -200.0 < result.min_v <= result.max_v < 50.0
        max_queue = max(max_queue, result.queued_events)
        spike_counts[expected_id] += 1

    assert network.current_tick == LONG_RUN_TICKS
    assert network.total_spikes == LONG_RUN_TICKS
    assert network.total_events_processed == LONG_RUN_TICKS - 1
    assert network.queued_event_count == 1
    assert max_queue == 1
    assert set(spike_counts.values()) == {LONG_RUN_TICKS // len(ids)}
    assert all(neuron.energy == 1.0 for neuron in network.neurons.values())


def test_recurrent_long_run_replay_is_deterministic() -> None:
    first, first_ids = _ring()
    second, second_ids = _ring()
    _prime(first, first_ids[0])
    _prime(second, second_ids[0])

    for _ in range(LONG_RUN_TICKS):
        first_result = first.step()
        second_result = second.step()
        assert _deterministic_projection(first_result) == _deterministic_projection(
            second_result
        )

    assert first.to_dict() == second.to_dict()


def test_recurrent_reference_artifact_matches_contract() -> None:
    path = ROOT / "research/generated/verification/recurrent_snn_reference.json"
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["status"] == "verified"
    assert payload["stage"] == 2
    assert payload["reference"]["topology"] == "A -> B -> C -> D -> A"
    assert payload["reference"]["ticks"] == LONG_RUN_TICKS
    assert payload["reference"]["weight"] == REFERENCE_WEIGHT
    assert payload["expected"]["total_spikes"] == LONG_RUN_TICKS
    assert payload["expected"]["events_processed"] == LONG_RUN_TICKS - 1
    assert payload["expected"]["max_queue_depth"] == 1
    assert all(payload["proofs"].values())
