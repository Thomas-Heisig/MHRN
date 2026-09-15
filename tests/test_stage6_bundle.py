from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.embodiment.models import SensorFrame
from src.memory import ActionConditionedWorldModel, NeuralEpisodicMemory, SemanticMemory, StateAction
from src.storage.stage6_bundle import (
    Stage6BundleError,
    read_stage6_bundle,
    write_stage6_bundle,
)


def _states(tmp_path: Path) -> tuple[Path, NeuralEpisodicMemory, SemanticMemory, ActionConditionedWorldModel]:
    runtime_manifest = tmp_path / "runtime.bundle.json"
    runtime_manifest.write_text('{"owner":"mhrn.runtime_bundle","runtime_tick":7}\n', encoding="utf-8")

    neural = NeuralEpisodicMemory(run_id="stage6-bundle-test")
    neural.reset_episode("episode-1")
    episode = neural.record(
        {"spike_ids": (1, 2, 3)},
        SensorFrame("sensor", 1, "symbol", {"phase": "encoding"}),
        None,
    )
    assert episode is not None
    semantic = SemanticMemory(min_episode_support=2)
    semantic.consolidate((episode,))
    world = ActionConditionedWorldModel(max_contexts=4)
    world.update({"position": 0}, StateAction("right", {}), {"position": 1})
    return runtime_manifest, neural, semantic, world


def test_stage6_bundle_roundtrip_binds_all_states(tmp_path: Path) -> None:
    runtime_manifest, neural, semantic, world = _states(tmp_path)
    manifest = write_stage6_bundle(
        tmp_path,
        runtime_manifest=runtime_manifest,
        neural_episodic=neural,
        semantic=semantic,
        world_model=world,
    )

    restored = read_stage6_bundle(manifest)

    assert restored.runtime_manifest == runtime_manifest
    assert restored.neural_episodic.state_dict() == neural.state_dict()
    assert restored.semantic.state_dict() == semantic.state_dict()
    assert restored.world_model.state_dict() == world.state_dict()


def test_stage6_bundle_rejects_modified_world_model_bytes(tmp_path: Path) -> None:
    runtime_manifest, neural, semantic, world = _states(tmp_path)
    manifest = write_stage6_bundle(
        tmp_path,
        runtime_manifest=runtime_manifest,
        neural_episodic=neural,
        semantic=semantic,
        world_model=world,
    )
    world_path = tmp_path / "stage6.world-model.json"
    world_path.write_text(world_path.read_text(encoding="utf-8") + " ", encoding="utf-8")

    with pytest.raises(Stage6BundleError, match="world model hash mismatch"):
        read_stage6_bundle(manifest)


def test_stage6_bundle_rejects_runtime_manifest_substitution(tmp_path: Path) -> None:
    runtime_manifest, neural, semantic, world = _states(tmp_path)
    manifest = write_stage6_bundle(
        tmp_path,
        runtime_manifest=runtime_manifest,
        neural_episodic=neural,
        semantic=semantic,
        world_model=world,
    )
    runtime_manifest.write_text('{"runtime_tick":8}\n', encoding="utf-8")

    with pytest.raises(Stage6BundleError, match="runtime manifest hash mismatch"):
        read_stage6_bundle(manifest)


def test_stage6_bundle_rejects_manifest_tampering(tmp_path: Path) -> None:
    runtime_manifest, neural, semantic, world = _states(tmp_path)
    manifest = write_stage6_bundle(
        tmp_path,
        runtime_manifest=runtime_manifest,
        neural_episodic=neural,
        semantic=semantic,
        world_model=world,
    )
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["run_id"] = "tampered"
    manifest.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(Stage6BundleError, match="manifest integrity"):
        read_stage6_bundle(manifest)
