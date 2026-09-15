from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V17 = ROOT / "research/publications/2026-09-15_recursive-epistemics_v1.7"


def _json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_v17_is_current_wip_and_viewer_opens_manuscript() -> None:
    catalog = _json("research/publications/catalog.json")
    assert catalog["current_publication_id"] == "PUB-RECURSIVE-EPISTEMICS-20260915-V1.7"
    assert catalog["current_entrypoint"].endswith("v1.7/MANUSCRIPT.md")
    current = next(item for item in catalog["publications"] if item.get("current"))
    assert current["version"] == "1.7"
    assert current["edition_status"] == "current_wip"
    assert current["reader"].endswith("v1.7/MANUSCRIPT.md")
    assert current["predecessor"] == "PUB-RECURSIVE-EPISTEMICS-20260915-V1.6"
    assert current["inherits_empirical_edition"] == "PUB-RECURSIVE-EPISTEMICS-20260913-V1.5"
    assert current["automatic_evidence_promotion"] is False


def test_v17_contains_complete_current_working_set() -> None:
    expected = {
        "README.md",
        "MANUSCRIPT.md",
        "FORSCHUNGSBERICHT.md",
        "AUTHOR_POSITION.md",
        "CONTRIBUTION_MAP.md",
        "SCIENTIFIC_STAGE_MATRIX.md",
        "INTEGRITY_AND_ATTRIBUTION.md",
        "REFERENCES.md",
        "WORK_IN_PROGRESS.md",
        "manifest.json",
    }
    assert expected <= {path.name for path in V17.iterdir() if path.is_file()}
    manuscript = (V17 / "MANUSCRIPT.md").read_text(encoding="utf-8")
    for token in (
        "Stage 6",
        "Logical Identity",
        "Proposal → Approval → Mutation → Journal → Undo",
        "Content Gateway",
        "Compute Backend",
        "Frozen 1.5",
        "Neuheits",
        "Quellenquarantäne",
    ):
        assert token in manuscript


def test_frozen_v15_and_v16_predecessor_remain_reachable() -> None:
    frozen = (ROOT / "research/publications/FROZEN_V1.5.md").read_text(encoding="utf-8")
    current = (ROOT / "research/publications/CURRENT.md").read_text(encoding="utf-8")
    assert "2026-09-13_recursive-epistemics_v1.5/MANUSCRIPT.md" in frozen
    assert "2026-09-15_recursive-epistemics_v1.7/MANUSCRIPT.md" in current
    assert "2026-09-15_recursive-epistemics_v1.6" in current


def test_author_position_distinguishes_cumulative_science_from_plagiarism() -> None:
    text = (V17 / "AUTHOR_POSITION.md").read_text(encoding="utf-8").lower()
    assert "epistemisch" in text
    assert "institutionell" in text
    assert "freier wissenstransfer" in text
    assert "provenienz" in text
    assert "keinen durchbruch" in text
    assert "neuheit" in text and "offen" in text


def test_document_governance_declares_every_docs_and_research_file() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/audit_document_governance.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "docs:" in result.stdout
    assert "research:" in result.stdout
    assert "Document governance audit: PASS" in result.stdout


def test_project_identity_points_to_v17_and_governance() -> None:
    identity = _json("project_identity.json")
    publication = identity["publication"]
    assert publication["edition"] == "1.7"
    assert publication["edition_status"] == "current_wip"
    assert publication["viewer_entrypoint"].endswith("v1.7/MANUSCRIPT.md")
    assert publication["predecessor"].endswith("v1.6")
    assert publication["empirical_baseline"].endswith("v1.5")
    assert identity["document_governance"]["audit"] == "scripts/audit_document_governance.py"
