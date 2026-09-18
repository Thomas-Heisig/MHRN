"""Read-only research registry and report source for the dashboard.

Exposes the MHRN Scientific Evidence Framework (B5D-SEF) artifacts
located under ``research/`` to the operator dashboard. The source is
strictly read-only and resolves paths defensively so a missing or
partially populated research tree never crashes the dashboard.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from .models import JSONValue


@dataclass(frozen=True)
class ResearchDocument:
    """One research artifact exposed to the dashboard."""

    name: str
    path: str
    kind: str
    size_bytes: int
    category: str


def classify_ai_operation(manifest: dict[str, Any]) -> str:
    """Classify AI execution provenance for read-only dashboard display."""
    explicit = manifest.get("ai_operation_mode", manifest.get("operation_mode"))
    if isinstance(explicit, str) and explicit in {
        "REPLAY",
        "LIVE_FROZEN_MODEL",
        "LIVE_EXTERNAL_API",
        "NONE",
        "UNKNOWN",
    }:
        return explicit
    interactions_value: object = manifest.get("ai_interactions", [])
    interactions: list[Any] = []
    if isinstance(interactions_value, list):
        interactions.extend(
            interactions_value  # pyright: ignore[reportUnknownArgumentType]
        )
    if not interactions and isinstance(manifest.get("ai_model_provenance"), dict):
        interactions = [{"model_provenance": manifest["ai_model_provenance"]}]
    if not interactions:
        return "NONE"
    network_mode = str(manifest.get("network_mode", "")).upper()
    for interaction in interactions:
        if not isinstance(interaction, dict):
            continue
        interaction_data = cast(dict[str, Any], interaction)
        provenance_value: Any = interaction_data.get("model_provenance", {})
        provenance = (
            cast(dict[str, Any], provenance_value)
            if isinstance(provenance_value, dict)
            else {}
        )
        if provenance:
            provider = str(
                provenance.get("provider", provenance.get("backend", ""))
            ).lower()
            if "replay" in provider or provenance.get("replay") is True:
                return "REPLAY"
            if network_mode in {"OFFLINE", "FROZEN_CORPUS"} and (
                provider in {"ollama", "local", "frozen_model"} or "frozen" in provider
            ):
                return "LIVE_FROZEN_MODEL"
            if network_mode == "LIVE_NETWORK" or (
                provider and provider not in {"unknown", "not_reported"}
            ):
                return "LIVE_EXTERNAL_API"
    return "UNKNOWN"


def classify_research_operation_status(manifest: dict[str, Any]) -> str:
    """Classify the scientific AI operating status for read-only display."""
    exposure = str(manifest.get("ai_exposure", "")).lower()
    taint = str(manifest.get("causal_taint", "")).upper()
    if exposure == "none" and taint == "PURE":
        return "PURE EXPERIMENT"
    if taint == "AI_INFLUENCED" or exposure in {
        "bounded_controller",
        "adaptive_controller",
    }:
        return "AI CAUSALLY ACTIVE"
    if taint == "PROPOSED" or exposure == "advisor":
        return "AI PROPOSING"
    if taint == "OBSERVED" or exposure in {"observer_only", "semantic_interface"}:
        return "AI OBSERVING"
    return "UNKNOWN"


def _experiment_date_from_id(experiment_id: str) -> str | None:
    """Infer an ISO date only when the experiment ID carries YYYYMMDD explicitly."""
    match = re.search(r"(20\d{6})(?:$|[-_])", experiment_id)
    if match is None:
        return None
    raw = match.group(1)
    return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"


def normalize_experiment_manifest(
    directory: Path, manifest: dict[str, Any]
) -> dict[str, Any]:
    """Project heterogeneous immutable manifests into one dashboard read model.

    The returned mapping is a copy. Canonical experiment files are never rewritten.
    This keeps older workflow manifests and newer source-bound experiment packages
    equally reviewable in the dashboard.
    """
    normalized = dict(manifest)
    experiment_id = str(
        normalized.get("experiment_id") or directory.name
    )
    normalized.setdefault("experiment_id", experiment_id)

    if not isinstance(normalized.get("research_questions"), list):
        question = normalized.get("research_question")
        if isinstance(question, str) and question:
            normalized["research_questions"] = [question]
    if not isinstance(normalized.get("hypotheses"), list):
        hypothesis = normalized.get("hypothesis")
        if isinstance(hypothesis, str) and hypothesis:
            normalized["hypotheses"] = [hypothesis]

    if not normalized.get("created_at"):
        timestamp = normalized.get("timestamp") or normalized.get("timestamp_utc")
        if isinstance(timestamp, str) and timestamp:
            normalized["created_at"] = timestamp
        else:
            inferred = _experiment_date_from_id(experiment_id)
            if inferred is not None:
                normalized["created_at"] = inferred

    if not normalized.get("experiment_status"):
        status = normalized.get("status")
        if isinstance(status, str) and status:
            normalized["experiment_status"] = status
        elif isinstance(normalized.get("results"), dict):
            result_status = cast(dict[str, Any], normalized["results"]).get("status")
            if isinstance(result_status, str) and result_status:
                normalized["experiment_status"] = (
                    "completed"
                    if result_status
                    in {
                        "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL",
                        "NO_PREDEFINED_TOPOLOGY_DIFFERENCE_DETECTED",
                    }
                    else result_status.lower()
                )

    existing_artifacts = normalized.get("artifacts")
    artifacts: dict[str, Any] = (
        dict(cast(dict[str, Any], existing_artifacts))
        if isinstance(existing_artifacts, dict)
        else {}
    )
    inferred_artifacts = {
        "report": "report.md",
        "summary": "summary.md",
        "statistics": "analysis/statistics.json",
        "raw_data": "data/evaluation.json",
        "calibration": "data/calibration.json",
        "review": "review_request.json",
        "manifest": "manifest.json",
        "checksums": "checksums.sha256",
    }
    for key, relative in inferred_artifacts.items():
        if key not in artifacts and (directory / relative).is_file():
            artifacts[key] = relative
    if artifacts:
        normalized["artifacts"] = artifacts

    results = normalized.get("results")
    if isinstance(results, dict):
        result_status = cast(dict[str, Any], results).get("status")
        if isinstance(result_status, str) and result_status:
            normalized.setdefault("scientific_status", result_status)
    return normalized


class ResearchSource:
    """Read-only view over the ``research/`` directory tree.

    Categories:
        registry   — YAML registry files (questions, hypotheses, ...)
        generated  — auto-generated markdown reports
        experiments — experiment manifests
        literature  — BibTeX databases
        schemas     — JSON schemas
    """

    _CATEGORIES: tuple[str, ...] = (
        "registry",
        "generated",
        "experiments",
        "reports",
        "analysis",
        "benchmarks",
        "literature",
        "publications",
        "schemas",
        "external_review",
        "ethics",
    )

    def __init__(self, research_root: Path) -> None:
        self._root = research_root.resolve()
        self._documents_cache: list[ResearchDocument] | None = None
        self._documents_cache_time: float = 0.0
        self._cache_ttl: float = 5.0  # Sekunden

    def is_available(self) -> bool:
        """Return True when the research root exists and is a directory."""
        return self._root.is_dir()

    def root(self) -> Path:
        return self._root

    def _invalidate_cache(self) -> None:
        """Force cache refresh on next call."""
        self._documents_cache = None
        self._documents_cache_time = 0.0

    def list_documents(self, max_count: int = 0) -> list[ResearchDocument]:
        """List research artifacts grouped by category, with caching.

        Args:
            max_count: Maximum number of documents to return.
                       0 = return all (uncached behavior).

        Returns:
            Sorted list of ResearchDocument objects.
        """
        now = time.monotonic()
        # Use cache only when requesting all documents
        if max_count == 0 and self._documents_cache is not None:
            if now - self._documents_cache_time < self._cache_ttl:
                return self._documents_cache

        if not self.is_available():
            return []

        documents: list[ResearchDocument] = []
        for category in self._CATEGORIES:
            directory = self._root / category
            if not directory.is_dir():
                continue
            for entry in sorted(directory.rglob("*")):
                if not entry.is_file():
                    continue
                rel = entry.relative_to(self._root)
                documents.append(
                    ResearchDocument(
                        name=entry.name,
                        path=str(rel).replace("\\", "/"),
                        kind=entry.suffix.lstrip(".") or "file",
                        size_bytes=entry.stat().st_size,
                        category=category,
                    )
                )
                # Early exit when max_count is set and reached
                if max_count > 0 and len(documents) >= max_count:
                    break
            if max_count > 0 and len(documents) >= max_count:
                break

        if max_count == 0:
            self._documents_cache = documents
            self._documents_cache_time = now

        return documents

    def read_content(self, relative_path: str) -> str:
        """Read a research file as UTF-8 text with path-traversal protection."""
        resolved = self._safe_resolve(relative_path)
        if resolved is None:
            raise FileNotFoundError(f"Research document not found: {relative_path}")
        return resolved.read_text(encoding="utf-8")

    def read_bytes(self, relative_path: str) -> bytes:
        resolved = self._safe_resolve(relative_path)
        if resolved is None:
            raise FileNotFoundError(f"Research document not found: {relative_path}")
        return resolved.read_bytes()

    def registry_summary(self) -> dict[str, JSONValue]:
        """Return a compact summary of registry counts for the dashboard."""
        summary: dict[str, JSONValue] = {
            "available": self.is_available(),
            "root": str(self._root),
            "categories": {},
        }
        if not self.is_available():
            return summary
        counts: dict[str, JSONValue] = {}
        for category in self._CATEGORIES:
            directory = self._root / category
            if directory.is_dir():
                counts[category] = sum(
                    1 for entry in directory.rglob("*") if entry.is_file()
                )
            else:
                counts[category] = 0
        summary["categories"] = counts
        return summary

    def generated_reports(self) -> list[dict[str, JSONValue]]:
        """List auto-generated markdown reports with metadata."""
        directory = self._root / "generated"
        if not directory.is_dir():
            return []
        reports: list[dict[str, JSONValue]] = []
        for entry in sorted(directory.glob("*.md")):
            reports.append(
                {
                    "name": entry.stem,
                    "path": str(entry.relative_to(self._root)).replace("\\", "/"),
                    "size_bytes": entry.stat().st_size,
                }
            )
        return reports

    def ai_reports(
        self, experiment_id: str | None = None
    ) -> list[dict[str, JSONValue]]:
        """List canonical AIRR JSON/Markdown pairs without exposing write access."""
        reports: list[dict[str, JSONValue]] = []
        directories = [
            directory
            for directory in (self._root / "experiments").glob("*/reports")
            if directory.is_dir()
        ]
        legacy_directory = self._root / "reports"
        if legacy_directory.is_dir():
            directories.append(legacy_directory)
        for directory in directories:
            current_experiment = directory.parent.name
            for entry in sorted(directory.glob("AIRR-*.json")):
                if entry.name.endswith(".review.json"):
                    continue
                reports.append(
                    {
                        "report_id": entry.stem,
                        "experiment_id": current_experiment,
                        "json_path": str(entry.relative_to(self._root)).replace(
                            "\\", "/"
                        ),
                        "markdown_path": str(
                            entry.with_suffix(".md").relative_to(self._root)
                        ).replace("\\", "/"),
                        "size_bytes": entry.stat().st_size,
                    }
                )
        if experiment_id is not None:
            reports = [
                report for report in reports if report["experiment_id"] == experiment_id
            ]
        return reports

    def experiment_manifest(self, experiment_id: str) -> dict[str, JSONValue] | None:
        """Load one experiment manifest.json if present."""
        candidate = self._root / "experiments" / experiment_id / "manifest.json"
        if not candidate.is_file():
            return None
        try:
            data: Any = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return data  # type: ignore[no-any-return]

    def _work_view_archived_ids(self) -> frozenset[str]:
        """Read the optional metadata-only archive index without mutating it."""
        index = self._root / "archive" / "experiment_index.json"
        if not index.is_file():
            return frozenset()
        try:
            payload: object = json.loads(index.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return frozenset()
        if not isinstance(payload, dict):
            return frozenset()
        experiments = cast(dict[object, object], payload).get("experiments", {})
        if not isinstance(experiments, dict):
            return frozenset()
        return frozenset(str(key) for key in cast(dict[object, object], experiments))

    def list_experiments(self) -> list[dict[str, JSONValue]]:
        """List experiments visible in the work view or retained for publication traceability.

        Metadata-archived ordinary experiments are hidden from the active work view.
        Published campaign indexes remain navigable even when archived because their
        manifests carry the scientific validity/evidence boundary used by historical
        publications. Keeping them visible does not promote them to evidence.
        """
        directory = self._root / "experiments"
        if not directory.is_dir():
            return []
        hidden = self._work_view_archived_ids()
        experiments: list[dict[str, JSONValue]] = []
        for entry in directory.iterdir():
            manifest = entry / "manifest.json"
            if not manifest.is_file():
                continue
            try:
                data: Any = json.loads(manifest.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            manifest_data = (
                cast(dict[str, Any], data) if isinstance(data, dict) else None
            )
            record_kind = (
                str(manifest_data.get("record_kind", ""))
                if manifest_data is not None
                else ""
            )
            if entry.name in hidden and record_kind != "campaign_index":
                continue
            dashboard_manifest = (
                normalize_experiment_manifest(entry, manifest_data)
                if manifest_data is not None
                else None
            )
            created_at = (
                str(dashboard_manifest.get("created_at"))
                if dashboard_manifest is not None
                and dashboard_manifest.get("created_at")
                else None
            )
            experiments.append(
                {
                    "ai_operation_mode": (
                        classify_ai_operation(manifest_data)
                        if manifest_data is not None
                        else "NONE"
                    ),
                    "research_operation_status": (
                        classify_research_operation_status(manifest_data)
                        if manifest_data is not None
                        else "UNKNOWN"
                    ),
                    "id": entry.name,
                    "created_at": created_at,
                    "path": str(entry.relative_to(self._root)).replace("\\", "/"),
                    "manifest": dashboard_manifest if dashboard_manifest is not None else data,
                }
            )
        experiments.sort(
            key=lambda item: str(item.get("created_at") or ""), reverse=True
        )
        return experiments

    def _safe_resolve(self, relative_path: str) -> Path | None:
        if not relative_path or ".." in relative_path:
            return None
        candidate = (self._root / relative_path).resolve()
        try:
            candidate.relative_to(self._root)
        except ValueError:
            return None
        if not candidate.is_file():
            return None
        return candidate


def create_research_source(research_root: Path | None) -> ResearchSource | None:
    """Create a ResearchSource if the root exists, else None."""
    if research_root is None or not research_root.exists():
        return None
    return ResearchSource(research_root)
