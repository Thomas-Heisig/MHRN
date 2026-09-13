"""Build edition 1.5 from retained DATA on the isolated, authorized audit branch."""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "work/scientific-main-audit-20260913"
OUT = Path("/tmp/alpha3-publication")
EDITION = "2026-09-13_recursive-epistemics_v1.5"


def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=ROOT, check=True, **kwargs)


def commit(message: str, paths: list[str]) -> None:
    run(["git", "add", "--", *paths])
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode:
        run(["git", "commit", "-m", message])
        run(["git", "push", "origin", "HEAD:refs/heads/" + BRANCH])


def sources() -> None:
    approved = {"scripts/publication_alpha3.py", "scripts/publication_alpha3_text.py"}
    changed = []
    for path in sorted((ROOT / ".maintenance").glob("alpha3-source-part-*.json")):
        wrapper = json.loads(path.read_text(encoding="utf-8"))
        encoded = wrapper["gzip_base64"]
        packed = base64.b64decode(encoded, validate=True)
        # Correct one identified textual transport duplication only if the
        # original complete expected digest then matches; never relax a digest.
        if hashlib.sha256(packed).hexdigest() != wrapper["payload_sha256"]:
            encoded = encoded.replace("WyXpkjjrs", "WyXpkjrs")
            packed = base64.b64decode(encoded, validate=True)
        if hashlib.sha256(packed).hexdigest() != wrapper["payload_sha256"]:
            raise ValueError("Transport checksum mismatch: " + path.name)
        entries = json.loads(gzip.decompress(packed))
        if {entry["path"] for entry in entries} != set(wrapper["paths"]):
            raise ValueError("Transport inventory mismatch")
        for entry in entries:
            if entry["path"] not in approved:
                raise ValueError("Unexpected source target")
            target = ROOT / entry["path"]
            current = hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None
            if current == entry["after"]:
                continue
            if current != entry["before"]:
                raise ValueError("Concurrent source change: " + entry["path"])
            data = entry["content"].encode("utf-8")
            if hashlib.sha256(data).hexdigest() != entry["after"]:
                raise ValueError("Source checksum mismatch")
            target.write_bytes(data)
            changed.append(entry["path"])
        path.unlink()
        changed.append(str(path.relative_to(ROOT)))
    if changed:
        commit("docs: install checksum-verified complete publication renderer and chapters", changed)
    run([sys.executable, ".maintenance/apply_scientific_audit.py"])


def main() -> int:
    if os.environ.get("GITHUB_REF_NAME") != BRANCH:
        raise RuntimeError("Write access is restricted to the audit branch")
    os.chdir(ROOT)
    OUT.mkdir(parents=True, exist_ok=True)
    run(["git", "config", "user.name", "MHRN scientific audit (AI-assisted)"])
    run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"])
    if len(sys.argv) > 1 and sys.argv[1] == "sources":
        sources()
        return 0
    folder = ROOT / "research/publications" / EDITION
    if not folder.exists():
        run([sys.executable, "scripts/publication_alpha3.py", "--campaign", "research/experiments/EXP-EMP-20260913-A3", "--docx", "--pdf", "--integrate"])
    run([sys.executable, "scripts/publication_alpha3.py", "--verify"])
    commit("docs: publish complete 69-chapter edition 1.5 and current scientific report", ["research/publications", "research/generated", "docs", "README.md", "project_identity.json", "research/README.md"])
    records = []
    for name, command in (
        ("black", [sys.executable, "-m", "black", "--check", "src", "tests", "scripts"]),
        ("ruff", [sys.executable, "-m", "ruff", "check", "src", "tests", "scripts"]),
        ("precommit", [sys.executable, "-m", "pre_commit", "run", "--all-files", "--show-diff-on-failure"]),
        ("full_baseline_large", [sys.executable, "scripts/generate_baseline.py"]),
        ("docs", [sys.executable, "scripts/check_doc_consistency.py", "--check-tests"]),
        ("browser_smoke", [sys.executable, "scripts/browser_check.py"]),
        ("browser_e2e", ["npx", "playwright", "test", "--reporter=line"]),
    ):
        log = OUT / (name + ".log")
        with log.open("w", encoding="utf-8") as stream:
            try:
                result = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, timeout=1200, check=False)
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 124
        records.append({"name": name, "command": command, "exit_code": code, "log": log.name})
        print(name, code, flush=True)
    report = {
        "schema_version": 1,
        "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "checks": records,
        "all_checks_passed": all(item["exit_code"] == 0 for item in records),
        "human_scientific_review": "pending",
        "automatic_evidence_promotion": False,
    }
    target = ROOT / "docs/05-quality/publication-alpha3-verification.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(target, OUT / "verification.json")
    commit("test: record actual publication, large-storage and browser verification", ["docs/05-quality/publication-alpha3-verification.json", "tests/test_baseline.json", "research/generated/verification"])
    for suffix in ("*.docx", "*.pdf"):
        for path in folder.glob(suffix):
            shutil.copy2(path, OUT / path.name)
    shutil.copy2(folder / "manifest.json", OUT / "publication-manifest.json")
    run(["git", "bundle", "create", str(OUT / "publication-source.bundle"), "--all"])
    return 0 if report["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
