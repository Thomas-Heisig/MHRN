"""Focused tests for incremental runtime persistence."""

from __future__ import annotations

import random
from pathlib import Path

from src.core import Brain5DConfig, NeuralNetwork, StepResult
from src.storage.delta_journal import DeltaType
from src.storage.incremental_runtime import IncrementalStorageSession
from src.storage.runtime import StorageRuntimeConfig


def test_dirty_synapse_collection_avoids_full_synapse_traversal(tmp_path: Path) -> None:
    network = NeuralNetwork(Brain5DConfig(dimensions=(3, 3, 3, 3, 3)), random.Random(3))
    source = network.add_neuron((1, 1, 1, 1, 1))
    target = network.add_neuron((1, 1, 1, 1, 2))
    network.connect(source, target, weight=0.2, delay=1)

    collector = IncrementalStorageSession(
        network,
        StorageRuntimeConfig(
            snapshot_path=tmp_path / "base.b5d",
            journal_path=tmp_path / "base.b5d.journal",
            capture_policy="dirty_tracking",
        ),
        neuron_state_interval_ticks=10,
    )
    collector.prime()

    synapse = network.get_synapses(source)[0]
    synapse.weight = 0.3
    synapse.mark_dirty()

    # Tick 1 is outside the 10-tick neuron-state cadence. Only the dirty
    # synapse should be inspected and encoded.
    deltas = collector.collect_deltas(StepResult(tick=1))

    assert [delta.delta_type for delta in deltas] == [DeltaType.SYNAPSE_WEIGHT]
    assert not network._dirty_neuron_ids
    assert not network._dirty_synapse_ids


def test_neuron_state_interval_is_explicit(tmp_path: Path) -> None:
    network = NeuralNetwork(Brain5DConfig(dimensions=(3, 3, 3, 3, 3)), random.Random(4))
    neuron_id = network.add_neuron((1, 1, 1, 1, 1))
    collector = IncrementalStorageSession(
        network,
        StorageRuntimeConfig(
            snapshot_path=tmp_path / "base.b5d",
            journal_path=tmp_path / "base.b5d.journal",
            capture_policy="dirty_tracking",
        ),
        neuron_state_interval_ticks=5,
    )
    collector.prime()

    network.neurons[neuron_id].v += 1.0
    network.neurons[neuron_id].mark_dirty()
    assert collector.collect_deltas(StepResult(tick=1)) == ()

    network.neurons[neuron_id].v += 1.0
    network.neurons[neuron_id].mark_dirty()
    deltas = collector.collect_deltas(StepResult(tick=4))
    assert [delta.delta_type for delta in deltas] == [DeltaType.NEURON_STATE]
