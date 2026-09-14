from __future__ import annotations

import json
from pathlib import Path

from src.embodiment.msba import Modality
from src.embodiment.specialized_areas import (
    LATEST_MSBA_DATA,
    STAGE4_MIN_NEURONS,
    STAGE4_MIN_SYNAPSES,
    SpecializedAreaNetwork,
    default_specialized_areas,
    reference_probe_suite,
    specialized_area_contract,
)

ROOT = Path(__file__).resolve().parents[1]


def test_stage4_has_three_distinct_modality_paths_and_rules() -> None:
    areas = default_specialized_areas()
    assert {area.modality for area in areas} == {
        Modality.AUDIO,
        Modality.VISION,
        Modality.DIGITAL,
    }
    assert len({area.pathway for area in areas}) == 3
    assert len({area.plasticity_rule for area in areas}) == 3
    assert (
        next(
            area for area in areas if area.modality is Modality.DIGITAL
        ).exact_payload_outside_snn
        is True
    )


def test_stage4_aggregated_topology_reaches_declared_lower_bound_without_faking_execution() -> (
    None
):
    network = SpecializedAreaNetwork()
    topology = network.topology_summary()
    assert topology["total_neuron_budget"] >= STAGE4_MIN_NEURONS
    assert topology["total_synapse_budget"] >= STAGE4_MIN_SYNAPSES
    assert topology["lower_bound_satisfied"] is True
    assert topology["edges_materialized"] is False
    assert topology["dynamic_scale_execution_verified"] is False
    assert topology["productive_activation_enabled"] is False
    sample_a = network.edge_sample()
    sample_b = network.edge_sample()
    assert sample_a == sample_b
    assert len(sample_a) == 12
    assert {row["modality"] for row in sample_a} == {"audio", "vision", "digital"}


def test_stage4_reference_probes_cover_audio_vision_and_exact_digital_integrity() -> (
    None
):
    suite_a = reference_probe_suite()
    suite_b = reference_probe_suite()
    assert suite_a == suite_b
    probes = suite_a["probes"]
    assert isinstance(probes, dict)
    audio = probes["audio"]
    vision = probes["vision"]
    digital = probes["digital"]
    assert isinstance(audio, dict)
    assert isinstance(vision, dict)
    assert isinstance(digital, dict)
    assert audio["plasticity_rule"] == "phase_weighted_t_stdp_candidate"
    assert "candidate_weight_delta" in audio
    assert vision["plasticity_rule"] == "s_stdp_plus_structural_growth_candidate"
    assert "candidate_growth_probability" in vision
    assert digital["exact_integrity_pass"] is True
    assert digital["input_sha256"] == digital["output_sha256"]
    assert all(probe["canonical_core_mutated"] is False for probe in probes.values())
    assert all(
        probe["productive_activation_enabled"] is False for probe in probes.values()
    )


def test_stage4_contract_links_the_latest_msba_data_without_promoting_it_to_evidence() -> (
    None
):
    contract = specialized_area_contract()
    assert contract["status"] == "implemented_experimental"
    boundary = contract["scientific_boundary"]
    assert isinstance(boundary, dict)
    assert boundary["automatic_evidence_promotion"] is False
    assert boundary["human_review_required_for_evid"] is True
    assert contract["research_data"] == list(LATEST_MSBA_DATA)
    for relative in LATEST_MSBA_DATA:
        experiment = ROOT / relative
        assert (experiment / "report.md").is_file()
        assert (experiment / "analysis" / "statistics.json").is_file()


def test_latest_msba_data_preserves_key_observed_controls() -> None:
    e01 = json.loads(
        (ROOT / LATEST_MSBA_DATA[0] / "analysis" / "statistics.json").read_text(
            encoding="utf-8"
        )
    )
    conditions = e01["conditions"]
    accuracies = {
        name: values["metrics"]["task_accuracy"]["mean"]
        for name, values in conditions.items()
    }
    assert len(set(accuracies.values())) == 1
    costs = {
        name: values["metrics"]["normalized_energy_units_per_correct_decision"]["mean"]
        for name, values in conditions.items()
    }
    assert costs["digital"] < costs["audio"] < costs["vision"]

    e04 = json.loads(
        (ROOT / LATEST_MSBA_DATA[3] / "analysis" / "statistics.json").read_text(
            encoding="utf-8"
        )
    )
    for values in e04["conditions"].values():
        assert values["metrics"]["checksum_mismatches"]["max"] == 0.0
        assert values["metrics"]["exact_payload_mismatches"]["max"] == 0.0

    e05 = json.loads(
        (ROOT / LATEST_MSBA_DATA[4] / "analysis" / "statistics.json").read_text(
            encoding="utf-8"
        )
    )
    adaptive = e05["conditions"]["adaptive_compensation"]["metrics"]
    fixed = e05["conditions"]["fixed_allocation"]["metrics"]
    assert adaptive["compensatory_gate_change"]["mean"] > 0.0
    assert adaptive["task_recovery"]["mean"] > fixed["task_recovery"]["mean"]


def test_stage4_contract_remains_core_independent() -> None:
    source = (ROOT / "src" / "embodiment" / "specialized_areas.py").read_text(
        encoding="utf-8"
    )
    assert "from src.core" not in source
    assert "import src.core" not in source
