"""Core data contracts for the non-canonical MHRN playground."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Mapping, TypeAlias

from .closed_loop import CLOSED_LOOP_PRESETS

Coordinate: TypeAlias = tuple[float, ...]
Edge: TypeAlias = tuple[int, int]
ActionInputMap: TypeAlias = str | tuple[tuple[float, ...], ...]

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
    edge_budget: int = 1024
    ticks: int = 256
    seed: int = 12345
    dimensions: int = 5
    dt_ms: float = 1.0
    weight: float = 4.0
    weight_decay: float = 0.0
    weight_max_clamp: float = 100.0
    delay_ticks: int = 1
    stimulus_current: float = 8.0
    stimulus_rate_hz: float = 20.0
    radius: float = 0.35
    k_neighbors: int = 16
    rewiring_probability: float = 0.15
    modules: int = 2
    ensemble_runs: int = 1
    persist: bool = False
    pan_enabled: bool = False
    pan_dimensions: int = 5
    pan_closed_loop: bool = True
    pan_feedback_gain: float = 0.05
    pan_health_decay: float = 0.001
    pan_apoptosis_threshold: float = 0.1
    pan_aging_threshold: float = 0.3
    pan_bias_current: float = 10.0
    clock_mode: str = "continuous"
    clock_base_hz: float = 100.0
    clock_event_batch_ms: float = 10.0
    neuron_backend: str = "cpu"
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
    behavior_learning_rate: float = 0.2
    behavior_epsilon: float = 0.2
    behavior_target_action: int = 0
    behavior_target_mode: str = "cycle"
    behavior_min_activity: float = 0.01
    behavior_episode_ticks: int = 16
    behavior_bias_current: float = 3.0
    geometry_lambda_a: float = 0.5
    geometry_lambda_b: float = 0.5
    geometry_sigma: float = 0.1
    geometry_p0: float = 0.3
    geometry_mode: str = "mixed_additive"
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

    closed_loop_preset: str = "custom"
    input_topology: str = "uniform"
    input_channels: int = 16
    input_channel_map: tuple[tuple[int, ...], ...] = ()
    input_amplitude_per_channel: tuple[float, ...] = ()
    input_frequency_per_channel: tuple[float, ...] = ()
    input_phase_per_channel: tuple[float, ...] = ()
    input_noise_sigma: float = 0.0
    target_cue_channel: int = 0
    reward_cue_channel: int = 0
    action_feedback_channel: int = 0
    posture_score_channel: int = 2
    reward_event_channel: int = 3
    posture_current_scale: float = 25.0
    reward_event_scale: float = 25.0
    posture_reward_enabled: bool = False
    posture_weight_upright: float = 0.4
    posture_weight_height: float = 0.3
    posture_weight_stability: float = 0.2
    posture_weight_symmetry: float = 0.1
    posture_target_height: float = 1.0
    posture_tilt_max: float = 1.0
    posture_velocity_max: float = 5.0
    trigger_good_score: float = 0.85
    trigger_good_duration: int = 10
    trigger_good_reward: float = 1.0
    trigger_warning_score: float = 0.4
    trigger_warning_reward: float = -0.3
    trigger_falling_rate: float = -0.05
    trigger_falling_reward: float = -1.0
    trigger_collapse_score: float = 0.1
    trigger_collapse_reward: float = -5.0
    trigger_recovery_bonus: float = 2.0
    reward_continuous_alpha: float = 0.1
    episode_termination_enabled: bool = True
    episode_max_ticks: int = 256
    episode_reset_on_collapse: bool = True

    pan_feedback_delay: int = 0
    pan_feedback_source: str = "population"
    pan_feedback_target: str = "all"
    pan_feedback_nonlinearity: str = "linear"
    pan_feedback_threshold: float = 0.0
    pan_feedback_saturation: float = 100.0

    action_loop_enabled: bool = False
    action_loop_delay: int = 1
    action_persistence: int = 1
    action_to_input_map: ActionInputMap = "auto"
    action_space_size: int = 4
    action_coupling_strength: float = 0.0
    action_noise: float = 0.0
    freeze_actions: bool = False
    frozen_action_sequence: tuple[int, ...] = ()

    reward_signal_enabled: bool = False
    reward_magnitude: float = 1.0
    reward_delay_ticks: int = 0
    reward_shaping: str = "sparse"
    reward_baseline: float = 0.0
    reward_decay: float = 0.0
    reward_channel: int = 0
    freeze_rewards: bool = False
    frozen_reward_sequence: tuple[float, ...] = ()
    parity_reference_source: str = "CPU_PYTHON_PLAYGROUND"
    parity_reference_commit: str = ""

    target_encoding: str = "none"
    target_persistence: int = 1
    target_cue_current: float = 0.0
    target_shuffle: bool = False
    target_predictability: str = "deterministic"

    credit_window: int = 64
    eligibility_trace_tau: float = 200.0
    credit_assignment: str = "none"
    td_lambda: float = 0.9
    gamma_discount: float = 0.95

    neuron_threshold_variance: float = 0.0
    neuron_tau_m_variance: float = 0.0
    inhibitory_fraction: float = 0.0
    gaba_strength: float = 1.0
    e_i_ratio: float = 1.0
    delay_distribution: str = "fixed"
    delay_mean_ticks: float = 1.0

    refractory_variance: float = 0.0
    adaptation_strength: float = 0.0
    adaptation_tau: float = 200.0
    oscillation_enabled: bool = False
    oscillation_frequency: float = 8.0

    geometry_input_coupling: bool = False
    geometry_input_sigma: float = 0.2
    sandbox_enabled: bool = False
    sandbox_physics: str = "stick_figure"
    sandbox_action_coupling: str = "direct"
    sandbox_sensor_noise: float = 0.05

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> "PlaygroundConfig":
        """Build a config from untrusted API/CLI input and validate all bounds."""

        defaults = cls()
        raw_payload = dict(payload)
        requested_preset = raw_payload.get("closed_loop_preset", "custom")
        if not isinstance(requested_preset, str):
            raise ValueError("closed_loop_preset must be a string")
        requested_preset = requested_preset.strip() or "custom"

        def resolve_preset(name: str, seen: set[str]) -> dict[str, object]:
            if name == "custom":
                return {}
            if name in seen:
                raise ValueError("closed_loop preset inheritance cycle")
            item = CLOSED_LOOP_PRESETS.get(name)
            if item is None:
                raise ValueError(f"unknown closed_loop_preset: {name}")
            raw_settings = item.get("settings", {})
            if not isinstance(raw_settings, Mapping):
                raise ValueError(f"invalid settings for preset: {name}")
            settings = dict(raw_settings)
            parent = settings.pop("closed_loop_preset", None)
            merged: dict[str, object] = {}
            if isinstance(parent, str):
                merged.update(resolve_preset(parent, seen | {name}))
            merged.update(settings)
            return merged

        if requested_preset != "custom":
            preset_payload = resolve_preset(requested_preset, set())
            preset_payload.update(raw_payload)
            payload = preset_payload
        else:
            payload = raw_payload

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

        def numbers(name: str, default: tuple[float, ...]) -> tuple[float, ...]:
            value = payload.get(name, default)
            if not isinstance(value, (list, tuple)):
                raise ValueError(f"{name} must be an array")
            result: list[float] = []
            for item in value:
                if isinstance(item, bool) or not isinstance(item, (int, float)):
                    raise ValueError(f"{name} values must be numeric")
                result.append(float(item))
            return tuple(result)

        def integers(name: str, default: tuple[int, ...]) -> tuple[int, ...]:
            value = payload.get(name, default)
            if not isinstance(value, (list, tuple)):
                raise ValueError(f"{name} must be an array")
            result: list[int] = []
            for item in value:
                if isinstance(item, bool) or not isinstance(item, (int, float)):
                    raise ValueError(f"{name} values must be integers")
                converted = int(item)
                if float(item) != float(converted):
                    raise ValueError(f"{name} values must be integers")
                result.append(converted)
            return tuple(result)

        def optional_text(name: str, default: str) -> str:
            value = payload.get(name, default)
            if not isinstance(value, str):
                raise ValueError(f"{name} must be a string")
            return value.strip()

        def integer_groups(
            name: str,
            default: tuple[tuple[int, ...], ...],
        ) -> tuple[tuple[int, ...], ...]:
            value = payload.get(name, default)
            if not isinstance(value, (list, tuple)):
                raise ValueError(f"{name} must be an array of arrays")
            groups: list[tuple[int, ...]] = []
            for group in value:
                if not isinstance(group, (list, tuple)):
                    raise ValueError(f"{name} must be an array of arrays")
                converted: list[int] = []
                for item in group:
                    if isinstance(item, bool) or not isinstance(item, (int, float)):
                        raise ValueError(
                            f"{name} values must be integer neuron indices"
                        )
                    integer_value = int(item)
                    if float(item) != float(integer_value):
                        raise ValueError(
                            f"{name} values must be integer neuron indices"
                        )
                    converted.append(integer_value)
                groups.append(tuple(converted))
            return tuple(groups)

        def action_map(name: str, default: ActionInputMap) -> ActionInputMap:
            value = payload.get(name, default)
            if isinstance(value, str):
                normalized = value.strip().lower()
                if normalized not in {"auto", "spatial"}:
                    raise ValueError(f"{name} must be auto, spatial, or an array")
                return normalized
            if not isinstance(value, (list, tuple)):
                raise ValueError(f"{name} must be auto, spatial, or an array")
            rows: list[tuple[float, ...]] = []
            for row in value:
                if not isinstance(row, (list, tuple)):
                    raise ValueError(f"{name} array rows must be arrays")
                converted: list[float] = []
                for item in row:
                    if isinstance(item, bool) or not isinstance(item, (int, float)):
                        raise ValueError(f"{name} values must be numeric")
                    converted.append(float(item))
                rows.append(tuple(converted))
            return tuple(rows)

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
            weight_decay=number("weight_decay", defaults.weight_decay),
            weight_max_clamp=number("weight_max_clamp", defaults.weight_max_clamp),
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
            pan_feedback_gain=number("pan_feedback_gain", defaults.pan_feedback_gain),
            pan_health_decay=number("pan_health_decay", defaults.pan_health_decay),
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
            neuron_backend=text("neuron_backend", defaults.neuron_backend).lower(),
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
                payload.get(
                    "execution_sync_on_switch", defaults.execution_sync_on_switch
                )
            ),
            execution_log_transitions=bool(
                payload.get(
                    "execution_log_transitions", defaults.execution_log_transitions
                )
            ),
            execution_log_state_hash=bool(
                payload.get(
                    "execution_log_state_hash", defaults.execution_log_state_hash
                )
            ),
            growth_enabled=bool(payload.get("growth_enabled", defaults.growth_enabled)),
            growth_neurogenesis=bool(
                payload.get("growth_neurogenesis", defaults.growth_neurogenesis)
            ),
            growth_synaptogenesis=bool(
                payload.get("growth_synaptogenesis", defaults.growth_synaptogenesis)
            ),
            growth_path_formation=bool(
                payload.get("growth_path_formation", defaults.growth_path_formation)
            ),
            growth_pruning=bool(payload.get("growth_pruning", defaults.growth_pruning)),
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
                payload.get(
                    "behavior_learning_enabled", defaults.behavior_learning_enabled
                )
            ),
            behavior_action_count=integer(
                "behavior_action_count", defaults.behavior_action_count
            ),
            behavior_learning_rate=number(
                "behavior_learning_rate", defaults.behavior_learning_rate
            ),
            behavior_epsilon=number("behavior_epsilon", defaults.behavior_epsilon),
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
            geometry_lambda_a=number("geometry_lambda_a", defaults.geometry_lambda_a),
            geometry_lambda_b=number("geometry_lambda_b", defaults.geometry_lambda_b),
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
            neural_io_phase=text("neural_io_phase", defaults.neural_io_phase),
            neural_io_correlation_id=text(
                "neural_io_correlation_id",
                defaults.neural_io_correlation_id or "auto",
            ),
            neural_io_modality=text("neural_io_modality", defaults.neural_io_modality),
            neural_io_source_id=text(
                "neural_io_source_id", defaults.neural_io_source_id
            ),
            closed_loop_preset=requested_preset,
            input_topology=text("input_topology", defaults.input_topology).lower(),
            input_channels=integer("input_channels", defaults.input_channels),
            input_channel_map=integer_groups(
                "input_channel_map", defaults.input_channel_map
            ),
            input_amplitude_per_channel=numbers(
                "input_amplitude_per_channel",
                defaults.input_amplitude_per_channel,
            ),
            input_frequency_per_channel=numbers(
                "input_frequency_per_channel",
                defaults.input_frequency_per_channel,
            ),
            input_phase_per_channel=numbers(
                "input_phase_per_channel",
                defaults.input_phase_per_channel,
            ),
            input_noise_sigma=number("input_noise_sigma", defaults.input_noise_sigma),
            target_cue_channel=integer(
                "target_cue_channel", defaults.target_cue_channel
            ),
            reward_cue_channel=integer(
                "reward_cue_channel", defaults.reward_cue_channel
            ),
            action_feedback_channel=integer(
                "action_feedback_channel", defaults.action_feedback_channel
            ),
            posture_score_channel=integer(
                "posture_score_channel", defaults.posture_score_channel
            ),
            reward_event_channel=integer(
                "reward_event_channel", defaults.reward_event_channel
            ),
            posture_current_scale=number(
                "posture_current_scale", defaults.posture_current_scale
            ),
            reward_event_scale=number(
                "reward_event_scale", defaults.reward_event_scale
            ),
            posture_reward_enabled=bool(
                payload.get("posture_reward_enabled", defaults.posture_reward_enabled)
            ),
            posture_weight_upright=number(
                "posture_weight_upright", defaults.posture_weight_upright
            ),
            posture_weight_height=number(
                "posture_weight_height", defaults.posture_weight_height
            ),
            posture_weight_stability=number(
                "posture_weight_stability", defaults.posture_weight_stability
            ),
            posture_weight_symmetry=number(
                "posture_weight_symmetry", defaults.posture_weight_symmetry
            ),
            posture_target_height=number(
                "posture_target_height", defaults.posture_target_height
            ),
            posture_tilt_max=number("posture_tilt_max", defaults.posture_tilt_max),
            posture_velocity_max=number(
                "posture_velocity_max", defaults.posture_velocity_max
            ),
            trigger_good_score=number(
                "trigger_good_score", defaults.trigger_good_score
            ),
            trigger_good_duration=integer(
                "trigger_good_duration", defaults.trigger_good_duration
            ),
            trigger_good_reward=number(
                "trigger_good_reward", defaults.trigger_good_reward
            ),
            trigger_warning_score=number(
                "trigger_warning_score", defaults.trigger_warning_score
            ),
            trigger_warning_reward=number(
                "trigger_warning_reward", defaults.trigger_warning_reward
            ),
            trigger_falling_rate=number(
                "trigger_falling_rate", defaults.trigger_falling_rate
            ),
            trigger_falling_reward=number(
                "trigger_falling_reward", defaults.trigger_falling_reward
            ),
            trigger_collapse_score=number(
                "trigger_collapse_score", defaults.trigger_collapse_score
            ),
            trigger_collapse_reward=number(
                "trigger_collapse_reward", defaults.trigger_collapse_reward
            ),
            trigger_recovery_bonus=number(
                "trigger_recovery_bonus", defaults.trigger_recovery_bonus
            ),
            reward_continuous_alpha=number(
                "reward_continuous_alpha", defaults.reward_continuous_alpha
            ),
            episode_termination_enabled=bool(
                payload.get(
                    "episode_termination_enabled", defaults.episode_termination_enabled
                )
            ),
            episode_max_ticks=integer("episode_max_ticks", defaults.episode_max_ticks),
            episode_reset_on_collapse=bool(
                payload.get(
                    "episode_reset_on_collapse", defaults.episode_reset_on_collapse
                )
            ),
            pan_feedback_delay=integer(
                "pan_feedback_delay", defaults.pan_feedback_delay
            ),
            pan_feedback_source=text(
                "pan_feedback_source", defaults.pan_feedback_source
            ).lower(),
            pan_feedback_target=text(
                "pan_feedback_target", defaults.pan_feedback_target
            ).lower(),
            pan_feedback_nonlinearity=text(
                "pan_feedback_nonlinearity", defaults.pan_feedback_nonlinearity
            ).lower(),
            pan_feedback_threshold=number(
                "pan_feedback_threshold", defaults.pan_feedback_threshold
            ),
            pan_feedback_saturation=number(
                "pan_feedback_saturation", defaults.pan_feedback_saturation
            ),
            action_loop_enabled=bool(
                payload.get("action_loop_enabled", defaults.action_loop_enabled)
            ),
            action_loop_delay=integer("action_loop_delay", defaults.action_loop_delay),
            action_persistence=integer(
                "action_persistence", defaults.action_persistence
            ),
            action_to_input_map=action_map(
                "action_to_input_map", defaults.action_to_input_map
            ),
            action_space_size=integer("action_space_size", defaults.action_space_size),
            action_coupling_strength=number(
                "action_coupling_strength", defaults.action_coupling_strength
            ),
            action_noise=number("action_noise", defaults.action_noise),
            freeze_actions=bool(payload.get("freeze_actions", defaults.freeze_actions)),
            frozen_action_sequence=integers(
                "frozen_action_sequence", defaults.frozen_action_sequence
            ),
            reward_signal_enabled=bool(
                payload.get(
                    "reward_signal_enabled",
                    defaults.reward_signal_enabled,
                )
            ),
            reward_magnitude=number("reward_magnitude", defaults.reward_magnitude),
            reward_delay_ticks=integer(
                "reward_delay_ticks", defaults.reward_delay_ticks
            ),
            reward_shaping=text("reward_shaping", defaults.reward_shaping).lower(),
            reward_baseline=number("reward_baseline", defaults.reward_baseline),
            reward_decay=number("reward_decay", defaults.reward_decay),
            reward_channel=integer(
                "reward_channel",
                integer("reward_cue_channel", defaults.reward_channel),
            ),
            freeze_rewards=bool(payload.get("freeze_rewards", defaults.freeze_rewards)),
            frozen_reward_sequence=numbers(
                "frozen_reward_sequence", defaults.frozen_reward_sequence
            ),
            parity_reference_source=optional_text(
                "parity_reference_source", defaults.parity_reference_source
            ),
            parity_reference_commit=optional_text(
                "parity_reference_commit", defaults.parity_reference_commit
            ),
            target_encoding=text("target_encoding", defaults.target_encoding).lower(),
            target_persistence=integer(
                "target_persistence", defaults.target_persistence
            ),
            target_cue_current=number(
                "target_cue_current", defaults.target_cue_current
            ),
            target_shuffle=bool(payload.get("target_shuffle", defaults.target_shuffle)),
            target_predictability=text(
                "target_predictability", defaults.target_predictability
            ).lower(),
            credit_window=integer("credit_window", defaults.credit_window),
            eligibility_trace_tau=number(
                "eligibility_trace_tau", defaults.eligibility_trace_tau
            ),
            credit_assignment=text(
                "credit_assignment", defaults.credit_assignment
            ).lower(),
            td_lambda=number("td_lambda", defaults.td_lambda),
            gamma_discount=number("gamma_discount", defaults.gamma_discount),
            neuron_threshold_variance=number(
                "neuron_threshold_variance",
                defaults.neuron_threshold_variance,
            ),
            neuron_tau_m_variance=number(
                "neuron_tau_m_variance", defaults.neuron_tau_m_variance
            ),
            inhibitory_fraction=number(
                "inhibitory_fraction", defaults.inhibitory_fraction
            ),
            gaba_strength=number("gaba_strength", defaults.gaba_strength),
            e_i_ratio=number("e_i_ratio", defaults.e_i_ratio),
            delay_distribution=text(
                "delay_distribution", defaults.delay_distribution
            ).lower(),
            delay_mean_ticks=number("delay_mean_ticks", defaults.delay_mean_ticks),
            refractory_variance=number(
                "refractory_variance", defaults.refractory_variance
            ),
            adaptation_strength=number(
                "adaptation_strength", defaults.adaptation_strength
            ),
            adaptation_tau=number("adaptation_tau", defaults.adaptation_tau),
            oscillation_enabled=bool(
                payload.get(
                    "oscillation_enabled",
                    defaults.oscillation_enabled,
                )
            ),
            oscillation_frequency=number(
                "oscillation_frequency", defaults.oscillation_frequency
            ),
            geometry_input_coupling=bool(
                payload.get(
                    "geometry_input_coupling",
                    defaults.geometry_input_coupling,
                )
            ),
            geometry_input_sigma=number(
                "geometry_input_sigma", defaults.geometry_input_sigma
            ),
            sandbox_enabled=bool(
                payload.get("sandbox_enabled", defaults.sandbox_enabled)
            ),
            sandbox_physics=text("sandbox_physics", defaults.sandbox_physics).lower(),
            sandbox_action_coupling=text(
                "sandbox_action_coupling",
                defaults.sandbox_action_coupling,
            ).lower(),
            sandbox_sensor_noise=number(
                "sandbox_sensor_noise", defaults.sandbox_sensor_noise
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
        if not 0.0 <= self.weight_decay <= 1.0:
            raise ValueError("weight_decay must be between 0 and 1")
        if not 0.0 < self.weight_max_clamp <= 100.0:
            raise ValueError("weight_max_clamp must be > 0 and <= 100")
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
        if self.neuron_backend not in {"cpu", "cuda_membrane"}:
            raise ValueError("neuron_backend must be cpu or cuda_membrane")
        if self.neuron_backend == "cuda_membrane" and self.neuron_model not in {
            "lif",
            "adex",
            "pan_adex_5d",
        }:
            raise ValueError("CUDA membrane backend supports LIF/AdEx/PAN-AdEx only")
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
        if self.hardware_profile_name not in {
            "reference_cpu",
            "cuda_8gb_balanced_plan",
        }:
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
        if not 1 <= self.behavior_action_count <= 16:
            raise ValueError("behavior_action_count must be between 1 and 16")
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
            raise ValueError("behavior_episode_ticks must be between 1 and 1000000")
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
            raise ValueError("geometry_mode must be mixed_additive or shortcut_union")
        if not 0.001 <= self.geometry_delay_velocity <= 10.0:
            raise ValueError("geometry_delay_velocity must be between 0.001 and 10")
        if (
            self.closed_loop_preset != "custom"
            and self.closed_loop_preset not in CLOSED_LOOP_PRESETS
        ):
            raise ValueError("unsupported closed_loop_preset")
        if self.input_topology not in {
            "uniform",
            "channel_partitioned",
            "spatial_gradient",
            "random_per_neuron",
        }:
            raise ValueError("unsupported input_topology")
        if not 1 <= self.input_channels <= 64:
            raise ValueError("input_channels must be between 1 and 64")
        if len(self.input_channel_map) > self.input_channels:
            raise ValueError("input_channel_map has more groups than input_channels")
        for group in self.input_channel_map:
            if any(index < 0 or index >= self.n_neurons for index in group):
                raise ValueError("input_channel_map contains an invalid neuron index")
        for name, values, low, high in (
            (
                "input_amplitude_per_channel",
                self.input_amplitude_per_channel,
                0.0,
                500.0,
            ),
            (
                "input_frequency_per_channel",
                self.input_frequency_per_channel,
                1.0,
                200.0,
            ),
            (
                "input_phase_per_channel",
                self.input_phase_per_channel,
                0.0,
                2.0 * math.pi,
            ),
        ):
            if len(values) > self.input_channels:
                raise ValueError(f"{name} has more values than input_channels")
            if any(value < low or value > high for value in values):
                raise ValueError(f"{name} values outside allowed range")
        if not 0.0 <= self.input_noise_sigma <= 1.0:
            raise ValueError("input_noise_sigma must be between 0 and 1")
        for name, channel in (
            ("target_cue_channel", self.target_cue_channel),
            ("reward_cue_channel", self.reward_cue_channel),
            ("reward_channel", self.reward_channel),
            ("action_feedback_channel", self.action_feedback_channel),
            ("posture_score_channel", self.posture_score_channel),
            ("reward_event_channel", self.reward_event_channel),
        ):
            if not 0 <= channel < self.input_channels:
                raise ValueError(f"{name} outside input channel range")
        if not 0 <= self.pan_feedback_delay <= 64:
            raise ValueError("pan_feedback_delay must be between 0 and 64")
        if self.pan_feedback_source not in {
            "population",
            "layer",
            "subset",
            "hypervector",
        }:
            raise ValueError("unsupported pan_feedback_source")
        if self.pan_feedback_target not in {"all", "layer", "random_subset"}:
            raise ValueError("unsupported pan_feedback_target")
        if self.pan_feedback_nonlinearity not in {"linear", "tanh", "sign", "clip"}:
            raise ValueError("unsupported pan_feedback_nonlinearity")
        if not 0.0 <= self.pan_feedback_threshold <= 1.0:
            raise ValueError("pan_feedback_threshold must be between 0 and 1")
        if not 0.0 <= self.pan_feedback_saturation <= 100.0:
            raise ValueError("pan_feedback_saturation must be between 0 and 100")
        if not 1 <= self.action_loop_delay <= 64:
            raise ValueError("action_loop_delay must be between 1 and 64")
        if not 1 <= self.action_persistence <= 128:
            raise ValueError("action_persistence must be between 1 and 128")
        if not 1 <= self.action_space_size <= 32:
            raise ValueError("action_space_size must be between 1 and 32")
        if (
            self.behavior_target_mode == "fixed"
            and self.behavior_target_action >= self.action_space_size
        ):
            raise ValueError("behavior_target_action outside closed-loop action range")
        if not 0.0 <= self.action_coupling_strength <= 10.0:
            raise ValueError("action_coupling_strength must be between 0 and 10")
        if not 0.0 <= self.action_noise <= 1.0:
            raise ValueError("action_noise must be between 0 and 1")
        required_episodes = self.ticks // self.behavior_episode_ticks
        if self.freeze_actions:
            if len(self.frozen_action_sequence) < required_episodes:
                raise ValueError(
                    "frozen_action_sequence must cover every completed episode"
                )
            if any(
                action < 0 or action >= self.action_space_size
                for action in self.frozen_action_sequence
            ):
                raise ValueError("frozen_action_sequence contains invalid action")
        if self.freeze_rewards:
            if not self.reward_signal_enabled:
                raise ValueError("freeze_rewards requires reward_signal_enabled")
            if len(self.frozen_reward_sequence) < required_episodes:
                raise ValueError(
                    "frozen_reward_sequence must cover every completed episode"
                )
            if any(
                not math.isfinite(reward) or abs(reward) > 100.0
                for reward in self.frozen_reward_sequence
            ):
                raise ValueError(
                    "frozen_reward_sequence values must be finite and <= 100 abs"
                )
        if self.freeze_actions or self.freeze_rewards:
            if self.parity_reference_source != "CPU_PYTHON_PLAYGROUND":
                raise ValueError(
                    "parity_reference_source must be CPU_PYTHON_PLAYGROUND"
                )
            if re.fullmatch(r"[0-9a-fA-F]{7,40}", self.parity_reference_commit) is None:
                raise ValueError(
                    "parity_reference_commit must be a 7-40 character git SHA"
                )
        if not isinstance(self.action_to_input_map, str):
            if len(self.action_to_input_map) > self.action_space_size:
                raise ValueError("action_to_input_map has more rows than actions")
            for row in self.action_to_input_map:
                if len(row) > self.input_channels:
                    raise ValueError("action_to_input_map row exceeds input_channels")
        if not 0.0 <= self.reward_magnitude <= 10.0:
            raise ValueError("reward_magnitude must be between 0 and 10")
        if not 0 <= self.reward_delay_ticks <= 64:
            raise ValueError("reward_delay_ticks must be between 0 and 64")
        if self.reward_shaping not in {"sparse", "dense", "potential_based"}:
            raise ValueError("unsupported reward_shaping")
        if not -1.0 <= self.reward_baseline <= 1.0:
            raise ValueError("reward_baseline must be between -1 and 1")
        if not 0.0 <= self.reward_decay <= 1.0:
            raise ValueError("reward_decay must be between 0 and 1")
        if self.target_encoding not in {
            "none",
            "one_hot",
            "rate",
            "population_latency",
        }:
            raise ValueError("unsupported target_encoding")
        if not 1 <= self.target_persistence <= 256:
            raise ValueError("target_persistence must be between 1 and 256")
        if not 0.0 <= self.target_cue_current <= 500.0:
            raise ValueError("target_cue_current must be between 0 and 500")
        if self.target_predictability not in {
            "deterministic",
            "stochastic",
            "adversarial",
        }:
            raise ValueError("unsupported target_predictability")
        if not 1 <= self.credit_window <= 512:
            raise ValueError("credit_window must be between 1 and 512")
        if not 1.0 <= self.eligibility_trace_tau <= 1000.0:
            raise ValueError("eligibility_trace_tau must be between 1 and 1000 ms")
        if self.credit_assignment not in {"none", "trace", "reward_modulated_stdp"}:
            raise ValueError("unsupported credit_assignment")
        if not 0.0 <= self.td_lambda <= 1.0:
            raise ValueError("td_lambda must be between 0 and 1")
        if not 0.0 <= self.gamma_discount <= 1.0:
            raise ValueError("gamma_discount must be between 0 and 1")
        for name, value in (
            ("neuron_threshold_variance", self.neuron_threshold_variance),
            ("neuron_tau_m_variance", self.neuron_tau_m_variance),
            ("inhibitory_fraction", self.inhibitory_fraction),
            ("refractory_variance", self.refractory_variance),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")
        if not 0.0 <= self.gaba_strength <= 10.0:
            raise ValueError("gaba_strength must be between 0 and 10")
        if not 0.0 <= self.e_i_ratio <= 10.0:
            raise ValueError("e_i_ratio must be between 0 and 10")
        if self.delay_distribution not in {"fixed", "uniform", "lognormal", "gamma"}:
            raise ValueError("unsupported delay_distribution")
        if not 1.0 <= self.delay_mean_ticks <= 32.0:
            raise ValueError("delay_mean_ticks must be between 1 and 32")
        if not 0.0 <= self.adaptation_strength <= 10.0:
            raise ValueError("adaptation_strength must be between 0 and 10")
        if not 10.0 <= self.adaptation_tau <= 1000.0:
            raise ValueError("adaptation_tau must be between 10 and 1000 ms")
        if not 0.5 <= self.oscillation_frequency <= 100.0:
            raise ValueError("oscillation_frequency must be between 0.5 and 100 Hz")
        if not 0.001 <= self.geometry_input_sigma <= 2.0:
            raise ValueError("geometry_input_sigma must be between 0.001 and 2")
        if not 0.0 <= self.sandbox_sensor_noise <= 1.0:
            raise ValueError("sandbox_sensor_noise must be between 0 and 1")
        if self.sandbox_physics != "stick_figure":
            raise ValueError("sandbox_physics must be stick_figure")
        if self.sandbox_action_coupling != "direct":
            raise ValueError("sandbox_action_coupling must be direct")

        if self.neural_io_enabled:
            if not 1 <= self.neural_io_input_channels <= 256:
                raise ValueError("neural_io_input_channels must be between 1 and 256")
            if not 1 <= self.neural_io_output_channels <= 256:
                raise ValueError("neural_io_output_channels must be between 1 and 256")
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
                raise ValueError("neural_io_input_current must be between 0 and 500")
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
            "weight_decay": self.weight_decay,
            "weight_max_clamp": self.weight_max_clamp,
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
            "neuron_backend": self.neuron_backend,
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
            "closed_loop_preset": self.closed_loop_preset,
            "input_topology": self.input_topology,
            "input_channels": self.input_channels,
            "input_channel_map": [list(group) for group in self.input_channel_map],
            "input_amplitude_per_channel": list(self.input_amplitude_per_channel),
            "input_frequency_per_channel": list(self.input_frequency_per_channel),
            "input_phase_per_channel": list(self.input_phase_per_channel),
            "input_noise_sigma": self.input_noise_sigma,
            "target_cue_channel": self.target_cue_channel,
            "reward_cue_channel": self.reward_cue_channel,
            "action_feedback_channel": self.action_feedback_channel,
            "posture_score_channel": self.posture_score_channel,
            "reward_event_channel": self.reward_event_channel,
            "posture_current_scale": self.posture_current_scale,
            "reward_event_scale": self.reward_event_scale,
            "posture_reward_enabled": self.posture_reward_enabled,
            "posture_weight_upright": self.posture_weight_upright,
            "posture_weight_height": self.posture_weight_height,
            "posture_weight_stability": self.posture_weight_stability,
            "posture_weight_symmetry": self.posture_weight_symmetry,
            "posture_target_height": self.posture_target_height,
            "posture_tilt_max": self.posture_tilt_max,
            "posture_velocity_max": self.posture_velocity_max,
            "trigger_good_score": self.trigger_good_score,
            "trigger_good_duration": self.trigger_good_duration,
            "trigger_good_reward": self.trigger_good_reward,
            "trigger_warning_score": self.trigger_warning_score,
            "trigger_warning_reward": self.trigger_warning_reward,
            "trigger_falling_rate": self.trigger_falling_rate,
            "trigger_falling_reward": self.trigger_falling_reward,
            "trigger_collapse_score": self.trigger_collapse_score,
            "trigger_collapse_reward": self.trigger_collapse_reward,
            "trigger_recovery_bonus": self.trigger_recovery_bonus,
            "reward_continuous_alpha": self.reward_continuous_alpha,
            "episode_termination_enabled": self.episode_termination_enabled,
            "episode_max_ticks": self.episode_max_ticks,
            "episode_reset_on_collapse": self.episode_reset_on_collapse,
            "pan_feedback_delay": self.pan_feedback_delay,
            "pan_feedback_source": self.pan_feedback_source,
            "pan_feedback_target": self.pan_feedback_target,
            "pan_feedback_nonlinearity": self.pan_feedback_nonlinearity,
            "pan_feedback_threshold": self.pan_feedback_threshold,
            "pan_feedback_saturation": self.pan_feedback_saturation,
            "action_loop_enabled": self.action_loop_enabled,
            "action_loop_delay": self.action_loop_delay,
            "action_persistence": self.action_persistence,
            "action_to_input_map": (
                self.action_to_input_map
                if isinstance(self.action_to_input_map, str)
                else [list(row) for row in self.action_to_input_map]
            ),
            "action_space_size": self.action_space_size,
            "action_coupling_strength": self.action_coupling_strength,
            "action_noise": self.action_noise,
            "freeze_actions": self.freeze_actions,
            "frozen_action_sequence": list(self.frozen_action_sequence),
            "reward_signal_enabled": self.reward_signal_enabled,
            "reward_magnitude": self.reward_magnitude,
            "reward_delay_ticks": self.reward_delay_ticks,
            "reward_shaping": self.reward_shaping,
            "reward_baseline": self.reward_baseline,
            "reward_decay": self.reward_decay,
            "reward_channel": self.reward_channel,
            "freeze_rewards": self.freeze_rewards,
            "frozen_reward_sequence": list(self.frozen_reward_sequence),
            "parity_reference_source": self.parity_reference_source,
            "parity_reference_commit": self.parity_reference_commit,
            "target_encoding": self.target_encoding,
            "target_persistence": self.target_persistence,
            "target_cue_current": self.target_cue_current,
            "target_shuffle": self.target_shuffle,
            "target_predictability": self.target_predictability,
            "credit_window": self.credit_window,
            "eligibility_trace_tau": self.eligibility_trace_tau,
            "credit_assignment": self.credit_assignment,
            "td_lambda": self.td_lambda,
            "gamma_discount": self.gamma_discount,
            "neuron_threshold_variance": self.neuron_threshold_variance,
            "neuron_tau_m_variance": self.neuron_tau_m_variance,
            "inhibitory_fraction": self.inhibitory_fraction,
            "gaba_strength": self.gaba_strength,
            "e_i_ratio": self.e_i_ratio,
            "delay_distribution": self.delay_distribution,
            "delay_mean_ticks": self.delay_mean_ticks,
            "refractory_variance": self.refractory_variance,
            "adaptation_strength": self.adaptation_strength,
            "adaptation_tau": self.adaptation_tau,
            "oscillation_enabled": self.oscillation_enabled,
            "oscillation_frequency": self.oscillation_frequency,
            "geometry_input_coupling": self.geometry_input_coupling,
            "geometry_input_sigma": self.geometry_input_sigma,
            "sandbox_enabled": self.sandbox_enabled,
            "sandbox_physics": self.sandbox_physics,
            "sandbox_action_coupling": self.sandbox_action_coupling,
            "sandbox_sensor_noise": self.sandbox_sensor_noise,
        }

    def to_runtime_dict(self) -> dict[str, object]:
        """Return transient config including the exact I/O payload.

        This mapping is for in-process re-execution only and must never be
        persisted or returned as a session result.
        """

        payload = self.to_dict()
        payload["neural_io_input_payload"] = self.neural_io_input_payload
        return payload
