#!/usr/bin/env python3
"""Execute EXP-S6-SEM-CL-003 only after explicit frozen authorization."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from src.research.continual_semantization import load_mnist
from src.research.continual_semantization_dose import (
    EXPERIMENT_ID,
    CL003Config,
    run_experiment,
    write_result_bundle,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUTHORIZATION = (
    ROOT / "research" / "preregistrations" / "authorizations" / "EXP-S6-SEM-CL-003.json"
)
DEFAULT_FREEZE = (
    ROOT / "research" / "preregistrations" / "frozen" / "EXP-S6-SEM-CL-003-FREEZE.json"
)
DEFAULT_OUTPUT = ROOT / "research" / "experiments" / EXPERIMENT_ID / "results"
DEFAULT_CACHE = ROOT / ".cache" / "mnist"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def _require_authorization(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RuntimeError(
            "CL-003 execution authorization is absent; empirical run is blocked"
        )
    authorization = _read_json(path)
    if authorization.get("experiment_id") != EXPERIMENT_ID:
        raise RuntimeError("authorization experiment id mismatch")
    if authorization.get("execution_authorized") is not True:
        raise RuntimeError("CL-003 execution authorization is false")
    return authorization


def _verify_freeze(path: Path) -> dict[str, str]:
    if not path.exists():
        raise RuntimeError("CL-003 freeze manifest is absent")
    manifest = _read_json(path)
    if manifest.get("experiment_id") != EXPERIMENT_ID:
        raise RuntimeError("freeze manifest experiment id mismatch")
    expected = manifest.get("sha256")
    if not isinstance(expected, dict) or not expected:
        raise RuntimeError("freeze manifest has no source hashes")
    observed: dict[str, str] = {}
    for relative, expected_digest in sorted(expected.items()):
        if not isinstance(relative, str) or not isinstance(expected_digest, str):
            raise RuntimeError("invalid freeze hash entry")
        target = ROOT / relative
        if not target.is_file():
            raise RuntimeError(f"freeze-bound file is missing: {relative}")
        digest = _sha256(target)
        observed[relative] = digest
        if digest != expected_digest:
            raise RuntimeError(
                f"freeze hash mismatch for {relative}: {digest} != {expected_digest}"
            )
    return observed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--authorization", type=Path, default=DEFAULT_AUTHORIZATION)
    parser.add_argument("--freeze", type=Path, default=DEFAULT_FREEZE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    authorization = _require_authorization(args.authorization)
    source_hashes = _verify_freeze(args.freeze)
    preregistration = {
        "experiment_id": EXPERIMENT_ID,
        "execution_authorized": True,
        "authorization": authorization,
    }
    data = load_mnist(args.cache)
    result = run_experiment(
        data,
        CL003Config(),
        preregistration=preregistration,
        source_hashes=source_hashes,
    )
    write_result_bundle(result, args.output)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
