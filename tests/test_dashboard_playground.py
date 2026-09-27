"""Dashboard wiring contract for the dedicated Playground workspace."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "src" / "dashboard" / "static"


def test_playground_frontend_is_initialized() -> None:
    frontend = (STATIC / "frontend" / "index.js").read_text(encoding="utf-8")
    assert 'import { initPlayground } from "./modules/playground.js";' in frontend
    assert "initPlayground();" in frontend


def test_playground_is_first_class_workspace() -> None:
    router = (STATIC / "frontend" / "workspace-router.js").read_text(encoding="utf-8")
    assert 'label: "Playground"' in router
    assert 'owner: "playground"' in router
    assert 'createGeneratedWorkspace("playground", "Playground"' in router
    assert '"/api/playground/catalog"' in router


def test_playground_api_is_routed_without_research_promotion() -> None:
    server = (ROOT / "src" / "dashboard" / "server.py").read_text(encoding="utf-8")
    api = (ROOT / "src" / "dashboard" / "playground_api.py").read_text(encoding="utf-8")
    assert 'path.startswith("/api/playground/")' in server
    assert '"/api/playground/run"' in api
    assert '"/api/playground/robustness"' in api
    assert "promote_validated_experiment" not in api
    assert "EvidenceEngine" not in api
    assert "human_review" not in api


def test_playground_ui_has_permanent_non_scientific_boundary() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    assert "explorativ, nicht-wissenschaftlich, keine EVID-Bindung" in module
    assert "MHRN 5D" in module
    assert "Generic N-D" in module
    assert "Robustheitskontrollen" in module


def test_playground_api_has_bounded_concurrency_and_rate() -> None:
    api = (ROOT / "src" / "dashboard" / "playground_api.py").read_text(encoding="utf-8")
    assert "_MAX_CONCURRENT_RUNS = 2" in api
    assert "_RUNS_PER_MINUTE = 20" in api
    assert "threading.BoundedSemaphore" in api
    assert "PlaygroundRateLimitError" in api



def test_playground_ui_exposes_pan_as_non_scientific_option() -> None:
    module = (
        STATIC / "frontend" / "modules" / "playground.js"
    ).read_text(encoding="utf-8")
    assert "PAN-Hyperstate" in module
    assert "PAN explorativ aktivieren" in module
    assert "keine validierte PID" in module
    assert "PAN Research Candidates" in module
