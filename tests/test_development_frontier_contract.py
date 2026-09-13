from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from src.dashboard.development_timeline import build_development_timeline
from src.dashboard.verification import BaselineEvaluation

ROOT = Path(__file__).resolve().parents[1]


def _baseline() -> BaselineEvaluation:
    return BaselineEvaluation(
        available=True,
        stale=False,
        passed=1,
        failed=0,
        skipped=0,
        collection_errors=0,
        tested_commit=None,
        current_commit=None,
        tested_tree_digest=None,
        current_tree_digest=None,
    )


def test_frontier_contract_is_research_only_and_references_real_files() -> None:
    contract = json.loads(
        (
            ROOT / "src/dashboard/static/development-frontier-placeholders.json"
        ).read_text(encoding="utf-8")
    )
    assert contract["status"] == "PLANNED_RESEARCH_ONLY"
    assert set(contract["stages"]) == {"8", "9", "10"}
    for stage in contract["stages"].values():
        assert (ROOT / stage["research_document"]).is_file()
        assert (ROOT / stage["experiment_backlog"]).is_file()


def test_frontier_foundations_do_not_raise_timeline_maturity() -> None:
    with patch(
        "src.dashboard.development_timeline.evaluate_test_baseline",
        return_value=_baseline(),
    ):
        timeline = build_development_timeline(ROOT)
    for number in (8, 9, 10):
        stage = next(item for item in timeline["stages"] if item["stage"] == number)
        assert stage["implementation_score"] == 0.0
        assert stage["status"] == "planned"
        assert all(item["status"] == "planned" for item in stage["criteria"])
