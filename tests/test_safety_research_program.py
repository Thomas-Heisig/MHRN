from pathlib import Path

from src.research.catalog_status import question_facets
from src.research.registry import ResearchRegistry

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
SAFETY_QUESTIONS = tuple(f"RQ-SAFE-{index:03d}" for index in range(1, 10))
SAFETY_HYPOTHESES = tuple(f"H-SAFE-{index:03d}-A" for index in range(1, 10))


def test_safety_research_program_is_registered_but_not_operational() -> None:
    registry = ResearchRegistry(RESEARCH / "registry").load_all()

    assert all(question_id in registry.questions for question_id in SAFETY_QUESTIONS)
    assert all(
        hypothesis_id in registry.hypotheses for hypothesis_id in SAFETY_HYPOTHESES
    )

    rows = {row["id"]: row for row in question_facets(RESEARCH, registry)}
    for question_id in SAFETY_QUESTIONS:
        row = rows[question_id]
        assert row["operational"] is False
        assert row["workflow_selectable"] is False
        assert row["execution_status"] == "BLOCKED_ADAPTER_AND_REVIEW_REQUIRED"
        assert row["evidence_status"] == "none"
        assert row["progress_is_not_evidence"] is True


def test_safety_hypotheses_start_untested_without_evidence() -> None:
    registry = ResearchRegistry(RESEARCH / "registry").load_all()

    for hypothesis_id in SAFETY_HYPOTHESES:
        hypothesis = registry.hypotheses[hypothesis_id]
        assert hypothesis.status == "untested"
        assert hypothesis.evidence == []
        assert hypothesis.research_question in SAFETY_QUESTIONS
