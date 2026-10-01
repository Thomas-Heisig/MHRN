# MHRN Canonical Learning and Synapse Contract v0.1

**Status:** canonical design contract; backend implementation alignment pending  
**Scientific evidence:** none created by this document  
**Required before:** CUDA-1.6 scientific closed-loop runs

## Purpose

CPU and CUDA must not implement two merely similar learning rules and then call the result backend parity. This contract defines the semantic surface that both backends must implement before plastic closed-loop parity can be treated as a scientific question.

The existing `LearningEngine` remains the current canonical CPU implementation reference. The current CUDA-1.5 plastic path is an engineering reference and must be aligned to this contract before canonical scientific use.

## Versioned contract

```text
learning_contract_id = mhrn-learning-synapse-v1
```

A scientific run records at least:

- learning contract id and artifact hash;
- neuron/synapse identity schema;
- parameter bundle hash;
- update-order version;
- RNG algorithm/version where stochastic release is enabled;
- execution backend and backend artifact hash.

## Synapse identity

A learning state is bound to a stable canonical synapse identity, not to array position, CSR position or Python object identity.

The target contract is:

```text
edge_id: uint64
```

Until stable `edge_id` is fully canonicalized, any experiment using pair keys such as `(pre_id, post_id)` must explicitly reject parallel synapses.

## Normative tick order

For contract v1 a tick is conceptually separated into these phases:

1. complete neuron/network state advance for tick `t`;
2. obtain the complete spike set for `t`;
3. construct synapse events in stable identity order;
4. evaluate pair-based STDP against spike history strictly earlier than `t`;
5. update eligibility from the pair-event delta;
6. apply direct STDP weight change when enabled;
7. commit current-tick pre/post spike timestamps;
8. apply rewards due at `t` in deterministic reward order;
9. apply weight bounds and state invariants;
10. publish checkpoint/telemetry state only after the learning phase is complete.

Backends may fuse kernels internally, but observable semantics must be equivalent to this phase order.

## Same-tick rule

The v1 contract does not treat simultaneous pre/post spikes as either LTP or LTD.

```text
delta_t = 0 -> pair contribution = 0
```

This matches the current CPU nearest-neighbour rule, which requires strictly positive temporal separation.

Any future alternate simultaneous-spike rule requires a new contract version.

## Pair-based STDP

For a current presynaptic spike at tick `t` and the previous postsynaptic spike `t_post < t`:

```text
LTD = -a_minus * exp((t_post - t) / tau_minus)
```

For a current postsynaptic spike at tick `t` and the previous presynaptic spike `t_pre < t`:

```text
LTP = +a_plus * exp(-(t - t_pre) / tau_plus)
```

The pair delta is the sum of applicable terms for that synapse event.

All parameters are finite, versioned and included in the parameter-bundle hash.

## Eligibility

Eligibility is a per-synapse continuation-critical state.

A pair-event delta is added at the event tick. Between observations the trace follows the versioned decay law of the canonical eligibility implementation.

The checkpoint must preserve enough state to reproduce an uninterrupted continuation exactly for the declared determinism class.

A backend must not replace the eligibility law with an approximately similar trace without changing the learning-contract version.

## Reward semantics

A reward record contains at least:

```text
value
emitted_tick
effective_tick
sequence_id
```

For delay `d`:

```text
effective_tick = emitted_tick + d
```

At the effective tick the reward update is:

```text
delta_w_reward = reward_learning_rate * reward_value * eligibility(effective_tick)
```

Rewards due on the same tick are applied in stable `sequence_id` order.

Pending rewards are continuation-critical checkpoint state.

A CUDA frozen-reward array is equivalent only if it represents exactly the same ordered reward records and effective ticks.

## Credit window

A generic fixed `credit_window` is not silently interchangeable with the canonical eligibility decay plus reward-delay model.

If a bounded credit-window optimization is used, it must be proven equivalent over the declared parameter range or be assigned a different learning-contract version.

## STP

STP is not yet part of the current CPU `LearningEngine` semantic core and therefore cannot be silently folded into `mhrn-learning-synapse-v1`.

For CUDA-1.5 STP, canonicalization requires a versioned sub-contract defining:

- release probability;
- deterministic RNG key/counter semantics;
- depletion rule;
- recovery rule;
- whether the emitted delayed amplitude freezes the pre-update or post-update state;
- continuation state required for checkpoint/replay.

Until that sub-contract is implemented on the canonical CPU reference, STP parity remains an engineering-reference result.

## Delayed-signal semantics

Once a synaptic event is emitted into a delay queue/ring, its carried amplitude is immutable.

Later weight or STP updates must not retroactively alter an already emitted delayed event.

The checkpoint therefore stores the pending emitted event/amplitude state, not merely current weights.

## Weight decay and clamping

Weight bounds are part of the contract.

For the current CPU learning contract:

```text
min_weight <= weight <= max_weight
```

Direct STDP updates are clamped immediately. Reward updates follow the configured `reward_clamp_weights` policy.

Any unconditional per-tick weight decay used by a backend is a semantic difference unless that decay is explicitly added to a later contract version and implemented on all compared backends.

## Deterministic iteration

All synapse events, reward applications and checkpoint serialization are ordered by stable canonical identity.

Hash-map, set, warp scheduling and CSR insertion order are not semantic ordering mechanisms.

## Canonical parity ladder

Before CUDA-1.6 with learning:

- D1: exact spike/event parity;
- D2-L: weight, eligibility, spike-history and STP-state parity for every canonical edge;
- replay: checkpoint/restore continuation parity;
- negative controls: intentional update-order/RNG perturbation must be detected fail-closed.

## Promotion gate

CUDA-1.5 is eligible for canonical backend use only after:

1. CPU and CUDA implement the same versioned learning contract;
2. all continuation-critical learning state is checkpointed;
3. parity is demonstrated over a preregistered parameter/seed matrix;
4. no Playground-only state is required by the canonical path.
