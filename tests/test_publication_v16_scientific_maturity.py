from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_v16_is_historical_predecessor_without_rewriting_v15_baseline() -> None:
    catalog = _json("research/publications/catalog.json")
    current = next(item for item in catalog["publications"] if item.get("current"))
    assert current["version"] == "1.7"
    v16 = next(
        item
        for item in catalog["publications"]
        if item["id"] == "PUB-RECURSIVE-EPISTEMICS-20260915-V1.6"
    )
    assert v16["current"] is False
    assert v16["edition_status"] == "historical_integrative_predecessor"
    assert v16["automatic_evidence_promotion"] is False
    assert v16["inherits_empirical_edition"] == (
        "PUB-RECURSIVE-EPISTEMICS-20260913-V1.5"
    )

    baseline = next(
        item
        for item in catalog["publications"]
        if item["id"] == "PUB-RECURSIVE-EPISTEMICS-20260913-V1.5"
    )
    assert baseline["current"] is False
    assert baseline["edition_status"] == "frozen_empirical_baseline"

    manifest = _json(
        "research/publications/" "2026-09-15_recursive-epistemics_v1.6/manifest.json"
    )
    assert manifest["historical_data_modified"] is False
    assert manifest["inherited_campaign"] == "EXP-EMP-20260913-A3"
    assert manifest["accepted_evidence"] is False


def test_v16_scientific_stage_and_integrity_contracts_remain_available() -> None:
    folder = ROOT / "research/publications/2026-09-15_recursive-epistemics_v1.6"
    for name in (
        "README.md",
        "MANUSCRIPT.md",
        "FORSCHUNGSBERICHT.md",
        "SCIENTIFIC_STAGE_MATRIX.md",
        "INTEGRITY_AND_ATTRIBUTION.md",
        "REFERENCES.md",
        "manifest.json",
    ):
        assert (folder / name).is_file(), name

    matrix = (folder / "SCIENTIFIC_STAGE_MATRIX.md").read_text(encoding="utf-8")
    assert "Semantization" in matrix
    assert "Predictive Coding" in matrix
    assert "Weltmodell" in matrix


def test_release_frontend_has_first_class_scientific_timeline() -> None:
    source = (ROOT / "src/dashboard/static/scientific-progress.js").read_text(
        encoding="utf-8"
    )
    assert 'button.dataset.workspaceView = "science"' in source
    assert 'panel.dataset.releaseView = "science"' in source
    assert 'button.dataset.scienceReleaseRoute = "true"' in source
    assert '[data-area-route="science"]' in source
    assert '.mhrn-context-nav[data-area="release"]' in source
    assert "showScientificReleaseView" in source
    assert "Wissenschaftliche Timeline" in source
    assert "Technische Timeline" in source
    assert "reviewte EVID" in source


def test_integrity_gate_refuses_plagiarism_certification() -> None:
    gate = (
        (ROOT / "docs/05-quality/RESEARCH_INTEGRITY_GATE.md")
        .read_text(encoding="utf-8")
        .lower()
    )
    assert "keine plagiatsfreiheit zertifizieren" in gate
    assert "textähnlichkeitsprüfung" in gate
    assert "eigenwiederverwendung" in gate
