#!/usr/bin/env python3
"""Prospective promotion-eligible Stage-1 topology replication.

This runner reuses the already verified V3-R1 topology implementation but writes
a new append-only experiment with fresh seeds and the current EvidenceEngine
provenance contract. Execution creates DATA only; EVID promotion is separate.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import time
from pathlib import Path
from typing import Any

from src.research.experiment_recorder import ExperimentRecorder
from src.research_assistant.governance import (
    DataPartition,
    NetworkMode,
    ResearchRunMode,
)

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-PROMO-R1.json"
EXPERIMENT_ID = "EXP-S1-TOPO-PROMO-R1-20260927"
OUT = ROOT / "research" / "experiments" / EXPERIMENT_ID
CANDIDATE = ROOT / "scripts" / "run_stage1_topology_v3_r1.py"
CONFIG = ROOT / "configs" / "learning_experiment.yaml"

HISTORICAL_SEEDS = (
    set(range(2101, 2121)) | set(range(6101, 6121)) | set(range(6201, 6221))
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
        "research/preregistrations/PREREG-S1-TOPO-PROMO-R1.json",
    }
    for name in names:
        if not name:
            continue
        if name.startswith(("src/", "scripts/")) or name in include_exact:
            selected[name] = _sha256_file(ROOT / name)
    return _canonical_digest(selected)


def _load_candidate() -> Any:
    spec = importlib.util.spec_from_file_location("stage1_topology_v3_r1", CANDIDATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load run_stage1_topology_v3_r1.py")
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


def _report(
    prereg: dict[str, Any],
    summary: dict[str, Any],
    analysis: dict[str, Any],
    integrity: dict[str, Any],
) -> str:
    return (
        f"# {EXPERIMENT_ID}: Stage-1 topology promotion R1\n\n"
        f"**Claim:** `{prereg['claim_id']}`  \n"
        f"**RQ/H:** `{prereg['research_question']}` / `{prereg['hypothesis']}`  \n"
        "**Role:** promotion-eligible DATA; no automatic EVID promotion  \n"
        "**Independent replication:** false\n\n"
        "## Result\n\n"
        f"- status: `{analysis['status']}`\n"
        f"- design integrity: {integrity['pass']}\n"
        f"- ceiling-resolution criterion: {analysis['ceiling_resolution_supported']}\n"
        f"- V2-latency replication criterion: {analysis['replication_supported']}\n"
        f"- evaluation runs: {sum(int(v['n']) for v in summary.values())}\n\n"
        "## Claim boundary\n\n"
        f"{prereg['interpretation_boundary']}\n"
    )


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    if prereg.get("status") != "FROZEN_BEFORE_PROMOTION_REPLICATION":
        raise RuntimeError("promotion preregistration is not frozen")
    if prereg.get("execution_authorized") is not True:
        raise RuntimeError("promotion replication is not authorized")
    if prereg.get("claim_id") != "CLAIM-S1-TOPO-001":
        raise RuntimeError("unexpected scoped claim")
    if prereg["evidence_engine_contract"]["automatic_evidence_promotion"]:
        raise RuntimeError("automatic EVID promotion must remain disabled")
    if OUT.exists():
        raise FileExistsError(f"Refusing to overwrite existing experiment: {OUT}")

    seeds = {int(seed) for seed in prereg["evaluation"]["seeds"]}
    if len(seeds) != len(prereg["evaluation"]["seeds"]):
        raise RuntimeError("evaluation seeds must be unique")
    if seeds & HISTORICAL_SEEDS:
        raise RuntimeError("promotion seeds overlap historical topology seeds")

    recorder = ExperimentRecorder(EXPERIMENT_ID, output_dir=OUT, fail_fast=True)
    if recorder.manifest["git"].get("dirty") is not False:
        raise RuntimeError("promotion replication requires a clean git tree")

    started = time.perf_counter()
    topo = _load_candidate()
    base_config = topo.load_config()

    evaluation: list[dict[str, Any]] = []
    for seed in prereg["evaluation"]["seeds"]:
        for condition in topo.CONDITIONS:
            evaluation.append(topo.simulate(base_config, prereg, condition, int(seed)))

    summary = topo.summarize(evaluation)
    analysis = topo.analyze(evaluation, prereg)
    integrity = topo.validate_design(prereg, evaluation)
    integrity.setdefault("checks", {})["all_historical_topology_seeds_disjoint"] = (
        seeds.isdisjoint(HISTORICAL_SEEDS)
    )
    integrity["pass"] = bool(
        integrity.get("pass")
        and integrity["checks"]["all_historical_topology_seeds_disjoint"]
    )
    if not integrity["pass"]:
        analysis["status"] = "NOT_TESTED_INTEGRITY_FAILURE"

    data_path = OUT / "data" / "evaluation.json"
    stats_path = OUT / "analysis" / "statistics.json"
    report_path = OUT / "report.md"
    _write_json(data_path, evaluation)
    _write_json(
        stats_path,
        {
            "schema_version": 1,
            "experiment_id": EXPERIMENT_ID,
            "claim_id": prereg["claim_id"],
            "protocol": prereg["protocol"],
            "condition_summary": summary,
            "analysis": analysis,
            "integrity": integrity,
            "claim_boundary": prereg["interpretation_boundary"],
        },
    )
    report_path.write_text(
        _report(prereg, summary, analysis, integrity), encoding="utf-8"
    )

    config_digest = _sha256_file(PREREG)
    prompt_digest = _sha256_bytes(b"NO_PROMPT_STAGE1_TOPOLOGY_PROMOTION_R1")
    analysis_digest = _sha256_bytes(b"V3_R1_SINGLE_HOLM_10_PRIMARY_PLUS_HOLM_5_LATENCY")
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
        neuron_count=int(prereg["matched_budgets"]["neuron_count"]),
        edge_count=int(prereg["matched_budgets"]["expected_edge_count"]),
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
        ceiling_resolution_supported=bool(analysis["ceiling_resolution_supported"]),
        replication_supported=bool(analysis["replication_supported"]),
        automatic_evidence_promotion=False,
        scientific_evidence=False,
        human_review_required=True,
        independent_authorship_replication=False,
    )
    recorder.record_runtime(time.perf_counter() - started)
    recorder.mark_completed().save()

    print((OUT / "manifest.json").read_text(encoding="utf-8"))
    if not integrity["pass"]:
        raise SystemExit("STAGE1_TOPOLOGY_PROMOTION_INTEGRITY_FAILURE")


if __name__ == "__main__":
    main()
