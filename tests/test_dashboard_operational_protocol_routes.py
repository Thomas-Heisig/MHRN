from __future__ import annotations

import json
from http.client import HTTPConnection
from pathlib import Path
from threading import Thread
from typing import Any

import src.dashboard.server as server_module
from src.dashboard.research_source import ResearchSource
from src.dashboard.server import DashboardServer
from src.dashboard.state import DashboardStateStore


class _FakeScienceService:
    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        pass

    def run_science(self, body: dict[str, object]) -> dict[str, object]:
        return {
            "experiment_id": str(body.get("experiment_id") or "EXP-ROUTE-SNN-001"),
            "manifest": "experiments/EXP-ROUTE-SNN-001/manifest.json",
            "report": "experiments/EXP-ROUTE-SNN-001/report.md",
            "result": {"runner": "run_sustained_stability"},
        }


def _request(server: DashboardServer, body: dict[str, object]) -> tuple[int, dict[str, object]]:
    host, port = server.server_address[:2]
    connection = HTTPConnection(str(host), int(port), timeout=5)
    try:
        payload = json.dumps(body)
        connection.request(
            "POST",
            "/api/experiment/workflow/run",
            payload,
            {"Content-Type": "application/json"},
        )
        response = connection.getresponse()
        return response.status, json.loads(response.read().decode("utf-8"))
    finally:
        connection.close()


def test_single_run_accepts_registered_sustained_activity_protocol(monkeypatch: Any) -> None:
    monkeypatch.setattr(server_module, "ExperimentWorkflowService", _FakeScienceService)
    server = DashboardServer(
        ("127.0.0.1", 0),
        DashboardStateStore(),
        None,
        research_source=ResearchSource(Path("research")),
    )
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        status, response = _request(
            server,
            {
                "experiment_id": "EXP-ROUTE-SNN-001",
                "question_id": "RQ-SNN-001",
                "hypothesis_id": "H-SNN-001-A",
                "title": "Sustained activity stability",
                "conditions": "registered",
                "ticks": 100000,
                "seeds": "42-51",
                "notes": "routing regression",
                "protocol": "sustained_activity_stability_v1",
            },
        )
        assert status == 200, response
        assert response["ok"] is True
        assert response["result"] == {"runner": "run_sustained_stability"}
    finally:
        server.shutdown()
        server.server_close()


def test_single_run_still_rejects_unknown_protocol(monkeypatch: Any) -> None:
    monkeypatch.setattr(server_module, "ExperimentWorkflowService", _FakeScienceService)
    server = DashboardServer(
        ("127.0.0.1", 0),
        DashboardStateStore(),
        None,
        research_source=ResearchSource(Path("research")),
    )
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        status, response = _request(
            server,
            {
                "experiment_id": "EXP-ROUTE-UNKNOWN",
                "protocol": "definitely_unknown_protocol_v1",
            },
        )
        assert status == 400
        assert "Unknown experiment protocol" in str(response.get("error"))
    finally:
        server.shutdown()
        server.server_close()
