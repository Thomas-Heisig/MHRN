"""Repository-derived development maturity for the Release workspace.

The timeline is an engineering observability projection, not a scientific
claim. Criteria are evaluated from structured repository artifacts, concrete
module/test paths, registry objects, verification JSON and measured runtime
size. Markdown roadmap prose is exposed as a source link only; it cannot
make a stage pass.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypedDict, cast

from src.dashboard.verification import evaluate_test_baseline
from src.research.registry import ResearchRegistry

CriterionStatus = str


class Criterion(TypedDict):
    id: str
    label: str
    status: CriterionStatus
    source: str
    evidence: list[str]


class RuntimeSize(TypedDict):
    neurons: int | None
    synapses: int | None
    source: str
    status: str
    snapshot_tick: int | None


class TimelineStage(TypedDict):
    stage: int
    id: str
    name: str
    short_label: str
    description: list[str]
    scale: dict[str, str]
    criteria: list[Criterion]
    implementation_score: float
    verification_score: float
    research_readiness_score: float
    status: str
    relevant_modules: list[str]
    relevant_tests: list[str]
    relevant_experiments: list[str]
    relevant_research_questions: list[str]
    known_limits: list[str]
    open_todos: list[str]
    next_technical_steps: list[str]


class DevelopmentTimeline(TypedDict):
    schema_version: int
    current_stage: float
    scientific_stage: float
    stage_floor: int
    stage_next: int | None
    progress_to_next: float
    scientific_progress_to_next: float
    current_label: str
    scientific_label: str
    current_runtime: RuntimeSize
    last_observed_runtime: RuntimeSize | None
    stages: list[TimelineStage]
    engineering_score: float
    verification_score: float
    scientific_evidence_score: float
    confidence: float
    sources: list[dict[str, object]]
    last_updated: str
    scientific_note: str
    consciousness_claim: str


@dataclass(frozen=True)
class CriterionSpec:
    id: str
    label: str
    paths: tuple[str, ...] = ()
    tests: tuple[str, ...] = ()
    verification: tuple[str, ...] = ()
    registry: str | None = None
    registry_minimum: int = 1
    planned: bool = False


@dataclass(frozen=True)
class StageSpec:
    stage: int
    id: str
    name: str
    short_label: str
    description: tuple[str, ...]
    scale: dict[str, str]
    criteria: tuple[CriterionSpec, ...]
    modules: tuple[str, ...]
    tests: tuple[str, ...]
    experiments: tuple[str, ...]
    research_questions: tuple[str, ...]
    limits: tuple[str, ...]
    todos: tuple[str, ...]
    next_steps: tuple[str, ...]


_STATUS_VALUES = {"implemented", "verified", "experimental", "planned", "missing"}
_IMPLEMENTATION_POINTS = {
    "implemented": 1.0,
    "verified": 1.0,
    "experimental": 0.75,
    "planned": 0.0,
    "missing": 0.0,
}
_VERIFICATION_POINTS = {
    "implemented": 0.25,
    "verified": 1.0,
    "experimental": 0.25,
    "planned": 0.0,
    "missing": 0.0,
}
_RESEARCH_POINTS = {
    "implemented": 0.1,
    "verified": 0.5,
    "experimental": 0.25,
    "planned": 0.0,
    "missing": 0.0,
}


def _stage_specs() -> tuple[StageSpec, ...]:
    """Return the canonical, intentionally explicit ten-stage model."""
    return (
        StageSpec(
            0,
            "single_neuron",
            "Einzelne Nervenzelle",
            "Neuron",
            (
                "Einzelnes künstliches Neuron",
                "deterministische Membrandynamik",
                "Spike-, Reset- und Erholungsverhalten",
                "versionierte und umschaltbare Neuronenmodelle",
            ),
            {"neurons": "1", "synapses": "0-1"},
            (
                CriterionSpec(
                    "neuron_model",
                    "Versioned neuron model",
                    paths=("src/core/neuron.py", "src/core/neuron_models.py"),
                    tests=("tests/test_single_neuron_contract.py",),
                    verification=(
                        "research/generated/verification/single_neuron_reference.json",
                    ),
                ),
                CriterionSpec(
                    "membrane_dynamics",
                    "Deterministic membrane dynamics",
                    paths=("src/core/neuron.py", "src/core/neuron_models.py"),
                    tests=("tests/test_single_neuron_contract.py",),
                    verification=(
                        "research/generated/verification/single_neuron_reference.json",
                    ),
                ),
                CriterionSpec(
                    "spike_and_refractory",
                    "Spike, reset, recovery and refractory variant",
                    tests=("tests/test_single_neuron_contract.py",),
                    verification=(
                        "research/generated/verification/single_neuron_reference.json",
                    ),
                ),
                CriterionSpec(
                    "single_cell_verification",
                    "Deterministic replay and state continuation",
                    tests=("tests/test_single_neuron_contract.py",),
                    verification=(
                        "research/generated/verification/single_neuron_reference.json",
                    ),
                ),
                CriterionSpec(
                    "model_switch_provenance",
                    "Model selection and provenance",
                    paths=("src/core/neuron_models.py",),
                    tests=("tests/test_single_neuron_contract.py",),
                    verification=(
                        "research/generated/verification/single_neuron_reference.json",
                    ),
                ),
            ),
            ("src/core/neuron.py", "src/core/neuron_models.py"),
            ("tests/test_neuron.py", "tests/test_single_neuron_contract.py"),
            (),
            (),
            (
                "This stage is a software primitive, not evidence of biological equivalence.",
            ),
            (),
            (),
        ),
        StageSpec(
            1,
            "small_snn",
            "Kleines SNN",
            "SNN",
            (
                "Mehrere gekoppelte Neuronen",
                "erste Synapsen",
                "einfache Spike-Ausbreitung",
            ),
            {"neurons": "10-1,000", "synapses": "10-10,000"},
            (
                CriterionSpec(
                    "network_core",
                    "Network core",
                    paths=("src/core/network.py", "src/core/synapse.py"),
                ),
                CriterionSpec(
                    "spike_propagation",
                    "Spike propagation",
                    tests=("tests/test_network.py", "tests/test_small_snn_contract.py"),
                    verification=(
                        "research/generated/verification/small_snn_reference.json",
                    ),
                ),
                CriterionSpec(
                    "sparse_topology",
                    "Sparse topology",
                    paths=("src/core/spatial_index.py",),
                ),
            ),
            ("src/core/network.py", "src/core/synapse.py", "src/core/spatial_index.py"),
            ("tests/test_network.py", "tests/test_small_snn_contract.py"),
            (),
            (),
            ("Small-network tests do not establish large-scale tractability.",),
            (),
            (),
        ),
        StageSpec(
            2,
            "recurrent_snn",
            "Stabiles rekurrentes SNN",
            "Rekurrenz",
            (
                "Rekurrente Konnektivität",
                "stabile Spike-Dynamik",
                "lange deterministische Runs",
            ),
            {"neurons": "1,000-10,000", "synapses": "10,000-100,000"},
            (
                CriterionSpec(
                    "recurrent_network",
                    "Recurrent network execution",
                    paths=("src/core/network.py",),
                    tests=("tests/test_recurrent_snn_contract.py",),
                    verification=(
                        "research/generated/verification/recurrent_snn_reference.json",
                    ),
                ),
                CriterionSpec(
                    "deterministic_runtime",
                    "Deterministic runtime state",
                    paths=("src/controller/runtime.py",),
                    tests=(
                        "tests/test_v06_pause_resume_identity.py",
                        "tests/test_recurrent_snn_contract.py",
                    ),
                    verification=(
                        "research/generated/verification/recurrent_snn_reference.json",
                    ),
                ),
                CriterionSpec(
                    "restart_restore",
                    "Restart and restore identity",
                    paths=("src/storage/recovery.py", "src/storage/b5d.py"),
                    verification=(
                        "research/generated/verification/restore_determinism.json",
                    ),
                ),
                CriterionSpec(
                    "long_run_protocol", "Long-run protocol", registry="protocols"
                ),
            ),
            (
                "src/core/network.py",
                "src/controller/runtime.py",
                "src/storage/recovery.py",
                "src/storage/b5d.py",
            ),
            (
                "tests/test_v06_pause_resume_identity.py",
                "tests/test_recurrent_snn_contract.py",
                "tests/test_recurrent_snn_timeline.py",
                "tests/test_recurrent_snn_frontend.py",
            ),
            (
                "research/protocols",
                "research/experiments/EXP-BATCH-20260908200906-01",
            ),
            ("RQ-SNN-001", "RQ10"),
            (
                "A deterministic runtime is not a claim about cognition.",
                "Stage 2 is technically complete at the scoped deterministic recurrence boundary; target-scale tractability remains a separate benchmark question.",
            ),
            (),
            (),
        ),
        StageSpec(
            3,
            "plastic_neural_tissue",
            "Plastisches Nervengewebe",
            "Plastizität",
            (
                "STDP",
                "Drei-Faktor-Plastizität",
                "Homeostase",
                "strukturelle Plastizität und Ressourcenregulation",
            ),
            {"neurons": "10,000-100,000", "synapses": "10^5-10^7"},
            (
                CriterionSpec(
                    "stdp_implemented",
                    "STDP",
                    paths=("src/core/synapse.py", "src/learning/stdp_plugin.py"),
                    tests=("tests/test_stdp_integration.py",),
                    verification=(
                        "research/generated/verification/plastic_neural_tissue_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "three_factor_plasticity",
                    "Three-factor plasticity",
                    paths=(
                        "src/learning/eligibility.py",
                        "src/learning/reward.py",
                        "src/learning/learning_engine.py",
                    ),
                    tests=(
                        "tests/test_reward.py",
                        "tests/test_learning_experiment.py",
                    ),
                    verification=(
                        "research/generated/verification/plastic_neural_tissue_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "homeostasis_implemented",
                    "Homeostasis",
                    paths=("src/homeostasis/engine.py",),
                    tests=("tests/test_homeostasis_engine.py",),
                    verification=(
                        "research/generated/verification/plastic_neural_tissue_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "structural_plasticity",
                    "Structural growth and pruning",
                    paths=(
                        "src/self_organization/engine.py",
                        "src/self_organization/coordinator.py",
                        "src/storage/structural_journal.py",
                    ),
                    verification=(
                        "research/generated/verification/structural_e2e.json",
                        "research/generated/verification/plastic_neural_tissue_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "integrated_plasticity_reference",
                    "Integrated plasticity reference and persisted adaptive state",
                    tests=(
                        "tests/test_stage3_plastic_neural_tissue.py",
                        "tests/test_checkpoint_v4.py",
                    ),
                    verification=(
                        "research/generated/verification/plastic_neural_tissue_reference_alpha3.json",
                    ),
                ),
            ),
            (
                "src/core/synapse.py",
                "src/learning",
                "src/homeostasis/engine.py",
                "src/self_organization",
                "src/storage/structural_journal.py",
            ),
            (
                "tests/test_stdp_integration.py",
                "tests/test_reward.py",
                "tests/test_learning_experiment.py",
                "tests/test_homeostasis_engine.py",
                "tests/test_structural_e2e.py",
                "tests/test_structural_determinism.py",
                "tests/test_checkpoint_v4.py",
                "tests/test_stage3_plastic_neural_tissue.py",
            ),
            (
                "src/experiments/learning_lab.py",
                "scripts/run_stage3_reference.py",
                "research/generated/verification/plastic_neural_tissue_reference_alpha3.json",
            ),
            ("RQ1", "RQ3", "RQ5", "RQ10"),
            (
                "The scoped reference does not establish the declared 10,000-100,000 neuron Stage-3 target scale.",
                "Engineering verification does not promote productive-learning DATA to scientific EVID.",
            ),
            ("R2 productive-learning evidence closure",),
            (
                "Run preregistered independent learning-on/off, sham/information-destroyed and held-out experiments with human evidence review.",
            ),
        ),
        StageSpec(
            4,
            "specialized_neural_areas",
            "Spezialisierte neuronale Areale",
            "Areale",
            (
                "Auditive, visuelle und digitale Pfade",
                "modality-specific pathways",
                "unterschiedliche Adapter- und Plastizitätsregeln",
            ),
            {"neurons": "10^5-10^6", "synapses": "10^7-10^8"},
            (
                CriterionSpec(
                    "modality_pathways",
                    "Typed modality pathways",
                    paths=(
                        "src/signal_processing",
                        "src/embodiment/msba.py",
                        "src/embodiment/specialized_areas.py",
                    ),
                    tests=("tests/test_stage4_specialized_neural_areas.py",),
                    verification=(
                        "research/generated/verification/specialized_neural_areas_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "neural_symbiosis_gateway",
                    "Neural Symbiosis gateway",
                    paths=(
                        "src/embodiment/neural_symbiosis.py",
                        "src/embodiment/peripheral_adapters.py",
                        "src/experiments/msba_lab.py",
                    ),
                    tests=(
                        "tests/test_gateway_runtime.py",
                        "tests/test_msba_experiment_runner.py",
                    ),
                    verification=(
                        "research/generated/verification/specialized_neural_areas_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "provenance_bound_treatments",
                    "Provenance-bound treatments and matched controls",
                    paths=(
                        "src/embodiment/msba.py",
                        "src/embodiment/peripheral_adapters.py",
                        "src/research/experiment_recorder.py",
                    ),
                    tests=("tests/test_msba_experiment_runner.py",),
                    verification=(
                        "research/generated/verification/specialized_neural_areas_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "scaled_area_network",
                    "Aggregated Stage-4 area scale contract",
                    paths=("src/embodiment/specialized_areas.py",),
                    tests=("tests/test_stage4_specialized_neural_areas.py",),
                    verification=(
                        "research/generated/verification/specialized_neural_areas_reference_alpha3.json",
                    ),
                ),
            ),
            (
                "src/signal_processing",
                "src/embodiment/msba.py",
                "src/embodiment/neural_symbiosis.py",
                "src/embodiment/peripheral_adapters.py",
                "src/embodiment/specialized_areas.py",
            ),
            (
                "tests/test_msba.py",
                "tests/test_signal_processing_contracts.py",
                "tests/test_gateway_runtime.py",
                "tests/test_msba_experiment_runner.py",
                "tests/test_stage4_specialized_neural_areas.py",
                "tests/test_dashboard_embodiment_routes.py",
            ),
            (
                "src/experiments/msba_lab.py",
                "scripts/run_stage4_reference.py",
                "research/experiments/EXP-BATCH-20260914074039-90",
                "research/experiments/EXP-BATCH-20260914074039-91",
                "research/experiments/EXP-BATCH-20260914074039-92",
                "research/experiments/EXP-BATCH-20260914074039-93",
                "research/experiments/EXP-BATCH-20260914074039-94",
            ),
            (
                "RQ9",
                "RQ11",
                "RQ-MSBA-E01",
                "RQ-MSBA-E02",
                "RQ-MSBA-E03",
                "RQ-MSBA-E04",
                "RQ-MSBA-E05",
            ),
            (
                "The Stage-4 lower-bound scale is an aggregated topology budget; a dynamically executed 100k-neuron/10M-edge multimodal SNN is not claimed.",
                "Peripheral adapters and plasticity remain experiment-only; productive activation stays locked.",
                "Recorded E01-E05 runs are DATA and are not automatically promoted to EVID.",
            ),
            (
                "R4 scientific evidence promotion and independent review remain separate from scoped engineering completion.",
                "Large dynamic multimodal scaling remains a performance/scaling study rather than a Stage-4 contract prerequisite.",
            ),
            (
                "Run independent confirmatory review of E01-E05 before any EVID promotion.",
                "Benchmark dynamically materialized multimodal networks separately at increasing scale.",
            ),
        ),
        StageSpec(
            5,
            "integrated_artificial_nervous_system",
            "Integriertes künstliches Nervensystem",
            "Nervensystem",
            (
                "Sensorik, Interozeption und Aktorik",
                "Feedbackschleifen",
                "Embodiment und Ressourcenhaushalt",
            ),
            {"neurons": "10^6-10^7", "synapses": "10^8-10^9"},
            (
                CriterionSpec(
                    "sensor_contracts",
                    "Sensor input contracts",
                    paths=("src/embodiment/models.py", "src/embodiment/connections.py"),
                ),
                CriterionSpec(
                    "interoception",
                    "Interoception",
                    paths=("src/embodiment/interoception.py",),
                ),
                CriterionSpec(
                    "authorized_actuation",
                    "Authorized actuator path",
                    paths=("src/embodiment/controlled.py", "src/embodiment/audit.py"),
                ),
                CriterionSpec(
                    "closed_loop_environment",
                    "Closed-loop environment",
                    paths=(
                        "src/experience/engine.py",
                        "src/embodiment/deterministic.py",
                    ),
                    tests=("tests/test_experience_engine.py",),
                ),
                CriterionSpec(
                    "resource_accounting",
                    "Resource accounting",
                    paths=("src/embodiment/msba.py",),
                ),
            ),
            ("src/embodiment", "src/experience"),
            ("tests/test_experience_engine.py",),
            ("src/experiments/embodiment_lab.py",),
            ("RQ6", "RQ7", "RQ8", "RQ9"),
            ("Real-device and long-horizon embodiment claims remain out of scope.",),
            ("R3 closed-loop embodiment evidence closure",),
            ("Complete independent closed-loop replications and failure controls.",),
        ),
        StageSpec(
            6,
            "memory_world_model",
            "Gedächtnis und Weltmodell",
            "Weltmodell",
            (
                "Episodisches und semantisches Gedächtnis",
                "zeitliche Modelle",
                "Vorhersage und Prediction Error",
            ),
            {"neurons": "10^7-10^8", "synapses": "10^9-10^10"},
            (
                CriterionSpec(
                    "temporal_memory",
                    "Temporal state memory",
                    paths=("src/research/temporal.py",),
                    tests=("tests/test_temporal.py",),
                ),
                CriterionSpec(
                    "episodic_memory",
                    "Bounded working and episodic memory foundation",
                    paths=("src/memory/store.py", "src/memory/layer.py"),
                    tests=(
                        "tests/test_memory_layer.py",
                        "tests/test_experience_engine.py",
                    ),
                ),
                CriterionSpec("semantic_memory", "Semantic memory", planned=True),
                CriterionSpec(
                    "world_model_prediction",
                    "Observation-only one-step world-model prediction foundation",
                    paths=(
                        "src/memory/world_model.py",
                        "src/experience/composition.py",
                        "src/research/cognition_experiments.py",
                    ),
                    tests=(
                        "tests/test_memory_layer.py",
                        "tests/test_cognition_operational_experiments.py",
                    ),
                ),
            ),
            (
                "src/research/temporal.py",
                "src/memory",
                "src/experience/composition.py",
                "src/research/cognition_experiments.py",
            ),
            (
                "tests/test_temporal.py",
                "tests/test_memory_layer.py",
                "tests/test_cognition_operational_experiments.py",
                "tests/test_experience_engine.py",
            ),
            (
                "research/experiments/EXP-EMP-20260910/016-memory_delayed_information_v1",
                "research/experiments/EXP-EMP-20260910/017-world_model_prediction_v1",
            ),
            ("RQ-MEM-002", "RQ-WM-001"),
            (
                "Bounded working/episodic memory is not semantic memory.",
                "The current predictor is observation-only and one-step, not a complete multi-step world model.",
                "The registered cognition campaign is an exploratory component screen with snn_involved=false and is not accepted EVID.",
                "Coupled cognition state is not yet in the canonical runtime checkpoint boundary; pause/resume identity is unproven.",
            ),
            (
                "Couple cognition state to the canonical snapshot/checkpoint boundary and prove pause/resume identity.",
                "Semantic memory remains unimplemented.",
                "Confirmatory SNN-involved memory/world-model evidence remains open.",
            ),
            (
                "Integrate coupled cognition persistence with runtime checkpoints.",
                "Add a provenance-bound semantic-memory and recall contract.",
                "Run confirmatory held-out SNN-involved controls with human evidence review.",
            ),
        ),
        StageSpec(
            7,
            "self_model_embodied_identity",
            "Selbstmodell und verkörperte Identität",
            "Selbstmodell",
            (
                "Eigenzustand und Umwelt unterscheiden",
                "Handlungsursachen und eigene Sensorik/Aktorik modellieren",
                "dauerhafter interner Zustand",
            ),
            {"neurons": "10^7-10^8+", "synapses": "not specified"},
            (
                CriterionSpec(
                    "versioned_technical_identity",
                    "Versioned technical identity and snapshot binding",
                    paths=("src/profiles/service.py",),
                    tests=("tests/test_profiles.py",),
                ),
                CriterionSpec(
                    "operational_behavior_state",
                    "Persistent operational behavior-state foundation",
                    paths=(
                        "src/profiles/behavior.py",
                        "src/experience/composition.py",
                        "src/research/cognition_experiments.py",
                    ),
                    tests=(
                        "tests/test_memory_layer.py",
                        "tests/test_cognition_operational_experiments.py",
                    ),
                ),
                CriterionSpec(
                    "self_model_backend", "Persistent self-model state", planned=True
                ),
                CriterionSpec(
                    "causal_action_attribution",
                    "Causal action attribution",
                    planned=True,
                ),
                CriterionSpec(
                    "sensor_actuator_confidence",
                    "Sensor and actuator inventory/confidence inputs",
                    paths=("src/embodiment/models.py", "src/embodiment/connections.py"),
                ),
                CriterionSpec(
                    "self_model_restore", "Self-model restore identity", planned=True
                ),
            ),
            (
                "src/profiles/service.py",
                "src/profiles/behavior.py",
                "src/experience/composition.py",
                "src/embodiment/models.py",
                "src/embodiment/connections.py",
            ),
            (
                "tests/test_profiles.py",
                "tests/test_memory_layer.py",
                "tests/test_cognition_operational_experiments.py",
            ),
            ("research/experiments/EXP-EMP-20260910/018-behavior_profile_control_v1",),
            ("RQ-PROFILE-001", "RQ6", "RQ7"),
            (
                "Versioned Wesen identity and an operational behavior profile are technical foundations, not a self-model.",
                "Causal self/other attribution and canonical coupled-state restore identity are not implemented.",
                "No consciousness inference is permitted from identity, profile or behavior-state persistence.",
            ),
            (
                "Connect Profile + State loading to the canonical runtime restore hook.",
                "Implement observer-only causal action attribution before recursive feedback.",
                "Keep autonomous identity mutation locked until bounded mutation, journal and rollback gates exist.",
            ),
            (
                "Prove coupled profile/state restore and pause/resume identity.",
                "Add controlled self-versus-external action-attribution experiments.",
            ),
        ),
        StageSpec(
            8,
            "autonomous_lifelong_development",
            "Autonome lebenslange Entwicklung",
            "Autonome Entwicklung",
            (
                "Continual Learning",
                "autonome Reorganisation",
                "wiederverwendbare Kompetenzen und angepasste Lernstrategien",
            ),
            {"neurons": "10^8-10^9", "synapses": "10^10-10^11"},
            (
                CriterionSpec("continual_learning", "Continual learning", planned=True),
                CriterionSpec(
                    "autonomous_reorganization",
                    "Autonomous reorganization",
                    planned=True,
                ),
                CriterionSpec(
                    "strategy_adaptation", "Learning-strategy adaptation", planned=True
                ),
            ),
            ("src/dashboard/static/development-frontier-placeholders.json",),
            ("tests/test_development_frontier_contract.py",),
            (
                "research/experiments/EXP-LIFE-0001-R1",
                "research/experiments/STAGES_8_10_EXPERIMENT_BACKLOG.md",
                "research/frontiers/STAGES_8_10_FOUNDATIONS.md",
            ),
            ("RQ-LIFE-001", "RQ-GEN-001", "RQ-STRUCT-001", "RQ-HOM-002", "RQ-REPL-001"),
            (
                "Stage-8 theory/design/experiment-planning foundations do not raise implementation maturity.",
                "EXP-LIFE-0001-R1 is an exploratory interference precursor, not evidence of autonomous lifelong learning.",
            ),
            ("E8-A through E8-G remain planned research work.",),
            (
                "Run continuously trained shared-network sequential retention without learned-state resets.",
                "Require rollback, resource-matched controls and independent replication before stronger claims.",
            ),
        ),
        StageSpec(
            9,
            "integrated_artificial_cognition",
            "Hochintegrierte künstliche Kognition",
            "Integrierte Kognition",
            (
                "Aufmerksamkeit, Motivation und Planung",
                "langfristige Erinnerung",
                "integrierte multimodale Verarbeitung und Konsolidierung",
            ),
            {"neurons": "10^8-10^9+", "synapses": "not specified"},
            (
                CriterionSpec(
                    "attention_and_planning", "Attention and planning", planned=True
                ),
                CriterionSpec(
                    "integrated_multimodal_processing",
                    "Integrated multimodal processing",
                    planned=True,
                ),
                CriterionSpec(
                    "consolidation", "Sleep or consolidation phases", planned=True
                ),
            ),
            ("src/dashboard/static/development-frontier-placeholders.json",),
            ("tests/test_development_frontier_contract.py",),
            (
                "research/experiments/STAGES_8_10_EXPERIMENT_BACKLOG.md",
                "research/frontiers/STAGES_8_10_FOUNDATIONS.md",
            ),
            (
                "RQ-CNS-103",
                "RQ-CNS-105",
                "RQ-CNS-110",
                "RQ-CNS-111",
                "RQ-CNS-112",
                "RQ-CNS-116",
                "RQ-MEM-002",
                "RQ-WM-001",
            ),
            (
                "Stage-9 material is a research architecture and placeholder contract, not an observed integrated cognitive capability.",
                "Attention, motivation and planning remain operational constructs rather than subjective-state claims.",
            ),
            ("E9-A through E9-G remain planned research work.",),
            (
                "Implement and ablate bounded attention, planning, multimodal integration and consolidation under matched budgets.",
                "Require independent replication for each claimed functional capability.",
            ),
        ),
        StageSpec(
            10,
            "consciousness_research",
            "Bewusstseinsforschung",
            "Forschungsfrontier",
            (
                "Ausschließlich Forschungsstufe",
                "operationale Kriterien, Interventionen und Reproduzierbarkeit",
                "Ethik- und Abbruchkriterien",
            ),
            {
                "neurons": "biological reference: ~86 billion",
                "synapses": "biological reference: ~10^14-10^15",
            },
            (
                CriterionSpec(
                    "operational_criteria",
                    "Predefined operational criteria",
                    planned=True,
                ),
                CriterionSpec(
                    "independent_replication", "Independent replication", planned=True
                ),
                CriterionSpec(
                    "ethics_and_stop_criteria", "Ethics and stop criteria", planned=True
                ),
            ),
            (
                "src/dashboard/static/development-frontier-placeholders.json",
                "src/research/cognition_governance.py",
            ),
            ("tests/test_development_frontier_contract.py",),
            (
                "research/experiments/STAGES_8_10_EXPERIMENT_BACKLOG.md",
                "research/frontiers/STAGES_8_10_FOUNDATIONS.md",
                "research/protocols/COGNITION_CONSCIOUSNESS.md",
                "research/ethics/AI_WELFARE_POLICY.md",
            ),
            (
                "RQ-CNS-101",
                "RQ-CNS-108",
                "RQ-CNS-109",
                "RQ-CNS-113",
                "RQ-CNS-114",
                "RQ-EPI-101",
                "RQ-EPI-102",
                "RQ-WEL-101",
                "RQ-WEL-102",
                "RQ-WEL-103",
            ),
            (
                "Stage 10 is a research-quality frontier and never automatically establishes consciousness, sentience or moral status.",
                "Theory, literature, ethics and experiment designs do not count as implementation or evidence for consciousness.",
            ),
            ("E10-A through E10-H remain planned research/governance work.",),
            (
                "Preregister contrasting operational predictions and causal interventions.",
                "Require ethics/stop governance and independent adversarial replication before interpretation.",
            ),
        ),
    )


def _safe_json(path: Path) -> dict[str, Any] | None:
    try:
        raw: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return cast(dict[str, Any], raw) if isinstance(raw, dict) else None


def _artifact_verified(path: Path) -> bool:
    data = _safe_json(path)
    if data is None:
        return False
    status = str(data.get("status", "")).lower()
    if status in {"verified", "passed", "green", "satisfied"}:
        return True
    proofs = data.get("proofs")
    if not isinstance(proofs, dict):
        return False
    typed_proofs = cast(dict[str, object], proofs)
    return bool(typed_proofs) and all(value is True for value in typed_proofs.values())


def _registry_count(registry: ResearchRegistry, kind: str, repo_root: Path) -> int:
    if kind == "questions":
        return len(registry.questions)
    if kind == "hypotheses":
        return len(registry.hypotheses)
    if kind == "claims":
        return len(registry.claims)
    if kind == "protocols":
        return len(list((repo_root / "research" / "registry").glob("*protocol*.yaml")))
    return 0


def _criterion_status(
    repo_root: Path,
    spec: CriterionSpec,
    registry: ResearchRegistry,
    baseline: Any,
) -> tuple[str, list[str]]:
    if spec.planned:
        return "planned", []
    evidence: list[str] = []
    paths_ok = all((repo_root / path).exists() for path in spec.paths)
    tests_ok = all((repo_root / path).is_file() for path in spec.tests)
    registry_ok = (
        spec.registry is None
        or _registry_count(registry, spec.registry, repo_root) >= spec.registry_minimum
    )
    verification_ok = bool(spec.verification) and all(
        _artifact_verified(repo_root / path) for path in spec.verification
    )
    if paths_ok:
        evidence.extend(spec.paths)
    if tests_ok:
        evidence.extend(spec.tests)
    if registry_ok and spec.registry:
        evidence.append(f"research/registry:{spec.registry}")
    if verification_ok:
        evidence.extend(spec.verification)
    if not paths_ok and not tests_ok and not registry_ok:
        return "missing", evidence
    baseline_ok = (
        baseline.available
        and not baseline.stale
        and baseline.failed == 0
        and baseline.collection_errors == 0
    )
    # all(()) is True, but no declared tests cannot verify a criterion.
    if verification_ok or (bool(spec.tests) and tests_ok and baseline_ok):
        return "verified", evidence
    if paths_ok and (spec.tests or spec.verification):
        return "experimental", evidence
    return "implemented", evidence


def _score(criteria: list[Criterion], points: dict[str, float]) -> float:
    if not criteria:
        return 0.0
    return round(sum(points[item["status"]] for item in criteria) / len(criteria), 3)


def _stage_status(
    implementation: float, verification: float, criteria: list[Criterion]
) -> str:
    if implementation >= 0.8 and verification >= 0.5:
        return "reached"
    if any(item["status"] in {"experimental", "verified"} for item in criteria):
        return "active"
    if any(item["status"] == "implemented" for item in criteria):
        return "implemented"
    return "planned"


def _snapshot_size(repo_root: Path) -> RuntimeSize | None:
    path = repo_root / "artifacts" / "latest.b5d"
    if not path.is_file():
        return None
    try:
        from src.storage.b5d import B5DReader

        with B5DReader(path) as reader:
            return {
                "neurons": int(reader.header.neuron_count),
                "synapses": int(reader.header.synapse_count),
                "source": "last_observed",
                "status": "unavailable",
                "snapshot_tick": int(reader.header.snapshot_tick),
            }
    except (OSError, ValueError, RuntimeError):
        return None


def _runtime_size(
    runtime: Mapping[str, object] | None, repo_root: Path
) -> tuple[RuntimeSize, RuntimeSize | None]:
    if runtime is not None:
        neurons = runtime.get("neurons")
        synapses = runtime.get("synapses")
        if (
            isinstance(neurons, int)
            and isinstance(synapses, int)
            and neurons >= 0
            and synapses >= 0
        ):
            return (
                {
                    "neurons": neurons,
                    "synapses": synapses,
                    "source": "runtime",
                    "status": "active",
                    "snapshot_tick": None,
                },
                None,
            )
    snapshot = _snapshot_size(repo_root)
    if snapshot is not None:
        unavailable: RuntimeSize = {**snapshot, "status": "unavailable"}
        return (unavailable, snapshot)
    return (
        {
            "neurons": None,
            "synapses": None,
            "source": "unavailable",
            "status": "unavailable",
            "snapshot_tick": None,
        },
        None,
    )


def _scientific_evidence_score(repo_root: Path, registry: ResearchRegistry) -> float:
    accepted = 0
    for claim in registry.claims.values():
        if claim.status.lower() in {"accepted", "validated", "evidenced", "promoted"}:
            accepted += 1
    evidence_dir = repo_root / "research" / "registry" / "evidence"
    evidence_records = (
        sum(1 for path in evidence_dir.glob("*.json") if path.is_file())
        if evidence_dir.is_dir()
        else 0
    )
    return round(
        min(1.0, (accepted + evidence_records) / max(1, len(registry.claims) * 2)), 3
    )


def build_development_timeline(
    repo_root: Path,
    *,
    runtime: Mapping[str, object] | None = None,
    gate_status: dict[str, object] | None = None,
    now: datetime | None = None,
) -> DevelopmentTimeline:
    """Build the current timeline from repository state without manual stage data."""
    registry = ResearchRegistry(repo_root / "research" / "registry").load_all()
    baseline = evaluate_test_baseline(repo_root)
    stages: list[TimelineStage] = []
    for stage_spec in _stage_specs():
        criteria: list[Criterion] = []
        for criterion_spec in stage_spec.criteria:
            status, evidence = _criterion_status(
                repo_root, criterion_spec, registry, baseline
            )
            if status not in _STATUS_VALUES:
                status = "missing"
            criteria.append(
                {
                    "id": criterion_spec.id,
                    "label": criterion_spec.label,
                    "status": status,
                    "source": "repository",
                    "evidence": evidence,
                }
            )
        implementation = _score(criteria, _IMPLEMENTATION_POINTS)
        verification = _score(criteria, _VERIFICATION_POINTS)
        research = _score(criteria, _RESEARCH_POINTS)
        stages.append(
            {
                "stage": stage_spec.stage,
                "id": stage_spec.id,
                "name": stage_spec.name,
                "short_label": stage_spec.short_label,
                "description": list(stage_spec.description),
                "scale": dict(stage_spec.scale),
                "criteria": criteria,
                "implementation_score": implementation,
                "verification_score": verification,
                "research_readiness_score": research,
                "status": _stage_status(implementation, verification, criteria),
                "relevant_modules": list(stage_spec.modules),
                "relevant_tests": list(stage_spec.tests),
                "relevant_experiments": list(stage_spec.experiments),
                "relevant_research_questions": list(stage_spec.research_questions),
                "known_limits": list(stage_spec.limits),
                "open_todos": list(stage_spec.todos),
                "next_technical_steps": list(stage_spec.next_steps),
            }
        )

    reached = [stage for stage in stages if stage["status"] == "reached"]
    stage_floor = max((stage["stage"] for stage in reached), default=0)
    next_stage = next((stage for stage in stages if stage["stage"] > stage_floor), None)
    progress = next_stage["implementation_score"] if next_stage else 1.0
    scientific_reached = [
        stage
        for stage in stages
        if stage["verification_score"] >= 0.5
        and stage["research_readiness_score"] >= 0.5
    ]
    scientific_floor = max((stage["stage"] for stage in scientific_reached), default=0)
    scientific_next = next(
        (stage for stage in stages if stage["stage"] > scientific_floor), None
    )
    scientific_progress = (
        scientific_next["research_readiness_score"] if scientific_next else 1.0
    )
    runtime_size, last_observed = _runtime_size(runtime, repo_root)
    evidence_score = _scientific_evidence_score(repo_root, registry)
    gate_ready = bool(
        gate_status
        and cast(dict[str, object], gate_status.get("release_readiness", {})).get(
            "ready"
        )
        is True
    )
    confidence = 0.8 if baseline.available and not baseline.stale else 0.55
    if runtime_size["source"] == "unavailable":
        confidence -= 0.1
    if gate_ready:
        confidence += 0.05
    current_stage = round(stage_floor + progress, 2)
    scientific_stage = round(scientific_floor + scientific_progress, 2)
    current_name = next_stage["name"] if next_stage else stages[-1]["name"]
    scientific_name = scientific_next["name"] if scientific_next else stages[-1]["name"]
    timestamp = (
        (now or datetime.now(timezone.utc))
        .astimezone(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )
    sources: list[dict[str, object]] = [
        {
            "path": "research/registry",
            "available": (repo_root / "research/registry").is_dir(),
            "kind": "structured_registry",
        },
        {
            "path": "research/registry/questions.yaml",
            "available": (repo_root / "research/registry/questions.yaml").is_file(),
            "kind": "research_questions",
        },
        {
            "path": "research/registry/hypotheses.yaml",
            "available": (repo_root / "research/registry/hypotheses.yaml").is_file(),
            "kind": "research_hypotheses",
        },
        {
            "path": "configs",
            "available": (repo_root / "configs").is_dir(),
            "kind": "structured_configuration",
        },
        {
            "path": "research/generated/verification",
            "available": (repo_root / "research/generated/verification").is_dir(),
            "kind": "verification_artifacts",
        },
        {
            "path": "gate_status",
            "available": gate_status is not None,
            "kind": "live_gate_projection",
        },
        {
            "path": "tests/test_baseline.json",
            "available": baseline.available,
            "kind": "test_baseline",
            "stale": baseline.stale,
        },
        {
            "path": "artifacts/latest.b5d",
            "available": (repo_root / "artifacts/latest.b5d").is_file(),
            "kind": "last_observed_snapshot",
        },
        {
            "path": "docs/08-roadmap/TODO.md",
            "available": (repo_root / "docs/08-roadmap/TODO.md").is_file(),
            "kind": "context_only",
        },
        {
            "path": "docs/08-roadmap/ROADMAP.md",
            "available": (repo_root / "docs/08-roadmap/ROADMAP.md").is_file(),
            "kind": "context_only",
        },
    ]
    return {
        "schema_version": 1,
        "current_stage": current_stage,
        "scientific_stage": scientific_stage,
        "stage_floor": stage_floor,
        "stage_next": next_stage["stage"] if next_stage else None,
        "progress_to_next": round(progress, 3),
        "scientific_progress_to_next": round(scientific_progress, 3),
        "current_label": f"{stages[stage_floor]['name']} -> {current_name}",
        "scientific_label": f"{stages[scientific_floor]['name']} -> {scientific_name}",
        "current_runtime": runtime_size,
        "last_observed_runtime": last_observed,
        "stages": stages,
        "engineering_score": round(
            sum(stage["implementation_score"] for stage in stages) / len(stages), 3
        ),
        "verification_score": round(
            sum(stage["verification_score"] for stage in stages) / len(stages), 3
        ),
        "scientific_evidence_score": evidence_score,
        "confidence": round(max(0.0, min(1.0, confidence)), 3),
        "sources": sources,
        "last_updated": timestamp,
        "scientific_note": "Engineering maturity and technical verification do not imply scientific evidence or consciousness.",
        "consciousness_claim": "unsupported",
    }


__all__ = ["build_development_timeline", "DevelopmentTimeline"]
