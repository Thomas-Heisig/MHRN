"""Incremental hot-path collector for runtime persistence.

The original :class:`StorageSession` remains the conservative reference path.
This collector is used by the asynchronous operator/runtime path when
``capture_policy=dirty_tracking``. It consumes the network's dirty sets after
all hooks registered before storage have run and avoids rebuilding the complete
synapse map on every tick.

Neuron membrane state is special: an active spiking neuron legitimately changes
on almost every tick. ``neuron_state_interval_ticks`` therefore controls an
explicit persistence trade-off:

* ``1`` keeps per-tick neuron-state capture for exact restart-oriented runs.
* ``>1`` captures neuron state at a bounded cadence for interactive/operator
  runs while spike, synapse and topology deltas remain event-driven.

Using an interval greater than one is an engineering performance mode, not a
claim of per-tick restart equivalence.
"""

from __future__ import annotations

from collections.abc import MutableSet
from typing import cast

from .delta_codec import (
    NeuronAddDelta,
    NeuronRemoveDelta,
    NeuronStateDelta,
    SpikeEventDelta,
    SynapseAddDelta,
    SynapseRemoveDelta,
    SynapseWeightDelta,
    encode_neuron_add,
    encode_neuron_remove,
    encode_neuron_state,
    encode_spike_event,
    encode_synapse_add,
    encode_synapse_remove,
    encode_synapse_weight,
)
from .delta_journal import DeltaRecord
from .optical_codec import state_from_neuron
from .runtime import (
    RuntimeNetworkLike,
    RuntimeSynapseLike,
    StepResultLike,
    StorageRuntimeConfig,
    StorageSession,
)


class IncrementalStorageSession(StorageSession):
    """Storage collector whose per-tick synapse work is proportional to dirties."""

    def __init__(
        self,
        network: RuntimeNetworkLike,
        config: StorageRuntimeConfig,
        *,
        neuron_state_interval_ticks: int = 1,
    ) -> None:
        super().__init__(network, config)
        if neuron_state_interval_ticks <= 0:
            raise ValueError("neuron_state_interval_ticks must be positive")
        self.neuron_state_interval_ticks = int(neuron_state_interval_ticks)

    def prime(self) -> None:
        """Prime fingerprints and discard construction-time dirty markers."""
        super().prime()
        self._consume_network_dirty_sets()

    def _network_dirty_sets(
        self, result: StepResultLike
    ) -> tuple[set[int], set[tuple[int, int]]]:
        neuron_dirty = getattr(self.network, "_dirty_neuron_ids", None)
        synapse_dirty = getattr(self.network, "_dirty_synapse_ids", None)
        if isinstance(neuron_dirty, set):
            neuron_ids = {
                int(cast(int | float | str | bytes | bytearray, value))
                for value in cast(set[object], neuron_dirty)
            }
        else:
            neuron_ids = {int(value) for value in result.dirty_neuron_ids}
        if isinstance(synapse_dirty, set):
            synapse_ids = {
                (
                    int(cast(int | float | str | bytes | bytearray, source_id)),
                    int(cast(int | float | str | bytes | bytearray, target_id)),
                )
                for source_id, target_id in cast(
                    set[tuple[object, object]], synapse_dirty
                )
            }
        else:
            synapse_ids = {
                (int(source_id), int(target_id))
                for source_id, target_id in result.dirty_synapse_ids
            }
        return neuron_ids, synapse_ids

    def _consume_network_dirty_sets(self) -> None:
        """Clear dirty markers already consumed by this storage hook.

        Hooks that execute after storage can mark the sets again; those changes
        are then observed on the next storage callback.
        """
        for attribute in ("_dirty_neuron_ids", "_dirty_synapse_ids"):
            values = getattr(self.network, attribute, None)
            if isinstance(values, MutableSet):
                values.clear()

    def _current_synapse(
        self, source_id: int, target_id: int
    ) -> RuntimeSynapseLike | None:
        outgoing = self.network.synapses.get(source_id, ())
        for synapse in outgoing:
            if int(synapse.target_id) == target_id:
                return synapse
        return None

    def collect_deltas(self, result: StepResultLike) -> tuple[DeltaRecord, ...]:
        """Collect one tick without a full O(E) topology reconstruction."""
        tick = int(result.tick)
        deltas: list[DeltaRecord] = []
        dirty_neurons, dirty_synapses = self._network_dirty_sets(result)

        try:
            for neuron_id in sorted(dirty_neurons):
                current_neuron = self.network.neurons.get(neuron_id)
                previous_neuron = self._neurons.get(neuron_id)
                if current_neuron is None and previous_neuron is not None:
                    deltas.append(
                        encode_neuron_remove(tick, NeuronRemoveDelta(neuron_id))
                    )
                    self._neurons.pop(neuron_id, None)
                    self._topology_deltas += 1
                elif current_neuron is not None and previous_neuron is None:
                    optical = state_from_neuron(current_neuron)
                    deltas.append(
                        encode_neuron_add(
                            tick,
                            NeuronAddDelta(
                                neuron_id=neuron_id,
                                tick=tick,
                                optical=optical,
                                a=float(current_neuron.a),
                                b=float(current_neuron.b),
                                c=float(current_neuron.c),
                                d=float(current_neuron.d),
                                spike_cost=float(current_neuron.spike_cost),
                                spike_counter=int(current_neuron.spike_counter),
                                last_spike_tick=int(current_neuron.last_spike_tick),
                            ),
                        )
                    )
                    self._neurons[neuron_id] = self._neuron_fingerprint(current_neuron)
                    self._topology_deltas += 1

            capture_neuron_state = (
                self.neuron_state_interval_ticks == 1
                or (tick + 1) % self.neuron_state_interval_ticks == 0
            )
            if capture_neuron_state:
                # O(N) at the declared cadence. There is no honest O(changes)
                # shortcut for v/u because membrane state changes continuously.
                for neuron_id, neuron in self.network.neurons.items():
                    numeric_id = int(neuron_id)
                    neuron_fingerprint = self._neuron_fingerprint(neuron)
                    previous_neuron_fingerprint = self._neurons.get(numeric_id)
                    if (
                        previous_neuron_fingerprint is not None
                        and neuron_fingerprint != previous_neuron_fingerprint
                    ):
                        deltas.append(
                            encode_neuron_state(
                                tick,
                                NeuronStateDelta(
                                    neuron_id=numeric_id,
                                    membrane_v=neuron_fingerprint.v,
                                    recovery_u=neuron_fingerprint.u,
                                    energy=neuron_fingerprint.energy,
                                    spike_counter=neuron_fingerprint.spike_counter,
                                    last_spike_tick=neuron_fingerprint.last_spike_tick,
                                ),
                            )
                        )
                        self._neuron_deltas += 1
                    self._neurons[numeric_id] = neuron_fingerprint

            for source_id, target_id in sorted(dirty_synapses):
                key = (source_id, target_id)
                current_synapse = self._current_synapse(source_id, target_id)
                previous_synapse = self._synapses.get(key)
                if current_synapse is None:
                    if previous_synapse is not None:
                        deltas.append(
                            encode_synapse_remove(
                                tick,
                                SynapseRemoveDelta(
                                    source_id=source_id, target_id=target_id
                                ),
                            )
                        )
                        self._synapses.pop(key, None)
                        self._topology_deltas += 1
                    continue

                synapse_fingerprint = self._synapse_fingerprint(current_synapse)
                if previous_synapse is None:
                    deltas.append(
                        encode_synapse_add(
                            tick,
                            SynapseAddDelta(
                                source_id=source_id,
                                target_id=target_id,
                                weight=synapse_fingerprint.weight,
                                eligibility=synapse_fingerprint.eligibility,
                                delay=synapse_fingerprint.delay,
                                last_pre_spike=synapse_fingerprint.last_pre_spike,
                            ),
                        )
                    )
                    self._topology_deltas += 1
                elif synapse_fingerprint != previous_synapse:
                    deltas.append(
                        encode_synapse_weight(
                            tick,
                            SynapseWeightDelta(
                                source_id=source_id,
                                target_id=target_id,
                                weight=synapse_fingerprint.weight,
                                eligibility=synapse_fingerprint.eligibility,
                                last_pre_spike=synapse_fingerprint.last_pre_spike,
                            ),
                        )
                    )
                    self._synapse_deltas += 1
                self._synapses[key] = synapse_fingerprint

            if self.config.capture_spike_events:
                for neuron_id in result.spike_ids:
                    deltas.append(
                        encode_spike_event(
                            tick, SpikeEventDelta(neuron_id=int(neuron_id))
                        )
                    )
                    self._spike_events += 1

            return tuple(deltas)
        finally:
            self._consume_network_dirty_sets()


__all__ = ["IncrementalStorageSession"]
