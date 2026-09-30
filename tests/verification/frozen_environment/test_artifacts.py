"""Frozen-Environment artifact serialization tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.embodiment.deterministic import DeterministicTargetEnvironment
from src.experience.frozen_environment import (
    FreezeMode,
    FrozenEnvironmentManifest,
    RNGContractMode,
    WorldRNGContract,
)
from src.verification.frozen_environment import (
    load_manifest_artifact,
    serialize_manifest_artifact,
    write_manifest_artifact,
)


def _manifest() -> FrozenEnvironmentManifest:
    env = DeterministicTargetEnvironment(target=2)
    env.reset(seed=0)
    return FrozenEnvironmentManifest(
        mode=FreezeMode.FE2_FROZEN_WORLD_LIVE_ACTIONS,
        environment_id=env.environment_id,
        environment_version="1",
        environment_config={"target": 2},
        rng=WorldRNGContract(
            algorithm="none",
            version="1",
            mode=RNGContractMode.NONE,
            initial_fingerprint=env.rng_fingerprint(),
        ),
        sensor_schedule=(0, 1),
        action_schema={"actions": ["left", "right"]},
        reward_contract={"type": "target-hit"},
        episode_policy={"reset": "explicit"},
        initial_world_state=env.snapshot_state(),
    )


def test_manifest_artifact_bytes_are_stable(tmp_path: Path) -> None:
    manifest = _manifest()
    assert serialize_manifest_artifact(manifest) == serialize_manifest_artifact(
        _manifest()
    )
    path = write_manifest_artifact(tmp_path / "manifest.json", manifest)
    restored = load_manifest_artifact(path)
    assert restored.manifest_sha256 == manifest.manifest_sha256
    assert serialize_manifest_artifact(restored) == serialize_manifest_artifact(
        manifest
    )


def test_manifest_artifact_digest_tamper_fails_closed(tmp_path: Path) -> None:
    path = write_manifest_artifact(tmp_path / "manifest.json", _manifest())
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["manifest_sha256"] = "0" * 64
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="digest mismatch"):
        load_manifest_artifact(path)
