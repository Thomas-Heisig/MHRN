from __future__ import annotations

from src.research.stage6_neural_world_model_experiment import run_s6_nwm_001


def _condition(runs: list[object], name: str) -> object:
    return next(run for run in runs if getattr(run, "condition") == name)


def test_s6_nwm_001_has_neural_and_statistical_controls() -> None:
    runs = run_s6_nwm_001({}, (101,))
    assert len(runs) == 4
    assert {run.condition for run in runs} == {
        "spiking_trained",
        "spiking_untrained",
        "spiking_target_shuffled",
        "statistical_reference",
    }
    for run in runs:
        assert run.metrics["exact_context_encoder"] is True
        assert run.metrics["held_out_context_generalization"] is False
        assert run.metrics["scientific_evidence"] is False


def test_s6_nwm_001_trained_spiking_candidate_beats_neural_controls() -> None:
    runs = run_s6_nwm_001({}, (101,))
    trained = _condition(runs, "spiking_trained")
    untrained = _condition(runs, "spiking_untrained")
    shuffled = _condition(runs, "spiking_target_shuffled")

    assert trained.metrics["snn_involved"] is True  # type: ignore[attr-defined]
    assert trained.metrics["prediction_coverage"] > 0.0  # type: ignore[attr-defined]
    assert trained.metrics["exact_accuracy"] > untrained.metrics["exact_accuracy"]  # type: ignore[attr-defined]
    assert trained.metrics["exact_accuracy"] > shuffled.metrics["exact_accuracy"]  # type: ignore[attr-defined]
    assert trained.metrics["mean_correct_weight_margin"] > 0.0  # type: ignore[attr-defined]


def test_s6_nwm_001_statistical_reference_stays_non_neural() -> None:
    reference = _condition(run_s6_nwm_001({}, (103,)), "statistical_reference")

    assert reference.metrics["snn_involved"] is False  # type: ignore[attr-defined]
    assert reference.metrics["exact_accuracy"] == 1.0  # type: ignore[attr-defined]
    assert reference.metrics["prediction_coverage"] == 1.0  # type: ignore[attr-defined]


def test_s6_nwm_001_is_deterministic_for_fixed_seed() -> None:
    assert run_s6_nwm_001({}, (107,)) == run_s6_nwm_001({}, (107,))
