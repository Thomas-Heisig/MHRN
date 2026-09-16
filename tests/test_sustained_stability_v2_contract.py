from __future__ import annotations

from pathlib import Path

import yaml

from src.research.protocol_registry import (
    OPERATIONAL_RUNNERS,
    validate_operational_protocol,
)
from src.research.stability_followups import run_sustained_stability_v2


def _config() -> dict[str, object]:
    raw = yaml.safe_load(
        Path("configs/learning_experiment.yaml").read_text(encoding="utf-8")
    )
    assert isinstance(raw, dict)
    return raw


def test_v2_seed_labels_materially_change_parameterizations() -> None:
    runs = run_sustained_stability_v2(_config(), seeds=(101, 102, 103), ticks=2_000)
    assert len(runs) == 6
    by_seed: dict[int, list[object]] = {}
    for item in runs:
        assert item.metrics["ticks_executed"] == 2_000
        assert item.metrics["finite_state"] is True
        assert item.metrics["topology_unchanged"] is True
        by_seed.setdefault(item.seed, []).append(item)
    digests = set()
    params = set()
    for seed_runs in by_seed.values():
        assert {item.condition for item in seed_runs} == {
            "no_input_control",
            "tonic_drive",
        }
        pair_digests = {str(item.metrics["realization_digest"]) for item in seed_runs}
        assert len(pair_digests) == 1
        digests.update(pair_digests)
        params.add(
            (
                float(seed_runs[0].metrics["realization_weight_scale"]),
                float(seed_runs[0].metrics["realization_drive_scale"]),
            )
        )
    assert len(digests) == 3
    assert len(params) == 3


def test_v2_protocol_is_frozen_and_registered() -> None:
    assert (
        OPERATIONAL_RUNNERS["sustained_activity_stability_v2"]
        == "run_sustained_stability_v2"
    )
    prereg = validate_operational_protocol(
        Path("research"),
        question_id="RQ-SNN-006",
        hypothesis_id="H-SNN-006-A",
        protocol_id="sustained_activity_stability_v2",
        seed_count=10,
    )
    assert prereg["freeze"]["status"] == "FROZEN"
    assert prereg["seed_strategy"]["seeds"] == list(range(101, 111))
