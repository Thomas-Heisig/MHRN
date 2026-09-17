from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.research_assistant.airr import AIRRPipeline


def _backend(_prompt: str) -> tuple[dict[str, Any], dict[str, str | float]]:
    return (
        {
            "assessment": "Technische Interpretation.",
            "observations": [],
            "effect_direction": "not_determined",
            "methodological_concerns": [],
            "alternative_explanations": [],
            "recommended_experiments": [],
            "requested_evidence": [],
            "confidence": 0.95,
        },
        {"provider": "test", "model": "fixture", "model_digest": "fixture"},
    )


def _fixture(
    root: Path,
    *,
    conditions: list[str],
    protocol: str,
    question_id: str = "RQ-SNN-002",
    hypothesis_id: str = "H-SNN-002-A",
) -> None:
    experiment = root / "experiments" / "EXP-AIRR-SEM"
    analysis = experiment / "analysis"
    analysis.mkdir(parents=True)
    (root / "registry" / "evidence").mkdir(parents=True)
    (root / "registry" / "questions.yaml").write_text(
        f"- id: {question_id}\n  question: Registered test question?\n",
        encoding="utf-8",
    )
    (root / "registry" / "hypotheses.yaml").write_text(
        f"- id: {hypothesis_id}\n  research_question: {question_id}\n  hypothesis: Registered hypothesis.\n",
        encoding="utf-8",
    )
    (root / "registry" / "claims.yaml").write_text("[]\n", encoding="utf-8")
    (experiment / "workflow.json").write_text(
        json.dumps({"protocol": protocol}), encoding="utf-8"
    )
    (experiment / "manifest.json").write_text(
        json.dumps(
            {
                "experiment_status": "completed",
                "research_questions": [question_id],
                "hypotheses": [hypothesis_id],
                "artifacts": {"workflow": "workflow.json"},
                "git": {"commit": "abc123", "dirty": False},
            }
        ),
        encoding="utf-8",
    )
    runs = [
        {"condition": condition, "seed": 101, "metrics": {}}
        for condition in conditions
    ]
    (analysis / "ai_packet.json").write_text(
        json.dumps({"run_preview": runs}), encoding="utf-8"
    )
    (analysis / "statistics.json").write_text(
        json.dumps(
            {
                "generated_by": "deterministic_statistics_engine",
                "conditions": {condition: {"run_count": 1} for condition in conditions},
            }
        ),
        encoding="utf-8",
    )


def test_airr_forces_reported_confidence_to_zero_on_semantic_mismatch(
    tmp_path: Path,
) -> None:
    _fixture(
        tmp_path,
        conditions=["same_seed_tonic_replica_pair"],
        protocol="tonic_spike_reproducibility_v1",
    )
    report = AIRRPipeline(tmp_path).analyze("EXP-AIRR-SEM", _backend)
    assert report.content["ai_confidence"] == 0.0
    epistemic = report.content["epistemic_status"]
    assert epistemic["semantic_alignment"] == "MISMATCH"
    assert epistemic["confidence_gate"] == "FORCED_ZERO_SEMANTIC_MISMATCH"
    assert report.content["aiar"]["writer"]["output"]["confidence"] == 0.95


def test_airr_preserves_interpretive_confidence_for_direct_match(
    tmp_path: Path,
) -> None:
    _fixture(
        tmp_path,
        conditions=["recurrence_off", "recurrence_on"],
        protocol="science_suite_v1",
    )
    report = AIRRPipeline(tmp_path).analyze("EXP-AIRR-SEM", _backend)
    assert report.content["ai_confidence"] == 0.95
    epistemic = report.content["epistemic_status"]
    assert epistemic["semantic_alignment"] == "DIRECT_MATCH"
    assert epistemic["confidence_gate"] == "PASSED"


def test_airr_blocks_snn003_interpretation_when_v1_design_is_inadequate(
    tmp_path: Path,
) -> None:
    _fixture(
        tmp_path,
        conditions=["1d", "2d", "3d", "5d", "5d_shuffled", "random_graph"],
        protocol="topology_propagation_v1",
        question_id="RQ-SNN-003",
        hypothesis_id="H-SNN-003-B",
    )
    report = AIRRPipeline(tmp_path).analyze("EXP-AIRR-SEM", _backend)
    epistemic = report.content["epistemic_status"]
    assert epistemic["semantic_alignment"] == "DIRECT_MATCH"
    assert epistemic["design_adequacy"] == "INADEQUATE_TO_TEST_HYPOTHESIS"
    assert epistemic["confidence_gate"] == "FORCED_ZERO_DESIGN_INADEQUACY"
    assert report.content["ai_confidence"] == 0.0
    assert "nicht testadäquat" in report.content["executive_summary"]
    assert report.content["aiar"]["writer"]["output"]["confidence"] == 0.95
