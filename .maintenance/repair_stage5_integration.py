"""Apply the six-file, reviewed integration repair without touching other work.

Only unique preimages are accepted. This script is run in an isolated GitHub
checkout; formatting uses the repository-pinned Black/Ruff versions. It neither
changes tests' assertions nor rewrites research DATA or evidence status.
"""

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, before: str, after: str) -> None:
    target = ROOT / path
    source = target.read_text(encoding="utf-8")
    if after in source and before not in source:
        return
    if source.count(before) != 1:
        raise RuntimeError(f"preimage is not unique: {path}: {before!r}")
    target.write_text(source.replace(before, after, 1), encoding="utf-8")


def main() -> None:
    replace_once(
        "src/embodiment/integrated_nervous_system.py",
        "STAGE5_REFERENCE_EXPERIMENT = (",
        "from .models import JSONValue\n\nSTAGE5_REFERENCE_EXPERIMENT = (",
    )
    replace_once(
        "src/embodiment/integrated_nervous_system.py",
        "    readings = {",
        "    readings: dict[str, JSONValue] = {",
    )
    replace_once(
        "src/embodiment/specialized_areas.py",
        "        feature_values = [float(value) for value in features]",
        "        feature_values = list(self._numeric_payload(features))",
    )
    replace_once(
        "src/embodiment/specialized_areas.py",
        '        "topology_edge_sample": network.edge_sample(),',
        '        "topology_edge_sample": [item for item in network.edge_sample()],',
    )
    replace_once(
        "src/dashboard/server.py",
        "            forschungsbericht = None\n            for fb_name",
        "            forschungsbericht: dict[str, JSONValue] | None = None\n            for fb_name",
    )
    replace_once(
        "src/dashboard/server.py",
        '            exports = []\n            for ext in (".pdf", ".docx"):',
        '            exports: list[JSONValue] = []\n            for ext in (".pdf", ".docx"):',
    )
    targets = [
        "src/embodiment/integrated_nervous_system.py",
        "src/embodiment/specialized_areas.py",
        "src/dashboard/server.py",
        "scripts/apply_stage5_timeline.py",
        "scripts/run_stage5_reference.py",
        "tests/test_stage5_frontend_contract.py",
    ]
    subprocess.run(["python", "-m", "black", *targets], cwd=ROOT, check=True)
    subprocess.run(["python", "-m", "ruff", "check", *targets], cwd=ROOT, check=True)
    changed = subprocess.check_output(
        ["git", "diff", "--name-only"], cwd=ROOT, text=True
    ).splitlines()
    if not set(changed) <= set(targets):
        raise RuntimeError(f"repair changed unexpected paths: {changed}")


if __name__ == "__main__":
    main()
