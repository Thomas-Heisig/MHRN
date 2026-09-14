# Conversation handover: Stage 5 and Stage 6

Date: 2026-09-14. Source baseline: `8a8422687c7a879550a9f4fc3a484bcfcbfa0533`.
Working branch: `feature/stage5-integrated-nervous-system-20260914`.

## Scope correction

The canonical definitions in `src/dashboard/development_timeline.py` identify:

- Stage 5: integrated artificial nervous system (sensor input, interoception,
  authorized actuation, closed-loop feedback and resource accounting).
- Stage 6: memory and world model (temporal, episodic and semantic memory,
  consolidation, prediction and prediction error).

The latest instruction advances Stage 5. The preceding discussion primarily
concerned Stage 6. This branch does not silently renumber the timeline and does
not replace the previously created Stage-6 branch. Main remains unchanged.

## Decisions retained from the conversation

The six separate research objects are temporal traces, episodic memory,
semantic generalization, consolidation/replay, prediction/error and world
modelling. None can be established merely by the existence of the others.

Multi-timescale architecture is compatible with complementary-learning-systems
hypotheses; it is not proof of a biological implementation. Dedicated error
populations and dendritic mismatch are competing model choices. Environmental
prediction error, activity prediction error and reward require different names,
units and intervention switches.

External LLM predictions must not silently become evidence that the canonical
SNN learned environmental dynamics. Such assistance requires a separately
labelled control arm and provenance. A completed run produces DATA, not
accepted EVID. Engineering, verification and scientific evidence scores must
remain distinct. No consciousness or biological-equivalence claim follows.

## Stage-6 audit handover (not fixed by this Stage-5 increment)

The earlier audit found an event store and observation-only one-step statistical
predictor, rather than a demonstrated neuronally encoded episodic/semantic
memory. The following remain explicit follow-up items and must be rechecked
against their implementation branch before being marked resolved:

1. Align the newer cognition frontend with actual episode-count and prediction
   endpoints; avoid creating a third overlapping cognition view.
2. Preserve categorical/boolean types and separate numeric versus categorical
   errors; do not mix differently scaled measurements without a contract.
3. Persist transition eviction ordering, and test save/load continuation after
   reaching capacity rather than testing only equal dictionaries.
4. Independently control memory read, memory write, predictor inference,
   predictor learning, replay and consolidation.
5. Correct the persistence baseline and distinguish online/prequential scoring
   from a held-out evaluation. Use genuine delays and distractors for neural
   retention rather than only assigning later tick labels to stored answers.
6. Prove causal contribution to behaviour with lesion/shuffle/no-memory controls;
   then evaluate replay, semantic transfer and multi-step action-conditioned
   predictions. Couple cognition persistence to the canonical checkpoint.

Continue existing `RQ-MEM-002` and `RQ-WM-001`. Earlier archived component screens
with `snn_involved=false` and `accepted_evidence=false` are not neural-memory
proofs. The Stage-6 percentage is a status-derived engineering heuristic, not a
fraction of scientific validity.

## Stage-5 changes in this branch

`src/embodiment/loop_contract.py` defines bounded cycle and dispatch bookkeeping.
`ControlledEmbodimentAgent` validates the target against both descriptor and
adapter, reserves attempt budget before I/O, rejects old command ticks and
bounds pending human overrides. Exceptions after dispatch preserve an unknown
physical-effect state and latch the emergency stop. Reset expires episode-local
permissions but cannot clear that stop.

`ControlledSensorAdapter` rejects wrong-source, wrong-modality and stale frames.
`ExperienceEngine` checks frame/action tick alignment and finite input/reward,
prevents overlapping prepares and consumes the cycle before downstream side
effects. A memory-persistence failure after actuation cannot replay that cycle.
These changes extend existing paths; they do not add a parallel embodiment stack.

## Verification boundary

The isolated guard suite contains 29 passing cases in the local work environment,
including 16 seeded adversarial command streams. Modified Python files compile.
The complete repository and its dependency graph were not available locally;
full-repository tests were not executed locally. The dedicated `Stage 5 contract`
workflow runs integration regressions together with existing embodiment,
experience, memory and embodiment-lab tests against the committed source. Its
observed result, not this document, determines CI status.

The new integration tests use deterministic adapters and a test network; they
must not be described as real-SNN experiments or independent replications.
No maturity percentage, scientific evidence status or release version is promoted
by this increment. See `research/specifications/STAGE5_CLOSED_LOOP_CONTRACT.md`
for acceptance criteria and the remaining experimental programme.
