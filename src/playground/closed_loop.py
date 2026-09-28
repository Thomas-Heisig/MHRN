"""Closed-loop environment helpers for the non-canonical Playground.

The implementation is deliberately bounded and deterministic. It creates an
actual action -> consequence -> reward loop for Playground experiments, but it
does not make scientific, biological, cognitive, or generalization claims.
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .models import PlaygroundConfig


CLOSED_LOOP_PRESETS: dict[str, dict[str, object]] = {
    "pan_full_balanced": {
        "label": "PAN · Vollprofil (Standard)",
        "description": "Ausgewogener CPU-Startpunkt: 256 Neuronen, 2000 Ticks, PAN/STP/STDP, "
        "Wachstum, Neural I/O und Strichmann. Getrennte Signalkanäle; kein "
        "Nachweis global optimaler Werte.",
        "hypothesis": "Explorative gemeinsame Ausführung der implementierten PAN-Mechanismen; "
        "Güte und Laufzeit müssen je Aufgabe gemessen werden.",
        "expected_success": None,
        "required_features": [
            "pan",
            "action_loop",
            "reward_modulated_stdp",
            "sandbox",
            "neural_io",
            "growth",
        ],
        "settings": {
            "name": "pan_full_balanced",
            "neuron_backend": "cpu",
            "neuron_model": "pan_adex_5d",
            "synapse_model": "pan_stp_stdp",
            "plasticity_rule": "structural",
            "topology": "mhrn_5d",
            "stimulus": "oscillatory",
            "readout": "population_vector",
            "n_neurons": 256,
            "edge_budget": 2048,
            "ticks": 2000,
            "seed": 12345,
            "dimensions": 5,
            "dt_ms": 1.0,
            "weight": 4.0,
            "weight_decay": 0.001,
            "weight_max_clamp": 20.0,
            "delay_ticks": 2,
            "stimulus_current": 8.0,
            "stimulus_rate_hz": 20.0,
            "radius": 0.35,
            "k_neighbors": 16,
            "rewiring_probability": 0.15,
            "modules": 2,
            "ensemble_runs": 1,
            "persist": True,
            "pan_enabled": True,
            "pan_dimensions": 5,
            "pan_closed_loop": True,
            "pan_feedback_gain": 1.5,
            "pan_health_decay": 0.001,
            "pan_apoptosis_threshold": 0.1,
            "pan_aging_threshold": 0.3,
            "pan_bias_current": 10.0,
            "clock_mode": "dual",
            "clock_base_hz": 100.0,
            "clock_event_batch_ms": 10.0,
            "execution_mode": "HYBRID_AUTO",
            "execution_initial_mode": "EVENT_ONLY",
            "execution_theta_high": 0.3,
            "execution_theta_low": 0.05,
            "execution_hysteresis": 0.02,
            "execution_min_dwell": 100,
            "execution_activity_window": 100,
            "execution_transition_mode": "clean",
            "execution_sync_on_switch": True,
            "execution_log_transitions": True,
            "execution_log_state_hash": True,
            "growth_enabled": True,
            "growth_neurogenesis": True,
            "growth_synaptogenesis": True,
            "growth_path_formation": True,
            "growth_pruning": True,
            "growth_activity_threshold": 0.03,
            "growth_coactivation_threshold": 1,
            "growth_information_threshold": 0.03,
            "growth_prune_threshold": 0.05,
            "growth_max_synapses_per_neuron": 32,
            "growth_max_new_synapses_per_barrier": 8,
            "cuda_budget_mb": 2048,
            "offload_enabled": False,
            "offload_snapshot_interval": 1000,
            "hardware_profile_name": "reference_cpu",
            "thalamic_gating_enabled": True,
            "thalamic_relay_threshold": 0.0,
            "thalamic_attention_gain": 1.15,
            "thalamic_inhibition_gain": 0.5,
            "cortical_layers_enabled": True,
            "cortical_layer_count": 6,
            "cortical_plasticity": True,
            "cortical_learning_rate": 0.01,
            "behavior_learning_enabled": True,
            "behavior_action_count": 4,
            "behavior_learning_rate": 0.2,
            "behavior_epsilon": 0.2,
            "behavior_target_action": 0,
            "behavior_target_mode": "cycle",
            "behavior_min_activity": 0.01,
            "behavior_episode_ticks": 64,
            "behavior_bias_current": 20.0,
            "geometry_lambda_a": 0.5,
            "geometry_lambda_b": 0.5,
            "geometry_sigma": 0.1,
            "geometry_p0": 0.3,
            "geometry_mode": "mixed_additive",
            "geometry_delay_velocity": 0.25,
            "neural_io_enabled": True,
            "neural_io_input_channels": 8,
            "neural_io_output_channels": 16,
            "neural_io_input_codec": "population_latency_v1",
            "neural_io_output_decoder": "population_rate_v1",
            "neural_io_input_payload": 0.5,
            "neural_io_window_ticks": 16,
            "neural_io_input_current": 25.0,
            "neural_io_input_role": "GATEWAY_AFFERENT",
            "neural_io_output_role": "GATEWAY_EFFERENT",
            "neural_io_phase": "QUERY",
            "neural_io_correlation_id": "auto",
            "neural_io_modality": "digital",
            "neural_io_source_id": "playground.input",
            "input_topology": "channel_partitioned",
            "input_channels": 8,
            "input_channel_map": (),
            "input_amplitude_per_channel": [8.0, 8.0, 8.0, 8.0, 4.0, 4.0, 4.0, 4.0],
            "input_frequency_per_channel": [
                20.0,
                22.0,
                24.0,
                26.0,
                30.0,
                32.0,
                34.0,
                36.0,
            ],
            "input_phase_per_channel": [0.0, 0.25, 0.5, 0.75, 0.0, 0.25, 0.5, 0.75],
            "input_noise_sigma": 0.1,
            "target_cue_channel": 0,
            "reward_cue_channel": 5,
            "action_feedback_channel": 6,
            "posture_score_channel": 2,
            "reward_event_channel": 3,
            "posture_current_scale": 25.0,
            "reward_event_scale": 25.0,
            "posture_reward_enabled": True,
            "posture_weight_upright": 0.4,
            "posture_weight_height": 0.3,
            "posture_weight_stability": 0.2,
            "posture_weight_symmetry": 0.1,
            "posture_target_height": 1.0,
            "posture_tilt_max": 1.0,
            "posture_velocity_max": 5.0,
            "trigger_good_score": 0.85,
            "trigger_good_duration": 10,
            "trigger_good_reward": 1.0,
            "trigger_warning_score": 0.4,
            "trigger_warning_reward": -0.3,
            "trigger_falling_rate": -0.05,
            "trigger_falling_reward": -1.0,
            "trigger_collapse_score": 0.1,
            "trigger_collapse_reward": -5.0,
            "trigger_recovery_bonus": 2.0,
            "reward_continuous_alpha": 0.1,
            "episode_termination_enabled": True,
            "episode_max_ticks": 256,
            "episode_reset_on_collapse": True,
            "pan_feedback_delay": 0,
            "pan_feedback_source": "population",
            "pan_feedback_target": "all",
            "pan_feedback_nonlinearity": "tanh",
            "pan_feedback_threshold": 0.0,
            "pan_feedback_saturation": 20.0,
            "action_loop_enabled": True,
            "action_loop_delay": 1,
            "action_persistence": 1,
            "action_to_input_map": "spatial",
            "action_space_size": 4,
            "action_coupling_strength": 2.0,
            "action_noise": 0.05,
            "freeze_actions": False,
            "frozen_action_sequence": (),
            "reward_signal_enabled": True,
            "reward_magnitude": 5.0,
            "reward_delay_ticks": 0,
            "reward_shaping": "sparse",
            "reward_baseline": 0.0,
            "reward_decay": 0.0,
            "reward_channel": 1,
            "freeze_rewards": False,
            "frozen_reward_sequence": (),
            "parity_reference_source": "CPU_PYTHON_PLAYGROUND",
            "parity_reference_commit": "",
            "target_encoding": "one_hot",
            "target_persistence": 16,
            "target_cue_current": 30.0,
            "target_shuffle": True,
            "target_predictability": "deterministic",
            "credit_window": 64,
            "eligibility_trace_tau": 200.0,
            "credit_assignment": "reward_modulated_stdp",
            "td_lambda": 0.9,
            "gamma_discount": 0.95,
            "neuron_threshold_variance": 0.3,
            "neuron_tau_m_variance": 0.2,
            "inhibitory_fraction": 0.25,
            "gaba_strength": 6.0,
            "e_i_ratio": 3.0,
            "delay_distribution": "lognormal",
            "delay_mean_ticks": 3.0,
            "refractory_variance": 0.3,
            "adaptation_strength": 0.0,
            "adaptation_tau": 200.0,
            "oscillation_enabled": True,
            "oscillation_frequency": 8.0,
            "geometry_input_coupling": True,
            "geometry_input_sigma": 0.2,
            "sandbox_enabled": True,
            "sandbox_physics": "stick_figure",
            "sandbox_action_coupling": "direct",
            "sandbox_sensor_noise": 0.05,
        },
    },
    "open_loop_baseline": {
        "description": "Kein Aktions-Loop, kein Ziel- oder Reward-Signal.",
        "hypothesis": "Kontrolle: Verhalten bleibt ohne kausalen Loop am Zufallsniveau.",
        "expected_success": 0.25,
        "required_features": [],
        "settings": {
            "pan_feedback_gain": 0.05,
            "action_loop_enabled": False,
            "reward_signal_enabled": False,
            "target_encoding": "none",
            "input_topology": "uniform",
            "inhibitory_fraction": 0.0,
            "neuron_threshold_variance": 0.0,
            "neuron_tau_m_variance": 0.0,
        },
    },
    "strong_feedback_only": {
        "description": "Starkes PAN-Feedback ohne Aktions- oder Reward-Loop.",
        "hypothesis": "Prueft, ob starkes Feedback allein die Dynamik differenziert.",
        "expected_success": None,
        "required_features": ["pan_feedback"],
        "settings": {
            "pan_enabled": True,
            "pan_feedback_gain": 2.0,
            "pan_feedback_nonlinearity": "tanh",
            "pan_feedback_saturation": 20.0,
            "action_loop_enabled": False,
            "reward_signal_enabled": False,
            "target_encoding": "none",
            "input_topology": "uniform",
            "inhibitory_fraction": 0.0,
        },
    },
    "differentiated_input_only": {
        "description": "Acht getrennte Eingangskanaele ohne Aktions-Loop.",
        "hypothesis": "Prueft Input-Differenzierung ohne geschlossene Kausalitaetskette.",
        "expected_success": None,
        "required_features": ["differentiated_input"],
        "settings": {
            "input_topology": "channel_partitioned",
            "input_channels": 8,
            "input_amplitude_per_channel": [8, 8, 8, 8, 4, 4, 4, 4],
            "input_frequency_per_channel": [20, 22, 24, 26, 30, 32, 34, 36],
            "input_phase_per_channel": [0, 0.25, 0.5, 0.75, 0, 0.25, 0.5, 0.75],
            "pan_feedback_gain": 0.05,
            "action_loop_enabled": False,
            "reward_signal_enabled": False,
            "target_encoding": "none",
            "inhibitory_fraction": 0.0,
        },
    },
    "minimal_closed_loop": {
        "description": "Differenzierter Input + Ziel-Cue + Aktion + Reward.",
        "hypothesis": "Prueft, ob ein minimal geschlossener Loop Lernen ueber Zufall erlaubt.",
        "expected_success": 0.5,
        "required_features": ["action_loop", "target_cue", "reward_channel"],
        "settings": {
            "neuron_model": "pan_adex_5d",
            "pan_enabled": True,
            "behavior_learning_enabled": True,
            "input_topology": "channel_partitioned",
            "input_channels": 8,
            "target_encoding": "one_hot",
            "target_cue_channel": 0,
            "target_cue_current": 30.0,
            "target_persistence": 16,
            "action_loop_enabled": True,
            "action_space_size": 4,
            "action_to_input_map": "auto",
            "action_coupling_strength": 2.0,
            "pan_feedback_gain": 1.5,
            "pan_feedback_nonlinearity": "tanh",
            "reward_signal_enabled": True,
            "reward_magnitude": 5.0,
            "reward_channel": 1,
            "inhibitory_fraction": 0.2,
            "gaba_strength": 4.0,
            "neuron_threshold_variance": 0.15,
            "neuron_tau_m_variance": 0.1,
        },
    },
    "credit_assignment": {
        "description": "Minimaler Loop plus reward-modulated eligibility traces.",
        "hypothesis": "Prueft, ob zeitliche Kreditzuweisung die Policy-Anpassung stabilisiert.",
        "expected_success": None,
        "required_features": ["action_loop", "reward_modulated_stdp"],
        "settings": {
            "closed_loop_preset": "minimal_closed_loop",
            "credit_assignment": "reward_modulated_stdp",
            "credit_window": 64,
            "eligibility_trace_tau": 200.0,
            "td_lambda": 0.9,
            "gamma_discount": 0.95,
        },
    },
    "heterogeneous_network": {
        "description": "Minimaler Loop plus E/I- und Neuronen-Heterogenitaet.",
        "hypothesis": "Prueft, ob Heterogenitaet Synchronie reduziert und Aktivitaet differenziert.",
        "expected_success": None,
        "required_features": ["heterogeneity"],
        "settings": {
            "closed_loop_preset": "minimal_closed_loop",
            "inhibitory_fraction": 0.25,
            "gaba_strength": 6.0,
            "e_i_ratio": 3.0,
            "neuron_threshold_variance": 0.3,
            "neuron_tau_m_variance": 0.2,
            "refractory_variance": 0.3,
            "delay_distribution": "lognormal",
            "delay_mean_ticks": 3.0,
            "oscillation_enabled": True,
            "oscillation_frequency": 8.0,
        },
    },
    "spatial_embodiment": {
        "description": "Heterogener Loop mit raeumlich gekoppeltem Input.",
        "hypothesis": "Prueft, ob Geometrie-Input-Kopplung messbare Embodiment-Effekte erzeugt.",
        "expected_success": None,
        "required_features": ["spatial_input", "action_loop"],
        "settings": {
            "closed_loop_preset": "heterogeneous_network",
            "input_topology": "spatial_gradient",
            "geometry_input_coupling": True,
            "geometry_input_sigma": 0.2,
            "action_to_input_map": "spatial",
        },
    },
    "full_embodiment": {
        "description": "Raeumlicher Closed Loop plus Stick-Figure-Sandbox.",
        "hypothesis": "Explorativer Gesamtsandkasten fuer sensorimotorische Kopplung.",
        "expected_success": None,
        "required_features": ["spatial_input", "action_loop", "sandbox"],
        "settings": {
            "closed_loop_preset": "spatial_embodiment",
            "sandbox_enabled": True,
            "sandbox_physics": "stick_figure",
            "sandbox_action_coupling": "direct",
            "sandbox_sensor_noise": 0.05,
        },
    },
}

CLOSED_LOOP_PRESETS.update(
    {
        "baseline_open_loop": {
            "description": "Kontrolle ohne Aktions- und Reward-Loop.",
            "hypothesis": "Ohne Closed Loop bleibt Verhalten am Zufallsniveau.",
            "expected_success": 0.25,
            "required_features": ["control"],
            "settings": {
                "action_loop_enabled": False,
                "reward_signal_enabled": False,
                "target_encoding": "none",
                "pan_feedback_gain": 0.05,
                "inhibitory_fraction": 0.0,
                "input_topology": "uniform",
                "plasticity_rule": "structural",
                "weight": 4,
                "ticks": 2000,
            },
        },
        "baseline_heterogeneous": {
            "description": "E/I-Balance und Neuronenheterogenität ohne Closed Loop.",
            "hypothesis": "Heterogenität reduziert Synchronie, erzeugt aber allein kein Lernen.",
            "expected_success": 0.25,
            "required_features": ["heterogeneity"],
            "settings": {
                "closed_loop_preset": "baseline_open_loop",
                "inhibitory_fraction": 0.25,
                "gaba_strength": 6,
                "e_i_ratio": 3,
                "neuron_threshold_variance": 0.3,
                "neuron_tau_m_variance": 0.2,
                "delay_distribution": "lognormal",
                "delay_mean_ticks": 3,
            },
        },
        "fix_weight_explosion": {
            "description": "Gewichtszerfall und hartes Maximum gegen Gewichts-Explosion.",
            "hypothesis": "Decay und Clamp halten die Gewichte im deklarierten Korridor.",
            "expected_success": None,
            "required_features": ["weight_stabilization"],
            "settings": {
                "plasticity_rule": "structural",
                "weight": 4,
                "weight_decay": 0.01,
                "weight_max_clamp": 10,
                "ticks": 2000,
                "inhibitory_fraction": 0.25,
                "pan_feedback_gain": 1.5,
            },
        },
        "fix_channel_separation": {
            "description": "Getrennte Kanäle für Ziel, Reward und Aktion.",
            "hypothesis": "Drei getrennte Signale bleiben im Netzwerk unterscheidbar.",
            "expected_success": None,
            "required_features": ["channel_separation"],
            "settings": {
                "target_cue_channel": 0,
                "reward_cue_channel": 5,
                "action_feedback_channel": 6,
                "input_channels": 8,
                "input_amplitude_per_channel": [8, 8, 8, 8, 8, 5, 5, 0],
            },
        },
        "fix_weight_and_channels": {
            "description": "Kombiniert Gewichts-Stabilisierung und Kanaltrennung.",
            "hypothesis": "Ein stabiler, differenzierter Closed Loop wird möglich.",
            "expected_success": None,
            "required_features": ["weight_stabilization", "channel_separation"],
            "settings": {
                "closed_loop_preset": "fix_weight_explosion",
                "target_cue_channel": 0,
                "reward_cue_channel": 5,
                "action_feedback_channel": 6,
                "input_channels": 8,
                "inhibitory_fraction": 0.25,
                "pan_feedback_gain": 1.5,
            },
        },
        "feedback_gain_sweep": {
            "description": "Niedrigerer PAN-Feedback-Gain mit tanh-Sättigung.",
            "hypothesis": "Ein Gain von 0.5 kann stabiler als 1.5 sein.",
            "expected_success": None,
            "required_features": ["pan_feedback"],
            "settings": {
                "pan_feedback_gain": 0.5,
                "pan_feedback_nonlinearity": "tanh",
                "pan_feedback_saturation": 20,
            },
        },
        "input_differentiation": {
            "description": "Per-Kanal-Amplituden, Frequenzen und Phasen.",
            "hypothesis": "Differenzierter Input kann neuronale Spezialisierung erzeugen.",
            "expected_success": None,
            "required_features": ["differentiated_input"],
            "settings": {
                "input_topology": "channel_partitioned",
                "input_channels": 8,
                "input_amplitude_per_channel": [8, 8, 8, 8, 4, 4, 4, 4],
                "input_frequency_per_channel": [20, 22, 24, 26, 30, 32, 34, 36],
                "input_phase_per_channel": [0, 0.25, 0.5, 0.75, 0, 0.25, 0.5, 0.75],
                "input_noise_sigma": 0.1,
            },
        },
        "credit_assignment_trace": {
            "description": "Reward-modulierte Eligibility-Traces.",
            "hypothesis": "Zeitliche Kreditzuweisung stabilisiert Policy-Anpassung.",
            "expected_success": None,
            "required_features": ["reward_modulated_stdp"],
            "settings": {
                "credit_assignment": "reward_modulated_stdp",
                "credit_window": 64,
                "eligibility_trace_tau": 200,
                "td_lambda": 0.9,
                "gamma_discount": 0.95,
            },
        },
        "reward_shaping_dense": {
            "description": "Dichter, schwächerer Reward statt Sparse-Reward.",
            "hypothesis": "Dense Reward erzeugt mehr Policy-Updates, eventuell mit weniger Stabilität.",
            "expected_success": None,
            "required_features": ["dense_reward"],
            "settings": {
                "reward_shaping": "dense",
                "reward_magnitude": 2,
                "reward_delay_ticks": 0,
            },
        },
        "d1_minimal_closed_loop": {
            "description": "Minimaler geschlossener Kreis mit Stabilisierung und Lernraten-Defaults.",
            "hypothesis": "PAN kann mit einem minimalen Loop über Zufall lernen.",
            "expected_success": 0.30,
            "required_features": ["action_loop", "target_cue", "reward_channel"],
            "settings": {
                "closed_loop_preset": "minimal_closed_loop",
                "action_loop_enabled": True,
                "action_space_size": 4,
                "target_encoding": "one_hot",
                "target_cue_channel": 0,
                "reward_signal_enabled": True,
                "reward_channel": 5,
                "posture_reward_enabled": True,
                "posture_score_channel": 2,
                "reward_event_channel": 3,
                "pan_feedback_gain": 1.5,
                "inhibitory_fraction": 0.25,
                "weight_decay": 0.01,
                "weight_max_clamp": 10,
                "behavior_learning_rate": 0.2,
                "behavior_epsilon": 0.2,
                "ticks": 2000,
            },
        },
        "d2_full_embodiment_v2": {
            "description": "Vollständiger räumlicher Closed Loop mit allen Hebeln.",
            "hypothesis": "Die kombinierte Kopplung erzeugt komplexe, aber prüfbare Dynamik.",
            "expected_success": None,
            "required_features": [
                "spatial_input",
                "action_loop",
                "sandbox",
                "reward_modulated_stdp",
            ],
            "settings": {
                "closed_loop_preset": "d1_minimal_closed_loop",
                "input_topology": "spatial_gradient",
                "geometry_input_coupling": True,
                "geometry_input_sigma": 0.2,
                "action_to_input_map": "spatial",
                "action_coupling_strength": 2,
                "credit_assignment": "reward_modulated_stdp",
                "oscillation_enabled": True,
                "oscillation_frequency": 8,
                "sandbox_enabled": True,
                "sandbox_physics": "stick_figure",
            },
        },
        "d3_spatial_embodiment_only": {
            "description": "Räumliche Kopplung ohne Ziel- oder Reward-Signal.",
            "hypothesis": "Räumliche Kopplung erzeugt Reaktivität, aber keine Zielgerichtetheit.",
            "expected_success": 0.25,
            "required_features": ["spatial_input", "action_loop"],
            "settings": {
                "input_topology": "spatial_gradient",
                "geometry_input_coupling": True,
                "geometry_input_sigma": 0.2,
                "action_to_input_map": "spatial",
                "action_loop_enabled": True,
                "reward_signal_enabled": False,
                "target_encoding": "none",
            },
        },
        "e1_diagnose_silence": {
            "description": "Diagnostikprofil für niedrige Aktivität.",
            "hypothesis": "Findet die Grenze zwischen Stille und Aktivität.",
            "expected_success": None,
            "required_features": ["diagnostic"],
            "settings": {
                "stimulus_current": 4,
                "pan_bias_current": 5,
                "weight": 4,
                "inhibitory_fraction": 0.25,
            },
        },
        "e2_diagnose_synchrony": {
            "description": "Diagnostikprofil für E/I-Synchronie.",
            "hypothesis": "Identifiziert die Inhibitionsschwelle der Synchronie.",
            "expected_success": None,
            "required_features": ["diagnostic"],
            "settings": {
                "inhibitory_fraction": 0.1,
                "gaba_strength": 3,
                "pan_feedback_gain": 0.5,
            },
        },
        "e3_diagnose_context_policy": {
            "description": "Policy-Diagnostik ohne Zielsignal.",
            "hypothesis": "Prüft Policy-Verhalten ohne Kontext-Cue.",
            "expected_success": 0.25,
            "required_features": ["diagnostic"],
            "settings": {
                "target_encoding": "none",
                "target_cue_channel": 0,
                "behavior_target_mode": "fixed",
                "behavior_target_action": 0,
            },
        },
        "f1_robustness_seed_sweep": {
            "description": "Reproduzierbarkeit mit Seed 42 und D1-Basis.",
            "hypothesis": "Die Erfolgsrate bleibt über Seeds vergleichbar.",
            "expected_success": None,
            "required_features": ["seed_sweep"],
            "settings": {"closed_loop_preset": "d1_minimal_closed_loop", "seed": 42},
        },
        "f2_robustness_scale_up": {
            "description": "Skalierung auf 512 Neuronen.",
            "hypothesis": "Mehr Neuronen verbessern Lernen nicht automatisch.",
            "expected_success": None,
            "required_features": ["scale_up"],
            "settings": {
                "closed_loop_preset": "d1_minimal_closed_loop",
                "n_neurons": 512,
                "edge_budget": 4096,
                "k_neighbors": 16,
            },
        },
        "f3_robustness_ablation": {
            "description": "Ablationsbasis mit deaktiviertem Feedback.",
            "hypothesis": "Ein kritischer Hebel fehlt und reduziert Lernen.",
            "expected_success": 0.25,
            "required_features": ["ablation"],
            "settings": {
                "closed_loop_preset": "d1_minimal_closed_loop",
                "pan_feedback_gain": 0.05,
            },
        },
        "g1_two_action_simple": {
            "description": "Minimale Zwei-Aktionen-Lernaufgabe.",
            "hypothesis": "Ein fixes Ziel mit zwei Aktionen sollte schnell lernbar sein.",
            "expected_success": 0.9,
            "required_features": ["sanity_check"],
            "settings": {
                "closed_loop_preset": "d1_minimal_closed_loop",
                "behavior_action_count": 2,
                "action_space_size": 2,
                "behavior_target_mode": "fixed",
                "behavior_target_action": 0,
                "behavior_epsilon": 0.1,
                "behavior_learning_rate": 0.3,
            },
        },
        "g2_one_action_trivial": {
            "description": "Trivialer Ein-Aktions-Sanity-Check.",
            "hypothesis": "Die einzige mögliche Aktion muss ab Episode 1 erfolgreich sein.",
            "expected_success": 1.0,
            "required_features": ["sanity_check"],
            "settings": {
                "closed_loop_preset": "d1_minimal_closed_loop",
                "behavior_action_count": 1,
                "action_space_size": 1,
                "behavior_target_mode": "fixed",
                "behavior_target_action": 0,
                "behavior_epsilon": 0.0,
            },
        },
        "g3_gaba_sweep": {
            "description": "E/I-Stärkeprofil für GABA-Sweep.",
            "hypothesis": "Eine mittlere GABA-Stärke balanciert Aktivität und Synchronie.",
            "expected_success": None,
            "required_features": ["gaba_sweep"],
            "settings": {"inhibitory_fraction": 0.25, "gaba_strength": 2},
        },
        "g4_feedback_nonlinearity": {
            "description": "Vergleich der Feedback-Nichtlinearität.",
            "hypothesis": "Die Form der Rückkopplung verändert Stabilität und Lernen.",
            "expected_success": None,
            "required_features": ["feedback_sweep"],
            "settings": {"pan_feedback_nonlinearity": "linear"},
        },
    }
)


CLOSED_LOOP_PRESETS["pan_cuda_hybrid"] = {
    "label": "PAN · CUDA-Hybrid",
    "description": "PAN-Vollprofil mit CUDA-Membran, PAN-Zustand/Feedback, synaptischer Aussendung und Reward-Updates. Körper, Policy, RNG und Neuron-Traces bleiben CPU; die Delay-Queue liegt auf der GPU. NVIDIA-Treiber und NVRTC erforderlich; kein Speedup-Versprechen.",
    "hypothesis": "Explorativer hybrider CPU/GPU-Vergleich mit denselben PAN-Parametern und expliziter Komponentenanzeige.",
    "expected_success": None,
    "required_features": ["pan", "cuda_driver", "nvrtc", "sandbox", "neural_io"],
    "settings": {
        "closed_loop_preset": "pan_full_balanced",
        "name": "pan_cuda_hybrid",
        "neuron_backend": "cuda_pan",
    },
}


def closed_loop_catalog() -> dict[str, object]:
    """Return UI-safe closed-loop capabilities and preset metadata."""

    presets = []
    for name, item in CLOSED_LOOP_PRESETS.items():
        features = cast(list[str], item["required_features"])
        settings = cast(dict[str, object], item["settings"])
        presets.append(
            {
                "name": name,
                "label": item.get("label", name),
                "description": item["description"],
                "hypothesis": item["hypothesis"],
                "expected_success": item["expected_success"],
                "required_features": list(features),
                "settings": dict(settings),
            }
        )
    return {
        "classification": "PLAYGROUND_CLOSED_LOOP",
        "scientific_evidence": False,
        "runtime_status": "IMPLEMENTED_BOUNDED_REFERENCE",
        "input_topologies": [
            "uniform",
            "channel_partitioned",
            "spatial_gradient",
            "random_per_neuron",
        ],
        "feedback_sources": ["population", "layer", "subset", "hypervector"],
        "feedback_targets": ["all", "layer", "random_subset"],
        "feedback_nonlinearities": ["linear", "tanh", "sign", "clip"],
        "target_encodings": ["none", "one_hot", "rate", "population_latency"],
        "target_predictability": ["deterministic", "stochastic", "adversarial"],
        "reward_shaping": ["sparse", "dense", "potential_based"],
        "credit_assignment": ["none", "trace", "reward_modulated_stdp"],
        "delay_distributions": ["fixed", "uniform", "lognormal", "gamma"],
        "presets": presets,
        "note": (
            "Closed-loop behavior is Playground-only. Preset expectations are "
            "hypotheses, not observed results or evidence."
        ),
    }


def _expand(values: Sequence[float], count: int, default: float) -> list[float]:
    clean = [float(value) for value in values]
    if not clean:
        return [default for _ in range(count)]
    return [clean[index % len(clean)] for index in range(count)]


class ClosedLoopRuntime:
    """Deterministic channelized action/consequence/reward environment."""

    def __init__(
        self,
        config: PlaygroundConfig,
        coordinates: Sequence[Sequence[float]],
    ) -> None:
        self.config = config
        self.n_neurons = config.n_neurons
        self.channels = config.input_channels
        self.coordinates = coordinates
        self.rng = random.Random(config.seed ^ 0xC105ED)
        self.channel_map = self._build_channel_map()
        self.amplitudes = _expand(
            config.input_amplitude_per_channel,
            self.channels,
            0.0,
        )
        self.frequencies = _expand(
            config.input_frequency_per_channel,
            self.channels,
            20.0,
        )
        self.phases = _expand(
            config.input_phase_per_channel,
            self.channels,
            0.0,
        )
        self.action_history: list[int] = []
        self.target_history: list[int] = []
        self.reward_history: list[float] = []
        self.successes = 0
        self.pending_actions: list[tuple[int, int, int]] = []
        self.pending_rewards: list[tuple[int, float, int, int]] = []
        self.delivered_rewards: list[tuple[int, int, float]] = []
        self.reward_trace = 0.0
        self.last_action: int | None = None
        self.observed_context: str | None = None
        self.previous_action: int | None = None
        self.target_permutation = list(range(config.action_space_size))
        if config.target_shuffle:
            self.rng.shuffle(self.target_permutation)

    def _build_channel_map(self) -> list[list[int]]:
        provided = self.config.input_channel_map
        if provided:
            return [list(group) for group in provided]

        groups: list[list[int]] = [[] for _ in range(self.channels)]
        if self.config.input_topology == "uniform":
            all_neurons = list(range(self.n_neurons))
            return [list(all_neurons) for _ in range(self.channels)]

        if (
            self.config.input_topology == "spatial_gradient"
            or self.config.geometry_input_coupling
        ) and self.coordinates:
            ordered = sorted(
                range(self.n_neurons),
                key=lambda index: (
                    float(self.coordinates[index][0])
                    if self.coordinates[index]
                    else 0.0
                ),
            )
        elif self.config.input_topology == "random_per_neuron":
            ordered = list(range(self.n_neurons))
            self.rng.shuffle(ordered)
        else:
            ordered = list(range(self.n_neurons))

        for position, neuron_id in enumerate(ordered):
            channel = min(
                self.channels - 1,
                (position * self.channels) // max(self.n_neurons, 1),
            )
            if self.config.input_topology == "random_per_neuron":
                channel = self.rng.randrange(self.channels)
            groups[channel].append(neuron_id)
        return groups

    def _target_for_episode(self, episode: int) -> int:
        count = self.config.action_space_size
        if self.config.behavior_target_mode == "fixed":
            return self.config.behavior_target_action
        mode = self.config.target_predictability
        if mode == "stochastic":
            target_rng = random.Random(self.config.seed ^ 0x7A267 ^ episode)
            target = target_rng.randrange(count)
        elif mode == "adversarial":
            target = (
                (self.last_action + 1) % count
                if self.last_action is not None
                else episode % count
            )
        else:
            target = episode % count
        if self.target_permutation:
            target = self.target_permutation[target % len(self.target_permutation)]
        return target

    def current_target(self, tick: int) -> int:
        episode_ticks = max(1, self.config.behavior_episode_ticks)
        episode = tick // episode_ticks
        return self._target_for_episode(episode)

    def _target_channel_values(self, tick: int) -> list[float]:
        values = [0.0 for _ in range(self.channels)]
        if (
            self.config.target_encoding == "none"
            or self.config.target_cue_control == "absent"
        ):
            return values
        episode_ticks = max(1, self.config.behavior_episode_ticks)
        phase_tick = tick % episode_ticks
        if phase_tick >= self.config.target_persistence:
            return values
        target = self.current_target(tick)
        if self.config.target_cue_control == "randomized":
            # Separate RNG stream: changes the emitted cue, never the evaluator target.
            cue_rng = random.Random(
                self.config.seed ^ 0xC0E123 ^ (tick // episode_ticks)
            )
            target = cue_rng.randrange(self.config.action_space_size)
        base = self.config.target_cue_channel % self.channels
        if self.config.target_encoding == "one_hot":
            channel = (base + target) % self.channels
            values[channel] = self.config.target_cue_current
        elif self.config.target_encoding == "rate":
            values[base] = self.config.target_cue_current * (
                (target + 1) / max(self.config.action_space_size, 1)
            )
        else:
            latency = target % max(1, self.config.target_persistence)
            if phase_tick == latency:
                values[base] = self.config.target_cue_current
        return values

    def _action_vector(self, action: int) -> list[float]:
        mapping = self.config.action_to_input_map
        if not isinstance(mapping, str) and mapping:
            rows = cast(Sequence[Sequence[float]], mapping)
            row = rows[action % len(rows)]
            return _expand(row, self.channels, 0.0)

        values = [0.0 for _ in range(self.channels)]
        base = self.config.action_feedback_channel % self.channels
        if mapping == "spatial":
            center = (action / max(self.config.action_space_size - 1, 1)) * max(
                self.channels - 1, 1
            )
            sigma = max(self.config.geometry_input_sigma * self.channels, 0.5)
            for channel in range(self.channels):
                distance = (channel - center) / sigma
                values[channel] = math.exp(-0.5 * distance * distance)
        else:
            values[(base + action) % self.channels] = 1.0
        return values

    def _channel_values(self, tick: int) -> list[float]:
        time_s = tick * self.config.dt_ms / 1000.0
        values = []
        for channel in range(self.channels):
            phase = self.phases[channel]
            angle = 2.0 * math.pi * self.frequencies[channel] * time_s + phase
            carrier = 0.5 + 0.5 * math.sin(angle)
            values.append(self.amplitudes[channel] * carrier)

        target_values = self._target_channel_values(tick)
        # The policy only sees an emitted cue, never the evaluator's target.
        # Remember a transient cue within its episode, and forget it at reset.
        if tick % max(1, self.config.behavior_episode_ticks) == 0:
            self.observed_context = None
        if any(value != 0.0 for value in target_values):
            phase = tick % max(1, self.config.behavior_episode_ticks)
            signature = ",".join(format(value, ".12g") for value in target_values)
            suffix = (
                f":at:{phase}"
                if self.config.target_encoding == "population_latency"
                else ""
            )
            self.observed_context = (
                f"cue:{self.config.target_encoding}:{signature}{suffix}"
            )
        for channel in range(self.channels):
            values[channel] += target_values[channel]

        active_actions: list[tuple[int, int, int]] = []
        for start, end, action in self.pending_actions:
            if start <= tick < end:
                vector = self._action_vector(action)
                for channel in range(self.channels):
                    noise = (
                        self.rng.gauss(0.0, self.config.action_noise)
                        if self.config.action_noise > 0.0
                        else 0.0
                    )
                    values[channel] += self.config.action_coupling_strength * (
                        vector[channel] + noise
                    )
            if tick < end:
                active_actions.append((start, end, action))
        self.pending_actions = active_actions

        remaining_rewards: list[tuple[int, float, int, int]] = []
        for reward_tick, reward, action, target in self.pending_rewards:
            if reward_tick <= tick:
                self.reward_trace += reward
                self.delivered_rewards.append((action, target, reward))
            else:
                remaining_rewards.append((reward_tick, reward, action, target))
        self.pending_rewards = remaining_rewards

        if self.config.reward_signal_enabled and abs(self.reward_trace) > 1e-12:
            channel = self.config.reward_channel % self.channels
            values[channel] += self.reward_trace
        self.reward_trace *= self.config.reward_decay
        if abs(self.reward_trace) < 1e-9:
            self.reward_trace = 0.0
        return values

    def currents(self, tick: int) -> list[float]:
        values = self._channel_values(tick)
        currents = [0.0 for _ in range(self.n_neurons)]
        counts = [0 for _ in range(self.n_neurons)]
        for channel, neurons in enumerate(self.channel_map):
            for neuron_id in neurons:
                if 0 <= neuron_id < self.n_neurons:
                    currents[neuron_id] += values[channel]
                    counts[neuron_id] += 1
        for neuron_id in range(self.n_neurons):
            if counts[neuron_id] > 1:
                currents[neuron_id] /= counts[neuron_id]
            noise_sigma = self.config.input_noise_sigma
            if self.config.sandbox_enabled:
                noise_sigma = min(
                    1.0,
                    noise_sigma + self.config.sandbox_sensor_noise,
                )
            if noise_sigma > 0.0:
                currents[neuron_id] += self.rng.gauss(0.0, noise_sigma)
        return currents

    def _reward(self, action: int, target: int) -> float:
        magnitude = self.config.reward_magnitude
        shaping = self.config.reward_shaping
        match = action == target
        if shaping == "dense":
            distance = abs(action - target) / max(
                self.config.action_space_size - 1,
                1,
            )
            reward = magnitude * (1.0 - 2.0 * distance)
        elif shaping == "potential_based":
            current_distance = abs(action - target)
            if self.previous_action is None:
                previous_distance = self.config.action_space_size - 1
            else:
                previous_distance = abs(self.previous_action - target)
            reward = (
                magnitude
                * (previous_distance - current_distance)
                / max(
                    self.config.action_space_size - 1,
                    1,
                )
            )
            if match:
                reward += magnitude
        else:
            reward = magnitude if match else 0.0
        return reward - self.config.reward_baseline

    def note_action(self, *, action: int, tick: int) -> tuple[int, float]:
        target = self.current_target(tick)
        episode_index = len(self.action_history)
        reward = self._reward(action, target)
        if self.config.freeze_rewards:
            reward = self.config.frozen_reward_sequence[episode_index]
        if action == target:
            self.successes += 1
        self.previous_action = self.last_action
        self.last_action = action
        self.action_history.append(action)
        self.target_history.append(target)
        self.reward_history.append(reward)

        if self.config.action_loop_enabled:
            start = tick + self.config.action_loop_delay
            end = start + self.config.action_persistence
            self.pending_actions.append((start, end, action))
        if self.config.reward_signal_enabled:
            reward_tick = tick + self.config.reward_delay_ticks
            if self.config.reward_delay_ticks == 0:
                self.reward_trace += reward
                self.delivered_rewards.append((action, target, reward))
            else:
                self.pending_rewards.append((reward_tick, reward, action, target))
        return target, reward

    def consume_delivered_rewards(self) -> list[tuple[int, int, float]]:
        rewards = list(self.delivered_rewards)
        self.delivered_rewards.clear()
        return rewards

    def summary(self) -> dict[str, object]:
        episodes = len(self.action_history)
        if self.config.freeze_actions and self.config.freeze_rewards:
            parity_mode = "FROZEN_ACTIONS_AND_REWARDS"
        elif self.config.freeze_actions:
            parity_mode = "FROZEN_ACTIONS"
        elif self.config.freeze_rewards:
            parity_mode = "FROZEN_REWARDS"
        else:
            parity_mode = "LIVE_CLOSED_LOOP"
        return {
            "classification": "PLAYGROUND_CLOSED_LOOP",
            "scientific_evidence": False,
            "preset": self.config.closed_loop_preset,
            "input_topology": self.config.input_topology,
            "input_channels": self.channels,
            "channel_sizes": [len(group) for group in self.channel_map],
            "action_loop_enabled": self.config.action_loop_enabled,
            "action_space_size": self.config.action_space_size,
            "freeze_actions": self.config.freeze_actions,
            "freeze_rewards": self.config.freeze_rewards,
            "parity_reference_source": self.config.parity_reference_source,
            "parity_reference_commit": self.config.parity_reference_commit,
            "target_encoding": self.config.target_encoding,
            "policy_context_source": "emitted_target_cue_within_episode",
            "observed_context": self.observed_context,
            "reward_signal_enabled": self.config.reward_signal_enabled,
            "reward_shaping": self.config.reward_shaping,
            "credit_assignment": self.config.credit_assignment,
            "episodes": episodes,
            "successes": self.successes,
            "success_fraction": self.successes / episodes if episodes else 0.0,
            "action_history": list(self.action_history[-128:]),
            "target_history": list(self.target_history[-128:]),
            "reward_history": list(self.reward_history[-128:]),
            "pending_action_effects": len(self.pending_actions),
            "pending_rewards": len(self.pending_rewards),
            "causal_chain": "target/input -> network -> action -> delayed input/reward",
            "parity_mode": parity_mode,
        }


def neuron_parameter_sets(
    base: Mapping[str, float],
    config: PlaygroundConfig,
) -> list[dict[str, float]]:
    """Create deterministic per-neuron threshold/tau variation."""

    rng = random.Random(config.seed ^ 0x4E455552)
    result: list[dict[str, float]] = []
    for _ in range(config.n_neurons):
        params = {key: float(value) for key, value in base.items()}
        if "threshold" in params and config.neuron_threshold_variance > 0.0:
            sigma = max(1.0, abs(params["threshold"]) * 0.1)
            params["threshold"] += rng.gauss(
                0.0,
                sigma * config.neuron_threshold_variance,
            )
        if config.neuron_tau_m_variance > 0.0:
            factor = max(
                0.1,
                1.0 + rng.gauss(0.0, config.neuron_tau_m_variance),
            )
            for key in ("tau_m_ms", "soma_tau_ms", "dendrite_tau_ms"):
                if key in params:
                    params[key] = max(0.05, params[key] * factor)
        result.append(params)
    return result


def inhibitory_mask(
    n_neurons: int,
    fraction: float,
    seed: int,
) -> list[bool]:
    rng = random.Random(seed ^ 0x1A11B17)
    order = list(range(n_neurons))
    rng.shuffle(order)
    count = int(round(n_neurons * fraction))
    selected = set(order[:count])
    return [index in selected for index in range(n_neurons)]


def sample_delay_ticks(
    config: PlaygroundConfig,
    rng: random.Random,
) -> int:
    """Sample one bounded synaptic delay according to the configured family."""

    mode = config.delay_distribution
    mean = max(1.0, config.delay_mean_ticks)
    if mode == "uniform":
        value = rng.uniform(1.0, max(1.0, 2.0 * mean - 1.0))
    elif mode == "lognormal":
        sigma = 0.5
        mu = math.log(mean) - 0.5 * sigma * sigma
        value = rng.lognormvariate(mu, sigma)
    elif mode == "gamma":
        value = rng.gammavariate(2.0, mean / 2.0)
    else:
        value = float(config.delay_ticks)
    return max(1, min(64, int(round(value))))


class TemporalDynamics:
    """Small deterministic refractory/adaptation/oscillation reference."""

    def __init__(self, config: PlaygroundConfig) -> None:
        self.config = config
        self.rng = random.Random(config.seed ^ 0x71AE)
        self.refractory_until = [-1 for _ in range(config.n_neurons)]
        self.adaptation = [0.0 for _ in range(config.n_neurons)]
        self.refractory_ticks = []
        for _ in range(config.n_neurons):
            jitter = self.rng.gauss(0.0, config.refractory_variance)
            self.refractory_ticks.append(max(1, int(round(1.0 + 2.0 * jitter))))

    def begin_tick(self) -> None:
        if self.config.adaptation_strength <= 0.0:
            return
        decay = math.exp(-self.config.dt_ms / max(self.config.adaptation_tau, 1e-6))
        self.adaptation = [value * decay for value in self.adaptation]

    def can_step(self, neuron_id: int, tick: int) -> bool:
        return tick > self.refractory_until[neuron_id]

    def current_adjustment(self, neuron_id: int, tick: int) -> float:
        current = -self.config.adaptation_strength * self.adaptation[neuron_id]
        if self.config.oscillation_enabled:
            time_s = tick * self.config.dt_ms / 1000.0
            current += math.sin(
                2.0 * math.pi * self.config.oscillation_frequency * time_s
            )
        return current

    def note_spikes(self, spiked_neurons: Sequence[int], tick: int) -> None:
        for neuron_id in spiked_neurons:
            self.refractory_until[neuron_id] = tick + self.refractory_ticks[neuron_id]
            self.adaptation[neuron_id] += 1.0

    def summary(self) -> dict[str, object]:
        return {
            "classification": "PLAYGROUND_TEMPORAL_DYNAMICS",
            "scientific_evidence": False,
            "refractory_variance": self.config.refractory_variance,
            "adaptation_strength": self.config.adaptation_strength,
            "adaptation_tau_ms": self.config.adaptation_tau,
            "oscillation_enabled": self.config.oscillation_enabled,
            "oscillation_frequency_hz": self.config.oscillation_frequency,
            "mean_refractory_ticks": sum(self.refractory_ticks)
            / max(len(self.refractory_ticks), 1),
        }
