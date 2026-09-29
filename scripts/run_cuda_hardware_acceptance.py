"""Run post-extraction CUDA hardware acceptance on a physical NVIDIA GPU.

This script is intentionally separate from hosted CI. It fails closed when
nvidia-smi is unavailable and enables the existing opt-in hardware tests.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full",
        action="store_true",
        help="rerun all recurrent/plasticity physical acceptance cases too",
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

    command = [
        sys.executable,
        "-m",
        "pytest",
        "-v",
        "--tb=short",
        "tests/test_cuda_wave4_backend.py::test_physical_cpu_cuda_cross_backend_d1_d2_parity",
    ]
    if args.full:
        command.extend(
            [
                "tests/test_playground_cuda_recurrent.py",
                "tests/test_playground_cuda_plasticity.py",
                "-k",
                "physical",
            ]
        )

    print("Running:", " ".join(command))
    completed = subprocess.run(command, cwd=ROOT, env=env, check=False)
    if completed.returncode:
        raise SystemExit(completed.returncode)

    print("CUDA post-extraction hardware acceptance: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
