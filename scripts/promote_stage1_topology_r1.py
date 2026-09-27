#!/usr/bin/env python3
"""Explicit EvidenceEngine promotion for Stage-1 topology promotion R1.

This script is intentionally one-shot and idempotent. It never runs during the
experiment itself and never performs automatic EVID promotion.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.research.evidence_engine import EvidenceEngine
from src.research.registry import ResearchRegistry

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_ID = "EXP-S1-TOPO-PROMO-R1-20260927"
CLAIM_ID = "CLAIM-S1-TOPO-001"
HYPOTHESIS_ID = "H-SNN-003-B"
EXPERIMENT_DIR = ROOT / "research" / "experiments" / EXPERIMENT_ID
EVIDENCE_DIR = ROOT / "research" / "registry" / "evidence"
STATUS_PATH = EXPERIMENT_DIR / "EVIDENCE_PROMOTION_STATUS.json"


def _existing_evidence() -> str | None:
    for path in sorted(EVIDENCE_DIR.glob("EVID-*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if (
            payload.get("experiment_id") == EXPERIMENT_ID
            and payload.get("claim_id") == CLAIM_ID
            and payload.get("hypothesis_id") == HYPOTHESIS_ID
        ):
            return str(payload.get("evidence_id") or path.stem)
    return None


def main() -> int:
    if not (EXPERIMENT_DIR / "human_review.json").is_file():
        raise RuntimeError("canonical human_review.json is required before promotion")

    existing = _existing_evidence()
    if existing:
        print(json.dumps({"status": "ALREADY_PROMOTED", "evidence_id": existing}))
        return 0

    registry = ResearchRegistry().load_all()
    engine = EvidenceEngine(registry)

    evidence_id = engine.promote_validated_experiment(
        experiment_id=EXPERIMENT_ID,
        claim_id=CLAIM_ID,
        hypothesis_id=HYPOTHESIS_ID,
        result_summary=(
            "The prospective Stage-1 topology promotion replication reproduced the "
            "bounded topology-sensitive propagation result on predeclared fresh seeds "
            "6301-6320 within the registered 64-neuron/246-edge Small-SNN operating "
            "envelope. Design integrity passed, the preregistered ceiling-resolution "
            "criterion passed, and all five first-output-latency replication contrasts "
            "reproduced the registered direction. The human review explicitly preserves "
            "the null findings and does not support 5D superiority."
        ),
        evidence_mode="stochastic_experiment",
        effect_size={
            "activation_auc_0_32_median_delta": {
                "1d_to_2d": 4.3984375,
                "2d_to_3d": 1.3828125,
                "3d_to_5d": -3.0703125,
                "5d_to_5d_shuffled": -3.2890625,
                "5d_to_random_graph": -2.4609375,
            },
            "half_activation_latency_censored_median_delta": {
                "1d_to_2d": -4.0,
                "2d_to_3d": -2.0,
                "3d_to_5d": 0.0,
                "5d_to_5d_shuffled": 0.0,
                "5d_to_random_graph": 0.0,
            },
            "first_output_latency_censored_median_delta": {
                "1d_to_2d": -10.0,
                "2d_to_3d": -3.0,
                "3d_to_5d": -1.0,
                "5d_to_5d_shuffled": -3.0,
                "5d_to_random_graph": -2.5,
            },
        },
        verification={
            "preregistration_id": "PREREG-S1-TOPO-PROMO-R1",
            "replication_class": "INTERNAL_PROMOTION_REPLICATION",
            "design_integrity_passed": True,
            "ceiling_resolution_supported": True,
            "replication_supported": True,
            "evaluation_runs": 120,
            "evaluation_seeds": list(range(6301, 6321)),
            "historical_seed_disjoint": True,
            "single_holm_family_primary_tests": True,
            "null_findings_preserved": [
                "half_activation_latency_censored 3d->5d not significant",
                "half_activation_latency_censored 5d->5d_shuffled not significant",
                "half_activation_latency_censored 5d->random_graph not significant under registered CI+Holm rule",
            ],
            "independent_authorship_replication": False,
            "five_d_superiority_supported": False,
        },
        limitations=(
            "Internal promotion replication only. Scope is limited to the registered "
            "64-neuron, 246-edge, weight-55, 128-tick Small-SNN operating envelope. "
            "No 5D superiority, no scaling claim, no cognition/learning/memory claim, "
            "no biological equivalence, and no independent external replication. "
            "The non-significant half-activation-latency contrasts are preserved."
        ),
    )

    status = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "human_review_status": "COMPLETED_SUPPORTS_SCOPED_CLAIM",
        "evidence_promotion_status": "COMPLETED",
        "evidence_id": evidence_id,
        "claim_id": CLAIM_ID,
        "hypothesis_id": HYPOTHESIS_ID,
        "scientific_evidence": True,
        "automatic_evidence_promotion": False,
        "independent_replication_complete": False,
        "independent_authorship_replication": False,
        "maturity_effect": {
            "reviewed_evidence": "partial -> met",
            "stage1_scientific_maturity": "75% -> 85%",
            "remaining_gap_to_92_5": "7.5% independent reference/cross-implementation replication",
            "remaining_gap_to_100": "15% full independent replication criterion",
        },
        "boundaries": [
            "No 5D superiority",
            "No scaling beyond the registered 64-neuron operating envelope",
            "No cognition, learning or memory claim",
            "No biological equivalence",
            "No independent external replication claim",
            "Null findings remain part of the evidence record",
        ],
    }
    STATUS_PATH.write_text(
        json.dumps(status, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PROMOTED", "evidence_id": evidence_id}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
