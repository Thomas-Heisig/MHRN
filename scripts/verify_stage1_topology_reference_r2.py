#!/usr/bin/env python3
"""Verifier for Stage-1 Brian2 cross-implementation reference DATA R2.

This verifier is intentionally separate from the blinded reference runner. It
may read the canonical preregistration targets and classify persisted reference
DATA, but it never mutates EVID or maturity state automatically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-REFERENCE-R2.json"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def paired_sign_p(values: list[float]) -> float:
    nonzero = [value for value in values if abs(value) > 1e-12]
    n = len(nonzero)
    if n == 0:
        return 1.0
    positive = sum(value > 0 for value in nonzero)
    extreme = min(positive, n - positive)
    one_tail = sum(math.comb(n, k) for k in range(0, extreme + 1)) / (2**n)
    return min(1.0, 2.0 * one_tail)


def bootstrap_median_ci(values: list[float], label: str) -> list[float]:
    if not values:
        return [0.0, 0.0]
    seed = int(hashlib.sha256(label.encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    medians: list[float] = []
    for _ in range(5000):
        sample = [values[rng.randrange(len(values))] for _ in values]
        medians.append(float(statistics.median(sample)))
    medians.sort()
    low_index = int(0.025 * (len(medians) - 1))
    high_index = int(0.975 * (len(medians) - 1))
    return [medians[low_index], medians[high_index]]


def holm(rows: list[dict[str, Any]]) -> None:
    ordered = sorted(enumerate(rows), key=lambda item: float(item[1]["p_raw"]))
    running = 0.0
    m = len(rows)
    adjusted: dict[int, float] = {}
    for rank, (index, row) in enumerate(ordered):
        value = min(1.0, (m - rank) * float(row["p_raw"]))
        running = max(running, value)
        adjusted[index] = running
    for index, row in enumerate(rows):
        row["p_holm"] = adjusted[index]


def interval_relation(ci: list[float], bound: list[float]) -> str:
    low, high = map(float, ci)
    b_low, b_high = map(float, bound)
    if high < b_low or low > b_high:
        return "wholly_outside"
    if low >= b_low and high <= b_high:
        return "wholly_inside"
    return "spans_boundary"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    prereg = read_json(PREREG)
    data_path = Path(args.data)
    output_path = Path(args.output)
    payload = read_json(data_path)
    if not isinstance(payload, dict):
        raise TypeError("reference DATA must be a JSON object")

    expected_conditions = list(prereg["evaluation"]["conditions"])
    expected_seeds = [int(v) for v in prereg["evaluation"]["seeds"]]
    runs_raw = payload.get("runs")
    runs = [dict(row) for row in runs_raw] if isinstance(runs_raw, list) else []

    errors: list[str] = []
    if payload.get("framework") != "Brian2":
        errors.append("framework mismatch")
    if str(payload.get("framework_version")) != str(
        prereg["independence_contract"]["framework_version"]
    ):
        errors.append("framework version mismatch")
    if payload.get("conditions") != expected_conditions:
        errors.append("condition list mismatch")
    if payload.get("seeds") != expected_seeds:
        errors.append("seed list mismatch")
    if len(runs) != 120:
        errors.append(f"expected 120 runs, got {len(runs)}")

    lookup: dict[tuple[str, int], dict[str, Any]] = {}
    for row in runs:
        key = (str(row.get("condition")), int(row.get("seed", -1)))
        if key in lookup:
            errors.append(f"duplicate run {key}")
        lookup[key] = row
        if int(row.get("node_count", -1)) != 64:
            errors.append(f"node count mismatch {key}")
        if int(row.get("edge_count", -1)) != 246:
            errors.append(f"edge count mismatch {key}")

    for condition in expected_conditions:
        for seed in expected_seeds:
            if (condition, seed) not in lookup:
                errors.append(f"missing run {(condition, seed)}")

    primary_rows: list[dict[str, Any]] = []
    bounds = prereg["canonical_targets"]["frozen_bounds"]
    canonical = prereg["canonical_targets"]["first_output_latency_median_deltas"]

    for left, right in prereg["evaluation"]["primary_contrasts"]:
        label = f"{left}_to_{right}"
        differences = [
            float(lookup[(right, seed)]["first_output_latency_censored"])
            - float(lookup[(left, seed)]["first_output_latency_censored"])
            for seed in expected_seeds
            if (left, seed) in lookup and (right, seed) in lookup
        ]
        median = float(statistics.median(differences)) if differences else 0.0
        ci = bootstrap_median_ci(differences, f"latency:{label}")
        bound = [float(v) for v in bounds[label]]
        target = float(canonical[label])
        canonical_sign = -1 if target < 0 else 1
        direction_retained = (median < 0 if canonical_sign < 0 else median > 0)
        in_bound = bound[0] <= median <= bound[1]
        row = {
            "label": label,
            "contrast": [left, right],
            "paired_differences": differences,
            "median_difference": median,
            "bootstrap_ci95": ci,
            "p_raw": paired_sign_p(differences),
            "canonical_sign": canonical_sign,
            "direction_retained": direction_retained,
            "equivalence_bound": bound,
            "median_inside_bound": in_bound,
            "ci_relation_to_bound": interval_relation(ci, bound),
        }
        primary_rows.append(row)

    holm(primary_rows)
    alpha = float(prereg["evaluation"]["alpha"])
    for row in primary_rows:
        ci = row["bootstrap_ci95"]
        row["ci_excludes_zero"] = bool(float(ci[1]) < 0 or float(ci[0]) > 0)
        row["holm_significant"] = bool(float(row["p_holm"]) < alpha)
        row["primary_criterion_pass"] = bool(
            row["direction_retained"]
            and row["median_inside_bound"]
            and row["holm_significant"]
            and row["ci_excludes_zero"]
        )

    auc_expected = prereg["canonical_targets"]["activation_auc_direction_only"]
    auc_rows: list[dict[str, Any]] = []
    for left, right in prereg["evaluation"]["primary_contrasts"]:
        label = f"{left}_to_{right}"
        differences = [
            float(lookup[(right, seed)]["activation_auc_0_32"])
            - float(lookup[(left, seed)]["activation_auc_0_32"])
            for seed in expected_seeds
            if (left, seed) in lookup and (right, seed) in lookup
        ]
        median = float(statistics.median(differences)) if differences else 0.0
        expected = str(auc_expected[label])
        direction_match = median > 0 if expected == "positive" else median < 0
        auc_rows.append(
            {
                "label": label,
                "median_difference": median,
                "expected_direction": expected,
                "direction_match": direction_match,
            }
        )

    reversal_count = sum(not row["direction_retained"] for row in primary_rows)
    significant_count = sum(bool(row["holm_significant"]) for row in primary_rows)
    wholly_outside_count = sum(
        row["ci_relation_to_bound"] == "wholly_outside" for row in primary_rows
    )
    spans_boundary_count = sum(
        row["ci_relation_to_bound"] == "spans_boundary" for row in primary_rows
    )
    primary_pass_count = sum(bool(row["primary_criterion_pass"]) for row in primary_rows)
    auc_match_count = sum(bool(row["direction_match"]) for row in auc_rows)

    if errors:
        classification = "INCONCLUSIVE_REFERENCE_REPLICATION"
        reason = "design_integrity_or_comparability_failure"
    elif reversal_count > 0:
        classification = "FAILED_REPLICATION"
        reason = "primary_direction_reversal"
    elif significant_count < 3:
        classification = "FAILED_REPLICATION"
        reason = "fewer_than_three_primary_contrasts_holm_significant"
    elif wholly_outside_count >= 2:
        classification = "FAILED_REPLICATION"
        reason = "two_or_more_primary_effects_wholly_outside_bounds"
    elif primary_pass_count == 5 and auc_match_count >= 4:
        classification = "PARTIAL_REPLICATION"
        reason = "all_primary_and_secondary_concordance_criteria_met"
    elif spans_boundary_count > 0:
        classification = "INCONCLUSIVE_REFERENCE_REPLICATION"
        reason = "equivalence_boundary_spanned"
    elif primary_pass_count in (3, 4):
        classification = "INCONCLUSIVE_REFERENCE_REPLICATION"
        reason = "three_or_four_primary_criteria_met_without_reversal"
    elif wholly_outside_count == 1 and primary_pass_count == 4:
        classification = "INCONCLUSIVE_REFERENCE_REPLICATION"
        reason = "one_primary_effect_wholly_outside_bound"
    else:
        classification = "INCONCLUSIVE_REFERENCE_REPLICATION"
        reason = "predeclared_success_and_failure_rules_do_not_resolve_stably"

    result = {
        "schema_version": 1,
        "preregistration_id": prereg["preregistration_id"],
        "reference_data": str(data_path),
        "design_integrity_passed": not errors,
        "integrity_errors": errors,
        "primary_endpoint": "first_output_latency_censored",
        "primary_tests": primary_rows,
        "secondary_auc_direction_checks": auc_rows,
        "summary": {
            "primary_direction_reversals": reversal_count,
            "holm_significant_primary": significant_count,
            "primary_wholly_outside_bounds": wholly_outside_count,
            "primary_spanning_bounds": spans_boundary_count,
            "primary_criteria_passed": primary_pass_count,
            "auc_direction_matches": auc_match_count,
        },
        "classification": classification,
        "classification_reason": reason,
        "replication_credit_automatically_awarded": False,
        "scientific_evidence": False,
        "human_review_required": True,
        "maturity_update_automatic": False,
        "claim_boundary": (
            "This verifier classifies only the preregistered project-side "
            "cross-implementation reference result. Even PARTIAL_REPLICATION "
            "cannot become EVID or Stage-1 maturity credit without separate "
            "human review and canonical state update."
        ),
    }

    if output_path.exists():
        raise FileExistsError(f"refusing to overwrite {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "classification": classification,
                "reason": reason,
                "design_integrity_passed": not errors,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
