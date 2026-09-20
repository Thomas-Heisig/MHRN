from pathlib import Path

from src.research.protocol_registry import protocol_catalog

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "src" / "dashboard" / "static"
RESEARCH = ROOT / "research"


def test_operational_protocols_expose_prefill_templates() -> None:
    catalog = protocol_catalog(RESEARCH)
    assert catalog
    for protocol in catalog:
        minimum = protocol["minimum_independent_seeds"]
        assert minimum >= 1
        assert protocol["default_seed_expression"]
        assert "standard" in protocol["condition_profiles"]
        assert protocol["condition_profiles"]["standard"]


def test_experiment_workflow_wrapper_prefills_seed_and_condition_controls() -> None:
    source = (STATIC / "experiment-workflow.js").read_text(encoding="utf-8")
    assert 'from "./experiment-workflow-base.js' in source
    assert "default_seed_expression" in source
    assert "condition_profiles" in source
    assert "_configureConditionProfiles" in source
    assert "Exploratory / diagnostic protocol" in source
    assert "<details" in source


def test_experiment_workflow_batch_ui_is_bound_and_lists_all_questions() -> None:
    source = (STATIC / "experiment-workflow-base.js").read_text(encoding="utf-8")
    html = (STATIC / "index.html").read_text(encoding="utf-8")
    assert "_bindBatchWorkflow" in source
    assert "_runBatchWorkflow" in source
    assert "/api/experiment/workflow/batch" in source
    assert "this.questions.map" in source
    assert 'id="workflow-batch-open"' in html
    assert 'id="workflow-batch-start"' in html


def test_wesen_shell_keeps_embodiment_sibling_and_moves_utilities_to_footer() -> None:
    source = (STATIC / "wesen.js").read_text(encoding="utf-8")
    assert 'import "./wesen-base.js"' in source
    assert "mergeEmbodimentIntoWesen" in source
    assert 'byId("tab-embodiment")' in source
    assert 'data-footer-tab="settings"' in source
    assert 'data-footer-tab="gate"' not in source
    assert 'data-tab="embodiment"' in source
    assert "embodimentButton?.remove()" not in source
    assert "appendChild(embodiment)" not in source
    assert 'embodimentButton.classList.add("wesen-utility-hidden")' in source


def test_visual_shell_v2_is_visible_and_exposes_global_routes() -> None:
    from tests.dashboard_assets import dashboard_css, stylesheet_paths

    frontend = (STATIC / "frontend" / "index.js").read_text(encoding="utf-8")
    router = (STATIC / "frontend" / "workspace-router.js").read_text(encoding="utf-8")
    assert 'import { initWorkspaceRouter } from "./workspace-router.js";' in frontend
    assert "initWorkspaceRouter();" in frontend
    for area in (
        "dashboard",
        "science",
        "wesen",
        "control",
        "release",
        "settings",
        "review",
        "files",
    ):
        assert f"  {area}: {{" in router
    assert 'data-mhrn-area="${id}"' in router
    assert "selectRoute(button.dataset.mhrnArea" in router
    assert "parameter-inspector-card" in router
    assert "/api/research/reviews" in router
    assert "#control-causal-flow,#runtime-control-card" in router
    assert all(path.name != "visual-shell.css" for path in stylesheet_paths())
    assert ".brain5d-primary-nav" in dashboard_css()
    assert ".mhrn-context-nav" in dashboard_css()
