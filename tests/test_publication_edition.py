"""Regression tests for edition 1.8 provenance and deterministic publication build."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from scripts import build_publication_edition as publication

ROOT = Path(__file__).resolve().parents[1]


def write(root: Path, path: str, text: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "user.email", "test@example.invalid"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "user.name", "Fixture"], check=True
    )
    write(
        tmp_path,
        publication.PREVIOUS + "/MANUSCRIPT.md",
        "# Historical source\n\nOriginal.\n",
    )
    write(
        tmp_path,
        "research/registry/questions.yaml",
        "- id: RQ-FIXTURE-001\n  status: open\n  hypotheses: [H-FIXTURE-001-A]\n  question: Test?\n",
    )
    write(
        tmp_path,
        "research/registry/hypotheses.yaml",
        "- id: H-FIXTURE-001-A\n  status: untested\n  question: RQ-FIXTURE-001\n",
    )
    write(tmp_path, "research/publications/catalog.json", '{"publications": []}')
    write(tmp_path, "docs/unclassified.md", "# Retained idea\n\nNot discarded.\n")
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "-qm", "fixture baseline"], check=True
    )
    baseline = publication.git(tmp_path, "rev-parse", "HEAD").decode().strip()
    shutil.copytree(ROOT / publication.EDITION, tmp_path / publication.EDITION)
    write(
        tmp_path,
        "scripts/build_publication_edition.py",
        (ROOT / "scripts/build_publication_edition.py").read_text(encoding="utf-8"),
    )
    cfg = json.loads(
        (tmp_path / publication.EDITION / "edition.json").read_text(encoding="utf-8")
    )
    cfg["baseline_commit"] = baseline
    (tmp_path / publication.EDITION / "edition.json").write_text(
        publication.json_text(cfg), encoding="utf-8"
    )
    return tmp_path


def test_deterministic_build_and_no_evidence_promotion(repository: Path) -> None:
    first = publication.build(repository)
    assert first == publication.build(repository)
    assert set(first) == set(publication.OUTPUTS)
    publication.materialize(repository)
    assert publication.materialize(repository, check=True)["result"] == "PASS"
    manifest = json.loads(first["manifest.json"])
    assert manifest["accepted_evidence"] is False
    assert manifest["automatic_evidence_promotion"] is False
    assert manifest["complete_chat_archive_available"] is False


def test_historical_publication_mutation_or_deletion_fails(repository: Path) -> None:
    target = repository / publication.PREVIOUS / "MANUSCRIPT.md"
    target.write_text("changed", encoding="utf-8")
    with pytest.raises(ValueError, match="Historical publication changed"):
        publication.build(repository)
    target.unlink()
    with pytest.raises(ValueError, match="Historical publication changed"):
        publication.build(repository)


def test_stale_generated_output_fails(repository: Path) -> None:
    publication.materialize(repository)
    write(repository, publication.EDITION + "/MANUSCRIPT.md", "stale")
    with pytest.raises(ValueError, match="Stale/missing"):
        publication.materialize(repository, check=True)


def test_all_eleven_parts_required(repository: Path) -> None:
    path = repository / publication.EDITION / "edition.json"
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg["parts"] = cfg["parts"][:-1]
    path.write_text(publication.json_text(cfg), encoding="utf-8")
    with pytest.raises(ValueError, match="eleven"):
        publication.build(repository)


def test_registry_projection_preserves_source_object(repository: Path) -> None:
    objects = publication.registry_objects(repository)
    by_id = {item["id"]: item for item in objects}
    original = yaml.safe_load(
        (repository / "research/registry/questions.yaml").read_text(encoding="utf-8")
    )[0]
    assert by_id["RQ-FIXTURE-001"]["source_object"] == original
    assert by_id["RQ-FIXTURE-001"]["status"] == "open"
    assert by_id["H-FIXTURE-001-A"]["parent_ids"] == ["RQ-FIXTURE-001"]


def test_inventory_retains_unclassified_source_and_heading(repository: Path) -> None:
    outputs = publication.build(repository)
    census = json.loads(outputs["registers/source_inventory.json"])
    rows = {row["path"]: row for row in census["files"]}
    assert "docs/unclassified.md" in rows
    assert rows["docs/unclassified.md"]["publication_parts"] == ["XI"]
    sections = json.loads(outputs["registers/section_inventory.json"])["sections"]
    assert any(row["heading"] == "# Retained idea" for row in sections)


def test_unknown_citation_invalid_path_and_chat_promotion_fail(
    repository: Path,
) -> None:
    with pytest.raises(ValueError, match="Unknown"):
        publication.cite("Unsupported [@invented]", {})
    with pytest.raises(ValueError, match="Unsafe"):
        publication.inside(ROOT, "../outside")
    path = repository / publication.EDITION / "sources/chat_reconstruction.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["events"][0]["provenance_class"] = "S1"
    path.write_text(publication.json_text(data), encoding="utf-8")
    with pytest.raises(ValueError, match="Chat summaries"):
        publication.build(repository)


def test_publication_cannot_accept_evidence(repository: Path) -> None:
    path = repository / publication.EDITION / "sources/synthesis_claims.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data[0]["status"] = "accepted_EVID"
    path.write_text(publication.json_text(data), encoding="utf-8")
    with pytest.raises(ValueError, match="cannot accept evidence"):
        publication.build(repository)


def test_active_catalog_and_identity_are_consistent() -> None:
    catalog = publication.load(ROOT, "research/publications/catalog.json")
    current = [item for item in catalog["publications"] if item.get("current")]
    assert len(current) == 1
    assert current[0]["version"] == "1.8"
    assert current[0]["predecessor"].endswith("V1.7")
    assert current[0]["automatic_evidence_promotion"] is False
    identity = publication.load(ROOT, "project_identity.json")["publication"]
    assert identity["edition"] == "1.8"
    assert "research/" + current[0]["entrypoint"] == identity["viewer_entrypoint"]
    assert (ROOT / identity["viewer_entrypoint"]).is_file()
    assert publication.materialize(ROOT, check=True)["result"] == "PASS"
