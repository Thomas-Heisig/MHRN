"""Integrity-bound Stage-6 cognition supplement for an existing runtime bundle.

The base RuntimeBundle format remains immutable. This additive manifest binds
neural episodic memory, semantic memory and the multistep world-model reference
to the exact bytes of an existing runtime bundle manifest.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from src.memory import ActionConditionedWorldModel, NeuralEpisodicMemory, SemanticMemory


class Stage6BundleError(ValueError):
    """Raised when a Stage-6 supplement is malformed or integrity-invalid."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _safe_name(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or Path(value).name != value:
        raise Stage6BundleError(f"invalid {label} filename")
    return value


@dataclass(frozen=True, slots=True)
class Stage6StateBundle:
    runtime_manifest: Path
    neural_episodic: NeuralEpisodicMemory
    semantic: SemanticMemory
    world_model: ActionConditionedWorldModel
    manifest_path: Path


def write_stage6_bundle(
    directory: Path,
    *,
    runtime_manifest: Path,
    neural_episodic: NeuralEpisodicMemory,
    semantic: SemanticMemory,
    world_model: ActionConditionedWorldModel,
    name: str = "stage6",
) -> Path:
    """Write new Stage-6 state files bound to an existing runtime manifest."""

    if not name or Path(name).name != name:
        raise Stage6BundleError("bundle name must be one safe path component")
    if not runtime_manifest.is_file():
        raise Stage6BundleError("runtime bundle manifest does not exist")
    directory.mkdir(parents=True, exist_ok=True)
    neural_path = directory / f"{name}.neural-episodic.json"
    semantic_path = directory / f"{name}.semantic.json"
    world_path = directory / f"{name}.world-model.json"
    manifest_path = directory / f"{name}.bundle.json"

    _atomic_json(neural_path, neural_episodic.state_dict())
    _atomic_json(semantic_path, semantic.state_dict())
    _atomic_json(world_path, world_model.state_dict())

    payload: dict[str, Any] = {
        "schema_version": 1,
        "owner": "mhrn.stage6_state_bundle",
        "runtime_manifest": runtime_manifest.name,
        "runtime_manifest_sha256": _sha256(runtime_manifest),
        "run_id": neural_episodic.run_id,
        "neural_episodic_file": neural_path.name,
        "neural_episodic_sha256": _sha256(neural_path),
        "semantic_file": semantic_path.name,
        "semantic_sha256": _sha256(semantic_path),
        "world_model_file": world_path.name,
        "world_model_sha256": _sha256(world_path),
        "scientific_status": "continuation_integrity_not_evidence",
    }
    unsigned = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    payload["integrity_digest"] = hashlib.sha256(unsigned).hexdigest()
    _atomic_json(manifest_path, payload)
    return manifest_path


def read_stage6_bundle(manifest_path: Path) -> Stage6StateBundle:
    """Restore Stage-6 state only when every bound byte sequence still matches."""

    try:
        raw_object: object = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise Stage6BundleError("Stage-6 bundle manifest could not be read") from error
    if not isinstance(raw_object, dict):
        raise Stage6BundleError("Stage-6 bundle manifest must be an object")
    raw = cast(dict[str, Any], raw_object)
    if raw.get("schema_version") != 1 or raw.get("owner") != "mhrn.stage6_state_bundle":
        raise Stage6BundleError("unsupported Stage-6 bundle schema")

    unsigned = dict(raw)
    digest = unsigned.pop("integrity_digest", None)
    expected = hashlib.sha256(
        json.dumps(
            unsigned,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()
    if not isinstance(digest, str) or digest != expected:
        raise Stage6BundleError("Stage-6 bundle manifest integrity check failed")

    runtime_name = _safe_name(raw.get("runtime_manifest"), "runtime manifest")
    neural_name = _safe_name(raw.get("neural_episodic_file"), "neural episodic")
    semantic_name = _safe_name(raw.get("semantic_file"), "semantic")
    world_name = _safe_name(raw.get("world_model_file"), "world model")
    runtime_path = manifest_path.parent / runtime_name
    neural_path = manifest_path.parent / neural_name
    semantic_path = manifest_path.parent / semantic_name
    world_path = manifest_path.parent / world_name

    checks = (
        (runtime_path, raw.get("runtime_manifest_sha256"), "runtime manifest"),
        (neural_path, raw.get("neural_episodic_sha256"), "neural episodic"),
        (semantic_path, raw.get("semantic_sha256"), "semantic"),
        (world_path, raw.get("world_model_sha256"), "world model"),
    )
    for path, expected_hash, label in checks:
        if not path.is_file() or _sha256(path) != expected_hash:
            raise Stage6BundleError(f"{label} hash mismatch")

    try:
        neural_raw = cast(
            dict[str, Any], json.loads(neural_path.read_text(encoding="utf-8"))
        )
        semantic_raw = cast(
            dict[str, Any], json.loads(semantic_path.read_text(encoding="utf-8"))
        )
        world_raw = cast(
            dict[str, Any], json.loads(world_path.read_text(encoding="utf-8"))
        )
        neural = NeuralEpisodicMemory.from_state_dict(neural_raw)
        semantic = SemanticMemory.from_state_dict(semantic_raw)
        world_model = ActionConditionedWorldModel.from_state_dict(world_raw)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise Stage6BundleError("Stage-6 state could not be restored") from error
    if neural.run_id != raw.get("run_id"):
        raise Stage6BundleError("Stage-6 run identity mismatch")
    return Stage6StateBundle(
        runtime_manifest=runtime_path,
        neural_episodic=neural,
        semantic=semantic,
        world_model=world_model,
        manifest_path=manifest_path,
    )


__all__ = [
    "Stage6BundleError",
    "Stage6StateBundle",
    "read_stage6_bundle",
    "write_stage6_bundle",
]
