from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "research/snn-stability-v2-20260916"


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def append_registry_entries() -> None:
    questions = ROOT / "research/registry/questions.yaml"
    q_text = questions.read_text(encoding="utf-8")
    if "- id: RQ-SNN-006\n" not in q_text:
        q_text += """
- id: RQ-SNN-006
  domain: Spiking Neural Networks
  question: Bleibt die unter RQ-SNN-001 beobachtete Langzeitstabilitaet unter vorab definierten lokalen Variationen von synaptischem Gewicht und Tonic-Drive erhalten?
  relevance: Trennt die deterministische Stabilitaet einer festen Parameterisierung von lokaler Robustheit ueber tatsaechlich unterschiedliche, seed-gebundene Modellparameterisierungen.
  literature:
  - SRC-IZHIKEVICH-2003
  - SRC-GERSTNER-2014
  hypotheses:
  - H-SNN-006-A
  evidence: []
  status: open
  answer:
    current: null
    confidence: none
    limitations: null
  created: '2026-09-16'
  updated: '2026-09-16'
"""
        questions.write_text(q_text, encoding="utf-8")

    hypotheses = ROOT / "research/registry/hypotheses.yaml"
    h_text = hypotheses.read_text(encoding="utf-8")
    if "- id: H-SNN-006-A\n" not in h_text:
        h_text += """
- id: H-SNN-006-A
  research_question: RQ-SNN-006
  hypothesis: Alle zehn vorab registrierten, unterschiedlichen seed-gebundenen Parameterrealisierungen bleiben ueber 100.000 Ticks numerisch und topologisch stabil; unter gepaartem Tonic-Drive bleibt die post-burn-in Aktivitaet positiv mit CV und relativer Drift jeweils <= 0.25.
  status: untested
  evidence: []
  created: '2026-09-16'
  updated: '2026-09-16'
"""
        hypotheses.write_text(h_text, encoding="utf-8")


def commit_registry_before_run() -> None:
    from src.research.registry import ResearchRegistry

    registry = ResearchRegistry(ROOT / "research/registry").load_all()
    question = registry.questions.get("RQ-SNN-006")
    hypothesis = registry.hypotheses.get("H-SNN-006-A")
    assert question is not None
    assert hypothesis is not None
    assert hypothesis.research_question == question.id

    run("git", "config", "user.name", "GitHub Actions")
    run("git", "config", "user.email", "actions@users.noreply.github.com")
    run("git", "add", "research/registry/questions.yaml", "research/registry/hypotheses.yaml")
    if subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=ROOT, check=False
    ).returncode != 0:
        run("git", "commit", "-m", "Register RQ-SNN-006 robustness hypothesis")
        run("git", "push", "origin", f"HEAD:{BRANCH}")
    run("git", "diff", "--check")
    if subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip():
        raise RuntimeError("working tree must be clean before EXP-GEN-0041")


def validate_frozen_contract() -> None:
    run(
        "python",
        "-m",
        "pytest",
        "-q",
        "tests/test_sustained_stability_v2_contract.py",
        "tests/test_scientific_execution_contract.py",
        "tests/test_dashboard_operational_protocol_routes.py",
    )


def execute_experiment() -> None:
    from src.dashboard.experiment_workflow import ExperimentWorkflowService

    result = ExperimentWorkflowService(ROOT / "research").run_science(
        {
            "experiment_id": "EXP-GEN-0041",
            "question_id": "RQ-SNN-006",
            "hypothesis_id": "H-SNN-006-A",
            "title": "sustained_activity_stability_v2 — seed-bound robustness",
            "conditions": "paired no_input_control and tonic_drive across ten distinct seed-bound parameterizations",
            "ticks": 100000,
            "seeds": "101-110",
            "notes": "First execution after frozen PREREG-SNN-006; no post-hoc threshold or parameter changes.",
            "protocol": "sustained_activity_stability_v2",
        }
    )
    print(json.dumps(result, indent=2, default=str))


def evaluate_preregistered_criteria() -> None:
    exp = ROOT / "research/experiments/EXP-GEN-0041"
    manifest = json.loads((exp / "manifest.json").read_text(encoding="utf-8"))
    runs = json.loads((exp / "DATA/runs_compact.json").read_text(encoding="utf-8"))
    stats = json.loads((exp / "analysis/statistics.json").read_text(encoding="utf-8"))

    assert manifest["experiment_status"] == "completed"
    assert manifest["validity"]["valid"] is True
    assert manifest["git"]["dirty"] is False
    assert manifest["execution_contract"]["tick_validation"]["status"] == "SATISFIED"
    assert manifest["execution_contract"]["protocol"] == "sustained_activity_stability_v2"
    assert len(runs) == 20
    assert {int(item["seed"]) for item in runs} == set(range(101, 111))

    by_seed: dict[int, list[dict[str, object]]] = {}
    for item in runs:
        by_seed.setdefault(int(item["seed"]), []).append(item)

    failures: list[str] = []
    unique_digests: set[str] = set()
    weight_scales: list[float] = []
    drive_scales: list[float] = []
    tonic_means: list[float] = []
    tonic_cvs: list[float] = []
    tonic_drifts: list[float] = []

    for seed, seed_runs in sorted(by_seed.items()):
        if {str(item["condition"]) for item in seed_runs} != {
            "no_input_control",
            "tonic_drive",
        }:
            failures.append(f"seed {seed}: missing paired condition")
            continue
        pair_digests = {
            str(item["metrics"]["realization_digest"]) for item in seed_runs
        }
        if len(pair_digests) != 1:
            failures.append(f"seed {seed}: paired realization digest mismatch")
        unique_digests.update(pair_digests)

        first_metrics = seed_runs[0]["metrics"]
        weight_scales.append(float(first_metrics["realization_weight_scale"]))
        drive_scales.append(float(first_metrics["realization_drive_scale"]))

        for item in seed_runs:
            metrics = item["metrics"]
            condition = str(item["condition"])
            if int(metrics["ticks_executed"]) != 100000:
                failures.append(f"seed {seed} {condition}: incomplete ticks")
            if metrics["finite_state"] is not True:
                failures.append(f"seed {seed} {condition}: non-finite state")
            if metrics["topology_unchanged"] is not True:
                failures.append(f"seed {seed} {condition}: topology changed")
            if metrics["realization_unique_across_registered_seeds"] is not True:
                failures.append(f"seed {seed}: uniqueness flag false")
            if condition == "tonic_drive":
                mean_spikes = float(metrics["post_burn_in_mean_spikes"])
                cv = float(metrics["post_burn_in_spike_cv"])
                drift = float(metrics["post_burn_in_spike_relative_drift"])
                tonic_means.append(mean_spikes)
                tonic_cvs.append(cv)
                tonic_drifts.append(drift)
                if mean_spikes <= 0.0:
                    failures.append(f"seed {seed}: tonic activity absent")
                if cv > 0.25:
                    failures.append(f"seed {seed}: CV threshold failed ({cv})")
                if drift > 0.25:
                    failures.append(f"seed {seed}: drift threshold failed ({drift})")
                if metrics["robustness_stability_pass"] is not True:
                    failures.append(f"seed {seed}: robustness_stability_pass false")

    if len(unique_digests) != 10:
        failures.append(
            f"expected 10 unique seed-bound realizations, got {len(unique_digests)}"
        )

    decision = "criteria_satisfied" if not failures else "criteria_failed"
    evaluation = {
        "schema_version": "1.0",
        "experiment_id": "EXP-GEN-0041",
        "preregistration": "PREREG-SNN-006",
        "automated_criteria_evaluation": decision,
        "human_review_status": "PENDING",
        "scientific_evidence_promoted": False,
        "registered_realizations": 10,
        "unique_realizations": len(unique_digests),
        "run_count": 20,
        "criteria_failures": failures,
        "observed_ranges": {
            "weight_scale": [min(weight_scales), max(weight_scales)],
            "drive_scale": [min(drive_scales), max(drive_scales)],
            "tonic_post_burn_in_mean_spikes": [min(tonic_means), max(tonic_means)],
            "tonic_spike_cv": [min(tonic_cvs), max(tonic_cvs)],
            "tonic_relative_drift": [min(tonic_drifts), max(tonic_drifts)],
        },
        "statistics_schema": stats.get("schema_version"),
        "scope": "simulated three-neuron local parameter robustness only",
        "limitations": [
            "deterministic pseudo-random parameter realizations are not independent biological samples",
            "fixed three-neuron topology",
            "local +/-5% weight/drive parameter neighborhood only",
            "continuous tonic drive tests driven stability, not autonomous persistence",
        ],
        "next_preregistered_target": "drive-removal persistence",
    }
    analysis = exp / "analysis"
    (analysis / "PREREGISTERED-CRITERIA-EVALUATION.json").write_text(
        json.dumps(evaluation, indent=2) + "\n", encoding="utf-8"
    )
    review_lines = [
        "# EXP-GEN-0041 — Human Review Candidate",
        "",
        f"Automated preregistered-criteria result: **{decision}**",
        "",
        "Human review remains **PENDING**. This document is a review candidate and does not represent a human decision.",
        "",
        f"- Unique seed-bound realizations: `{len(unique_digests)}/10`",
        f"- Runs: `20`",
        f"- Tick contract: `{manifest['execution_contract']['tick_validation']['status']}`",
        f"- Tonic mean spikes/window range: `{min(tonic_means):.6g} .. {max(tonic_means):.6g}`",
        f"- Maximum tonic CV: `{max(tonic_cvs):.6g}`",
        f"- Maximum tonic relative drift: `{max(tonic_drifts):.6g}`",
        "",
        "## Scope",
        "",
        "The result can only address robustness of this simulated three-neuron model within the preregistered local +/-5% weight/drive parameter neighborhood. It is not evidence from independent biological samples.",
        "",
        "## Criteria failures",
        "",
    ]
    review_lines.extend(["- None."] if not failures else [f"- {item}" for item in failures])
    review_lines.extend(
        [
            "",
            "## Next experiment",
            "",
            "Preregister a drive-removal protocol to test whether activity persists after tonic input is withdrawn. This distinguishes driven stability from autonomous recurrent persistence.",
            "",
        ]
    )
    (analysis / "HUMAN-REVIEW-CANDIDATE-2026-09-16.md").write_text(
        "\n".join(review_lines), encoding="utf-8"
    )

    if failures:
        raise RuntimeError("Preregistered criteria failed: " + "; ".join(failures))


def commit_experiment() -> None:
    run("git", "diff", "--check")
    run("git", "add", "research/experiments/EXP-GEN-0041")
    run("git", "commit", "-m", "Record EXP-GEN-0041 preregistered SNN robustness data")
    run("git", "push", "origin", f"HEAD:{BRANCH}")


def final_verify() -> None:
    run(
        "python",
        "-m",
        "pytest",
        "-q",
        "tests/test_sustained_stability_v2_contract.py",
        "tests/test_scientific_execution_contract.py",
        "tests/test_dashboard_operational_protocol_routes.py",
        "tests/test_research_data_v2.py",
        "tests/test_snn_evidence_pipeline_regressions.py",
    )
    run(
        "python",
        "-m",
        "ruff",
        "check",
        "src/research/stability_followups.py",
        "src/research/protocol_registry.py",
        "src/dashboard/experiment_workflow.py",
        "tests/test_sustained_stability_v2_contract.py",
    )
    run(
        "python",
        "-m",
        "black",
        "--check",
        "src/research/stability_followups.py",
        "src/research/protocol_registry.py",
        "src/dashboard/experiment_workflow.py",
        "tests/test_sustained_stability_v2_contract.py",
    )


def cleanup_helpers() -> None:
    removable = [
        path
        for path in (
            "scripts/one_shot_snn_v2_cycle.py",
            "scripts/one_shot_snn_v2_resume.py",
        )
        if (ROOT / path).exists()
    ]
    if removable:
        run("git", "rm", *removable)
        run("git", "commit", "-m", "chore: remove one-shot SNN v2 executors")
        run("git", "push", "origin", f"HEAD:{BRANCH}")


def main() -> None:
    append_registry_entries()
    commit_registry_before_run()
    validate_frozen_contract()
    execute_experiment()
    evaluate_preregistered_criteria()
    commit_experiment()
    final_verify()
    cleanup_helpers()


if __name__ == "__main__":
    main()
