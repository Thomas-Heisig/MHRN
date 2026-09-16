from pathlib import Path

from src.research.registry import ResearchRegistry
from src.research.report_builder import ReportBuilder


def test_current_report_generation_does_not_touch_experiment_reports(
    tmp_path: Path,
) -> None:
    registry_dir = tmp_path / "registry"
    registry_dir.mkdir()
    (registry_dir / "questions.yaml").write_text(
        "- id: RQ-TEST-001\n"
        "  domain: test\n"
        "  question: Does report generation stay current-only?\n"
        "  relevance: lifecycle\n"
        "  status: open\n",
        encoding="utf-8",
    )
    (registry_dir / "hypotheses.yaml").write_text("[]\n", encoding="utf-8")
    (registry_dir / "claims.yaml").write_text("[]\n", encoding="utf-8")
    (registry_dir / "sources.yaml").write_text("[]\n", encoding="utf-8")

    historical_report = tmp_path / "experiments" / "EXP-HIST-001" / "report.md"
    historical_report.parent.mkdir(parents=True)
    historical_report.write_text("historical experiment report\n", encoding="utf-8")

    output_dir = tmp_path / "generated"
    paths = ReportBuilder(ResearchRegistry(registry_dir).load_all()).write_all(
        output_dir
    )

    assert set(paths) == {
        "RESEARCH_CATALOG.md",
        "EVIDENCE_MATRIX.md",
        "OPEN_QUESTIONS.md",
        "CLAIM_REGISTER.md",
        "DISSERTATION_MAP.md",
    }
    assert "RQ-TEST-001" in (output_dir / "RESEARCH_CATALOG.md").read_text(
        encoding="utf-8"
    )
    assert historical_report.read_text(encoding="utf-8") == (
        "historical experiment report\n"
    )


def test_evidence_matrix_keeps_rq_claim_and_experiment_status_separate(
    tmp_path: Path,
) -> None:
    registry_dir = tmp_path / "registry"
    registry_dir.mkdir()
    (registry_dir / "questions.yaml").write_text(
        "- id: RQ-TEST-002\n"
        "  domain: test\n"
        "  question: Is the research question answered independently of claim status?\n"
        "  relevance: integrity\n"
        "  status: answered\n"
        "  hypotheses: [H-TEST-002-A]\n"
        "  answer:\n"
        "    current: The RQ has a bounded answer.\n"
        "    confidence: moderate\n",
        encoding="utf-8",
    )
    (registry_dir / "hypotheses.yaml").write_text(
        "- id: H-TEST-002-A\n"
        "  research_question: RQ-TEST-002\n"
        "  hypothesis: Test hypothesis\n"
        "  status: refuted\n",
        encoding="utf-8",
    )
    (registry_dir / "claims.yaml").write_text(
        "- id: CLAIM-TEST-002\n"
        "  claim: A deliberately refuted claim\n"
        "  research_question: RQ-TEST-002\n"
        "  hypothesis: H-TEST-002-A\n"
        "  status: refuted\n"
        "  confidence: high\n"
        "  experiments: [EXP-TEST-002]\n",
        encoding="utf-8",
    )
    (registry_dir / "sources.yaml").write_text("[]\n", encoding="utf-8")

    matrix = ReportBuilder(
        ResearchRegistry(registry_dir).load_all()
    ).build_evidence_matrix()

    assert "| Forschungsfrage | RQ-Status |" in matrix
    assert "| `RQ-TEST-002` | answered |" in matrix
    assert "`CLAIM-TEST-002`=refuted" in matrix
    assert "`EXP-TEST-002`" in matrix
    assert "### Forschungsfragen (RQ-Status)" in matrix
    assert "| answered | 1 |" in matrix
    assert "| **Gesamt RQs** | **1** |" in matrix
    assert "### Claims (Claim-Status)" in matrix
    assert "| refuted | 1 |" in matrix
    assert "| **Gesamt Claims** | **1** |" in matrix
