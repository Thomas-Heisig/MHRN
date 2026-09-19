"""Promotion-eligible internal replication for the Stage-0 V2 conformance claim.

This run is deliberately DATA-only. It records the current EvidenceEngine
provenance contract but never creates EVID automatically. It is not an
independently authored replication.
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
PREREG = (
    ROOT
    / "research/preregistrations/operational/single_neuron_conformance_v2_promotion_r1.json"
)
EXPERIMENT_ID = "EXP-STAGE0-20260918-MODEL-CONFORMANCE-V2-PROMO-R1"
OUT_DIR = ROOT / "research/experiments" / EXPERIMENT_ID
CANDIDATE = ROOT / "scripts/stage0_conformance_v2.py"


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
    prefixes = ("src/", "scripts/")
    selected: dict[str, str] = {}
    for name in names:
        if not name:
            continue
        if name.startswith(prefixes) or name in {
            "pyproject.toml",
            "research/preregistrations/operational/single_neuron_conformance_v2_promotion_r1.json",
        }:
            selected[name] = _sha256_file(ROOT / name)
    return _canonical_digest(selected)


def _load_candidate() -> Any:
    spec = importlib.util.spec_from_file_location(
        "stage0_conformance_candidate", CANDIDATE
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load stage0_conformance_v2.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _report(payload: dict[str, Any], prereg: dict[str, Any]) -> str:
    a_rows = payload["H-EVAL-006-A"]["runs"]
    b_rows = payload["H-EVAL-006-B"]["runs"]
    max_izh = max(
        max(
            row["max_abs_pre_reset_v_error"],
            row["max_abs_pre_reset_u_error"],
            row["max_abs_post_reset_v_error"],
            row["max_abs_post_reset_u_error"],
        )
        for row in a_rows
    )
    max_lif = max(row["max_abs_v_error"] for row in b_rows)
    return (
        "# Stage-0 promotion replication R1\n\n"
        f"**Experiment:** \`{EXPERIMENT_ID}\`  \n"
        f"**Preregistration:** \`{prereg['preregistration_id']}\`  \n"
        "**Mode:** internal promotion replication; DATA only  \n"
        "**Independent authorship replication:** false\n\n"
        "## Result\n\n"
        f"- H-EVAL-006-A: {payload['H-EVAL-006-A']['supported_by_protocol']}\n"
        f"- H-EVAL-006-B: {payload['H-EVAL-006-B']['supported_by_protocol']}\n"
        f"- H-EVAL-006-C: {payload['H-EVAL-006-C']['supported_by_protocol']} (semantic mapping claim)\n"
        f"- Maximum Izhikevich local-state error: {max_izh:.17g}\n"
        f"- Maximum LIF membrane error: {max_lif:.17g}\n"
        f"- Frozen tolerance: {prereg['source_protocol_invariants']['absolute_tolerance']}\n\n"
        "## Claim boundary\n\n"
        "A positive result can make the scoped claim eligible for separate EvidenceEngine review/promotion. "
        "It does not itself create EVID, does not overwrite the V1 long-horizon negative, and does not count "
        "as independent replication, biological equivalence or evidence for untested regimes.\n"
    )


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    if prereg["status"] != "FROZEN_BEFORE_PROMOTION_REPLICATION":
        raise RuntimeError("promotion replication is not frozen")
    if prereg["evidence_engine_contract"]["automatic_evidence_promotion"]:
        raise RuntimeError("automatic evidence promotion must remain disabled")
    if prereg["independence_boundary"]["independent_authorship_replication"]:
        raise RuntimeError("internal promotion replication must not claim independence")
    if OUT_DIR.exists():
        raise FileExistsError(f"Refusing to overwrite existing experiment: {OUT_DIR}")

    recorder = ExperimentRecorder(EXPERIMENT_ID, output_dir=OUT_DIR, fail_fast=True)
    if recorder.manifest["git"].get("dirty") is not False:
        raise RuntimeError(
            "promotion replication requires a clean git tree before execution"
        )

    started = time.perf_counter()
    module = _load_candidate()
    seeds = tuple(int(seed) for seed in prereg["replication_validation"]["seeds"])
    expected_mapping = {1: 2, 2: 3, 3: 4}

    izh_rows = [module._izh_local(seed) for seed in seeds]
    izh_pass = all(row["conformance_within_1e_8"] for row in izh_rows)

    lif_default_rows: list[dict[str, Any]] = []
    lif_refractory_rows: list[dict[str, Any]] = []
    for seed in seeds:
        for row in module._lif_mapping(seed):
            native_ticks = int(row["native_refractory_ticks"])
            brian_ms = int(row["brian2_refractory_ms"])
            if native_ticks == 0 and brian_ms == 0:
                lif_default_rows.append(row)
            if (
                native_ticks in expected_mapping
                and brian_ms == expected_mapping[native_ticks]
            ):
                lif_refractory_rows.append(row)

    lif_default_pass = len(lif_default_rows) == len(seeds) and all(
        row["spike_events_equal"] and row["max_abs_v_error"] <= 1e-8
        for row in lif_default_rows
    )
    expected_secondary_count = len(seeds) * len(expected_mapping)
    lif_refractory_pass = len(lif_refractory_rows) == expected_secondary_count and all(
        row["spike_events_equal"] and row["max_abs_v_error"] <= 1e-8
        for row in lif_refractory_rows
    )

    payload: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "preregistration_id": prereg["preregistration_id"],
        "parent_preregistration_id": prereg["parent_preregistration_id"],
        "protocol": prereg["protocol"],
        "mode": "REPLICATION",
        "replication_class": "INTERNAL_PROMOTION_REPLICATION",
        "seeds": list(seeds),
        "H-EVAL-006-A": {"supported_by_protocol": izh_pass, "runs": izh_rows},
        "H-EVAL-006-B": {
            "supported_by_protocol": lif_default_pass,
            "runs": lif_default_rows,
        },
        "H-EVAL-006-C": {
            "supported_by_protocol": lif_refractory_pass,
            "claim_type": "semantic_mapping",
            "mapping": {str(k): v for k, v in expected_mapping.items()},
            "runs": lif_refractory_rows,
        },
        "all_declared_hypotheses_pass": izh_pass
        and lif_default_pass
        and lif_refractory_pass,
        "automatic_evid_promotion": False,
        "human_review_required": True,
        "independent_authorship_replication": False,
        "source_data_mutated": False,
    }

    data_dir = OUT_DIR / "DATA"
    data_dir.mkdir(parents=True, exist_ok=False)
    data_path = data_dir / "confirmatory_result.json"
    raw = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    data_path.write_bytes(raw)
    report_path = OUT_DIR / "report.md"
    report_path.write_text(_report(payload, prereg), encoding="utf-8")

    config_digest = _sha256_file(PREREG)
    prompt_digest = _sha256_bytes(b"NO_PROMPT_STAGE0_PROMOTION_R1")
    analysis_digest = _sha256_bytes(b"FROZEN_STAGE0_V2_SUCCESS_RULE")
    code_digest = _tracked_source_digest()
    data_digest = _sha256_bytes(raw)

    recorder.record_config(
        str(PREREG.relative_to(ROOT)).replace("\\", "/"), config_digest
    )
    recorder.record_research_links(
        research_questions=[prereg["research_question_id"]],
        hypotheses=list(prereg["hypothesis_ids"]),
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
    recorder.record_simulation_params(seeds=list(seeds), dt_ms=1.0)
    recorder.record_artifact("confirmatory_data", "DATA/confirmatory_result.json")
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
        protocol=prereg["protocol"],
        replication_class="INTERNAL_PROMOTION_REPLICATION",
        result_status=(
            "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
            if payload["all_declared_hypotheses_pass"]
            else "NOT_SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
        ),
        all_declared_hypotheses_pass=payload["all_declared_hypotheses_pass"],
        automatic_evidence_promotion=False,
        scientific_evidence=False,
        human_review_required=True,
        independent_authorship_replication=False,
    )
    recorder.record_runtime(time.perf_counter() - started)
    recorder.mark_completed().save()

    print("PROMOTION_RESULT_JSON")
    print(data_path.read_text(encoding="utf-8"))
    print("PROMOTION_MANIFEST_JSON")
    print((OUT_DIR / "manifest.json").read_text(encoding="utf-8"))
    print("PROMOTION_REPORT")
    print(report_path.read_text(encoding="utf-8"))

    if not payload["all_declared_hypotheses_pass"]:
        raise SystemExit("STAGE0_PROMOTION_REPLICATION_FAILED")


if __name__ == "__main__":
    main()
