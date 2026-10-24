"""Verify archived V4 bytes and recompute the primary outcome from traces."""

import hashlib
import json
import math
import statistics
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/experiments/EXP-EMB001B-UNSEEN-V4-20261024"


def main():
    archive = json.loads((OUT / "archive-index.json").read_text())
    assert (
        hashlib.sha256((OUT / archive["archive"]).read_bytes()).hexdigest()
        == archive["sha256"]
    )
    freeze = json.loads((OUT / "freeze.json").read_text())
    git = ["git", "-c", f"safe.directory={ROOT.as_posix()}"]
    for name, expected in freeze["hashes"].items():
        name = name.replace("\\", "/")
        blob = subprocess.check_output(
            git + ["show", freeze["commit"] + ":" + name], cwd=ROOT
        )
        assert hashlib.sha256(blob).hexdigest() == expected, name
    outcomes = json.loads((OUT / "outcomes.json").read_text())
    assert len(outcomes) == 120
    differences = []
    with zipfile.ZipFile(OUT / archive["archive"]) as z:
        for name, expected in json.loads((OUT / "sha256sums.json").read_text()).items():
            data = (
                z.read(name)
                if name in archive["members"]
                else (OUT / name).read_bytes()
            )
            assert hashlib.sha256(data).hexdigest() == expected, name
        for seed in freeze["protocol"]["seeds"]:
            raw = json.loads(z.read(f"runs-{seed}.json"))
            assert set(raw["runs"]) == set(freeze["protocol"]["conditions"])
            donor = raw["runs"]["donor_unperturbed"]
            assert donor == json.loads(z.read(f"donor-{seed}.json"))
            assert raw["schedule"] == [
                (0.003 if seed % 2 == 0 else -0.003) if 250 <= t < 500 else 0.0
                for t in range(1000)
            ]
            values = {}
            for condition, run in raw["runs"].items():
                trace = run["metrics"]["trace"]
                assert run["error"] is None and len(trace) == 1000
                assert run["before"] == donor["before"]
                assert run["metrics"]["graph"] == donor["metrics"]["graph"]
                assert (
                    run["metrics"]["gateway_state_before"]
                    == donor["metrics"]["gateway_state_before"]
                )
                value = math.sqrt(
                    statistics.mean(
                        (r["target_rad"] - r["q_rad"]) ** 2 for r in trace[250:]
                    )
                )
                row = next(
                    r
                    for r in outcomes
                    if r["seed"] == seed and r["condition"] == condition
                )
                assert value == row["post_disturbance_rmse"]
                values[condition] = value
            yoke = raw["runs"]["yoked_challenge"]
            assert (
                raw["runs"]["yoked_unperturbed"]["metrics"]["trace"]
                == donor["metrics"]["trace"]
            )
            assert [
                [r["observed_q_rad"], r["observed_omega_rad_s"]]
                for r in yoke["metrics"]["trace"]
            ] == donor["sensor_tape"]
            assert yoke["motor_tape"] == donor["motor_tape"]
            assert yoke["sensor_tape"] != donor["sensor_tape"]
            assert all(
                r["observed_q_rad"] == r["observed_omega_rad_s"] == 0
                for r in raw["runs"]["feedback_absent_challenge"]["metrics"]["trace"]
            )
            differences.append(
                {
                    "seed": seed,
                    "difference": values["yoked_challenge"]
                    - values["closed_challenge"],
                }
            )
    result = json.loads((OUT / "result.json").read_text())
    assert result["valid"] and result["status_after"] == ""
    assert differences == result["paired_differences"]
    assert (
        statistics.mean(r["difference"] for r in differences)
        == result["summary"]["pooled"]["mean"]
    )
    print(
        "PASS: source bindings, archived hashes, 120 raw runs, causal controls and paired primary outcomes"
    )


if __name__ == "__main__":
    main()
