#!/usr/bin/env python3
"""Fail closed on cross-system scientific maturity and publication integrity.

This checker validates internal consistency only. It does not certify
plagiarism-freedom, scientific validity, peer review, novelty, or biological
equivalence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
V18 = "research/publications/2026-09-17_recursive-epistemics_v1.8"
V17 = "research/publications/2026-09-15_recursive-epistemics_v1.7"
V16 = "research/publications/2026-09-15_recursive-epistemics_v1.6"
V15 = "research/publications/2026-09-13_recursive-epistemics_v1.5"


def load_json(path: str) -> dict[str, Any]:
    value = json.loads((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path}: expected JSON object")
    return value


def main() -> int:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    scientific = load_json("src/dashboard/static/scientific-progress.json")
    weights = scientific.get("weights", {})
    stages = scientific.get("stages", [])
    require(
        isinstance(weights, dict),
        "scientific-progress weights must be an object",
    )
    require(
        isinstance(stages, list),
        "scientific-progress stages must be a list",
    )
    if isinstance(weights, dict):
        expected_weights = {
            "research_question",
            "protocol",
            "data",
            "reviewed_evidence",
            "independent_replication",
            "attribution",
        }
        require(
            set(weights) == expected_weights,
            "scientific-progress weights changed without contract update",
        )
        total_weight = sum(float(value) for value in weights.values())
        require(
            abs(total_weight - 1.0) < 1e-9,
            "scientific-progress weights must sum to 1",
        )

    if isinstance(stages, list):
        stage_numbers = [
            stage.get("stage") for stage in stages if isinstance(stage, dict)
        ]
        require(
            stage_numbers == list(range(11)),
            "scientific-progress must cover stages 0 through 10 exactly once",
        )
        for stage in stages:
            if not isinstance(stage, dict):
                errors.append("scientific-progress stage is not an object")
                continue
            stage_no = stage.get("stage")
            score = float(stage.get("score", -1))
            require(
                0.0 <= score <= 1.0,
                f"stage {stage_no} score out of range",
            )
            require(
                bool(stage.get("claim_boundary")),
                f"stage {stage_no} missing claim boundary",
            )
            criteria = stage.get("criteria")
            require(
                isinstance(criteria, list) and bool(criteria),
                f"stage {stage_no} missing scientific criteria",
            )

        stage6 = next(
            (
                stage
                for stage in stages
                if isinstance(stage, dict) and stage.get("stage") == 6
            ),
            None,
        )
        require(stage6 is not None, "stage 6 missing")
        if isinstance(stage6, dict):
            boundary = str(stage6.get("claim_boundary", "")).lower()
            require(
                "keine semantization" in boundary,
                "stage 6 must deny completed semantization",
            )
            require(
                "kein hierarchisches predictive coding" in boundary,
                "stage 6 must deny completed hierarchical predictive coding",
            )
            require(
                "kein generatives weltmodell" in boundary,
                "stage 6 must deny a completed generative world model",
            )

    catalog = load_json("research/publications/catalog.json")
    publications = catalog.get("publications", [])
    current = [
        item for item in publications if isinstance(item, dict) and item.get("current")
    ]
    require(
        len(current) == 1,
        "publication catalog must have exactly one current edition",
    )
    if len(current) == 1:
        item = current[0]
        require(
            item.get("version") == "1.8",
            "current publication must be edition 1.8",
        )
        require(
            item.get("edition_status") == "current_wip",
            "edition 1.7 must be visibly marked current_wip",
        )
        require(
            item.get("entrypoint", "").endswith("v1.8/MANUSCRIPT.md"),
            "Publication Viewer must open the current v1.8 manuscript",
        )
        require(
            item.get("automatic_evidence_promotion") is False,
            "current publication must not auto-promote evidence",
        )
        require(
            item.get("predecessor") == "PUB-RECURSIVE-EPISTEMICS-20260915-V1.7",
            "edition 1.8 predecessor mismatch",
        )
        require(
            item.get("inherits_empirical_edition")
            == "PUB-RECURSIVE-EPISTEMICS-20260913-V1.5",
            "edition 1.7 must retain edition 1.5 empirical provenance",
        )
        require(
            catalog.get("current_publication_id") == item.get("id"),
            "current_publication_id mismatch",
        )
        require(
            catalog.get("current_publication") == item.get("id"),
            "current_publication mismatch",
        )
    require(
        catalog.get("frozen_empirical_baseline")
        == "PUB-RECURSIVE-EPISTEMICS-20260913-V1.5",
        "frozen 1.5 baseline pointer missing",
    )

    v17 = load_json(f"{V17}/manifest.json")
    require(
        v17.get("historical_data_modified") is False,
        "v1.7 may not rewrite historical data",
    )
    require(
        v17.get("accepted_evidence") is False,
        "v1.7 may not manufacture accepted evidence",
    )
    require(
        v17.get("automatic_evidence_promotion") is False,
        "v1.7 may not auto-promote evidence",
    )
    require(
        v17.get("inherited_campaign") == "EXP-EMP-20260913-A3",
        "v1.7 campaign provenance mismatch",
    )
    require(
        v17.get("predecessor_edition", "").endswith("v1.6"),
        "v1.7 predecessor edition missing",
    )
    require(
        v17.get("viewer_entrypoint") == "MANUSCRIPT.md",
        "v1.7 manifest viewer entrypoint mismatch",
    )

    v16 = load_json(f"{V16}/manifest.json")
    require(
        v16.get("historical_data_modified") is False,
        "v1.6 provenance must remain intact",
    )
    require(
        v16.get("accepted_evidence") is False,
        "v1.6 may not manufacture accepted evidence",
    )
    require(
        (ROOT / V15 / "manifest.json").is_file(),
        "frozen 1.5 manifest is missing",
    )
    require(
        (ROOT / "research/publications/FROZEN_V1.5.md").is_file(),
        "stable frozen 1.5 entrypoint is missing",
    )
    require(
        (ROOT / "research/publications/CURRENT.md").is_file(),
        "stable current publication pointer is missing",
    )

    identity = load_json("project_identity.json")
    publication = identity.get("publication", {})
    scope = identity.get("scientific_scope", {})
    governance = identity.get("document_governance", {})
    require(
        isinstance(publication, dict) and publication.get("edition") == "1.8",
        "project identity publication edition mismatch",
    )
    require(
        isinstance(publication, dict)
        and publication.get("edition_status") == "current_wip",
        "project identity must expose WIP status",
    )
    require(
        isinstance(scope, dict)
        and scope.get("engineering_maturity_is_scientific_evidence") is False,
        "engineering/science boundary missing",
    )
    require(
        isinstance(scope, dict)
        and scope.get("scientific_maturity_is_consciousness_metric") is False,
        "scientific score must not be a consciousness metric",
    )
    require(
        isinstance(scope, dict)
        and scope.get("candidate_contribution_novelty") == "requires_prior_art_review",
        "novelty uncertainty boundary missing",
    )
    require(
        isinstance(governance, dict)
        and governance.get("audit") == "scripts/audit_document_governance.py",
        "document governance audit is not registered",
    )

    required_files = [
        "research/INTEGRITY_AND_ATTRIBUTION.md",
        "research/RELATED_WORK.md",
        "research/CURRENT_SCIENTIFIC_STATE.md",
        "docs/00-governance/DOCUMENT_GOVERNANCE.md",
        "docs/05-quality/RESEARCH_INTEGRITY_GATE.md",
        "docs/08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md",
        "research/document_governance_overrides.json",
        "scripts/audit_document_governance.py",
        f"{V18}/MANUSCRIPT.md",
        f"{V17}/MANUSCRIPT.md",
        f"{V17}/FORSCHUNGSBERICHT.md",
        f"{V17}/AUTHOR_POSITION.md",
        f"{V17}/CONTRIBUTION_MAP.md",
        f"{V17}/SCIENTIFIC_STAGE_MATRIX.md",
        f"{V17}/INTEGRITY_AND_ATTRIBUTION.md",
        f"{V17}/REFERENCES.md",
        f"{V17}/WORK_IN_PROGRESS.md",
    ]
    for path in required_files:
        require(
            (ROOT / path).is_file(),
            f"missing required scientific-integrity file: {path}",
        )

    integrity_path = ROOT / "research/INTEGRITY_AND_ATTRIBUTION.md"
    integrity = integrity_path.read_text(encoding="utf-8").lower()
    related = (ROOT / "research/RELATED_WORK.md").read_text(encoding="utf-8")
    manuscript = (ROOT / V18 / "MANUSCRIPT.md").read_text(encoding="utf-8").lower()
    author_position = (
        (ROOT / V17 / "AUTHOR_POSITION.md").read_text(encoding="utf-8").lower()
    )
    plain_integrity = integrity.replace("**", "").replace("__", "")
    require(
        "does not certify" in plain_integrity,
        "integrity policy must refuse plagiarism certification",
    )
    require(
        "human source review" in plain_integrity,
        "integrity policy must require human source review",
    )
    require(
        "ArithSpec" in related and "QUARANTINED" in related,
        "unverified ArithSpec claim must remain quarantined",
    )
    require(
        "frozen 1.5" in manuscript,
        "current manuscript must identify frozen 1.5",
    )
    require(
        "neuheit" in manuscript and "prior-art" in manuscript,
        "current manuscript must expose novelty uncertainty",
    )
    require(
        "freier wissenstransfer" in author_position
        and "attribution" in author_position,
        "author position must preserve the knowledge-transfer/attribution distinction",
    )

    if errors:
        print("Scientific maturity/integrity gate: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Scientific maturity/integrity gate: PASS")
    print(
        "Internal consistency verified; no claim of plagiarism-freedom, novelty, "
        "or scientific acceptance is made."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
