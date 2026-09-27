"""Bounded event-driven structural growth for the non-canonical PAN Playground."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any

Edge = tuple[int, int]
State = MutableMapping[str, Any]


class GrowthEngine:
    """Mutate a fixed-capacity Playground network at dual-clock barriers.

    Neurogenesis is intentionally pool-backed: an apoptotic PAN slot can be
    reactivated, but the reference runtime never reallocates the population.
    """

    def __init__(
        self,
        *,
        n_neurons: int,
        edge_budget: int,
        max_synapses_per_neuron: int,
        max_new_synapses_per_barrier: int,
        activity_threshold: float,
        coactivation_threshold: int,
        information_threshold: float,
        prune_threshold: float,
        neurogenesis: bool = True,
        synaptogenesis: bool = True,
        path_formation: bool = True,
        pruning: bool = True,
    ) -> None:
        self.n_neurons = n_neurons
        self.edge_budget = edge_budget
        self.max_synapses_per_neuron = max_synapses_per_neuron
        self.max_new_synapses_per_barrier = max_new_synapses_per_barrier
        self.activity_threshold = activity_threshold
        self.coactivation_threshold = coactivation_threshold
        self.information_threshold = information_threshold
        self.prune_threshold = prune_threshold
        self.neurogenesis = neurogenesis
        self.synaptogenesis = synaptogenesis
        self.path_formation = path_formation
        self.pruning = pruning
        self.activity_ema = [0.0 for _ in range(n_neurons)]
        self.coactivation: dict[Edge, int] = defaultdict(int)
        self.neurogenesis_events: list[dict[str, object]] = []
        self.synaptogenesis_events: list[dict[str, object]] = []
        self.path_events: list[dict[str, object]] = []
        self.pruning_events: list[dict[str, object]] = []
        self.barriers = 0

    def _add_edge(
        self,
        *,
        tick: int,
        source: int,
        target: int,
        reason: str,
        adjacency: list[set[int]],
        incoming: list[set[int]],
        weights: MutableMapping[Edge, float],
        delays: MutableMapping[Edge, int],
        eligibility: MutableMapping[Edge, float],
        release_state: MutableMapping[Edge, float],
        weight: float,
        delay_ticks: int,
    ) -> bool:
        edge = (source, target)
        if (
            source == target
            or edge in weights
            or len(weights) >= self.edge_budget
            or len(adjacency[source]) >= self.max_synapses_per_neuron
        ):
            return False
        adjacency[source].add(target)
        incoming[target].add(source)
        weights[edge] = weight
        delays[edge] = delay_ticks
        eligibility[edge] = 0.0
        release_state[edge] = 1.0
        event = {
            "tick": tick,
            "source": source,
            "target": target,
            "reason": reason,
        }
        if reason == "coactivation":
            self.synaptogenesis_events.append(event)
        else:
            self.path_events.append(event)
        return True

    def _reactivate_slot(
        self,
        *,
        tick: int,
        states: Sequence[State],
    ) -> bool:
        if max(self.activity_ema, default=0.0) < self.activity_threshold:
            return False
        for neuron_id, state in enumerate(states):
            if bool(state.get("pan_alive", True)):
                continue
            state["pan_alive"] = True
            state["pan_health"] = 0.75
            state["pan_energy"] = 0.75
            state["pan_amplitude"] = 0.8
            state["pan_activity_ema"] = 0.0
            state["pan_consolidation"] = 0.0
            self.neurogenesis_events.append(
                {
                    "tick": tick,
                    "neuron_id": neuron_id,
                    "mode": "POOL_BACKED_REACTIVATION",
                }
            )
            return True
        return False

    def evaluate(
        self,
        *,
        tick: int,
        events: Sequence[Mapping[str, object]],
        states: Sequence[State],
        adjacency: list[set[int]],
        incoming: list[set[int]],
        weights: MutableMapping[Edge, float],
        delays: MutableMapping[Edge, int],
        eligibility: MutableMapping[Edge, float],
        release_state: MutableMapping[Edge, float],
        default_weight: float,
        default_delay_ticks: int,
    ) -> tuple[int, int]:
        """Apply one bounded growth/pruning barrier and return add/remove counts."""

        self.barriers += 1
        spike_counts = [0 for _ in range(self.n_neurons)]
        spiking: set[int] = set()
        for event in events:
            if event.get("kind") != "SPIKE":
                continue
            raw_id = event.get("neuron_id")
            if not isinstance(raw_id, int) or not 0 <= raw_id < self.n_neurons:
                continue
            spike_counts[raw_id] += 1
            spiking.add(raw_id)

        peak = max(spike_counts, default=0)
        normalizer = max(peak, 1)
        for neuron_id, count in enumerate(spike_counts):
            instant = count / normalizer
            self.activity_ema[neuron_id] = (
                0.8 * self.activity_ema[neuron_id] + 0.2 * instant
            )

        ordered = sorted(spiking)
        for index, source in enumerate(ordered):
            for target in ordered[index + 1 :]:
                self.coactivation[(source, target)] += 1
                self.coactivation[(target, source)] += 1

        if self.neurogenesis:
            self._reactivate_slot(tick=tick, states=states)

        added = 0
        candidates = sorted(
            self.coactivation.items(),
            key=lambda item: (-item[1], item[0][0], item[0][1]),
        )
        for (source, target), score in (
            candidates if self.synaptogenesis else []
        ):
            if added >= self.max_new_synapses_per_barrier:
                break
            if score < self.coactivation_threshold:
                break
            if self._add_edge(
                tick=tick,
                source=source,
                target=target,
                reason="coactivation",
                adjacency=adjacency,
                incoming=incoming,
                weights=weights,
                delays=delays,
                eligibility=eligibility,
                release_state=release_state,
                weight=default_weight,
                delay_ticks=default_delay_ticks,
            ):
                added += 1
                self.coactivation[(source, target)] = 0

        information = [
            (float(state.get("pan_information_proxy", 0.0)), neuron_id)
            for neuron_id, state in enumerate(states)
            if bool(state.get("pan_alive", True))
        ]
        information.sort(reverse=True)
        if (
            self.path_formation
            and added < self.max_new_synapses_per_barrier
            and len(information) >= 2
            and information[0][0] >= self.information_threshold
            and information[1][0] >= self.information_threshold
        ):
            source = information[0][1]
            target = information[1][1]
            if self._add_edge(
                tick=tick,
                source=source,
                target=target,
                reason="information_path",
                adjacency=adjacency,
                incoming=incoming,
                weights=weights,
                delays=delays,
                eligibility=eligibility,
                release_state=release_state,
                weight=default_weight,
                delay_ticks=default_delay_ticks,
            ):
                added += 1

        removed = 0
        weak_edges = sorted(
            (
                (edge, value)
                for edge, value in weights.items()
                if value <= self.prune_threshold
            ),
            key=lambda item: (item[1], item[0][0], item[0][1]),
        )
        max_prune = self.max_new_synapses_per_barrier
        for edge, value in (weak_edges[:max_prune] if self.pruning else []):
            source, target = edge
            adjacency[source].discard(target)
            incoming[target].discard(source)
            for mapping in (weights, delays, eligibility, release_state):
                mapping.pop(edge, None)
            self.pruning_events.append(
                {
                    "tick": tick,
                    "source": source,
                    "target": target,
                    "weight": value,
                }
            )
            removed += 1

        self._trim_logs()
        return added, removed

    def _trim_logs(self) -> None:
        for events in (
            self.neurogenesis_events,
            self.synaptogenesis_events,
            self.path_events,
            self.pruning_events,
        ):
            if len(events) > 512:
                del events[:-512]

    def summary(self) -> dict[str, object]:
        return {
            "classification": "PLAYGROUND_GENERATIVE_GROWTH",
            "scientific_evidence": False,
            "evidence_eligible": False,
            "mode": "EVENT_DRIVEN_BOUNDED_REFERENCE",
            "population_allocation": "FIXED_CAPACITY_POOL",
            "neurogenesis_semantics": "REACTIVATE_APOPTOTIC_SLOT_NO_REALLOCATION",
            "barriers": self.barriers,
            "neurogenesis_events": list(self.neurogenesis_events),
            "synaptogenesis_events": list(self.synaptogenesis_events),
            "path_events": list(self.path_events),
            "pruning_events": list(self.pruning_events),
            "activity_threshold": self.activity_threshold,
            "coactivation_threshold": self.coactivation_threshold,
            "information_threshold": self.information_threshold,
            "prune_threshold": self.prune_threshold,
            "max_synapses_per_neuron": self.max_synapses_per_neuron,
            "max_new_synapses_per_barrier": self.max_new_synapses_per_barrier,
            "neurogenesis_enabled": self.neurogenesis,
            "synaptogenesis_enabled": self.synaptogenesis,
            "path_formation_enabled": self.path_formation,
            "pruning_enabled": self.pruning,
        }
