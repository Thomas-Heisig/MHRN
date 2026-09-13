"""Regression coverage for canonical Cell Model and Settings navigation."""

from __future__ import annotations

from pathlib import Path

STATIC = Path(__file__).parent.parent / "src" / "dashboard" / "static"


def read(path: str) -> str:
    return (STATIC / path).read_text(encoding="utf-8")


def test_cell_model_is_promoted_to_canonical_science_route() -> None:
    script = read("frontend/modules/neuron-model-science.js")

    assert 'const ROUTE_ID = "cellmodel"' in script
    assert '[ROUTE_ID, "Cell Model", "network", "view", ROUTE_ID]' in script
    assert 'architecture.selectRoute("science", ROUTE_ID)' in script
    assert "data.areaRoute = ROUTE_ID" in script
    assert "data.routeCard = ROUTE_ID" in script


def test_cell_model_does_not_depend_on_hidden_legacy_network_tabs() -> None:
    script = read("frontend/modules/neuron-model-science.js")
    router = read("frontend/workspace-router.js")

    assert "document.querySelector('[data-workspace-views=\"network\"]')" not in script
    assert "#tab-network > .workspace-view-tabs" in router
    assert "classList.add(ROUTED_CLASS)" in router


def test_cell_model_exposes_settings_shortcuts() -> None:
    script = read("frontend/modules/neuron-model-science.js")
    styles = read("neuron-model-settings.css")

    assert 'data-route-jump="control:parameters"' in script
    assert 'data-route-jump="settings:overview"' in script
    assert ">Alle Parameter<" in script
    assert ">App Settings<" in script
    assert ".neuron-model-shortcuts" in styles


def test_settings_navigation_has_fallback_for_legacy_three_area_shell() -> None:
    script = read("frontend/modules/neuron-model-science.js")

    assert "ensureSettingsNavigationFallback" in script
    assert 'button.dataset.mhrnArea = "settings"' in script
    assert 'architecture.selectRoute("settings", "overview")' in script


def test_cell_model_route_restores_from_workspace_router_storage() -> None:
    script = read("frontend/modules/neuron-model-science.js")

    assert "mhrn-workspace-router-v1" in script
    assert 'saved?.area === "science"' in script
    assert "saved?.route === ROUTE_ID" in script
