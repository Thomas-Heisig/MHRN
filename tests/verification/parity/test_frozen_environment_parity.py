"""D3a/D3b/D3c Frozen-Environment parity tests."""

from __future__ import annotations

from src.embodiment.deterministic import DeterministicTargetEnvironment
from src.embodiment.models import ActionCommand
from src.experience.frozen_environment import (
    FreezeMode,
    FrozenEnvironmentManifest,
    FrozenWorldSession,
    RNGContractMode,
    WorldRNGContract,
)
from src.verification.parity import exact_frozen_environment_parity
from src.verification.parity.contract import ParityClass


def _run(mode: FreezeMode, actions: tuple[str, ...]):
    template = DeterministicTargetEnvironment(target=2)
    template.reset(seed=0)
    manifest = FrozenEnvironmentManifest(
        mode=mode,
        environment_id=template.environment_id,
        environment_version="1",
        environment_config={"target": 2},
        rng=WorldRNGContract(
            algorithm="none",
            version="1",
            mode=RNGContractMode.NONE,
            initial_fingerprint="deterministic-target:no-runtime-rng:v1",
        ),
        sensor_schedule=tuple(range(len(actions))),
        action_schema={"actions": ["left", "right"]},
        reward_contract={"type": "target-hit"},
        episode_policy={"reset": "explicit"},
        initial_world_state=template.snapshot_state(),
    )
    session = FrozenWorldSession(
        manifest,
        DeterministicTargetEnvironment(target=2),
    )
    session.begin()
    for tick, action in enumerate(actions):
        session.step(ActionCommand("target-actuator", tick, action))
    return session.trace()


def test_fe2_trace_maps_to_d3b_and_is_exact() -> None:
    reference = _run(
        FreezeMode.FE2_FROZEN_WORLD_LIVE_ACTIONS,
        ("right", "right"),
    )
    candidate = _run(
        FreezeMode.FE2_FROZEN_WORLD_LIVE_ACTIONS,
        ("right", "right"),
    )
    result = exact_frozen_environment_parity(reference, candidate)
    assert result.parity_class is ParityClass.D3B
    assert result.passed


def test_fe3_trace_maps_to_d3c_and_detects_action_divergence() -> None:
    reference = _run(
        FreezeMode.FE3_FULL_DETERMINISTIC_LIVE_LOOP,
        ("right", "right"),
    )
    candidate = _run(
        FreezeMode.FE3_FULL_DETERMINISTIC_LIVE_LOOP,
        ("left", "right"),
    )
    result = exact_frozen_environment_parity(reference, candidate)
    assert result.parity_class is ParityClass.D3C
    assert not result.passed
    assert result.details["records_exact"] is False


def test_manifest_mismatch_fails_closed() -> None:
    reference = _run(
        FreezeMode.FE2_FROZEN_WORLD_LIVE_ACTIONS,
        ("right", "right"),
    )
    candidate = _run(
        FreezeMode.FE3_FULL_DETERMINISTIC_LIVE_LOOP,
        ("right", "right"),
    )
    result = exact_frozen_environment_parity(reference, candidate)
    assert not result.passed
    assert result.details["mode_exact"] is False
