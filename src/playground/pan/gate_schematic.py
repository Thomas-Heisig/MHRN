"""Generated gate schematics for the non-canonical PAN Playground layer."""

from __future__ import annotations

from dataclasses import dataclass

from ..models import PlaygroundConfig


@dataclass(frozen=True, slots=True)
class GateSpec:
    """Descriptive executable gate primitive derived from Playground settings."""

    name: str
    kind: str
    inputs: tuple[str, ...]
    threshold: float | None = None
    duration_ms: float | None = None
    semantics: str = ""

    def descriptor(self) -> dict[str, object]:
        return {
            "name": self.name,
            "kind": self.kind,
            "inputs": list(self.inputs),
            "threshold": self.threshold,
            "duration_ms": self.duration_ms,
            "semantics": self.semantics,
        }


class GateSchematic:
    """Bounded gate collection with simple threshold evaluation."""

    def __init__(self, gates: tuple[GateSpec, ...]) -> None:
        self.gates = gates
        self._by_name = {gate.name: gate for gate in gates}

    def threshold_triggered(self, name: str, value: float) -> bool:
        """Evaluate the threshold sense of one named gate."""

        gate = self._by_name[name]
        if gate.threshold is None:
            raise ValueError(f"{name} has no scalar threshold")
        if gate.kind.startswith("NAND"):
            return value <= gate.threshold
        return value >= gate.threshold

    def descriptor(self) -> dict[str, object]:
        return {
            "classification": "PLAYGROUND_GATE_SCHEMATIC",
            "scientific_evidence": False,
            "evidence_eligible": False,
            "generation": "SETTINGS_DERIVED",
            "gate_count": len(self.gates),
            "gates": [gate.descriptor() for gate in self.gates],
            "hardware_execution": "PYTHON_REFERENCE_ONLY",
            "cuda_kernel_status": "NOT_WIRED_IN_REFERENCE_RUNTIME",
        }


def settings_to_gates(config: PlaygroundConfig) -> GateSchematic:
    """Translate validated Playground/PAN settings into gate primitives."""

    gates = (
        GateSpec(
            "apoptosis",
            "NAND_THRESHOLD",
            ("pan_health", "theta_dead"),
            threshold=config.pan_apoptosis_threshold,
            semantics="health_at_or_below_threshold_marks_slot_inactive",
        ),
        GateSpec(
            "aging",
            "AND_THRESHOLD",
            ("pan_health", "theta_aging"),
            threshold=config.pan_aging_threshold,
            semantics="health_at_or_above_threshold_permits_growth",
        ),
        GateSpec(
            "feedback",
            "XOR_AND_GAIN",
            ("population_hyperstate", "feedback_projection"),
            threshold=config.pan_feedback_gain,
            semantics="bounded_closed_loop_gain_not_boolean_hardware",
        ),
        GateSpec(
            "geometry_sigma",
            "AND_GAUSSIAN",
            ("distance", "sigma"),
            threshold=config.geometry_sigma,
            semantics="geometric_probability_scale",
        ),
        GateSpec(
            "geometry_probability",
            "AND_PROBABILITY",
            ("candidate", "p0"),
            threshold=config.geometry_p0,
            semantics="connection_probability_parameter",
        ),
        GateSpec(
            "connection_radius",
            "AND_THRESHOLD",
            ("distance", "radius"),
            threshold=config.radius,
            semantics="connection_candidate_distance_bound",
        ),
        GateSpec(
            "conduction_velocity",
            "AND_DELAY",
            ("xyz_distance", "velocity"),
            threshold=config.geometry_delay_velocity,
            semantics="xyz_only_delay_parameter",
        ),
        GateSpec(
            "base_clock",
            "TIMER",
            ("clock",),
            duration_ms=1000.0 / config.clock_base_hz,
            semantics="logical_base_period",
        ),
        GateSpec(
            "continuous_step",
            "SUB_TICK",
            ("clock",),
            duration_ms=config.dt_ms,
            semantics="reference_runtime_continuous_step",
        ),
        GateSpec(
            "event_batch",
            "EVENT_QUEUE",
            ("event_queue",),
            duration_ms=config.clock_event_batch_ms,
            semantics="dual_scheduler_sync_barrier",
        ),
        GateSpec(
            "neurogenesis",
            "AND_THRESHOLD",
            ("activity", "healthy_slot"),
            threshold=config.growth_activity_threshold,
            semantics="pool_backed_reactivation_of_apoptotic_slot",
        ),
        GateSpec(
            "synaptogenesis",
            "AND_THRESHOLD",
            ("coactivation",),
            threshold=float(config.growth_coactivation_threshold),
            semantics="bounded_new_edge_trigger",
        ),
        GateSpec(
            "path_formation",
            "AND_THRESHOLD",
            ("information_proxy",),
            threshold=config.growth_information_threshold,
            semantics="bounded_short_path_trigger",
        ),
        GateSpec(
            "pruning",
            "NAND_THRESHOLD",
            ("weight",),
            threshold=config.growth_prune_threshold,
            semantics="weak_edge_pruning_trigger",
        ),
    )
    return GateSchematic(gates)
