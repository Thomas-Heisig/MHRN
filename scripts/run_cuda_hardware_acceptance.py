"""Run canonical CUDA hardware acceptance on a physical NVIDIA GPU.

Hosted CI cannot prove physical CUDA execution. This runner groups the
post-extraction Wave-4 D1/D2 checks with the existing live Builder D3c bridge.
The Builder bridge is *not* the canonical Frozen-Environment FE-3 acceptance:
that remains pending until a live FrozenEnvironment -> backend adapter exists.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _gpu_identity() -> str:
    executable = shutil.which("nvidia-smi")
    if executable is None:
        raise SystemExit(
            "CUDA hardware acceptance requires nvidia-smi on a physical NVIDIA host"
        )
    completed = subprocess.run(
        [
            executable,
            "--query-gpu=name,driver_version",
            "--format=csv,noheader",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    identity = completed.stdout.strip()
    if not identity:
        raise SystemExit("nvidia-smi returned no GPU identity")
    return identity


def _run_case(
    *,
    label: str,
    selectors: list[str],
    env: dict[str, str],
) -> dict[str, object]:
    command = [sys.executable, "-m", "pytest", "-v", "--tb=short", *selectors]
    print(f"[{label}] Running:", " ".join(command))
    completed = subprocess.run(command, cwd=ROOT, env=env, check=False)
    return {
        "label": label,
        "passed": completed.returncode == 0,
        "returncode": completed.returncode,
        "selectors": selectors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full",
        action="store_true",
        help="rerun all recurrent/plasticity physical acceptance cases too",
    )
    parser.add_argument(
        "--include-fe3",
        action="store_true",
        help=(
            "also run the physical live Builder CPU/CUDA D3c bridge; "
            "this does not mark canonical Frozen-Environment FE-3 accepted"
        ),
    )
    parser.add_argument(
        "--require-gpu",
        default="",
        help="fail unless the reported GPU identity contains this string",
    )
    args = parser.parse_args()

    identity = _gpu_identity()
    print(f"CUDA hardware identity: {identity}")
    if args.require_gpu and args.require_gpu.lower() not in identity.lower():
        raise SystemExit(
            f"required GPU substring {args.require_gpu!r} not present in {identity!r}"
        )

    env = dict(os.environ)
    env["MHRN_TEST_CUDA_HARDWARE"] = "1"

    results: list[dict[str, object]] = []
    results.append(
        _run_case(
            label="WAVE4_D1_D2",
            selectors=[
                "tests/test_cuda_wave4_backend.py::"
                "test_physical_cpu_cuda_cross_backend_d1_d2_parity"
            ],
            env=env,
        )
    )

    if args.full:
        results.append(
            _run_case(
                label="WAVE4_RECURRENT_PLASTICITY_FULL",
                selectors=[
                    "tests/test_playground_cuda_recurrent.py",
                    "tests/test_playground_cuda_plasticity.py",
                    "-k",
                    "physical",
                ],
                env=env,
            )
        )

    bridge_status = "NOT_REQUESTED"
    if args.include_fe3:
        bridge = _run_case(
            label="BUILDER_D3C_BRIDGE",
            selectors=[
                "tests/test_playground_cuda_builder.py::"
                "test_full_pan_builder_hardware_d3"
            ],
            env=env,
        )
        results.append(bridge)
        bridge_status = "PASS" if bool(bridge["passed"]) else "FAIL"

    passed = all(bool(item["passed"]) for item in results)
    report = {
        "classification": "CUDA_HARDWARE_ACCEPTANCE_REPORT",
        "scientific_evidence": False,
        "gpu_identity": identity,
        "wave4_physical": "PASS" if bool(results[0]["passed"]) else "FAIL",
        "builder_d3c_bridge": bridge_status,
        "frozen_environment_fe3": "PENDING_LIVE_BACKEND_ADAPTER",
        "full_fe3_accepted": False,
        "kernel_semantics_changed": False,
        "results": results,
        "passed": passed,
    }
    print(json.dumps(report, sort_keys=True))

    if not passed:
        raise SystemExit(1)

    print("CUDA hardware acceptance selections: PASS")
    if args.include_fe3:
        print(
            "Builder D3c bridge: PASS; canonical Frozen-Environment FE-3 remains "
            "PENDING_LIVE_BACKEND_ADAPTER"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
