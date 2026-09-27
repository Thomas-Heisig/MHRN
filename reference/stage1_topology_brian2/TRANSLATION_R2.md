# Brian2 cross-implementation translation contract — R2

**Target:** Stage-1 topology reference replication  
**Preregistration:** `PREREG-S1-TOPO-REFERENCE-R2`  
**Framework:** Brian2 2.10.1  
**Status:** R2 pre-freeze specification; R1 was aborted before reference DATA and remains immutable historical provenance; no reference evaluation DATA are authorized

This document makes the MHRN-to-Brian2 translation auditable. It is not an evidence artifact and does not contain the canonical MHRN target effect vector or equivalence bounds used by the later verifier.

## 1. Independence boundary

The reference package under `reference/stage1_topology_brian2/` must not import MHRN runtime modules, research registries, EVID artifacts, historical experiment statistics, or comparison targets.

The project-side calibration scripts may compare MHRN and reference behavior before freeze, but the later Brian2 evaluation runner is blind to MHRN effect sizes and replication classification.

## 2. Neuron state transition

### MHRN source semantics

For each 1 ms tick, with state `v,u` and total current `I`:

1. `v += 0.5 * (0.04*v^2 + 5*v + 140 - u + I)`
2. repeat the same half-step for `v`
3. `u += 0.02 * (0.2*v - u)`
4. spike iff `v >= 30 + threshold_adaptation`
5. on spike: `v=-65; u+=8; threshold_adaptation+=0.01`
6. update low-pass firing-rate estimate
7. decay threshold adaptation by `0.999`
8. apply homeostatic threshold update `0.001*(firing_rate_estimate-10)`, clamped to [-10,10]

### Brian2 equivalent

The reference implementation does **not** use Brian2's default numerical Izhikevich integration. It schedules the explicit two-half-Euler equations with `run_regularly`, then uses Brian2 threshold/reset scheduling and an explicit post-reset adaptation/homeostasis update.

### Validation

- `CAL-S1-TOPO-REFERENCE-INTEGRATOR-R1`: single-tick subthreshold and spiking parity plus persistent multi-tick parity.
- `CAL-S1-TOPO-REFERENCE-RESET-R1`: explicit reset and post-spike next-tick parity.

All state variables and spike decisions must match at absolute tolerance `1e-12`.

## 3. Threshold adaptation and homeostasis

The code-backed mechanism audit established both mechanisms as active and spike-timing relevant in the canonical Stage-1 run.

Therefore they are mandatory in the Brian2 reference dynamics.

Energy and spike traces are maintained by MHRN but do not feed back into membrane integration, threshold, refractory state or spike gating under the registered Stage-1 configuration. Their omission from the causal Brian2 dynamics is permitted only while the source-hash-bound audit remains valid.

## 4. Synaptic event semantics

### MHRN source semantics

A spike generated at tick `t` queues one event per outgoing fixed synapse for `t + delay`. For the registered reference contract:

- weight = 55
- delay = 1 tick
- no plasticity
- events due at the current tick are accumulated into postsynaptic current before that tick's neuron integration

### Independent reference equivalent

The reference implementation uses its own minimal integer-tick event queue. The queue stores `(delivery_tick, target, weight)` and applies due current before the Brian2 neuron state transition for that tick. It does not import or call MHRN event-buffer code.

### Validation

`CAL-S1-TOPO-REFERENCE-SYNAPSE-R1` uses two neurons and one synapse. A source spike at tick 0 must:

- queue exactly one event;
- deliver no event at tick 0;
- deliver exactly one event at tick 1;
- apply weight 55 to the target before target integration at tick 1;
- reproduce MHRN target state and spike decision at tolerance `1e-12`.

## 5. Topology translation

For each registered shape, coordinates and edges are independently generated from the frozen textual rules.

**Label-order rule:** first generate the full lexicographic Cartesian product of the declared 5D shape. Then sort that list by (1) the sum of normalized coordinates `value_i / max(size_i-1, 1)` and (2) the coordinate tuple as deterministic tie-break. This matches the canonical MHRN label-order semantics without importing its topology builder. An earlier DRAFT described this too loosely as only “lexicographic product order”; the wording was corrected before reference DATA existed.

- 64 materialized neurons;
- future-only directed edges;
- out-degree cap 4;
- total edge budget 246;
- normalized Euclidean coordinate distance for geometric conditions;
- deterministic seed-derived tie resolution;
- `5d_shuffled`: independently specified deterministic coordinate-to-label shuffle before geometric edge construction;
- `random_graph`: independent deterministic PRNG selection of future targets without replacement.

No MHRN topology builder may be imported.

## 6. Stimulus and readout

All conditions use:

- input labels 0–3;
- output labels 60–63;
- current 100 at tick 0 only;
- 128 evaluation ticks;
- identical propagation metric definitions.

The Brian2 runner emits raw reference DATA only. It does not contain canonical MHRN effect sizes, equivalence bounds, or replication verdict logic.

## 7. Metrics

- `first_output_latency_censored`: first tick with any output-label spike; otherwise 129.
- `activation_auc_0_32`: sum over ticks 0–31 of cumulative ever-active neuron fraction.
- `total_spikes`: total emitted spikes.
- `delivered_events`: total synaptic events delivered.
- `final_active_fraction`: fraction of neurons that spiked at least once.

## 8. Failure semantics

Any parity failure, source-drift failure, independence violation, seed collision or semantic ambiguity blocks freeze. It may be corrected only before reference evaluation DATA exist, with the correction documented in the preregistration history.

A later failed or inconclusive reference replication remains a valid scientific outcome and cannot be rescued by modifying this translation after seeing reference results.


## 9. R1 → R2 supersession

R1 was frozen but subsequently aborted before any reference evaluation DATA after an audit identified ambiguity in the frozen coordinate-to-label topology wording. R2 does not reinterpret any result because no R1 reference result exists.

R2 makes the mapping executable and testable: create the Cartesian product, sort by `(sum(value_i/max(size_i-1,1)), coordinate_tuple)`, then assign logical labels. The new pre-freeze gate `CAL-S1-TOPO-REFERENCE-TOPOLOGY-MAP-R2` must show exact coordinate-list and full edge-list parity for every condition across independent probe seeds before R2 may freeze.
