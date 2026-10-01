# Learning / Synapse Contract — Draft v0.1

**Contract ID:** `mhrn-learning-synapse-v0.1-draft`  
**Status:** `DRAFT_NOT_FROZEN`  
**Research question:** `RQ-LEARN-SEM-001`  
**Scientific evidence:** none created by this contract  
**CUDA plasticity status:** `NON_CANONICAL_DRAFT`

## Purpose

Wave 7 freezes semantics before treating CPU and CUDA learning as
interchangeable. The current CPU `LearningEngine` and CUDA plasticity
reference are both useful implementations, but they are not the same learning
rule today.

The executable descriptor lives in `src/learning/contract.py` and intentionally
reports `ready_for_cross_backend_learning=false`.

## Current CPU reference semantics

For each completed network tick:

1. spike IDs are deduplicated and sorted;
2. pre/post synapse events are collected;
3. events are processed in sorted `(pre_id, target_id)` order;
4. nearest-neighbour pair STDP is evaluated against strictly earlier spikes;
5. same-tick pre/post contributes zero to the pair rule;
6. the pair delta is added to eligibility when enabled;
7. direct STDP applies the same pair delta and clamps weight bounds;
8. current pre/post spike timestamps are committed;
9. delayed rewards due at the tick are applied;
10. rewards iterate synapses in sorted stable-key order.

CPU pair equations are:

```text
LTP = +a_plus * exp(-dt / tau_plus), dt > 0
LTD = -a_minus * exp( dt / tau_minus), dt < 0
dt = 0 -> 0 pair contribution
```

Eligibility uses lazy exponential decay `exp(-dt/tau_ticks)` then adds the
pair-event delta. Reward learning uses
`reward_learning_rate * reward * eligibility(effective_tick)`, where
`effective_tick = emitted_tick + reward_delay_ticks`.

CPU checkpoint v4 already records last pre/post ticks, eligibility state and
pending rewards for continuation/restore.

## STP candidate semantics — not frozen

The current CUDA reference contains a deterministic candidate STP rule:

- Counter-RNG key: `(seed, tick, edge)`;
- release probability: `min(0.95, 0.25 + 0.7 * available)`;
- depletion after a pre event: `max(0.1, available * 0.72)`;
- recovery: `min(1.0, available + 0.025)`.

These values are inventory, not acceptance. The canonical CPU learning engine
does not currently implement this STP state, so Wave 7 must decide whether this
rule becomes the common contract, is revised, or remains backend-specific.

## Known CPU/CUDA semantic mismatches

The contract remains unfrozen because at least these differences are real:

1. CPU learning identity is currently `(pre_id, target_id)`; stable
   `edge_id` semantics for parallel edges are not canonical.
2. CPU has no canonical STP state.
3. CUDA reference uses a fixed credit window; CPU uses delayed reward plus
   continuously decaying eligibility without that same fixed-window rule.
4. CUDA reference applies per-tick weight decay; CPU `LearningEngine` does
   not.
5. Current CUDA pair amplitudes/defaults differ from CPU defaults.

None may be hidden behind tolerances. They require an explicit contract
decision or a new versioned rule.

## Delayed-signal rule

Once a synaptic amplitude is emitted into a delay queue/ring, later weight or
STP updates must not retroactively alter that pending event. This rule is part
of future CPU/CUDA alignment and checkpoint parity.

## Freeze criteria

Wave 7 can only move from Draft to Frozen when:

- stable edge identity is defined;
- STP state/update semantics are accepted or explicitly excluded from the
  contract version;
- reward-credit semantics are identical across compared backends;
- weight-decay semantics are identical across compared backends;
- CPU and CUDA implement the same versioned contract;
- continuation-critical learning state round-trips through canonical
  checkpoint/restore;
- negative-control tests detect deliberate ordering/decay/reward deviations.

## Evidence boundary

A frozen contract would establish a software semantics target only. It would
not prove learning effectiveness, biological validity or scientific evidence.
Those require separate preregistered experiments and Human Review.

## Machine-readable divergence inventory

The five blocking semantic decisions are also recorded in `research/specifications/WAVE7_LEARNING_DIVERGENCES.json`:

1. stable edge identity, including parallel-edge semantics;
2. STP state and update semantics;
3. reward credit-window versus delayed-reward/eligibility semantics;
4. per-tick weight-decay semantics;
5. STDP pair amplitudes/default parameters.

Every item remains `OPEN`. Cross-backend learning equivalence remains blocked until each item has an explicit versioned resolution and the common contract is implemented by both compared backends.
