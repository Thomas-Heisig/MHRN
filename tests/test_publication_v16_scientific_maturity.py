from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_v16_is_current_without_rewriting_v15_empirical_baseline() -> None:
    catalog = _json("research/publications/catalog.json")
    assert catalog["current_publication_id"] == "PUB-RECURSIVE-EPISTEMICS-20260915-V1.6"
    current = next(item for item in catalog["publications"] if item.get("current"))
    assert current["version"] == "1.6"
    assert current["automatic_evidence_promotion"] is False
    assert current["inherits_empirical_edition"] == "PUB-RECURSIVE-EPISTEMICS-20260913-V1.5"

    baseline = next(
        item
        for item in catalog["publications"]
        if item["id"] == "PUB-RECURSIVE-EPISTEMICS-20260913-V1.5"
    )
    assert baseline["current"] is False
    assert baseline["edition_status"] == "historical_empirical_baseline"

    manifest = _json("research/publications/2026-09-15_recursive-epistemics_v1.6/manifest.json")
    assert manifest["historical_data_modified"] is False
    assert manifest["inherited_campaign"] == "EXP-EMP-20260913-A3"
    assert manifest["accepted_evidence"] is False


def test_project_identity_separates_engineering_and_scientific_scope() -> None:
    identity = _json("project_identity.json")
    assert identity["publication"]["edition"] == "1.6"
    assert identity["publication"]["empirical_baseline"].endswith("recursive-epistemics_v1.5")
    scope = identity["scientific_scope"]
    assert scope["engineering_maturity_is_scientific_evidence"] is False
    assert scope["scientific_maturity_is_consciousness_metric"] is False
    assert scope["automatic_evidence_promotion"] is False


def test_v16_contains_scientific_stage_and_integrity_contracts() -> None:
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
    assert "Stage 6" in matrix or "Stufe 6" in matrix
    assert "Semantization" in matrix
    assert "Predictive Coding" in matrix
    assert "Weltmodell" in matrix
    assert "kein Stage-Score" in matrix or "Kein Stage-Score" in matrix


def test_release_frontend_has_first_class_scientific_timeline() -> None:
    source = (ROOT / "src/dashboard/static/scientific-progress.js").read_text(encoding="utf-8")
    assert 'button.dataset.workspaceView = "science"' in source
    assert 'panel.dataset.releaseView = "science"' in source
    assert "Wissenschaftliche Timeline" in source
    assert "Technische Timeline" in source
    assert "reviewte EVID" in source


def test_integrity_gate_refuses_plagiarism_certification() -> None:
    gate = (ROOT / "docs/05-quality/RESEARCH_INTEGRITY_GATE.md").read_text(encoding="utf-8").lower()
    assert "keine plagiatsfreiheit zertifizieren" in gate
    assert "textähnlichkeitsprüfung" in gate
    assert "eigenwiederverwendung" in gate
