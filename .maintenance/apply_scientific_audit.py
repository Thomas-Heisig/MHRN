"""Apply reviewed source corrections on the isolated audit branch only.

Every stored line edit is protected by complete before/after SHA-256 digests.
No experimental DATA, historical publication or evidence record is rewritten.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "work/scientific-main-audit-20260913"


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def main() -> None:
    if os.environ.get("GITHUB_REF_NAME") != BRANCH:
        raise RuntimeError("The maintenance writer is restricted to the audit branch")
    os.chdir(ROOT)
    changed: list[str] = []
    for payload in sorted((ROOT / ".maintenance").glob("scientific-repair-*.json")):
        edits = json.loads(payload.read_text(encoding="utf-8"))
        for name, spec in edits.items():
            target = (ROOT / name).resolve()
            target.relative_to(ROOT)
            if name.startswith(("research/experiments/", "research/publications/", "research/registry/evidence/", "research/preregistrations/")):
                raise ValueError("Immutable scientific path in maintenance payload")
            before = target.read_bytes() if target.exists() else b""
            if target.exists() and digest(before) == spec["after"]:
                continue
            if (digest(before) if target.exists() else None) != spec["before"]:
                raise ValueError("Source changed concurrently: " + name)
            lines = before.decode("utf-8").splitlines(keepends=True)
            for start, stop, replacement in reversed(spec["edits"]):
                lines[start:stop] = [replacement]
            after = "".join(lines).encode("utf-8")
            if digest(after) != spec["after"]:
                raise ValueError("Patch checksum mismatch: " + name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(after)
            changed.append(name)
        payload.unlink()
        changed.append(str(payload.relative_to(ROOT)))
    if changed:
        subprocess.run(["git", "config", "user.name", "MHRN audit (AI-assisted)"], check=True)
        subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "add", "--", *changed], check=True)
        subprocess.run(["git", "commit", "-m", "fix: apply source-bound scientific audit and alpha3 version"], check=True)
        subprocess.run(["git", "push", "origin", "HEAD:refs/heads/" + BRANCH], check=True)


if __name__ == "__main__":
    main()
