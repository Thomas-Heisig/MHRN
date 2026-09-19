from __future__ import annotations

import json
from pathlib import Path

from src.dashboard.review_inbox import build_review_inbox


def _write_report(
    root: Path, experiment: str, report: str, *, reviewed: bool = False
) -> None:
    directory = root / "experiments" / experiment / "reports"
    directory.mkdir(parents=True, exist_ok=True)
    payload = {
        "report_id": report,
        "research_question_id": "RQ-TEST-001",
        "generated_at": "2026-09-08T00:00:00+00:00",
        "human_review_required": True,
        "status": "review_pending",
        "scientific_evidence": False,
        "content": {"executive_summary": "Review me"},
    }
    (directory / f"{report}.json").write_text(json.dumps(payload), encoding="utf-8")
    if reviewed:
        (directory / f"{report}.review.json").write_text(
            json.dumps(
                {"review_status": "accepted_as_interpretation", "reviewer": "Human"}
            ),
            encoding="utf-8",
        )


def test_review_inbox_lists_only_open_airr(tmp_path: Path) -> None:
    _write_report(tmp_path, "EXP-A", "AIRR-2026-0001")
    _write_report(tmp_path, "EXP-B", "AIRR-2026-0002", reviewed=True)
    inbox = build_review_inbox(tmp_path)
    assert inbox["open"] == 1
    assert inbox["completed"] == 1
    item = inbox["items"][0]
    assert item["experiment_id"] == "EXP-A"
    assert item["review_endpoint"].endswith("/EXP-A/AIRR-2026-0001/review")


def test_review_inbox_never_promotes_evidence(tmp_path: Path) -> None:
    _write_report(tmp_path, "EXP-A", "AIRR-2026-0001")
    inbox = build_review_inbox(tmp_path)
    assert "scientific_evidence" not in inbox["items"][0]


def test_review_inbox_does_not_close_on_ai_review(tmp_path: Path) -> None:
    directory = tmp_path / "experiments" / "EXP-AI-REVIEW"
    directory.mkdir(parents=True)
    (directory / "review_request.json").write_text(
        json.dumps(
            {
                "human_review_status": "PENDING",
                "evidence_readiness": "BLOCKED_HUMAN_REVIEW",
            }
        ),
        encoding="utf-8",
    )
    (directory / "review_request.json.review.json").write_text(
        json.dumps(
            {
                "review_status": "accepted_as_interpretation",
                "reviewer": "KI",
            }
        ),
        encoding="utf-8",
    )

    inbox = build_review_inbox(tmp_path)

    assert inbox["open"] == 1
    assert inbox["completed"] == 0
    assert inbox["items"][0]["experiment_id"] == "EXP-AI-REVIEW"


def test_review_inbox_lists_results_artifact_requiring_human_review(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "experiments" / "EXP-S6-SEM-CL-003" / "results"
    directory.mkdir(parents=True)
    (directory / "results.json").write_text(
        json.dumps(
            {
                "experiment_id": "EXP-S6-SEM-CL-003",
                "human_review_required": True,
                "scientific_evidence": False,
                "result_classification": "H1_negative_H2_negative",
            }
        ),
        encoding="utf-8",
    )

    inbox = build_review_inbox(tmp_path)

    assert inbox["open"] == 1
    item = inbox["items"][0]
    assert item["experiment_id"] == "EXP-S6-SEM-CL-003"
    assert item["artifact_path"].endswith("results/results.json")
    assert item["result_status"] == "H1_negative_H2_negative"


def test_review_inbox_skips_results_with_human_reviewed_evidence(
    tmp_path: Path,
) -> None:
    experiment = tmp_path / "experiments" / "EXP-S6-SEM-CL-002"
    results = experiment / "results"
    results.mkdir(parents=True)
    (results / "results.json").write_text(
        json.dumps(
            {
                "human_review_required": True,
                "scientific_evidence": False,
                "evidence_status": "human_reviewed_project_evidence",
            }
        ),
        encoding="utf-8",
    )
    (experiment / "EVID.json").write_text("{}", encoding="utf-8")

    inbox = build_review_inbox(tmp_path)

    assert inbox["open"] == 0


def test_review_inbox_does_not_treat_ai_artifact_review_as_human(
    tmp_path: Path,
) -> None:
    experiment = tmp_path / "experiments" / "EXP-GEN-0041" / "analysis"
    experiment.mkdir(parents=True)
    artifact = experiment / "PREREGISTERED-CRITERIA-EVALUATION.json"
    artifact.write_text(
        json.dumps(
            {
                "human_review_status": "PENDING",
                "scientific_evidence_promoted": False,
            }
        ),
        encoding="utf-8",
    )
    (experiment / "PREREGISTERED-CRITERIA-EVALUATION.json.review.json").write_text(
        json.dumps(
            {
                "review_status": "accepted_as_interpretation",
                "reviewer": "KI",
            }
        ),
        encoding="utf-8",
    )

    inbox = build_review_inbox(tmp_path)

    assert inbox["open"] == 1
    assert inbox["completed"] == 0


def test_review_inbox_lists_source_bound_stage1_review_request(tmp_path: Path) -> None:
    directory = tmp_path / "experiments" / "EXP-S1-TOPO-V2-20260918"
    directory.mkdir(parents=True)
    (directory / "review_request.json").write_text(
        json.dumps(
            {
                "human_review_status": "PENDING",
                "evidence_readiness": "BLOCKED_HUMAN_REVIEW",
                "research_question": "RQ-SNN-003",
                "hypothesis": "H-SNN-003-B",
                "result_status": "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL",
                "interpretation_boundary": "Stage-1 topology support only; no 5D superiority claim.",
            }
        ),
        encoding="utf-8",
    )

    inbox = build_review_inbox(tmp_path)

    assert inbox["open"] == 1
    item = inbox["items"][0]
    assert item["experiment_id"] == "EXP-S1-TOPO-V2-20260918"
    assert item["title"] == "EXP-S1-TOPO-V2-20260918 · Human Review"
    assert item["research_question_id"] == "RQ-SNN-003"
    assert item["hypothesis_id"] == "H-SNN-003-B"
    assert item["result_status"] == "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
    assert "no 5D superiority" in item["summary"]


def test_review_inbox_human_sidecar_closes_ai_reviewed_artifact(tmp_path: Path) -> None:
    experiment = tmp_path / "experiments" / "EXP-AI-THEN-HUMAN"
    experiment.mkdir(parents=True)
    artifact = experiment / "review_request.json"
    artifact.write_text(
        json.dumps(
            {
                "human_review_status": "PENDING",
                "evidence_readiness": "BLOCKED_HUMAN_REVIEW",
            }
        ),
        encoding="utf-8",
    )
    (experiment / "review_request.json.review.json").write_text(
        json.dumps(
            {
                "review_status": "accepted_as_interpretation",
                "reviewer": "KI",
            }
        ),
        encoding="utf-8",
    )
    (experiment / "review_request.json.human-review.json").write_text(
        json.dumps(
            {
                "review_status": "accepted_as_interpretation",
                "reviewer": "Thomas Heisig",
            }
        ),
        encoding="utf-8",
    )

    inbox = build_review_inbox(tmp_path)

    assert inbox["open"] == 0
    assert inbox["completed"] == 1


def test_review_inbox_prefers_canonical_review_request_over_manifest(
    tmp_path: Path,
) -> None:
    experiment = tmp_path / "experiments" / "EXP-CANONICAL"
    experiment.mkdir(parents=True)
    (experiment / "manifest.json").write_text(
        json.dumps(
            {
                "human_review_status": "PENDING",
                "scientific_evidence": False,
                "result_status": "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL",
            }
        ),
        encoding="utf-8",
    )
    (experiment / "review_request.json").write_text(
        json.dumps(
            {
                "human_review_status": "PENDING",
                "research_question": "RQ-TEST-002",
                "hypothesis": "H-TEST-002-A",
                "result_status": "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL",
            }
        ),
        encoding="utf-8",
    )

    inbox = build_review_inbox(tmp_path)

    assert inbox["open"] == 1
    item = inbox["items"][0]
    assert item["experiment_id"] == "EXP-CANONICAL"
    assert item["artifact_path"] == "experiments/EXP-CANONICAL/review_request.json"
    assert item["title"] == "EXP-CANONICAL · Human Review"
