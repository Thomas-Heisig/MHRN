"""Execute a source-frozen audit; technical completion is never EVID acceptance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "work/scientific-main-audit-20260913"
CAMPAIGN = "EXP-EMP-20260913-A3"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("Audit output must be outside the source checkout")
    output.mkdir(parents=True, exist_ok=False)
    source = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    records: list[dict[str, Any]] = []
    protected = {
        path: hashlib.sha256(path.read_bytes()).hexdigest()
        for folder in (
            "research/experiments",
            "research/publications",
            "research/preregistrations",
            "research/registry/evidence",
        )
        for path in (ROOT / folder).rglob("*")
        if path.is_file()
    }

    def run(name: str, command: list[str], timeout: int = 1800) -> int:
        log = output / (name + ".log")
        with log.open("w", encoding="utf-8") as stream:
            try:
                result = subprocess.run(
                    command,
                    cwd=ROOT,
                    stdout=stream,
                    stderr=subprocess.STDOUT,
                    timeout=timeout,
                    check=False,
                )
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 124
        records.append(
            {"name": name, "command": command, "exit_code": code, "log": log.name}
        )
        print(f"{name}: {code}", flush=True)
        return code

    campaign = output / CAMPAIGN
    published = ROOT / "research" / "experiments" / CAMPAIGN
    if published.exists():
        raise ValueError("This campaign already exists; never overwrite DATA")
    # Serial measurement precedes test execution to avoid within-run competition.
    run(
        "campaign",
        [
            sys.executable,
            "scripts/empirical_campaign.py",
            "--output",
            str(campaign),
            "--campaign-id",
            CAMPAIGN,
        ],
        2400,
    )
    run(
        "stage3",
        [
            sys.executable,
            "scripts/run_stage3_reference.py",
            "--output",
            str(output / "stage3.json"),
        ],
    )
    run("full_baseline", [sys.executable, "scripts/generate_baseline.py"])
    for name, command in (
        ("black", ["-m", "black", "--check", "src", "tests", "scripts"]),
        ("ruff", ["-m", "ruff", "check", "src", "tests", "scripts"]),
        ("mypy", ["-m", "mypy", "src/"]),
        ("pyright", ["-m", "pyright"]),
        ("catalog", ["scripts/generate_catalog_audit_report.py"]),
        ("docs", ["scripts/check_doc_consistency.py", "--check-tests"]),
    ):
        run(name, [sys.executable, *command])
    changed = [
        str(path.relative_to(ROOT))
        for path, digest in protected.items()
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest
    ]
    if changed:
        raise RuntimeError("Historical scientific artifacts changed: " + repr(changed))
    completion = campaign / "completion.json"
    if (
        not completion.exists()
        or not json.loads(completion.read_text())["source_unchanged"]
    ):
        raise RuntimeError(
            "Campaign did not finish with unchanged source; no publication"
        )
    shutil.copytree(campaign, published)
    report = {
        "schema_version": 1,
        "source_revision": source,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
        "checks": records,
        "historical_scientific_bytes_unchanged": True,
        "all_checks_passed": all(item["exit_code"] == 0 for item in records),
        "authority": "execution_and_engineering_only",
        "accepted_evidence": False,
        "human_review": "pending",
        "campaign": CAMPAIGN,
    }
    report_path = ROOT / "docs" / "05-quality" / "scientific-audit-20260913.json"
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output / "audit.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    shutil.copy2(
        output / "stage3.json",
        ROOT
        / "research/generated/verification/plastic_neural_tissue_reference_alpha3.json",
    )
    if os.environ.get("GITHUB_REF_NAME") == BRANCH:
        subprocess.run(
            ["git", "config", "user.name", "MHRN audit (AI-assisted)"],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(
            [
                "git",
                "config",
                "user.email",
                "41898282+github-actions[bot]@users.noreply.github.com",
            ],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(
            [
                "git",
                "add",
                "research/experiments/" + CAMPAIGN,
                "research/generated",
                "docs/05-quality/scientific-audit-20260913.json",
                "tests/test_baseline.json",
            ],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "research: retain complete alpha3 audit, negative outcomes and source-bound checks",
            ],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(
            ["git", "push", "origin", "HEAD:refs/heads/" + BRANCH], cwd=ROOT, check=True
        )
    subprocess.run(
        ["git", "bundle", "create", str(output / "audit-source.bundle"), "--all"],
        cwd=ROOT,
        check=True,
    )
    return 0 if report["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
