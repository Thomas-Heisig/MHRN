#!/usr/bin/env python3
"""Classify every file below docs/ and research/ and fail on invalid governance.

The classifier is intentionally conservative: paths get a declared scientific
role, but classification never upgrades a document to accepted evidence.
Use --write to materialize the complete per-file catalogue for human review.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OVERRIDES = ROOT / "research/document_governance_overrides.json"
OUTPUTS = {
    "docs": ROOT / "docs/DOCUMENT_CATALOG.json",
    "research": ROOT / "research/RESEARCH_CATALOG.json",
}
SKIP = {
    "docs/DOCUMENT_CATALOG.json",
    "research/RESEARCH_CATALOG.json",
}


def _load_overrides() -> dict[str, dict[str, Any]]:
    payload = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    overrides = payload.get("overrides")
    if not isinstance(overrides, dict):
        raise ValueError(
            "document governance overrides must contain an object named overrides"
        )
    return {str(key).rstrip("/"): dict(value) for key, value in overrides.items()}


def _base(path: str) -> dict[str, Any]:
    return {
        "path": path,
        "domain": path.split("/", 1)[0],
        "kind": "documentation",
        "status": "current",
        "authority": "contextual_documentation",
        "mutability": "editable",
        "citation": "cite_exact_path_and_revision",
        "evidence_role": "not_evidence_by_itself",
        "rationale": (
            "Rule-classified repository documentation; exact scientific authority "
            "depends on referenced DATA/EVID."
        ),
    }


def _apply_prefix_override(
    path: str,
    item: dict[str, Any],
    overrides: dict[str, dict[str, Any]],
) -> None:
    matches = [
        prefix for prefix in overrides if path == prefix or path.startswith(prefix + "/")
    ]
    if not matches:
        return
    prefix = max(matches, key=len)
    item.update(overrides[prefix])
    item["classification_rule"] = f"override:{prefix}"


def _research_rule(path: str, item: dict[str, Any]) -> None:
    lower = path.lower()
    parts = path.split("/")
    top = parts[1] if len(parts) > 1 else ""

    normative = {
        "registry": (
            "registry",
            "normative_research_registry",
            "research_definition_not_evidence_by_itself",
        ),
        "schemas": ("schema", "normative_schema", "contract_not_evidence"),
        "protocols": (
            "protocol",
            "normative_protocol_or_method",
            "protocol_not_result",
        ),
        "ethics": (
            "ethics_policy",
            "normative_ethics_context",
            "policy_not_evidence",
        ),
        "critique": ("critique", "critical_analysis", "interpretation_only"),
        "literature": (
            "literature",
            "source_index",
            "external_source_provenance",
        ),
        "specifications": (
            "specification",
            "normative_design_contract",
            "contract_not_evidence",
        ),
        "preregistrations": (
            "preregistration",
            "frozen_or_versioned_experiment_plan",
            "preregistration_not_result",
        ),
        "benchmarks": (
            "benchmark",
            "benchmark_reference_or_method",
            "benchmark_definition_not_evidence_by_itself",
        ),
        "prompts": (
            "analysis_prompt",
            "analysis_method_configuration",
            "prompt_not_evidence",
        ),
        "frontiers": (
            "frontier_programme",
            "research_planning",
            "planning_only",
        ),
    }
    if top in normative:
        kind, authority, evidence_role = normative[top]
        item.update(kind=kind, authority=authority, evidence_role=evidence_role)
        item["classification_rule"] = f"research-zone:{top}"
        if top == "preregistrations":
            item.update(
                mutability="immutable_after_registration_or_versioned_replacement",
                citation="cite_preregistration_id_and_revision",
            )
        elif top == "frontiers":
            item.update(citation="cite_as_planning_not_result")
    elif top == "experiments":
        item.update(
            kind="experiment",
            status="experimental",
            authority="experiment_artifact",
            mutability="append_only_or_immutable_after_completion",
            citation="cite_experiment_id_path_digest",
            evidence_role="data_or_review_state_as_declared_by_manifest",
            rationale=(
                "Experimental artifact; execution and DATA do not automatically "
                "imply accepted EVID."
            ),
        )
        item["classification_rule"] = "research-zone:experiments"
    elif top == "workflows":
        item.update(
            kind="experiment_workflow",
            status="experimental",
            authority="workflow_execution_record",
            mutability="append_only_or_immutable_after_completion",
            citation="cite_workflow_or_experiment_id_and_revision",
            evidence_role="workflow_record_not_evidence_by_itself",
        )
        item["classification_rule"] = "research-zone:workflows"
    elif top == "proposals":
        item.update(
            kind="research_proposal",
            status="experimental",
            authority="proposal_only",
            citation="cite_as_proposal_not_result",
            evidence_role="proposal_not_evidence",
        )
        item["classification_rule"] = "research-zone:proposals"
    elif top == "generated":
        item.update(
            kind="generated",
            status="generated",
            authority="generated_projection",
            mutability="regenerable",
            citation="cite_underlying_source_not_projection_when_possible",
            evidence_role="projection_not_evidence_by_itself",
        )
        item["classification_rule"] = "research-zone:generated"
    elif top == "publications":
        item.update(
            kind="publication",
            status=(
                "historical"
                if "2026-09-15_recursive-epistemics_v1.7" not in path
                else "current_wip"
            ),
            authority="publication_interpretation",
            citation="cite_with_edition",
            evidence_role="interpretation_only",
        )
        item["classification_rule"] = "research-zone:publications"
    elif top in {"external_review", "reviews"}:
        item.update(
            kind="review",
            authority="human_or_external_review_record",
            evidence_role="review_state",
        )
        item["classification_rule"] = f"research-zone:{top}"
    elif top in {"data", "datasets", "raw", "artifacts"}:
        item.update(
            kind="data",
            status="experimental",
            authority="data_artifact",
            mutability="immutable_or_append_only",
            citation="cite_path_digest_and_origin",
            evidence_role="data_not_accepted_evidence_by_itself",
        )
        item["classification_rule"] = f"research-zone:{top}"
    else:
        item.update(
            kind="research_document",
            authority="research_context",
            evidence_role="interpretation_or_navigation",
        )
        item["classification_rule"] = "research-zone:top-level-context"

    if "/archive" in lower or "/archives" in lower or lower.endswith(
        (".zip", ".tar", ".gz")
    ):
        item.update(
            status="archive",
            mutability="immutable",
            citation="cite_archive_and_digest",
        )
        item["classification_rule"] += "+archive"
    if any(
        token in lower
        for token in ("historical", "legacy", "deprecated", "superseded")
    ):
        item.update(
            status="historical",
            authority="historical_context",
            evidence_role="historical_only",
        )
        item["classification_rule"] += "+historical-name"


def _docs_rule(path: str, item: dict[str, Any]) -> None:
    lower = path.lower()
    parts = path.split("/")
    top = parts[1] if len(parts) > 1 else ""
    zone_map = {
        "00-governance": (
            "governance",
            "normative_document_governance",
            "policy_not_evidence",
            "current",
        ),
        "01-guides": (
            "guide",
            "operator_or_developer_guidance",
            "not_evidence",
            "current",
        ),
        "02-architecture": (
            "architecture",
            "current_architecture_documentation",
            "design_contract_not_evidence",
            "current",
        ),
        "03-dashboard": (
            "dashboard_contract",
            "technical_interface_documentation",
            "contract_not_evidence",
            "current",
        ),
        "04-integration": (
            "integration_record",
            "historical_integration_context",
            "historical_only",
            "historical",
        ),
        "05-quality": (
            "quality_policy",
            "normative_quality_contract",
            "quality_contract_not_evidence",
            "current",
        ),
        "06-research": (
            "research_documentation",
            "research_context",
            "interpretation_only",
            "current",
        ),
        "07-changelog": (
            "changelog",
            "historical_change_record",
            "historical_only",
            "historical",
        ),
        "08-roadmap": (
            "roadmap",
            "planning",
            "planning_only",
            "current",
        ),
        "09-sprints": (
            "sprint_record",
            "historical_planning_record",
            "historical_only",
            "historical",
        ),
        "10-releases": (
            "release_record",
            "historical_release_provenance",
            "historical_only",
            "historical",
        ),
        "11-readme": (
            "historical_readme",
            "historical_context",
            "historical_only",
            "historical",
        ),
        "12-updates": (
            "update_record",
            "historical_change_record",
            "historical_only",
            "historical",
        ),
        "99-archive": (
            "archive",
            "archived_context",
            "historical_only",
            "archive",
        ),
    }
    if top in zone_map:
        kind, authority, evidence_role, status = zone_map[top]
        item.update(
            kind=kind,
            authority=authority,
            evidence_role=evidence_role,
            status=status,
        )
        item["classification_rule"] = f"docs-zone:{top}"
        if status == "archive":
            item.update(mutability="immutable", citation="cite_archive_and_digest")
        elif status == "historical":
            item.update(citation="cite_with_version_or_date")
    else:
        item.update(
            kind="documentation",
            authority="project_documentation",
            evidence_role="not_evidence_by_itself",
        )
        item["classification_rule"] = "docs-zone:top-level-context"

    if top == "08-roadmap":
        item.update(citation="cite_as_planning_not_result")
    if top == "06-research" and "/old/" in lower:
        item.update(
            status="historical",
            authority="historical_research_context",
            evidence_role="historical_only",
            citation="cite_as_historical_draft",
        )
        item["classification_rule"] += "+old"
    if top in {"01-guides", "03-dashboard", "06-research"} and any(
        token in lower
        for token in (
            "v040",
            "v050",
            "v0.5",
            "alpha4",
            "alpha5",
            "alpha7",
            "brain-5d",
            "geliehene_intelligenz",
        )
    ):
        item.update(
            status="historical",
            authority="historical_versioned_context",
            evidence_role="historical_only",
            citation="cite_with_version_and_date",
        )
        item["classification_rule"] += "+versioned-history"


def classify(path: str, overrides: dict[str, dict[str, Any]]) -> dict[str, Any]:
    item = _base(path)
    if path.startswith("research/"):
        _research_rule(path, item)
    elif path.startswith("docs/"):
        _docs_rule(path, item)
    else:
        raise ValueError(f"path outside governance scope: {path}")
    _apply_prefix_override(path, item, overrides)
    item.setdefault("classification_rule", "base")
    item["review_required"] = "top-level-context" in item["classification_rule"]
    return item


def inventory(
    domain: str,
    overrides: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    base = ROOT / domain
    files = []
    for file in sorted(path for path in base.rglob("*") if path.is_file()):
        rel = file.relative_to(ROOT).as_posix()
        if rel in SKIP:
            continue
        files.append(classify(rel, overrides))
    return files


def _validate(items: list[dict[str, Any]], errors: list[str]) -> None:
    required = {
        "path",
        "domain",
        "kind",
        "status",
        "authority",
        "mutability",
        "citation",
        "evidence_role",
        "rationale",
        "classification_rule",
    }
    valid_status = {
        "current",
        "current_wip",
        "frozen",
        "historical",
        "generated",
        "experimental",
        "superseded",
        "archive",
    }
    paths: set[str] = set()
    for item in items:
        missing = required - set(item)
        if missing:
            errors.append(f"{item.get('path')}: missing {sorted(missing)}")
        if item.get("status") not in valid_status:
            errors.append(f"{item.get('path')}: invalid status {item.get('status')!r}")
        path = str(item.get("path"))
        if path in paths:
            errors.append(f"duplicate catalogue path: {path}")
        paths.add(path)
        if item.get("evidence_role") == "accepted_evidence" and "EVID" not in path:
            errors.append(f"{path}: accepted evidence may not be inferred from location")


def _write(domain: str, items: list[dict[str, Any]]) -> None:
    summary = {
        "file_count": len(items),
        "status": dict(sorted(Counter(str(item["status"]) for item in items).items())),
        "kind": dict(sorted(Counter(str(item["kind"]) for item in items).items())),
        "authority": dict(
            sorted(Counter(str(item["authority"]) for item in items).items())
        ),
        "review_required": sum(bool(item.get("review_required")) for item in items),
    }
    payload = {
        "schema_version": 1,
        "generated_by": "scripts/audit_document_governance.py",
        "scope": domain,
        "warning": (
            "Classification describes document role; it does not promote DATA "
            "to EVID or certify scientific validity."
        ),
        "summary": summary,
        "files": items,
    }
    OUTPUTS[domain].write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="materialize complete per-file catalogues",
    )
    parser.add_argument(
        "--strict-review",
        action="store_true",
        help="fail if generic top-level contextual files remain",
    )
    args = parser.parse_args()

    overrides = _load_overrides()
    errors: list[str] = []
    all_items: dict[str, list[dict[str, Any]]] = {}
    for domain in ("docs", "research"):
        items = inventory(domain, overrides)
        all_items[domain] = items
        _validate(items, errors)
        if args.strict_review:
            for item in items:
                if item.get("review_required"):
                    errors.append(f"{item['path']}: requires explicit governance review")
        if args.write:
            _write(domain, items)

    for domain, items in all_items.items():
        counts = Counter(str(item["status"]) for item in items)
        print(
            f"{domain}: {len(items)} files declared; "
            f"status={dict(sorted(counts.items()))}"
        )
    if errors:
        print("Document governance audit: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Document governance audit: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
