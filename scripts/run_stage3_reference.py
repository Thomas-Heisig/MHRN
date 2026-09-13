"""Run the scoped Stage-3 plastic neural tissue engineering reference.

This runner deliberately separates engineering verification from scientific
promotion. It executes the existing mechanism-level tests for STDP,
three-factor learning, homeostasis, structural plasticity and checkpointed
learning state, then runs matched deterministic learning controls.

The generated JSON is a verification artifact. It is not an EVID record and
must not be used to promote a scientific claim automatically.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, cast

import yaml

from src.experiments.learning_lab import run_learning_experiment
from src.version import MHRN_VERSION

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "research"
    / "generated"
    / "verification"
    / "plastic_neural_tissue_reference.json"
)
CONFIG_PATH = REPO_ROOT / "configs" / "learning_experiment.yaml"

TEST_GROUPS: dict[str, tuple[str, ...]] = {
    "stdp_and_three_factor": (
        "tests/test_stdp_integration.py",
        "tests/test_reward.py",
        "tests/test_learning_experiment.py",
    ),
    "homeostasis": ("tests/test_homeostasis_engine.py",),
    "structural_plasticity": (
        "tests/test_structural_e2e.py",
        "tests/test_structural_determinism.py",
    ),
    "learning_state_checkpoint": ("tests/test_checkpoint_v4.py",),
}


def _load_config() -> dict[str, Any]:
    raw_object: object = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw_object, dict):
        raise TypeError("learning experiment config root must be a mapping")
    raw = cast(dict[object, object], raw_object)
    return {str(key): value for key, value in raw.items()}


def _run_test_group(paths: tuple[str, ...]) -> bool:
    missing = [path for path in paths if not (REPO_ROOT / path).is_file()]
    if missing:
        return False
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *paths, "-q"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=600,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
    return result.returncode == 0


def _condition_payload(result: Any) -> dict[str, Any]:
    payload = asdict(result)
    payload["learned"] = bool(result.learned)
    return payload


def build_report(*, run_tests: bool = True) -> dict[str, Any]:
    """Build a deterministic Stage-3 verification report."""
    config = _load_config()

    learning_on = run_learning_experiment(config, "learning_on")
    learning_on_replay = run_learning_experiment(config, "learning_on")
    learning_off = run_learning_experiment(config, "learning_off")
    sham_replay = run_learning_experiment(config, "sham_replay")

    on_payload = _condition_payload(learning_on)
    replay_payload = _condition_payload(learning_on_replay)
    off_payload = _condition_payload(learning_off)
    sham_payload = _condition_payload(sham_replay)

    group_results = {
        name: (_run_test_group(paths) if run_tests else None)
        for name, paths in TEST_GROUPS.items()
    }

    finite_means = all(
        math.isfinite(float(payload["final_mean_weight"]))
        for payload in (on_payload, replay_payload, off_payload, sham_payload)
    )
    bounded_means = all(
        0.0 <= float(payload["final_mean_weight"]) <= 1.0
        for payload in (on_payload, replay_payload, off_payload, sham_payload)
    )

    proofs: dict[str, bool | None] = {
        "stdp_and_three_factor_tests_passed": group_results["stdp_and_three_factor"],
        "homeostasis_tests_passed": group_results["homeostasis"],
        "structural_plasticity_tests_passed": group_results["structural_plasticity"],
        "learning_state_checkpoint_tests_passed": group_results[
            "learning_state_checkpoint"
        ],
        "three_factor_learning_changes_weights": bool(
            learning_on.reward_weight_updates > 0
            and learning_on.final_mean_weight > learning_on.initial_mean_weight
        ),
        "learning_on_changes_fresh_probe_response": bool(learning_on.learned),
        "learning_off_control_has_no_reward_updates": bool(
            learning_off.reward_weight_updates == 0
            and math.isclose(
                learning_off.final_mean_weight,
                learning_off.initial_mean_weight,
                rel_tol=0.0,
                abs_tol=1e-15,
            )
        ),
        "sham_replay_destroys_eligibility_effect": bool(
            sham_replay.reward_weight_updates == 0
            and math.isclose(
                sham_replay.final_mean_weight,
                sham_replay.initial_mean_weight,
                rel_tol=0.0,
                abs_tol=1e-15,
            )
        ),
        "deterministic_learning_replay_identity": on_payload == replay_payload,
        "finite_bounded_weight_summary": finite_means and bounded_means,
    }
    verified = all(value is True for value in proofs.values())
    status = (
        "verified"
        if verified
        else (
            "failed"
            if any(value is False for value in proofs.values())
            else "incomplete"
        )
    )

    return {
        "schema_version": 1,
        "suite": "plastic_neural_tissue_reference",
        "stage": 3,
        "status": status,
        "tests_executed": run_tests,
        "scope": "engineering_verification",
        "software_version": MHRN_VERSION,
        "protocol": {
            "config": "configs/learning_experiment.yaml",
            "protocol_id": learning_on.protocol_id,
            "protocol_version": learning_on.protocol_version,
            "conditions": ["learning_on", "learning_off", "sham_replay"],
            "deterministic_replay": True,
        },
        "test_groups": {
            name: {"paths": list(paths), "passed": group_results[name]}
            for name, paths in TEST_GROUPS.items()
        },
        "conditions": {
            "learning_on": on_payload,
            "learning_off": off_payload,
            "sham_replay": sham_payload,
        },
        "proofs": proofs,
        "scientific_promotion": {
            "automatic_evidence_promotion": False,
            "note": (
                "This reference closes a scoped engineering verification gap only. "
                "Preregistered independent learning-on/off/holdout runs and human "
                "evidence review remain required for scientific claims."
            ),
        },
        "limits": [
            "The reference uses the bounded learning-experiment topology rather than the declared 10,000-100,000 neuron Stage-3 scale.",
            "Passing the reference does not establish long-horizon stability for arbitrary plastic networks or reward formulations.",
            "Structural plasticity is verified by the existing deterministic E2E suite; this runner does not claim biological tissue equivalence.",
            "No cognition or consciousness inference follows from plasticity verification.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Recompute deterministic learning controls without spawning pytest groups.",
    )
    args = parser.parse_args()
    report = build_report(run_tests=not args.skip_tests)
    output = args.output
    if not output.is_absolute():
        output = REPO_ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Stage-3 reference: {report['status']} -> {output}")
    return 0 if report["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
