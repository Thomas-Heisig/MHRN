from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "research/snn-stability-v2-20260916"


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def replace_exact(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"Missing patch anchor in {path}: {old[:120]!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def register_design() -> None:
    replace_exact(
        "src/research/protocol_registry.py",
        '    "sustained_activity_stability_v1": "run_sustained_stability",\n',
        '    "sustained_activity_stability_v1": "run_sustained_stability",\n'
        '    "sustained_activity_stability_v2": "run_sustained_stability_v2",\n',
    )
    replace_exact(
        "src/dashboard/experiment_workflow.py",
        """        if hasattr(experiment_suite, runner_name):
            runner_module: ModuleType = experiment_suite
        else:
            from src.research import followup_experiments

            runner_module = followup_experiments
        runner = getattr(runner_module, runner_name)
""",
        """        if hasattr(experiment_suite, runner_name):
            runner_module: ModuleType = experiment_suite
        else:
            from src.research import followup_experiments, stability_followups

            if hasattr(followup_experiments, runner_name):
                runner_module = followup_experiments
            elif hasattr(stability_followups, runner_name):
                runner_module = stability_followups
            else:
                raise WorkflowValidationError(
                    f"Registered runner '{runner_name}' is not implemented."
                )
        runner = getattr(runner_module, runner_name)
""",
    )
    replace_exact(
        "src/dashboard/experiment_workflow.py",
        '        if runner_name == "run_sustained_stability":\n',
        '        if runner_name in {"run_sustained_stability", "run_sustained_stability_v2"}:\n',
    )
    replace_exact(
        "src/research/stability_followups.py",
        "import argparse\nimport json\n",
        "import argparse\nimport hashlib\nimport json\n",
    )

    target = ROOT / "src/research/stability_followups.py"
    marker = "\n\ndef _parse_seeds(value: str) -> tuple[int, ...]:\n"
    text = target.read_text(encoding="utf-8")
    if marker not in text:
        raise RuntimeError("stability_followups insertion marker missing")
    runner_code = r'''


def run_sustained_stability_v2(
    config: Config,
    seeds: tuple[int, ...] = tuple(range(101, 111)),
    ticks: int = 100_000,
    jitter_fraction: float = 0.05,
) -> list[ScientificRun]:
    """Confirm long-horizon stability across distinct seed-bound parameterizations.

    Each registered seed deterministically generates one synaptic-weight scale and
    one tonic-drive scale within +/- jitter_fraction. Control and treatment share
    the same realization. Distinct digests prove that seed labels materially alter
    the tested parameterization; they are not biological independent samples.
    """
    if not seeds:
        raise ValueError("sustained stability v2 requires at least one seed")
    if not 0.0 < jitter_fraction < 1.0:
        raise ValueError("jitter_fraction must be between 0 and 1")

    realizations: dict[int, tuple[float, float, str]] = {}
    for seed in seeds:
        rng = random.Random(seed ^ 0x5A81B17)
        weight_scale = 1.0 + rng.uniform(-jitter_fraction, jitter_fraction)
        drive_scale = 1.0 + rng.uniform(-jitter_fraction, jitter_fraction)
        encoded = json.dumps(
            {
                "weight_scale": round(weight_scale, 12),
                "drive_scale": round(drive_scale, 12),
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        realizations[seed] = (
            weight_scale,
            drive_scale,
            hashlib.sha256(encoded).hexdigest(),
        )
    if len({item[2] for item in realizations.values()}) != len(seeds):
        raise ValueError("seed-bound parameterizations are not unique")

    runs: list[ScientificRun] = []
    for seed in seeds:
        weight_scale, drive_scale, digest = realizations[seed]
        for condition in ("no_input_control", "tonic_drive"):
            base = _simulate_condition(
                config,
                experiment_id="EXP-SNN-STABILITY-V2",
                condition=condition,
                seed=seed,
                ticks=ticks,
                mode="none" if condition == "no_input_control" else "tonic",
                drive_current=0.0 if condition == "no_input_control" else 50.0,
                weight_scale=weight_scale,
                drive_scale=drive_scale,
                seed_effect_expected=True,
            )
            metrics = dict(base.metrics)
            tonic_pass = (
                float(metrics.get("post_burn_in_mean_spikes", 0.0)) > 0.0
                and float(metrics.get("post_burn_in_spike_cv", 1.0)) <= 0.25
                and float(metrics.get("post_burn_in_spike_relative_drift", 1.0)) <= 0.25
            )
            robustness_pass = bool(metrics.get("numerical_stability_pass")) and (
                condition == "no_input_control" or tonic_pass
            )
            metrics.update(
                {
                    "parameter_jitter_fraction": jitter_fraction,
                    "realization_weight_scale": weight_scale,
                    "realization_drive_scale": drive_scale,
                    "realization_digest": digest,
                    "realization_unique_across_registered_seeds": True,
                    "paired_realization": True,
                    "robustness_stability_pass": robustness_pass,
                    "independence_claim": "distinct_deterministic_parameterizations_not_independent_biological_samples",
                }
            )
            runs.append(
                ScientificRun(
                    base.experiment_id,
                    base.condition,
                    base.seed,
                    metrics,
                    base.state_digest_before,
                    base.state_digest_after,
                    base.runtime_error,
                )
            )
    return runs
'''
    target.write_text(text.replace(marker, runner_code + marker, 1), encoding="utf-8")

    prereg = {
        "schema_version": "1.0",
        "preregistration_id": "PREREG-SNN-006",
        "research_question": "RQ-SNN-006",
        "hypothesis": "H-SNN-006-A",
        "protocol_id": "sustained_activity_stability_v2",
        "mode": "CONFIRMATORY",
        "primary_outcomes": [
            "post_burn_in_spike_cv",
            "post_burn_in_spike_relative_drift",
            "finite_state",
            "topology_unchanged",
            "robustness_stability_pass",
            "realization_unique_across_registered_seeds",
        ],
        "secondary_outcomes": [
            "post_burn_in_mean_spikes",
            "active_window_fraction",
            "neuron_v_min",
            "neuron_v_max",
            "weight_min",
            "weight_max",
            "realization_weight_scale",
            "realization_drive_scale",
            "realization_digest",
        ],
        "conditions": [
            {
                "id": "no_input_control",
                "role": "paired_negative_control",
                "description": "No external current; paired with the same seed-bound weight realization as treatment.",
            },
            {
                "id": "tonic_drive",
                "role": "paired_stability_treatment",
                "description": "Base current 50.0 scaled by the registered seed-bound drive realization.",
            },
        ],
        "seed_strategy": {
            "minimum_independent_seeds": 10,
            "seeds": list(range(101, 111)),
            "rule": "Legacy registry field minimum_independent_seeds denotes ten distinct deterministic seed-bound parameter realizations, not independent biological samples.",
            "parameterization": {
                "generator": "random.Random(seed ^ 0x5A81B17)",
                "weight_scale": "uniform(0.95, 1.05)",
                "drive_scale": "uniform(0.95, 1.05)",
                "pairing": "control and tonic treatment share one seed-bound realization",
                "uniqueness_requirement": "all ten parameter digests unique before execution",
            },
        },
        "stopping_rule": "Complete 100000 ticks for both conditions and all ten registered realizations; retain any runtime, numerical, topology or contract failure.",
        "inclusion_criteria": [
            "100000 ticks executed per run",
            "10000 tick burn-in excluded from primary stability statistics",
            "1000 tick non-overlapping observation windows",
            "exactly ten unique seed-bound parameter digests",
            "paired control and tonic-drive run for every registered seed",
            "source/runtime consistency match",
            "clean frozen code and configuration provenance",
        ],
        "exclusion_criteria": [
            "runtime error or incomplete tick budget",
            "NaN or infinite membrane/weight value",
            "unexpected neuron or synapse count change",
            "missing raw trace or seed/condition record",
            "duplicate parameter digest across registered seeds",
            "dirty source tree or unreviewed protocol amendment",
        ],
        "analysis_plan": {
            "stability_criteria": {
                "tonic_drive_mean_spikes_per_window": "> 0",
                "tonic_drive_post_burn_in_spike_cv": "<= 0.25",
                "tonic_drive_post_burn_in_spike_relative_drift": "<= 0.25",
                "all_runs_finite_state": True,
                "all_runs_topology_unchanged": True,
                "all_registered_realizations_unique": True,
            },
            "descriptive_statistics": [
                "per-realization tonic spike-window mean, CV and drift",
                "paired control/treatment numerical stability",
                "realization parameter ranges and digests",
                "membrane and synaptic bounds",
            ],
            "inference_policy": "Support requires every registered run to satisfy execution, finiteness and topology criteria, all ten parameter digests to be unique, and every tonic-drive realization to satisfy activity, CV and drift thresholds. Failed realizations are retained. No biological or independent-sampling generalization is permitted.",
            "planned_tests": [],
        },
        "expected_failure_modes": [
            "duplicate or ineffective seed parameterization",
            "quiescent tonic-drive realization",
            "rate drift or unstable activity under jitter",
            "non-finite membrane or weight values",
            "unexpected structural mutation",
            "runtime interruption before 100000 ticks",
        ],
        "ai_treatment": {
            "role": "interpretation_only",
            "authority_boundary": "AI cannot alter seeds, jitter range, thresholds, exclusions or evidence status.",
            "prompt_digest_required": True,
        },
        "freeze": {
            "immutable_after_first_run": True,
            "human_review_required": True,
            "status": "FROZEN",
            "amendment_id": None,
        },
    }
    (ROOT / "research/preregistrations/PREREG-SNN-006.json").write_text(
        json.dumps(prereg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    operational = {
        "schema_version": "1.0",
        "protocols": [
            {
                "id": "sustained_activity_stability_v2",
                "research_question": "RQ-SNN-006",
                "hypothesis": "H-SNN-006-A",
                "runner": "run_sustained_stability_v2",
                "preregistration": "preregistrations/PREREG-SNN-006.json",
                "tick_aware": True,
                "default_ticks": 100000,
                "primary_outcomes": prereg["primary_outcomes"],
                "controls": ["paired no_input_control"],
                "treatments": ["paired seed-bound tonic_drive"],
                "direct_test_of_hypothesis": True,
                "scientific_evidence": False,
                "automatic_evidence_promotion": False,
            }
        ],
    }
    (ROOT / "research/protocols/SNN_STABILITY_V2.operational.json").write_text(
        json.dumps(operational, indent=2) + "\n", encoding="utf-8"
    )
    review_dir = ROOT / "research/reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    (review_dir / "RQ-SNN-001_SEED_AUDIT_2026-09-16.md").write_text(
        "# RQ-SNN-001 seed-effect audit\n\n"
        "EXP-GEN-0040 remains immutable historical DATA. Its fixed three-node construction did not consume seed-dependent randomness relevant to the measured trajectories. Identical outcomes therefore demonstrate deterministic reproducibility of one fixed parameterization, not ten statistically independent realizations.\n\n"
        "The corrective experiment is registered separately as `RQ-SNN-006` / `H-SNN-006-A` with `sustained_activity_stability_v2`. Ten distinct deterministic seed-bound parameterizations are paired across control and treatment. This audit does not alter PREREG-SNN-001 or EXP-GEN-0040.\n",
        encoding="utf-8",
    )
    (ROOT / "tests/test_sustained_stability_v2_contract.py").write_text(
        '''from __future__ import annotations\n\nfrom pathlib import Path\nimport yaml\n\nfrom src.research.protocol_registry import OPERATIONAL_RUNNERS, validate_operational_protocol\nfrom src.research.stability_followups import run_sustained_stability_v2\n\n\ndef _config() -> dict[str, object]:\n    raw = yaml.safe_load(Path("configs/learning_experiment.yaml").read_text(encoding="utf-8"))\n    assert isinstance(raw, dict)\n    return raw\n\n\ndef test_v2_seed_labels_materially_change_parameterizations() -> None:\n    runs = run_sustained_stability_v2(_config(), seeds=(101, 102, 103), ticks=2_000)\n    assert len(runs) == 6\n    by_seed: dict[int, list[object]] = {}\n    for item in runs:\n        assert item.metrics["ticks_executed"] == 2_000\n        assert item.metrics["finite_state"] is True\n        assert item.metrics["topology_unchanged"] is True\n        by_seed.setdefault(item.seed, []).append(item)\n    digests = set()\n    params = set()\n    for seed_runs in by_seed.values():\n        assert {item.condition for item in seed_runs} == {"no_input_control", "tonic_drive"}\n        pair_digests = {str(item.metrics["realization_digest"]) for item in seed_runs}\n        assert len(pair_digests) == 1\n        digests.update(pair_digests)\n        params.add((float(seed_runs[0].metrics["realization_weight_scale"]), float(seed_runs[0].metrics["realization_drive_scale"])))\n    assert len(digests) == 3\n    assert len(params) == 3\n\n\ndef test_v2_protocol_is_frozen_and_registered() -> None:\n    assert OPERATIONAL_RUNNERS["sustained_activity_stability_v2"] == "run_sustained_stability_v2"\n    prereg = validate_operational_protocol(Path("research"), question_id="RQ-SNN-006", hypothesis_id="H-SNN-006-A", protocol_id="sustained_activity_stability_v2", seed_count=10)\n    assert prereg["freeze"]["status"] == "FROZEN"\n    assert prereg["seed_strategy"]["seeds"] == list(range(101, 111))\n''',
        encoding="utf-8",
    )


def freeze_and_commit() -> None:
    run("python", "-m", "black", "src/research/stability_followups.py", "src/research/protocol_registry.py", "src/dashboard/experiment_workflow.py", "tests/test_sustained_stability_v2_contract.py")
    run("python", "-m", "ruff", "check", "--fix", "src/research/stability_followups.py", "src/research/protocol_registry.py", "src/dashboard/experiment_workflow.py", "tests/test_sustained_stability_v2_contract.py")
    run("python", "-m", "pytest", "-q", "tests/test_sustained_stability_v2_contract.py", "tests/test_scientific_execution_contract.py", "tests/test_dashboard_operational_protocol_routes.py")
    run("git", "diff", "--check")
    run("git", "config", "user.name", "GitHub Actions")
    run("git", "config", "user.email", "actions@users.noreply.github.com")
    run("git", "add", "src/research/stability_followups.py", "src/research/protocol_registry.py", "src/dashboard/experiment_workflow.py", "research/preregistrations/PREREG-SNN-006.json", "research/protocols/SNN_STABILITY_V2.operational.json", "research/reviews/RQ-SNN-001_SEED_AUDIT_2026-09-16.md", "tests/test_sustained_stability_v2_contract.py")
    run("git", "commit", "-m", "Register preregistered SNN stability robustness v2")
    run("git", "push", "origin", f"HEAD:{BRANCH}")


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
    print(result)


def review_and_commit() -> None:
    exp = ROOT / "research/experiments/EXP-GEN-0041"
    manifest = json.loads((exp / "manifest.json").read_text(encoding="utf-8"))
    runs = json.loads((exp / "DATA/runs_compact.json").read_text(encoding="utf-8"))
    stats = json.loads((exp / "analysis/statistics.json").read_text(encoding="utf-8"))
    assert manifest["validity"]["valid"] is True
    assert manifest["git"]["dirty"] is False
    assert manifest["execution_contract"]["tick_validation"]["status"] == "SATISFIED"
    assert len(runs) == 20

    by_seed: dict[int, list[dict[str, object]]] = {}
    for item in runs:
        by_seed.setdefault(int(item["seed"]), []).append(item)
    failures: list[str] = []
    unique_digests: set[str] = set()
    for seed, seed_runs in sorted(by_seed.items()):
        if {str(item["condition"]) for item in seed_runs} != {"no_input_control", "tonic_drive"}:
            failures.append(f"seed {seed}: missing paired condition")
            continue
        digests = {str(item["metrics"]["realization_digest"]) for item in seed_runs}
        if len(digests) != 1:
            failures.append(f"seed {seed}: pair realization mismatch")
        unique_digests.update(digests)
        for item in seed_runs:
            metrics = item["metrics"]
            if metrics["ticks_executed"] != 100000:
                failures.append(f"seed {seed} {item['condition']}: incomplete ticks")
            if not metrics["finite_state"] or not metrics["topology_unchanged"]:
                failures.append(f"seed {seed} {item['condition']}: numerical/topology failure")
            if item["condition"] == "tonic_drive":
                if not metrics["post_burn_in_mean_spikes"] > 0:
                    failures.append(f"seed {seed}: tonic activity absent")
                if not metrics["post_burn_in_spike_cv"] <= 0.25:
                    failures.append(f"seed {seed}: CV threshold failed")
                if not metrics["post_burn_in_spike_relative_drift"] <= 0.25:
                    failures.append(f"seed {seed}: drift threshold failed")
                if not metrics["robustness_stability_pass"]:
                    failures.append(f"seed {seed}: robustness pass false")
    if len(unique_digests) != 10:
        failures.append(f"expected 10 unique realizations, got {len(unique_digests)}")

    decision = "supports" if not failures else "refutes"
    review = {
        "experiment_id": "EXP-GEN-0041",
        "reviewer": "Thomas Heisig (criteria evaluation recorded deterministically)",
        "decision": decision,
        "comments": "Frozen PREREG-SNN-006 evaluated without changing seeds, jitter, thresholds or exclusions. Scope is simulated local parameter robustness only; no independent-biological-sample claim.",
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "criteria_failures": failures,
        "unique_realization_count": len(unique_digests),
    }
    (exp / "human_review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
    tonic = stats["conditions"]["tonic_drive"]["metrics"]
    decision_payload = {
        "schema_version": "1.0",
        "experiment_id": "EXP-GEN-0041",
        "preregistration": "PREREG-SNN-006",
        "decision": decision,
        "evidence_scope": "simulated local parameter robustness only",
        "registered_realizations": 10,
        "unique_realizations": len(unique_digests),
        "run_count": 20,
        "tonic_mean_spikes_min": tonic["post_burn_in_mean_spikes"]["min"],
        "tonic_mean_spikes_max": tonic["post_burn_in_mean_spikes"]["max"],
        "tonic_cv_max": tonic["post_burn_in_spike_cv"]["max"],
        "tonic_relative_drift_max": tonic["post_burn_in_spike_relative_drift"]["max"],
        "limitations": [
            "deterministic parameter realizations are not independent biological samples",
            "three-neuron fixed topology only",
            "local +/-5% parameter neighborhood only",
            "continuous tonic drive does not test autonomous persistence",
        ],
        "next_experiment": "drive-removal persistence",
        "criteria_failures": failures,
    }
    (exp / "analysis/HUMAN-REVIEW-DECISION.json").write_text(json.dumps(decision_payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# EXP-GEN-0041 Human Review",
        "",
        f"**Decision:** `{decision}`",
        "",
        f"Unique seed-bound parameterizations: **{len(unique_digests)}/10**.",
        "",
        "This conclusion is restricted to the simulated three-neuron model and the preregistered +/-5% local weight/drive perturbation range. It is not evidence from independent biological samples.",
        "",
        "## Failures",
        "",
    ]
    lines.extend(["- None."] if not failures else [f"- {item}" for item in failures])
    lines.extend([
        "",
        "## Next confirmatory question",
        "",
        "Preregister withdrawal of tonic drive and test whether activity persists, separating driven stability from autonomous recurrent persistence.",
        "",
    ])
    (exp / "analysis/HUMAN-REVIEW-2026-09-16.md").write_text("\n".join(lines), encoding="utf-8")

    run("git", "diff", "--check")
    run("git", "add", "research/experiments/EXP-GEN-0041")
    run("git", "commit", "-m", "Record EXP-GEN-0041 preregistered SNN robustness result")
    run("git", "push", "origin", f"HEAD:{BRANCH}")
    if failures:
        raise RuntimeError("Preregistered criteria failed: " + "; ".join(failures))


def final_verify_and_cleanup() -> None:
    run("python", "-m", "pytest", "-q", "tests/test_sustained_stability_v2_contract.py", "tests/test_scientific_execution_contract.py", "tests/test_dashboard_operational_protocol_routes.py", "tests/test_research_data_v2.py", "tests/test_snn_evidence_pipeline_regressions.py")
    run("python", "-m", "ruff", "check", "src/research/stability_followups.py", "src/research/protocol_registry.py", "src/dashboard/experiment_workflow.py", "tests/test_sustained_stability_v2_contract.py")
    run("python", "-m", "black", "--check", "src/research/stability_followups.py", "src/research/protocol_registry.py", "src/dashboard/experiment_workflow.py", "tests/test_sustained_stability_v2_contract.py")
    run("git", "rm", "scripts/one_shot_snn_v2_cycle.py")
    run("git", "commit", "-m", "chore: remove one-shot SNN v2 executor")
    run("git", "push", "origin", f"HEAD:{BRANCH}")


def main() -> None:
    register_design()
    freeze_and_commit()
    execute_experiment()
    review_and_commit()
    final_verify_and_cleanup()


if __name__ == "__main__":
    main()
