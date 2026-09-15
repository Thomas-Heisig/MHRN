from __future__ import annotations

import json
import random
from collections.abc import Mapping, Sequence

import pytest

from src.memory import MemoryStore, MemoryWorldModel, TransitionWorldModel
from src.storage.checkpoint import capture_runtime_checkpoint
from src.storage.runtime_bundle import (
    RuntimeBundleError,
    read_runtime_bundle,
    write_runtime_bundle,
)


class _Event:
    source_id = 1
    target_id = 2
    weight = 0.25
    delivery_tick = 8


class _Neuron:
    def __init__(self, neuron_id: int) -> None:
        self.neuron_id = neuron_id
        self.a = 0.02
        self.b = 0.2
        self.c = -65.0
        self.d = 8.0
        self.v = -63.0
        self.u = -13.0
        self.energy = 0.9
        self.spike_cost = 0.001
        self.spike_counter = 2
        self.last_spike_tick = 4
        self.threshold_adaptation = 0.1
        self.last_external_current = 1.0
        self.last_synaptic_current = 0.5
        self.firing_rate_estimate = 2.0
        self.pre_trace = 0.2
        self.post_trace = 0.3
        self._spike_count_window = 1
        self._last_update_tick = 7


class _Synapse:
    target_id = 2
    weight = 0.5
    delay = 1
    eligibility = 0.1
    last_pre_spike = 4


class _Network:
    def __init__(self) -> None:
        self.rng = random.Random(7)
        self.current_tick = 7
        self.total_spikes = 2
        self.total_events_processed = 3
        self.pending_currents: Mapping[int, float] = {1: 0.5}
        self.input_cells = {1}
        self.output_cells = {2}
        self.event_slots: Sequence[Sequence[_Event]] = [[], [_Event()]]
        self.neurons = {1: _Neuron(1), 2: _Neuron(2)}
        self.synapses = {1: [_Synapse()]}


def _cognition() -> MemoryWorldModel:
    return MemoryWorldModel(
        MemoryStore(run_id="bundle-test"),
        TransitionWorldModel(max_contexts=4),
        "bundle-test",
    )


def test_runtime_bundle_roundtrip_binds_checkpoint_and_cognition(tmp_path) -> None:
    checkpoint = capture_runtime_checkpoint(_Network())  # type: ignore[arg-type]
    cognition = _cognition()

    manifest = write_runtime_bundle(tmp_path / "bundle", checkpoint, cognition)
    restored = read_runtime_bundle(manifest)

    assert restored.checkpoint == checkpoint
    assert restored.cognition.state_dict() == cognition.state_dict()
    assert restored.cognition.persistence_path == manifest.parent / "runtime.cognition.json"


def test_runtime_bundle_rejects_modified_cognition_bytes(tmp_path) -> None:
    checkpoint = capture_runtime_checkpoint(_Network())  # type: ignore[arg-type]
    manifest = write_runtime_bundle(tmp_path / "bundle", checkpoint, _cognition())
    cognition_path = manifest.parent / "runtime.cognition.json"
    cognition_path.write_text(cognition_path.read_text(encoding="utf-8") + " ", encoding="utf-8")

    with pytest.raises(RuntimeBundleError, match="cognition state hash mismatch"):
        read_runtime_bundle(manifest)


def test_runtime_bundle_rejects_manifest_tampering(tmp_path) -> None:
    checkpoint = capture_runtime_checkpoint(_Network())  # type: ignore[arg-type]
    manifest = write_runtime_bundle(tmp_path / "bundle", checkpoint, _cognition())
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["runtime_tick"] = 99
    manifest.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(RuntimeBundleError, match="manifest integrity"):
        read_runtime_bundle(manifest)


def test_runtime_bundle_rejects_unsafe_name(tmp_path) -> None:
    checkpoint = capture_runtime_checkpoint(_Network())  # type: ignore[arg-type]
    with pytest.raises(RuntimeBundleError, match="safe path"):
        write_runtime_bundle(tmp_path, checkpoint, _cognition(), name="../runtime")
