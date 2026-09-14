from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_neural_symbiosis_api_publishes_stage4_contract() -> None:
    server = _text("src/dashboard/server.py")
    assert "specialized_area_contract" in server
    assert '"specialized_areas": specialized' in server
    assert '"dynamic_100k_10m_execution_verified": False' in server
    assert '"automatic_evidence_promotion": False' in server


def test_wesen_frontend_renders_stage4_specialized_areas() -> None:
    source = _text("src/dashboard/static/wesen-neural-symbiosis.js")
    assert "wesen-stage4-areas" in source
    assert "Stage 4 · Specialized areas" in source
    assert "specialized_areas" in source
    assert "dynamic_scale_execution_verified" in source
    assert "plasticity_rule" in source


def test_public_msba_frontend_renders_stage4_specialized_areas() -> None:
    source = _text("src/dashboard/static/msba/msba.js")
    assert "renderSpecializedAreas" in source
    assert "stage4-area-list" in source
    assert "symbiosis.specialized_areas" in source
    assert "aggregated topology contract" in source


def test_timeline_uses_verification_instead_of_planned_stage4_scale() -> None:
    source = _text("src/dashboard/development_timeline.py")
    start = source.index('            "specialized_neural_areas",')
    end = source.index('            "integrated_artificial_nervous_system",', start)
    stage4 = source[start:end]
    assert '"scaled_area_network"' in stage4
    assert "planned=True" not in stage4
    assert "specialized_neural_areas_reference_alpha3.json" in stage4
    assert "tests/test_stage4_specialized_neural_areas.py" in stage4
    assert "RQ-MSBA-E05" in stage4
