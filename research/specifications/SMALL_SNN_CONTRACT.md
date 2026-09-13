# Stage 1 — Small SNN Software Contract

## Scope

Stage 1 is the first network-level software contract after the Stage-0 single-neuron primitive. It establishes that multiple MHRN neurons can be coupled by explicit sparse synapses and that spikes propagate through the event queue with declared delays.

This contract is **engineering verification only**. It is not evidence of biological equivalence, cognition, useful learning, consciousness, or large-scale tractability.

## Canonical reference network

The deterministic reference treatment is a three-cell feed-forward chain:

`A -> B -> C`

- neuron model: `izhikevich-2003`
- `dt = 1 ms`
- secondary single-cell mechanisms disabled through `NeuronConfig.isolated_reference()`
- A -> B: weight `100.0`, delay `1` tick
- B -> C: weight `100.0`, delay `2` ticks
- reference-only synaptic bounds: `w_min = 0.0`, `w_max = 100.0`
- initial trigger: `A.v = 30 mV` at tick 0

The elevated reference weight is intentionally isolated to this software verification fixture. It does not change production defaults and is not presented as a biological parameter.

## Required causal trace

| Tick | Spikes | Delivered events | Queued events after tick |
| --- | --- | ---: | ---: |
| 0 | A | 0 | 1 |
| 1 | B | 1 | 1 |
| 2 | — | 0 | 1 |
| 3 | C | 1 | 0 |

## Required proofs

1. **Explicit sparse topology** — exactly three neurons and two directed synapses are present in the reference network.
2. **Delayed event delivery** — each event is delivered at its declared delivery tick, not earlier or later.
3. **Causal spike propagation** — A causes the delayed drive to B; B then causes the delayed drive to C.
4. **Deterministic replay** — identical seed, configuration and initial state produce identical tick results and final serialized network state.
5. **Batch/tick equivalence** — `step_batch(n)` produces the same deterministic state transition as `n` consecutive `step()` calls.

## Canonical implementation sources

- `src/core/network.py`
- `src/core/synapse.py`
- `src/core/spatial_index.py`
- `tests/test_network.py`
- `tests/test_small_snn_contract.py`
- `research/generated/verification/small_snn_reference.json`

## Dashboard surfaces

Stage 1 is exposed as the same first-class concept across the operator interface:

- **02 · Wissenschaft -> Kleines SNN** — live topology and Stage-1 contract.
- **03 · Runtime & Wesen -> SNN** — read-only live network state and topology.
- **04 · Control -> SNN-Parameter** — scientifically sensitive construction parameters through Pending Changes.
- **05 · Release -> Entwicklung** — repository-derived engineering maturity; the Stage-1 implementation score reaches 100% only when the scoped verification artifact is present and valid.

## Evidence boundary

Completion of this contract means only that the small-network software mechanics described above are implemented and explicitly verified. The following remain separate questions:

- stability of recurrent networks over long runs,
- learning efficacy,
- robustness under perturbation,
- scaling to large neuron/synapse counts,
- biological plausibility beyond the declared abstractions,
- cognition or consciousness.
