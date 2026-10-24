# OBJ-MEM-COMPRESSION-001 — R1 review-ready protocol

Date: 2026-10-24. Status: **REVIEW_READY_NOT_FROZEN**. Execution authorized:
**false**. No evaluation data collected. This document resolves design choices;
it does not attest to a reviewed or executable implementation.

Proposed new canonical binding: `RQ-MEM-COMPRESSION-001 / H-MEM-COMPRESSION-001-A`.
These IDs are proposals, not silently substituted for the existing memory
hypotheses. R1 approval and registry admission remain necessary. The authority
for this gate is edition 1.8, section 19.7: source/config hashes, canonical
RQ/H binding and R1 human approval must be bound before FROZEN.

## Question and fixed decision

Can semantic prototype replay use at most 10% of the full raw-replay memory
budget while preserving at least 95% of its retention? This is a narrow
compression claim. Five percent relative loss is the maximum acceptable
loss, not five accuracy percentage points.

After a technically valid complete run, retain SemanticMemory as a candidate
compression component only if the simultaneous non-inferiority and byte
budget gates below pass. Additionally require non-inferiority to matched-byte
raw replay and a positive semantic advantage over random prototypes.
Otherwise de-center SemanticMemory in the default architecture for this task;
retain its implementation as an experimental option. An inconclusive interval
does not prove inferiority, but does not justify retaining a central role.
Missing or invalid data mean NOT_TESTED, not a negative scientific finding.
Changing the task, loss tolerance or denominator requires a new registration.

## Task, seeds, learning and controls

Use Split-MNIST tasks (0,1), (2,3), (4,5), (6,7), (8,9), in that order;
1,000 training and 200 held-out test examples per class. Select the first
eligible examples after a per-class permutation from the paired seed. Store
the exact dataset file hashes and selected indices before evaluation. The
test split never updates memory, normalization, readout, selection or tuning.
Evaluation seeds are 95001–95030; implementation-only fixture seeds 31–33
must use synthetic inputs, not MNIST evaluation outcomes.

Use the existing sparse encoder (pooling 4; thresholds .2,.4,.6,.8),
OnlineSoftmaxReadout learning rate .025, same initial readout per seed,
10,000 update slots (2,000/task); later tasks use 400 replay slots replacing
current-example updates. The replay slot schedule and all test exposure are
identical across replay conditions. No hyperparameter search (zero trials),
no condition-specific training, no extra replay updates. Prototype extraction
may observe each arriving training example once; it cannot revisit discarded
episodes. Charge its computational cost separately, never hide it as free
preprocessing. Freeze the encoder/readout/selection implementation before use.

| Arm | Retained budget | Purpose |
| --- | --- | --- |
| raw_full | B100 | Full raw-replay reference |
| semantic_10 | floor(B100/10) | Compression candidate |
| raw_10 | floor(B100/10) | Essential matched-byte replay baseline |
| random_prototype_10 | floor(B100/10) | Representation-content control |
| no_replay | 0 memory bytes | Same 10,000 slots, current examples only |
| learning_off | 0 memory bytes | Initial readout, no optimizer updates; diagnostic only |

Raw selection uses a seeded reservoir of past training records, never test
performance. Random prototypes match label/task and feature count of the
semantic candidates but sample feature IDs uniformly without access to the
semantic IDs. Memory capacity is bytes, not object count. Underfilled arms
retain unused capacity; they do not receive extra training or information.
The learning-off arm is not presented as a matched-update efficacy baseline.

## Complete 10% accounting contract

Define B100 at each task boundary as the canonical serialized size of every
raw record seen so far, including features, label, task ID, length and index
metadata, plus its replay-selection state. Define B10=floor(B100/10).
The same B10 applies to all three restricted arms, independently of their
actual compression success. Report boundary and peak values, not just final
snapshot size. If header/metadata alone exceeds B10, declare capacity failure.

Serialization is uncompressed, little-endian, schema-versioned: header and
all counts use uint64; labels/task IDs uint32; sorted unique feature IDs
uint32 with uint64 lengths; numeric prototype accumulators float64; integer
support counters uint64. Include all record headers, offsets, membership
lists, provenance IDs needed at runtime, RNG state, lookup indices, retained
episodic buffer, support histograms, pending consolidation state, caches,
eviction metadata and replay cursors. No hidden full raw store, duplicate
representation, external index, pickle compression or disk spill is allowed.
Report a per-category ledger after every update and consolidation operation.
The state serializer must prove that restoring only the charged state
reproduces the next replay selection and update.

The primary budget is replay-memory information, not process RSS. Immutable
encoder parameters and program code are excluded only when byte-identical
across replay arms. The common readout is excluded only with identical
architecture, dtype, allocated bytes and update-slot count; its learned values
may differ. Record its entire state and size separately. Extra trainable
parameters, optimizer buffers or learned encoders are forbidden. One current
input is excluded with identical shape/dtype and no retained copy. Training
data are streamed through a coordinator inaccessible
to arm memory after the current update. Test data stay outside all learners.
Temporary workspaces are capped at B10 additional bytes in restricted arms,
B100 in raw_full; publish peak workspace and combined peak. Python allocator
overhead, shared library memory and whole-process RSS are measured separately.
No claim of tenfold total-RAM reduction may follow from this retained-state
ratio. Offline output logs are write-only to the learner and cannot act as
memory. Any persistent arm-specific auxiliary state belongs in the ledger.

When capacity would be exceeded, use deterministic eviction before the next
update: lowest support, then oldest creation index, then canonical record ID
for prototypes; seeded reservoir order for raw replay. Charge temporary
incoming/consolidation records to the workspace ceiling. Never prune based
on test outcomes. The executable serializer, eviction and peak-accounting
tests are mandatory prerequisites; the existing object-count matching from
CL-003 does not satisfy this contract.

## Outcomes, uncertainty and failure handling

After each task evaluate each learned task. Retention R(seed,arm) is the
unweighted mean final accuracy on tasks 1–4 (800 test examples/task are NOT
assumed: exactly 400/task). Task 5 is excluded from retention and reported
separately as plasticity. Also report taskwise accuracy and forgetting.
Primary non-inferiority contrast per paired seed:
`R(semantic_10) - 0.95 * R(raw_full)`.
Require its lower 95% paired-bootstrap percentile bound >=0, 20,000 resamples,
analysis RNG seed 20261024. Report ratio of means as descriptive only;
if raw_full mean <=0, ratio is undefined and the study is invalid.

Two additional conjunctive gates: lower 95% bound of
`R(semantic_10)-0.95*R(raw_10)` >=0; lower 95% bound of
`R(semantic_10)-R(random_prototype_10)` >0. All three gates must pass;
this intersection rule does not select whichever comparison succeeds.
Also require raw_full mean retention >=0.50 and positive lower 95% bound
against no_replay to establish a functioning replay reference. Thresholds
are prospective engineering choices, not established literature effects.
Thirty seeds is a fixed feasibility choice, not a guarantee of power.

Run all 30 paired seeds, six arms; CPU only, one worker, 2 GiB process RSS,
30 minutes/seed/arm, 90 CPU hours total maximum, 20 GiB output ceiling.
Measure wall time and RSS at least once per second. Exceeding any cap stops
the study with partial artifacts retained. No replacement seeds, retries,
post-hoc exclusions or outcome-dependent stopping. Numerical errors, budget
violations, dataset drift, leaks and missing pairs block positive conclusions.

## Freeze checklist still required

1. Register the proposed RQ/H and obtain R1 human review of this exact text.
2. Implement and test byte serializer, restore/selection equivalence, streaming
   isolation, deterministic eviction, full-ledger peak checks and analysis.
3. Bind clean Git commit/tree, config, dataset/index, source and test hashes,
   environment, seed freshness scan and the review record in a freeze artifact.
4. Obtain separate execution authorization after the complete freeze.

Neither the earlier approval of the research idea nor this chat's request to
prepare the protocol is represented as a scientific R1 review of this new plan.
