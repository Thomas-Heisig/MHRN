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
