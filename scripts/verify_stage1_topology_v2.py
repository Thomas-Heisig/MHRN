#!/usr/bin/env python3
"""Verify downloaded Stage-1 topology propagation v2 DATA deterministically."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from run_stage1_topology_v2 import (
    CONDITIONS,
    analyze,
    calibration_gate,
    summarize,
    validate_design,
)

ROOT = Path(__file__).resolve().parents[1]
EXP_ID = "EXP-S1-TOPO-V2-20260918"
OUT = ROOT / "research" / "experiments" / EXP_ID
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-V2.json"
CONFIG = ROOT / "configs" / "learning_experiment.yaml"
RUNNER = ROOT / "scripts" / "run_stage1_topology_v2.py"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    required = [
        OUT / "manifest.json",
        OUT / "report.md",
        OUT / "checksums.sha256",
        OUT / "data" / "calibration.json",
        OUT / "data" / "evaluation.json",
        OUT / "analysis" / "calibration_gate.json",
        OUT / "analysis" / "statistics.json",
    ]
    for path in required:
        if not path.is_file():
            fail(f"missing: {path.relative_to(ROOT)}", errors)
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        return 1

    prereg = read_json(PREREG)
    manifest = read_json(OUT / "manifest.json")
    calibration = read_json(OUT / "data" / "calibration.json")
    evaluation = read_json(OUT / "data" / "evaluation.json")
    gates = read_json(OUT / "analysis" / "calibration_gate.json")
    statistics = read_json(OUT / "analysis" / "statistics.json")

    expected_hashes = {
        "preregistration": sha256(PREREG),
        "config": sha256(CONFIG),
        "runner_source": sha256(RUNNER),
        "calibration_data": sha256(OUT / "data" / "calibration.json"),
        "evaluation_data": sha256(OUT / "data" / "evaluation.json"),
        "calibration_gate": sha256(OUT / "analysis" / "calibration_gate.json"),
        "statistics": sha256(OUT / "analysis" / "statistics.json"),
    }
    for key, digest in expected_hashes.items():
        if manifest["artifacts_sha256"].get(key) != digest:
            fail(f"manifest hash mismatch: {key}", errors)

    checksum_lines = (OUT / "checksums.sha256").read_text(encoding="utf-8").splitlines()
    checksum_map: dict[str, str] = {}
    for line in checksum_lines:
        parts = line.split("  ", 1)
        if len(parts) != 2:
            fail(f"malformed checksum line: {line}", errors)
            continue
        checksum_map[parts[1]] = parts[0]
    checksum_targets = {
        "manifest.json": OUT / "manifest.json",
        "report.md": OUT / "report.md",
        "data/calibration.json": OUT / "data" / "calibration.json",
        "data/evaluation.json": OUT / "data" / "evaluation.json",
        "analysis/calibration_gate.json": OUT / "analysis" / "calibration_gate.json",
        "analysis/statistics.json": OUT / "analysis" / "statistics.json",
    }
    for name, path in checksum_targets.items():
        if checksum_map.get(name) != sha256(path):
            fail(f"checksums.sha256 mismatch: {name}", errors)

    calibration_seeds = {int(v) for v in prereg["calibration"]["seeds"]}
    evaluation_seeds = {int(v) for v in prereg["evaluation"]["seeds"]}
    chosen_weight = statistics.get("chosen_synaptic_weight")
    if calibration_seeds & evaluation_seeds:
        fail("calibration and evaluation seeds overlap", errors)

    expected_conditions = set(CONDITIONS)
    calibration_conditions = {str(row["condition"]) for row in calibration}
    if calibration_conditions != expected_conditions:
        fail("calibration condition set mismatch", errors)

    if chosen_weight is not None:
        if len(evaluation) != len(evaluation_seeds) * len(CONDITIONS):
            fail("evaluation run count mismatch", errors)
        if {str(row["condition"]) for row in evaluation} != expected_conditions:
            fail("evaluation condition set mismatch", errors)
        if {int(row["seed"]) for row in evaluation} != evaluation_seeds:
            fail("evaluation seed set mismatch", errors)
        if not all(int(row["node_count"]) == 64 for row in evaluation):
            fail("evaluation contains non-64-neuron run", errors)
        if not all(float(row["synaptic_weight"]) == float(chosen_weight) for row in evaluation):
            fail("evaluation weight not frozen", errors)

        recomputed_summary = summarize(evaluation)
        recomputed_primary = analyze(evaluation, float(prereg["evaluation"]["alpha"]))
        recomputed_integrity = validate_design(
            prereg, calibration, evaluation, float(chosen_weight)
        )
        if statistics.get("condition_summary") != recomputed_summary:
            fail("condition summary differs from deterministic recomputation", errors)
        if statistics.get("primary_analysis") != recomputed_primary:
            fail("primary statistics differ from deterministic recomputation", errors)
        if statistics.get("integrity") != recomputed_integrity:
            fail("integrity assessment differs from deterministic recomputation", errors)
        if not recomputed_integrity["pass"]:
            fail("design integrity did not pass", errors)

    censor_sentinel = int(prereg["matched_budgets"]["evaluation_ticks"]) + 1
    endpoint_diagnostics: dict[str, Any] = {}
    for condition in CONDITIONS:
        rows = [row for row in evaluation if str(row["condition"]) == condition]
        active_values = sorted({float(row["active_fraction"]) for row in rows})
        latency_values = sorted(
            {int(row["first_output_latency_censored"]) for row in rows}
        )
        censored_count = 0
        for row in rows:
            latency = row.get("first_output_latency")
            censored = int(row["first_output_latency_censored"])
            if latency is None:
                censored_count += 1
                if censored != censor_sentinel:
                    fail(f"censor sentinel mismatch: {condition}", errors)
            elif censored != int(latency):
                fail(f"uncensored latency mismatch: {condition}", errors)
        endpoint_diagnostics[condition] = {
            "active_fraction_unique_values": active_values,
            "first_output_latency_censored_unique_values": latency_values,
            "censored_output_runs": censored_count,
        }

    candidates = [float(v) for v in prereg["calibration"]["candidate_synaptic_weights"]]
    recomputed_gates: list[dict[str, Any]] = []
    selected: float | None = None
    for candidate in candidates:
        if not any(float(row["synaptic_weight"]) == candidate for row in calibration):
            break
        gate = calibration_gate(calibration, candidate)
        recomputed_gates.append(gate)
        if gate["pass"]:
            selected = candidate
            break
    if gates != recomputed_gates:
        fail("calibration gate differs from deterministic recomputation", errors)
    if selected != chosen_weight:
        fail("chosen calibration weight does not match preregistered selection rule", errors)

    if manifest["source_freeze"].get("dirty_before_execution") is not False:
        fail("source freeze was dirty before execution", errors)
    if manifest.get("stage") != 1:
        fail("manifest stage mismatch", errors)
    if manifest.get("research_question") != "RQ-SNN-003":
        fail("research question mismatch", errors)
    if manifest.get("hypothesis") != "H-SNN-003-B":
        fail("hypothesis mismatch", errors)
    if manifest.get("scientific_evidence") is not False:
        fail("DATA was incorrectly promoted to EVID", errors)

    status = "PASS" if not errors else "FAIL"
    payload = {
        "status": status,
        "experiment_id": EXP_ID,
        "result_status": statistics.get("status"),
        "chosen_synaptic_weight": chosen_weight,
        "calibration_runs": len(calibration),
        "evaluation_runs": len(evaluation),
        "censor_sentinel": censor_sentinel,
        "endpoint_diagnostics": endpoint_diagnostics,
        "total_censored_output_runs": sum(
            int(item["censored_output_runs"]) for item in endpoint_diagnostics.values()
        ),
        "source_freeze": manifest["source_freeze"].get("commit"),
        "errors": errors,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
