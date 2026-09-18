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


def test_evidence_matrix_lists_manifest_linked_data_without_evid_promotion(
    tmp_path: Path,
) -> None:
    registry_dir = tmp_path / "registry"
    registry_dir.mkdir()
    (registry_dir / "questions.yaml").write_text(
        "- id: RQ-DATA-001\n"
        "  domain: test\n"
        "  question: Does source-bound DATA stay separate from EVID?\n"
        "  relevance: integrity\n"
        "  status: open\n"
        "  hypotheses: [H-DATA-001-A]\n"
        "  answer:\n"
        "    current: A DATA result is pending human review.\n"
        "    confidence: data_supported_review_pending\n",
        encoding="utf-8",
    )
    (registry_dir / "hypotheses.yaml").write_text(
        "- id: H-DATA-001-A\n"
        "  research_question: RQ-DATA-001\n"
        "  hypothesis: Topology changes a measured endpoint.\n"
        "  status: untested\n"
        "  evidence: []\n",
        encoding="utf-8",
    )
    (registry_dir / "claims.yaml").write_text("[]\n", encoding="utf-8")
    (registry_dir / "sources.yaml").write_text("[]\n", encoding="utf-8")

    experiment = tmp_path / "experiments" / "EXP-DATA-001"
    experiment.mkdir(parents=True)
    (experiment / "manifest.json").write_text(
        '{"experiment_id":"EXP-DATA-001","research_question":"RQ-DATA-001",'
        '"hypothesis":"H-DATA-001-A","scientific_evidence":false}\n',
        encoding="utf-8",
    )

    matrix = ReportBuilder(
        ResearchRegistry(registry_dir).load_all()
    ).build_evidence_matrix()

    row = next(line for line in matrix.splitlines() if line.startswith("| \`RQ-DATA-001\`"))
    assert "\`EXP-DATA-001\`" in row
    cells = [cell.strip() for cell in row.strip("|").split("|")]
    assert cells[6] == "\`EXP-DATA-001\`"
    assert cells[7] == "—"
    assert cells[8] == "data_supported_review_pending"
