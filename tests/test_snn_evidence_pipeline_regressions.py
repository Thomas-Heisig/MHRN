from __future__ import annotations

import json
from pathlib import Path

from src.research.experiment_summary import (
    build_descriptive_statistics,
    write_detailed_experiment_summary,
    write_statistics_artifact,
)


def _runs():
    base = {"experiment_id": "EXP-TEST-SNN-EVID", "seed": 42, "runtime_error": None}
    return [
        {
            **base,
            "condition": "no_input_control",
            "metrics": {
                "ticks_executed": 100000,
                "post_burn_in_mean_spikes": 0.0,
                "post_burn_in_spike_cv": 0.0,
                "post_burn_in_spike_relative_drift": 0.0,
                "finite_state": True,
                "topology_unchanged": True,
                "stability_pass": True,
            },
        },
        {
            **base,
            "condition": "tonic_drive",
            "metrics": {
                "ticks_executed": 100000,
                "post_burn_in_mean_spikes": 300.0,
                "post_burn_in_spike_cv": 0.0,
                "post_burn_in_spike_relative_drift": 0.0,
                "finite_state": True,
                "topology_unchanged": True,
                "stability_pass": True,
            },
        },
    ]


def _deterministic_replica_runs():
    runs = []
    metrics_by_condition = {
        "recurrence_off_replica_a": (3, 2, 0, 1),
        "recurrence_off_replica_b": (3, 2, 0, 1),
        "recurrence_on_replica_a": (33, 33, 10, 61),
        "recurrence_on_replica_b": (33, 33, 10, 61),
    }
    for seed in (101, 102, 103):
        for condition, values in metrics_by_condition.items():
            spikes, synaptic_events, recurrent_events, propagation_depth = values
            runs.append(
                {
                    "experiment_id": "EXP-TEST-DET-001",
                    "condition": condition,
                    "seed": seed,
                    "metrics": {
                        "ticks_executed": 256,
                        "total_spikes": spikes,
                        "delivered_synaptic_events": synaptic_events,
                        "activated_neurons": 3,
                        "recurrent_events": recurrent_events,
                        "propagation_depth": propagation_depth,
                        "stopped_on_quiescence": False,
                    },
                    "runtime_error": None,
                }
            )
    return runs


def _write_determinism_fixture(tmp_path: Path, *, git_dirty: bool) -> Path:
    e = tmp_path / "experiments" / "EXP-TEST-DET-001"
    (e / "DATA").mkdir(parents=True)
    runs = _deterministic_replica_runs()
    (e / "DATA" / "runs_compact.json").write_text(
        json.dumps(runs), encoding="utf-8"
    )
    (e / "manifest.json").write_text(
        json.dumps(
            {
                "experiment_status": "completed",
                "research_questions": ["RQ-DET-001"],
                "hypotheses": ["H-SNN-003-A"],
                "research_run_mode": "EXPLORATORY",
                "network_mode": "OFFLINE",
                "simulation": {
                    "ticks": 256,
                    "seeds": [101, 102, 103],
                    "protocol": "deterministic_replica_v1",
                },
                "results": {"run_count": 12},
                "git": {"commit": "fixture", "dirty": git_dirty},
                "artifacts": {"data": "DATA/runs_compact.json"},
            }
        ),
        encoding="utf-8",
    )
    (e / "workflow.json").write_text(
        json.dumps(
            {
                "title": "Deterministic replica",
                "conditions": "registered replica pairs",
                "ticks": 256,
                "seeds": [101, 102, 103],
                "protocol": "deterministic_replica_v1",
            }
        ),
        encoding="utf-8",
    )
    write_statistics_artifact(e, runs)
    write_detailed_experiment_summary(
        tmp_path, "EXP-TEST-DET-001", {"status": "unavailable", "reason": "fixture"}
    )
    return e / "summary.md"


def test_boolean_primary_outcomes_are_aggregated():
    s = build_descriptive_statistics(_runs())
    assert s["schema_version"] == "2.2"
    b = s["conditions"]["tonic_drive"]["boolean_metrics"]
    assert b["finite_state"] == {
        "n": 1,
        "true_count": 1,
        "false_count": 0,
        "true_fraction": 1.0,
        "all_true": True,
    }
    assert b["topology_unchanged"]["all_true"] is True
    assert b["stability_pass"]["all_true"] is True


def test_summary_committed_data_and_visible_values(tmp_path: Path):
    e = tmp_path / "experiments" / "EXP-TEST-SNN-EVID"
    (e / "DATA").mkdir(parents=True)
    (e / "DATA" / "runs_compact.json").write_text(json.dumps(_runs()), encoding="utf-8")
    (e / "manifest.json").write_text(
        json.dumps(
            {
                "experiment_status": "completed",
                "research_questions": ["RQ-SNN-001"],
                "hypotheses": ["H-SNN-001-A"],
                "research_run_mode": "CONFIRMATORY",
                "network_mode": "OFFLINE",
                "simulation": {
                    "ticks": 100000,
                    "seeds": [42],
                    "protocol": "sustained_activity_stability_v1",
                },
                "results": {"run_count": 2},
                "git": {"commit": "fixture", "dirty": False},
                "artifacts": {"data": "DATA/runs_compact.json"},
            }
        ),
        encoding="utf-8",
    )
    (e / "workflow.json").write_text(
        json.dumps(
            {
                "title": "Sustained stability",
                "conditions": "control; treatment",
                "ticks": 100000,
                "seeds": [42],
                "protocol": "sustained_activity_stability_v1",
            }
        ),
        encoding="utf-8",
    )
    write_statistics_artifact(e, _runs())
    write_detailed_experiment_summary(
        tmp_path, "EXP-TEST-SNN-EVID", {"status": "unavailable", "reason": "fixture"}
    )
    s = (e / "summary.md").read_text(encoding="utf-8")
    assert "Mittelwert: `mean(x) = (1/n) * sum_i x_i`" in s
    assert "`absolute_difference=300`" in s
    assert "Boolesche Endpunkte und operative Telemetrie" in s and "`finite_state`" in s
    assert "Deterministische Statistikdatei: `analysis/statistics.json`" in s
    assert "- `DATA/runs_compact.json`" in s and "DATA/runs.json" not in s


def test_rq_det_001_clean_source_is_direct_match_and_requires_human_review(
    tmp_path: Path,
):
    summary_path = _write_determinism_fixture(tmp_path, git_dirty=False)
    summary = summary_path.read_text(encoding="utf-8")
    assert "RQ/Condition-Pruefung: `DIRECT_MATCH`" in summary
    assert "Evidence Readiness: `HUMAN_REVIEW_REQUIRED`" in summary
    assert "RQ-DET-001 erwartet je Seed identische Replica-Paare" in summary
    assert "`stopped_on_quiescence` ist kein Erfolgs- oder Evidenzkriterium" in summary
    assert "min_ticks == max_ticks" in summary


def test_rq_det_001_dirty_source_remains_blocked(tmp_path: Path):
    summary_path = _write_determinism_fixture(tmp_path, git_dirty=True)
    summary = summary_path.read_text(encoding="utf-8")
    assert "RQ/Condition-Pruefung: `DIRECT_MATCH`" in summary
    assert "Evidence Readiness: `BLOCKED_DIRTY_SOURCE_TREE`" in summary
