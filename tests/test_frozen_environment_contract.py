"""Executable Frozen-Environment contract tests."""

from __future__ import annotations

import pytest

from src.embodiment.deterministic import DeterministicTargetEnvironment
from src.embodiment.models import ActionCommand
from src.embodiment.msba import SymbolFrame
from src.embodiment.neural_io_contracts import BoundaryFrame
from src.experience.frozen_environment import (
    FreezeMode,
    FrozenBoundaryFrame,
    FrozenBoundaryReplay,
    FrozenEnvironmentManifest,
    FrozenWorldSession,
    RNGContractMode,
    WorldRNGContract,
)


def _frame(
    *, tick: int, sequence: int = 0, arrival_time_ns: int | None = None
) -> BoundaryFrame:
    symbol = SymbolFrame(
        payload=f'{{"tick":{tick}}}'.encode(),
        codec="json",
        sequence=sequence,
        provenance="frozen-environment-test",
    )
    return BoundaryFrame(
        schema_version=1,
        frame_id=f"frame-{tick}-{sequence}",
        stream_id="sensor-test",
        sequence=sequence,
        direction="INBOUND",
        kind="DIGITAL",
        content_type="application/json",
        schema_id="test-v1",
        symbol_frame=symbol,
        correlation_id=f"corr-{tick}",
        priority=0,
        source_id="fixture",
        provenance="test",
        arrival_time_ns=arrival_time_ns,
        admitted_tick=tick,
    )


def _rng() -> WorldRNGContract:
    return WorldRNGContract(
        algorithm="none",
        version="1",
        mode=RNGContractMode.NONE,
        initial_fingerprint="deterministic-target:no-runtime-rng:v1",
    )


def _manifest(mode: FreezeMode) -> FrozenEnvironmentManifest:
    if mode is FreezeMode.FE1_BOUNDARY_REPLAY:
        frame = FrozenBoundaryFrame.from_frame(_frame(tick=0))
        return FrozenEnvironmentManifest(
            mode=mode,
            environment_id="boundary-replay",
            environment_version="1",
            environment_config={"source": "fixture"},
            rng=WorldRNGContract(
                algorithm="none",
                version="1",
                mode=RNGContractMode.NONE,
                initial_fingerprint="none",
            ),
            sensor_schedule=(0,),
            action_schema={"kind": "none"},
            reward_contract={"kind": "none"},
            episode_policy={"reset": "explicit"},
            boundary_frames=(frame,),
        )

    env = DeterministicTargetEnvironment(target=2)
    env.reset(seed=0)
    return FrozenEnvironmentManifest(
        mode=mode,
        environment_id=env.environment_id,
        environment_version="1",
        environment_config={"target": 2},
        rng=_rng(),
        sensor_schedule=(0, 1),
        action_schema={"actuator_id": "target-actuator", "actions": ["right", "left"]},
        reward_contract={"type": "target-hit", "hit_reward": 1.0},
        episode_policy={"reset": "explicit", "pending_rewards_cross_episode": False},
        initial_world_state=env.snapshot_state(),
    )


def test_fe1_boundary_replay_roundtrip_is_exact_and_ordered() -> None:
    manifest = _manifest(FreezeMode.FE1_BOUNDARY_REPLAY)
    replay = FrozenBoundaryReplay(manifest)
    frames = replay.frames_for_tick(0)
    assert len(frames) == 1
    assert frames[0].payload == b'{"tick":0}'
    assert frames[0].payload_sha256 == manifest.boundary_frames[0].payload_sha256
    with pytest.raises(RuntimeError, match="exhausted"):
        replay.frames_for_tick(0)


def test_frozen_boundary_rejects_wall_clock_input() -> None:
    with pytest.raises(ValueError, match="wall-clock"):
        FrozenBoundaryFrame.from_frame(_frame(tick=0, arrival_time_ns=123))


@pytest.mark.parametrize(
    "mode",
    [
        FreezeMode.FE2_FROZEN_WORLD_LIVE_ACTIONS,
        FreezeMode.FE3_FULL_DETERMINISTIC_LIVE_LOOP,
    ],
)
def test_frozen_world_session_replays_initial_state_and_live_actions(
    mode: FreezeMode,
) -> None:
    manifest = _manifest(mode)
    world = DeterministicTargetEnvironment(target=99)
    session = FrozenWorldSession(manifest, world)
    session.begin()

    first = session.step(ActionCommand("target-actuator", 0, "right"))
    second = session.step(ActionCommand("target-actuator", 1, "right"))

    assert first.state["position"] == 1
    assert first.reward == 0.0
    assert second.state["position"] == 2
    assert second.reward == 1.0
    trace = session.trace()
    assert trace.mode is mode
    assert len(trace.records) == 2
    assert trace.manifest_sha256 == manifest.manifest_sha256
    assert trace.trace_sha256


def test_manifest_digest_is_stable_and_sensitive_to_reward_contract() -> None:
    left = _manifest(FreezeMode.FE2_FROZEN_WORLD_LIVE_ACTIONS)
    same = _manifest(FreezeMode.FE2_FROZEN_WORLD_LIVE_ACTIONS)
    changed = FrozenEnvironmentManifest(
        mode=left.mode,
        environment_id=left.environment_id,
        environment_version=left.environment_version,
        environment_config=left.environment_config,
        rng=left.rng,
        sensor_schedule=left.sensor_schedule,
        action_schema=left.action_schema,
        reward_contract={"type": "target-hit", "hit_reward": 0.5},
        episode_policy=left.episode_policy,
        initial_world_state=left.initial_world_state,
    )
    assert left.manifest_sha256 == same.manifest_sha256
    assert left.manifest_sha256 != changed.manifest_sha256


def test_fe2_fe3_require_explicit_world_state() -> None:
    with pytest.raises(ValueError, match="initial world state"):
        FrozenEnvironmentManifest(
            mode=FreezeMode.FE2_FROZEN_WORLD_LIVE_ACTIONS,
            environment_id="world",
            environment_version="1",
            environment_config={},
            rng=_rng(),
            sensor_schedule=(0,),
            action_schema={},
            reward_contract={},
            episode_policy={},
        )
