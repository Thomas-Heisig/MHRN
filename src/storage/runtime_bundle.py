"""Versioned runtime bundle for checkpoint + cognition continuation.

The existing RuntimeCheckpoint V4 format stays unchanged. Stage 6 needs the
memory/world-model state to travel with the exact runtime checkpoint without
silently redefining older checkpoint files. This module therefore creates a
small integrity-bound bundle manifest beside two independently validated state
files.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.memory.layer import MemoryWorldModel, MemoryWorldModelError

from .checkpoint import RuntimeCheckpoint, read_runtime_checkpoint, write_runtime_checkpoint


class RuntimeBundleError(ValueError):
    """Raised when a runtime/cognition bundle is incomplete or inconsistent."""


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
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@dataclass(frozen=True, slots=True)
class RuntimeBundle:
    """Restored, mutually bound runtime and cognition state."""

    checkpoint: RuntimeCheckpoint
    cognition: MemoryWorldModel
    manifest_path: Path


def write_runtime_bundle(
    directory: Path,
    checkpoint: RuntimeCheckpoint,
    cognition: MemoryWorldModel,
    *,
    name: str = "runtime",
) -> Path:
    """Write a new integrity-bound runtime bundle.

    Individual state formats remain owned by their existing modules. The
    manifest binds exact bytes and run identity; it never edits a legacy file in
    place. Callers should write into a new directory for each durable snapshot.
    """

    if not name or Path(name).name != name:
        raise RuntimeBundleError("bundle name must be one safe path component")
    directory.mkdir(parents=True, exist_ok=True)
    runtime_path = directory / f"{name}.checkpoint.json"
    cognition_path = directory / f"{name}.cognition.json"
    manifest_path = directory / f"{name}.bundle.json"

    write_runtime_checkpoint(runtime_path, checkpoint)
    cognition.save(cognition_path)

    payload = {
        "schema_version": 1,
        "owner": "mhrn.runtime_bundle",
        "runtime_file": runtime_path.name,
        "cognition_file": cognition_path.name,
        "runtime_sha256": _sha256(runtime_path),
        "cognition_sha256": _sha256(cognition_path),
        "run_id": cognition.run_id,
        "runtime_tick": checkpoint.current_tick,
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


def read_runtime_bundle(manifest_path: Path) -> RuntimeBundle:
    """Restore only when manifest, both files and cognition identity agree."""

    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeBundleError("runtime bundle manifest could not be read") from error
    if not isinstance(raw, dict):
        raise RuntimeBundleError("runtime bundle manifest must be an object")
    if raw.get("schema_version") != 1 or raw.get("owner") != "mhrn.runtime_bundle":
        raise RuntimeBundleError("unsupported runtime bundle schema")

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
        raise RuntimeBundleError("runtime bundle manifest integrity check failed")

    runtime_file = raw.get("runtime_file")
    cognition_file = raw.get("cognition_file")
    if not isinstance(runtime_file, str) or Path(runtime_file).name != runtime_file:
        raise RuntimeBundleError("invalid runtime checkpoint filename")
    if not isinstance(cognition_file, str) or Path(cognition_file).name != cognition_file:
        raise RuntimeBundleError("invalid cognition filename")

    runtime_path = manifest_path.parent / runtime_file
    cognition_path = manifest_path.parent / cognition_file
    if _sha256(runtime_path) != raw.get("runtime_sha256"):
        raise RuntimeBundleError("runtime checkpoint hash mismatch")
    if _sha256(cognition_path) != raw.get("cognition_sha256"):
        raise RuntimeBundleError("cognition state hash mismatch")

    checkpoint = read_runtime_checkpoint(runtime_path)
    try:
        cognition = MemoryWorldModel.load(cognition_path)
    except MemoryWorldModelError as error:
        raise RuntimeBundleError("cognition state could not be restored") from error

    if cognition.run_id != raw.get("run_id"):
        raise RuntimeBundleError("runtime bundle run identity mismatch")
    if checkpoint.current_tick != raw.get("runtime_tick"):
        raise RuntimeBundleError("runtime bundle tick mismatch")

    return RuntimeBundle(checkpoint, cognition, manifest_path)


__all__ = [
    "RuntimeBundle",
    "RuntimeBundleError",
    "read_runtime_bundle",
    "write_runtime_bundle",
]
