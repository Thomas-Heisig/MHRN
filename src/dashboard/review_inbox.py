"""Review inbox aggregation for research artifacts.

The inbox is intentionally read-only. Decisions are still written through the
existing append-only human-review writers in ``research_assistant.airr``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast


_VALID_REVIEW_STATUSES = {"accepted_as_interpretation", "rejected"}
_NON_HUMAN_REVIEWERS = {
    "ai",
    "artificial intelligence",
    "artificial_intelligence",
    "bot",
    "ki",
    "machine",
    "system",
}


def _json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return cast(dict[str, Any], value) if isinstance(value, dict) else None


def _is_human_review(path: Path) -> bool:
    review = _json(path)
    if not review or review.get("review_status") not in _VALID_REVIEW_STATUSES:
        return False
    reviewer = review.get("reviewer")
    if not isinstance(reviewer, str) or not reviewer.strip():
        return False
    reviewer_kind = " ".join(reviewer.casefold().replace("_", " ").split())
    return reviewer_kind not in _NON_HUMAN_REVIEWERS


def build_review_inbox(research_root: Path) -> dict[str, Any]:
    root = research_root.resolve()
    experiments = root / "experiments"
    items: list[dict[str, Any]] = []
    if not experiments.is_dir():
        return {"open": 0, "completed": 0, "items": []}

    completed = 0
    for report_path in sorted(experiments.glob("*/reports/AIRR-*.json")):
        if report_path.name.endswith(".review.json"):
            continue
        report = _json(report_path)
        if not report:
            continue
        experiment_id = report_path.parents[1].name
        report_id = str(report.get("report_id") or report_path.stem)
        review_path = report_path.with_name(f"{report_id}.review.json")
        if review_path.is_file() and _is_human_review(review_path):
            completed += 1
            continue
        if report.get("human_review_required") is not True:
            continue
        if report.get("status") != "review_pending":
            continue
        content_value = report.get("content")
        content = (
            cast(dict[str, Any], content_value)
            if isinstance(content_value, dict)
            else {}
        )
        items.append(
            {
                "kind": "airr",
                "experiment_id": experiment_id,
                "report_id": report_id,
                "artifact_path": str(report_path.relative_to(root)).replace("\\", "/"),
                "research_question_id": report.get("research_question_id"),
                "generated_at": report.get("generated_at"),
                "title": f"{experiment_id} · {report_id}",
                "summary": content.get("executive_summary"),
                "review_endpoint": f"/api/research/ai-reports/{experiment_id}/{report_id}/review",
            }
        )

    for target in sorted(experiments.glob("*/**/*")):
        if (
            not target.is_file()
            or target.name.endswith(".review.json")
            or target.name.endswith(".human-review.json")
        ):
            continue
        if target.suffix.lower() not in {".md", ".json"}:
            continue
        review_paths = (
            target.with_name(f"{target.name}.human-review.json"),
            target.with_name(f"{target.name}.review.json"),
        )
        if any(path.is_file() and _is_human_review(path) for path in review_paths):
            completed += 1
            continue
        payload = _json(target) if target.suffix.lower() == ".json" else None
        already_evidenced = bool(
            isinstance(payload, dict)
            and payload.get("evidence_status") == "human_reviewed_project_evidence"
        ) or (target.name == "results.json" and target.parents[1].joinpath("EVID.json").is_file())
        explicit = bool(
            isinstance(payload, dict)
            and (
                payload.get("human_review") == "PENDING"
                or payload.get("human_review_status") in {"PENDING", "NOT_PERFORMED"}
                or payload.get("evidence_readiness") == "BLOCKED_HUMAN_REVIEW"
                or (
                    target.name == "results.json"
                    and payload.get("human_review_required") is True
                    and payload.get("scientific_evidence") is False
                )
            )
            and not already_evidenced
        )
        if not explicit:
            continue
        relative = str(target.relative_to(root)).replace("\\", "/")
        experiment_id = target.relative_to(experiments).parts[0]
        research_question = (
            str(
                payload.get("research_question_id")
                or payload.get("research_question")
            )
            if isinstance(payload, dict)
            and (payload.get("research_question_id") or payload.get("research_question"))
            else None
        )
        hypothesis = (
            str(payload.get("hypothesis"))
            if isinstance(payload, dict) and payload.get("hypothesis")
            else None
        )
        result_status = (
            str(payload.get("result_status") or payload.get("result_classification"))
            if isinstance(payload, dict)
            and (payload.get("result_status") or payload.get("result_classification"))
            else None
        )
        boundary = (
            str(payload.get("interpretation_boundary"))
            if isinstance(payload, dict) and payload.get("interpretation_boundary")
            else "DATA artifact requires human review; automatic EVID promotion is disabled."
        )
        items.append(
            {
                "kind": "artifact",
                "experiment_id": experiment_id,
                "artifact_path": relative,
                "research_question_id": research_question,
                "hypothesis_id": hypothesis,
                "result_status": result_status,
                "title": (
                    f"{experiment_id} · Human Review"
                    if target.name == "review_request.json"
                    else target.name
                ),
                "summary": boundary,
                "review_endpoint": "/api/research/reviews",
            }
        )

    items.sort(
        key=lambda item: (str(item.get("experiment_id")), str(item.get("title")))
    )
    return {"open": len(items), "completed": completed, "items": items}
