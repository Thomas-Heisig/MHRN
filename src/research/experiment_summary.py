"""Deterministic, data-first experiment summaries for MHRN research runs."""

# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnnecessaryIsInstance=false

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import fmean, median, pstdev
from typing import Any

_SUITE_REQUIRED_GROUPS = {
    "ping",
    "temporal",
    "stdp",
    "learning",
    "time",
    "5d",
    "regulation",
}

_PRIMARY_SUMMARY_METRICS = {
    "ticks_executed",
    "total_spikes",
    "delivered_synaptic_events",
    "activated_neurons",
    "recurrent_events",
    "propagation_depth",
}


def _read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _number(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    result = float(value)
    return result if math.isfinite(result) else None


def _stats(values: list[float]) -> dict[str, float | int]:
    if not values:
        return {"n": 0}
    return {
        "n": len(values),
        "mean": fmean(values),
        "median": median(values),
        "std": pstdev(values),
        "min": min(values),
        "max": max(values),
    }


def build_descriptive_statistics(runs: list[dict[str, Any]]) -> dict[str, Any]:
    """Build deterministic descriptive statistics without model participation."""
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        by_condition[str(run.get("condition", "unknown"))].append(run)

    known_numeric_metrics = {
        "ticks_executed",
        "total_spikes",
        "activated_neurons",
        "delivered_synaptic_events",
        "synaptic_activity_ticks",
        "recurrent_events",
        "propagation_depth",
        "first_response_latency",
        "last_response_latency",
        "return_latency",
        "ticks_per_second",
        "duration_seconds",
        "mean_weight_delta",
        "initial_mean_weight",
        "final_mean_weight",
        "rewards_received",
        "reward_weight_updates",
        "p_success_before",
        "p_success_after",
        "train_trial_count",
        "validation_trial_count",
        "holdout_trial_count",
    }
    discovered_numeric_metrics = {
        str(name)
        for run in runs
        for name, value in (run.get("metrics") or {}).items()
        if _number(value) is not None
    }
    numeric_metric_names = sorted(known_numeric_metrics | discovered_numeric_metrics)
    boolean_metric_names = sorted(
        {
            str(name)
            for run in runs
            for name, value in (run.get("metrics") or {}).items()
            if isinstance(value, bool)
        }
    )

    nested_paths = {
        "functional_activation": ("functional_state", "activation"),
        "functional_safety": ("functional_state", "safety"),
        "functional_valence": ("functional_state", "valence"),
        "functional_uncertainty": ("functional_state", "uncertainty"),
        "regulatory_continuity_risk": (
            "regulatory_state",
            "values",
            "continuity_risk",
        ),
        "regulatory_energy_reserve": (
            "regulatory_state",
            "values",
            "energy_reserve",
        ),
        "regulatory_resource_pressure": (
            "regulatory_state",
            "values",
            "resource_pressure",
        ),
        "regulatory_sensory_integrity": (
            "regulatory_state",
            "values",
            "sensory_integrity",
        ),
        "regulatory_thermal_margin": (
            "regulatory_state",
            "values",
            "thermal_margin",
        ),
    }

    conditions: dict[str, Any] = {}
    for condition, condition_runs in sorted(by_condition.items()):
        metric_stats: dict[str, Any] = {}
        for name in numeric_metric_names:
            values = [
                value
                for run in condition_runs
                for value in [_number((run.get("metrics") or {}).get(name))]
                if value is not None
            ]
            if values:
                metric_stats[name] = _stats(values)

        boolean_stats: dict[str, Any] = {}
        for name in boolean_metric_names:
            values = [
                value
                for run in condition_runs
                for value in [(run.get("metrics") or {}).get(name)]
                if isinstance(value, bool)
            ]
            if values:
                true_count = sum(values)
                boolean_stats[name] = {
                    "n": len(values),
                    "true_count": true_count,
                    "false_count": len(values) - true_count,
                    "true_fraction": true_count / len(values),
                    "all_true": all(values),
                }

        for name, path in nested_paths.items():
            nested_values: list[float] = []
            for run in condition_runs:
                current: object = run.get("metrics") or {}
                for part in path:
                    current = current.get(part) if isinstance(current, dict) else None
                value = _number(current)
                if value is not None:
                    nested_values.append(value)
            if nested_values:
                metric_stats[name] = _stats(nested_values)

        conditions[condition] = {
            "run_count": len(condition_runs),
            "seeds": sorted(
                {
                    int(run["seed"])
                    for run in condition_runs
                    if isinstance(run.get("seed"), int)
                }
            ),
            "metrics": metric_stats,
            "boolean_metrics": boolean_stats,
        }

    temporal_values: dict[str, list[float]] = defaultdict(list)
    temporal_reference_counts: dict[str, int] = defaultdict(int)
    for run in runs:
        comparisons = (run.get("metrics") or {}).get("comparisons")
        if not isinstance(comparisons, list):
            continue
        for comparison in comparisons:
            if not isinstance(comparison, dict):
                continue
            horizon = str(comparison.get("horizon", "unknown"))
            discrepancy = _number(comparison.get("discrepancy"))
            if discrepancy is not None:
                temporal_values[horizon].append(discrepancy)
            if comparison.get("reference_tick") is not None:
                temporal_reference_counts[horizon] += 1

    temporal: dict[str, Any] = {}
    for horizon in sorted(set(temporal_values) | set(temporal_reference_counts)):
        all_values = temporal_values[horizon]
        nonzero = [value for value in all_values if value != 0.0]
        temporal[horizon] = {
            "discrepancy": _stats(all_values),
            "reference_comparisons": temporal_reference_counts[horizon],
            "nonzero_comparisons": len(nonzero),
            "nonzero_fraction": len(nonzero) / len(all_values) if all_values else 0.0,
            "nonzero_discrepancy": _stats(nonzero),
        }

    isi_by_condition: dict[str, Any] = {}
    for condition, condition_runs in sorted(by_condition.items()):
        intervals: list[float] = []
        for run in condition_runs:
            sequence = (run.get("metrics") or {}).get("spike_sequence")
            if not isinstance(sequence, list):
                continue
            ticks = [
                int(item["tick"])
                for item in sequence
                if isinstance(item, dict) and isinstance(item.get("tick"), int)
            ]
            intervals.extend(float(b - a) for a, b in zip(ticks, ticks[1:]))
        if intervals:
            isi_by_condition[condition] = _stats(intervals)

    result: dict[str, Any] = {
        "generated_by": "deterministic_statistics_engine",
        "schema_version": "2.2",
        "run_count": len(runs),
        "conditions": conditions,
        "formulas": {
            "mean": "mean(x) = (1/n) * sum_i x_i",
            "population_std": "sigma = sqrt((1/n) * sum_i (x_i - mean(x))^2)",
            "difference": "Delta_x = mean(x_B) - mean(x_A)",
            "ratio": "R_x = mean(x_B) / mean(x_A), defined only when mean(x_A) != 0",
            "inter_spike_interval": "ISI_i = t_(i+1) - t_i",
        },
    }
    if temporal:
        result["temporal_horizons"] = temporal
    if isi_by_condition:
        result["inter_spike_intervals"] = isi_by_condition

    condition_names = sorted(conditions)
    if len(condition_names) == 2:
        a, b = condition_names
        effects: dict[str, Any] = {}
        common = set(conditions[a]["metrics"]) & set(conditions[b]["metrics"])
        for metric in sorted(common):
            av = conditions[a]["metrics"][metric].get("mean")
            bv = conditions[b]["metrics"][metric].get("mean")
            if isinstance(av, (int, float)) and isinstance(bv, (int, float)):
                effects[metric] = {
                    "reference_condition": a,
                    "comparison_condition": b,
                    "absolute_difference": float(bv) - float(av),
                    "ratio": None if float(av) == 0.0 else float(bv) / float(av),
                }
        result["two_condition_effects"] = effects
    return result


def write_statistics_artifact(experiment_dir: Path, runs: list[dict[str, Any]]) -> Path:
    """Persist deterministic statistics so AIRR and summary share one numeric source."""
    path = experiment_dir / "analysis" / "statistics.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            build_descriptive_statistics(runs),
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def _semantic_status(
    question_id: str, protocol: str, conditions: set[str]
) -> tuple[str, str]:
    """Classify direct RQ tests separately from matching substudies in a suite."""
    plain = {item.split(":", 1)[-1] for item in conditions}

    def classify(found: bool, note: str) -> tuple[str, str]:
        if not found:
            return "MISMATCH", note
        if protocol == "science_all_v1":
            return (
                "CONTAINS_MATCH",
                note + " Die relevante Teilstudie ist in science_all_v1 enthalten; "
                "nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten.",
            )
        return "DIRECT_MATCH", note

    if question_id == "RQ-REC-001":
        return classify(
            any(item.startswith("w0_") for item in plain)
            and any(
                item.startswith("w100_") or item.startswith("w125_") for item in plain
            ),
            "REC-001 erwartet eine registrierte Rekurrenz-Gewicht/Delay-Karte mit Nullkontrolle.",
        )
    if question_id == "RQ-REC-002":
        return classify(
            {"loop_delay_1", "loop_delay_2", "loop_delay_4", "loop_delay_8"}.issubset(
                plain
            ),
            "REC-002 erwartet die registrierte Loop-Delay-Leiter.",
        )
    if question_id == "RQ-GEN-001":
        return classify(
            any(item.startswith("learning_on_drive_") for item in plain)
            and any(item.startswith("learning_off_drive_") for item in plain)
            and any(item.startswith("sham_replay_drive_") for item in plain),
            "GEN-001 erwartet Learning-on, Learning-off und Sham-Replay über registrierte Perturbationsproben.",
        )
    if question_id == "RQ-REPL-001":
        return classify(
            {"recurrence_off", "recurrence_on"}.issubset(plain),
            "REPL-001 erwartet beide Rekurrenzarme mit unabhängiger Seedstrategie.",
        )
    if question_id == "RQ-5D-005":
        return classify(
            {"1d", "2d", "3d", "5d"}.issubset(plain),
            "5D-005 erwartet topology-matched 1D/2D/3D/5D-Einbettungen.",
        )
    if question_id == "RQ-REG-002":
        return classify(
            {"regulation_off", "regulation_on"}.issubset(plain),
            "REG-002 erwartet Regulation-off und Regulation-on unter gleichem Perturbationsplan.",
        )
    if question_id == "RQ-TEMP-002":
        return classify(
            {"forward", "reverse", "simultaneous"}.issubset(plain),
            "TEMP-002 erwartet Forward-, Reverse- und Simultankontrolle.",
        )
    if question_id == "RQ-PERF-001":
        return classify(
            "subsystem_profile" in plain,
            "PERF-001 erwartet subsystemaufgelöste Runtime-Messungen.",
        )
    if question_id == "RQ-LIFE-001":
        return classify(
            "sequential_three_task_screen" in plain,
            "LEARN-INTERF-001 v1 ist ein explizit als Vorläufer markierter Interferenz-Screen.",
        )
    if question_id.startswith("RQ-PING-"):
        return classify(
            {"recurrence_off", "recurrence_on"}.issubset(plain),
            "PING erwartet recurrence_off und recurrence_on.",
        )
    if question_id.startswith("RQ-TEMP-"):
        return classify(
            "fast_medium_slow" in plain,
            "TEMP erwartet fast_medium_slow mit FAST/MEDIUM/SLOW-Horizonten.",
        )
    if question_id.startswith("RQ-TIME-"):
        time_conditions = {
            item.split(":", 1)[1]
            for item in conditions
            if item.startswith("time:") and ":" in item
        }
        direct_conditions = {item for item in conditions if ":" not in item}
        candidates = time_conditions or direct_conditions
        return classify(
            bool(candidates) and all(item.isdigit() for item in candidates),
            "TIME erwartet numerische Tick-Leiter-Bedingungen.",
        )
    if question_id.startswith("RQ-5D-"):
        return classify(
            {"1d", "2d", "3d", "5d", "random_graph"}.issubset(plain),
            "5D erwartet die registrierten Dimensions-/Topologiebedingungen.",
        )
    if question_id == "RQ-SUITE-001":
        present_groups = {item.split(":", 1)[0] for item in conditions if ":" in item}
        found = (
            _SUITE_REQUIRED_GROUPS.issubset(present_groups)
            and protocol == "science_all_v1"
        )
        return (
            "DIRECT_MATCH" if found else "MISMATCH",
            "SUITE erwartet science_all_v1 und PING, TEMP, STDP, Learning, TIME, 5D sowie Regulation unter gemeinsamer Provenienz.",
        )
    if question_id == "RQ-SNN-002":
        return classify(
            {"recurrence_off", "recurrence_on"}.issubset(plain),
            "RQ-SNN-002 erwartet einen kontrollierten Impulsantwort-Vergleich mit recurrence_off und recurrence_on.",
        )
    if question_id == "RQ-SNN-001":
        if protocol == "sustained_activity_stability_v1":
            return (
                "DIRECT_MATCH",
                "RQ-SNN-001 verwendet das dedizierte Sustained-Activity-Protokoll mit Kontroll- und Tonic-Drive-Bedingung.",
            )
        return (
            "MISMATCH",
            "RQ-SNN-001 fordert langfristig stabile Spike-Dynamik unter fortlaufender Aktivitaet. science_suite_v1/science_all_v1 bleiben dafuer diagnostisch; eine Primaerpruefung erfordert weiterhin ein dediziertes Sustained-Activity-Protokoll.",
        )
    return (
        "NOT_AUTOMATICALLY_CLASSIFIED",
        "Keine automatische semantische Regel fuer diese RQ-Familie registriert.",
    )


def _fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.6g}"
    if value is None:
        return "—"
    return str(value)


def _suite_integrity(
    runs: list[dict[str, Any]], statistics: dict[str, Any]
) -> dict[str, Any]:
    """Audit suite artifact completeness independently of report columns."""
    raw_conditions = {str(run.get("condition", "unknown")) for run in runs}
    statistics_conditions_value = statistics.get("conditions", {})
    statistics_conditions: dict[str, Any] = (
        statistics_conditions_value
        if isinstance(statistics_conditions_value, dict)
        else {}
    )
    present_groups = {
        condition.split(":", 1)[0] for condition in raw_conditions if ":" in condition
    }
    missing_groups = sorted(_SUITE_REQUIRED_GROUPS - present_groups)
    missing_statistics = sorted(raw_conditions - set(statistics_conditions))
    empty_statistics = sorted(
        condition
        for condition, payload in statistics_conditions.items()
        if not isinstance(payload, dict)
        or (
            (not isinstance(payload.get("metrics"), dict) or not payload.get("metrics"))
            and (
                not isinstance(payload.get("boolean_metrics"), dict)
                or not payload.get("boolean_metrics")
            )
        )
    )
    runtime_error_count = sum(
        run.get("runtime_error") not in (None, "", False) for run in runs
    )
    statistics_run_count = statistics.get("run_count")
    run_count_matches = statistics_run_count == len(runs)
    complete = (
        not missing_groups
        and not missing_statistics
        and not empty_statistics
        and runtime_error_count == 0
        and run_count_matches
    )
    return {
        "status": "COMPLETE_FOR_REGISTERED_GROUPS" if complete else "INCOMPLETE",
        "raw_run_count": len(runs),
        "statistics_run_count": statistics_run_count,
        "run_count_matches": run_count_matches,
        "raw_condition_count": len(raw_conditions),
        "statistics_condition_count": len(statistics_conditions),
        "present_groups": sorted(present_groups),
        "missing_groups": missing_groups,
        "missing_statistics": missing_statistics,
        "empty_statistics": empty_statistics,
        "runtime_error_count": runtime_error_count,
    }


def _mean_metrics(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        return {}
    metrics = payload.get("metrics", {})
    if not isinstance(metrics, dict):
        return {}
    result: dict[str, object] = {}
    for name, stats in metrics.items():
        if isinstance(stats, dict) and "mean" in stats:
            result[str(name)] = stats.get("mean")
    return result


def _render_airr_sections(
    lines: list[str], experiment_dir: Path, ai_report: dict[str, object]
) -> None:
    lines.extend(
        [
            "",
            "## 8. AI Research Report",
            "",
            f"- AIRR Status: `{ai_report.get('status', 'unknown')}`",
            "- Wissenschaftliche Evidenz durch KI: `false`",
            "- Human Review: `PENDING`",
        ]
    )
    if ai_report.get("status") != "generated" or not ai_report.get("report_id"):
        if ai_report.get("status") == "failed":
            lines.extend(
                [
                    "",
                    f"AIRR-Fehler: `{ai_report.get('message', ai_report.get('reason', 'unknown'))}`. Die deterministische Datenauswertung oben bleibt davon unberuehrt.",
                ]
            )
        return

    report_id = str(ai_report["report_id"])
    report = _read_json(experiment_dir / "reports" / f"{report_id}.json", {})
    content = report.get("content", {}) if isinstance(report, dict) else {}
    if not isinstance(content, dict):
        content = {}
    lines.extend(
        [
            f"- AIRR Markdown: `reports/{report_id}.md`",
            f"- AIRR JSON: `reports/{report_id}.json`",
            "",
            "### 8.1 KI-Einschaetzung",
            "",
            str(
                content.get(
                    "executive_summary",
                    content.get("conclusion", "Keine Einschätzung vorhanden."),
                )
            ),
            "",
            f"KI-Konfidenz: `{content.get('ai_confidence', 0.0)}` — dies ist keine statistische Konfidenz.",
        ]
    )
    interpretation = content.get("interpretation", {})
    if not isinstance(interpretation, dict):
        interpretation = {}
    observations = interpretation.get("observations", [])
    limitation_fallback: list[str] = []
    if isinstance(observations, list):
        for observation in observations:
            if (
                isinstance(observation, dict)
                and str(observation.get("type", "")).strip().lower() == "limitations"
                and observation.get("value")
            ):
                limitation_fallback.append(
                    f"AIRR-Limitation dokumentieren: {observation['value']}"
                )

    missing_evidence = content.get("missing_evidence", [])
    if not isinstance(missing_evidence, list) or not missing_evidence:
        requested = interpretation.get("requested_evidence", [])
        missing_evidence = (
            requested
            if isinstance(requested, list) and requested
            else limitation_fallback
        )

    recommended = content.get("recommended_follow_up", [])
    if not isinstance(recommended, list) or not recommended:
        interpreted_recommended = interpretation.get("recommended_experiments", [])
        recommended = (
            interpreted_recommended if isinstance(interpreted_recommended, list) else []
        )

    sections = (
        ("Methodische Kritik", content.get("methodological_critique", [])),
        ("Alternative Erklaerungen", content.get("alternative_explanations", [])),
        ("Fehlende Nachweise", missing_evidence),
        ("Empfohlene Folgeexperimente", recommended),
    )
    for heading, values in sections:
        lines.extend(["", f"### {heading}", ""])
        if isinstance(values, list) and values:
            lines.extend(f"- {value}" for value in values)
        elif heading == "Empfohlene Folgeexperimente":
            lines.append("- Keine expliziten Folgeexperimente im AIRR angegeben.")
        else:
            lines.append("- Keine expliziten Angaben.")


def write_detailed_experiment_summary(
    research_root: Path, experiment_id: str, ai_report: dict[str, object]
) -> str:
    """Write a comprehensive data-first summary beside one experiment."""
    experiment_dir = research_root / "experiments" / experiment_id
    manifest = _read_json(experiment_dir / "manifest.json", {})
    workflow = _read_json(experiment_dir / "workflow.json", {})
    runs_path = experiment_dir / "DATA" / "runs_compact.json"
    if not runs_path.is_file():
        runs_path = experiment_dir / "DATA" / "runs.json"
    raw_runs = _read_json(runs_path, [])
    runs = (
        [item for item in raw_runs if isinstance(item, dict)]
        if isinstance(raw_runs, list)
        else []
    )
    statistics_path = experiment_dir / "analysis" / "statistics.json"
    stored_statistics = _read_json(statistics_path, None)
    if (
        isinstance(stored_statistics, dict)
        and stored_statistics.get("generated_by") == "deterministic_statistics_engine"
    ):
        statistics = stored_statistics
    else:
        statistics = build_descriptive_statistics(runs)
        statistics_path = write_statistics_artifact(experiment_dir, runs)

    simulation = manifest.get("simulation", {}) if isinstance(manifest, dict) else {}
    results = manifest.get("results", {}) if isinstance(manifest, dict) else {}
    question_ids = (
        manifest.get("research_questions", []) if isinstance(manifest, dict) else []
    )
    hypothesis_ids = (
        manifest.get("hypotheses", []) if isinstance(manifest, dict) else []
    )
    question_id = (
        str(question_ids[0])
        if isinstance(question_ids, list) and question_ids
        else "NOT_AVAILABLE"
    )
    protocol = str(
        simulation.get("protocol", workflow.get("protocol", "NOT_AVAILABLE"))
        if isinstance(simulation, dict)
        else workflow.get("protocol", "NOT_AVAILABLE")
    )
    conditions = {str(run.get("condition", "unknown")) for run in runs}
    semantic_status, semantic_note = _semantic_status(question_id, protocol, conditions)
    suite_integrity = (
        _suite_integrity(runs, statistics)
        if protocol == "science_all_v1" or question_id == "RQ-SUITE-001"
        else None
    )

    git_info = manifest.get("git", {}) if isinstance(manifest, dict) else {}
    git_dirty = bool(git_info.get("dirty")) if isinstance(git_info, dict) else True
    if semantic_status == "MISMATCH":
        evidence_readiness = "BLOCKED_SEMANTIC_MISMATCH"
    elif semantic_status == "NOT_AUTOMATICALLY_CLASSIFIED":
        evidence_readiness = "BLOCKED_UNCLASSIFIED_SEMANTICS"
    elif git_dirty:
        evidence_readiness = "BLOCKED_DIRTY_SOURCE_TREE"
    elif question_id == "RQ-SUITE-001":
        evidence_readiness = "DIAGNOSTIC_ONLY"
    else:
        evidence_readiness = "HUMAN_REVIEW_REQUIRED"

    requested_ticks = (
        simulation.get("ticks", workflow.get("ticks", "NOT_AVAILABLE"))
        if isinstance(simulation, dict)
        else workflow.get("ticks", "NOT_AVAILABLE")
    )
    actual_ticks = [
        int(value)
        for run in runs
        for value in [(run.get("metrics") or {}).get("ticks_executed")]
        if isinstance(value, int) and not isinstance(value, bool)
    ]
    tick_contract = "NOT_APPLICABLE"
    if isinstance(requested_ticks, int) and actual_ticks:
        tick_contract = (
            "SATISFIED" if min(actual_ticks) >= requested_ticks else "VIOLATED"
        )

    lines = [
        f"# {experiment_id}: Wissenschaftliche Zusammenfassung",
        "",
        "Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.",
        "",
        "## 1. Identifikation und Status",
        "",
        f"- Experimentstatus: `{manifest.get('experiment_status', 'unknown')}`",
        f"- Forschungsfrage: `{question_id}`",
        f"- Hypothese: `{hypothesis_ids[0] if isinstance(hypothesis_ids, list) and hypothesis_ids else 'NOT_AVAILABLE'}`",
        f"- Protokoll: `{protocol}`",
        f"- Durchlaeufe: `{results.get('run_count', len(runs)) if isinstance(results, dict) else len(runs)}`",
        f"- Seeds: `{simulation.get('seeds', workflow.get('seeds', [])) if isinstance(simulation, dict) else workflow.get('seeds', [])}`",
        f"- Angeforderte Ticks: `{requested_ticks}`",
        f"- Tickgebundene SNN-Läufe (PING/TEMP/5D): `{min(actual_ticks) if actual_ticks else 'nicht direkt messbar'} .. {max(actual_ticks) if actual_ticks else 'nicht direkt messbar'}` ausgeführte Ticks",
        f"- Tick-Vertrag: `{tick_contract}`",
        "- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.",
        "- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.",
        f"- Laufmodus: `{manifest.get('research_run_mode', 'unknown')}`",
        f"- Netzwerkmodus: `{manifest.get('network_mode', 'unknown')}`",
        "",
        "## 2. Semantische Konsistenz",
        "",
        f"- RQ/Condition-Pruefung: `{semantic_status}`",
        f"- Evidence Readiness: `{evidence_readiness}`",
        f"- Begründung: {semantic_note}",
        f"- Beobachtete Conditions: `{', '.join(sorted(conditions)) or 'keine'}`",
    ]
    if suite_integrity is not None:
        lines.extend(
            [
                f"- Suite-Artefaktintegrität: `{suite_integrity['status']}`",
                f"- DATA/Statistik-Laufzahl: `{suite_integrity['raw_run_count']}` / `{suite_integrity['statistics_run_count']}`",
                f"- DATA/Statistik-Conditions: `{suite_integrity['raw_condition_count']}` / `{suite_integrity['statistics_condition_count']}`",
                f"- Registrierte Gruppen vorhanden: `{', '.join(suite_integrity['present_groups'])}`",
                f"- Fehlende Gruppen: `{', '.join(suite_integrity['missing_groups']) or 'keine'}`",
                f"- Conditions ohne Statistikblock: `{', '.join(suite_integrity['missing_statistics']) or 'keine'}`",
                f"- Conditions ohne numerische Statistikmetriken: `{', '.join(suite_integrity['empty_statistics']) or 'keine'}`",
                f"- Runtime-Fehlerläufe: `{suite_integrity['runtime_error_count']}`",
            ]
        )
    lines.extend(
        [
            "",
            "`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.",
            "",
            "## 3. Ausfuehrungsparameter",
            "",
            f"- Titel: {workflow.get('title', 'NOT_AVAILABLE')}",
            f"- Bedingungen: {workflow.get('conditions', 'NOT_AVAILABLE')}",
            f"- Notizen: {workflow.get('notes') or 'Keine.'}",
            f"- Konfiguration: `{(manifest.get('config') or {}).get('path', 'NOT_AVAILABLE') if isinstance(manifest.get('config'), dict) else 'NOT_AVAILABLE'}`",
            f"- Config SHA-256: `{(manifest.get('config') or {}).get('sha256', 'NOT_AVAILABLE') if isinstance(manifest.get('config'), dict) else 'NOT_AVAILABLE'}`",
            f"- Git Commit: `{(manifest.get('git') or {}).get('commit', 'NOT_AVAILABLE') if isinstance(manifest.get('git'), dict) else 'NOT_AVAILABLE'}`",
            f"- Git dirty: `{(manifest.get('git') or {}).get('dirty', 'NOT_AVAILABLE') if isinstance(manifest.get('git'), dict) else 'NOT_AVAILABLE'}`",
            f"- Runtime: `{(manifest.get('runtime') or {}).get('duration_seconds', 'NOT_AVAILABLE') if isinstance(manifest.get('runtime'), dict) else 'NOT_AVAILABLE'}` s",
            "",
            "## 4. Deterministische Formeln",
            "",
            "Die im Bericht verwendeten deskriptiven Groessen sind:",
            "",
            "- Mittelwert: `mean(x) = (1/n) * sum_i x_i`",
            "- Populationsstandardabweichung: `sigma = sqrt((1/n) * sum_i (x_i - mean(x))^2)`",
            "- Absolute Differenz: `Delta_x = mean(x_B) - mean(x_A)`",
            "- Verhältnis: `R_x = mean(x_B) / mean(x_A)` fuer `mean(x_A) != 0`",
            "- Inter-Spike-Intervall: `ISI_i = t_(i+1) - t_i`",
            "",
            "Diese Formeln sind deskriptiv. Ohne registrierten Inferenztest, unabhaengige Stichprobenannahme und passende Versuchsplanung werden daraus keine Signifikanz- oder Kausalbehauptungen abgeleitet.",
            "",
            "## 5. Ergebnisse nach Bedingung",
            "",
            "| Condition | n | Seeds | Ticks mean | Spikes mean | Syn. events mean | Aktivierte Neuronen mean | Recurrent events mean | Propagation depth mean |",
            "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    condition_statistics_value = statistics.get("conditions", {})
    condition_statistics: dict[str, Any] = (
        condition_statistics_value
        if isinstance(condition_statistics_value, dict)
        else {}
    )
    for condition, payload in condition_statistics.items():
        metrics = payload.get("metrics", {}) if isinstance(payload, dict) else {}

        def mean_of(name: str) -> object:
            item = metrics.get(name, {}) if isinstance(metrics, dict) else {}
            return item.get("mean") if isinstance(item, dict) else None

        lines.append(
            "| "
            + " | ".join(
                [
                    condition,
                    (
                        str(payload.get("run_count", 0))
                        if isinstance(payload, dict)
                        else "0"
                    ),
                    (
                        ",".join(map(str, payload.get("seeds", [])))
                        if isinstance(payload, dict)
                        else ""
                    ),
                    _fmt(mean_of("ticks_executed")),
                    _fmt(mean_of("total_spikes")),
                    _fmt(mean_of("delivered_synaptic_events")),
                    _fmt(mean_of("activated_neurons")),
                    _fmt(mean_of("recurrent_events")),
                    _fmt(mean_of("propagation_depth")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "**Wichtig:** `—` bedeutet in dieser Tabelle ausschließlich, dass die jeweilige SNN-Metrik für diese Bedingung nicht definiert oder nicht erhoben wird. Es bedeutet **nicht**, dass für die Bedingung keine DATA vorliegen. Protokollspezifische Messwerte werden direkt darunter ausgewiesen.",
            "",
            "### 5.1 Protokollspezifische Metrikabdeckung",
            "",
            "| Condition | zusätzliche numerische Mittelwerte |",
            "| --- | --- |",
        ]
    )
    for condition, payload in condition_statistics.items():
        means = _mean_metrics(payload)
        extras = [
            f"`{name}={_fmt(value)}`"
            for name, value in sorted(means.items())
            if name not in _PRIMARY_SUMMARY_METRICS
        ]
        lines.append(
            f"| {condition} | {'; '.join(extras) if extras else 'keine zusätzlichen numerischen Metriken'} |"
        )

    boolean_rows: list[str] = []
    for condition, payload in condition_statistics.items():
        boolean_metrics = (
            payload.get("boolean_metrics", {}) if isinstance(payload, dict) else {}
        )
        if not isinstance(boolean_metrics, dict):
            continue
        for name, values in sorted(boolean_metrics.items()):
            if not isinstance(values, dict):
                continue
            boolean_rows.append(
                f"| {condition} | `{name}` | {values.get('n', 0)} | "
                f"{values.get('true_count', 0)} | {values.get('false_count', 0)} | "
                f"{values.get('all_true', False)} |"
            )
    if boolean_rows:
        lines.extend(
            [
                "",
                "#### Primäre und weitere boolesche Endpunkte",
                "",
                "| Condition | Outcome | n | true | false | all_true |",
                "| --- | --- | ---: | ---: | ---: | --- |",
                *boolean_rows,
            ]
        )

    effects = statistics.get("two_condition_effects", {})
    if isinstance(effects, dict) and effects:
        lines.extend(["", "### 5.2 Deskriptive Zwei-Bedingungs-Effekte", ""])
        for metric, effect in effects.items():
            if isinstance(effect, dict):
                lines.append(
                    f"- `{metric}`: `absolute_difference={_fmt(effect.get('absolute_difference'))}`; `ratio={_fmt(effect.get('ratio'))}`; Referenz `{effect.get('reference_condition')}`, Vergleich `{effect.get('comparison_condition')}`."
                )

    isi = statistics.get("inter_spike_intervals", {})
    if isinstance(isi, dict) and isi:
        lines.extend(["", "### 5.3 Inter-Spike-Intervalle", ""])
        for condition, stats in isi.items():
            if isinstance(stats, dict):
                lines.append(
                    f"- `{condition}`: n={stats.get('n')}, mean={_fmt(stats.get('mean'))}, median={_fmt(stats.get('median'))}, min={_fmt(stats.get('min'))}, max={_fmt(stats.get('max'))} Ticks."
                )

    temporal = statistics.get("temporal_horizons", {})
    if isinstance(temporal, dict) and temporal:
        lines.extend(
            [
                "",
                "### 5.4 Temporal-State-Horizonte",
                "",
                "Die Diskrepanzwerte stammen aus Zustandsvergleichen gegen Referenzticks. Sie sind **keine Spike-Metrik** und koennen deshalb auch dann definiert sein, wenn `total_spikes = 0` ist. Ein solcher Lauf ist fuer Spike-basierte Aussagen quieszent, kann aber weiterhin den registrierten Zustandsvergleich ausfuehren.",
                "",
            ]
        )
        for horizon, payload in temporal.items():
            discrepancy = (
                payload.get("discrepancy", {}) if isinstance(payload, dict) else {}
            )
            nonzero = (
                payload.get("nonzero_discrepancy", {})
                if isinstance(payload, dict)
                else {}
            )
            lines.append(
                f"- `{horizon}`: Referenzvergleiche={payload.get('reference_comparisons', 0) if isinstance(payload, dict) else 0}; discrepancy mean={_fmt(discrepancy.get('mean') if isinstance(discrepancy, dict) else None)}, max={_fmt(discrepancy.get('max') if isinstance(discrepancy, dict) else None)}; nonzero={payload.get('nonzero_comparisons', 0) if isinstance(payload, dict) else 0} ({_fmt(payload.get('nonzero_fraction') if isinstance(payload, dict) else None)}); mean(nonzero)={_fmt(nonzero.get('mean') if isinstance(nonzero, dict) else None)}."
            )

    lines.extend(
        [
            "",
            "## 6. Einzelne Läufe",
            "",
            "| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |",
            "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for run in runs:
        metrics_value = run.get("metrics")
        run_metrics = dict(metrics_value) if isinstance(metrics_value, dict) else {}
        lines.append(
            "| "
            + " | ".join(
                [
                    _fmt(run.get("seed")),
                    _fmt(run.get("condition")),
                    _fmt(run_metrics.get("ticks_executed", run_metrics.get("ticks"))),
                    _fmt(run_metrics.get("total_spikes")),
                    _fmt(run_metrics.get("delivered_synaptic_events")),
                    _fmt(run_metrics.get("activated_neurons")),
                    _fmt(run_metrics.get("recurrent_events")),
                    _fmt(run_metrics.get("propagation_depth")),
                    _fmt(run.get("runtime_error")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 7. Reproduzierbarkeit und Provenienz",
            "",
            "Identische Ausgaben ueber mehrere Seeds dokumentieren reproduzierbare Modelltrajektorien unter diesen Bedingungen. Sie sind nicht automatisch statistisch unabhaengige Replikate. State-Digests sind Integritaets-/Identitaetsmarker und keine metrischen Zustandsabstaende.",
            "",
            f"Deterministische Statistikdatei: `{statistics_path.relative_to(experiment_dir).as_posix()}`",
        ]
    )
    _render_airr_sections(lines, experiment_dir, ai_report)

    lines.extend(["", "## 9. Artefakte", ""])
    for path in sorted(experiment_dir.rglob("*")):
        if path.is_file() and path.name != "summary.md":
            relative = path.relative_to(experiment_dir).as_posix()
            if relative == "DATA/runs.json":
                continue
            lines.append(f"- `{relative}`")

    lines.extend(
        [
            "",
            "## 10. Wissenschaftliche Grenze und Schlussfolgerung",
            "",
            "Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.",
            "",
            f"**Gesamtstatus:** technische Ausfuehrung `{manifest.get('experiment_status', 'unknown')}`, Tick-Vertrag `{tick_contract}`, semantische Zuordnung `{semantic_status}`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.",
            "",
        ]
    )

    summary_path = experiment_dir / "summary.md"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return f"experiments/{experiment_id}/summary.md"
