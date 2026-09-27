"""Core data contracts for the non-canonical MHRN playground."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping, TypeAlias

Coordinate: TypeAlias = tuple[float, ...]
Edge: TypeAlias = tuple[int, int]

_NAME_RE = re.compile(r"[^A-Za-z0-9_.-]+")


@dataclass(frozen=True, slots=True)
class Topology:
    """Neutral topology returned by every playground topology generator."""

    name: str
    dimensions: int
    edges: tuple[Edge, ...]
    coordinates: tuple[Coordinate, ...]
    metadata: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class PlaygroundConfig:
    """Validated bounded configuration for one exploratory playground session."""

    name: str = "playground_session"
    neuron_model: str = "izhikevich_rs"
    synapse_model: str = "static"
    plasticity_rule: str = "none"
    topology: str = "mhrn_5d"
    stimulus: str = "deterministic"
    readout: str = "population_vector"
    n_neurons: int = 128
    edge_budget: int = 512
    ticks: int = 256
    seed: int = 12345
    dimensions: int = 5
    dt_ms: float = 1.0
    weight: float = 8.0
    delay_ticks: int = 1
    stimulus_current: float = 12.0
    stimulus_rate_hz: float = 20.0
    radius: float = 0.35
    k_neighbors: int = 8
    rewiring_probability: float = 0.15
    modules: int = 4
    ensemble_runs: int = 1
    persist: bool = False
    pan_enabled: bool = False
    pan_dimensions: int = 5
    pan_closed_loop: bool = True
    pan_feedback_gain: float = 0.05
    pan_health_decay: float = 0.001
    pan_apoptosis_threshold: float = 0.1
    pan_aging_threshold: float = 0.3
    pan_bias_current: float = 15.0
    clock_mode: str = "continuous"
    clock_base_hz: float = 100.0
    clock_event_batch_ms: float = 10.0
    execution_mode: str = "TICK_ONLY"
    execution_initial_mode: str = "EVENT_ONLY"
    execution_theta_high: float = 0.30
    execution_theta_low: float = 0.05
    execution_hysteresis: float = 0.02
    execution_min_dwell: int = 100
    execution_activity_window: int = 100
    execution_transition_mode: str = "clean"
    execution_sync_on_switch: bool = True
    execution_log_transitions: bool = True
    execution_log_state_hash: bool = True
    growth_enabled: bool = False
    growth_neurogenesis: bool = True
    growth_synaptogenesis: bool = True
    growth_path_formation: bool = True
    growth_pruning: bool = True
    growth_activity_threshold: float = 0.25
    growth_coactivation_threshold: int = 2
    growth_information_threshold: float = 0.25
    growth_prune_threshold: float = 0.05
    growth_max_synapses_per_neuron: int = 128
    growth_max_new_synapses_per_barrier: int = 8
    cuda_budget_mb: int = 2048
    offload_enabled: bool = False
    offload_snapshot_interval: int = 1000
    hardware_profile_name: str = "reference_cpu"
    thalamic_gating_enabled: bool = False
    thalamic_relay_threshold: float = 0.0
    thalamic_attention_gain: float = 1.15
    thalamic_inhibition_gain: float = 0.35
    cortical_layers_enabled: bool = False
    cortical_layer_count: int = 6
    cortical_plasticity: bool = True
    cortical_learning_rate: float = 0.01
    behavior_learning_enabled: bool = False
    behavior_action_count: int = 4
    behavior_learning_rate: float = 0.05
    behavior_epsilon: float = 0.05
    behavior_target_action: int = 0
    behavior_target_mode: str = "cycle"
    behavior_min_activity: float = 0.01
    behavior_episode_ticks: int = 16
    behavior_bias_current: float = 3.0
    geometry_lambda_a: float = 0.5
    geometry_lambda_b: float = 0.5
    geometry_sigma: float = 0.1
    geometry_p0: float = 0.3
    geometry_mode: str = "shortcut_union"
    geometry_delay_velocity: float = 0.25
    neural_io_enabled: bool = False
    neural_io_input_channels: int = 16
    neural_io_output_channels: int = 16
    neural_io_input_codec: str = "population_latency_v1"
    neural_io_output_decoder: str = "population_rate_v1"
    neural_io_input_payload: object = 0.5
    neural_io_window_ticks: int = 16
    neural_io_input_current: float = 25.0
    neural_io_input_role: str = "GATEWAY_AFFERENT"
    neural_io_output_role: str = "GATEWAY_EFFERENT"
    neural_io_phase: str = "QUERY"
    neural_io_correlation_id: str = ""
    neural_io_modality: str = "digital"
    neural_io_source_id: str = "playground.input"

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> "PlaygroundConfig":
        """Build a config from untrusted API/CLI input and validate all bounds."""

        defaults = cls()

        def text(name: str, default: str) -> str:
            value = payload.get(name, default)
            if not isinstance(value, str):
                raise ValueError(f"{name} must be a string")
            value = value.strip()
            if not value:
                raise ValueError(f"{name} must not be empty")
            return value

        def integer(name: str, default: int) -> int:
            value = payload.get(name, default)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be an integer")
            converted = int(value)
            if float(value) != float(converted):
                raise ValueError(f"{name} must be an integer")
            return converted

        def number(name: str, default: float) -> float:
            value = payload.get(name, default)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric")
            return float(value)

        raw_name = text("name", defaults.name)
        safe_name = _NAME_RE.sub("_", raw_name).strip("._-")[:80] or defaults.name
        config = cls(
            name=safe_name,
            neuron_model=text("neuron_model", defaults.neuron_model),
            synapse_model=text("synapse_model", defaults.synapse_model),
            plasticity_rule=text("plasticity_rule", defaults.plasticity_rule),
            topology=text("topology", defaults.topology),
            stimulus=text("stimulus", defaults.stimulus),
            readout=text("readout", defaults.readout),
            n_neurons=integer("n_neurons", defaults.n_neurons),
            edge_budget=integer("edge_budget", defaults.edge_budget),
            ticks=integer("ticks", defaults.ticks),
            seed=integer("seed", defaults.seed),
            dimensions=integer("dimensions", defaults.dimensions),
            dt_ms=number("dt_ms", defaults.dt_ms),
            weight=number("weight", defaults.weight),
            delay_ticks=integer("delay_ticks", defaults.delay_ticks),
            stimulus_current=number("stimulus_current", defaults.stimulus_current),
            stimulus_rate_hz=number("stimulus_rate_hz", defaults.stimulus_rate_hz),
            radius=number("radius", defaults.radius),
            k_neighbors=integer("k_neighbors", defaults.k_neighbors),
            rewiring_probability=number(
                "rewiring_probability", defaults.rewiring_probability
            ),
            modules=integer("modules", defaults.modules),
            ensemble_runs=integer("ensemble_runs", defaults.ensemble_runs),
            persist=bool(payload.get("persist", defaults.persist)),
            pan_enabled=bool(payload.get("pan_enabled", defaults.pan_enabled)),
            pan_dimensions=integer("pan_dimensions", defaults.pan_dimensions),
            pan_closed_loop=bool(
                payload.get("pan_closed_loop", defaults.pan_closed_loop)
            ),
            pan_feedback_gain=number(
                "pan_feedback_gain", defaults.pan_feedback_gain
            ),
            pan_health_decay=number(
                "pan_health_decay", defaults.pan_health_decay
            ),
            pan_apoptosis_threshold=number(
                "pan_apoptosis_threshold", defaults.pan_apoptosis_threshold
            ),
            pan_aging_threshold=number(
                "pan_aging_threshold", defaults.pan_aging_threshold
            ),
            pan_bias_current=number("pan_bias_current", defaults.pan_bias_current),
            clock_mode=text("clock_mode", defaults.clock_mode),
            clock_base_hz=number("clock_base_hz", defaults.clock_base_hz),
            clock_event_batch_ms=number(
                "clock_event_batch_ms", defaults.clock_event_batch_ms
            ),
            execution_mode=text("execution_mode", defaults.execution_mode).upper(),
            execution_initial_mode=text(
                "execution_initial_mode", defaults.execution_initial_mode
            ).upper(),
            execution_theta_high=number(
                "execution_theta_high", defaults.execution_theta_high
            ),
            execution_theta_low=number(
                "execution_theta_low", defaults.execution_theta_low
            ),
            execution_hysteresis=number(
                "execution_hysteresis", defaults.execution_hysteresis
            ),
            execution_min_dwell=integer(
                "execution_min_dwell", defaults.execution_min_dwell
            ),
            execution_activity_window=integer(
                "execution_activity_window", defaults.execution_activity_window
            ),
            execution_transition_mode=text(
                "execution_transition_mode", defaults.execution_transition_mode
            ).lower(),
            execution_sync_on_switch=bool(
                payload.get("execution_sync_on_switch", defaults.execution_sync_on_switch)
            ),
            execution_log_transitions=bool(
                payload.get("execution_log_transitions", defaults.execution_log_transitions)
            ),
            execution_log_state_hash=bool(
                payload.get("execution_log_state_hash", defaults.execution_log_state_hash)
            ),
            growth_enabled=bool(
                payload.get("growth_enabled", defaults.growth_enabled)
            ),
            growth_neurogenesis=bool(
                payload.get("growth_neurogenesis", defaults.growth_neurogenesis)
            ),
            growth_synaptogenesis=bool(
                payload.get("growth_synaptogenesis", defaults.growth_synaptogenesis)
            ),
            growth_path_formation=bool(
                payload.get("growth_path_formation", defaults.growth_path_formation)
            ),
            growth_pruning=bool(
                payload.get("growth_pruning", defaults.growth_pruning)
            ),
            growth_activity_threshold=number(
                "growth_activity_threshold", defaults.growth_activity_threshold
            ),
            growth_coactivation_threshold=integer(
                "growth_coactivation_threshold", defaults.growth_coactivation_threshold
            ),
            growth_information_threshold=number(
                "growth_information_threshold", defaults.growth_information_threshold
            ),
            growth_prune_threshold=number(
                "growth_prune_threshold", defaults.growth_prune_threshold
            ),
            growth_max_synapses_per_neuron=integer(
                "growth_max_synapses_per_neuron",
                defaults.growth_max_synapses_per_neuron,
            ),
            growth_max_new_synapses_per_barrier=integer(
                "growth_max_new_synapses_per_barrier",
                defaults.growth_max_new_synapses_per_barrier,
            ),
            cuda_budget_mb=integer("cuda_budget_mb", defaults.cuda_budget_mb),
            offload_enabled=bool(
                payload.get("offload_enabled", defaults.offload_enabled)
            ),
            offload_snapshot_interval=integer(
                "offload_snapshot_interval", defaults.offload_snapshot_interval
            ),
            hardware_profile_name=text(
                "hardware_profile_name", defaults.hardware_profile_name
            ),
            thalamic_gating_enabled=bool(
                payload.get("thalamic_gating_enabled", defaults.thalamic_gating_enabled)
            ),
            thalamic_relay_threshold=number(
                "thalamic_relay_threshold", defaults.thalamic_relay_threshold
            ),
            thalamic_attention_gain=number(
                "thalamic_attention_gain", defaults.thalamic_attention_gain
            ),
            thalamic_inhibition_gain=number(
                "thalamic_inhibition_gain", defaults.thalamic_inhibition_gain
            ),
            cortical_layers_enabled=bool(
                payload.get("cortical_layers_enabled", defaults.cortical_layers_enabled)
            ),
            cortical_layer_count=integer(
                "cortical_layer_count", defaults.cortical_layer_count
            ),
            cortical_plasticity=bool(
                payload.get("cortical_plasticity", defaults.cortical_plasticity)
            ),
            cortical_learning_rate=number(
                "cortical_learning_rate", defaults.cortical_learning_rate
            ),
            behavior_learning_enabled=bool(
                payload.get("behavior_learning_enabled", defaults.behavior_learning_enabled)
            ),
            behavior_action_count=integer(
                "behavior_action_count", defaults.behavior_action_count
            ),
            behavior_learning_rate=number(
                "behavior_learning_rate", defaults.behavior_learning_rate
            ),
            behavior_epsilon=number(
                "behavior_epsilon", defaults.behavior_epsilon
            ),
            behavior_target_action=integer(
                "behavior_target_action", defaults.behavior_target_action
            ),
            behavior_target_mode=text(
                "behavior_target_mode", defaults.behavior_target_mode
            ).lower(),
            behavior_min_activity=number(
                "behavior_min_activity", defaults.behavior_min_activity
            ),
            behavior_episode_ticks=integer(
                "behavior_episode_ticks", defaults.behavior_episode_ticks
            ),
            behavior_bias_current=number(
                "behavior_bias_current", defaults.behavior_bias_current
            ),
            geometry_lambda_a=number(
                "geometry_lambda_a", defaults.geometry_lambda_a
            ),
            geometry_lambda_b=number(
                "geometry_lambda_b", defaults.geometry_lambda_b
            ),
            geometry_sigma=number("geometry_sigma", defaults.geometry_sigma),
            geometry_p0=number("geometry_p0", defaults.geometry_p0),
            geometry_mode=text("geometry_mode", defaults.geometry_mode),
            geometry_delay_velocity=number(
                "geometry_delay_velocity", defaults.geometry_delay_velocity
            ),
            neural_io_enabled=bool(
                payload.get("neural_io_enabled", defaults.neural_io_enabled)
            ),
            neural_io_input_channels=integer(
                "neural_io_input_channels", defaults.neural_io_input_channels
            ),
            neural_io_output_channels=integer(
                "neural_io_output_channels", defaults.neural_io_output_channels
            ),
            neural_io_input_codec=text(
                "neural_io_input_codec", defaults.neural_io_input_codec
            ),
            neural_io_output_decoder=text(
                "neural_io_output_decoder", defaults.neural_io_output_decoder
            ),
            neural_io_input_payload=payload.get(
                "neural_io_input_payload", defaults.neural_io_input_payload
            ),
            neural_io_window_ticks=integer(
                "neural_io_window_ticks", defaults.neural_io_window_ticks
            ),
            neural_io_input_current=number(
                "neural_io_input_current", defaults.neural_io_input_current
            ),
            neural_io_input_role=text(
                "neural_io_input_role", defaults.neural_io_input_role
            ),
            neural_io_output_role=text(
                "neural_io_output_role", defaults.neural_io_output_role
            ),
            neural_io_phase=text(
                "neural_io_phase", defaults.neural_io_phase
            ),
            neural_io_correlation_id=text(
                "neural_io_correlation_id",
                defaults.neural_io_correlation_id or "auto",
            ),
            neural_io_modality=text(
                "neural_io_modality", defaults.neural_io_modality
            ),
            neural_io_source_id=text(
                "neural_io_source_id", defaults.neural_io_source_id
            ),
        )
        config.validate()
        return config

    def validate(self) -> None:
        if not 2 <= self.n_neurons <= 1024:
            raise ValueError("n_neurons must be between 2 and 1024")
        max_edges = min(20_000, self.n_neurons * (self.n_neurons - 1))
        if not self.n_neurons <= self.edge_budget <= max_edges:
            raise ValueError(f"edge_budget must be between n_neurons and {max_edges}")
        if not 1 <= self.ticks <= 2048:
            raise ValueError("ticks must be between 1 and 2048")
        if not 1 <= self.dimensions <= 32:
            raise ValueError("dimensions must be between 1 and 32")
        if not 0.05 <= self.dt_ms <= 5.0:
            raise ValueError("dt_ms must be between 0.05 and 5.0")
        if not 0.0 <= self.weight <= 100.0:
            raise ValueError("weight must be between 0 and 100")
        if not 1 <= self.delay_ticks <= 64:
            raise ValueError("delay_ticks must be between 1 and 64")
        if not 0.0 <= self.stimulus_current <= 500.0:
            raise ValueError("stimulus_current must be between 0 and 500")
        if not 0.0 <= self.stimulus_rate_hz <= 1000.0:
            raise ValueError("stimulus_rate_hz must be between 0 and 1000")
        if not 0.001 <= self.radius <= 2.0:
            raise ValueError("radius must be between 0.001 and 2.0")
        if not 1 <= self.k_neighbors <= min(64, self.n_neurons - 1):
            raise ValueError("k_neighbors outside allowed range")
        if not 0.0 <= self.rewiring_probability <= 1.0:
            raise ValueError("rewiring_probability must be between 0 and 1")
        if not 1 <= self.modules <= min(32, self.n_neurons):
            raise ValueError("modules outside allowed range")
        if not 1 <= self.ensemble_runs <= 8:
            raise ValueError("ensemble_runs must be between 1 and 8")
        if not 5 <= self.pan_dimensions <= 32:
            raise ValueError("pan_dimensions must be between 5 and 32")
        if not 0.0 <= self.pan_feedback_gain <= 5.0:
            raise ValueError("pan_feedback_gain must be between 0 and 5")
        if not 0.0 <= self.pan_health_decay <= 1.0:
            raise ValueError("pan_health_decay must be between 0 and 1")
        if not 0.0 <= self.pan_apoptosis_threshold <= 1.0:
            raise ValueError("pan_apoptosis_threshold must be between 0 and 1")
        if not 0.0 <= self.pan_aging_threshold <= 1.0:
            raise ValueError("pan_aging_threshold must be between 0 and 1")
        if not 0.0 <= self.pan_bias_current <= 500.0:
            raise ValueError("pan_bias_current must be between 0 and 500")
        if self.pan_aging_threshold < self.pan_apoptosis_threshold:
            raise ValueError("pan_aging_threshold must be >= pan_apoptosis_threshold")
        if self.clock_mode not in {"continuous", "dual"}:
            raise ValueError("clock_mode must be continuous or dual")
        if not 1.0 <= self.clock_base_hz <= 10_000.0:
            raise ValueError("clock_base_hz must be between 1 and 10000")
        if not self.dt_ms <= self.clock_event_batch_ms <= 1000.0:
            raise ValueError("clock_event_batch_ms must be between dt_ms and 1000")
        if self.execution_mode not in {"EVENT_ONLY", "TICK_ONLY", "HYBRID_AUTO"}:
            raise ValueError("unsupported execution_mode")
        if self.execution_initial_mode not in {"EVENT_ONLY", "TICK_ONLY"}:
            raise ValueError("execution_initial_mode must be EVENT_ONLY or TICK_ONLY")
        if not 0.0 <= self.execution_theta_low <= self.execution_theta_high <= 1.0:
            raise ValueError("execution thresholds must satisfy 0 <= low <= high <= 1")
        if not 0.0 <= self.execution_hysteresis <= 0.5:
            raise ValueError("execution_hysteresis must be between 0 and 0.5")
        if not 0 <= self.execution_min_dwell <= 1_000_000:
            raise ValueError("execution_min_dwell must be between 0 and 1000000")
        if not 1 <= self.execution_activity_window <= 1_000_000:
            raise ValueError("execution_activity_window must be between 1 and 1000000")
        if self.execution_transition_mode not in {"clean", "fast", "debug"}:
            raise ValueError("unsupported execution_transition_mode")
        if not 0.0 <= self.growth_activity_threshold <= 1.0:
            raise ValueError("growth_activity_threshold must be between 0 and 1")
        if not 1 <= self.growth_coactivation_threshold <= 1000:
            raise ValueError("growth_coactivation_threshold must be between 1 and 1000")
        if not 0.0 <= self.growth_information_threshold <= 1.0:
            raise ValueError("growth_information_threshold must be between 0 and 1")
        if not 0.0 <= self.growth_prune_threshold <= 100.0:
            raise ValueError("growth_prune_threshold must be between 0 and 100")
        if not 1 <= self.growth_max_synapses_per_neuron <= 512:
            raise ValueError("growth_max_synapses_per_neuron must be between 1 and 512")
        if not 1 <= self.growth_max_new_synapses_per_barrier <= 256:
            raise ValueError(
                "growth_max_new_synapses_per_barrier must be between 1 and 256"
            )
        if not 128 <= self.cuda_budget_mb <= 16_384:
            raise ValueError("cuda_budget_mb must be between 128 and 16384")
        if not 1 <= self.offload_snapshot_interval <= 1_000_000:
            raise ValueError("offload_snapshot_interval must be between 1 and 1000000")
        if self.growth_enabled and self.clock_mode != "dual":
            raise ValueError("growth_enabled requires clock_mode=dual")
        if self.hardware_profile_name not in {"reference_cpu", "cuda_8gb_balanced_plan"}:
            raise ValueError("unsupported hardware_profile_name")
        if not 0.0 <= self.thalamic_relay_threshold <= 1.0:
            raise ValueError("thalamic_relay_threshold must be between 0 and 1")
        if not 0.0 <= self.thalamic_attention_gain <= 4.0:
            raise ValueError("thalamic_attention_gain must be between 0 and 4")
        if not 0.0 <= self.thalamic_inhibition_gain <= 1.0:
            raise ValueError("thalamic_inhibition_gain must be between 0 and 1")
        if not 2 <= self.cortical_layer_count <= 12:
            raise ValueError("cortical_layer_count must be between 2 and 12")
        if not 0.0 <= self.cortical_learning_rate <= 1.0:
            raise ValueError("cortical_learning_rate must be between 0 and 1")
        if not 2 <= self.behavior_action_count <= 16:
            raise ValueError("behavior_action_count must be between 2 and 16")
        if not 0.0 < self.behavior_learning_rate <= 1.0:
            raise ValueError("behavior_learning_rate must be > 0 and <= 1")
        if not 0.0 <= self.behavior_epsilon <= 1.0:
            raise ValueError("behavior_epsilon must be between 0 and 1")
        if not 0 <= self.behavior_target_action < self.behavior_action_count:
            raise ValueError("behavior_target_action outside action range")
        if self.behavior_target_mode not in {"fixed", "cycle"}:
            raise ValueError("behavior_target_mode must be fixed or cycle")
        if not 0.0 <= self.behavior_min_activity <= 1.0:
            raise ValueError("behavior_min_activity must be between 0 and 1")
        if not 1 <= self.behavior_episode_ticks <= 1_000_000:
            raise ValueError(
                "behavior_episode_ticks must be between 1 and 1000000"
            )
        if not 0.0 <= self.behavior_bias_current <= 100.0:
            raise ValueError("behavior_bias_current must be between 0 and 100")
        if not 0.0 <= self.geometry_lambda_a <= 10.0:
            raise ValueError("geometry_lambda_a must be between 0 and 10")
        if not 0.0 <= self.geometry_lambda_b <= 10.0:
            raise ValueError("geometry_lambda_b must be between 0 and 10")
        if not 0.001 <= self.geometry_sigma <= 2.0:
            raise ValueError("geometry_sigma must be between 0.001 and 2")
        if not 0.0 <= self.geometry_p0 <= 1.0:
            raise ValueError("geometry_p0 must be between 0 and 1")
        if self.geometry_mode not in {"mixed_additive", "shortcut_union"}:
            raise ValueError(
                "geometry_mode must be mixed_additive or shortcut_union"
            )
        if not 0.001 <= self.geometry_delay_velocity <= 10.0:
            raise ValueError(
                "geometry_delay_velocity must be between 0.001 and 10"
            )
        if self.neural_io_enabled:
            if not 1 <= self.neural_io_input_channels <= 256:
                raise ValueError(
                    "neural_io_input_channels must be between 1 and 256"
                )
            if not 1 <= self.neural_io_output_channels <= 256:
                raise ValueError(
                    "neural_io_output_channels must be between 1 and 256"
                )
            if (
                self.neural_io_input_channels + self.neural_io_output_channels
                > self.n_neurons
            ):
                raise ValueError("neural I/O populations must not overlap")
            if not 1 <= self.neural_io_window_ticks <= self.ticks:
                raise ValueError(
                    "neural_io_window_ticks must be between 1 and session ticks"
                )
            if not 0.0 <= self.neural_io_input_current <= 500.0:
                raise ValueError(
                    "neural_io_input_current must be between 0 and 500"
                )
            if self.neural_io_input_role not in {
                "AFFERENT",
                "GATEWAY_AFFERENT",
            }:
                raise ValueError(
                    "neural_io_input_role must be AFFERENT or GATEWAY_AFFERENT"
                )
            if self.neural_io_output_role not in {
                "EFFERENT",
                "GATEWAY_EFFERENT",
            }:
                raise ValueError(
                    "neural_io_output_role must be EFFERENT or GATEWAY_EFFERENT"
                )
            if self.neural_io_phase not in {
                "IDLE",
                "QUERY",
                "WAIT",
                "RESPONSE",
                "TIMEOUT",
            }:
                raise ValueError("unsupported neural_io_phase")

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "neuron_model": self.neuron_model,
            "synapse_model": self.synapse_model,
            "plasticity_rule": self.plasticity_rule,
            "topology": self.topology,
            "stimulus": self.stimulus,
            "readout": self.readout,
            "n_neurons": self.n_neurons,
            "edge_budget": self.edge_budget,
            "ticks": self.ticks,
            "seed": self.seed,
            "dimensions": self.dimensions,
            "dt_ms": self.dt_ms,
            "weight": self.weight,
            "delay_ticks": self.delay_ticks,
            "stimulus_current": self.stimulus_current,
            "stimulus_rate_hz": self.stimulus_rate_hz,
            "radius": self.radius,
            "k_neighbors": self.k_neighbors,
            "rewiring_probability": self.rewiring_probability,
            "modules": self.modules,
            "ensemble_runs": self.ensemble_runs,
            "persist": self.persist,
            "pan_enabled": self.pan_enabled,
            "pan_dimensions": self.pan_dimensions,
            "pan_closed_loop": self.pan_closed_loop,
            "pan_feedback_gain": self.pan_feedback_gain,
            "pan_health_decay": self.pan_health_decay,
            "pan_apoptosis_threshold": self.pan_apoptosis_threshold,
            "pan_aging_threshold": self.pan_aging_threshold,
            "pan_bias_current": self.pan_bias_current,
            "clock_mode": self.clock_mode,
            "clock_base_hz": self.clock_base_hz,
            "clock_event_batch_ms": self.clock_event_batch_ms,
            "execution_mode": self.execution_mode,
            "execution_initial_mode": self.execution_initial_mode,
            "execution_theta_high": self.execution_theta_high,
            "execution_theta_low": self.execution_theta_low,
            "execution_hysteresis": self.execution_hysteresis,
            "execution_min_dwell": self.execution_min_dwell,
            "execution_activity_window": self.execution_activity_window,
            "execution_transition_mode": self.execution_transition_mode,
            "execution_sync_on_switch": self.execution_sync_on_switch,
            "execution_log_transitions": self.execution_log_transitions,
            "execution_log_state_hash": self.execution_log_state_hash,
            "growth_enabled": self.growth_enabled,
            "growth_neurogenesis": self.growth_neurogenesis,
            "growth_synaptogenesis": self.growth_synaptogenesis,
            "growth_path_formation": self.growth_path_formation,
            "growth_pruning": self.growth_pruning,
            "growth_activity_threshold": self.growth_activity_threshold,
            "growth_coactivation_threshold": self.growth_coactivation_threshold,
            "growth_information_threshold": self.growth_information_threshold,
            "growth_prune_threshold": self.growth_prune_threshold,
            "growth_max_synapses_per_neuron": self.growth_max_synapses_per_neuron,
            "growth_max_new_synapses_per_barrier": (
                self.growth_max_new_synapses_per_barrier
            ),
            "cuda_budget_mb": self.cuda_budget_mb,
            "offload_enabled": self.offload_enabled,
            "offload_snapshot_interval": self.offload_snapshot_interval,
            "hardware_profile_name": self.hardware_profile_name,
            "thalamic_gating_enabled": self.thalamic_gating_enabled,
            "thalamic_relay_threshold": self.thalamic_relay_threshold,
            "thalamic_attention_gain": self.thalamic_attention_gain,
            "thalamic_inhibition_gain": self.thalamic_inhibition_gain,
            "cortical_layers_enabled": self.cortical_layers_enabled,
            "cortical_layer_count": self.cortical_layer_count,
            "cortical_plasticity": self.cortical_plasticity,
            "cortical_learning_rate": self.cortical_learning_rate,
            "behavior_learning_enabled": self.behavior_learning_enabled,
            "behavior_action_count": self.behavior_action_count,
            "behavior_learning_rate": self.behavior_learning_rate,
            "behavior_epsilon": self.behavior_epsilon,
            "behavior_target_action": self.behavior_target_action,
            "behavior_target_mode": self.behavior_target_mode,
            "behavior_min_activity": self.behavior_min_activity,
            "behavior_episode_ticks": self.behavior_episode_ticks,
            "behavior_bias_current": self.behavior_bias_current,
            "geometry_lambda_a": self.geometry_lambda_a,
            "geometry_lambda_b": self.geometry_lambda_b,
            "geometry_sigma": self.geometry_sigma,
            "geometry_p0": self.geometry_p0,
            "geometry_mode": self.geometry_mode,
            "geometry_delay_velocity": self.geometry_delay_velocity,
            "neural_io_enabled": self.neural_io_enabled,
            "neural_io_input_channels": self.neural_io_input_channels,
            "neural_io_output_channels": self.neural_io_output_channels,
            "neural_io_input_codec": self.neural_io_input_codec,
            "neural_io_output_decoder": self.neural_io_output_decoder,
            "neural_io_input_payload_present": (
                self.neural_io_input_payload is not None
            ),
            "neural_io_window_ticks": self.neural_io_window_ticks,
            "neural_io_input_current": self.neural_io_input_current,
            "neural_io_input_role": self.neural_io_input_role,
            "neural_io_output_role": self.neural_io_output_role,
            "neural_io_phase": self.neural_io_phase,
            "neural_io_correlation_id": self.neural_io_correlation_id,
            "neural_io_modality": self.neural_io_modality,
            "neural_io_source_id": self.neural_io_source_id,
        }


    def to_runtime_dict(self) -> dict[str, object]:
        """Return transient config including the exact I/O payload.

        This mapping is for in-process re-execution only and must never be
        persisted or returned as a session result.
        """

        payload = self.to_dict()
        payload["neural_io_input_payload"] = self.neural_io_input_payload
        return payload
