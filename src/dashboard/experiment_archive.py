"""Non-destructive research experiment work-view archive.

Scientific experiment directories are canonical artifacts. Archiving therefore
must never move or rewrite ``research/experiments/<id>``. The dashboard archive
is a small metadata index that controls visibility in the active work view.

Legacy moved archives created by older dashboard versions remain discoverable
and can be restored once, preserving backwards compatibility without continuing
the destructive move-based design.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

from .research_source import normalize_experiment_manifest


class ExperimentArchiveError(ValueError):
    """Raised when an experiment archive operation is unsafe or invalid."""


class ExperimentArchiveService:
    """Maintain a reversible metadata-only archive for research experiments."""

    INDEX_SCHEMA_VERSION = 2

    def __init__(self, research_root: Path) -> None:
        self.root = research_root
        self.experiments = research_root / "experiments"
        self.archive_root = research_root / "archive"
        self.legacy_archive = self.archive_root / "experiments"
        self.index_path = self.archive_root / "experiment_index.json"

    def _validate_id(self, experiment_id: str) -> str:
        if not experiment_id or experiment_id in {".", ".."}:
            raise ExperimentArchiveError("experiment_id is required")
        if (
            Path(experiment_id).name != experiment_id
            or "/" in experiment_id
            or "\\" in experiment_id
        ):
            raise ExperimentArchiveError("invalid experiment_id")
        return experiment_id

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _load_index(self) -> dict[str, dict[str, Any]]:
        if not self.index_path.is_file():
            return {}
        try:
            payload: object = json.loads(self.index_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ExperimentArchiveError(
                "experiment archive index is unreadable"
            ) from exc
        if not isinstance(payload, dict):
            raise ExperimentArchiveError("experiment archive index must be an object")
        payload_map = cast(dict[object, object], payload)
        raw_items: object = payload_map.get("experiments", {})
        if not isinstance(raw_items, dict):
            raise ExperimentArchiveError(
                "experiment archive index experiments must be an object"
            )
        result: dict[str, dict[str, Any]] = {}
        for key, value in cast(dict[object, object], raw_items).items():
            if isinstance(key, str) and isinstance(value, dict):
                result[key] = cast(dict[str, Any], value)
        return result

    def _write_index(self, records: dict[str, dict[str, Any]]) -> None:
        self.archive_root.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": self.INDEX_SCHEMA_VERSION,
            "archive_mode": "metadata_only",
            "experiments": {key: records[key] for key in sorted(records)},
        }
        temp = self.index_path.with_suffix(".json.tmp")
        temp.write_text(
            json.dumps(payload, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temp.replace(self.index_path)

    def archived_ids(self) -> frozenset[str]:
        """Return metadata-archived experiment IDs without touching artifacts."""
        return frozenset(
            experiment_id
            for experiment_id, metadata in self._load_index().items()
            if metadata.get("archive_type", "experiment") == "experiment"
        )

    def archived_series_ids(self) -> frozenset[str]:
        """Return metadata-archived workflow series IDs."""
        return frozenset(
            series_id
            for series_id, metadata in self._load_index().items()
            if metadata.get("archive_type") == "series"
        )

    @staticmethod
    def _load_manifest(directory: Path) -> dict[str, Any] | None:
        """Load manifest.json from a directory if present and valid."""
        manifest_path = directory / "manifest.json"
        if not manifest_path.is_file():
            return None
        try:
            data: object = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return cast(dict[str, Any], data) if isinstance(data, dict) else None

    def list_archived(self) -> list[dict[str, Any]]:
        """List metadata-only entries plus discoverable legacy moved archives."""
        records = self._load_index()
        items: list[dict[str, Any]] = []
        for experiment_id, metadata in sorted(records.items(), reverse=True):
            if metadata.get("archive_type", "experiment") != "experiment":
                continue
            canonical = self.experiments / experiment_id
            manifest_data = self._load_manifest(canonical)
            dashboard_manifest = (
                normalize_experiment_manifest(canonical, manifest_data)
                if manifest_data is not None
                else None
            )
            items.append(
                {
                    "experiment_id": experiment_id,
                    "archived": True,
                    "archive_mode": "metadata_only",
                    "canonical_path": f"experiments/{experiment_id}",
                    "available": (canonical / "manifest.json").is_file(),
                    **(
                        {"manifest": dashboard_manifest}
                        if dashboard_manifest is not None
                        else {}
                    ),
                    **metadata,
                }
            )

        indexed = set(records)
        if self.legacy_archive.is_dir():
            for directory in sorted(self.legacy_archive.iterdir(), reverse=True):
                if not directory.is_dir() or directory.name in indexed:
                    continue
                manifest = directory / "manifest.json"
                if not manifest.is_file():
                    continue
                legacy_metadata: dict[str, Any] = {}
                metadata_path = directory / "archive.json"
                if metadata_path.is_file():
                    try:
                        loaded: object = json.loads(
                            metadata_path.read_text(encoding="utf-8")
                        )
                        if isinstance(loaded, dict):
                            legacy_metadata = cast(dict[str, Any], loaded)
                    except (OSError, json.JSONDecodeError):
                        legacy_metadata = {}
                manifest_data = self._load_manifest(directory)
                dashboard_manifest = (
                    normalize_experiment_manifest(directory, manifest_data)
                    if manifest_data is not None
                    else None
                )
                items.append(
                    {
                        "experiment_id": directory.name,
                        "archived": True,
                        "archive_mode": "legacy_moved",
                        "legacy": True,
                        "canonical_path": f"experiments/{directory.name}",
                        "available": True,
                        **(
                            {"manifest": dashboard_manifest}
                            if dashboard_manifest is not None
                            else {}
                        ),
                        **legacy_metadata,
                    }
                )
        return items

    def archive_experiment(
        self, experiment_id: str, reason: str = ""
    ) -> dict[str, Any]:
        """Hide an experiment from the active work view without moving it."""
        experiment_id = self._validate_id(experiment_id)
        source = self.experiments / experiment_id
        manifest = source / "manifest.json"
        if not manifest.is_file():
            raise ExperimentArchiveError(f"experiment not found: {experiment_id}")
        records = self._load_index()
        if experiment_id in records:
            existing = records[experiment_id]
            if existing.get("archive_type", "experiment") == "experiment":
                return {
                    "archived": True,
                    "already_archived": True,
                    "archive_mode": "metadata_only",
                    **existing,
                }
            raise ExperimentArchiveError(
                f"archive key is already used by a series: {experiment_id}"
            )
        if (self.legacy_archive / experiment_id).exists():
            raise ExperimentArchiveError(
                f"legacy archived experiment already exists: {experiment_id}"
            )
        archived_at = datetime.now(timezone.utc).isoformat()
        metadata = {
            "experiment_id": experiment_id,
            "archived_at": archived_at,
            "reason": reason.strip() or "manual work-view archive",
            "original_path": f"experiments/{experiment_id}",
            "manifest_sha256": self._sha256(manifest),
        }
        records[experiment_id] = metadata
        self._write_index(records)
        return {"archived": True, "archive_mode": "metadata_only", **metadata}

    @property
    def research_workflows(self) -> Path:
        return self.root / "workflows"

    def _series_experiment_ids(self, series_id: str) -> list[str]:
        workflow = self.research_workflows / f"{series_id}.json"
        if not workflow.is_file():
            raise ExperimentArchiveError(f"experiment series not found: {series_id}")
        try:
            payload: object = json.loads(workflow.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ExperimentArchiveError(
                f"experiment series is unreadable: {series_id}"
            ) from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
            raise ExperimentArchiveError(f"experiment series has no results: {series_id}")
        result_ids: list[str] = []
        for result in cast(list[object], payload["results"]):
            if isinstance(result, dict) and isinstance(result.get("experiment_id"), str):
                result_ids.append(result["experiment_id"])
        return list(dict.fromkeys(result_ids))

    def archive_series(self, series_id: str, reason: str = "") -> dict[str, Any]:
        """Hide a workflow series and its child experiments from active views."""
        series_id = self._validate_id(series_id)
        records = self._load_index()
        if series_id in records:
            existing = records[series_id]
            if existing.get("archive_type") == "series":
                return {
                    "archived": True,
                    "already_archived": True,
                    "archive_mode": "metadata_only",
                    **existing,
                }
            raise ExperimentArchiveError(
                f"archive key is already used by an experiment: {series_id}"
            )

        child_ids = self._series_experiment_ids(series_id)
        owned_child_ids: list[str] = []
        for child_id in child_ids:
            records = self._load_index()
            if child_id in records:
                continue
            if not (self.experiments / child_id / "manifest.json").is_file():
                raise ExperimentArchiveError(f"experiment not found: {child_id}")
            self.archive_experiment(child_id, reason or f"series {series_id}")
            owned_child_ids.append(child_id)

        records = self._load_index()
        metadata = {
            "archive_type": "series",
            "series_id": series_id,
            "experiment_id": series_id,
            "archived_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason.strip() or "manual work-view series archive",
            "original_path": f"workflows/{series_id}.json",
            "child_experiment_ids": child_ids,
            "owned_child_experiment_ids": owned_child_ids,
        }
        records[series_id] = metadata
        self._write_index(records)
        return {"archived": True, "archive_mode": "metadata_only", **metadata}

    def restore_experiment(self, experiment_id: str) -> dict[str, Any]:
        """Return an experiment to the active view, restoring legacy moves once."""
        experiment_id = self._validate_id(experiment_id)
        records = self._load_index()
        if experiment_id in records:
            if records[experiment_id].get("archive_type") == "series":
                return self.restore_series(experiment_id)
            canonical = self.experiments / experiment_id / "manifest.json"
            if not canonical.is_file():
                raise ExperimentArchiveError(
                    f"canonical experiment missing while archived: {experiment_id}"
                )
            records.pop(experiment_id)
            self._write_index(records)
            return {
                "experiment_id": experiment_id,
                "archived": False,
                "restored": True,
                "archive_mode": "metadata_only",
            }

        source = self.legacy_archive / experiment_id
        target = self.experiments / experiment_id
        if not (source / "manifest.json").is_file():
            raise ExperimentArchiveError(
                f"archived experiment not found: {experiment_id}"
            )
        if target.exists():
            raise ExperimentArchiveError(
                f"active experiment already exists: {experiment_id}"
            )
        metadata_path = source / "archive.json"
        if metadata_path.exists():
            metadata_path.unlink()
        self.experiments.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(target))
        return {
            "experiment_id": experiment_id,
            "archived": False,
            "restored": True,
            "archive_mode": "legacy_moved",
        }

    def restore_series(self, series_id: str) -> dict[str, Any]:
        """Restore a metadata-only series and children archived with it."""
        series_id = self._validate_id(series_id)
        records = self._load_index()
        metadata = records.get(series_id)
        if not metadata or metadata.get("archive_type") != "series":
            raise ExperimentArchiveError(f"archived series not found: {series_id}")
        for child_id in metadata.get("owned_child_experiment_ids", []):
            if isinstance(child_id, str):
                records.pop(child_id, None)
        records.pop(series_id, None)
        self._write_index(records)
        return {
            "series_id": series_id,
            "archived": False,
            "restored": True,
            "archive_mode": "metadata_only",
        }
