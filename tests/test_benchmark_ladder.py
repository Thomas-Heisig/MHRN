from __future__ import annotations

from scripts.benchmark_ladder import run_tier
from scripts.benchmark_plastic_network import run_benchmark


def test_scaling_tier_reports_neuron_and_synapse_profile() -> None:
    report = run_tier(
        neuron_count=100,
        ticks=2,
        seed=42,
        connections_per_neuron=2,
    )

    assert report["neurons"] == 100
    assert report["synapses"] > 0
    assert report["connections_per_neuron_requested"] == 2
    assert report["ticks_per_second"] > 0
    assert report["neurons_per_second"] > 0
    assert report["synapses_per_second"] > 0


def test_plastic_scale_benchmark_runs_bounded_learning_and_reports_stability() -> None:
    report = run_benchmark(
        neuron_count=40,
        synapse_count=80,
        epochs=2,
        seed=7,
        memory_budget_bytes=2 * 1024**2,
        stability_interval=1,
    )

    assert report["neurons"] == 40
    assert report["synapses"] == 80
    assert report["learning_stats"]["reward_weight_updates"] > 0
    assert report["synapse_candidate_visits_per_second"] > 0
    assert report["final_weights_finite"] is True
    assert report["final_out_of_bounds_weights"] == 0
    assert report["stability_invariants_passed"] is True
    assert 0 <= report["final_at_lower_bound_fraction"] <= 1
    assert report["workload"]["reward_per_epoch"] == 1.0
    assert "cpu" in report
    assert report["stage3_target_range"]["lower_bound_covered"] is False


def test_plastic_scale_benchmark_refuses_excessive_memory_estimate() -> None:
    import pytest

    with pytest.raises(ValueError, match="exceeds memory budget"):
        run_benchmark(
            neuron_count=40,
            synapse_count=80,
            epochs=1,
            memory_budget_bytes=1,
        )


def test_plastic_scale_off_control_keeps_weights_and_reports_activity() -> None:
    report = run_benchmark(
        neuron_count=40,
        synapse_count=80,
        epochs=8,
        seed=7,
        memory_budget_bytes=2 * 1024**2,
        stability_interval=2,
        plasticity_mode="off",
    )

    assert report["learning_stats"]["updates"] == 0
    assert report["learning_stats"]["reward_weight_updates"] == 0
    assert report["final_weights_finite"] is True
    assert report["functional_activity_passed"] is True
    assert report["weight_diversity_required"] is False
    assert report["stability_invariants_passed"] is True


def test_symmetric_stdp_heterogeneous_profile_distinguishes_synapses() -> None:
    report = run_benchmark(
        neuron_count=40,
        synapse_count=80,
        epochs=8,
        seed=7,
        memory_budget_bytes=2 * 1024**2,
        stability_interval=2,
        plasticity_mode="symmetric",
    )

    assert report["workload"]["stdp"]["a_minus"] == report["workload"]["stdp"]["a_plus"]
    assert report["final_weights_finite"] is True
    assert report["final_at_lower_bound_fraction"] < 1.0
    assert report["stability_snapshots"][-1]["weight_variance"] > 1e-12
    assert report["weight_diversity_passed"] is True
