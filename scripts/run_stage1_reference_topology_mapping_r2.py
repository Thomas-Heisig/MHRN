#!/usr/bin/env python3
"""Executable R2 topology mapping parity gate; calibration only, never EVID."""

from __future__ import annotations
import hashlib, json, random
from pathlib import Path
from typing import Any
from reference.stage1_topology_brian2 import runner_r2 as reference
from scripts.run_stage1_topology_v2 import (
    canonical_coords,
    edge_list,
    read_json,
    shape_for,
)

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-PROMO-R1.json"
PROTOCOL = ROOT / "reference" / "stage1_topology_brian2" / "reference_protocol_r2.json"
OUT = (
    ROOT
    / "research"
    / "calibrations"
    / "CAL-S1-TOPO-REFERENCE-TOPOLOGY-MAP-R2"
    / "result.json"
)
PROBE_SEEDS = (820099901, 820099902, 820099903)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def main() -> int:
    canon = read_json(CANON)
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    out_degree = int(protocol["network"]["out_degree_cap"])
    cases = []
    for condition in protocol["conditions"]:
        shape = shape_for(canon, condition)
        for seed in PROBE_SEEDS:
            mc = canonical_coords(shape)
            if condition == "5d_shuffled":
                random.Random(seed ^ 0x5D5D5D).shuffle(mc)
            me = edge_list(canon, condition, seed, mc)
            rc, re = reference._graph(condition, shape, seed, out_degree)
            ok = mc == rc and me == re and len(me) == 246
            cases.append(
                {
                    "condition": condition,
                    "probe_seed": seed,
                    "coordinate_digest_mhrn": digest(mc),
                    "coordinate_digest_reference": digest(rc),
                    "edge_digest_mhrn": digest(me),
                    "edge_digest_reference": digest(re),
                    "coordinate_lists_exactly_equal": mc == rc,
                    "edge_lists_exactly_equal": me == re,
                    "edge_count": len(me),
                    "pass": ok,
                }
            )
    payload = {
        "schema_version": 1,
        "calibration_id": "CAL-S1-TOPO-REFERENCE-TOPOLOGY-MAP-R2",
        "role": "pre-freeze topology translation calibration; not confirmatory DATA and not EVID",
        "probe_seeds": list(PROBE_SEEDS),
        "evaluation_seed_overlap": False,
        "cases": cases,
        "source_sha256": {
            "scripts/run_stage1_topology_v2.py": sha(
                ROOT / "scripts" / "run_stage1_topology_v2.py"
            ),
            "reference/stage1_topology_brian2/runner_r2.py": sha(
                ROOT / "reference" / "stage1_topology_brian2" / "runner_r2.py"
            ),
            "reference/stage1_topology_brian2/reference_protocol_r2.json": sha(
                PROTOCOL
            ),
        },
        "pass": all(c["pass"] for c in cases),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "calibration_id": payload["calibration_id"],
                "pass": payload["pass"],
                "cases": len(cases),
            }
        )
    )
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
