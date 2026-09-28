"""Regression coverage for the Stage-1 small-SNN frontend integration."""

from pathlib import Path

STATIC = Path(__file__).parent.parent / "src" / "dashboard" / "static"


def test_small_snn_module_is_initialized() -> None:
    index = (STATIC / "frontend" / "index.js").read_text(encoding="utf-8")
    assert "initSmallSNNStage" in index
    assert "./modules/small-snn-stage.js" in index


def test_small_snn_views_are_preserved_under_old() -> None:
    script = (STATIC / "frontend" / "modules" / "small-snn-stage.js").read_text(
        encoding="utf-8"
    )
    assert "const ROUTES = Object.freeze({});" in script
    assert 'data-route-jump="old:wesen-snn"' in script
    assert 'data-route-jump="old:control-snn"' in script
    assert 'data-route-jump="settings:parameters"' in script
    assert 'data-route-jump="old:science-snn"' in script
    assert 'data-route-jump="release:development"' in script


def test_small_snn_uses_real_network_inspector_endpoints() -> None:
    script = (STATIC / "frontend" / "modules" / "small-snn-stage.js").read_text(
        encoding="utf-8"
    )
    assert '"/api/network/summary"' in script
    assert '"/api/network/synapses?limit=120&offset=0"' in script
    assert "/api/network/neurons?limit=" in script
    assert "live_runtime" in script


def test_small_snn_live_polling_follows_canonical_router_state() -> None:
    script = (STATIC / "frontend" / "modules" / "small-snn-stage.js").read_text(
        encoding="utf-8"
    )
    assert "new MutationObserver(syncPolling)" in script
    assert 'attributeFilter: ["data-current-area", "data-current-route"]' in script
    assert (
        'const liveRoute = area === "old" && (route === "science-snn" || route === "wesen-snn")'
        in script
    )
    assert "setInterval(routeRefresh, 900)" in script
    assert "clearInterval(state.timer)" in script
    assert "runtimeInFlight" in script


def test_small_snn_runtime_shows_tick_progress_with_low_spike_activity() -> None:
    script = (STATIC / "frontend" / "modules" / "small-snn-stage.js").read_text(
        encoding="utf-8"
    )
    assert "runtimeLastTick" in script
    assert "deltaTick" in script
    assert 'deltaTick > 0 ? "RUNNING" : "IDLE/UNCHANGED"' in script
    assert "Δtick" in script
    assert "total spikes" in script
    assert "live_runtime" in script


def test_small_snn_parameter_changes_use_pending_workflow() -> None:
    script = (STATIC / "frontend" / "modules" / "small-snn-stage.js").read_text(
        encoding="utf-8"
    )
    assert "network.initial_connections_per_neuron" in script
    assert "network.neighbour_radius" in script
    assert "/api/parameters/pending/apply" in script
    assert "/pending`" in script
    assert "Neuer Run/Restart erforderlich" in script


def test_small_snn_styles_are_loaded_and_responsive() -> None:
    styles = (STATIC / "frontend" / "styles" / "index.css").read_text(encoding="utf-8")
    module_styles = (STATIC / "frontend" / "styles" / "small-snn.css").read_text(
        encoding="utf-8"
    )
    assert '@import url("./small-snn.css")' in styles
    assert ".small-snn-graph" in module_styles
    assert ".small-snn-node.active" in module_styles
    assert "@media(max-width:620px)" in module_styles
