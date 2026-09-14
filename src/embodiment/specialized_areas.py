"""Stage-4 modality-specific neural-area engineering contract.

This module closes the *engineering* gap between the generic Neural Symbiosis
catalog and the modality-specific MSBA experiments.  It provides three typed
reference areas (audio, vision and digital), an aggregated Stage-4 topology
budget, deterministic bounded topology samples and experiment-only reference
probes.

The declared 100k-neuron / 10M-synapse lower-bound topology is deliberately an
aggregated topology contract.  It does not materialize ten million edges and it
is not evidence that a 100k-neuron multimodal SNN has been executed.  Productive
peripheral activation remains locked and no function in this module imports or
mutates ``src.core``.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Sequence

from .models import JSONValue
from .msba import (
    Modality,
    ResourcePressure,
    SymbolFrame,
    phase_weighted_stdp,
    visual_growth_probability,
)
from .peripheral_adapters import (
    AdapterDeclaration,
    ExperimentAdapterFactory,
    declaration_artifact_hash,
)

STAGE4_MIN_NEURONS = 100_000
STAGE4_MIN_SYNAPSES = 10_000_000
DEFAULT_EDGE_SAMPLE_SIZE = 12

LATEST_MSBA_DATA = (
    "research/experiments/EXP-BATCH-20260914074039-90",
    "research/experiments/EXP-BATCH-20260914074039-91",
    "research/experiments/EXP-BATCH-20260914074039-92",
    "research/experiments/EXP-BATCH-20260914074039-93",
    "research/experiments/EXP-BATCH-20260914074039-94",
)


@dataclass(frozen=True, slots=True)
class SpecializedAreaSpec:
    """One bounded modality-specific processing-area declaration."""

    area_id: str
    name: str
    modality: Modality
    neuron_budget: int
    mean_fanout: int
    pathway: str
    adapter_transform: str
    plasticity_rule: str
    coordinate_features: tuple[str, ...]
    throttles: tuple[str, ...]
    exact_payload_outside_snn: bool = False

    def __post_init__(self) -> None:
        if not self.area_id.strip() or not self.name.strip():
            raise ValueError("area_id and name must not be empty")
        if self.neuron_budget <= 0 or self.mean_fanout <= 0:
            raise ValueError("neuron_budget and mean_fanout must be positive")
        if not self.pathway.strip() or not self.plasticity_rule.strip():
            raise ValueError("pathway and plasticity_rule must not be empty")

    @property
    def synapse_budget(self) -> int:
        """Return the aggregated directed-edge budget for this area."""

        return self.neuron_budget * self.mean_fanout

    def to_json(self) -> dict[str, JSONValue]:
        return {
            "area_id": self.area_id,
            "name": self.name,
            "modality": self.modality.value,
            "neuron_budget": self.neuron_budget,
            "mean_fanout": self.mean_fanout,
            "synapse_budget": self.synapse_budget,
            "pathway": self.pathway,
            "adapter_transform": self.adapter_transform,
            "plasticity_rule": self.plasticity_rule,
            "coordinate_features": list(self.coordinate_features),
            "throttles": list(self.throttles),
            "exact_payload_outside_snn": self.exact_payload_outside_snn,
            "activation_scope": "experiment_only",
        }


def default_specialized_areas() -> tuple[SpecializedAreaSpec, ...]:
    """Return the canonical Stage-4 audio, vision and digital area contracts."""

    return (
        SpecializedAreaSpec(
            area_id="stage4.audio.temporal",
            name="Auditory Temporal Area",
            modality=Modality.AUDIO,
            neuron_budget=25_000,
            mean_fanout=96,
            pathway="temporal_coherence",
            adapter_transform="threshold_features",
            plasticity_rule="phase_weighted_t_stdp_candidate",
            coordinate_features=(
                "band",
                "phase_or_envelope",
                "channel",
                "lag",
                "feature",
            ),
            throttles=("band_count", "update_rate", "delay_taps"),
        ),
        SpecializedAreaSpec(
            area_id="stage4.vision.spatial",
            name="Visual Spatial Area",
            modality=Modality.VISION,
            neuron_budget=50_000,
            mean_fanout=128,
            pathway="spatial_multiplex",
            adapter_transform="threshold_features",
            plasticity_rule="s_stdp_plus_structural_growth_candidate",
            coordinate_features=("x", "y", "feature", "scale", "frame"),
            throttles=("fps", "resolution", "roi", "feature_channels"),
        ),
        SpecializedAreaSpec(
            area_id="stage4.digital.symbolic",
            name="Digital Symbolic Area",
            modality=Modality.DIGITAL,
            neuron_budget=25_000,
            mean_fanout=48,
            pathway="quantized_high_fidelity",
            adapter_transform="identity",
            plasticity_rule="population_meta_gating_candidate",
            coordinate_features=(
                "symbol",
                "sequence",
                "source",
                "context",
                "route",
            ),
            throttles=("symbol_rate", "batching", "admission"),
            exact_payload_outside_snn=True,
        ),
    )


class SpecializedAreaNetwork:
    """Bounded experiment-only runtime facade for the Stage-4 area contracts."""

    def __init__(self, areas: Sequence[SpecializedAreaSpec] | None = None) -> None:
        configured = tuple(areas or default_specialized_areas())
        by_modality = {item.modality: item for item in configured}
        required = {Modality.AUDIO, Modality.VISION, Modality.DIGITAL}
        if set(by_modality) != required:
            raise ValueError(
                "Stage-4 network requires exactly audio, vision and digital"
            )
        self._areas = configured
        self._by_modality = by_modality

    @property
    def total_neurons(self) -> int:
        return sum(item.neuron_budget for item in self._areas)

    @property
    def total_synapses(self) -> int:
        return sum(item.synapse_budget for item in self._areas)

    def topology_summary(self) -> dict[str, JSONValue]:
        """Publish the scale budget without materializing its complete edge set."""

        return {
            "representation": "aggregated_topology_contract",
            "total_neuron_budget": self.total_neurons,
            "total_synapse_budget": self.total_synapses,
            "stage4_min_neurons": STAGE4_MIN_NEURONS,
            "stage4_min_synapses": STAGE4_MIN_SYNAPSES,
            "lower_bound_satisfied": (
                self.total_neurons >= STAGE4_MIN_NEURONS
                and self.total_synapses >= STAGE4_MIN_SYNAPSES
            ),
            "edges_materialized": False,
            "dynamic_scale_execution_verified": False,
            "productive_activation_enabled": False,
        }

    def edge_sample(
        self, limit: int = DEFAULT_EDGE_SAMPLE_SIZE
    ) -> list[dict[str, JSONValue]]:
        """Return a deterministic bounded sample of the declared topology."""

        if limit <= 0:
            raise ValueError("limit must be positive")
        rows: list[dict[str, JSONValue]] = []
        area_index = 0
        while len(rows) < limit:
            area = self._areas[area_index % len(self._areas)]
            ordinal = area_index // len(self._areas)
            digest = hashlib.sha256(
                f"{area.area_id}:{ordinal}".encode("utf-8")
            ).digest()
            source = int.from_bytes(digest[:8], "big") % area.neuron_budget
            offset = 1 + int.from_bytes(digest[8:16], "big") % max(
                1, area.neuron_budget - 1
            )
            target = (source + offset) % area.neuron_budget
            rows.append(
                {
                    "area_id": area.area_id,
                    "modality": area.modality.value,
                    "source_local_index": source,
                    "target_local_index": target,
                    "plasticity_rule": area.plasticity_rule,
                }
            )
            area_index += 1
        return rows

    def process_reference(
        self, modality: Modality | str, payload: JSONValue, *, tick: int = 1
    ) -> dict[str, JSONValue]:
        """Run one deterministic reference probe through a modality adapter."""

        selected = modality if isinstance(modality, Modality) else Modality(modality)
        area = self._by_modality[selected]
        declaration = self._declaration(area)
        adapter = ExperimentAdapterFactory.create(
            declaration, experiment_mode=True, production_activation=False
        )
        if selected is Modality.DIGITAL:
            return self._digital_probe(area, declaration, adapter, payload, tick)
        values = self._numeric_payload(payload)
        processed = adapter.process(list(values), tick)
        if not isinstance(processed, dict):
            raise RuntimeError("numeric specialized adapter returned invalid payload")
        features = processed.get("features")
        if not isinstance(features, list):
            raise RuntimeError("numeric specialized adapter omitted features")
        feature_values = list(self._numeric_payload(features))
        if selected is Modality.AUDIO:
            phase = math.atan2(
                values[1] if len(values) > 1 else 0.0,
                values[0] if values else 1.0,
            )
            candidate = phase_weighted_stdp(0.01, phase)
            candidate_key = "candidate_weight_delta"
        else:
            information_value = sum(abs(value) for value in values) / max(
                len(values), 1
            )
            candidate = visual_growth_probability(
                information_value,
                distance_5d=1.0,
                sigma=2.0,
                pressure=ResourcePressure(),
            )
            candidate_key = "candidate_growth_probability"
        result: dict[str, JSONValue] = {
            "area_id": area.area_id,
            "modality": selected.value,
            "tick": tick,
            "pathway": area.pathway,
            "adapter_transform": area.adapter_transform,
            "plasticity_rule": area.plasticity_rule,
            "encoded_features": [int(value) for value in feature_values],
            candidate_key: candidate,
            "adapter_provenance": declaration.provenance(),
            "canonical_core_mutated": False,
            "productive_activation_enabled": False,
        }
        return result

    @staticmethod
    def _numeric_payload(payload: JSONValue) -> tuple[float, ...]:
        if not isinstance(payload, list) or not payload:
            raise ValueError("audio/vision reference payload must be a non-empty list")
        values: list[float] = []
        for item in payload:
            if isinstance(item, bool) or not isinstance(item, (int, float)):
                raise ValueError("audio/vision reference payload must be numeric")
            values.append(float(item))
        return tuple(values)

    @staticmethod
    def _declaration(area: SpecializedAreaSpec) -> AdapterDeclaration:
        artifact = {
            "stage": 4,
            "area_id": area.area_id,
            "modality": area.modality.value,
            "pathway": area.pathway,
            "plasticity_rule": area.plasticity_rule,
        }
        return AdapterDeclaration(
            area_id=area.area_id,
            adapter_class="DeterministicPeripheralAdapter",
            framework="python-reference",
            model=f"stage4-{area.modality.value}-area-reference",
            version="1.0.0",
            artifact_sha256=declaration_artifact_hash(artifact),
            endpoint_identity=f"experiment://stage4/{area.modality.value}",
            modality=area.modality.value,
            transform=area.adapter_transform,
        )

    @staticmethod
    def _digital_probe(
        area: SpecializedAreaSpec,
        declaration: AdapterDeclaration,
        adapter: object,
        payload: JSONValue,
        tick: int,
    ) -> dict[str, JSONValue]:
        if not isinstance(payload, str):
            raise ValueError("digital reference payload must be a string")
        raw = payload.encode("utf-8")
        frame = SymbolFrame(raw, sequence=tick, provenance=area.area_id)
        processed = adapter.process(payload, tick)  # type: ignore[attr-defined]
        if not isinstance(processed, str):
            raise RuntimeError("digital specialized adapter returned invalid payload")
        output = processed.encode("utf-8")
        output_checksum = hashlib.sha256(output).hexdigest()
        return {
            "area_id": area.area_id,
            "modality": area.modality.value,
            "tick": tick,
            "pathway": area.pathway,
            "adapter_transform": area.adapter_transform,
            "plasticity_rule": area.plasticity_rule,
            "population_code": list(frame.deterministic_population()),
            "input_sha256": frame.checksum,
            "output_sha256": output_checksum,
            "exact_payload_equal": output == raw,
            "exact_integrity_pass": output == raw and output_checksum == frame.checksum,
            "adapter_provenance": declaration.provenance(),
            "canonical_core_mutated": False,
            "productive_activation_enabled": False,
        }


def reference_probe_suite() -> dict[str, JSONValue]:
    """Return deterministic end-to-end reference probes for all three pathways."""

    network = SpecializedAreaNetwork()
    probes: dict[str, JSONValue] = {
        "audio": network.process_reference(
            Modality.AUDIO, [0.8, -0.2, 0.35, -0.9], tick=17
        ),
        "vision": network.process_reference(
            Modality.VISION, [0.1, 0.7, -0.4, 0.9, -0.2, 0.5], tick=17
        ),
        "digital": network.process_reference(
            Modality.DIGITAL, "MHRN-STAGE4-DIGITAL-INTEGRITY", tick=17
        ),
    }
    canonical = json.dumps(probes, sort_keys=True, separators=(",", ":"))
    return {
        "probes": probes,
        "probe_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    }


def specialized_area_contract() -> dict[str, JSONValue]:
    """Publish the complete Stage-4 engineering contract for API/UI consumers."""

    network = SpecializedAreaNetwork()
    return {
        "schema_version": 1,
        "stage": 4,
        "id": "specialized_neural_areas",
        "name": "Spezialisierte neuronale Areale",
        "status": "implemented_experimental",
        "areas": [item.to_json() for item in default_specialized_areas()],
        "topology": network.topology_summary(),
        "topology_edge_sample": [item for item in network.edge_sample()],
        "reference_probes": reference_probe_suite(),
        "research_data": list(LATEST_MSBA_DATA),
        "scientific_boundary": {
            "scope": "engineering_verification",
            "aggregated_topology_is_not_dynamic_execution": True,
            "experiment_only_adapters": True,
            "productive_activation_enabled": False,
            "canonical_core_mutation": False,
            "automatic_evidence_promotion": False,
            "human_review_required_for_evid": True,
        },
    }


__all__ = [
    "DEFAULT_EDGE_SAMPLE_SIZE",
    "LATEST_MSBA_DATA",
    "STAGE4_MIN_NEURONS",
    "STAGE4_MIN_SYNAPSES",
    "SpecializedAreaNetwork",
    "SpecializedAreaSpec",
    "default_specialized_areas",
    "reference_probe_suite",
    "specialized_area_contract",
]
