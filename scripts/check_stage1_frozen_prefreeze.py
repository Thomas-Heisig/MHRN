"""Revalidate frozen R2 methods without replacing hash-bound audit artifacts."""

from __future__ import annotations

import hashlib
import importlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> None:
    freeze = json.loads(
        (
            ROOT / "research/preregistrations/PREREG-S1-TOPO-REFERENCE-R2.freeze.json"
        ).read_text(encoding="utf-8")
    )
    for key in (
        "mechanism_audit",
        "dynamics_reuse_validation",
        "topology_mapping_parity",
        "integrator_parity",
        "reset_parity",
        "synapse_delay_parity",
    ):
        entry = freeze[key]
        path = ROOT / entry["path"].replace("\\", "/")
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError(f"Frozen artifact changed: {key}")
    with tempfile.TemporaryDirectory(prefix="mhrn-r2-revalidation-") as directory:
        for name in (
            "audit_stage1_reference_mechanisms",
            "verify_stage1_reference_dynamics_reuse_r2",
            "run_stage1_reference_topology_mapping_r2",
        ):
            module = importlib.import_module(f"scripts.{name}")
            module.OUT = Path(directory) / f"{name}.json"
            if module.main() != 0:
                raise ValueError(f"Current method revalidation failed: {name}")
    print("PASS: frozen artifacts intact and current R2 method gates passed")


if __name__ == "__main__":
    main()
