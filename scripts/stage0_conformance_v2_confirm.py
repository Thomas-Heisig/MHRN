"""Confirmatory runner for PREREG-EVAL-006-V2.

No adaptive retry or parameter tuning is allowed here. The validation seeds and
criteria are frozen in research/preregistrations/operational/
single_neuron_conformance_v2.json before execution.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

PREREG = Path("research/preregistrations/operational/single_neuron_conformance_v2.json")
OUT = Path("stage0-conformance-v2-confirmatory.json")
CANDIDATE = Path("scripts/stage0_conformance_v2.py")


def _load_candidate() -> Any:
    spec = importlib.util.spec_from_file_location(
        "stage0_conformance_candidate", CANDIDATE
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load stage0_conformance_v2.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    if prereg["status"] != "FROZEN_BEFORE_CONFIRMATORY_EXECUTION":
        raise RuntimeError("confirmatory protocol is not frozen")
    module = _load_candidate()
    validation = prereg["confirmatory_validation"]
    seeds = tuple(int(seed) for seed in validation["seeds"])

    izh_rows = [module._izh_local(seed) for seed in seeds]
    izh_pass = all(row["conformance_within_1e_8"] for row in izh_rows)

    lif_default_rows: list[dict[str, Any]] = []
    lif_refractory_rows: list[dict[str, Any]] = []
    expected_mapping = {1: 2, 2: 3, 3: 4}
    for seed in seeds:
        sweep = module._lif_mapping(seed)
        for row in sweep:
            native_ticks = int(row["native_refractory_ticks"])
            brian_ms = int(row["brian2_refractory_ms"])
            if native_ticks == 0 and brian_ms == 0:
                lif_default_rows.append(row)
            if (
                native_ticks in expected_mapping
                and brian_ms == expected_mapping[native_ticks]
            ):
                lif_refractory_rows.append(row)

    lif_default_pass = len(lif_default_rows) == len(seeds) and all(
        row["spike_events_equal"] and row["max_abs_v_error"] <= 1e-8
        for row in lif_default_rows
    )
    expected_secondary_count = len(seeds) * len(expected_mapping)
    lif_refractory_pass = len(lif_refractory_rows) == expected_secondary_count and all(
        row["spike_events_equal"] and row["max_abs_v_error"] <= 1e-8
        for row in lif_refractory_rows
    )

    payload = {
        "preregistration_id": prereg["preregistration_id"],
        "protocol": prereg["protocol"],
        "mode": "CONFIRMATORY",
        "seeds": list(seeds),
        "diagnostic_seed_overlap": bool(set(seeds) & {20001, 20002, 20003}),
        "H-EVAL-006-A": {
            "supported_by_protocol": izh_pass,
            "runs": izh_rows,
        },
        "H-EVAL-006-B": {
            "supported_by_protocol": lif_default_pass,
            "runs": lif_default_rows,
        },
        "H-EVAL-006-C": {
            "supported_by_protocol": lif_refractory_pass,
            "mapping": {str(k): v for k, v in expected_mapping.items()},
            "runs": lif_refractory_rows,
        },
        "primary_success": izh_pass and lif_default_pass,
        "all_declared_hypotheses_pass": izh_pass
        and lif_default_pass
        and lif_refractory_pass,
        "automatic_evid_promotion": False,
        "human_review_required": True,
        "independent_authorship_replication": False,
    }
    OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(OUT.read_text(encoding="utf-8"))
    if not payload["all_declared_hypotheses_pass"]:
        raise SystemExit("CONFIRMATORY_STAGE0_CONFORMANCE_FAILED")


if __name__ == "__main__":
    main()
