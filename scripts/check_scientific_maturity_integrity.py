#!/usr/bin/env python3
"""Fail closed on the cross-system scientific maturity/integrity contract.

This checker validates internal consistency only.  It does not certify
plagiarism-freedom, scientific validity, peer review, or biological equivalence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


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
    require(isinstance(weights, dict), "scientific-progress weights must be an object")
    require(isinstance(stages, list), "scientific-progress stages must be a list")
    if isinstance(weights, dict):
        require(
            set(weights)
            == {
                "research_question",
                "protocol",
                "data",
                "reviewed_evidence",
                "independent_replication",
                "attribution",
            },
            "scientific-progress weights changed without contract update",
        )
        require(
            abs(sum(float(value) for value in weights.values()) - 1.0) < 1e-9,
            "scientific-progress weights must sum to 1",
        )
    if isinstance(stages, list):
        require(
            [stage.get("stage") for stage in stages if isinstance(stage, dict)]
            == list(range(11)),
            "scientific-progress must cover stages 0 through 10 exactly once",
        )
        for stage in stages:
            if not isinstance(stage, dict):
                errors.append("scientific-progress stage is not an object")
                continue
            score = float(stage.get("score", -1))
            require(0.0 <= score <= 1.0, f"stage {stage.get('stage')} score out of range")
            require(bool(stage.get("claim_boundary")), f"stage {stage.get('stage')} missing claim boundary")
            require(
                isinstance(stage.get("criteria"), list) and bool(stage.get("criteria")),
                f"stage {stage.get('stage')} missing scientific criteria",
            )

        stage6 = next(
            (stage for stage in stages if isinstance(stage, dict) and stage.get("stage") == 6),
            None,
        )
        require(stage6 is not None, "stage 6 missing")
        if isinstance(stage6, dict):
            boundary = str(stage6.get("claim_boundary", "")).lower()
            require("keine semantization" in boundary, "stage 6 must deny completed semantization")
            require(
                "kein hierarchisches predictive coding" in boundary,
                "stage 6 must deny completed hierarchical predictive coding",
            )
            require("kein generatives weltmodell" in boundary, "stage 6 must deny a completed generative world model")

    catalog = load_json("research/publications/catalog.json")
    publications = catalog.get("publications", [])
    current = [item for item in publications if isinstance(item, dict) and item.get("current")]
    require(len(current) == 1, "publication catalog must have exactly one current edition")
    if len(current) == 1:
        item = current[0]
        require(item.get("version") == "1.6", "current publication must be edition 1.6")
        require(item.get("automatic_evidence_promotion") is False, "current publication must not auto-promote evidence")
        require(
            item.get("inherits_empirical_edition") == "PUB-RECURSIVE-EPISTEMICS-20260913-V1.5",
            "edition 1.6 must retain edition 1.5 as empirical provenance",
        )
        require(catalog.get("current_publication_id") == item.get("id"), "current_publication_id mismatch")
        require(catalog.get("current_publication") == item.get("id"), "current_publication mismatch")

    v16 = load_json("research/publications/2026-09-15_recursive-epistemics_v1.6/manifest.json")
    require(v16.get("historical_data_modified") is False, "v1.6 may not rewrite historical data")
    require(v16.get("accepted_evidence") is False, "v1.6 may not manufacture accepted evidence")
    require(v16.get("automatic_evidence_promotion") is False, "v1.6 may not auto-promote evidence")
    require(v16.get("inherited_campaign") == "EXP-EMP-20260913-A3", "v1.6 campaign provenance mismatch")

    identity = load_json("project_identity.json")
    publication = identity.get("publication", {})
    scope = identity.get("scientific_scope", {})
    require(isinstance(publication, dict) and publication.get("edition") == "1.6", "project identity publication edition mismatch")
    require(isinstance(scope, dict) and scope.get("engineering_maturity_is_scientific_evidence") is False, "engineering/science boundary missing")
    require(isinstance(scope, dict) and scope.get("scientific_maturity_is_consciousness_metric") is False, "scientific score must not be a consciousness metric")

    release = load_json("releases/current.json")
    maturity = release.get("scientific_maturity", {})
    require(isinstance(maturity, dict) and maturity.get("separate_from_engineering") is True, "current release must expose a separate scientific maturity axis")
    require(isinstance(maturity, dict) and maturity.get("automatic_evidence_promotion") is False, "release scientific maturity must not auto-promote evidence")
    require(isinstance(maturity, dict) and maturity.get("consciousness_metric") is False, "release scientific maturity must not be a consciousness metric")

    required_files = [
        "research/INTEGRITY_AND_ATTRIBUTION.md",
        "research/RELATED_WORK.md",
        "research/CURRENT_SCIENTIFIC_STATE.md",
        "docs/05-quality/RESEARCH_INTEGRITY_GATE.md",
        "docs/08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md",
        "research/publications/2026-09-15_recursive-epistemics_v1.6/MANUSCRIPT.md",
        "research/publications/2026-09-15_recursive-epistemics_v1.6/FORSCHUNGSBERICHT.md",
        "research/publications/2026-09-15_recursive-epistemics_v1.6/SCIENTIFIC_STAGE_MATRIX.md",
    ]
    for path in required_files:
        require((ROOT / path).is_file(), f"missing required scientific-integrity file: {path}")

    integrity = (ROOT / "research/INTEGRITY_AND_ATTRIBUTION.md").read_text(encoding="utf-8").lower()
    related = (ROOT / "research/RELATED_WORK.md").read_text(encoding="utf-8")
    require("does not certify" in integrity, "integrity policy must refuse plagiarism certification")
    require("human source review" in integrity, "integrity policy must require human source review")
    require("ArithSpec" in related and "QUARANTINED" in related, "unverified ArithSpec claim must remain quarantined")

    if errors:
        print("Scientific maturity/integrity gate: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Scientific maturity/integrity gate: PASS")
    print("Internal consistency verified; no claim of plagiarism-freedom or scientific acceptance is made.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
