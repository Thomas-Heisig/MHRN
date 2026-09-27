"""Bounded deterministic exploratory simulation session."""

from __future__ import annotations

import datetime as dt
import math
import random
import time
import uuid
from dataclasses import dataclass

from .._isolation import PlaygroundIsolation, playground_manifest
from ..analysis import analyze_result
from ..geometry.metrics import conduction_delay_ticks, geometry_diagnostics
from ..instruments.monitors import RateMonitor, SpikeMonitor, StateMonitor
from ..models import PlaygroundConfig, Topology
from ..neural_io import NeuralIOInterface
from ..pan import (
    BehavioralLearningEngine,
    CorticalOrganization,
    CUDAMemoryPool,
    DualModeScheduler,
    GrowthEngine,
    ModeSwitcher,
    PANRuntime,
    SSDOffloader,
    ThalamicGating,
    hardware_profile,
    settings_to_gates,
)
from ..persist.session_recorder import record_session
from ..registry.neuron_models import NeuronModelSpec, get_neuron_model
from ..registry.plasticity_rules import require_plasticity_rule
from ..registry.readouts import apply_readout
from ..registry.stimulus_generators import build_stimulus
from ..registry.synapse_models import require_synapse_model
from ..registry.topology_generators import build_topology


@dataclass(slots=True)
class PlaygroundSession:
    """One isolated exploratory simulation with in-memory instrumentation."""

    config: PlaygroundConfig

    def _prepare(self) -> tuple[NeuronModelSpec, Topology]:
        model = get_neuron_model(self.config.neuron_model)
        require_synapse_model(self.config.synapse_model)
        require_plasticity_rule(self.config.plasticity_rule)
        topology = build_topology(
            self.config.topology,
            self.config.n_neurons,
            self.config.edge_budget,
            self.config.seed,
            dimensions=self.config.dimensions,
            radius=self.config.radius,
            k_neighbors=self.config.k_neighbors,
            rewiring_probability=self.config.rewiring_probability,
            modules=self.config.modules,
            geometry_lambda_a=self.config.geometry_lambda_a,
            geometry_lambda_b=self.config.geometry_lambda_b,
            geometry_sigma=self.config.geometry_sigma,
            geometry_p0=self.config.geometry_p0,
            geometry_mode=self.config.geometry_mode,
        )
        if not model.supports_dimensions(topology.dimensions):
            raise ValueError(
                f"{model.name} does not declare compatibility with "
                f"{topology.dimensions}D playground coordinates"
            )
        return model, topology

    def run(self) -> dict[str, object]:
        started = time.perf_counter()
        model, topology = self._prepare()
        config = self.config
        rng = random.Random(config.seed ^ 0xB5D)
        stimulus = build_stimulus(
            config.stimulus,
            config.n_neurons,
            config.stimulus_current,
            config.stimulus_rate_hz,
            config.dt_ms,
            config.seed,
        )

        states = [
            model.state_factory(model.parameters) for _ in range(config.n_neurons)
        ]
        adjacency: list[set[int]] = [set() for _ in range(config.n_neurons)]
        incoming: list[set[int]] = [set() for _ in range(config.n_neurons)]
        weights: dict[tuple[int, int], float] = {}
        delays: dict[tuple[int, int], int] = {}
        eligibility: dict[tuple[int, int], float] = {}
        release_state: dict[tuple[int, int], float] = {}
        for source, target in topology.edges:
            adjacency[source].add(target)
            incoming[target].add(source)
            edge = (source, target)
            weights[edge] = config.weight
            delays[edge] = (
                conduction_delay_ticks(
                    topology.coordinates[source],
                    topology.coordinates[target],
                    velocity_per_tick=config.geometry_delay_velocity,
                )
                if topology.name == "geometric_5d"
                else config.delay_ticks
            )
            eligibility[edge] = 0.0
            release_state[edge] = 1.0

        neural_io: NeuralIOInterface | None = None
        if config.neural_io_enabled:
            correlation_id = (
                ""
                if config.neural_io_correlation_id == "auto"
                else config.neural_io_correlation_id
            )
            neural_io = NeuralIOInterface(
                n_neurons=config.n_neurons,
                input_channels=config.neural_io_input_channels,
                output_channels=config.neural_io_output_channels,
                input_codec=config.neural_io_input_codec,
                output_decoder=config.neural_io_output_decoder,
                input_payload=config.neural_io_input_payload,
                window_ticks=config.neural_io_window_ticks,
                input_current=config.neural_io_input_current,
                ticks=config.ticks,
                dt_ms=config.dt_ms,
                seed=config.seed,
                input_role=config.neural_io_input_role,
                output_role=config.neural_io_output_role,
                initial_phase=config.neural_io_phase,
                correlation_id=correlation_id,
                modality=config.neural_io_modality,
                source_id=config.neural_io_source_id,
            )

        gate_schematic = settings_to_gates(config)
        dual_scheduler: DualModeScheduler | None = None
        if config.clock_mode == "dual":
            dual_scheduler = DualModeScheduler(
                dt_ms=config.dt_ms,
                base_hz=config.clock_base_hz,
                event_batch_ms=config.clock_event_batch_ms,
            )

        pan_runtime: PANRuntime | None = None
        if config.pan_enabled or config.neuron_model == "pan_adex_5d":
            degree = [
                len(adjacency[index]) + len(incoming[index])
                for index in range(config.n_neurons)
            ]
            pan_runtime = PANRuntime(
                n_neurons=config.n_neurons,
                dimensions=config.pan_dimensions,
                seed=config.seed,
                feedback_gain=config.pan_feedback_gain,
                health_decay=config.pan_health_decay,
                apoptosis_threshold=config.pan_apoptosis_threshold,
                closed_loop=config.pan_closed_loop,
                coordinates=topology.coordinates,
                degree=degree,
            )
            pan_runtime.initialize(states)

        growth_engine: GrowthEngine | None = None
        if config.growth_enabled:
            growth_engine = GrowthEngine(
                n_neurons=config.n_neurons,
                edge_budget=config.edge_budget,
                max_synapses_per_neuron=config.growth_max_synapses_per_neuron,
                max_new_synapses_per_barrier=(
                    config.growth_max_new_synapses_per_barrier
                ),
                activity_threshold=config.growth_activity_threshold,
                coactivation_threshold=config.growth_coactivation_threshold,
                information_threshold=config.growth_information_threshold,
                prune_threshold=config.growth_prune_threshold,
                neurogenesis=config.growth_neurogenesis,
                synaptogenesis=config.growth_synaptogenesis,
                path_formation=config.growth_path_formation,
                pruning=config.growth_pruning,
            )

        thalamic_gate: ThalamicGating | None = None
        if config.thalamic_gating_enabled:
            thalamic_gate = ThalamicGating(
                n_neurons=config.n_neurons,
                relay_threshold=config.thalamic_relay_threshold,
                attention_gain=config.thalamic_attention_gain,
                inhibition_gain=config.thalamic_inhibition_gain,
            )

        cortical_org: CorticalOrganization | None = None
        if config.cortical_layers_enabled:
            cortical_org = CorticalOrganization(
                n_neurons=config.n_neurons,
                layers=config.cortical_layer_count,
                plasticity=config.cortical_plasticity,
                learning_rate=config.cortical_learning_rate,
            )

        behavior_engine: BehavioralLearningEngine | None = None
        if config.behavior_learning_enabled:
            behavior_engine = BehavioralLearningEngine(
                n_neurons=config.n_neurons,
                action_count=config.behavior_action_count,
                learning_rate=config.behavior_learning_rate,
                epsilon=config.behavior_epsilon,
                target_action=config.behavior_target_action,
                target_mode=config.behavior_target_mode,
                min_activity=config.behavior_min_activity,
                episode_ticks=config.behavior_episode_ticks,
                bias_current=config.behavior_bias_current,
                seed=config.seed,
                output_neurons=(
                    cortical_org.output_layer_neurons()
                    if cortical_org is not None
                    else None
                ),
            )

        execution_switcher = ModeSwitcher(
            mode=config.execution_mode,
            initial_mode=config.execution_initial_mode,
            theta_high=config.execution_theta_high,
            theta_low=config.execution_theta_low,
            hysteresis=config.execution_hysteresis,
            min_dwell=config.execution_min_dwell,
            activity_window=config.execution_activity_window,
            transition_mode=config.execution_transition_mode,
            sync_on_switch=config.execution_sync_on_switch,
            log_transitions=config.execution_log_transitions,
            log_state_hash=config.execution_log_state_hash,
        )

        selected_hardware_profile = hardware_profile(config.hardware_profile_name)
        memory_pool = CUDAMemoryPool(max_mb=config.cuda_budget_mb)
        memory_estimate = memory_pool.estimate(
            neurons=config.n_neurons,
            synapses=config.edge_budget,
            state_dimensions=config.pan_dimensions,
        )
        offloader = SSDOffloader(
            enabled=config.offload_enabled,
            run_key=f"{config.name}-{config.seed}",
            snapshot_interval=config.offload_snapshot_interval,
        )

        initial_edge_count = len(weights)
        structural_added = 0
        structural_removed = 0
        queue_size = 65
        pending = [[0.0 for _ in range(config.n_neurons)] for _ in range(queue_size)]
        last_spike = [-10_000_000 for _ in range(config.n_neurons)]
        pre_trace = [0.0 for _ in range(config.n_neurons)]
        post_trace = [0.0 for _ in range(config.n_neurons)]
        spike_monitor = SpikeMonitor()
        rate_monitor = RateMonitor.create(config.n_neurons)
        state_monitor = StateMonitor()
        state_stride = max(1, math.ceil(config.ticks / 128))
        tick_spike_counts: list[int] = []
        previous_spikes: list[int] = []

        with PlaygroundIsolation():
            for tick in range(config.ticks):
                next_engine, switch_reason = execution_switcher.decide(tick)
                if (
                    switch_reason is not None
                    and next_engine != execution_switcher.current_engine
                ):
                    execution_switcher.transition(
                        tick=tick,
                        new_engine=next_engine,
                        reason=switch_reason,
                        states=states,
                        pending=pending,
                    )
                execution_switcher.note_tick()
                if dual_scheduler is not None:
                    dual_scheduler.begin_continuous_step()
                slot = tick % queue_size
                synaptic = pending[slot]
                pending[slot] = [0.0 for _ in range(config.n_neurons)]
                external = stimulus(tick)
                if config.neuron_model == "pan_adex_5d":
                    external = [value + config.pan_bias_current for value in external]
                if neural_io is not None:
                    io_current = neural_io.currents_for_tick(tick)
                    external = [
                        external[index] + io_current[index]
                        for index in range(config.n_neurons)
                    ]
                if thalamic_gate is not None:
                    external = thalamic_gate.apply(external, previous_spikes)
                if cortical_org is not None:
                    external = cortical_org.apply(external)
                if behavior_engine is not None:
                    behavior_bias = behavior_engine.bias_currents()
                    external = [
                        external[index] + behavior_bias[index]
                        for index in range(config.n_neurons)
                    ]
                feedback = (
                    pan_runtime.feedback_currents()
                    if pan_runtime is not None
                    else [0.0 for _ in range(config.n_neurons)]
                )
                spiked_this_tick: list[int] = []
                if execution_switcher.current_engine == "EVENT_ONLY":
                    active_neurons_for_step = [
                        index
                        for index in range(config.n_neurons)
                        if abs(external[index])
                        + abs(synaptic[index])
                        + abs(feedback[index])
                        > 1e-12
                    ]
                else:
                    active_neurons_for_step = list(range(config.n_neurons))

                for neuron_id in active_neurons_for_step:
                    state = states[neuron_id]
                    if pan_runtime is not None and not bool(
                        state.get("pan_alive", True)
                    ):
                        continue
                    current = (
                        external[neuron_id] + synaptic[neuron_id] + feedback[neuron_id]
                    )
                    if model.step(state, current, config.dt_ms, model.parameters):
                        spiked_this_tick.append(neuron_id)
                        spike_monitor.record(tick, neuron_id)
                        rate_monitor.record(neuron_id)

                for neuron_id in range(config.n_neurons):
                    pre_trace[neuron_id] *= 0.95
                    post_trace[neuron_id] *= 0.95
                for edge in list(eligibility):
                    eligibility[edge] *= 0.97

                plasticity = config.plasticity_rule
                synapse_mode = config.synapse_model
                pair_stdp = (
                    plasticity == "stdp"
                    or synapse_mode == "stdp"
                    or synapse_mode == "pan_stp_stdp"
                )
                triplet = plasticity == "triplet_stdp" or synapse_mode == "triplet_stdp"

                learning_scale = 1.0
                if plasticity == "metaplasticity":
                    elapsed_s = max((tick + 1) * config.dt_ms / 1000.0, 1e-9)
                    rate = sum(rate_monitor.counts) / config.n_neurons / elapsed_s
                    learning_scale = max(0.25, min(2.0, 10.0 / max(rate, 1.0)))

                for neuron_id in spiked_this_tick:
                    if pair_stdp or plasticity == "metaplasticity":
                        for target in list(adjacency[neuron_id]):
                            edge = (neuron_id, target)
                            delta = tick - last_spike[target]
                            if 0 < delta <= 20:
                                weights[edge] = max(
                                    0.0,
                                    weights[edge] - 0.08 * learning_scale,
                                )
                        for source in list(incoming[neuron_id]):
                            edge = (source, neuron_id)
                            delta = tick - last_spike[source]
                            if 0 < delta <= 20:
                                weights[edge] = min(
                                    100.0,
                                    weights[edge] + 0.1 * learning_scale,
                                )

                    if triplet:
                        for source in list(incoming[neuron_id]):
                            edge = (source, neuron_id)
                            weights[edge] = min(
                                100.0,
                                max(
                                    0.0,
                                    weights[edge]
                                    + 0.06 * pre_trace[source]
                                    + 0.025 * post_trace[neuron_id],
                                ),
                            )
                        for target in list(adjacency[neuron_id]):
                            edge = (neuron_id, target)
                            weights[edge] = max(
                                0.0,
                                weights[edge] - 0.04 * post_trace[target],
                            )

                    if plasticity in {
                        "eligibility_trace",
                        "three_factor",
                    } or synapse_mode in {
                        "eligibility_trace",
                        "three_factor",
                    }:
                        for source in list(incoming[neuron_id]):
                            eligibility[(source, neuron_id)] += 1.0
                        for target in list(adjacency[neuron_id]):
                            eligibility[(neuron_id, target)] -= 0.5

                    pre_trace[neuron_id] += 1.0
                    post_trace[neuron_id] += 1.0

                if plasticity == "three_factor" or synapse_mode == "three_factor":
                    modulator = math.sin(2.0 * math.pi * tick / 64.0)
                    for edge in list(weights):
                        weights[edge] = min(
                            100.0,
                            max(
                                0.0,
                                weights[edge] + 0.015 * eligibility[edge] * modulator,
                            ),
                        )

                if (
                    plasticity == "eligibility_trace"
                    or synapse_mode == "eligibility_trace"
                ):
                    for edge in list(weights):
                        weights[edge] = min(
                            100.0,
                            max(0.0, weights[edge] + 0.003 * eligibility[edge]),
                        )

                if plasticity == "homeostatic" and tick > 0 and tick % 64 == 0:
                    elapsed_s = max((tick + 1) * config.dt_ms / 1000.0, 1e-9)
                    mean_rate = sum(rate_monitor.counts) / config.n_neurons / elapsed_s
                    factor = max(
                        0.95,
                        min(1.05, 1.0 + (8.0 - mean_rate) * 0.002),
                    )
                    for edge in list(weights):
                        weights[edge] = max(
                            0.0,
                            min(100.0, weights[edge] * factor),
                        )

                if (
                    plasticity == "structural"
                    and tick > 0
                    and tick % 64 == 0
                    and weights
                ):
                    weakest = min(weights, key=weights.__getitem__)
                    source, target = weakest
                    adjacency[source].discard(target)
                    incoming[target].discard(source)
                    for mapping in (weights, delays, eligibility, release_state):
                        mapping.pop(weakest, None)
                    structural_removed += 1

                    attempts = 0
                    while attempts < 100:
                        attempts += 1
                        source = rng.randrange(config.n_neurons)
                        target = rng.randrange(config.n_neurons)
                        edge = (source, target)
                        if source == target or edge in weights:
                            continue
                        adjacency[source].add(target)
                        incoming[target].add(source)
                        weights[edge] = config.weight
                        delays[edge] = config.delay_ticks
                        eligibility[edge] = 0.0
                        release_state[edge] = 1.0
                        structural_added += 1
                        break

                delay_learning = (
                    plasticity == "delay_plasticity" or synapse_mode == "delay_plastic"
                )
                if delay_learning:
                    for neuron_id in spiked_this_tick:
                        for source in list(incoming[neuron_id]):
                            edge = (source, neuron_id)
                            delta = tick - last_spike[source]
                            if 0 < delta <= 12:
                                delays[edge] = max(1, delays[edge] - 1)
                            elif delta > 24:
                                delays[edge] = min(64, delays[edge] + 1)

                if neural_io is not None:
                    neural_io.observe(tick, spiked_this_tick)

                reward_signal = 0.0
                if behavior_engine is not None:
                    behavior_engine.observe(spiked_this_tick)
                    learned_reward = behavior_engine.maybe_learn(tick)
                    if learned_reward is not None:
                        reward_signal = learned_reward
                if cortical_org is not None:
                    cortical_org.observe(spiked_this_tick, reward_signal)

                if dual_scheduler is not None:
                    dual_scheduler.observe_spikes(tick, spiked_this_tick)

                if pan_runtime is not None:
                    pan_runtime.update(
                        tick=tick,
                        dt_ms=config.dt_ms,
                        states=states,
                        spiked_neurons=spiked_this_tick,
                        plasticity_active=plasticity != "none",
                    )

                for source in spiked_this_tick:
                    for target in list(adjacency[source]):
                        edge = (source, target)
                        amplitude = weights[edge]
                        if pan_runtime is not None:
                            amplitude *= float(states[source].get("pan_amplitude", 1.0))
                        if synapse_mode in {"quantal_stp", "pan_stp_stdp"}:
                            available = release_state[edge]
                            released = (
                                1.0
                                if rng.random() < min(0.95, 0.25 + 0.7 * available)
                                else 0.0
                            )
                            amplitude *= released
                            release_state[edge] = max(0.1, available * 0.72)
                        delivery_slot = (tick + delays[edge]) % queue_size
                        pending[delivery_slot][target] += amplitude
                    last_spike[source] = tick

                if synapse_mode in {"quantal_stp", "pan_stp_stdp"}:
                    for edge in list(release_state):
                        release_state[edge] = min(
                            1.0,
                            release_state[edge] + 0.025,
                        )

                if dual_scheduler is not None and dual_scheduler.sync_due(tick):
                    barrier_events = dual_scheduler.drain_barrier(tick)
                    offloader.flush_events(tick=tick, events=barrier_events)
                    if growth_engine is not None:
                        added, removed = growth_engine.evaluate(
                            tick=tick,
                            events=barrier_events,
                            states=states,
                            adjacency=adjacency,
                            incoming=incoming,
                            weights=weights,
                            delays=delays,
                            eligibility=eligibility,
                            release_state=release_state,
                            default_weight=config.weight,
                            default_delay_ticks=config.delay_ticks,
                        )
                        structural_added += added
                        structural_removed += removed
                    offloader.maybe_snapshot(
                        tick=tick,
                        payload={
                            "tick": tick,
                            "edge_count": len(weights),
                            "spike_count": len(spiked_this_tick),
                        },
                    )

                state_monitor.record(tick, states, state_stride)
                tick_spike_counts.append(len(spiked_this_tick))
                execution_switcher.observe(spiked_this_tick, config.n_neurons)
                previous_spikes = list(spiked_this_tick)

        if dual_scheduler is not None:
            final_events = dual_scheduler.finalize(config.ticks - 1)
            offloader.flush_events(tick=config.ticks - 1, events=final_events)
            if growth_engine is not None and final_events:
                added, removed = growth_engine.evaluate(
                    tick=config.ticks - 1,
                    events=final_events,
                    states=states,
                    adjacency=adjacency,
                    incoming=incoming,
                    weights=weights,
                    delays=delays,
                    eligibility=eligibility,
                    release_state=release_state,
                    default_weight=config.weight,
                    default_delay_ticks=config.delay_ticks,
                )
                structural_added += added
                structural_removed += removed

        rates = rate_monitor.rates_hz(config.ticks, config.dt_ms)
        total_spikes = len(spike_monitor.ticks)
        duration_s = config.ticks * config.dt_ms / 1000.0
        mean_rate = sum(rates) / max(len(rates), 1)
        active_neurons = sum(1 for value in rate_monitor.counts if value > 0)
        session_id = (
            "PG-"
            + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            + "-"
            + uuid.uuid4().hex[:8]
        )

        current_edges = list(weights)
        weight_values = list(weights.values())
        result: dict[str, object] = {
            "session_id": session_id,
            "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "manifest": playground_manifest(),
            "config": config.to_dict(),
            "model": model.descriptor(),
            "topology": {
                "name": topology.name,
                "dimensions": topology.dimensions,
                "neuron_count": config.n_neurons,
                "edge_count": len(current_edges),
                "coordinates": [list(point) for point in topology.coordinates],
                "edges": [list(edge) for edge in current_edges[:20_000]],
                "metadata": dict(topology.metadata),
            },
            "metrics": {
                "total_spikes": total_spikes,
                "duration_s": duration_s,
                "mean_rate_hz": mean_rate,
                "active_neurons": active_neurons,
                "active_fraction": active_neurons / config.n_neurons,
                "weight_mean": (
                    sum(weight_values) / len(weight_values) if weight_values else 0.0
                ),
                "weight_min": min(weight_values, default=0.0),
                "weight_max": max(weight_values, default=0.0),
                "delay_mean_ticks": (
                    sum(delays.values()) / len(delays) if delays else 0.0
                ),
            },
            "monitors": {
                "spikes": spike_monitor.rows(),
                "rates_hz": [round(value, 6) for value in rates],
                "tick_spike_counts": tick_spike_counts,
                "state_samples": state_monitor.samples,
            },
            "readout": apply_readout(config.readout, rates),
        }
        result["gates"] = gate_schematic.descriptor()
        result["storage"] = {
            **memory_pool.summary(memory_estimate),
            "offload": offloader.summary(),
        }
        result["hardware"] = selected_hardware_profile
        result["execution"] = execution_switcher.summary()
        result["interfaces"] = {
            "existing_gateway_contract": True,
            "network_area_adapter": "src.embodiment.neural_symbiosis.NetworkAreaAdapter",
            "gateway_runtime": "src.embodiment.gateway_runtime.GatewayRuntime",
            "msba_modalities": ["audio", "vision", "digital"],
            "new_parallel_llm_interface_created": False,
            "new_parallel_data_interface_created": False,
            "exact_payload_outside_snn": True,
        }
        if dual_scheduler is not None:
            result["clock"] = dual_scheduler.summary()
        else:
            result["clock"] = {
                "classification": "PLAYGROUND_CLOCK",
                "scientific_evidence": False,
                "mode": "continuous",
                "continuous_steps": config.ticks,
                "continuous_dt_ms": config.dt_ms,
            }
        if growth_engine is not None:
            result["growth"] = growth_engine.summary()
        if thalamic_gate is not None:
            result["thalamic_gating"] = thalamic_gate.summary()
        if cortical_org is not None:
            result["cortical_organization"] = cortical_org.summary()
        if behavior_engine is not None:
            result["behavioral_learning"] = behavior_engine.summary()

        if neural_io is not None:
            result["neural_io"] = neural_io.finalize()

        pan_summary: dict[str, object] | None = None
        if pan_runtime is not None:
            pan_summary = pan_runtime.summary(states)
            result["pan"] = pan_summary

        if topology.name == "geometric_5d":
            apoptosis_events = (
                pan_summary.get("apoptosis_events", [])
                if isinstance(pan_summary, dict)
                else []
            )
            result["geometry"] = geometry_diagnostics(
                topology.coordinates,
                current_edges,
                lambda_a=config.geometry_lambda_a,
                lambda_b=config.geometry_lambda_b,
                radius=config.radius,
                mode=config.geometry_mode,
                delays=delays,
                apoptosis_events=(
                    apoptosis_events if isinstance(apoptosis_events, list) else []
                ),
                activity_values=rates,
            )

        runtime = time.perf_counter() - started
        result["analysis"] = analyze_result(
            result,
            initial_weight=config.weight,
            final_weights=weight_values,
            initial_edge_count=initial_edge_count,
            final_edge_count=len(current_edges),
            structural_added=structural_added,
            structural_removed=structural_removed,
            runtime_seconds=runtime,
        )

        if config.persist:
            path = record_session(session_id, result)
            result["persisted_path"] = str(path)

        return result
