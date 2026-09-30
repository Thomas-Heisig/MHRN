"""Run canonical CUDA hardware acceptance on a physical NVIDIA GPU.

The runner always performs Wave-4 D1/D2. Optional FE-3 adds both the historical
Builder D3c bridge and the canonical FrozenEnvironment CPU-vs-CUDA live-loop
acceptance. All outputs are engineering verification only.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FE3_MANIFEST = (
    ROOT
    / "research"
    / "verification"
    / "frozen_environment"
    / "FE3_DETERMINISTIC_TARGET_V1.json"
)


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


def _last_json_object(stdout: str) -> dict[str, object] | None:
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def _run_command_case(
    *,
    label: str,
    command: list[str],
    env: dict[str, str],
    parse_report: bool = False,
) -> dict[str, object]:
    print(f"[{label}] Running:", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    result: dict[str, object] = {
        "label": label,
        "passed": completed.returncode == 0,
        "returncode": completed.returncode,
        "command": command,
    }
    if parse_report:
        result["report"] = _last_json_object(completed.stdout)
    return result


def _run_pytest_case(
    *,
    label: str,
    selectors: list[str],
    env: dict[str, str],
) -> dict[str, object]:
    return _run_command_case(
        label=label,
        command=[sys.executable, "-m", "pytest", "-v", "--tb=short", *selectors],
        env=env,
    )


def _write_artifacts(
    report: dict[str, object],
    output_dir: Path,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    day = datetime.now(timezone.utc).date().isoformat()
    json_path = output_dir / f"HARDWARE_ACCEPTANCE_{day}.json"
    markdown_path = output_dir / f"HARDWARE_ACCEPTANCE_{day}.md"
    json_path.write_text(
        json.dumps(report, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        "\n".join(
            [
                f"# Hardware Acceptance {day}",
                "",
                "**Classification:** Engineering Verification; not DATA/EVID.",
                "",
                f"- GPU: {report['gpu_identity']}",
                f"- Wave-4 D1/D2: {report['wave4_physical']}",
                f"- Builder D3c bridge: {report['builder_d3c_bridge']}",
                f"- Canonical Frozen-Environment FE-3: {report['frozen_environment_fe3']}",
                f"- Full FE-3 accepted: {report['full_fe3_accepted']}",
                "",
                "## Interpretation boundary",
                "",
                "- No scientific EVID or CLAIM is created.",
                "- No speedup claim is created.",
                "- PAN hyperstate is not in scope.",
                "- Canonical learning semantics are not in scope.",
                "- CPU/CUDA execution fingerprints are expected to differ because backend identity is provenance.",
                "- Exact FE-3 acceptance requires the same manifest hash, live-input fingerprint and D3c trajectory hash.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return json_path, markdown_path


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
            "add canonical Frozen-Environment FE-3 CPU-vs-CUDA D3c acceptance "
            "and the historical Builder D3c bridge; Wave-4 checks still run"
        ),
    )
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_FE3_MANIFEST),
        help="versioned FE-3 manifest artifact used by --include-fe3",
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "docs" / "canonical"),
        help="write dated JSON and Markdown engineering-verification artifacts here",
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
        _run_pytest_case(
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
            _run_pytest_case(
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
    fe3_status = "NOT_REQUESTED"
    full_fe3_accepted = False
    if args.include_fe3:
        bridge = _run_pytest_case(
            label="BUILDER_D3C_BRIDGE",
            selectors=[
                "tests/test_playground_cuda_builder.py::"
                "test_full_pan_builder_hardware_d3"
            ],
            env=env,
        )
        results.append(bridge)
        bridge_status = "PASS" if bool(bridge["passed"]) else "FAIL"

        fe3 = _run_command_case(
            label="FROZEN_ENVIRONMENT_FE3_CPU_CUDA_D3C",
            command=[
                sys.executable,
                "scripts/run_fe_acceptance.py",
                "--manifest",
                str(Path(args.manifest)),
                "--require-cuda",
            ],
            env=env,
            parse_report=True,
        )
        results.append(fe3)
        fe3_status = "PASS" if bool(fe3["passed"]) else "FAIL"
        full_fe3_accepted = bool(fe3["passed"])

    passed = all(bool(item["passed"]) for item in results)
    report: dict[str, object] = {
        "classification": "CUDA_HARDWARE_ACCEPTANCE_REPORT",
        "scientific_evidence": False,
        "gpu_identity": identity,
        "wave4_physical": "PASS" if bool(results[0]["passed"]) else "FAIL",
        "builder_d3c_bridge": bridge_status,
        "frozen_environment_fe3": fe3_status,
        "full_fe3_accepted": full_fe3_accepted,
        "fe3_manifest": str(Path(args.manifest)),
        "kernel_semantics_changed": False,
        "execution_fingerprint_rule": (
            "BACKEND_IDENTITY_IS_PROVENANCE; CPU/CUDA FINGERPRINTS DIFFER"
        ),
        "limitations": {
            "speedup_claim": False,
            "pan_hyperstate": False,
            "canonical_learning_contract": False,
            "scientific_data": False,
            "evidence": False,
        },
        "results": results,
        "passed": passed,
    }
    json_path, markdown_path = _write_artifacts(report, Path(args.output_dir))
    report["artifact_json"] = str(json_path)
    report["artifact_markdown"] = str(markdown_path)
    print(json.dumps(report, sort_keys=True))

    if not passed:
        raise SystemExit(1)

    print("CUDA hardware acceptance selections: PASS")
    if args.include_fe3:
        print(
            "Canonical Frozen-Environment FE-3 CPU/CUDA D3c: PASS; "
            "engineering verification only"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
