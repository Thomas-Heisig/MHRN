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


def _contract() -> dict[str, object]:
    return json.loads(
        (
            ROOT / "src/dashboard/static/development-frontier-placeholders.json"
        ).read_text(encoding="utf-8")
    )


def test_frontier_contract_is_research_only_and_references_real_files() -> None:
    contract = _contract()
    assert contract["status"] == "PLANNED_RESEARCH_ONLY"
    stages = contract["stages"]
    assert isinstance(stages, dict)
    assert set(stages) == {"8", "9", "10"}
    for stage in stages.values():
        assert isinstance(stage, dict)
        assert (ROOT / stage["research_document"]).is_file()
        assert (ROOT / stage["experiment_backlog"]).is_file()


def test_frontier_observer_is_real_read_only_module_without_maturity_promotion() -> (
    None
):
    contract = _contract()
    stages = contract["stages"]
    assert isinstance(stages, dict)
    stage10 = stages["10"]
    assert isinstance(stage10, dict)
    observer_module = stage10["observer_module"]
    assert isinstance(observer_module, str)
    assert observer_module == "src/research/self_monitor.py"
    assert (ROOT / observer_module).is_file()
    methods = stage10["method_placeholders"]
    assert isinstance(methods, list)
    assert any("SelfMonitor" in str(item) for item in methods)
    assert "read-only" in str(stage10["claim_boundary"])


def test_future_mechanisms_remain_explicit_placeholders() -> None:
    contract = _contract()
    stages = contract["stages"]
    assert isinstance(stages, dict)
    stage8 = stages["8"]
    stage9 = stages["9"]
    assert isinstance(stage8, dict)
    assert isinstance(stage9, dict)
    assert "SynapticConsolidationContract" in stage8["solution_placeholders"]
    assert "AttentionGainContract" in stage9["solution_placeholders"]


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
