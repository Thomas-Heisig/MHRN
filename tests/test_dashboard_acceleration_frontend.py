from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_acceleration_frontend_module_is_wired_once() -> None:
    index = (ROOT / "src" / "dashboard" / "static" / "frontend" / "index.js").read_text(
        encoding="utf-8"
    )
    module = (
        ROOT
        / "src"
        / "dashboard"
        / "static"
        / "frontend"
        / "modules"
        / "acceleration-integration.js"
    ).read_text(encoding="utf-8")
    assert "initAccelerationIntegrationStatus" in index
    assert index.count("initAccelerationIntegrationStatus();") == 1
    for panel_id in (
        "mhrn-acceleration-playground",
        "mhrn-acceleration-release",
        "mhrn-acceleration-science",
        "mhrn-acceleration-old",
    ):
        assert panel_id in module
    assert 'readJson("/api/integration/status")' in module
    assert 'readJson("/api/playground/integration")' in module
    assert "Keine Anzeige in diesem Panel erzeugt DATA oder EVID" in module
