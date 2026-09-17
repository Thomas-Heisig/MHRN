from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V17 = ROOT / "research/publications/2026-09-15_recursive-epistemics_v1.7"
V18 = ROOT / "research/publications/2026-09-17_recursive-epistemics_v1.8"


def _json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_v18_is_current_wip_and_v17_is_predecessor() -> None:
    catalog = _json("research/publications/catalog.json")
    assert catalog["current_publication_id"] == (
        "PUB-RECURSIVE-EPISTEMICS-20260917-V1.8"
    )
    assert catalog["current_entrypoint"].endswith("v1.8/MANUSCRIPT.md")
    current = next(item for item in catalog["publications"] if item.get("current"))
    assert current["version"] == "1.8"
    assert current["edition_status"] == "current_wip"
    assert current["reader"].endswith("v1.8/MANUSCRIPT.md")
    assert current["predecessor"] == "PUB-RECURSIVE-EPISTEMICS-20260915-V1.7"
    assert current["inherits_empirical_edition"] == (
        "PUB-RECURSIVE-EPISTEMICS-20260913-V1.5"
    )
    assert current["automatic_evidence_promotion"] is False
    predecessor = next(
        item for item in catalog["publications"] if item["id"] == current["predecessor"]
    )
    assert predecessor["current"] is False


def test_v18_contains_modular_2_0_structure_and_registers() -> None:
    for name in (
        "README.md",
        "MANUSCRIPT.md",
        "REFERENCES.md",
        "RESEARCH_REGISTER.md",
        "SOURCE_INDEX.md",
        "PRIOR_WORK_MAP.md",
        "LEGACY_V17.md",
        "EXTENDING.md",
        "manifest.json",
    ):
        assert (V18 / name).is_file(), name
    edition = _json(
        "research/publications/2026-09-17_recursive-epistemics_v1.8/edition.json"
    )
    assert [part["id"] for part in edition["parts"]] == [
        "I",
        "II",
        "III",
        "IV",
        "V",
        "VI",
        "VII",
        "VIII",
        "IX",
        "X",
        "XI",
    ]
    manifest = _json(
        "research/publications/2026-09-17_recursive-epistemics_v1.8/manifest.json"
    )
    assert manifest["historical_data_modified"] is False
    assert manifest["accepted_evidence"] is False
    assert manifest["automatic_evidence_promotion"] is False
    assert manifest["complete_chat_archive_available"] is False


def test_frozen_v15_and_historical_predecessors_remain_reachable() -> None:
    frozen = (ROOT / "research/publications/FROZEN_V1.5.md").read_text(encoding="utf-8")
    current = (ROOT / "research/publications/CURRENT.md").read_text(encoding="utf-8")
    assert "2026-09-13_recursive-epistemics_v1.5/MANUSCRIPT.md" in frozen
    assert "2026-09-17_recursive-epistemics_v1.8/MANUSCRIPT.md" in current
    assert "2026-09-15_recursive-epistemics_v1.7" in current
    assert (V17 / "MANUSCRIPT.md").is_file()
    assert (
        ROOT
        / "research/publications/2026-09-15_recursive-epistemics_v1.6/MANUSCRIPT.md"
    ).is_file()


def test_v17_author_position_remains_historical_source() -> None:
    text = (V17 / "AUTHOR_POSITION.md").read_text(encoding="utf-8").lower()
    assert "epistemisch" in text
    assert "institutionell" in text
    assert "freier wissenstransfer" in text
    assert "provenienz" in text
    assert "keinen durchbruch" in text
    assert "neuheit" in text and "offen" in text


def test_document_governance_declares_every_docs_and_research_file() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/audit_document_governance.py", "--strict-review"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "docs:" in result.stdout
    assert "research:" in result.stdout
    assert "Document governance audit: PASS" in result.stdout


def test_project_identity_points_to_v18_and_governance() -> None:
    identity = _json("project_identity.json")
    publication = identity["publication"]
    assert publication["edition"] == "1.8"
    assert publication["edition_status"] == "current_wip"
    assert publication["viewer_entrypoint"].endswith("v1.8/MANUSCRIPT.md")
    assert publication["predecessor"].endswith("v1.7")
    assert publication["empirical_baseline"].endswith("v1.5")
    assert identity["document_governance"]["audit"] == (
        "scripts/audit_document_governance.py"
    )
