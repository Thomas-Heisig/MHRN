"""Contracts for the isolated non-canonical MHRN Playground."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.core.spatial_index import pack_coords
from src.playground import Playground, PlaygroundComposer, PlaygroundConfig
from src.playground._isolation import (
    PlaygroundIsolation,
    PlaygroundIsolationError,
    playground_manifest,
)
from src.playground.pan.hypervector import bind, bundle
from src.playground.pan.literature import pan_literature_context
from src.playground.persist import session_recorder
from src.playground.persist.session_recorder import record_session
from src.playground.registry.topology_generators import build_topology
from src.playground.service import catalog, robustness, run
from src.research.registry import ResearchRegistry

ROOT = Path(__file__).resolve().parents[1]


def _small_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "name": "test",
        "n_neurons": 12,
        "edge_budget": 24,
        "ticks": 12,
        "seed": 7,
        "topology": "mhrn_5d",
        "neuron_model": "izhikevich_rs",
        "stimulus": "deterministic",
    }
    payload.update(overrides)
    return payload


def test_playground_manifest_is_never_scientific_evidence() -> None:
    manifest = playground_manifest()
    assert manifest["class"] == "PLAYGROUND"
    assert manifest["scientific_evidence"] is False
    assert manifest["data"] is False
    assert manifest["evidence_eligible"] is False
    assert manifest["registry_visible"] is False
    assert manifest["maturity_contributing"] is False
    assert manifest["promotion_path"] == "none"
    assert manifest["note"] == (
        "Exploratory session. Not part of scientific evaluation."
    )


def test_playground_blocks_canonical_research_writes() -> None:
    with pytest.raises(PlaygroundIsolationError):
        PlaygroundIsolation.write_text(
            ROOT / "research" / "registry" / "claims.yaml",
            "forbidden",
        )
    with pytest.raises(PlaygroundIsolationError):
        PlaygroundIsolation.write_text(
            ROOT / "src" / "research" / "forbidden.txt",
            "forbidden",
        )


def test_playground_catalog_contains_full_building_block_families() -> None:
    payload = catalog()
    model_names = {item["name"] for item in payload["models"]}
    assert {
        "izhikevich_rs",
        "izhikevich_fs",
        "izhikevich_ib",
        "izhikevich_chattering",
        "izhikevich_lts",
        "izhikevich_resonator",
        "izhikevich_sensory",
        "izhikevich_motor",
        "lif",
        "adex",
        "hodgkin_huxley_na_k_ca",
        "multi_compartment_linear",
        "multi_compartment_nmda",
    } <= model_names

    topology_names = {item["name"] for item in payload["topologies"]}
    assert {
        "mhrn_5d",
        "mhrn_5d_distance",
        "mhrn_5d_neighbourhood",
        "mhrn_experimental_nd",
        "mhrn_experimental_nd_distance",
        "mhrn_experimental_nd_neighbourhood",
        "generic_nd",
        "generic_nd_distance",
        "generic_nd_knn",
        "feedforward",
        "recurrent",
        "reservoir",
        "bipartite",
        "dense",
        "small_world",
        "scale_free",
        "modular",
        "recurrent_modular",
        "recurrent_small_world",
        "hierarchical",
    } <= topology_names

    plasticity_names = {item["name"] for item in payload["plasticity"]}
    assert {
        "stdp",
        "triplet_stdp",
        "metaplasticity",
        "eligibility_trace",
        "three_factor",
        "homeostatic",
        "structural",
        "delay_plasticity",
    } <= plasticity_names
    assert payload["limits"]["dimensions"] == 32


def test_native_mhrn_5d_uses_canonical_packing_contract() -> None:
    topology = build_topology("mhrn_5d", 8, 16, 3)
    assert topology.dimensions == 5
    assert topology.metadata["geometry_class"] == "mhrn_native_5d"
    packed = topology.metadata["packed_neuron_ids"]
    assert packed[0] == pack_coords(0, 0, 0, 0, 0)
    assert packed[1] == pack_coords(1, 0, 0, 0, 0)
    assert len(set(packed)) == 8


def test_experimental_mhrn_nd_is_explicitly_noncanonical() -> None:
    topology = build_topology(
        "mhrn_experimental_nd",
        12,
        24,
        4,
        dimensions=8,
    )
    assert topology.dimensions == 8
    assert topology.metadata["geometry_class"] == "mhrn_experimental_nd"
    assert topology.metadata["canonical_packed_id"] is False
    assert topology.metadata["packing_contract"] == "explicit_tuple_only"


def test_generic_nd_runs_above_five_dimensions() -> None:
    result = run(
        _small_payload(
            topology="generic_nd",
            dimensions=9,
        )
    )
    assert result["topology"]["dimensions"] == 9
    assert result["analysis"]["dimensionality"]["coordinate_dimensions"] == 9


def test_run_exposes_full_descriptive_analysis_and_is_non_evidential() -> None:
    result = run(_small_payload())
    assert result["manifest"]["class"] == "PLAYGROUND"
    assert result["manifest"]["scientific_evidence"] is False
    analysis = result["analysis"]
    assert analysis["classification"]["interpretation"] == (
        "descriptive_exploration_only"
    )
    assert "isi_cv_mean" in analysis["spike_time"]
    assert "clustering_coefficient" in analysis["network"]
    assert "pca_explained_variance_ratio" in analysis["dimensionality"]
    assert "weight_change_mean" in analysis["plasticity"]
    assert "runtime_seconds" in analysis["performance"]


@pytest.mark.parametrize(
    ("synapse", "plasticity"),
    [
        ("stdp", "stdp"),
        ("triplet_stdp", "triplet_stdp"),
        ("eligibility_trace", "eligibility_trace"),
        ("three_factor", "three_factor"),
        ("static", "metaplasticity"),
        ("static", "homeostatic"),
        ("static", "structural"),
        ("delay_plastic", "delay_plasticity"),
        ("quantal_stp", "none"),
    ],
)
def test_plasticity_and_synapse_building_blocks_execute(
    synapse: str, plasticity: str
) -> None:
    result = run(
        _small_payload(
            synapse_model=synapse,
            plasticity_rule=plasticity,
            ticks=10,
        )
    )
    assert result["manifest"]["evidence_eligible"] is False
    assert "plasticity" in result["analysis"]


def test_seed_ensemble_is_descriptive_only() -> None:
    result = run(_small_payload(ensemble_runs=3, ticks=8))
    assert result["ensemble"]["runs"] == 3
    assert "seed_to_seed" in result["ensemble"]
    assert result["manifest"]["scientific_evidence"] is False


def test_robustness_suite_is_non_preregistered_playground_only() -> None:
    result = robustness(_small_payload(ticks=8))
    assert result["classification"] == "PLAYGROUND_ROBUSTNESS"
    assert result["scientific_evidence"] is False
    assert {
        "coordinate_shuffle",
        "random_graph",
        "dimension_ablation",
        "neuron_dropout_20pct",
        "stimulus_perturbation",
    } <= set(result["controls"])


def test_playground_session_cannot_change_registry_or_maturity_files(
    tmp_path: Path,
) -> None:
    guarded = [
        ROOT / "research" / "registry" / "claims.yaml",
        ROOT / "research" / "registry" / "hypotheses.yaml",
        ROOT / "research" / "registry" / "stage1_baseline.json",
        ROOT / "research" / "generated" / "EVIDENCE_MATRIX.md",
    ]
    before = {path: path.read_bytes() for path in guarded if path.exists()}
    result = run(_small_payload())
    record_session("PG-TEST", result, root=tmp_path / "sessions")
    after = {path: path.read_bytes() for path in guarded if path.exists()}
    assert after == before


def test_research_registry_ignores_playground_json_even_inside_registry_dir(
    tmp_path: Path,
) -> None:
    registry_dir = tmp_path / "registry"
    registry_dir.mkdir()
    (registry_dir / "playground_session.json").write_text(
        json.dumps(playground_manifest()),
        encoding="utf-8",
    )
    registry = ResearchRegistry(registry_dir).load_all()
    assert registry.questions == {}
    assert registry.hypotheses == {}
    assert registry.claims == {}
    assert registry.sources == {}


def test_playground_config_rejects_unbounded_runs() -> None:
    with pytest.raises(ValueError):
        PlaygroundConfig.from_mapping(
            {"n_neurons": 2048, "edge_budget": 4096, "ticks": 20}
        )
    with pytest.raises(ValueError):
        PlaygroundConfig.from_mapping(
            {"n_neurons": 64, "edge_budget": 128, "dimensions": 33}
        )


def test_playground_facade_matches_interactive_api() -> None:
    session = Playground(**_small_payload(ticks=8))
    result = session.run(ticks=12)
    assert result["config"]["ticks"] == 12
    assert result["manifest"]["promotion_path"] == "none"


def test_composer_supports_more_than_five_dimensions() -> None:
    topology = (
        PlaygroundComposer(n_neurons=12, seed=5, dimensions=8)
        .add_layer("input", dim=1, n=4)
        .add_layer("hidden", dim=8, n=8)
        .connect("input", "hidden", budget=8)
        .connect("hidden", "hidden", budget=8)
        .build()
    )
    assert topology.name == "composed"
    assert topology.dimensions == 8
    assert len(topology.coordinates) == 12
    assert 8 <= len(topology.edges) <= 16


def test_public_mhrn_playground_namespace() -> None:
    from mhrn_playground import Playground as PublicPlayground

    session = PublicPlayground(**_small_payload(ticks=4))
    result = session.run()
    assert result["manifest"]["class"] == "PLAYGROUND"


def test_session_size_limit_is_enforced(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(session_recorder, "MAX_SESSION_BYTES", 128)
    payload = {
        "session_id": "PG-OVERSIZE",
        "manifest": playground_manifest(),
        "config": {"name": "oversize"},
        "blob": "x" * 1024,
    }
    with pytest.raises(ValueError, match="persistence limit"):
        record_session("PG-OVERSIZE", payload, root=tmp_path / "sessions")


def test_session_retention_prunes_expired_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "sessions"
    root.mkdir()
    old = root / "PG-OLD.json"
    old.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(session_recorder, "RETENTION_DAYS", 1)
    expired = 1_000_000.0
    import os

    os.utime(old, (expired, expired))
    session_recorder._prune_sessions(root, now=expired + 2 * 24 * 60 * 60)
    assert not old.exists()



def test_pan_catalog_is_explicitly_exploratory() -> None:
    payload = catalog()
    model_names = {item["name"] for item in payload["models"]}
    synapse_names = {item["name"] for item in payload["synapses"]}
    assert "pan_adex_5d" in model_names
    assert "pan_stp_stdp" in synapse_names
    pan = payload["pan"]
    assert pan["classification"] == "PLAYGROUND_PAN"
    assert pan["scientific_evidence"] is False
    assert pan["pid_status"] == "NOT_IMPLEMENTED"
    assert pan["information_axis"] == "local_surprise_proxy_not_PID"
    assert all(
        candidate["status"] == "DRAFT_IDEA_NOT_PREREGISTERED"
        for candidate in pan["research_candidates"]
    )


def test_pan_hypervector_binding_and_bundling_are_dimension_safe() -> None:
    left = [1.0, 2.0, 3.0, 4.0, 5.0]
    right = [2.0, 1.0, -1.0, 0.5, 2.0]
    assert bind(left, right) == [2.0, 2.0, -3.0, 2.0, 10.0]
    bundled = bundle([left, right])
    assert bundled == [1.0, 1.0, 1.0, 1.0, 1.0]
    with pytest.raises(ValueError):
        bind(left, right[:-1])


def test_pan_run_remains_non_evidential_and_exposes_hyperstate() -> None:
    result = run(
        _small_payload(
            neuron_model="pan_adex_5d",
            synapse_model="pan_stp_stdp",
            pan_enabled=True,
            pan_dimensions=7,
            pan_closed_loop=True,
            pan_feedback_gain=0.02,
            ticks=16,
        )
    )
    assert result["manifest"]["class"] == "PLAYGROUND"
    assert result["manifest"]["evidence_eligible"] is False
    pan = result["pan"]
    assert pan["classification"] == "PLAYGROUND_PAN"
    assert pan["scientific_evidence"] is False
    assert pan["dimensions"] == 7
    assert len(pan["population_vector"]) == 7
    assert len(pan["population_bundle"]) == 7
    assert pan["pid_status"] == "NOT_IMPLEMENTED"
    assert pan["world_model_status"] == (
        "exploratory_state_space_only_not_validated_world_model"
    )
    assert pan["promotion_path"].startswith("new hypothesis")


def test_pan_run_cannot_mutate_research_registry_or_maturity() -> None:
    guarded = [
        ROOT / "research" / "registry" / "claims.yaml",
        ROOT / "research" / "registry" / "hypotheses.yaml",
        ROOT / "research" / "registry" / "stage1_baseline.json",
        ROOT / "research" / "generated" / "EVIDENCE_MATRIX.md",
    ]
    before = {path: path.read_bytes() for path in guarded if path.exists()}
    result = run(
        _small_payload(
            pan_enabled=True,
            pan_dimensions=5,
            ticks=8,
        )
    )
    assert result["pan"]["scientific_evidence"] is False
    after = {path: path.read_bytes() for path in guarded if path.exists()}
    assert after == before


def test_pan_config_rejects_invalid_hyperstate_dimensions() -> None:
    with pytest.raises(ValueError, match="pan_dimensions"):
        PlaygroundConfig.from_mapping(
            {
                "n_neurons": 12,
                "edge_budget": 24,
                "pan_enabled": True,
                "pan_dimensions": 4,
            }
        )



def test_pan_literature_context_is_bounded_and_not_novelty_proof() -> None:
    context = pan_literature_context()
    assert context["classification"] == "PLAYGROUND_LITERATURE_CONTEXT"
    assert context["scientific_evidence_for_pan"] is False
    assert context["novelty_status"] == (
        "TARGETED_SEARCH_NO_INTEGRATED_EQUIVALENT_IDENTIFIED_NOT_NOVELTY_PROOF"
    )
    sources = context["sources"]
    assert len(sources) >= 10
    assert any(source["topic"] == "pid_learning" for source in sources)
    assert any(source["topic"] == "homeostasis" for source in sources)
    assert any(source["topic"] == "aging_transition" for source in sources)


def test_pan_literature_distinguishes_two_sadp_meanings() -> None:
    context = pan_literature_context()
    sources = context["sources"]
    amplitude = [
        source for source in sources
        if source["topic"] == "spike_amplitude_plasticity"
    ]
    agreement = [
        source for source in sources
        if source["topic"] == "spike_agreement_plasticity"
    ]
    assert amplitude and agreement
    assert amplitude[0]["key"] != agreement[0]["key"]
