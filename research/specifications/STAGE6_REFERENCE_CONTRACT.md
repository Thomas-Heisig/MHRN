# Stage 6A: memory and world-model reference contracts

Status: first engineering increment, not Stage-6 completion or accepted evidence.
Integration baseline: `53fec156d6c6fcd9e683526b396d82621288dca4` (PR #82).
Parent questions: `RQ-MEM-002` and `RQ-WM-001`, still open.

## Scope and scientific boundaries

The existing event store and one-step statistical predictor are reference
components. This increment fixes their measurement and continuation contracts;
it does not establish neuronally encoded episodic memory, semantic memory,
consolidation/replay, predictive coding or a multistep world model. There are no
new LLM-to-core writes and no external actuation permissions. Old experimental
DATA keep their generating revision and are not automatically promoted to EVID.

The six research objects remain separate: temporal traces, episodic recall,
semantic generalization, replay/consolidation, prediction/error and world models.
Multiple time scales are compatible with CLS hypotheses, not proof of biological
equivalence. Activity prediction error, environmental prediction error and reward
must not be treated as the same signal.

## Implemented reference contract

| Boundary | Requirement | Tests |
| --- | --- | --- |
| Categories | Preserve bool, string and null without confusing true with the string true | `tests/test_stage6_prediction_contract.py` |
| Numeric fields | Use per-field observation counts; reject nonfinite accumulation before eviction | prediction contract |
| Context | Include sensor and actuator identity; do not share statistics across unrelated interfaces | prediction contract |
| Continuation | Serialize FIFO order explicitly and compare future evictions after sorted JSON roundtrip | prediction contract and memory controls |
| Inference | Do not mutate model state on prediction | prediction contract |
| Errors | Separate per-field numeric absolute errors and categorical mismatch; expose missing/unsupported targets and coverage | prediction contract |
| Ablations | Episodic reading/writing and predictor inference/learning are four separate controls | `tests/test_stage6_memory_controls.py` |
| Persistence reference | Use the previous observed state, independently of episodic retrieval; clear on episode reset and reject different source identity | memory controls |
| UI | Read counts from the summary and predictions from their own endpoint; unknown is not zero | `tests/frontend/stage6-cognition-contract.test.mjs` |

`error()` remains a legacy mixed-unit scalar for compatibility. It is explicitly
NOT accuracy and should not be used as the primary outcome of a new scientific
comparison. Use `error_components()` / `compare_prediction()` and preregister
field units, scale normalization and primary metrics. Missing predictions are
not successful predictions; coverage must accompany any error summary.
The latest component errors are retained in the coupled state. The existing
PredictionRecord and dashboard prediction history still carry the legacy scalar;
a complete per-field research export remains a subsequent integration task.

The support-based uncertainty `1/(1+n)` is a heuristic, not calibrated probability.
Context count is bounded; total field/category diversity and payload bytes are
not yet bounded by a separate schema budget. Composite output fields remain
outside this scalar reference predictor.

## Configuration and changed semantics

All four values live under `experience.memory`:

```yaml
experience:
  enabled: true
  memory:
    enabled: true
    read_enabled: true
    write_enabled: true
    prediction_enabled: true
    learning_enabled: false
```

The last two values must be actual booleans, not strings. The example freezes
predictor updates while preserving inference and episodic storage. Disabling
`read_enabled` or `write_enabled` no longer implicitly disables predictor inference
or predictor learning. The existing frontend read/write switches only affect the
episodic store. Predictor switches are configuration-level in this increment;
there is not yet a separate mutable dashboard endpoint for them.

The one-observation persistence reference remains available when episodic read
is disabled. It must be labelled separately in no-memory experiments, not hidden
inside an allegedly memory-free treatment. A fully memoryless control must also
remove this temporal reference. Scoring uses the pre-action prediction before
model update. Cross-component tick/horizon alignment remains to be formalized
before multi-step experiments; the existing target-tick convention is retained.

## Persistence compatibility warning

Transition state uses `model_version=2`; coupled state uses `schema_version=2`.
Standalone MemoryStore state remains at its existing schema. Version-1 predictor
states lost category types and did not persist FIFO order. Exact restoration
cannot be claimed by guessing those values. Loading legacy coupled/predictor
state therefore fails explicitly and does not edit the original file.

Before using this branch with existing runs, retain a copy of the old state and
its code/config provenance. Rebuild into a NEW v2 destination from original typed
observations in known chronological order, or start a new run. A replay migration
utility is not supplied in this increment. Where the original chronology or raw
observations are unavailable, identity with the old trajectory is unproven.
Coupled save/load tests do not establish canonical runtime checkpoint integration
or restart-safe physical effects.

## Remaining Stage-6 research and implementation

1. Neural episodic representation: unique events, context binding, delayed and
   partial-cue recall after distractors; compare intact, lesioned, shuffled and
   frozen conditions using the real SNN, not database answer lookup.
2. Semantic generalization: common structure across episodes, held-out transfer
   and interference tests; distinguish local semantization from replay-based
   systems consolidation.
3. Replay/consolidation: no replay, ordered replay, time-shuffled replay and
   matched extra online training; control update, activity and resource budgets.
4. Environmental prediction error: test correct, disabled and shuffled error
   modulation independently from reward and activity mismatch.
5. World-model dynamics: action-conditioned multi-step rollouts, unseen contexts,
   frozen hold-out evaluation versus explicitly online/prequential evaluation,
   calibrated uncertainty and demonstrable decision benefit.
6. Full-stack closure: canonical checkpoints, per-field error export, predictor
   controls, reuse of normalization in the older profile view and browser tests.

Use independent seeds as statistical units, held-out task splits, preregistered
primary metrics and failure schedules, code/config hashes and uncertainty
intervals. The older constant-zero persistence experimental arm still needs a
separate correction and new versioned runs. These regression tests do not rerun
or validate the archived cognition experiments. Update scientific chapters only
with the distinction between implemented mechanism, executed DATA and accepted
human-reviewed evidence; do not increase scientific maturity from passing tests.
