"""Run frozen exploratory V4 to an external, new output directory."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import os
import platform
import statistics
import subprocess
import sys
import time
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

from src.research.connectome_embodiment import _simulate  # noqa: E402


def save(path, value):
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def git(*args):
    return (
        subprocess.check_output(
            ["git", "-c", f"safe.directory={ROOT.as_posix()}", *args], cwd=ROOT
        )
        .decode()
        .strip()
    )


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    out = parser.parse_args().output.resolve()
    if out.is_relative_to(ROOT):
        raise ValueError("Output must be outside the tested checkout")
    if git("status", "--porcelain"):
        raise ValueError("Clean committed source required")
    p = ROOT / "research/preregistrations/PREREG-EMB001B-UNSEEN-V4.json"
    protocol = json.loads(p.read_text())
    config_path = ROOT / "configs/learning_experiment.yaml"
    config = yaml.safe_load(config_path.read_text())
    out.mkdir(parents=True, exist_ok=False)
    save(
        out / "freeze.json",
        {
            "commit": git("rev-parse", "HEAD"),
            "tree": git("rev-parse", "HEAD^{tree}"),
            "utc_before_execution": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "command": [sys.executable, *sys.argv],
            "PYTHONHASHSEED": os.environ.get("PYTHONHASHSEED"),
            "protocol": protocol,
            "status_before": "",
            "hashes": {
                str(f.relative_to(ROOT)): sha(f)
                for f in [
                    p,
                    config_path,
                    Path(__file__),
                    *sorted((ROOT / "src").rglob("*.py")),
                ]
            },
        },
    )
    (out / "pip-freeze.txt").write_text(
        subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze", "--all"]
        ).decode(),
        encoding="utf-8",
        newline="\n",
    )
    results, integrity = [], []
    started = time.monotonic()
    for seed in protocol["seeds"]:
        ticks = protocol["ticks"]
        schedule = tuple(
            (0.003 if seed % 2 == 0 else -0.003) if 250 <= t < 500 else 0.0
            for t in range(ticks)
        )
        donor = _simulate(config, seed, ticks, "closed_loop", perturb=False)
        save(out / f"donor-{seed}.json", asdict(donor))
        runs = {
            "donor_unperturbed": donor,
            "yoked_unperturbed": _simulate(
                config, seed, ticks, "yoked_replay", donor=donor, perturb=False
            ),
            "closed_challenge": _simulate(
                config, seed, ticks, "closed_loop", external_torque_schedule=schedule
            ),
            "yoked_challenge": _simulate(
                config,
                seed,
                ticks,
                "yoked_replay",
                donor=donor,
                external_torque_schedule=schedule,
            ),
            "feedback_absent_challenge": _simulate(
                config,
                seed,
                ticks,
                "feedback_absent",
                external_torque_schedule=schedule,
            ),
            "pd_challenge": _simulate(
                config,
                seed,
                ticks,
                "controller_only",
                external_torque_schedule=schedule,
            ),
        }
        y = runs["yoked_challenge"]
        checks = {
            "complete": all(
                r.error is None and r.metrics["ticks_executed"] == ticks
                for r in runs.values()
            ),
            "initial_neural_equal": len({r.before for r in runs.values()}) == 1,
            "initial_body_equal": all(
                r.metrics["gateway_state_before"]
                == donor.metrics["gateway_state_before"]
                for r in runs.values()
            ),
            "graph_equal": all(
                r.metrics["graph"] == donor.metrics["graph"] for r in runs.values()
            ),
            "sentinel_exact": runs["yoked_unperturbed"].metrics["trace"]
            == donor.metrics["trace"],
            "donor_observations_exact": [
                (r["observed_q_rad"], r["observed_omega_rad_s"])
                for r in y.metrics["trace"]
            ]
            == donor.sensor_tape,
            "yoked_commands_unchanged": y.motor_tape == donor.motor_tape,
            "body_responds_to_disturbance": y.sensor_tape != donor.sensor_tape,
            "absent_zero": all(
                r["observed_q_rad"] == r["observed_omega_rad_s"] == 0
                for r in runs["feedback_absent_challenge"].metrics["trace"]
            ),
        }
        integrity.append({"seed": seed, "checks": checks})
        for condition, run in runs.items():
            trace = run.metrics["trace"][250:]
            rmse = math.sqrt(
                statistics.mean((r["target_rad"] - r["q_rad"]) ** 2 for r in trace)
            )
            results.append(
                {
                    "seed": seed,
                    "condition": condition,
                    "post_disturbance_rmse": rmse,
                    "full_rmse": run.metrics["tracking_rmse_rad"],
                    "error": run.error,
                }
            )
        save(
            out / f"runs-{seed}.json",
            {"schedule": schedule, "runs": {k: asdict(v) for k, v in runs.items()}},
        )
        save(out / "integrity.json", integrity)
        save(out / "outcomes.json", results)
        if (
            time.monotonic() - started > 600
            or sum(f.stat().st_size for f in out.iterdir()) > 100000000
        ):
            raise RuntimeError(
                "Frozen resource ceiling exceeded; partial outputs retained"
            )
    differences = []
    for seed in protocol["seeds"]:
        rows = {r["condition"]: r for r in results if r["seed"] == seed}
        differences.append(
            {
                "seed": seed,
                "difference": rows["yoked_challenge"]["post_disturbance_rmse"]
                - rows["closed_challenge"]["post_disturbance_rmse"],
            }
        )
    summary = {}
    for name, selected in (
        ("pooled", differences),
        ("positive_torque", [r for r in differences if r["seed"] % 2 == 0]),
        ("negative_torque", [r for r in differences if r["seed"] % 2]),
    ):
        values = [r["difference"] for r in selected]
        summary[name] = {
            "n": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "positive": sum(v > 0 for v in values),
            "zero": values.count(0),
            "negative": sum(v < 0 for v in values),
        }
    valid = all(all(row["checks"].values()) for row in integrity) and not git(
        "status", "--porcelain"
    )
    save(
        out / "result.json",
        {
            "valid": valid,
            "status_after": git("status", "--porcelain"),
            "paired_differences": differences,
            "summary": summary,
            "scientific_evidence": False,
        },
    )
    save(out / "sha256sums.json", {f.name: sha(f) for f in sorted(out.iterdir())})
    print(json.dumps({"valid": valid, "summary": summary}, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
