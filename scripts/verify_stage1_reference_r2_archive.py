"""Verify archived R2 bytes and replay only the frozen analysis, never simulation."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "research/experiments/EXP-S1-TOPO-REFERENCE-R2-20261024"


def main() -> None:
    checksums = json.loads((ARTIFACTS / "sha256sums.json").read_text(encoding="utf-8"))
    for name, digest in checksums.items():
        path = ARTIFACTS / name
        assert path.resolve().parent == ARTIFACTS.resolve()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, name
    index = json.loads((ARTIFACTS / "archive-index.json").read_text(encoding="utf-8"))
    with zipfile.ZipFile(ARTIFACTS / "raw-data-and-provenance.zip") as archive:
        assert sorted(archive.namelist()) == sorted(index)
        for name, entry in index.items():
            content = archive.read(name)
            assert len(content) == entry["bytes"], name
            assert hashlib.sha256(content).hexdigest() == entry["sha256"], name
        auth = json.loads(archive.read("execution-authorization.json"))
        source_commit = auth["source_commit"]
        for name, expected in auth["checked_bound_files"].items():
            content = subprocess.check_output(
                ["git", "show", f"{source_commit}:{name}"], cwd=ROOT
            )
            assert hashlib.sha256(content).hexdigest() == expected, name
        assert (
            hashlib.sha256(archive.read("run_reference_r2_20261024.py")).hexdigest()
            == auth["driver_sha256"]
        )
        expected_analysis = json.loads(archive.read("analysis.json"))
        with tempfile.TemporaryDirectory(
            prefix="mhrn-reference-r2-analysis-"
        ) as directory:
            target = Path(directory)
            for name in (
                "scripts/verify_stage1_topology_reference_r2.py",
                "research/preregistrations/PREREG-S1-TOPO-REFERENCE-R2.json",
            ):
                path = target / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(
                    subprocess.check_output(
                        ["git", "show", f"{source_commit}:{name}"], cwd=ROOT
                    )
                )
            raw_path = target / "reference-data.json"
            raw_path.write_bytes(archive.read("reference-data.json"))
            result_path = target / "analysis.json"
            subprocess.run(
                [
                    sys.executable,
                    str(target / "scripts/verify_stage1_topology_reference_r2.py"),
                    "--data",
                    str(raw_path),
                    "--output",
                    str(result_path),
                ],
                check=True,
            )
            reproduced = json.loads(result_path.read_text(encoding="utf-8"))
            reproduced.pop("reference_data")
            expected_analysis.pop("reference_data")
            assert reproduced == expected_analysis
    print("PASS: archived bytes, frozen source bindings and exact analysis replay")


if __name__ == "__main__":
    main()
