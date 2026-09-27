#!/usr/bin/env python3
"""Prospective promotion-eligible Stage-1 Temporal-Order replication.

The historical V2 task implementation is reused without rewriting its DATA.
This wrapper executes fresh preregistered seeds and records the current
EvidenceEngine provenance contract. Execution creates DATA only.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import time
from pathlib import Path
from typing import Any

import yaml

from src.research.experiment_recorder import ExperimentRecorder
from src.research_assistant.governance import (
    DataPartition,
    NetworkMode,
    ResearchRunMode,
)

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TEMP-PROMO-R1.json"
EXPERIMENT_ID = "EXP-S1-TEMP-PROMO-R1-20260927"
OUT = ROOT / "research" / "experiments" / EXPERIMENT_ID
CANDIDATE = ROOT / "scripts" / "run_stage1_temporal_order_v2.py"
CONFIG = ROOT / "configs" / "learning_experiment.yaml"

HISTORICAL_SEEDS = (
    set(range(101, 121))
    | set(range(2101, 2121))
    | set(range(6101, 6121))
    | set(range(6201, 6221))
    | set(range(6301, 6321))
    | set(range(7101, 7121))
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _canonical_digest(value: object) -> str:
    raw = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return _sha256_bytes(raw)


def _tracked_source_digest() -> str:
    names = (
        subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
        .decode()
        .split("\0")
    )
    selected: dict[str, str] = {}
    include_exact = {
        "pyproject.toml",
        "configs/learning_experiment.yaml",
        "research/preregistrations/PREREG-S1-TEMP-PROMO-R1.json",
    }
    for name in names:
        if not name:
            continue
        if name.startswith(("src/", "scripts/")) or name in include_exact:
            selected[name] = _sha256_file(ROOT / name)
    return _canonical_digest(selected)


def _load_candidate() -> Any:
    spec = importlib.util.spec_from_file_location("stage1_temporal_order_v2", CANDIDATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load run_stage1_temporal_order_v2.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.EXP_ID = EXPERIMENT_ID
    return module


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _integrity(
    runs: list[dict[str, Any]], prereg: dict[str, Any], temporal: Any
) -> dict[str, Any]:
    seeds = {int(v) for v in prereg["evaluation"]["seeds"]}
    checks = {
        "run_count": len(runs)
        == len(seeds) * len(temporal.ARMS) * len(temporal.ORDERS),
        "coverage": all(
            sum(
                int(r["seed"]) == seed and r["arm"] == arm and r["order"] == order
                for r in runs
            )
            == 1
            for seed in seeds
            for arm in temporal.ARMS
            for order in temporal.ORDERS
        ),
        "network_budget": all(
            int(r["node_count"]) == 6 and int(r["edge_count"]) == 4 for r in runs
        ),
        "paired_parameters": all(
            len(
                {
                    (
                        round(float(r["synaptic_weight"]), 12),
                        round(float(r["stimulus_current"]), 12),
                        round(float(r["total_injected_charge"]), 12),
                    )
                    for r in runs
                    if int(r["seed"]) == seed
                }
            )
            == 1
            for seed in seeds
        ),
        "arm_set": {str(r["arm"]) for r in runs} == {"intact", "identity_destroyed"},
        "order_set": {str(r["order"]) for r in runs}
        == {"forward", "reverse", "simultaneous"},
        "historical_seed_disjoint": seeds.isdisjoint(HISTORICAL_SEEDS),
        "unique_seed_count": len(seeds) == len(prereg["evaluation"]["seeds"]) == 20,
        "matched_injected_charge": all(
            len(
                {
                    round(float(r["total_injected_charge"]), 12)
                    for r in runs
                    if int(r["seed"]) == seed
                }
            )
            == 1
            for seed in seeds
        ),
    }
    return {"checks": checks, "pass": all(checks.values())}


def _report(
    prereg: dict[str, Any],
    analysis: dict[str, Any],
    integrity: dict[str, Any],
    run_count: int,
) -> str:
    summary = analysis["summary"]
    ci = summary["paired_accuracy_delta_bootstrap_ci95"]
    return (
        f"# {EXPERIMENT_ID}: Stage-1 Temporal-Order promotion R1\n\n"
        f"**Claim:** `{prereg['claim_id']}`  \n"
        f"**RQ/H:** `{prereg['research_question']}` / `{prereg['hypothesis']}`  \n"
        "**Role:** promotion-eligible DATA; no automatic EVID promotion  \n"
        "**Independent replication:** false\n\n"
        "## Result\n\n"
        f"- status: `{analysis['status']}`\n"
        f"- design integrity: {integrity['pass']}\n"
        f"- evaluation runs: {run_count}\n"
        f"- intact order accuracy median: {summary['intact_order_accuracy_median']:.6g}\n"
        f"- identity-destroyed order accuracy median: "
        f"{summary['identity_destroyed_order_accuracy_median']:.6g}\n"
        f"- simultaneous control success: "
        f"{summary['intact_simultaneous_success_fraction']:.6g}\n"
        f"- paired accuracy delta median: {summary['paired_accuracy_delta_median']:.6g}\n"
        f"- paired delta CI95: [{ci[0]:.6g}, {ci[1]:.6g}]\n"
        f"- paired sign-test p: {summary['paired_sign_test_p']:.9g}\n\n"
        "## Claim boundary\n\n"
        f"{prereg['claim_boundary']}\n"
    )


def main() -> int:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    if prereg.get("status") != "FROZEN_BEFORE_PROMOTION_REPLICATION":
        raise RuntimeError("promotion preregistration is not frozen")
    if prereg.get("execution_authorized") is not True:
        raise RuntimeError("promotion replication is not authorized")
    if prereg.get("claim_id") != "CLAIM-S1-TEMP-001":
        raise RuntimeError("unexpected scoped claim")
    if prereg["evidence_engine_contract"]["automatic_evidence_promotion"]:
        raise RuntimeError("automatic EVID promotion must remain disabled")
    if OUT.exists():
        raise FileExistsError(f"Refusing to overwrite existing experiment: {OUT}")

    seeds = {int(seed) for seed in prereg["evaluation"]["seeds"]}
    if len(seeds) != len(prereg["evaluation"]["seeds"]):
        raise RuntimeError("evaluation seeds must be unique")
    if seeds & HISTORICAL_SEEDS:
        raise RuntimeError("promotion seeds overlap historical Stage-1 seeds")

    recorder = ExperimentRecorder(EXPERIMENT_ID, output_dir=OUT, fail_fast=True)
    if recorder.manifest["git"].get("dirty") is not False:
        raise RuntimeError("promotion replication requires a clean git tree")

    started = time.perf_counter()
    temporal = _load_candidate()
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))

    runs = [
        temporal.simulate(config, prereg, int(seed), arm, order)
        for seed in prereg["evaluation"]["seeds"]
        for arm in temporal.ARMS
        for order in temporal.ORDERS
    ]
    analysis = temporal.analyze(runs, prereg)
    integrity = _integrity(runs, prereg, temporal)
    if not integrity["pass"]:
        analysis["status"] = "NOT_TESTED_INTEGRITY_FAILURE"

    data_path = OUT / "data" / "evaluation.json"
    stats_path = OUT / "analysis" / "statistics.json"
    report_path = OUT / "report.md"
    _write_json(data_path, runs)
    _write_json(
        stats_path,
        {
            "schema_version": 1,
            "experiment_id": EXPERIMENT_ID,
            "claim_id": prereg["claim_id"],
            "protocol": prereg["protocol"],
            "analysis": analysis,
            "integrity": integrity,
            "claim_boundary": prereg["claim_boundary"],
        },
    )
    report_path.write_text(
        _report(prereg, analysis, integrity, len(runs)), encoding="utf-8"
    )

    config_digest = _sha256_file(PREREG)
    prompt_digest = _sha256_bytes(b"NO_PROMPT_STAGE1_TEMPORAL_PROMOTION_R1")
    analysis_digest = _sha256_bytes(
        b"TEMP_V2_PAIRED_SIGN_TEST_BOOTSTRAP_IDENTITY_DESTROYED_CONTROL"
    )
    code_digest = _tracked_source_digest()
    data_digest = _sha256_file(data_path)

    recorder.record_config(
        str(PREREG.relative_to(ROOT)).replace("\\", "/"), config_digest
    )
    recorder.record_research_links(
        research_questions=[prereg["research_question"]],
        hypotheses=[prereg["hypothesis"]],
    )
    recorder.record_research_run_mode(ResearchRunMode.REPLICATION)
    recorder.record_network_mode(NetworkMode.OFFLINE)
    recorder.record_data_partition(DataPartition.SCIENTIFIC_HOLDOUT)
    recorder.lock_confirmatory_run(
        protocol=prereg,
        prompt_digest=prompt_digest,
        analysis_digest=analysis_digest,
    )
    recorder.record_research_run_mode(ResearchRunMode.REPLICATION)
    recorder.record_simulation_params(
        seeds=sorted(seeds),
        dt_ms=1.0,
        neuron_count=6,
        edge_count=4,
        arms=list(temporal.ARMS),
        orders=list(temporal.ORDERS),
    )
    recorder.record_artifact("evaluation_data", "data/evaluation.json")
    recorder.record_artifact("statistics", "analysis/statistics.json")
    recorder.record_artifact("report", "report.md")
    recorder.record_artifact(
        "preregistration", str(PREREG.relative_to(ROOT)).replace("\\", "/")
    )
    recorder.record_provenance_digests(
        code_digest=code_digest,
        config_digest=config_digest,
        prompt_digest=prompt_digest,
        data_digest=data_digest,
    )
    recorder.record_results(
        claim_id=prereg["claim_id"],
        protocol=prereg["protocol"],
        replication_class="INTERNAL_PROMOTION_REPLICATION",
        result_status=analysis["status"],
        design_integrity_passed=bool(integrity["pass"]),
        intact_order_accuracy_median=float(
            analysis["summary"]["intact_order_accuracy_median"]
        ),
        identity_destroyed_order_accuracy_median=float(
            analysis["summary"]["identity_destroyed_order_accuracy_median"]
        ),
        paired_accuracy_delta_median=float(
            analysis["summary"]["paired_accuracy_delta_median"]
        ),
        automatic_evidence_promotion=False,
        scientific_evidence=False,
        human_review_required=True,
        independent_authorship_replication=False,
    )
    recorder.record_runtime(time.perf_counter() - started)
    recorder.mark_completed().save()

    print((OUT / "manifest.json").read_text(encoding="utf-8"))
    if not integrity["pass"]:
        raise SystemExit("STAGE1_TEMPORAL_PROMOTION_INTEGRITY_FAILURE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
