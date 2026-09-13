"""Regression coverage for the Stage-2 recurrent-SNN frontend integration."""

from pathlib import Path

STATIC = Path(__file__).parent.parent / "src" / "dashboard" / "static"


def test_recurrent_snn_module_is_initialized() -> None:
    index = (STATIC / "frontend" / "index.js").read_text(encoding="utf-8")
    assert "initRecurrentSNNStage" in index
    assert "./modules/recurrent-snn-stage.js" in index


def test_recurrent_snn_is_routed_through_science_runtime_and_control() -> None:
    script = (STATIC / "frontend" / "modules" / "recurrent-snn-stage.js").read_text(
        encoding="utf-8"
    )
    assert '["recurrent", "Rekurrentes SNN", "network", "view", "recurrent"]' in script
    assert '["recurrent", "Rekurrenz", "wesen", "focus", "#mhrn-runtime-recurrent"]' in script
    assert (
        '["recurrent", "Rekurrenz-Parameter", "settings", "focus", "#mhrn-recurrent-control"]'
        in script
    )
    assert 'data-route-jump="release:development"' in script


def test_recurrent_snn_uses_live_network_endpoints() -> None:
    script = (STATIC / "frontend" / "modules" / "recurrent-snn-stage.js").read_text(
        encoding="utf-8"
    )
    assert '"/api/network/summary"' in script
    assert '"/api/network/synapses?limit=160&offset=0"' in script
    assert "/api/network/neurons?limit=" in script
    assert "live_runtime" in script


def test_recurrent_snn_runtime_exposes_tick_and_queue_progress() -> None:
    script = (STATIC / "frontend" / "modules" / "recurrent-snn-stage.js").read_text(
        encoding="utf-8"
    )
    assert "new MutationObserver(syncPolling)" in script
    assert 'attributeFilter: ["data-current-area", "data-current-route"]' in script
    assert 'const liveRoute = route === "recurrent"' in script
    assert "setInterval(routeRefresh, 1000)" in script
    assert "clearInterval(state.timer)" in script
    assert "state.inFlight" in script
    assert "deltaTick" in script
    assert 'deltaTick > 0 ? "RUNNING" : "IDLE/UNCHANGED"' in script
    assert "queue" in script


def test_recurrent_snn_parameter_changes_use_pending_workflow() -> None:
    script = (STATIC / "frontend" / "modules" / "recurrent-snn-stage.js").read_text(
        encoding="utf-8"
    )
    assert "network.initial_connections_per_neuron" in script
    assert "network.neighbour_radius" in script
    assert "neuron.refractory_ticks" in script
    assert "/api/parameters/pending/apply" in script
    assert "Neuer Run/Restart erforderlich" in script


def test_recurrent_snn_frontend_preserves_scientific_boundary() -> None:
    script = (STATIC / "frontend" / "modules" / "recurrent-snn-stage.js").read_text(
        encoding="utf-8"
    )
    assert "Engineering-Verifikation" in script
    assert "100.000 ticks/run DATA" in script
    assert "Kein Nachweis biologischer Äquivalenz" in script
