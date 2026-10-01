"""Frozen-Environment FE-1/FE-2/FE-3 acceptance tests."""

from __future__ import annotations

from pathlib import Path

from src.embodiment.deterministic import DeterministicTargetEnvironment
from src.embodiment.models import ActionCommand, EnvironmentObservation
from src.embodiment.msba import SymbolFrame
from src.embodiment.neural_io_contracts import BoundaryFrame
from src.experience.frozen_environment import (
    FreezeMode,
    FrozenBoundaryFrame,
    FrozenEnvironmentManifest,
    FrozenWorldAdapter,
    RNGContractMode,
    WorldRNGContract,
)
from src.verification.frozen_environment import (
    run_fe1_integrity,
    run_fe2_replay_determinism,
    run_fe3_cpu_self_control,
)


def _rng() -> WorldRNGContract:
    return WorldRNGContract(
        algorithm="none",
        version="1",
        mode=RNGContractMode.NONE,
        initial_fingerprint="deterministic-target:no-runtime-rng:v1",
    )


def _factory() -> FrozenWorldAdapter:
    return DeterministicTargetEnvironment(target=2)


def _policy(
    tick: int,
    _previous: EnvironmentObservation | None,
) -> ActionCommand:
    return ActionCommand("target-actuator", tick, "right")


def _world_manifest(mode: FreezeMode) -> FrozenEnvironmentManifest:
    env = DeterministicTargetEnvironment(target=2)
    env.reset(seed=0)
    return FrozenEnvironmentManifest(
        mode=mode,
        environment_id=env.environment_id,
        environment_version="1",
        environment_config={"target": 2},
        rng=_rng(),
        sensor_schedule=(0, 1),
        action_schema={"actions": ["left", "right"]},
        reward_contract={"type": "target-hit"},
        episode_policy={"reset": "explicit"},
        initial_world_state=env.snapshot_state(),
    )


def test_fe1_integrity_replays_exact_frame_hashes() -> None:
    symbol = SymbolFrame(
        payload=b'{"sensor":1}',
        codec="json",
        sequence=0,
        provenance="fe-test",
    )
    frame = BoundaryFrame(
        schema_version=1,
        frame_id="frame-0",
        stream_id="sensor",
        sequence=0,
        direction="INBOUND",
        kind="DIGITAL",
        content_type="application/json",
        schema_id="fe-test-v1",
        symbol_frame=symbol,
        correlation_id="corr-0",
        priority=0,
        source_id="fixture",
        provenance="test",
        arrival_time_ns=None,
        admitted_tick=0,
    )
    manifest = FrozenEnvironmentManifest(
        mode=FreezeMode.FE1_BOUNDARY_REPLAY,
        environment_id="boundary-replay-v1",
        environment_version="1",
        environment_config={},
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
        boundary_frames=(FrozenBoundaryFrame.from_frame(frame),),
    )
    result = run_fe1_integrity(manifest)
    assert result.passed
    assert result.details["frame_count"] == 1


def test_fe2_replay_is_exact_across_ten_repetitions() -> None:
    result = run_fe2_replay_determinism(
        _world_manifest(FreezeMode.FE2_FROZEN_WORLD_LIVE_ACTIONS),
        _factory,
        _policy,
        repeats=10,
    )
    assert result.passed
    assert result.details["repeats"] == 10
    assert result.details["all_trace_digests_exact"] is True


def test_fe3_cpu_self_control_uses_canonical_d3_parity() -> None:
    result = run_fe3_cpu_self_control(
        _world_manifest(FreezeMode.FE3_FULL_DETERMINISTIC_LIVE_LOOP),
        _factory,
        _policy,
    )
    assert result.passed
    assert result.details["scope"] == "D3C_ENVIRONMENT_TRAJECTORY_CPU_SELF_CONTROL"
    parity = result.details["parity"]
    assert isinstance(parity, dict)
    assert parity["parity_class"] == "D3c"
    assert parity["passed"] is True


def test_verification_package_has_no_playground_imports() -> None:
    package = Path("src/verification/frozen_environment")
    for path in package.glob("*.py"):
        assert "src.playground" not in path.read_text(encoding="utf-8")
