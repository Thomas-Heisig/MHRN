#!/usr/bin/env python3
"""Verify Stage-1 topology v3 R1 time-resolved replication DATA."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from run_stage1_topology_v3_r1 import (
    CONDITIONS,
    EXP_ID,
    analyze,
    read_json,
    sha256,
    summarize,
    validate_design,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "experiments" / EXP_ID
PREREG = (
    ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-V3-R1-TIME-RESOLVED.json"
)
CONFIG = ROOT / "configs" / "learning_experiment.yaml"
RUNNER = ROOT / "scripts" / "run_stage1_topology_v3_r1.py"


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    required = [
        OUT / "manifest.json",
        OUT / "report.md",
        OUT / "checksums.sha256",
        OUT / "data" / "evaluation.json",
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
    evaluation_raw: Any = json.loads(
        (OUT / "data" / "evaluation.json").read_text(encoding="utf-8")
    )
    if not isinstance(evaluation_raw, list):
        fail("evaluation data is not a list", errors)
        evaluation: list[dict[str, Any]] = []
    else:
        evaluation = [dict(row) for row in evaluation_raw if isinstance(row, dict)]
    statistics = read_json(OUT / "analysis" / "statistics.json")

    expected_hashes = {
        "preregistration": sha256(PREREG),
        "config": sha256(CONFIG),
        "runner_source": sha256(RUNNER),
        "evaluation_data": sha256(OUT / "data" / "evaluation.json"),
        "statistics": sha256(OUT / "analysis" / "statistics.json"),
    }
    for key, digest in expected_hashes.items():
        if manifest.get("artifacts_sha256", {}).get(key) != digest:
            fail(f"manifest hash mismatch: {key}", errors)

    checksum_map: dict[str, str] = {}
    for line in (OUT / "checksums.sha256").read_text(encoding="utf-8").splitlines():
        parts = line.split("  ", 1)
        if len(parts) != 2:
            fail(f"malformed checksum line: {line}", errors)
            continue
        checksum_map[parts[1]] = parts[0]
    for name in (
        "manifest.json",
        "report.md",
        "data/evaluation.json",
        "analysis/statistics.json",
    ):
        path = OUT / name
        if checksum_map.get(name) != hashlib.sha256(path.read_bytes()).hexdigest():
            fail(f"checksums.sha256 mismatch: {name}", errors)

    recomputed_summary = summarize(evaluation)
    recomputed_analysis = analyze(evaluation, prereg)
    recomputed_integrity = validate_design(prereg, evaluation)

    if statistics.get("schema_version") != 1:
        fail("statistics schema_version mismatch", errors)
    if statistics.get("condition_summary") != recomputed_summary:
        fail("condition summary differs from deterministic recomputation", errors)
    if statistics.get("analysis") != recomputed_analysis:
        fail("analysis differs from deterministic recomputation", errors)
    if statistics.get("integrity") != recomputed_integrity:
        fail("integrity differs from deterministic recomputation", errors)
    if not recomputed_integrity["pass"]:
        fail("design integrity did not pass", errors)

    if manifest.get("source_freeze", {}).get("dirty_before_execution") is not False:
        fail("source tree was dirty before execution", errors)
    if manifest.get("research_question") != "RQ-SNN-003":
        fail("research question mismatch", errors)
    if manifest.get("hypothesis") != "H-SNN-003-B":
        fail("hypothesis mismatch", errors)
    if manifest.get("scientific_evidence") is not False:
        fail("DATA was incorrectly promoted to EVID", errors)

    censor = int(prereg["evaluation"]["censor_sentinel"])
    diagnostics: dict[str, Any] = {}
    for condition in CONDITIONS:
        rows = [row for row in evaluation if str(row.get("condition")) == condition]
        diagnostics[condition] = {
            "n": len(rows),
            "final_active_fraction_unique": sorted(
                {float(row["final_active_fraction"]) for row in rows}
            ),
            "activation_auc_0_32_unique_count": len(
                {float(row["activation_auc_0_32"]) for row in rows}
            ),
            "half_activation_censored_runs": sum(
                int(row["half_activation_latency_censored"]) == censor for row in rows
            ),
            "first_output_censored_runs": sum(
                int(row["first_output_latency_censored"]) == censor for row in rows
            ),
        }

    payload = {
        "status": "PASS" if not errors else "FAIL",
        "experiment_id": EXP_ID,
        "result_status": recomputed_analysis["status"],
        "evaluation_runs": len(evaluation),
        "ceiling_resolution_supported": recomputed_analysis[
            "ceiling_resolution_supported"
        ],
        "replication_supported": recomputed_analysis["replication_supported"],
        "diagnostics": diagnostics,
        "source_freeze": manifest.get("source_freeze", {}).get("commit"),
        "errors": errors,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
