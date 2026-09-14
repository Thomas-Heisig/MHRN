"""Run the Stage-5 integrated artificial nervous-system reference verification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from src.embodiment.integrated_nervous_system import (
    STAGE5_REFERENCE_EXPERIMENT,
    integrated_nervous_system_contract,
)
from src.experiments.embodiment_lab import run_protocol

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_DIR = ROOT / STAGE5_REFERENCE_EXPERIMENT
VERIFICATION = (
    ROOT
    / "research/generated/verification/integrated_nervous_system_reference_alpha3.json"
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    analysis = run_protocol(
        EXPERIMENT_DIR,
        independent_runs=20,
        repetitions_per_condition=3,
    )
    contract = integrated_nervous_system_contract()
    conditions = analysis["conditions"]

    checks = {
        "360_controlled_runs": analysis["run_count"] == 360,
        "sensor_frames_reproducible": analysis["sensor_frames_reproducible"] is True,
        "authorized_actions_observed": conditions["authorized"]["accepted_action_count"] > 0
        and conditions["authorized"]["observed_effect_count"] > 0,
        "unauthorized_actions_blocked": conditions["unauthorized"]["accepted_action_count"] == 0,
        "actuator_failure_has_no_effect": conditions["actuator_failure"]["observed_effect_count"] == 0,
        "sensor_loss_detected": conditions["sensor_loss"]["runtime_errors"] > 0,
        "open_loop_replay_separate": conditions["open_loop_replay"]["action_sources"]
        == ["pre_registered_replay"],
        "all_stage5_layers_present": all(
            contract["layers"][name]["implemented"]
            for name in (
                "sensorik",
                "interozeption",
                "aktorik",
                "feedback",
                "ressourcenhaushalt",
            )
        ),
        "productive_external_actuation_locked": contract["boundaries"][
            "productive_external_actuation_enabled"
        ]
        is False,
        "no_automatic_evidence_promotion": analysis["evidence_eligible"] is False
        and contract["boundaries"]["automatic_evidence_promotion"] is False,
    }
    status = "verified" if all(checks.values()) else "failed"

    stage5_manifest = {
        "experiment_id": "EXP-STAGE5-20260914-INTEGRATED-NERVOUS-SYSTEM",
        "protocol_family": "EXP-EMB-0001",
        "scope": "engineering_verification",
        "research_question": "RQ-EMB-001",
        "hypotheses": {
            "H-EMB-001-A": "DATA-supported by deterministic closed-loop controls; not EVID",
            "H-EMB-001-B": "not tested by this protocol; requires matched external disturbance, yoked replay and interrupted-feedback tracking metrics",
        },
        "run_count": analysis["run_count"],
        "conditions": list(conditions),
        "source_freeze_sha": analysis["source_freeze_sha"],
        "data_sha256": _sha(EXPERIMENT_DIR / "DATA/runs.jsonl"),
        "analysis_sha256": _sha(EXPERIMENT_DIR / "DATA/analysis.json"),
        "automatic_evidence_promotion": False,
        "evidence_eligible": False,
        "limits": [
            "synthetic deterministic target environment only",
            "no real-device verification",
            "no long-horizon autonomous operation claim",
            "host/resource telemetry is digital interoception, not biological interoception",
            "resource accounting is not biological metabolism",
            "H-EMB-001-B remains untested by this protocol",
        ],
    }
    (EXPERIMENT_DIR / "stage5_manifest.json").write_text(
        json.dumps(stage5_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    payload = {
        "stage": 5,
        "status": status,
        "scope": "engineering_verification",
        "checks": checks,
        "experiment": stage5_manifest,
        "contract": contract,
        "scientific_status": {
            "RQ-EMB-001": "open",
            "H-EMB-001-A": "DATA-supported, not accepted EVID",
            "H-EMB-001-B": "untested by Stage-5 reference protocol",
        },
    }
    VERIFICATION.parent.mkdir(parents=True, exist_ok=True)
    VERIFICATION.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if status == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
