"""Facade used by the dashboard and CLI to access Playground capabilities."""

from __future__ import annotations

from dataclasses import replace
from typing import Mapping

from .analysis import ensemble_summary
from .builder.session import PlaygroundSession
from .geometry import geometry_literature_context
from .models import PlaygroundConfig
from .neural_io import CODEC_CATALOG, DECODER_CATALOG
from .pan import axis_schema, pan_literature_context, pan_research_candidates
from .persist.session_recorder import list_sessions
from .persist.session_replayer import replay_session
from .registry.neuron_models import NEURON_MODELS
from .registry.plasticity_rules import PLASTICITY_RULES
from .registry.readouts import READOUTS
from .registry.stimulus_generators import STIMULUS_REGISTRY
from .registry.synapse_models import SYNAPSE_MODELS
from .registry.topology_generators import TOPOLOGY_REGISTRY


def catalog() -> dict[str, object]:
    topology_notes = {
        "geometric_5d": (
            "Exploratory geometry with independent xyz Cartesian coordinates "
            "and cyclic torus coordinates a/b. State dimensions remain separate."
        ),
        "mhrn_5d": "Native MHRN (x,y,z,d4,d5) packing contract; default because it mirrors the MHRN architecture, not because it is superior.",
        "mhrn_5d_distance": "Native MHRN 5D coordinates with distance-bounded connectivity.",
        "mhrn_5d_neighbourhood": "Native MHRN 5D coordinates with k-nearest connectivity.",
        "generic_nd": "Generic N-dimensional grid (1..32D).",
        "generic_nd_distance": "Generic N-dimensional distance graph (1..32D).",
        "generic_nd_knn": "Generic N-dimensional k-nearest graph (1..32D).",
        "mhrn_experimental_nd": "Experimental extension of MHRN coordinate semantics beyond 5D; explicit tuple IDs, not canonical packed Brain5D storage.",
        "mhrn_experimental_nd_distance": "Experimental >5D MHRN-style geometry with distance connectivity; non-canonical tuple representation.",
        "mhrn_experimental_nd_neighbourhood": "Experimental >5D MHRN-style geometry with k-neighbour connectivity; non-canonical tuple representation.",
    }
    return {
        "class": "PLAYGROUND",
        "scientific_evidence": False,
        "models": [model.descriptor() for model in NEURON_MODELS.values()],
        "synapses": list(SYNAPSE_MODELS.values()),
        "plasticity": list(PLASTICITY_RULES.values()),
        "topologies": [
            {
                "name": name,
                "available": True,
                "note": topology_notes.get(name, "Exploratory network building block."),
            }
            for name in TOPOLOGY_REGISTRY
        ],
        "stimuli": [{"name": name, "available": True} for name in STIMULUS_REGISTRY],
        "readouts": [{"name": name, "available": True} for name in READOUTS],
        "analyses": [
            "ISI / CV(ISI)",
            "burst intervals",
            "first-spike / response latency",
            "persistence / propagation proxy",
            "synchrony / Fano",
            "population frequency spectrum",
            "degree distribution / hubs",
            "clustering / path length / components",
            "reciprocal and three-cycle motifs",
            "edge-distance distribution",
            "weight change / potentiation / depression / saturation",
            "structural additions / removals",
            "PCA explained variance / effective dimensionality",
            "seed-to-seed ensemble variation",
            "runtime / neuron updates / spikes per second",
            "PAN health / energy / apoptosis diagnostics",
            "PAN hyperstate population vector / bundle",
            "PAN closed-loop feedback magnitude",
            "settings-derived gate schematic",
            "dual event/continuous clock diagnostics",
            "bounded generative growth/pruning diagnostics",
            "CUDA memory-budget estimate / SSD offload telemetry",
            "geometric xyz/toroidal edge decomposition",
            "geometry Moran's-I autocorrelation",
            "xyz-only conduction-delay diagnostics",
            "neural I/O boundary / codec / projection / readout diagnostics",
            "functional thalamic relay / attention gating diagnostics",
            "hybrid cortical layer assignment / gain-plasticity diagnostics",
            "reward-modulated behavioral policy learning diagnostics",
            "QUERY / WAIT / RESPONSE / TIMEOUT lifecycle tracing",
        ],
        "robustness_controls": [
            "seed ensemble",
            "coordinate shuffle control",
            "random graph control",
            "dimension ablation",
            "neuron dropout / lesion",
            "stimulus perturbation",
        ],
        "pan": {
            "available": True,
            "classification": "PLAYGROUND_PAN",
            "scientific_evidence": False,
            "pid_status": "NOT_IMPLEMENTED",
            "gate_generation_status": "IMPLEMENTED_REFERENCE",
            "dual_clock_status": "IMPLEMENTED_REFERENCE",
            "generative_growth_status": "IMPLEMENTED_FIXED_CAPACITY_REFERENCE",
            "cuda_backend_status": "MEMORY_ESTIMATE_ONLY",
            "persistent_cuda_kernel_status": "NOT_IMPLEMENTED",
            "dynamic_parallelism_status": "NOT_IMPLEMENTED",
            "hardware_coupling_status": "NOT_IMPLEMENTED_EXPLORATORY_IDEA",
            "thermal_feedback_status": "NOT_IMPLEMENTED_EXPLORATORY_IDEA",
            "thalamic_gating_status": "IMPLEMENTED_FUNCTIONAL_REFERENCE",
            "cortical_layers_status": "IMPLEMENTED_FIXED_LABEL_PLASTIC_GAIN_REFERENCE",
            "behavioral_learning_status": "IMPLEMENTED_REWARD_POLICY_REFERENCE",
            "behavior_storage_principle": "POLICY_PARAMETERS_NOT_RAW_PAYLOADS",
            "existing_interfaces_reused": True,
            "information_axis": "local_surprise_proxy_not_PID",
            "default_axes": axis_schema(10),
            "research_candidates": pan_research_candidates(),
            "literature_context": pan_literature_context(),
            "note": (
                "Exploratory PAN layer only. Any research transition requires "
                "a new hypothesis, preregistration, freeze and canonical rerun."
            ),
        },
        "neural_io": {
            "available": True,
            "classification": "PLAYGROUND_NEURAL_IO",
            "scientific_evidence": False,
            "exact_payload_outside_snn": True,
            "boundary_principle": "Payload != Neural Representation",
            "architecture_principle": (
                "Codec != GatewayTopology != GatewayLearning"
            ),
            "roles": [
                "ASSOCIATIVE",
                "AFFERENT",
                "EFFERENT",
                "GATEWAY_AFFERENT",
                "GATEWAY_EFFERENT",
            ],
            "phases": ["IDLE", "QUERY", "WAIT", "RESPONSE", "TIMEOUT"],
            "codecs": [dict(item) for item in CODEC_CATALOG],
            "decoders": [dict(item) for item in DECODER_CATALOG],
            "network_area_adapter": (
                "src.embodiment.neural_symbiosis.NetworkAreaAdapter"
            ),
            "shared_query_response_layout": {
                "logical_shape": [100, 100],
                "logical_channels": 10_000,
                "status": "EXPERIMENTAL_CONCEPT_NOT_ALLOCATED_IN_PLAYGROUND",
            },
            "tool_plane_execution": False,
            "actuator_execution": False,
            "gateway_action_selection_status": "NOT_IMPLEMENTED_EXTERNAL_ROUND_TRIP",
            "playground_internal_policy_selection_status": "IMPLEMENTED_REFERENCE",
            "external_round_trip_status": "NOT_IMPLEMENTED",
            "lifecycle_status": "REFERENCE_STATE_MACHINE_ONLY",
            "note": (
                "Reference implementation of the postulated MHRN Gateway "
                "Neural Interface. Exact payloads stay outside the SNN."
            ),
        },
        "geometry": {
            "available": True,
            "classification": "PLAYGROUND_GEOMETRY",
            "scientific_evidence": False,
            "state_space_independent": True,
            "geometry_dimensions": 5,
            "axes": ["x", "y", "z", "a", "b"],
            "topological_manifold": "torus_S1_x_S1",
            "klein_bottle_status": "NOT_IMPLEMENTED",
            "modes": ["mixed_additive", "shortcut_union"],
            "activity_dependent_positioning_status": "NOT_IMPLEMENTED",
            "neurogenesis_status": "NOT_IMPLEMENTED",
            "literature_context": geometry_literature_context(),
        },
        "limits": {
            "n_neurons": 1024,
            "edges": 20_000,
            "ticks": 2048,
            "dimensions": 32,
            "ensemble_runs": 8,
            "cuda_budget_mb": 16384,
            "default_cuda_budget_mb": 2048,
            "hardware_profiles": ["reference_cpu", "cuda_8gb_balanced_plan"],
        },
        "governance": {
            "promotion_path": "none",
            "registry_visible": False,
            "maturity_contributing": False,
            "canonical_reexecution_required": True,
        },
    }


def _single(config: PlaygroundConfig) -> dict[str, object]:
    return PlaygroundSession(config).run()


def run(payload: Mapping[str, object]) -> dict[str, object]:
    config = PlaygroundConfig.from_mapping(payload)
    primary = _single(replace(config, ensemble_runs=1))
    if config.ensemble_runs <= 1:
        return primary
    ensemble: list[dict[str, object]] = [primary]
    for offset in range(1, config.ensemble_runs):
        ensemble.append(
            _single(
                replace(
                    config,
                    seed=config.seed + offset,
                    ensemble_runs=1,
                    persist=False,
                )
            )
        )
    primary["ensemble"] = ensemble_summary(ensemble)
    return primary


def robustness(payload: Mapping[str, object]) -> dict[str, object]:
    """Run bounded exploratory controls without producing scientific evidence."""

    base = PlaygroundConfig.from_mapping(payload)
    base = replace(base, ensemble_runs=1, persist=False)
    primary = _single(base)
    controls: dict[str, object] = {}

    controls["coordinate_shuffle"] = _single(
        replace(base, topology="5d_shuffled", dimensions=5)
    )
    controls["random_graph"] = _single(
        replace(base, topology="random_graph", dimensions=2)
    )

    ablations: list[dict[str, object]] = []
    for dimensions in sorted({2, 3, max(1, base.dimensions - 1), base.dimensions}):
        ablations.append(
            _single(
                replace(
                    base,
                    topology="generic_nd",
                    dimensions=dimensions,
                    seed=base.seed + 100 + dimensions,
                )
            )
        )
    dimension_ablation: list[dict[str, object]] = []
    for item in ablations:
        topology_value = item.get("topology")
        dimensions_value = (
            topology_value.get("dimensions")
            if isinstance(topology_value, Mapping)
            else None
        )
        dimension_ablation.append(
            {
                "dimensions": dimensions_value,
                "metrics": item.get("metrics"),
            }
        )
    controls["dimension_ablation"] = dimension_ablation

    reduced_n = max(2, int(base.n_neurons * 0.8))
    reduced_budget = max(
        reduced_n,
        min(base.edge_budget, reduced_n * (reduced_n - 1)),
    )
    controls["neuron_dropout_20pct"] = _single(
        replace(
            base,
            n_neurons=reduced_n,
            edge_budget=reduced_budget,
            seed=base.seed + 201,
        )
    )

    controls["stimulus_perturbation"] = _single(
        replace(
            base,
            stimulus_current=min(500.0, base.stimulus_current * 1.1 + 0.1),
            seed=base.seed + 301,
        )
    )

    def summary(item: object) -> object:
        if isinstance(item, dict) and "metrics" in item:
            return {
                "metrics": item.get("metrics"),
                "analysis": item.get("analysis"),
                "topology": {
                    "name": item.get("topology", {}).get("name"),
                    "dimensions": item.get("topology", {}).get("dimensions"),
                },
            }
        return item

    return {
        "manifest": primary["manifest"],
        "classification": "PLAYGROUND_ROBUSTNESS",
        "scientific_evidence": False,
        "primary": summary(primary),
        "controls": {
            key: (
                [summary(value) for value in item]
                if isinstance(item, list)
                else summary(item)
            )
            for key, item in controls.items()
        },
        "note": (
            "Exploratory robustness controls only. These are not matched, "
            "preregistered or evidence-eligible comparisons."
        ),
    }


def sessions() -> dict[str, object]:
    return {
        "class": "PLAYGROUND",
        "scientific_evidence": False,
        "sessions": list_sessions(),
    }


def replay(session_id: str) -> dict[str, object]:
    return replay_session(session_id)
