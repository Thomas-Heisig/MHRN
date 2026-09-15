"""Aggregate a Stage-6 DATA bundle without promoting it to evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, cast


def _load(path: Path) -> dict[str, Any]:
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Stage-6 DATA root must be an object")
    return cast(dict[str, Any], raw)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _numeric_metrics(rows: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    values: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        metrics = row.get("metrics")
        if not isinstance(metrics, dict):
            continue
        for key, value in cast(dict[str, Any], metrics).items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            values[key].append(float(value))
    output: dict[str, dict[str, float | int]] = {}
    for key, samples in sorted(values.items()):
        if not samples:
            continue
        output[key] = {
            "n": len(samples),
            "mean": sum(samples) / len(samples),
            "min": min(samples),
            "max": max(samples),
        }
    return output


def aggregate(data_path: Path) -> dict[str, Any]:
    data = _load(data_path)
    if data.get("scientific_evidence") is not False:
        raise ValueError("Stage-6 DATA must not be marked as accepted evidence")
    protocols = data.get("protocols")
    if not isinstance(protocols, dict):
        raise ValueError("Stage-6 DATA protocols must be an object")
    summary: dict[str, Any] = {}
    for protocol_id, raw_rows in sorted(cast(dict[str, Any], protocols).items()):
        if not isinstance(raw_rows, list):
            raise ValueError(f"protocol rows must be a list: {protocol_id}")
        rows = [cast(dict[str, Any], row) for row in raw_rows if isinstance(row, dict)]
        by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            by_condition[str(row.get("condition"))].append(row)
        summary[protocol_id] = {
            "run_count": len(rows),
            "conditions": {
                condition: {
                    "seed_count": len({int(row["seed"]) for row in condition_rows}),
                    "numeric_metrics": _numeric_metrics(condition_rows),
                }
                for condition, condition_rows in sorted(by_condition.items())
            },
        }
    return {
        "schema_version": 1,
        "source_data_sha256": _sha256(data_path),
        "source_commit": cast(dict[str, Any], data.get("source", {})).get("commit"),
        "protocol_sha256": cast(dict[str, Any], data.get("source", {})).get(
            "protocol_sha256"
        ),
        "preregistration_sha256": cast(dict[str, Any], data.get("source", {})).get(
            "preregistration_sha256"
        ),
        "seeds": data.get("seeds"),
        "scientific_evidence": False,
        "automatic_evidence_promotion": False,
        "protocols": summary,
    }


def _important_metrics(protocol_id: str) -> tuple[str, ...]:
    return {
        "s6_epi_001_v1": ("accuracy", "retrievals", "distractor_spikes"),
        "s6_sem_001_v1": ("accuracy", "matched_holdout", "mature_concepts"),
        "s6_rpl_001_v1": (
            "mean_reactivation_fidelity",
            "mature_concepts",
            "budget_matched",
        ),
        "s6_pe_001_v1": ("weight_delta", "prediction_error_updates", "reward_calls"),
        "s6_wm_001_v1": (
            "exact_final_state_rate",
            "mean_absolute_final_state_error",
            "completed_rollouts",
        ),
        "s6_wm_002_v1": ("utility_ratio", "achieved_utility", "recommendations"),
        "s6_nwm_001_v1": (
            "exact_accuracy",
            "prediction_coverage",
            "mean_latency_steps",
            "mean_correct_weight_margin",
        ),
    }.get(protocol_id, ())


def markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Stage 6 empirical DATA summary",
        "",
        "Status: descriptive DATA aggregation only; not accepted EVID.",
        "",
        f"Source commit: `{summary.get('source_commit')}`  ",
        f"DATA SHA-256: `{summary.get('source_data_sha256')}`  ",
        f"Protocol SHA-256: `{summary.get('protocol_sha256')}`  ",
        f"Preregistration SHA-256: `{summary.get('preregistration_sha256')}`  ",
        f"Seeds: `{summary.get('seeds')}`",
        "",
        "| Protocol | Condition | Seeds | Primary descriptive means |",
        "| --- | --- | ---: | --- |",
    ]
    protocols = cast(dict[str, Any], summary["protocols"])
    for protocol_id, protocol in sorted(protocols.items()):
        conditions = cast(dict[str, Any], protocol["conditions"])
        important = _important_metrics(protocol_id)
        for condition, values in sorted(conditions.items()):
            metrics = cast(dict[str, Any], values["numeric_metrics"])
            compact: list[str] = []
            for metric in important:
                stat = metrics.get(metric)
                if isinstance(stat, dict):
                    mean = cast(dict[str, Any], stat).get("mean")
                    if isinstance(mean, (int, float)):
                        compact.append(f"{metric}={float(mean):.6g}")
            lines.append(
                f"| `{protocol_id}` | `{condition}` | {values['seed_count']} | "
                + (", ".join(compact) if compact else "—")
                + " |"
            )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "These values are descriptive outputs from the frozen Stage-6 DATA bundle. "
            "They are not automatically inferential statistics, accepted evidence, or a "
            "basis for closing `RQ-MEM-002` or `RQ-WM-001`. Confirmatory claims require "
            "the preregistered larger independent-seed campaign, uncertainty estimates, "
            "failure reporting, and human scientific review.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=Path)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    args = parser.parse_args()
    summary = aggregate(args.data)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    args.markdown_output.write_text(markdown(summary), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
