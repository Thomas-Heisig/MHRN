# Stage 6: memory and world-model contracts

Status: engineering Blocks 1–7 implemented or under scoped verification; Stage 6 is **not scientifically complete** and no new accepted EVID is asserted.
Current merged technical baseline: `0ba372bc348fdb7731afea0ad09f5216207ed758` (PR #88, Blocks 1–6 on `main`).
Current continuation branch: `feature/stage6-decision-benefit-dissertation-20260915` (Block 7 and dissertation addendum).
Parent questions: `RQ-MEM-002` and `RQ-WM-001`, both still open with zero accepted evidence.

## 1. Scope and epistemic boundary

Stage 6 contains six distinguishable research objects:

1. temporal traces,
2. episodic representation and recall,
3. semantic abstraction/generalization,
4. replay/consolidation,
5. prediction and prediction error,
6. action-conditioned world modelling.

These objects are related but are not synonyms. In particular:

- episodic memory is not replay,
- replay is not semantic memory,
- semantic memory is not a world model,
- environmental prediction error is not reward,
- a multistep statistical rollout is not evidence of planning,
- alternative-action model rollouts are not by themselves causal counterfactual evidence,
- a passing software test is not scientific evidence.

Multiple time scales are compatible with Complementary Learning Systems hypotheses, not proof that MHRN reproduces hippocampal/neocortical anatomy or function. No Stage-6 component authorizes LLM-to-core writes, external actuation, safety-stop clearance, consciousness claims or EVID promotion.

## 2. Block status

| Block | Contract | Current technical status | Scientific status |
| --- | --- | --- | --- |
| 1 | typed prediction/error metrics and deterministic one-step predictor | implemented and regression-tested | reference DATA/engineering only |
| 2 | independent episodic read/write and predictor inference/learning controls | implemented and regression-tested | ablation infrastructure only |
| 3 | neural episodic representation and partial-cue retrieval from SNN spike patterns | implemented and regression-tested | task benefit after delay/distractors not yet demonstrated |
| 4 | semantic prototypes and bounded replay conditions | implemented and regression-tested | held-out semantization and replay benefit still unproven |
| 5 | environmental prediction-error plasticity separate from reward | merged via PR #87 | functional mechanism; no biological localization/effect evidence |
| 6 | action-conditioned multistep statistical world-model baseline | merged via PR #88; 16/16 scoped regressions + Black/Ruff/Mypy/Pyright passed | `statistical_multistep_reference_not_neural_evidence` |
| 7 | frozen offline decision-benefit evaluator for matched candidate horizons | implemented on continuation branch; scoped verification required before merge | recommendation is research output, never actuation authority |

## 3. One-step reference predictor

The original bounded transition predictor remains a technical baseline. Its contracts include:

| Boundary | Requirement |
| --- | --- |
| Categories | preserve bool, string and null without confusing typed values |
| Numeric fields | per-field observation counts; reject nonfinite accumulation |
| Context | include sensor and actuator identity |
| Continuation | serialize FIFO order explicitly |
| Inference | prediction is read-only |
| Errors | separate numeric absolute error, categorical mismatch, missing/unsupported targets and coverage |
| Ablations | episodic read/write and predictor inference/learning are independently switchable |
| Persistence reference | previous observed state is separate from episodic retrieval |
| UI | counts and predictions use canonical API fields; unknown is not zero |

`error()` is a legacy mixed-unit scalar and is not accuracy. New studies must use separated metrics, state the field scales and report prediction coverage. Support-based uncertainty remains heuristic rather than calibrated probability.

## 4. Neural episodic representation

`NeuralEpisodicMemory` stores sparse spike patterns derived from real network step results and binds them to run, episode, tick, sensor and modality metadata. Partial-cue retrieval uses explicit overlap/coverage criteria and memory capacity is bounded. Read and write controls are separate.

This implementation establishes an inspectable neural-event contract, not functional episodic-memory evidence. `RQ-MEM-002` still requires a delay+distractor task in which the target cannot be answered by directly reading stored sensor payload. A memory-specific lesion must remove any claimed benefit.

## 5. Semantic prototypes

`SemanticMemory` accumulates prototype support over **independent episodes**. Duplicate traces from one episode cannot inflate support. This prevents a trivial within-episode repetition from masquerading as cross-episode abstraction.

The remaining scientific test is held-out generalization: training/prototype episodes and evaluation episodes must be disjoint. Recognition of memorized training patterns is not sufficient evidence of semantic memory.

## 6. Replay and consolidation

`EpisodicReplayScheduler` provides bounded `off`, `ordered` and `shuffled` replay plans and deduplicates episode contributions. Replay can feed the semantic consolidation reference path.

This is not yet biological sleep and does not currently reinject spike sequences into a running SNN. A replay claim requires at minimum:

- no replay,
- ordered replay,
- shuffled replay,
- equal-budget additional awake training,

with update/activity/resource budgets recorded. A result that beats no-replay but not equal-budget awake training does not support a strong consolidation claim.

## 7. Prediction error independent from reward

`PredictionErrorPlasticity` applies an environmental prediction-error signal to existing eligibility traces using its own configuration and statistics. It does not call or alias `LearningEngine.set_reward()`.

Required scientific conditions include prediction error `correct`, `disabled` and `shuffled`, crossed independently with reward `on/off`. Reward counters and values must demonstrate that PE manipulations did not silently alter the reward pathway. This functional separation does not decide whether biological error is represented by dedicated neurons, dendritic compartments or another mechanism.

## 8. Action-conditioned multistep reference model

`ActionConditionedWorldModel` implements a bounded discrete contract:

`state + action -> next_state`

It supports deterministic majority prediction, support-derived heuristic uncertainty, fixed-budget action-sequence rollouts, explicit early termination on unknown transitions, alternative-action comparison and deterministic persistence/restore.

Its scientific marker is deliberately:

`statistical_multistep_reference_not_neural_evidence`

It is therefore a comparison model for future spiking/state-space implementations. It must not be described as a demonstrated neural world model, planning mechanism or causal world understanding.

## 9. Offline decision-benefit evaluation

`OfflineDecisionEvaluator` compares fixed, equal-horizon action-sequence candidates using a frozen multistep model. It:

- rejects mismatched candidate horizons,
- excludes incomplete/unknown rollouts from selection,
- rejects nonfinite scores,
- applies deterministic tie-breaking,
- verifies that evaluation did not mutate model state,
- returns `DecisionRecommendation`, never `ActionCommand`.

The evaluator's marker is:

`offline_reference_evaluator_not_actuation_authority`

This creates the technical substrate for a stronger world-model test: whether correct frozen predictions improve offline choice quality relative to disabled, shuffled and persistence controls. The evaluator itself is not evidence of such a benefit.

## 10. Persistence and compatibility

The one-step transition state uses `model_version=2`; coupled memory/world-model state uses `schema_version=2`. Legacy v1 predictor states did not preserve category types or FIFO order and therefore cannot be assumed to restore exactly. They must be retained with provenance and rebuilt into a new destination from original typed observations in known chronological order, or treated as historical/non-equivalent state.

The multistep reference model has its own explicit versioned state and validates context order, capacity and canonical next-state encodings during restore.

Canonical runtime-checkpoint coupling remains a separate full-stack closure item; successful component persistence tests do not prove restart-safe external effects.

## 11. Required Stage-6 experiments

The dissertation addendum dated 2026-09-15 defines the current preregistration matrix:

- `S6-EPI-001` — neural delay+distractor recall,
- `S6-SEM-001` — held-out semantization,
- `S6-RPL-001` — replay/no-replay/shuffled/equal-budget-awake comparison,
- `S6-PE-001` — prediction-error × reward factorial ablation,
- `S6-WM-001` — frozen held-out multistep prediction,
- `S6-WM-002` — offline decision benefit,
- `S6-NWM-001` — future neural/spiking world model versus statistical reference.

A confirmatory campaign should use independent seeds as statistical units, preregistered primary outcomes, held-out task splits, code/config hashes, uncertainty intervals, explicit exclusion rules and retained null/negative results. A target of at least 20 independent initialization seeds is the default unless a power analysis justifies another number.

## 12. Literature and dissertation linkage

The dated dissertation supplement is:

`research/publications/2026-09-15_stage6-memory-world-model_v1.5-addendum/`

It contains:

- Stage-6 claim boundaries and implementation map,
- a preregisterable experiment/ablation matrix,
- a literature synthesis covering complementary learning systems, spiking semantization, replay, predictive coding and world models,
- reproducibility and EVID-promotion rules.

The curated bibliography is:

`research/literature/stage6_memory_world_model.bib`

Historical dissertation files and binary exports remain immutable. The supplement is an additive scientific revision, not a retroactive rewrite of old claims or evidence.

## 13. Remaining implementation work

The highest-priority engineering/research closures are now:

1. implement and register the real SNN delay+distractor episodic task without payload-answer leakage;
2. add held-out semantic-generalization harness and episode-shuffle control;
3. connect replay to a controlled SNN reactivation experiment, keeping an equal-budget awake comparator;
4. provide registered PE correct/disabled/shuffled × reward on/off experiment execution;
5. create frozen multistep held-out and offline decision-benefit protocols with immutable train/test splits;
6. implement an actual spiking/state-space world-model candidate and compare it against the statistical reference;
7. couple Stage-6 state to canonical runtime checkpoints and expose per-field research metrics in full-stack diagnostics;
8. regenerate research catalogs only from the source registries after any new RQ/H definitions rather than editing generated files by hand.

Until those experiments are executed and independently reviewed, Stage 6 remains an active research stage rather than a completed scientific result.
