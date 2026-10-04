"""Release registry consistency and historical boundary tests."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]


def _release(name: str) -> dict[str, Any]:
    return cast(
        dict[str, Any],
        json.loads((ROOT / "releases" / name).read_text(encoding="utf-8")),
    )


def test_current_release_matches_canonical_published_version() -> None:
    with (ROOT / "pyproject.toml").open("rb") as stream:
        project = tomllib.load(stream)["project"]
    current = _release("current.json")

    assert project["version"] == "0.6.0a7"
    assert current["version"] == "0.6.0-alpha.7"
    assert current["pep440"] == project["version"]
    assert current["status"] == "release_candidate"
    assert current.get("release_type") == "pre-release"
    assert current.get("target_tag") == "v0.6.0-alpha.7"
    assert current["parent"] == "v0.6.0-alpha.6"
    assert current["as_of"] == "2026-09-27"
    assert current["milestone_status"] in {
        "stage3_engineering_reached_scientific_maturity_separate",
        "engineering_release_candidate_scientific_programme_active",
        "public_repository_hardening_release_candidate",
        "alpha7_release_candidate_from_2026_09_27_develop",
        "alpha7_release_candidate_integrated_pending_source_freeze_and_tag",
    }
    assert current["release_blockers"] == 0
    assert current["open"]
    assert current["scope"]
    assert any("release-only main" in item for item in current["scope"])
    assert any("repository-health" in item for item in current["scope"])
    assert any("Stage-6 semanticization" in item for item in current["open"])
    assert not any(
        "add registered delayed-information control runs" in item
        for item in current["open"]
    )
    assert "scientific EVID" in current["research_boundary"]
    assert current["scientific_maturity"]["automatic_evidence_promotion"] is False


def test_zenodo_archive_is_bound_to_alpha6_not_pending_alpha7() -> None:
    identity = json.loads((ROOT / "project_identity.json").read_text(encoding="utf-8"))
    alpha6 = _release("v0.6.0-alpha.6.json")
    current = _release("current.json")

    assert identity["platforms"]["zenodo"] == {
        "integration": "github_release_archive",
        "metadata_file": ".zenodo.json",
        "source_repository": "https://github.com/Thomas-Heisig/MHRN",
        "record_url": "https://zenodo.org/records/22860683",
        "doi": "10.5281/zenodo.22860683",
        "concept_doi": "10.5281/zenodo.22860682",
        "record_version": "0.6.0-alpha.6",
        "status": "published_verified",
        "creator_orcid": "0009-0002-9589-1872",
    }
    assert alpha6["publication_state"]["zenodo"] == "published_verified"
    assert alpha6["publication_state"]["doi"] == "10.5281/zenodo.22860683"
    assert current["publication_state"]["zenodo"] == "awaiting_github_release_archive"
    assert current["publication_state"]["doi"] is None


def test_alpha6_release_preserves_verified_historical_boundary() -> None:
    release = _release("v0.5.0-alpha.6.json")

    assert release["status"] == "released"
    assert release["tag"] == "v0.5.0-alpha.6"
    assert release["source_freeze"] == ("3025e681a5f46bfd8dc2e5dbb8e1474fa5132cd1")
    assert release["evidence_commit"] == ("70a4ee253a5fc30716d0ffe0058f146a1ad59cde")
    assert release["closure_commit"] == ("8fac75da723b4b9d28383dd4ec49497771f4572f")
    assert release["baseline"] == {
        "python": "3.13.14",
        "passed": 489,
        "failed": 0,
        "skipped": 5,
        "collection_errors": 0,
        "command": "python -m pytest tests/ -q --tb=short",
        "artifact": "tests/test_baseline.json",
    }
    assert [run["run"] for run in release["continuous_integration"]] == [
        145,
        147,
        148,
    ]
    assert release["gate_summary"]["scientific_gate"] == "passed"
    assert release["gate_summary"]["release_readiness"] == "ready"
