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


def test_playground_ui_exposes_corrected_setting_defaults() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    assert 'id="pg-weight"' in module and 'value="4"' in module
    assert 'id="pg-edges"' in module and 'value="1024"' in module
    assert 'id="pg-k"' in module and 'value="16"' in module
    assert 'id="pg-modules"' in module and 'value="2"' in module
    assert 'id="pg-current"' in module and 'value="8"' in module
    assert 'id="pg-pan-bias-current"' in module and 'value="10"' in module
    assert 'id="pg-behavior-lr"' in module and 'value="0.2"' in module
    assert 'id="pg-behavior-epsilon"' in module and 'value="0.2"' in module
    assert 'value="mixed_additive" selected' in module


def test_playground_ui_keeps_settings_overview_out_of_builder() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    assert 'id="pg-settings-reference"' not in module
    assert "Alle Einstellungsmöglichkeiten" not in module


def test_playground_resets_defaults_on_start_and_marks_overrides_by_hover() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    assert "const PLAYGROUND_DEFAULT_HINTS" in module
    assert "function updateDefaultHints()" in module
    assert "field.title = message" in module
    assert (
        'renderCatalog(await apiGet("/api/playground/catalog"));resetForm();' in module
    )
    assert "pg-non-default" in module


def test_playground_preset_lab_has_izhikevich_pan_and_local_storage() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    assert "Preset Lab" in module
    assert "izhikevich_reference" in module
    assert "pan_exploration" in module
    assert "PLAYGROUND_PRESETS_STORAGE" in module
    assert "function saveUserPreset()" in module
    assert "function deleteUserPreset()" in module
    assert 'id="pg-user-preset-save"' in module
    assert 'id="pg-user-preset-delete"' in module
    assert 'id="pg-closed-loop-preset"' not in module
    assert 'renderCatalog(await apiGet("/api/playground/catalog"));renderUserPresetOptions();resetForm();' in module
    assert 'change",()=>{renderUserPresetOptions();applyUserPreset();}' in module
    assert "const selected=select.value" in module
    assert "presets[selected]" in module
    assert 'synapse_model:"synapse-model"' in module
    assert 'plasticity_rule:"plasticity"' in module
    assert 'n_neurons:"neurons"' in module
    assert 'edge_budget:"edges"' in module
    assert 'stimulus_current:"current"' in module
    assert 'behavior_episode_ticks:"behavior-episode"' in module


def test_playground_preset_catalog_documentation_exists() -> None:
    path = ROOT / "docs" / "playground" / "PRESETS.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for preset in (
        "open_loop_baseline",
        "fix_weight_explosion",
        "d1_minimal_closed_loop",
        "g1_two_action_simple",
        "g2_one_action_trivial",
    ):
        assert preset in text


def test_playground_live_monitor_exposes_popup_controls_and_graphs() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    for marker in (
        "pg-live-monitor",
        "pg-live-monitor-chart",
        "pg-live-tile-reset",
        "pg-live-tile-figure",
        "pg-live-tile-raster",
        "pg-live-tile-rate",
        "pg-live-tile-topology",
        "pg-live-tile-input",
        "pg-live-tile-output",
        "pg-live-tile-membrane",
        "pg-live-tile-spectrum",
        "pg-live-tile-degree",
        "pg-live-monitor-start",
        "pg-live-monitor-pause",
        "pg-live-monitor-step",
        "pg-live-monitor-stop",
        "ensureLiveMonitor().showModal()",
        "drawLiveMonitorFigure",
        "openLiveZoom",
    ):
        assert marker in module


def test_playground_api_has_bounded_concurrency_and_rate() -> None:
    api = (ROOT / "src" / "dashboard" / "playground_api.py").read_text(encoding="utf-8")
    assert "_MAX_CONCURRENT_RUNS = 2" in api
    assert "_RUNS_PER_MINUTE = 20" in api
    assert "threading.BoundedSemaphore" in api
    assert "PlaygroundRateLimitError" in api


def test_playground_ui_exposes_pan_as_non_scientific_option() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    assert "PAN-Hyperstate" in module
    assert "PAN explorativ aktivieren" in module
    assert "keine validierte PID" in module
    assert "PAN Research Candidates" in module


def test_pan_research_context_and_glossary_exist() -> None:
    context = ROOT / "docs" / "playground" / "PAN_5D_RESEARCH_CONTEXT.md"
    glossary = ROOT / "docs" / "playground" / "GLOSSARY.md"
    assert context.exists()
    assert glossary.exists()
    context_text = context.read_text(encoding="utf-8")
    glossary_text = glossary.read_text(encoding="utf-8")
    assert "kein Beweis weltweiter Neuheit" in context_text
    assert "Spike-Amplitude-Dependent Plasticity" in glossary_text
    assert "Spike Agreement Dependent Plasticity" in glossary_text


def test_playground_ui_exposes_independent_geometry_controls() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    assert "Geometrischer Raum Dg" in module
    assert "Shortcut Union" in module
    assert "Mixed Additive" in module
    assert "Torus-Koordinaten" in module
    assert "Klein-Flasche" in module


def test_geometry_documentation_states_core_corrections() -> None:
    geometry = ROOT / "docs" / "playground" / "geometry.md"
    assert geometry.exists()
    text = geometry.read_text(encoding="utf-8")
    assert "Torus S¹ × S¹" in text
    assert "keine universelle Small-World-Schwelle" in text
    assert "effektive Dimension zwischen 4 und 6" in text
    assert "nicht als belegt übernommen" in text


def test_pan_complete_documentation_covers_all_candidates() -> None:
    path = ROOT / "docs" / "playground" / "PAN_COMPLETE_DOCUMENTATION.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "keine DATA" in text
    assert "keine EVID" in text
    assert "Research Candidates 1–18" in text
    for candidate in range(1, 19):
        assert f"### {candidate} —" in text


def test_geometry_documents_shortcut_normalization_as_open_question() -> None:
    path = ROOT / "docs" / "playground" / "geometry.md"
    text = path.read_text(encoding="utf-8")
    assert "Open normalization question" in text
    assert "geometric_3d" in text
    assert "No option is currently preferred" in text


def test_playground_ui_exposes_neural_input_output_interface() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    assert "09 · Neural I/O Interface" in module
    assert "GATEWAY_AFFERENT" in module
    assert "GATEWAY_EFFERENT" in module
    assert "Payload ≠ Neural Representation" in module
    assert "pg-analysis-io" in module


def test_neural_io_documentation_exists_and_preserves_boundary() -> None:
    path = ROOT / "docs" / "playground" / "neural_io.md"
    examples = ROOT / "docs" / "playground" / "neural_io_examples.md"
    assert path.exists()
    assert examples.exists()
    text = path.read_text(encoding="utf-8")
    assert "Payload != Neural Representation" in text
    assert "Codec != GatewayTopology != GatewayLearning" in text
    assert "QUERY" in text and "TIMEOUT" in text
    assert "tool_plane_execution = false" in text


def test_playground_ui_exposes_live_pan_session_controls() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    assert "17 · PAN Live Session & Sandbox" in module
    assert "pg-live-create" in module
    assert "pg-live-step" in module
    assert "pg-live-input" in module
    assert "pg-live-sandbox" in module
    assert "pg-live-stop" in module


def test_playground_api_exposes_stateful_live_routes_without_research_promotion() -> (
    None
):
    api = (ROOT / "src" / "dashboard" / "playground_api.py").read_text(encoding="utf-8")
    assert '"/api/playground/live/create"' in api
    assert 'action == "step"' in api
    assert 'action == "input"' in api
    assert 'action == "sandbox"' in api
    assert 'action == "stop"' in api
    assert "PANSessionDaemon" in api
    assert "EvidenceEngine" not in api


def test_playground_ui_exposes_meta_night_run_monitor() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    assert "18 · Meta-Nachtlauf" in module
    assert "pg-night-start" in module
    assert "pg-night-stop" in module
    assert "pg-night-refresh" in module
    assert '"/api/playground/night/start"' in module
    assert '"/api/playground/night/stop"' in module
    assert '"/api/playground/night"' in module


def test_playground_api_wires_meta_strategy_reward_and_night_run() -> None:
    api = (ROOT / "src" / "dashboard" / "playground_api.py").read_text(encoding="utf-8")
    assert "NightRunManager" in api
    assert '"/api/playground/night/start"' in api
    assert '"/api/playground/night/stop"' in api
    assert 'action == "strategy"' in api
    assert 'action == "reward"' in api
    assert "EvidenceEngine" not in api
    assert "promote_validated_experiment" not in api


def test_playground_ui_exposes_closed_loop_builder_sections() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    for section in (
        "10 · Input-Kanäle",
        "11 · Aktions-Loop",
        "12 · Ziel-Kodierung",
        "13 · Belohnung",
        "14 · Kredit-Zuweisung",
        "15 · Netzwerk-Heterogenität & Zeit",
        "Preset Lab",
    ):
        assert section in module
    assert 'id="pg-action-loop-enabled"' in module
    assert 'id="pg-pan-feedback-nonlinearity"' in module
    assert 'id="pg-target-encoding"' in module
    assert 'id="pg-reward-enabled"' in module
    assert 'id="pg-credit-assignment"' in module
    assert 'id="pg-user-preset-select"' in module
    assert 'id="pg-closed-loop-preset"' not in module
    assert "applyUserPreset" in module


def test_playground_ui_exposes_cuda_gate_compiler_preview() -> None:
    module = (STATIC / "frontend" / "modules" / "playground.js").read_text(
        encoding="utf-8"
    )
    api = (ROOT / "src" / "dashboard" / "playground_api.py").read_text(
        encoding="utf-8"
    )
    assert "19 · CUDA Gate Compiler" in module
    assert 'id="pg-cuda-compile"' in module
    assert 'id="pg-cuda-target-sm"' in module
    assert '"/api/playground/cuda/compile"' in module
    assert 'path == "/api/playground/cuda/compile"' in api
    assert "compile_mapping" in api
    assert "EvidenceEngine" not in api
