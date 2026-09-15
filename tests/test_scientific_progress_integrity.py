from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "src" / "dashboard" / "static" / "scientific-progress.json"
INTEGRITY = ROOT / "research" / "INTEGRITY_AND_ATTRIBUTION.md"
RELATED = ROOT / "research" / "RELATED_WORK.md"
LOADER = ROOT / "src" / "dashboard" / "static" / "formula-renderer.js"
TIMELINE = ROOT / "src" / "dashboard" / "static" / "scientific-progress.js"


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_scientific_manifest_covers_canonical_stages_zero_through_ten() -> None:
    data = _manifest()
    stages = data["stages"]
    assert isinstance(stages, list)
    assert [stage["stage"] for stage in stages] == list(range(11))
    assert all(0.0 <= float(stage["score"]) <= 1.0 for stage in stages)


def test_scientific_weights_are_explicit_and_normalized() -> None:
    data = _manifest()
    weights = data["weights"]
    assert isinstance(weights, dict)
    assert set(weights) == {
        "research_question",
        "protocol",
        "data",
        "reviewed_evidence",
        "independent_replication",
        "attribution",
    }
    assert abs(sum(float(value) for value in weights.values()) - 1.0) < 1e-9


def test_stage6_does_not_overclaim_memory_or_world_model_maturity() -> None:
    stage6 = next(stage for stage in _manifest()["stages"] if stage["stage"] == 6)
    boundary = str(stage6["claim_boundary"]).lower()
    assert "keine semantization" in boundary
    assert "kein hierarchisches predictive coding" in boundary
    assert "kein generatives weltmodell" in boundary
    assert float(stage6["score"]) < 0.5


def test_integrity_policy_refuses_false_plagiarism_certification() -> None:
    text = (
        INTEGRITY.read_text(encoding="utf-8")
        .lower()
        .replace("**", "")
        .replace("__", "")
    )
    assert "does not certify" in text
    assert "similarity" in text
    assert "human source review" in text
    assert "ai-generated references" in text


def test_related_work_quarantines_unverified_citations() -> None:
    text = RELATED.read_text(encoding="utf-8")
    assert "ArithSpec" in text and "QUARANTINED" in text
    assert "NeuroEval" in text
    assert "D'Alba" in text
    assert "Predictive coding with spiking neural networks" in text
    assert "Spiking world model" in text


def test_scientific_timeline_is_loaded_without_replacing_formula_contract() -> None:
    loader = LOADER.read_text(encoding="utf-8")
    timeline = TIMELINE.read_text(encoding="utf-8")
    assert 'import "./scientific-progress.js"' in loader
    assert 'MATH_ROOT_SELECTOR = ".fm-markdown, .pub-reader-article"' in loader
    assert 'processHtmlClass: "fm-markdown|pub-reader-article"' in loader
    assert "scientific-progress.json" in timeline
    assert "Wissenschaftliche Timeline" in timeline
    assert "keine Kognitionskennzahl" in timeline
