"""Apply the reviewed CI repair after verifying all source and result digests."""
from __future__ import annotations

import gzip
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".maintenance/frontend-ci-repair.json.gz"
OVERRIDES = ROOT / ".maintenance/frontend-ci-repair-overrides.json"
ALLOWED = ("src/dashboard/", "src/storage/optical_codec.py", "tests/browser/", ".github/workflows/ci.yml")


def main() -> None:
    if os.environ.get("GITHUB_REF_NAME") != "main":
        raise RuntimeError("This source-bound integration repair is restricted to main")
    plan = json.loads(gzip.decompress(MANIFEST.read_bytes()))
    if OVERRIDES.exists():
        plan.update(json.loads(OVERRIDES.read_text(encoding="utf-8")))
    prepared = []
    for name, spec in plan.items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or not any(name.startswith(prefix) for prefix in ALLOWED):
            raise ValueError(f"Unexpected repair target: {name}")
        path = ROOT / relative
        if path.is_symlink():
            raise ValueError(f"Symlink repair target: {name}")
        before = path.read_bytes() if path.exists() else None
        digest = hashlib.sha256(before).hexdigest() if before is not None else None
        if digest != spec["before"]:
            raise ValueError(f"Concurrent or stale source at {name}: {digest}")
        lines = (before or b"").decode("utf-8").splitlines(keepends=True)
        previous = len(lines) + 1
        for start, stop, replacement in reversed(spec["edits"]):
            if not 0 <= start <= stop <= len(lines) or stop > previous:
                raise ValueError(f"Invalid or overlapping edit in {name}")
            lines[start:stop] = replacement.splitlines(keepends=True)
            previous = start
        after = "".join(lines).encode("utf-8")
        if hashlib.sha256(after).hexdigest() != spec["after"]:
            raise ValueError(f"Repair result digest mismatch: {name}")
        prepared.append((path, after))
    for path, data in prepared:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    receipt = Path("/tmp/frontend-ci-repair/paths.json")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(list(plan)) + "\n", encoding="utf-8")
    print(f"Applied {len(prepared)} digest-verified CI repairs; no scientific DATA changed.")


if __name__ == "__main__":
    main()
