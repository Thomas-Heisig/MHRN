"""Regression coverage for the interactive runtime hot path."""

from __future__ import annotations

import random
from pathlib import Path

import yaml

from src.core import Brain5DConfig, NeuralNetwork
from src.core.network import NeuralNetwork as ReferenceNeuralNetwork
from src.core.runtime_network import RuntimeNeuralNetwork
from src.core.synapse import SynapseConfig
from src.homeostasis.engine import HomeostasisEngine as ReferenceHomeostasisEngine
from src.homeostasis.hot_path import HotPathHomeostasisEngine
from src.storage.delta_journal import DeltaJournal, DeltaRecord, DeltaType
from src.storage.fast_delta_journal import FastDeltaJournal

ROOT = Path(__file__).resolve().parents[1]


def _network(cls: type[ReferenceNeuralNetwork]) -> ReferenceNeuralNetwork:
    config = Brain5DConfig(
        dimensions=(4, 4, 4, 4, 4),
        synapse=SynapseConfig(w_min=0.0, w_max=100.0),
    )
    network = cls(config, random.Random(7))
    a = network.add_neuron((1, 1, 1, 1, 1))
    b = network.add_neuron((1, 1, 1, 1, 2))
    network.connect(a, b, weight=100.0, delay=1)
    network.neurons[a].v = 30.0
    return network


def test_public_core_uses_runtime_hot_path() -> None:
    assert NeuralNetwork is RuntimeNeuralNetwork


def test_runtime_network_matches_reference_state() -> None:
    reference = _network(ReferenceNeuralNetwork)
    optimized = _network(RuntimeNeuralNetwork)

    reference_results = tuple(reference.step() for _ in range(4))
    optimized_results = tuple(optimized.step() for _ in range(4))

    assert [result.spike_ids for result in optimized_results] == [
        result.spike_ids for result in reference_results
    ]
    assert [result.delivered_events for result in optimized_results] == [
        result.delivered_events for result in reference_results
    ]
    assert optimized.to_dict() == reference.to_dict()


def test_hot_homeostasis_matches_reference_equations() -> None:
    config = {
        "homeostasis": {
            "enabled": True,
            "target_rate_hz": 5.0,
            "rate_tau_ticks": 200.0,
            "threshold_learning_rate": 0.001,
            "threshold_min": -15.0,
            "threshold_max": 30.0,
            "energy_enabled": True,
            "target_energy": 1.0,
            "energy_recovery_rate": 0.001,
            "energy_min": 0.0,
            "energy_max": 1.0,
        }
    }
    reference_network = _network(ReferenceNeuralNetwork)
    optimized_network = _network(ReferenceNeuralNetwork)
    reference_engine = ReferenceHomeostasisEngine(reference_network, config)
    optimized_engine = HotPathHomeostasisEngine(optimized_network, config)

    reference_result = reference_network.step()
    optimized_result = optimized_network.step()
    reference_engine.update(reference_result)
    optimized_engine.update(optimized_result)

    assert optimized_engine.stats == reference_engine.stats
    for neuron_id in reference_network.neurons:
        left = reference_network.neurons[neuron_id]
        right = optimized_network.neurons[neuron_id]
        assert right.threshold_adaptation == left.threshold_adaptation
        assert right.energy == left.energy


def test_fast_journal_commit_remains_readable_by_reference_reader(tmp_path: Path) -> None:
    path = tmp_path / "runtime.journal"
    journal = FastDeltaJournal(path, fsync_on_commit=False)
    journal.open()
    journal.append(DeltaRecord(DeltaType.SPIKE_EVENT, 1, b"one"))
    journal.append(DeltaRecord(DeltaType.SPIKE_EVENT, 2, b"two"))

    # A live commit must not need a complete journal scan.
    journal.scan = lambda: (_ for _ in ()).throw(AssertionError("unexpected scan"))  # type: ignore[method-assign]
    marker = journal.commit()
    assert marker is not None
    journal.close()

    with DeltaJournal(path, fsync_on_commit=False) as reader:
        scan = reader.validate()
        assert len(scan.committed_entries) == 2
        assert scan.last_commit is not None
        assert scan.last_commit.tick == 2


def test_live_profile_selects_incremental_runtime_persistence() -> None:
    config = yaml.safe_load((ROOT / "configs" / "poc_alpha5_live.yaml").read_text())
    runtime = config["storage"]["runtime"]
    journal = config["storage"]["journal"]
    live = config["dashboard"]["live_telemetry"]

    assert runtime["capture_policy"] == "dirty_tracking"
    assert runtime["async_enabled"] is True
    assert runtime["drop_on_overflow"] is False
    assert runtime["neuron_state_interval_ticks"] == 1
    assert journal["commit_interval_ticks"] >= 100
    assert live["capture_interval_ticks"] >= 50
    assert live["capture_interval_ticks"] <= live["activity_window_ticks"]
