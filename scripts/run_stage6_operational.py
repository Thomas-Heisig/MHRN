"""Execute the frozen Stage-6 functional experiment bundle as DATA only."""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

from src.research.stage6_experiments import RUNNERS

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "research/protocols/STAGE6_OPERATIONAL_PROTOCOLS.json"
PREREG_PATH = ROOT / "research/preregistrations/operational/stage6_bundle_v1.json"


def _load(path: Path) -> dict[str, Any]:
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"JSON object required: {path}")
    return cast(dict[str, Any], raw)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _commit() -> str:
    return (
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT)
        .decode("utf-8")
        .strip()
    )


def run_bundle(*, seeds: tuple[int, ...]) -> dict[str, Any]:
    protocols = _load(PROTOCOL_PATH)
    prereg = _load(PREREG_PATH)
    seed_strategy = cast(dict[str, Any], prereg["seed_strategy"])
    minimum = int(seed_strategy["minimum_independent_seeds"])
    if len(seeds) < minimum or len(set(seeds)) != len(seeds):
        raise ValueError(f"Stage-6 bundle requires at least {minimum} unique seeds")

    rows: dict[str, list[dict[str, Any]]] = {}
    for raw_protocol in cast(list[object], protocols["protocols"]):
        if not isinstance(raw_protocol, dict):
            raise ValueError("protocol entry must be an object")
        protocol = cast(dict[str, Any], raw_protocol)
        protocol_id = str(protocol["id"])
        runner = RUNNERS.get(protocol_id)
        if runner is None:
            raise ValueError(f"missing Stage-6 runner: {protocol_id}")
        output = [dataclasses.asdict(row) for row in runner({}, seeds)]
        declared = set(cast(list[str], protocol["conditions"]))
        actual = {str(row["condition"]) for row in output}
        if actual != declared:
            raise ValueError(
                f"condition mismatch for {protocol_id}: declared={sorted(declared)} actual={sorted(actual)}"
            )
        if any(
            row["metrics"].get("scientific_evidence") is not False for row in output
        ):
            raise ValueError(f"DATA-only boundary violated: {protocol_id}")
        rows[protocol_id] = output

    return {
        "schema_version": 1,
        "program": protocols["program"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "authority": "DATA_ONLY_HUMAN_REVIEW_REQUIRED",
        "scientific_evidence": False,
        "automatic_evidence_promotion": False,
        "source": {
            "commit": _commit(),
            "protocol_sha256": _sha256(PROTOCOL_PATH),
            "preregistration_sha256": _sha256(PREREG_PATH),
        },
        "seeds": list(seeds),
        "protocols": rows,
    }


def _parse_seeds(value: str) -> tuple[int, ...]:
    values = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    if not values:
        raise argparse.ArgumentTypeError("at least one seed is required")
    return values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=_parse_seeds, default=(101, 102, 103))
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "research/experiments/STAGE6-LATEST-DATA.json",
    )
    args = parser.parse_args()
    payload = run_bundle(seeds=args.seeds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
