"""Executable canonical Frozen-Environment contract for D3 parity.

The contract freezes causal environment inputs/state without freezing backend
outputs. It is engineering verification infrastructure only and creates no
scientific DATA or EVID by itself.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, runtime_checkable

from src.embodiment.models import ActionCommand, EnvironmentObservation, JSONValue
from src.embodiment.msba import SymbolFrame
from src.embodiment.neural_io_contracts import BoundaryFrame

FROZEN_ENVIRONMENT_CONTRACT_ID = "mhrn-frozen-environment-v1"


class FreezeMode(StrEnum):
    """Causal freeze levels used by the canonical D3 ladder."""

    FE1_BOUNDARY_REPLAY = "FE-1"
    FE2_FROZEN_WORLD_LIVE_ACTIONS = "FE-2"
    FE3_FULL_DETERMINISTIC_LIVE_LOOP = "FE-3"


class RNGContractMode(StrEnum):
    """How an environment proves its random-state provenance."""

    NONE = "NONE"
    STATE = "STATE"
    COUNTER = "COUNTER"


def canonical_digest(value: object) -> str:
    """Return a stable SHA-256 digest for finite canonical JSON."""

    try:
        raw = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("value must be finite canonical JSON") from exc
    return hashlib.sha256(raw).hexdigest()


def _json_mapping(value: Mapping[str, JSONValue], *, field: str) -> dict[str, JSONValue]:
    result = dict(value)
    try:
        json.dumps(
            result,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be finite canonical JSON") from exc
    return result


@dataclass(frozen=True, slots=True)
class WorldRNGContract:
    """Versioned random-state contract for one frozen world."""

    algorithm: str
    version: str
    mode: RNGContractMode
    initial_fingerprint: str
    state: Mapping[str, JSONValue] | None = None
    counter_axes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.algorithm.strip() or not self.version.strip():
            raise ValueError("RNG algorithm/version must not be empty")
        if not self.initial_fingerprint.strip():
            raise ValueError("initial RNG fingerprint must not be empty")
        if self.mode is RNGContractMode.STATE:
            if self.state is None:
                raise ValueError("STATE RNG contract requires serialized state")
            _json_mapping(self.state, field="rng.state")
        elif self.mode is RNGContractMode.COUNTER:
            if not self.counter_axes or any(not axis.strip() for axis in self.counter_axes):
                raise ValueError("COUNTER RNG contract requires named counter axes")
            if len(set(self.counter_axes)) != len(self.counter_axes):
                raise ValueError("counter axes must be unique")
        elif self.state is not None or self.counter_axes:
            raise ValueError("NONE RNG contract cannot carry state or counter axes")

    def to_mapping(self) -> dict[str, object]:
        return {
            "algorithm": self.algorithm,
            "version": self.version,
            "mode": self.mode.value,
            "initial_fingerprint": self.initial_fingerprint,
            "state": None if self.state is None else dict(self.state),
            "counter_axes": list(self.counter_axes),
        }

    @property
    def contract_sha256(self) -> str:
        return canonical_digest(self.to_mapping())


@dataclass(frozen=True, slots=True)
class FrozenBoundaryFrame:
    """Exact serializable BoundaryFrame used only by explicit freeze artifacts."""

    schema_version: int
    frame_id: str
    stream_id: str
    sequence: int
    direction: str
    kind: str
    content_type: str
    schema_id: str | None
    payload_b64: str
    payload_sha256: str
    symbol_codec: str
    symbol_sequence: int
    symbol_provenance: str
    correlation_id: str
    priority: int
    source_id: str
    provenance: str
    admitted_tick: int

    @classmethod
    def from_frame(cls, frame: BoundaryFrame) -> "FrozenBoundaryFrame":
        if frame.arrival_time_ns is not None:
            raise ValueError("frozen BoundaryFrame must not depend on wall-clock arrival time")
        payload = frame.payload
        return cls(
            schema_version=frame.schema_version,
            frame_id=frame.frame_id,
            stream_id=frame.stream_id,
            sequence=frame.sequence,
            direction=frame.direction,
            kind=frame.kind,
            content_type=frame.content_type,
            schema_id=frame.schema_id,
            payload_b64=base64.b64encode(payload).decode("ascii"),
            payload_sha256=frame.payload_sha256,
            symbol_codec=frame.symbol_frame.codec,
            symbol_sequence=frame.symbol_frame.sequence,
            symbol_provenance=frame.symbol_frame.provenance,
            correlation_id=frame.correlation_id,
            priority=frame.priority,
            source_id=frame.source_id,
            provenance=frame.provenance,
            admitted_tick=frame.admitted_tick,
        )

    def __post_init__(self) -> None:
        if self.schema_version < 1:
            raise ValueError("BoundaryFrame schema_version must be >= 1")
        if self.sequence < 0 or self.symbol_sequence < 0 or self.admitted_tick < 0:
            raise ValueError("BoundaryFrame sequence/tick fields must be >= 0")
        if not self.frame_id or not self.stream_id or not self.source_id:
            raise ValueError("BoundaryFrame identity fields must not be empty")
        try:
            payload = base64.b64decode(self.payload_b64.encode("ascii"), validate=True)
        except (ValueError, UnicodeError) as exc:
            raise ValueError("payload_b64 must be valid base64") from exc
        if hashlib.sha256(payload).hexdigest() != self.payload_sha256:
            raise ValueError("frozen BoundaryFrame payload digest mismatch")

    def to_frame(self) -> BoundaryFrame:
        payload = base64.b64decode(self.payload_b64.encode("ascii"), validate=True)
        symbol = SymbolFrame(
            payload=payload,
            codec=self.symbol_codec,
            sequence=self.symbol_sequence,
            provenance=self.symbol_provenance,
        )
        if symbol.checksum != self.payload_sha256:
            raise ValueError("frozen BoundaryFrame checksum changed during restore")
        return BoundaryFrame(
            schema_version=self.schema_version,
            frame_id=self.frame_id,
            stream_id=self.stream_id,
            sequence=self.sequence,
            direction=self.direction,
            kind=self.kind,
            content_type=self.content_type,
            schema_id=self.schema_id,
            symbol_frame=symbol,
            correlation_id=self.correlation_id,
            priority=self.priority,
            source_id=self.source_id,
            provenance=self.provenance,
            arrival_time_ns=None,
            admitted_tick=self.admitted_tick,
        )

    def to_mapping(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "frame_id": self.frame_id,
            "stream_id": self.stream_id,
            "sequence": self.sequence,
            "direction": self.direction,
            "kind": self.kind,
            "content_type": self.content_type,
            "schema_id": self.schema_id,
            "payload_b64": self.payload_b64,
            "payload_sha256": self.payload_sha256,
            "symbol_codec": self.symbol_codec,
            "symbol_sequence": self.symbol_sequence,
            "symbol_provenance": self.symbol_provenance,
            "correlation_id": self.correlation_id,
            "priority": self.priority,
            "source_id": self.source_id,
            "provenance": self.provenance,
            "arrival_time_ns": None,
            "admitted_tick": self.admitted_tick,
        }

    @property
    def record_sha256(self) -> str:
        return canonical_digest(self.to_mapping())


@dataclass(frozen=True, slots=True)
class FrozenEnvironmentManifest:
    """Serializable source freeze for FE-1/FE-2/FE-3 execution."""

    mode: FreezeMode
    environment_id: str
    environment_version: str
    environment_config: Mapping[str, JSONValue]
    rng: WorldRNGContract
    sensor_schedule: tuple[int, ...]
    action_schema: Mapping[str, JSONValue]
    reward_contract: Mapping[str, JSONValue]
    episode_policy: Mapping[str, JSONValue]
    initial_world_state: Mapping[str, JSONValue] | None = None
    boundary_frames: tuple[FrozenBoundaryFrame, ...] = ()
    external_disturbances: tuple[Mapping[str, JSONValue], ...] = ()
    schema_version: int = 1
    contract_id: str = FROZEN_ENVIRONMENT_CONTRACT_ID

    def __post_init__(self) -> None:
        if self.schema_version != 1 or self.contract_id != FROZEN_ENVIRONMENT_CONTRACT_ID:
            raise ValueError("unsupported frozen-environment contract version")
        if not self.environment_id.strip() or not self.environment_version.strip():
            raise ValueError("environment identity/version must not be empty")
        if any(type(tick) is not int or tick < 0 for tick in self.sensor_schedule):
            raise ValueError("sensor schedule ticks must be non-negative integers")
        if tuple(sorted(set(self.sensor_schedule))) != self.sensor_schedule:
            raise ValueError("sensor schedule must be strictly increasing and unique")
        _json_mapping(self.environment_config, field="environment_config")
        _json_mapping(self.action_schema, field="action_schema")
        _json_mapping(self.reward_contract, field="reward_contract")
        _json_mapping(self.episode_policy, field="episode_policy")
        if self.initial_world_state is not None:
            _json_mapping(self.initial_world_state, field="initial_world_state")
        for index, disturbance in enumerate(self.external_disturbances):
            _json_mapping(disturbance, field=f"external_disturbances[{index}]")

        frame_ids = [frame.frame_id for frame in self.boundary_frames]
        stream_sequences = [(frame.stream_id, frame.sequence) for frame in self.boundary_frames]
        if len(set(frame_ids)) != len(frame_ids):
            raise ValueError("frozen BoundaryFrame ids must be unique")
        if len(set(stream_sequences)) != len(stream_sequences):
            raise ValueError("frozen BoundaryFrame stream/sequence pairs must be unique")
        schedule = set(self.sensor_schedule)
        if any(frame.admitted_tick not in schedule for frame in self.boundary_frames):
            raise ValueError("all frozen BoundaryFrames must belong to the sensor schedule")

        if self.mode is FreezeMode.FE1_BOUNDARY_REPLAY:
            if not self.boundary_frames:
                raise ValueError("FE-1 requires at least one exact BoundaryFrame")
        elif self.initial_world_state is None:
            raise ValueError("FE-2/FE-3 require an explicit initial world state")

    def to_mapping(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "contract_id": self.contract_id,
            "mode": self.mode.value,
            "environment_id": self.environment_id,
            "environment_version": self.environment_version,
            "environment_config": dict(self.environment_config),
            "rng": self.rng.to_mapping(),
            "sensor_schedule": list(self.sensor_schedule),
            "action_schema": dict(self.action_schema),
            "reward_contract": dict(self.reward_contract),
            "episode_policy": dict(self.episode_policy),
            "initial_world_state": (
                None if self.initial_world_state is None else dict(self.initial_world_state)
            ),
            "boundary_frames": [frame.to_mapping() for frame in self.boundary_frames],
            "external_disturbances": [
                dict(disturbance) for disturbance in self.external_disturbances
            ],
            "scientific_evidence": False,
        }

    @property
    def manifest_sha256(self) -> str:
        return canonical_digest(self.to_mapping())


@dataclass(frozen=True, slots=True)
class FrozenTrajectoryRecord:
    """One canonical causal record for D3a/D3b/D3c comparison."""

    tick: int
    pre_state_hash: str
    boundary_frame_hashes: tuple[str, ...]
    action_hash: str
    reward_hash: str
    post_state_hash: str
    rng_fingerprint: str
    terminated: bool
    truncated: bool

    def __post_init__(self) -> None:
        if type(self.tick) is not int or self.tick < 0:
            raise ValueError("trajectory tick must be a non-negative integer")
        required = (
            self.pre_state_hash,
            self.action_hash,
            self.reward_hash,
            self.post_state_hash,
            self.rng_fingerprint,
        )
        if any(not value for value in required):
            raise ValueError("trajectory hashes/fingerprint must not be empty")

    def to_mapping(self) -> dict[str, object]:
        return {
            "tick": self.tick,
            "pre_state_hash": self.pre_state_hash,
            "boundary_frame_hashes": list(self.boundary_frame_hashes),
            "action_hash": self.action_hash,
            "reward_hash": self.reward_hash,
            "post_state_hash": self.post_state_hash,
            "rng_fingerprint": self.rng_fingerprint,
            "terminated": self.terminated,
            "truncated": self.truncated,
        }

    @property
    def record_sha256(self) -> str:
        return canonical_digest(self.to_mapping())


@dataclass(frozen=True, slots=True)
class FrozenEnvironmentTrace:
    """Ordered trajectory bound to exactly one frozen manifest."""

    mode: FreezeMode
    manifest_sha256: str
    records: tuple[FrozenTrajectoryRecord, ...]

    def __post_init__(self) -> None:
        if not self.manifest_sha256:
            raise ValueError("trace manifest hash must not be empty")
        ticks = tuple(record.tick for record in self.records)
        if ticks and ticks != tuple(sorted(set(ticks))):
            raise ValueError("trajectory ticks must be strictly increasing and unique")

    def to_mapping(self) -> dict[str, object]:
        return {
            "mode": self.mode.value,
            "manifest_sha256": self.manifest_sha256,
            "records": [record.to_mapping() for record in self.records],
            "scientific_evidence": False,
        }

    @property
    def trace_sha256(self) -> str:
        return canonical_digest(self.to_mapping())


@runtime_checkable
class FrozenWorldAdapter(Protocol):
    """Environment surface required by FE-2 and FE-3."""

    @property
    def environment_id(self) -> str: ...

    def snapshot_state(self) -> Mapping[str, JSONValue]: ...

    def restore_state(self, state: Mapping[str, JSONValue]) -> None: ...

    def rng_fingerprint(self) -> str: ...

    def step(self, action: ActionCommand) -> EnvironmentObservation: ...


class FrozenBoundaryReplay:
    """Fail-closed FE-1 BoundaryFrame replay in registered tick order."""

    def __init__(self, manifest: FrozenEnvironmentManifest) -> None:
        if manifest.mode is not FreezeMode.FE1_BOUNDARY_REPLAY:
            raise ValueError("FrozenBoundaryReplay requires FE-1 manifest")
        self.manifest = manifest
        self._cursor = 0
        grouped: dict[int, list[FrozenBoundaryFrame]] = {}
        for frame in manifest.boundary_frames:
            grouped.setdefault(frame.admitted_tick, []).append(frame)
        self._grouped = {
            tick: tuple(sorted(frames, key=lambda item: (item.stream_id, item.sequence)))
            for tick, frames in grouped.items()
        }

    def reset(self) -> None:
        self._cursor = 0

    def frames_for_tick(self, tick: int) -> tuple[BoundaryFrame, ...]:
        if self._cursor >= len(self.manifest.sensor_schedule):
            raise RuntimeError("FE-1 replay is exhausted")
        expected = self.manifest.sensor_schedule[self._cursor]
        if tick != expected:
            raise RuntimeError(
                f"FE-1 replay tick mismatch: expected {expected}, received {tick}"
            )
        frozen = self._grouped.get(tick, ())
        if not frozen:
            raise RuntimeError(f"FE-1 manifest has no BoundaryFrame for tick {tick}")
        self._cursor += 1
        return tuple(frame.to_frame() for frame in frozen)


def action_digest(action: ActionCommand | None) -> str:
    payload: object
    if action is None:
        payload = {"action": None}
    else:
        payload = {
            "actuator_id": action.actuator_id,
            "tick": action.tick,
            "action": action.action,
            "payload": action.payload,
        }
    return canonical_digest(payload)


def reward_digest(observation: EnvironmentObservation | None) -> str:
    if observation is None:
        return canonical_digest({"observation": None})
    if not math.isfinite(observation.reward):
        raise ValueError("environment reward must be finite")
    return canonical_digest(
        {
            "tick": observation.tick,
            "reward": observation.reward,
            "terminated": observation.terminated,
            "truncated": observation.truncated,
        }
    )


def build_trajectory_record(
    *,
    tick: int,
    pre_state: Mapping[str, JSONValue],
    boundary_frames: Sequence[BoundaryFrame],
    action: ActionCommand | None,
    observation: EnvironmentObservation | None,
    post_state: Mapping[str, JSONValue],
    rng_fingerprint: str,
) -> FrozenTrajectoryRecord:
    if any(frame.admitted_tick != tick for frame in boundary_frames):
        raise ValueError("BoundaryFrame tick must match trajectory tick")
    frozen_frames = tuple(FrozenBoundaryFrame.from_frame(frame) for frame in boundary_frames)
    return FrozenTrajectoryRecord(
        tick=tick,
        pre_state_hash=canonical_digest(dict(pre_state)),
        boundary_frame_hashes=tuple(frame.record_sha256 for frame in frozen_frames),
        action_hash=action_digest(action),
        reward_hash=reward_digest(observation),
        post_state_hash=canonical_digest(dict(post_state)),
        rng_fingerprint=rng_fingerprint,
        terminated=False if observation is None else observation.terminated,
        truncated=False if observation is None else observation.truncated,
    )


class FrozenWorldSession:
    """Executable FE-2/FE-3 world session with live actions."""

    def __init__(
        self,
        manifest: FrozenEnvironmentManifest,
        world: FrozenWorldAdapter,
    ) -> None:
        if manifest.mode is FreezeMode.FE1_BOUNDARY_REPLAY:
            raise ValueError("FrozenWorldSession requires FE-2 or FE-3 manifest")
        self.manifest = manifest
        self.world = world
        self._started = False
        self._records: list[FrozenTrajectoryRecord] = []

    def begin(self) -> None:
        if self.world.environment_id != self.manifest.environment_id:
            raise ValueError("environment identity does not match frozen manifest")
        state = self.manifest.initial_world_state
        if state is None:
            raise ValueError("frozen world manifest has no initial state")
        self.world.restore_state(state)
        restored = dict(self.world.snapshot_state())
        if canonical_digest(restored) != canonical_digest(dict(state)):
            raise RuntimeError("world restore does not reproduce frozen initial state")
        if self.world.rng_fingerprint() != self.manifest.rng.initial_fingerprint:
            raise RuntimeError("world RNG fingerprint does not match frozen manifest")
        self._records.clear()
        self._started = True

    def step(
        self,
        action: ActionCommand,
        *,
        boundary_frames: Sequence[BoundaryFrame] = (),
    ) -> EnvironmentObservation:
        if not self._started:
            raise RuntimeError("frozen world session must begin before step")
        if type(action.tick) is not int or action.tick < 0:
            raise ValueError("action tick must be a non-negative integer")
        if self._records and action.tick <= self._records[-1].tick:
            raise ValueError("frozen world action ticks must increase")
        if self.manifest.sensor_schedule and action.tick not in set(
            self.manifest.sensor_schedule
        ):
            raise ValueError("action tick is outside the frozen sensor schedule")

        pre_state = dict(self.world.snapshot_state())
        observation = self.world.step(action)
        post_state = dict(self.world.snapshot_state())
        record = build_trajectory_record(
            tick=action.tick,
            pre_state=pre_state,
            boundary_frames=boundary_frames,
            action=action,
            observation=observation,
            post_state=post_state,
            rng_fingerprint=self.world.rng_fingerprint(),
        )
        self._records.append(record)
        return observation

    def trace(self) -> FrozenEnvironmentTrace:
        if not self._started:
            raise RuntimeError("frozen world session has not begun")
        return FrozenEnvironmentTrace(
            mode=self.manifest.mode,
            manifest_sha256=self.manifest.manifest_sha256,
            records=tuple(self._records),
        )


__all__ = [
    "FROZEN_ENVIRONMENT_CONTRACT_ID",
    "FreezeMode",
    "FrozenBoundaryFrame",
    "FrozenBoundaryReplay",
    "FrozenEnvironmentManifest",
    "FrozenEnvironmentTrace",
    "FrozenTrajectoryRecord",
    "FrozenWorldAdapter",
    "FrozenWorldSession",
    "RNGContractMode",
    "WorldRNGContract",
    "action_digest",
    "build_trajectory_record",
    "canonical_digest",
    "reward_digest",
]
