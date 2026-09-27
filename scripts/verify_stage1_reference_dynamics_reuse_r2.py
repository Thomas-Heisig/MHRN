#!/usr/bin/env python3
"""Validate immutable reuse of R1 dynamics parity artifacts for R2.

This writes an R2 method-validation artifact without modifying the historical
R1 integrator/reset/synapse calibration files.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INTEGRATOR = (
    ROOT / "research/calibrations/CAL-S1-TOPO-REFERENCE-INTEGRATOR-R1/result.json"
)
RESET = ROOT / "research/calibrations/CAL-S1-TOPO-REFERENCE-RESET-R1/result.json"
SYNAPSE = ROOT / "research/calibrations/CAL-S1-TOPO-REFERENCE-SYNAPSE-R1/result.json"
OUT = ROOT / "research/calibrations/CAL-S1-TOPO-REFERENCE-DYNAMICS-REUSE-R2/result.json"


def read(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_source(actual_path: str, expected: str) -> dict[str, Any]:
    path = ROOT / actual_path
    current = sha(path)
    return {
        "path": actual_path,
        "expected_sha256": expected,
        "current_sha256": current,
        "match": current == expected,
    }


def main() -> int:
    integ, reset, syn = map(read, (INTEGRATOR, RESET, SYNAPSE))
    checks = [
        check_source(
            "reference/stage1_topology_brian2/integrator_probe.py",
            str(integ["provenance"]["reference_probe_sha256"]),
        ),
        check_source(
            "src/core/neuron.py", str(integ["provenance"]["mhrn_neuron_source_sha256"])
        ),
        check_source(
            "src/core/neuron_models.py",
            str(integ["provenance"]["mhrn_neuron_model_source_sha256"]),
        ),
        check_source(
            "reference/stage1_topology_brian2/integrator_probe.py",
            str(reset["provenance"]["reference_probe_sha256"]),
        ),
        check_source(
            "src/core/neuron.py", str(reset["provenance"]["mhrn_neuron_source_sha256"])
        ),
        check_source(
            "src/core/neuron_models.py",
            str(reset["provenance"]["mhrn_neuron_model_source_sha256"]),
        ),
        check_source(
            "reference/stage1_topology_brian2/synapse_probe.py",
            str(syn["provenance"]["reference_probe_sha256"]),
        ),
        check_source(
            "src/core/network.py", str(syn["provenance"]["mhrn_network_source_sha256"])
        ),
        check_source(
            "src/core/neuron.py", str(syn["provenance"]["mhrn_neuron_source_sha256"])
        ),
    ]
    pass_value = bool(
        integ.get("pass") is True
        and integ.get("multi_tick", {}).get("pass") is True
        and integ.get("multi_tick", {}).get("contains_spike") is True
        and reset.get("pass") is True
        and syn.get("pass") is True
        and integ.get("provenance", {}).get("brian2_version") == "2.10.1"
        and reset.get("provenance", {}).get("brian2_version") == "2.10.1"
        and syn.get("provenance", {}).get("brian2_version") == "2.10.1"
        and all(item["match"] for item in checks)
    )
    payload = {
        "schema_version": 1,
        "calibration_id": "CAL-S1-TOPO-REFERENCE-DYNAMICS-REUSE-R2",
        "role": "R2 pre-freeze source-hash revalidation of immutable R1 dynamics parity artifacts; not DATA and not EVID",
        "historical_artifacts": {
            "integrator": {
                "path": str(INTEGRATOR.relative_to(ROOT)),
                "sha256": sha(INTEGRATOR),
                "pass": integ.get("pass"),
            },
            "reset": {
                "path": str(RESET.relative_to(ROOT)),
                "sha256": sha(RESET),
                "pass": reset.get("pass"),
            },
            "synapse_delay": {
                "path": str(SYNAPSE.relative_to(ROOT)),
                "sha256": sha(SYNAPSE),
                "pass": syn.get("pass"),
            },
        },
        "source_hash_checks": checks,
        "python_version": platform.python_version(),
        "brian2_version": "2.10.1",
        "historical_artifacts_modified": False,
        "pass": pass_value,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "calibration_id": payload["calibration_id"],
                "pass": pass_value,
                "checks": len(checks),
            }
        )
    )
    return 0 if pass_value else 1


if __name__ == "__main__":
    raise SystemExit(main())
