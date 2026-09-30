#!/usr/bin/env python3
"""Run FE-1/FE-2/FE-3 engineering acceptance for one frozen manifest."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable

from src.embodiment.deterministic import DeterministicTargetEnvironment
from src.embodiment.models import ActionCommand, EnvironmentObservation
from src.experience.frozen_environment import FreezeMode, FrozenWorldAdapter
from src.verification.frozen_environment import (
    load_manifest_artifact,
    run_fe1_integrity,
    run_fe2_replay_determinism,
    run_fe3_cpu_self_control,
)


def _target_world_factory(target: int) -> Callable[[], FrozenWorldAdapter]:
    def factory() -> FrozenWorldAdapter:
        return DeterministicTargetEnvironment(target=target)

    return factory


def _right_policy(
    tick: int,
    _previous: EnvironmentObservation | None,
) -> ActionCommand:
    return ActionCommand("target-actuator", tick, "right")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument(
        "--require-cuda",
        action="store_true",
        help=(
            "Fail unless canonical FrozenEnvironment FE-3 has a live backend adapter; "
            "the Builder D3c hardware bridge does not satisfy this gate."
        ),
    )
    args = parser.parse_args()

    manifest = load_manifest_artifact(args.manifest)
    results: list[dict[str, object]] = []

    if manifest.mode is FreezeMode.FE1_BOUNDARY_REPLAY:
        results.append(run_fe1_integrity(manifest).to_mapping())
    else:
        target = manifest.environment_config.get("target")
        if type(target) is not int:
            raise ValueError(
                "acceptance CLI currently supports deterministic-target manifests only"
            )
        factory = _target_world_factory(target)
        results.append(
            run_fe2_replay_determinism(
                manifest,
                factory,
                _right_policy,
                repeats=args.repeats,
            ).to_mapping()
        )
        if manifest.mode is FreezeMode.FE3_FULL_DETERMINISTIC_LIVE_LOOP:
            results.append(
                run_fe3_cpu_self_control(
                    manifest,
                    factory,
                    _right_policy,
                ).to_mapping()
            )

    cuda_status = "PENDING_FROZEN_ENVIRONMENT_LIVE_BACKEND_ADAPTER"
    passed = all(bool(item["passed"]) for item in results)
    if args.require_cuda:
        passed = False

    report = {
        "classification": "FROZEN_ENVIRONMENT_ACCEPTANCE_REPORT",
        "scientific_evidence": False,
        "manifest_sha256": manifest.manifest_sha256,
        "mode": manifest.mode.value,
        "results": results,
        "cuda_d3": cuda_status,
        "passed": passed,
    }
    print(json.dumps(report, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
