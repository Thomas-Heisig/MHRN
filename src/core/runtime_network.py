"""Hot-path network implementation for interactive runtime execution.

The canonical ``network.NeuralNetwork`` remains the reference implementation.
This subclass preserves its tick equations and event semantics while relying on
stable insertion order instead of sorting the complete neuron map every tick.
MHRN construction and restore are deterministic, so insertion order is part of
the reproducible runtime state.
"""

from __future__ import annotations

import time

from .network import NeuralNetwork, SpikeEvent, StepResult


class RuntimeNeuralNetwork(NeuralNetwork):
    """NeuralNetwork with deterministic O(N) hot-path iteration."""

    def step(self) -> StepResult:
        start = time.perf_counter()
        tick = self.current_tick
        slot_index = tick % len(self.event_slots)

        external_currents = self.pending_currents.copy()
        self.pending_currents.clear()

        synaptic_currents: dict[int, float] = {}
        # Events are appended deterministically by the same runtime. Avoid a
        # redundant sort of the current circular-buffer slot.
        events = self.event_slots[slot_index]
        for event in events:
            if self.debug_invariants and event.delivery_tick != tick:
                raise RuntimeError(
                    f"Queue invariant violated: tick={tick}, "
                    f"delivery={event.delivery_tick}"
                )
            if event.target_id in self.neurons:
                synaptic_currents[event.target_id] = (
                    synaptic_currents.get(event.target_id, 0.0) + event.weight
                )
            self.total_events_processed += 1

        delivered = len(events)
        self.event_slots[slot_index] = []
        self._queued_event_count -= delivered
        if self.debug_invariants and self._queued_event_count < 0:
            raise RuntimeError("queued_event_count became negative")

        spike_ids: list[int] = []
        output_spikes: list[int] = []
        active = len(self.neurons)
        sum_v = 0.0
        sum_energy = 0.0
        min_v = float("inf")
        max_v = -float("inf")

        for neuron_id, neuron in self.neurons.items():
            external = external_currents.get(neuron_id, 0.0)
            synaptic = synaptic_currents.get(neuron_id, 0.0)
            neuron.last_external_current = external
            neuron.last_synaptic_current = synaptic

            spiked = neuron.step(external + synaptic, tick)
            sum_v += neuron.v
            sum_energy += neuron.energy
            min_v = min(min_v, neuron.v)
            max_v = max(max_v, neuron.v)

            if not spiked:
                continue
            spike_ids.append(neuron_id)
            self.total_spikes += 1
            if neuron_id in self.output_cells:
                output_spikes.append(neuron_id)

            # Connection lists are created/restored deterministically. Sorting
            # local fan-out on every spike is therefore redundant.
            for connection in self.synapses.get(neuron_id, ()):
                connection.last_pre_spike = tick
                connection.mark_dirty()
                delivery_tick = tick + connection.delay
                slot = delivery_tick % len(self.event_slots)
                self.event_slots[slot].append(
                    SpikeEvent(
                        neuron_id,
                        connection.target_id,
                        connection.weight,
                        delivery_tick,
                    )
                )
                self._queued_event_count += 1

        if active:
            mean_v = sum_v / active
            mean_energy = sum_energy / active
        else:
            mean_v = min_v = max_v = mean_energy = 0.0

        self.current_tick = tick + 1
        self._step_count += 1

        if self.debug_invariants:
            actual = sum(len(slot) for slot in self.event_slots)
            if actual != self._queued_event_count:
                raise RuntimeError(
                    "Queue accounting mismatch: "
                    f"counter={self._queued_event_count}, actual={actual}"
                )

        elapsed = (time.perf_counter() - start) * 1000.0
        result = StepResult(
            tick=tick,
            spike_ids=tuple(spike_ids),
            output_spike_ids=tuple(output_spikes),
            spikes_this_tick=len(spike_ids),
            total_spikes=self.total_spikes,
            delivered_events=delivered,
            queued_events=self._queued_event_count,
            external_injection_count=len(external_currents),
            external_total_current=sum(external_currents.values()),
            synaptic_current_targets=len(synaptic_currents),
            mean_v=mean_v,
            min_v=min_v,
            max_v=max_v,
            mean_energy=mean_energy,
            core_step_ms=elapsed,
            # No caller consumes the all-neuron boolean map. Spike IDs are the
            # compact authoritative activity representation.
            neuron_activity={},
            total_synapses=self._synapse_count,
            dirty_neuron_ids=tuple(sorted(self._dirty_neuron_ids)),
            dirty_synapse_ids=tuple(sorted(self._dirty_synapse_ids)),
        )

        for hook in tuple(self._post_step_hooks):
            try:
                hook(result)
            except Exception:
                pass
        return result


__all__ = ["RuntimeNeuralNetwork"]
