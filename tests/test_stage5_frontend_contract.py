"""Static full-stack contract tests for the Stage-5 dashboard projection."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "src/dashboard/static"


def test_stage5_frontend_module_is_loaded() -> None:
    index = (STATIC / "frontend/index.js").read_text(encoding="utf-8")
    assert 'import { initIntegratedNervousSystem } from "./modules/integrated-nervous-system.js";' in index
    assert "initIntegratedNervousSystem();" in index


def test_stage5_frontend_consumes_existing_embodiment_apis() -> None:
    source = (
        STATIC / "frontend/modules/integrated-nervous-system.js"
    ).read_text(encoding="utf-8")
    for endpoint in (
        "/api/embodiment/state",
        "/api/embodiment/pipeline",
        "/api/embodiment/connections",
    ):
        assert endpoint in source
    for label in (
        "Sensorik",
        "Interozeption",
        "Aktorik",
        "Feedback",
        "Ressourcen",
    ):
        assert label in source


def test_stage5_frontend_keeps_scientific_boundary_visible() -> None:
    source = (
        STATIC / "frontend/modules/integrated-nervous-system.js"
    ).read_text(encoding="utf-8")
    assert "keine automatische EVID-Freigabe" in source
    assert "Real-Device/Langzeit" in source
