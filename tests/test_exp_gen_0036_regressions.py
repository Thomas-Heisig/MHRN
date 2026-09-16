from __future__ import annotations

from src.research.experiment_summary import _suite_integrity, build_descriptive_statistics
from src.research_assistant.models import normalize_output


def test_suite_integrity_does_not_treat_non_snn_metrics_as_missing_data() -> None:
    runs = [
        {
            "condition": "ping:recurrence_off",
            "seed": 42,
            "metrics": {"ticks_executed": 1000, "total_spikes": 3},
            "runtime_error": None,
        },
        {
            "condition": "temporal:fast_medium_slow",
            "seed": 42,
            "metrics": {
                "ticks_executed": 1000,
                "total_spikes": 0,
                "comparisons": [
                    {"horizon": "fast", "reference_tick": 1, "discrepancy": 0.5}
                ],
            },
            "runtime_error": None,
        },
        {
            "condition": "stdp:productive_reward_stdp",
            "seed": 42,
            "metrics": {"mean_weight_delta": 0.2, "final_mean_weight": 0.3},
            "runtime_error": None,
        },
        {
            "condition": "learning:learning_on",
            "seed": 42,
            "metrics": {
                "mean_weight_delta": 0.467,
                "final_mean_weight": 0.517,
                "train_trial_count": 100,
            },
            "runtime_error": None,
        },
        {
            "condition": "time:1000",
            "seed": 42,
            "metrics": {"ticks": 1000, "duration_seconds": 0.1},
            "runtime_error": None,
        },
        {
            "condition": "5d:5d",
            "seed": 42,
            "metrics": {"ticks_executed": 1000, "total_spikes": 3},
            "runtime_error": None,
        },
        {
            "condition": "regulation:nominal",
            "seed": 42,
            "metrics": {"resource_pressure": 0.2},
            "runtime_error": None,
        },
    ]

    statistics = build_descriptive_statistics(runs)
    integrity = _suite_integrity(runs, statistics)

    assert integrity["status"] == "COMPLETE_FOR_REGISTERED_GROUPS"
    assert integrity["missing_groups"] == []
    assert integrity["missing_statistics"] == []
    assert integrity["empty_statistics"] == []
    assert (
        statistics["conditions"]["learning:learning_on"]["metrics"]
        ["final_mean_weight"]["mean"]
        == 0.517
    )


def test_temporal_discrepancy_is_valid_even_when_spike_count_is_zero() -> None:
    statistics = build_descriptive_statistics(
        [
            {
                "condition": "temporal:fast_medium_slow",
                "seed": 42,
                "metrics": {
                    "ticks_executed": 1000,
                    "total_spikes": 0,
                    "comparisons": [
                        {
                            "horizon": "fast",
                            "reference_tick": 25,
                            "discrepancy": 0.75,
                        }
                    ],
                },
                "runtime_error": None,
            }
        ]
    )

    assert (
        statistics["conditions"]["temporal:fast_medium_slow"]["metrics"]
        ["total_spikes"]["mean"]
        == 0.0
    )
    assert statistics["temporal_horizons"]["fast"]["discrepancy"]["mean"] == 0.75


def test_nested_airr_output_is_adapted_instead_of_marked_unavailable() -> None:
    normalized = normalize_output(
        {
            "analysis": {
                "overview": "Technische Diagnose vorhanden.",
                "key_findings": [
                    {"category": "Vollstaendigkeit", "finding": "DATA vorhanden."}
                ],
                "conclusion": "Die Diagnose ist inhaltlich verwertbar.",
            },
            "recommendations": {
                "next_steps": [
                    {"step": "Human Review", "description": "Manuell pruefen."}
                ]
            },
            "limitations": ["Keine Primaerevidenz fuer Fach-RQs."],
        }
    )

    assert normalized["assessment"] == "Die Diagnose ist inhaltlich verwertbar."
    assert normalized["schema_adapted"] is True
    assert normalized.get("analysis_unavailable") is not True
    assert normalized["observations"]
    assert normalized["methodological_concerns"]
    assert normalized["recommended_experiments"]
    assert normalized["confidence"] == 0.0
