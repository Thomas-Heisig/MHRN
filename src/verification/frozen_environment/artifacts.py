"""Canonical frozen-environment artifact serialization and verification."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

from src.embodiment.models import JSONValue
from src.experience.frozen_environment import (
    FreezeMode,
    FrozenBoundaryFrame,
    FrozenEnvironmentManifest,
    RNGContractMode,
    WorldRNGContract,
)

FROZEN_ENVIRONMENT_ARTIFACT_TYPE = "MHRN_FROZEN_ENVIRONMENT_MANIFEST"
FROZEN_ENVIRONMENT_ARTIFACT_SCHEMA = 1


def _mapping(value: object, *, field: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be a mapping")
    return cast(Mapping[str, object], value)


def _json_mapping(value: object, *, field: str) -> Mapping[str, JSONValue]:
    mapped = _mapping(value, field=field)
    try:
        json.dumps(
            mapped,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be finite canonical JSON") from exc
    return cast(Mapping[str, JSONValue], mapped)


def _sequence(value: object, *, field: str) -> Sequence[object]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise ValueError(f"{field} must be a sequence")
    return cast(Sequence[object], value)


def _text(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _integer(value: object, *, field: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{field} must be an integer")
    return value


def _optional_text(value: object, *, field: str) -> str | None:
    if value is None:
        return None
    return _text(value, field=field)


def _rng_from_mapping(value: object) -> WorldRNGContract:
    data = _mapping(value, field="manifest.rng")
    mode = RNGContractMode(_text(data.get("mode"), field="manifest.rng.mode"))
    state_value = data.get("state")
    state = (
        None
        if state_value is None
        else _json_mapping(state_value, field="manifest.rng.state")
    )
    axes_raw = _sequence(data.get("counter_axes", []), field="manifest.rng.counter_axes")
    axes = tuple(_text(item, field="manifest.rng.counter_axes[]") for item in axes_raw)
    return WorldRNGContract(
        algorithm=_text(data.get("algorithm"), field="manifest.rng.algorithm"),
        version=_text(data.get("version"), field="manifest.rng.version"),
        mode=mode,
        initial_fingerprint=_text(
            data.get("initial_fingerprint"),
            field="manifest.rng.initial_fingerprint",
        ),
        state=state,
        counter_axes=axes,
    )


def _boundary_frame_from_mapping(value: object) -> FrozenBoundaryFrame:
    data = _mapping(value, field="manifest.boundary_frames[]")
    return FrozenBoundaryFrame(
        schema_version=_integer(
            data.get("schema_version"), field="boundary_frame.schema_version"
        ),
        frame_id=_text(data.get("frame_id"), field="boundary_frame.frame_id"),
        stream_id=_text(data.get("stream_id"), field="boundary_frame.stream_id"),
        sequence=_integer(data.get("sequence"), field="boundary_frame.sequence"),
        direction=_text(data.get("direction"), field="boundary_frame.direction"),
        kind=_text(data.get("kind"), field="boundary_frame.kind"),
        content_type=_text(
            data.get("content_type"), field="boundary_frame.content_type"
        ),
        schema_id=_optional_text(
            data.get("schema_id"), field="boundary_frame.schema_id"
        ),
        payload_b64=_text(data.get("payload_b64"), field="boundary_frame.payload_b64"),
        payload_sha256=_text(
            data.get("payload_sha256"), field="boundary_frame.payload_sha256"
        ),
        symbol_codec=_text(
            data.get("symbol_codec"), field="boundary_frame.symbol_codec"
        ),
        symbol_sequence=_integer(
            data.get("symbol_sequence"), field="boundary_frame.symbol_sequence"
        ),
        symbol_provenance=_text(
            data.get("symbol_provenance"), field="boundary_frame.symbol_provenance"
        ),
        correlation_id=_text(
            data.get("correlation_id"), field="boundary_frame.correlation_id"
        ),
        priority=_integer(data.get("priority"), field="boundary_frame.priority"),
        source_id=_text(data.get("source_id"), field="boundary_frame.source_id"),
        provenance=_text(data.get("provenance"), field="boundary_frame.provenance"),
        admitted_tick=_integer(
            data.get("admitted_tick"), field="boundary_frame.admitted_tick"
        ),
    )


def manifest_from_mapping(value: Mapping[str, object]) -> FrozenEnvironmentManifest:
    """Restore one manifest from its canonical JSON mapping."""

    schedule_raw = _sequence(
        value.get("sensor_schedule", []), field="manifest.sensor_schedule"
    )
    boundary_raw = _sequence(
        value.get("boundary_frames", []), field="manifest.boundary_frames"
    )
    disturbance_raw = _sequence(
        value.get("external_disturbances", []),
        field="manifest.external_disturbances",
    )
    state_raw = value.get("initial_world_state")
    initial_world_state = (
        None
        if state_raw is None
        else _json_mapping(state_raw, field="manifest.initial_world_state")
    )
    return FrozenEnvironmentManifest(
        schema_version=_integer(
            value.get("schema_version"), field="manifest.schema_version"
        ),
        contract_id=_text(value.get("contract_id"), field="manifest.contract_id"),
        mode=FreezeMode(_text(value.get("mode"), field="manifest.mode")),
        environment_id=_text(
            value.get("environment_id"), field="manifest.environment_id"
        ),
        environment_version=_text(
            value.get("environment_version"), field="manifest.environment_version"
        ),
        environment_config=_json_mapping(
            value.get("environment_config"), field="manifest.environment_config"
        ),
        rng=_rng_from_mapping(value.get("rng")),
        sensor_schedule=tuple(
            _integer(item, field="manifest.sensor_schedule[]") for item in schedule_raw
        ),
        action_schema=_json_mapping(
            value.get("action_schema"), field="manifest.action_schema"
        ),
        reward_contract=_json_mapping(
            value.get("reward_contract"), field="manifest.reward_contract"
        ),
        episode_policy=_json_mapping(
            value.get("episode_policy"), field="manifest.episode_policy"
        ),
        initial_world_state=initial_world_state,
        boundary_frames=tuple(
            _boundary_frame_from_mapping(item) for item in boundary_raw
        ),
        external_disturbances=tuple(
            _json_mapping(item, field="manifest.external_disturbances[]")
            for item in disturbance_raw
        ),
    )


def manifest_artifact_mapping(
    manifest: FrozenEnvironmentManifest,
) -> dict[str, object]:
    """Return the self-verifying artifact envelope for one manifest."""

    return {
        "artifact_type": FROZEN_ENVIRONMENT_ARTIFACT_TYPE,
        "schema_version": FROZEN_ENVIRONMENT_ARTIFACT_SCHEMA,
        "scientific_evidence": False,
        "manifest_sha256": manifest.manifest_sha256,
        "manifest": manifest.to_mapping(),
    }


def serialize_manifest_artifact(manifest: FrozenEnvironmentManifest) -> str:
    """Serialize without timestamps or insertion-order dependence."""

    return (
        json.dumps(
            manifest_artifact_mapping(manifest),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    )


def write_manifest_artifact(
    path: str | Path,
    manifest: FrozenEnvironmentManifest,
) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(serialize_manifest_artifact(manifest), encoding="utf-8")
    return target


def load_manifest_artifact(path: str | Path) -> FrozenEnvironmentManifest:
    """Load one artifact and fail closed if its declared hash is stale."""

    source = Path(path)
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read frozen-environment artifact: {source}") from exc
    envelope = _mapping(raw, field="artifact")
    if (
        envelope.get("artifact_type") != FROZEN_ENVIRONMENT_ARTIFACT_TYPE
        or envelope.get("schema_version") != FROZEN_ENVIRONMENT_ARTIFACT_SCHEMA
    ):
        raise ValueError("unsupported frozen-environment artifact envelope")
    manifest_raw = _mapping(envelope.get("manifest"), field="artifact.manifest")
    manifest = manifest_from_mapping(manifest_raw)
    declared = _text(
        envelope.get("manifest_sha256"), field="artifact.manifest_sha256"
    )
    if declared != manifest.manifest_sha256:
        raise ValueError("frozen-environment manifest digest mismatch")
    return manifest


__all__ = [
    "FROZEN_ENVIRONMENT_ARTIFACT_SCHEMA",
    "FROZEN_ENVIRONMENT_ARTIFACT_TYPE",
    "load_manifest_artifact",
    "manifest_artifact_mapping",
    "manifest_from_mapping",
    "serialize_manifest_artifact",
    "write_manifest_artifact",
]
