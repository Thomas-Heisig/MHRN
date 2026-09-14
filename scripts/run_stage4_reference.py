"""Run the scoped Stage-4 specialized neural-area engineering reference.

The resulting JSON is an engineering verification artifact, not scientific
EVID.  The runner verifies typed modality pathways, modality-specific candidate
plasticity, exact digital integrity, the aggregated Stage-4 topology contract,
and the existing MSBA experiment-runner controls.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from src.embodiment.specialized_areas import (
    LATEST_MSBA_DATA,
    specialized_area_contract,
)
from src.version import MHRN_VERSION

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "research"
    / "generated"
    / "verification"
    / "specialized_neural_areas_reference_alpha3.json"
)

TEST_PATHS = (
    "tests/test_stage4_specialized_neural_areas.py",
    "tests/test_msba.py",
    "tests/test_signal_processing.py",
    "tests/test_neural_symbiosis.py",
    "tests/test_gateway_runtime.py",
    "tests/test_msba_experiment_runner.py",
    "tests/test_dashboard_embodiment_routes.py",
)


def _run_tests() -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *TEST_PATHS, "-q"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=900,
    )
    output = (result.stdout + "\n" + result.stderr).strip()
    return result.returncode == 0, output[-12_000:]


def _load_statistics(relative: str) -> dict[str, Any]:
    path = REPO_ROOT / relative / "analysis" / "statistics.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"statistics root must be an object: {path}")
    return value


def _data_checks() -> dict[str, bool]:
    e01 = _load_statistics(LATEST_MSBA_DATA[0])
    e04 = _load_statistics(LATEST_MSBA_DATA[3])
    e05 = _load_statistics(LATEST_MSBA_DATA[4])

    e01_conditions = e01["conditions"]
    accuracies = [
        row["metrics"]["task_accuracy"]["mean"]
        for row in e01_conditions.values()
    ]
    costs = {
        name: row["metrics"]["normalized_energy_units_per_correct_decision"][
            "mean"
        ]
        for name, row in e01_conditions.items()
    }
    e04_integrity = all(
        row["metrics"]["checksum_mismatches"]["max"] == 0.0
        and row["metrics"]["exact_payload_mismatches"]["max"] == 0.0
        for row in e04["conditions"].values()
    )
    e05_adaptive = e05["conditions"]["adaptive_compensation"]["metrics"]
    e05_fixed = e05["conditions"]["fixed_allocation"]["metrics"]
    return {
        "e01_matched_accuracy": len(set(accuracies)) == 1,
        "e01_modality_cost_order_observed": costs["digital"] < costs["audio"] < costs["vision"],
        "e04_exact_integrity_observed": e04_integrity,
        "e05_adaptive_compensation_exceeds_fixed_in_recorded_data": (
            e05_adaptive["task_recovery"]["mean"]
            > e05_fixed["task_recovery"]["mean"]
        ),
    }


def build_report(*, run_tests: bool = True) -> dict[str, Any]:
    contract = specialized_area_contract()
    topology = contract["topology"]
    probes = contract["reference_probes"]
    if not isinstance(topology, dict) or not isinstance(probes, dict):
        raise TypeError("invalid specialized-area contract")
    probe_rows = probes["probes"]
    if not isinstance(probe_rows, dict):
        raise TypeError("invalid Stage-4 probe suite")

    tests_passed: bool | None
    test_output = "tests not executed"
    if run_tests:
        tests_passed, test_output = _run_tests()
    else:
        tests_passed = None

    data_checks = _data_checks()
    proofs: dict[str, bool | None] = {
        "target_modalities_present": set(probe_rows) == {"audio", "vision", "digital"},
        "aggregated_stage4_lower_bound_satisfied": bool(
            topology["lower_bound_satisfied"]
        ),
        "scale_claim_remains_aggregated_not_dynamic": (
            topology["edges_materialized"] is False
            and topology["dynamic_scale_execution_verified"] is False
        ),
        "digital_reference_integrity_passes": bool(
            probe_rows["digital"]["exact_integrity_pass"]
        ),
        "canonical_core_remains_unmutated": all(
            row["canonical_core_mutated"] is False for row in probe_rows.values()
        ),
        "productive_activation_remains_locked": all(
            row["productive_activation_enabled"] is False
            for row in probe_rows.values()
        ),
        "latest_msba_data_checks_pass": all(data_checks.values()),
        "stage4_targeted_tests_pass": tests_passed,
    }
    verified = all(value is True for value in proofs.values())
    status = (
        "verified"
        if verified
        else "failed" if any(value is False for value in proofs.values()) else "incomplete"
    )
    return {
        "schema_version": 1,
        "suite": "specialized_neural_areas_reference",
        "stage": 4,
        "status": status,
        "scope": "engineering_verification",
        "software_version": MHRN_VERSION,
        "tests_executed": run_tests,
        "test_paths": list(TEST_PATHS),
        "test_output_tail": test_output,
        "contract": contract,
        "recorded_msba_data_checks": data_checks,
        "proofs": proofs,
        "scientific_promotion": {
            "automatic_evidence_promotion": False,
            "accepted_evid_created": False,
            "note": (
                "The reference verifies the scoped Stage-4 engineering contract and "
                "links existing MSBA DATA. It does not establish a dynamically executed "
                "100k-neuron/10M-edge multimodal SNN or scientific efficacy."
            ),
        },
        "limits": [
            "The 100k-neuron/10M-synapse lower bound is an aggregated topology budget, not a materialized dynamic run.",
            "Peripheral adapters remain experiment-only and productive activation remains locked.",
            "Candidate modality-specific plasticity mathematics is exercised without mutating canonical SNN learning state.",
            "The linked MSBA experiment series remains DATA until the project evidence workflow performs human review and any warranted EVID promotion.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args()
    report = build_report(run_tests=not args.skip_tests)
    output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Stage-4 reference: {report['status']} -> {output}")
    return 0 if report["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
