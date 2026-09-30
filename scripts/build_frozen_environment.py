#!/usr/bin/env python3
"""Build a deterministic Frozen-Environment engineering manifest artifact."""

from __future__ import annotations

import argparse
import json

from src.embodiment.deterministic import DeterministicTargetEnvironment
from src.embodiment.msba import SymbolFrame
from src.embodiment.neural_io_contracts import BoundaryFrame
from src.experience.frozen_environment import (
    FreezeMode,
    FrozenBoundaryFrame,
    FrozenEnvironmentManifest,
    RNGContractMode,
    WorldRNGContract,
)
from src.verification.frozen_environment import write_manifest_artifact


def _boundary_frame(tick: int) -> FrozenBoundaryFrame:
    symbol = SymbolFrame(
        payload=json.dumps({"tick": tick}, sort_keys=True).encode("utf-8"),
        codec="json",
        sequence=tick,
        provenance="fe-builder",
    )
    return FrozenBoundaryFrame.from_frame(
        BoundaryFrame(
            schema_version=1,
            frame_id=f"fe-frame-{tick}",
            stream_id="fe-sensor",
            sequence=tick,
            direction="INBOUND",
            kind="DIGITAL",
            content_type="application/json",
            schema_id="fe-builder-v1",
            symbol_frame=symbol,
            correlation_id=f"fe-{tick}",
            priority=0,
            source_id="fe-builder",
            provenance="engineering-verification",
            arrival_time_ns=None,
            admitted_tick=tick,
        )
    )


def _build(mode: FreezeMode, *, target: int, ticks: int, seed: int) -> FrozenEnvironmentManifest:
    if ticks < 1:
        raise ValueError("ticks must be >= 1")
    schedule = tuple(range(ticks))
    if mode is FreezeMode.FE1_BOUNDARY_REPLAY:
        return FrozenEnvironmentManifest(
            mode=mode,
            environment_id="boundary-replay-v1",
            environment_version="1",
            environment_config={"builder": "deterministic-fixture"},
            rng=WorldRNGContract(
                algorithm="none",
                version="1",
                mode=RNGContractMode.NONE,
                initial_fingerprint="none",
            ),
            sensor_schedule=schedule,
            action_schema={"kind": "none"},
            reward_contract={"kind": "none"},
            episode_policy={"reset": "explicit"},
            boundary_frames=tuple(_boundary_frame(tick) for tick in schedule),
        )

    env = DeterministicTargetEnvironment(target=target)
    env.reset(seed=seed)
    return FrozenEnvironmentManifest(
        mode=mode,
        environment_id=env.environment_id,
        environment_version="1",
        environment_config={"target": target},
        rng=WorldRNGContract(
            algorithm="none",
            version="1",
            mode=RNGContractMode.NONE,
            initial_fingerprint=env.rng_fingerprint(),
        ),
        sensor_schedule=schedule,
        action_schema={
            "actuator_id": "target-actuator",
            "actions": ["left", "right"],
        },
        reward_contract={"type": "target-hit", "hit_reward": 1.0},
        episode_policy={
            "reset": "explicit",
            "pending_rewards_cross_episode": False,
        },
        initial_world_state=env.snapshot_state(),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=[mode.value for mode in FreezeMode], required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--target", type=int, default=2)
    parser.add_argument("--ticks", type=int, default=2)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    manifest = _build(
        FreezeMode(args.mode),
        target=args.target,
        ticks=args.ticks,
        seed=args.seed,
    )
    path = write_manifest_artifact(args.output, manifest)
    print(
        json.dumps(
            {
                "classification": "FROZEN_ENVIRONMENT_ENGINEERING_ARTIFACT",
                "scientific_evidence": False,
                "path": str(path),
                "mode": manifest.mode.value,
                "manifest_sha256": manifest.manifest_sha256,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
