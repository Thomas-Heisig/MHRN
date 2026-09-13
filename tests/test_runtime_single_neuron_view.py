"""Regression coverage for the Runtime & Wesen single-neuron view."""

from __future__ import annotations

import random
from pathlib import Path

from src.core import Brain5DConfig, NeuralNetwork
from src.core.spatial_index import linear_to_5d
from src.dashboard.network_inspector import NetworkInspector

STATIC = Path(__file__).parent.parent / "src" / "dashboard" / "static"


def _network() -> NeuralNetwork:
    config = Brain5DConfig.from_dict(
        {
            "dimensions": [4, 4, 4, 4, 4],
            "network": {
                "initial_connections_per_neuron": 1,
                "neighbour_radius": 2.0,
            },
        }
    )
    network = NeuralNetwork(config, random.Random(7))
    neuron_id = linear_to_5d(0, config.dimensions)
    network.add_neuron(neuron_id)
    neuron = network.get_neuron(neuron_id)
    assert neuron is not None
    neuron.last_external_current = 4.0
    neuron.last_synaptic_current = 2.0
    neuron.pre_trace = 0.5
    neuron.post_trace = 0.25
    neuron.threshold_adaptation = 0.75
    neuron.firing_rate_estimate = 1.5
    return network


def test_live_neuron_record_exposes_integrated_cell_state() -> None:
    record = NetworkInspector(_network()).neurons(limit=1).neurons[0]
    expected = {
        "model",
        "model_provenance",
        "config",
        "current_threshold",
        "threshold_adaptation",
        "last_external_current",
        "last_synaptic_current",
        "pre_trace",
        "post_trace",
        "firing_rate_estimate",
        "model_switch_count",
        "last_model_switch_tick",
        "enabled",
        "refractory_until_tick",
        "refractory_active",
        "refractory_remaining_ticks",
        "runtime_tick",
    }
    assert expected <= set(record)
    assert record["model"] == "izhikevich-2003"
    assert record["last_external_current"] == 4.0
    assert record["last_synaptic_current"] == 2.0
    assert record["pre_trace"] == 0.5
    assert record["post_trace"] == 0.25
    assert record["threshold_adaptation"] == 0.75
    assert isinstance(record["model_provenance"], dict)
    assert isinstance(record["config"], dict)


def test_runtime_neuron_frontend_is_initialized_from_new_frontend() -> None:
    index = (STATIC / "frontend" / "index.js").read_text(encoding="utf-8")
    module = (STATIC / "frontend" / "modules" / "runtime-neuron.js").read_text(
        encoding="utf-8"
    )
    router = (STATIC / "frontend" / "workspace-router.js").read_text(encoding="utf-8")
    styles = (STATIC / "frontend" / "styles" / "runtime-neuron.css").read_text(
        encoding="utf-8"
    )
    style_index = (STATIC / "frontend" / "styles" / "index.css").read_text(
        encoding="utf-8"
    )

    assert 'import { initRuntimeNeuron } from "./modules/runtime-neuron.js";' in index
    assert "initRuntimeNeuron();" in index
    assert '["neuron", "Neuron", "wesen", "focus", "#mhrn-runtime-neuron"]' in router
    assert 'panel.id = "mhrn-runtime-neuron"' in module
    assert "/api/network/neurons?limit=1&offset=" in module
    assert "model_provenance" in module
    assert "threshold_adaptation" in module
    assert "pre_trace" in module and "post_trace" in module
    assert "last_external_current" in module and "last_synaptic_current" in module
    assert "refractory_remaining_ticks" in module
    assert "biologischer Äquivalenz" in module
    assert ".runtime-neuron-panel" in styles
    assert '@import url("./runtime-neuron.css");' in style_index


def test_runtime_neuron_polling_follows_canonical_router_state() -> None:
    module = (STATIC / "frontend" / "modules" / "runtime-neuron.js").read_text(
        encoding="utf-8"
    )

    assert 'document.body.dataset.currentArea === "wesen"' in module
    assert 'document.body.dataset.currentRoute === "neuron"' in module
    assert "new MutationObserver(syncPolling)" in module
    assert 'attributeFilter: ["data-current-area", "data-current-route"]' in module
    assert "setInterval" in module
    assert "clearInterval" in module
    assert "state.inFlight" in module


def test_runtime_neuron_shows_tick_progress_even_without_new_spikes() -> None:
    module = (STATIC / "frontend" / "modules" / "runtime-neuron.js").read_text(
        encoding="utf-8"
    )

    assert "lastRuntimeTick" in module
    assert "deltaTick" in module
    assert 'deltaTick > 0 ? "RUNNING" : "IDLE/UNCHANGED"' in module
    assert "Δtick" in module
    assert "live_runtime" in module
