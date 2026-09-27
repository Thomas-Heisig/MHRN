#!/usr/bin/env python3
"""Explicit EvidenceEngine promotion for Stage-1 Temporal-Order promotion R1."""

from __future__ import annotations

import json
from pathlib import Path

from src.research.evidence_engine import EvidenceEngine
from src.research.registry import ResearchRegistry

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_ID = "EXP-S1-TEMP-PROMO-R1-20260927"
CLAIM_ID = "CLAIM-S1-TEMP-001"
HYPOTHESIS_ID = "H-TEMP-002-A"
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
    review_path = EXPERIMENT_DIR / "human_review.json"
    if not review_path.is_file():
        raise RuntimeError("canonical human_review.json is required before promotion")

    review = json.loads(review_path.read_text(encoding="utf-8"))
    if review.get("decision") != "supports":
        raise RuntimeError(
            "Temporal-Order promotion requires a canonical supports review"
        )
    if review.get("automatic_evidence_promotion") is not False:
        raise RuntimeError("automatic evidence promotion must remain disabled")

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
            "The prospective Stage-1 Temporal-Order promotion replication supported "
            "the bounded six-neuron two-channel temporal-order claim on 20 fresh "
            "predeclared paired seeds. Intact forward/reverse order accuracy had median "
            "1.0, the matched identity-destroyed arm had median 0.0, the paired delta "
            "median was 1.0 with bootstrap CI [1.0, 1.0], and the exact paired sign-test "
            "p-value was 1.9073486328125e-6. The preregistered simultaneous condition "
            "was correctly decoded as simultaneous and is a non-inferential task-adequacy "
            "control. The human review explicitly records perfect-score saturation as a "
            "methodological limitation and does not extend the result to memory, cognition "
            "or general temporal reasoning."
        ),
        evidence_mode="stochastic_experiment",
        effect_size={
            "intact_order_accuracy_median": 1.0,
            "identity_destroyed_order_accuracy_median": 0.0,
            "paired_accuracy_delta_median": 1.0,
            "paired_accuracy_delta_bootstrap_ci95": [1.0, 1.0],
            "paired_sign_test_p": 1.9073486328125e-6,
            "intact_simultaneous_success_fraction": 1.0,
        },
        verification={
            "preregistration_id": "PREREG-S1-TEMP-PROMO-R1",
            "replication_class": "INTERNAL_PROMOTION_REPLICATION",
            "design_integrity_passed": True,
            "evaluation_runs": 120,
            "evaluation_seed_count": 20,
            "historical_seed_disjoint": True,
            "identity_destroyed_control_present": True,
            "simultaneous_control_role": "non-inferential task-adequacy control",
            "all_preregistered_gates_passed": True,
            "perfect_score_saturation_noted": True,
            "independent_authorship_replication": False,
        },
        limitations=(
            "Internal promotion replication only. Scope is limited to the registered "
            "six-neuron, four-synapse, two-channel acyclic Small-SNN task and the frozen "
            "decoder. Perfect ceiling/floor separation limits mechanistic resolution and "
            "motivates a separate prospective stress test. No learning, memory, order "
            "memory, cognition, general temporal reasoning, biological equivalence, "
            "scaling, 5D superiority or independent external replication is established."
        ),
    )

    status = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "human_review_status": "COMPLETED_SUPPORTS_SCOPED_CLAIM_WITH_LIMITATIONS",
        "evidence_promotion_status": "COMPLETED",
        "evidence_id": evidence_id,
        "claim_id": CLAIM_ID,
        "hypothesis_id": HYPOTHESIS_ID,
        "scientific_evidence": True,
        "automatic_evidence_promotion": False,
        "independent_replication_complete": False,
        "independent_authorship_replication": False,
        "maturity_effect": {
            "reviewed_evidence": "remains met",
            "stage1_scientific_maturity": "remains 85%",
            "reason": (
                "The 20% reviewed-evidence gate was already satisfied by the topology "
                "EVID line. A second internal EVID line strengthens Stage-1 support but "
                "does not fill the independent-replication component."
            ),
            "remaining_gap_to_92_5": (
                "7.5% independently implemented reference/cross-implementation replication"
            ),
            "remaining_gap_to_100": "15% full independent replication criterion",
        },
        "methodological_follow_up": (
            "research/notes/2026-09-27_stage1_temporal_order_decoder_followup.md"
        ),
        "boundaries": [
            "No learning or memory claim",
            "No cognition or general temporal reasoning claim",
            "No scaling beyond the six-neuron task",
            "No biological equivalence",
            "No 5D superiority",
            "No independent external replication",
            "Perfect-score saturation remains an explicit limitation",
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
