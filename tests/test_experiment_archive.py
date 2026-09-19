"""Tests for non-destructive experiment work-view archive operations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.dashboard.experiment_archive import ExperimentArchiveService
from src.dashboard.experiment_organizer import ExperimentOrganizerService


def _write_experiment(root: Path, experiment_id: str) -> tuple[Path, dict[str, Any]]:
    experiment = root / "experiments" / experiment_id
    experiment.mkdir(parents=True)
    manifest: dict[str, object] = {
        "experiment_id": experiment_id,
        "experiment_status": "completed",
    }
    payload: dict[str, Any] = {"runs": [{"seed": 42, "condition": "control"}]}
    (experiment / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (experiment / "DATA.json").write_text(json.dumps(payload), encoding="utf-8")
    return experiment, payload


def test_archive_and_restore_keep_canonical_experiment_contents(tmp_path: Path) -> None:
    experiment, payload = _write_experiment(tmp_path, "EXP-ARCHIVE-0001")
    manifest_before = (experiment / "manifest.json").read_bytes()
    data_before = (experiment / "DATA.json").read_bytes()

    service = ExperimentArchiveService(tmp_path)
    archived = service.archive_experiment("EXP-ARCHIVE-0001", "completed run cleanup")

    assert archived["experiment_id"] == "EXP-ARCHIVE-0001"
    assert archived["archive_mode"] == "metadata_only"
    assert experiment.is_dir()
    assert (experiment / "manifest.json").read_bytes() == manifest_before
    assert (experiment / "DATA.json").read_bytes() == data_before
    assert service.archived_ids() == frozenset({"EXP-ARCHIVE-0001"})
    listed = service.list_archived()[0]
    assert listed["reason"] == "completed run cleanup"
    assert listed["canonical_path"] == "experiments/EXP-ARCHIVE-0001"
    assert listed["available"] is True
    assert listed["manifest_sha256"]

    restored = service.restore_experiment("EXP-ARCHIVE-0001")

    assert restored == {
        "experiment_id": "EXP-ARCHIVE-0001",
        "archived": False,
        "restored": True,
        "archive_mode": "metadata_only",
    }
    assert json.loads((experiment / "DATA.json").read_text(encoding="utf-8")) == payload
    assert (experiment / "manifest.json").read_bytes() == manifest_before
    assert service.archived_ids() == frozenset()
    assert service.list_archived() == []


def test_legacy_moved_archive_remains_restoreable(tmp_path: Path) -> None:
    legacy = tmp_path / "archive" / "experiments" / "EXP-LEGACY-0001"
    legacy.mkdir(parents=True)
    (legacy / "manifest.json").write_text(
        json.dumps({"experiment_id": "EXP-LEGACY-0001"}), encoding="utf-8"
    )
    (legacy / "DATA.json").write_text("{}", encoding="utf-8")
    (legacy / "archive.json").write_text(
        json.dumps({"reason": "old dashboard archive"}), encoding="utf-8"
    )

    service = ExperimentArchiveService(tmp_path)
    listed = service.list_archived()

    assert listed[0]["archive_mode"] == "legacy_moved"
    assert listed[0]["legacy"] is True

    restored = service.restore_experiment("EXP-LEGACY-0001")

    assert restored["archive_mode"] == "legacy_moved"
    restored_dir = tmp_path / "experiments" / "EXP-LEGACY-0001"
    assert (restored_dir / "manifest.json").is_file()
    assert not (restored_dir / "archive.json").exists()


def test_archiving_an_already_archived_experiment_is_idempotent(tmp_path: Path) -> None:
    _write_experiment(tmp_path, "EXP-ARCHIVE-IDEMPOTENT")
    service = ExperimentArchiveService(tmp_path)

    first = service.archive_experiment("EXP-ARCHIVE-IDEMPOTENT")
    second = service.archive_experiment("EXP-ARCHIVE-IDEMPOTENT")

    assert first["archived"] is True
    assert second["already_archived"] is True
    assert service.archived_ids() == frozenset({"EXP-ARCHIVE-IDEMPOTENT"})


def test_archive_and_restore_series_archives_children_without_moving_files(
    tmp_path: Path,
) -> None:
    child_a, _ = _write_experiment(tmp_path, "EXP-SERIES-01")
    child_b, _ = _write_experiment(tmp_path, "EXP-SERIES-02")
    workflows = tmp_path / "workflows"
    workflows.mkdir()
    (workflows / "SERIES-0001.json").write_text(
        json.dumps(
            {
                "workflow_id": "SERIES-0001",
                "results": [
                    {"experiment_id": "EXP-SERIES-01"},
                    {"experiment_id": "EXP-SERIES-02"},
                ],
            }
        ),
        encoding="utf-8",
    )

    service = ExperimentArchiveService(tmp_path)
    archived = service.archive_series("SERIES-0001")

    assert archived["archive_type"] == "series"
    assert service.archived_series_ids() == frozenset({"SERIES-0001"})
    listed = service.list_archived()
    assert any(
        item.get("archive_type") == "series" and item.get("series_id") == "SERIES-0001"
        for item in listed
    )
    assert child_a.is_dir() and child_b.is_dir()
    assert service.archive_series("SERIES-0001")["already_archived"] is True

    restored = service.restore_series("SERIES-0001")

    assert restored["restored"] is True
    assert service.archived_series_ids() == frozenset()
    assert service.archived_ids() == frozenset()
    assert child_a.is_dir() and child_b.is_dir()


def test_series_reports_partial_child_archiving(tmp_path: Path) -> None:
    _write_experiment(tmp_path, "EXP-PARTIAL-01")
    _write_experiment(tmp_path, "EXP-PARTIAL-02")
    workflows = tmp_path / "workflows"
    workflows.mkdir()
    (workflows / "SERIES-PARTIAL.json").write_text(
        json.dumps(
            {
                "workflow_id": "SERIES-PARTIAL",
                "completed": 2,
                "failed": 0,
                "results": [
                    {"experiment_id": "EXP-PARTIAL-01", "status": "completed"},
                    {"experiment_id": "EXP-PARTIAL-02", "status": "completed"},
                ],
            }
        ),
        encoding="utf-8",
    )

    archive = ExperimentArchiveService(tmp_path)
    archive.archive_experiment("EXP-PARTIAL-01")
    series = ExperimentOrganizerService(tmp_path).list_series(
        archive.archived_series_ids(), archive.archived_ids()
    )[0]

    assert series["archived"] is True
    assert series["archive_state"] == "partial"
    assert series["inferred_from_children"] is True
    assert series["archived_child_count"] == 1
    assert series["child_count"] == 2
