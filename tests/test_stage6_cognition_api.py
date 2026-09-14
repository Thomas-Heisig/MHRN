"""Actual HTTP cognition boundaries: read gating and typed error projection."""

from __future__ import annotations

import json
from http.client import HTTPConnection
from threading import Thread
from types import SimpleNamespace

from src.dashboard.server import DashboardServer
from src.dashboard.state import DashboardStateStore
from src.embodiment.models import EnvironmentObservation, SensorFrame
from src.memory import MemoryStore, MemoryWorldModel, TransitionWorldModel


def test_cognition_http_projection_preserves_state_and_read_control(tmp_path) -> None:
    model = MemoryWorldModel(
        MemoryStore(run_id="api-test"), TransitionWorldModel(), "api-test"
    )
    for tick in range(3):
        frame = SensorFrame("api-fixture", tick, "digital", {"cue": 1})
        observed = EnvironmentObservation(tick + 1, {"matched": False, "x": 0})
        model.complete(frame, None, observed, tick, model.predict(frame, None, tick))
    server = DashboardServer(
        ("127.0.0.1", 0),
        DashboardStateStore(),
        None,
        profiles_root=tmp_path / "profiles",
        experience=SimpleNamespace(memory=model, behavior_profile=None),
    )
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def request(path, body=None):
        connection = HTTPConnection(*server.server_address, timeout=5)
        try:
            connection.request(
                "GET" if body is None else "POST",
                path,
                None if body is None else json.dumps(body),
                {"Content-Type": "application/json"},
            )
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()

    try:
        before = model.state_dict()
        status, data = request("/api/cognition/predictions?limit=2")
        assert status == 200
        assert len(data["predictions"]) == 2
        record = data["predictions"][-1]
        assert record["predicted_state"]["matched"] is False
        assert record["error_components"]["categorical_mismatch"] == {"matched": 0.0}
        assert record["error_components"]["numeric_absolute"] == {"x": 0.0}
        assert record["error_components"]["coverage"] == 1.0
        assert (
            record["error_components"]["aggregate_kind"]
            == "legacy_mixed_units_not_accuracy"
        )
        assert (
            before == model.state_dict()
        ), "HTTP projection must not mutate canonical persisted records"
        assert request("/api/cognition/predictions?limit=0")[0] == 400
        status, _ = request(
            "/api/cognition/memory/controls",
            {"read_enabled": False, "write_enabled": True},
        )
        assert status == 200
        assert request("/api/cognition/predictions")[1]["predictions"] == []
        assert request("/api/cognition/memory/episodes")[1]["episodes"] == []
        assert request("/api/cognition/state")[1]["memory"]["latest_prediction"] is None
        world = request("/api/cognition/world-model")[1]
        assert world["model"] is None
        assert world["prediction_enabled"] is True
        assert world["learning_enabled"] is True
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
