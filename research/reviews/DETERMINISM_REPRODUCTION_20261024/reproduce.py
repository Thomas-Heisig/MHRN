"""Source-bound reproduction; invoke with CLEAN_CHECKOUT OUTPUT_DIRECTORY."""
import dataclasses
import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


root = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
if len(sys.argv) > 3 and sys.argv[3] == "--worker":
    sys.path.insert(0, str(root))
    import yaml
    from src.research.experiment_suite import run_ping_v2
    config = yaml.safe_load((root / "configs/learning_experiment.yaml").read_text(encoding="utf-8"))
    write(output, [dataclasses.asdict(run) for run in run_ping_v2(config, seeds=(101, 102, 103), ticks=256)])
    sys.exit(0)

output.mkdir(parents=True, exist_ok=False)


def git(*args):
    return subprocess.check_output(["git", "-c", f"safe.directory={root.as_posix()}", "-c", "core.autocrlf=false", *args], cwd=root).decode("utf-8").strip()


assert not git("status", "--porcelain", "--untracked-files=all"), "Checkout must be clean"
files = {}
for line in git("ls-files", "-s", "src", "configs").splitlines():
    metadata, name = line.split("\t", 1)
    blob = metadata.split()[1]
    data = (root / name).read_bytes()
    actual_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual_blob == blob, f"Non-exact source bytes: {name}"
    files[name] = {"git_blob": blob, "sha256": digest(data)}
historical = root / "research/experiments/EXP-BATCH-20260914074039-03"
config_hash = files["configs/learning_experiment.yaml"]["sha256"]
old_manifest = json.loads((historical / "manifest.json").read_text())
assert config_hash == old_manifest["config"]["sha256"], "Historical config differs"
freeze = {
    "created_before_execution_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "commit": git("rev-parse", "HEAD"), "tree": git("rev-parse", "HEAD^{tree}"),
    "status_before": git("status", "--porcelain", "--untracked-files=all"),
    "source_and_config": files, "config_matches_historical": True,
    "protocol": "deterministic_replica_v1", "runner": "src.research.experiment_suite.run_ping_v2",
    "seeds": [101, 102, 103], "ticks": 256,
    "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
    "machine": platform.machine(), "processor": platform.processor(),
    "harness_sha256": digest(Path(__file__).read_bytes()),
    "command": [sys.executable, *sys.argv],
    "comparison": "All metrics plus before/after state digests in A/B pairs; historical four manuscript totals; full output across fresh processes",
    "scientific_evidence": False,
}
write(output / "freeze.json", freeze)
(output / "pip-freeze.txt").write_bytes(subprocess.check_output([sys.executable, "-m", "pip", "freeze", "--all"]))
processes = []
for hashseed in (0, 1, 42):
    target = output / f"runs-hashseed-{hashseed}.json"
    command = [sys.executable, "-B", str(Path(__file__).resolve()), str(root), str(target), "--worker"]
    env = dict(os.environ, PYTHONHASHSEED=str(hashseed), PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run(command, cwd=root, env=env, capture_output=True)
    (output / f"stdout-{hashseed}.txt").write_bytes(result.stdout)
    (output / f"stderr-{hashseed}.txt").write_bytes(result.stderr)
    processes.append({"command": command, "PYTHONHASHSEED": hashseed, "exit_code": result.returncode})
    write(output / "processes.json", processes)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors="replace"))

runs = json.loads((output / "runs-hashseed-0.json").read_text())
checks = []
keys = ("total_spikes", "delivered_synaptic_events", "recurrent_events", "propagation_depth")
for seed in (101, 102, 103):
    for arm, expected in (("recurrence_off", [3, 2, 0, 1]), ("recurrence_on", [33, 33, 10, 61])):
        a, b = [next(r for r in runs if r["seed"] == seed and r["condition"] == f"{arm}_replica_{replica}") for replica in ("a", "b")]
        old = json.loads(gzip.decompress(next((historical / "DATA/raw").glob(f"*{arm}_replica_a-seed-{seed}.json.gz")).read_bytes()))
        checks.append({"seed": seed, "arm": arm,
                       "all_metrics_equal": a["metrics"] == b["metrics"],
                       "initial_state_equal": a["state_digest_before"] == b["state_digest_before"],
                       "final_state_equal": a["state_digest_after"] == b["state_digest_after"],
                       "ticks_satisfied": a["metrics"]["ticks_executed"] == b["metrics"]["ticks_executed"] == 256,
                       "no_runtime_errors": a["runtime_error"] is None and b["runtime_error"] is None,
                       "observed": [a["metrics"][key] for key in keys], "expected": expected,
                       "historical_totals": [old["metrics"][key] for key in keys]})
equal_processes = len({digest((output / f"runs-hashseed-{seed}.json").read_bytes()) for seed in (0, 1, 42)}) == 1
status_after = git("status", "--porcelain", "--untracked-files=all")
passed = equal_processes and not status_after and all(all(c[k] for k in ("all_metrics_equal", "initial_state_equal", "final_state_equal", "ticks_satisfied", "no_runtime_errors")) and c["observed"] == c["expected"] == c["historical_totals"] for c in checks)
write(output / "result.json", {"passed": passed, "checks": checks, "fresh_process_outputs_identical": equal_processes, "status_after": status_after, "metric_order": keys, "run_count": 36, "pair_count": 18})
write(output / "sha256sums.json", {p.name: digest(p.read_bytes()) for p in sorted(output.iterdir()) if p.is_file()})
print(json.dumps({"passed": passed, "checks": checks, "fresh_process_outputs_identical": equal_processes}, indent=2))
sys.exit(0 if passed else 1)
