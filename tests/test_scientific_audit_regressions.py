"""Fail-closed scientific verification and bounded document-cache regressions."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from scripts import run_stage3_reference as reference
from scripts.empirical_campaign import encode, sha, validate_rows, verified_result
from src.dashboard.docs_source import DocumentationSource
from tests.dashboard_assets import stylesheet_paths


def test_document_cache_does_not_reenter_public_dispatch(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("A source document")
    source = DocumentationSource(tmp_path)
    first = source.list_documents()
    assert len(first) == 1
    assert source.list_documents() is first
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "other.md").write_text("Another source")
    source.invalidate_cache()
    assert len(source.list_documents(recursive=True)) == 2
    assert len(source.list_documents(recursive=True, max_count=1)) == 1
    with pytest.raises(FileNotFoundError):
        source.read_content("../escape.md")


def test_skipped_stage3_tests_cannot_be_verified() -> None:
    report = reference.build_report(run_tests=False)
    assert report["status"] == "incomplete"
    assert not report["tests_executed"]
    assert all(group["passed"] is None for group in report["test_groups"].values())


def test_stage3_verification_invokes_every_test_group(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, ...]] = []

    def passed(paths: tuple[str, ...]) -> bool:
        calls.append(paths)
        return True

    monkeypatch.setattr(reference, "_run_test_group", passed)
    report = reference.build_report(run_tests=True)
    assert report["status"] == "verified"
    assert calls == list(reference.TEST_GROUPS.values())
    monkeypatch.setattr(reference, "_run_test_group", lambda paths: False)
    assert reference.build_report(run_tests=True)["status"] == "failed"


def test_campaign_seed_coverage_rejects_partial_observation() -> None:
    assert validate_rows([], [1, 2]) == ["empty_run_series"]
    assert validate_rows([{"condition": "on", "seed": 1}], [1, 2]) == [
        "seed_coverage:on"
    ]
    assert (
        validate_rows(
            [{"condition": "on", "seed": 1}, {"condition": "on", "seed": 2}], [1, 2]
        )
        == []
    )


def test_campaign_analysis_rejects_tampered_data(tmp_path: Path) -> None:
    spec = {"protocol": "audit-fixture"}
    result = {"protocol": "audit-fixture", "status": "completed", "runs": []}
    raw = encode(result)
    packed = gzip.compress(raw, mtime=0)
    (tmp_path / "runs.json.gz").write_bytes(packed)
    receipt = {
        "protocol": "audit-fixture",
        "status": "completed",
        "run_count": 0,
        "compressed_data_sha256": sha(packed),
        "uncompressed_data_sha256": sha(raw),
    }
    (tmp_path / "receipt.json").write_text(json.dumps(receipt))
    assert verified_result(tmp_path, spec) == result
    (tmp_path / "runs.json.gz").write_bytes(packed + b"tampered")
    with pytest.raises(ValueError, match="digest mismatch"):
        verified_result(tmp_path, spec)


def test_dashboard_loaded_stylesheet_graph_is_complete() -> None:
    paths = stylesheet_paths()
    assert paths
    assert len(paths) == len(set(paths))
    assert any(path.name == "workspace-architecture.css" for path in paths)
    assert all(path.is_file() for path in paths)
