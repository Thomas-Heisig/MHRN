# Stage 6: memory and world-model contracts

Status: the Stage-6 engineering programme now includes executable functional protocols and an experimental spiking transition candidate. Stage 6 is **not scientifically complete** and no new accepted EVID is asserted.

Merged baseline before this continuation: PR #90 / `c3f8ab745eb501b062ef3a8858f52529e99e61e8`.
Parent questions: `RQ-MEM-002` and `RQ-WM-001`, both still open.

## 1. Scope and epistemic boundary

Stage 6 keeps six research objects distinct:

1. temporal traces,
2. episodic representation and recall,
3. semantic abstraction/generalization,
4. replay/consolidation,
5. prediction and prediction error,
6. action-conditioned world modelling.

The following equivalences are explicitly forbidden:

- episodic memory ≠ replay,
- replay ≠ semantic memory,
- semantic memory ≠ world model,
- environmental prediction error ≠ reward,
- statistical transition model ≠ neural world model,
- exact-context spiking association ≠ generalizing world model,
- replay reactivation ≠ biological sleep,
- offline recommendation ≠ actuation authority,
- passing software tests or DATA ≠ accepted scientific EVID.

No Stage-6 component authorizes LLM-to-core writes, external actuation, emergency-stop clearance, consciousness claims or automatic evidence promotion.

## 2. Current technical programme

| Area | Implemented contract | Current scientific boundary |
| --- | --- | --- |
| Typed prediction/error | deterministic one-step reference, per-field error components, coverage | engineering reference only |
| Memory controls | independent episodic read/write and predictor inference/learning | ablation infrastructure only |
| Neural episodes | sparse real-SNN patterns, context binding, partial-cue retrieval | no hippocampal equivalence claim |
| Semantic prototypes | support across independent episodes and held-out protocol | no human-semantic equivalence claim |
| Replay | ordered/shuffled/no-replay/equal-budget-awake, with real SNN reinjection | controlled reactivation, not biological sleep |
| Prediction error | eligibility-based PE plasticity independent from reward API | functional separation, not biological localization |
| Statistical world model | action-conditioned one-step and bounded multistep rollout | `statistical_multistep_reference_not_neural_evidence` |
| Offline decision benefit | frozen equal-horizon candidate scoring | research recommendation, no actuation authority |
| Continuation integrity | Stage-6 state hash-bound to existing RuntimeBundle manifest | integrity contract, not complete pause/resume proof |
| Spiking transition candidate | exact-context STDP context→next-state association via real SNN spikes | experimental neural candidate, no unknown-state generalization |

## 3. Neural episodic and semantic memory

`NeuralEpisodicMemory` records sparse spike patterns from real network results and binds them to run, episode, tick, sensor and modality. Retrieval uses sparse overlap and can be independently disabled from writing.

`S6-EPI-001` removes the key weakness of the historical delayed-information component screen: the target is encoded in neural spike identity, not read back from stored answer payload. Real distractor neurons fire between encoding and query. Read-off, write-off and episode-shuffle conditions are explicit.

`SemanticMemory` accumulates support only across independent episodes. `S6-SEM-001` separates training and held-out episodes and includes label-shuffle and no-semantic controls. A successful software run establishes that the protocol is executable, not that semantic memory has been scientifically demonstrated.

## 4. Replay and consolidation

`S6-RPL-001` now reinjects stored episodic spike patterns into a real SNN. The protocol compares:

- no replay,
- ordered replay,
- time-shuffled replay,
- equal-budget additional awake reactivation.

SNN-step budgets are recorded and matched. A strong consolidation claim would require ordered replay to provide a retained functional benefit beyond both no-replay and equal-budget-awake controls. Reinjecting patterns is not equivalent to modelling biological sleep physiology.

## 5. Prediction error remains distinct from reward

`PredictionErrorPlasticity` applies environmental error to existing eligibility traces using an independent configuration and statistics. It does not alias or call the reward API.

`S6-PE-001` crosses PE `correct`, `disabled`, and `shuffled` with reward `on/off`. Reward-call counters are part of the protocol so that PE manipulation cannot silently become a reward manipulation.

## 6. Statistical world-model reference

`ActionConditionedWorldModel` remains a transparent bounded reference:

`state + action -> next_state`

It supports deterministic transition selection, bounded action-sequence rollouts, unknown-transition termination and versioned persistence. `S6-WM-001` evaluates frozen multistep predictions against shuffled, persistence and no-model controls. `S6-WM-002` evaluates whether correct frozen rollouts improve an offline utility score against disabled, shuffled and persistence conditions.

The statistical model remains explicitly non-neural and must not be renamed as evidence of a learned spiking world model.

## 7. Experimental spiking transition candidate

`SpikingTransitionWorldModel` introduces the first Stage-6 transition mechanism in which the association itself is represented by real SNN synaptic weights.

Current mechanism:

- one explicit context neuron per discrete `(state_key, action_key)`,
- one output neuron per known next state,
- context→output synapses initialized at zero,
- teacher-forced context-before-target spike timing,
- existing Pair-STDP through `LearningEngine`,
- inference by stimulating only the known context neuron,
- prediction only when a registered output neuron actually spikes,
- no `LearningEngine.update()` during inference or inference cooldown,
- before/after synaptic-weight guard around inference,
- unknown contexts return no prediction instead of guessing.

Scientific marker:

`experimental_exact_context_neural_candidate`

`S6-NWM-001` compares:

- trained spiking candidate,
- untrained spiking control,
- target-shuffled spiking control,
- statistical reference.

Primary outcomes are exact accuracy, prediction coverage, output latency and correct-target synaptic weight margin.

This can support only a bounded claim that an exact discrete transition can be encoded by learned SNN synapses and recalled through output spikes. It does **not** demonstrate distributed state representation, unseen-state generalization, recursive neural multistep prediction, planning or causal world understanding.

## 8. Protocol governance and preregistration

Stage 6 deliberately uses several orthogonal operational protocols for the same RQ. The historical global registry assumes at most one operational protocol per question, so Stage 6 uses a dedicated one-to-many registry rather than rewriting historical campaign semantics.

Dedicated files:

- `research/protocols/STAGE6_OPERATIONAL_PROTOCOLS.json`
- `research/preregistrations/operational/stage6_bundle_v1.json`
- `src/research/stage6_protocol_registry.py`
- `scripts/run_stage6_operational.py`

Registered protocols:

- `S6-EPI-001`
- `S6-SEM-001`
- `S6-RPL-001`
- `S6-PE-001`
- `S6-WM-001`
- `S6-WM-002`
- `S6-NWM-001`

The frozen bundle requires at least three unique seeds for the engineering DATA run, retains negative/null results, binds source/protocol/preregistration hashes, and has `automatic_evidence_promotion=false`. The default confirmatory target remains at least 20 independent initialization seeds unless a power analysis justifies another design.

## 9. Persistence and continuation

The older `RuntimeBundle` remains historically unchanged. `Stage6StateBundle` adds a versioned supplement that SHA-256-binds:

- exact RuntimeBundle manifest bytes,
- `NeuralEpisodicMemory`,
- `SemanticMemory`,
- `ActionConditionedWorldModel`,
- Stage-6 run identity and state-file hashes.

This proves integrity of the associated continuation state. It does not yet prove bit-identical coupled pause/resume behaviour of every Stage-6 mechanism, especially the new spiking transition candidate and any external effects.

## 10. Empirical DATA handling

The operational runner executes all seven protocols under one source revision and writes `scientific_evidence=false`. A separate deterministic analysis script aggregates descriptive means/minima/maxima while retaining the source DATA, protocol and preregistration hashes.

A versioned three-seed snapshot is an engineering/exploratory DATA artifact. It must not close `RQ-MEM-002` or `RQ-WM-001`. Confirmatory interpretation requires the larger independent-seed campaign, uncertainty estimates, retained failures, preregistered decision rules and human scientific review.

## 11. Remaining Stage-6 research closures

The highest-priority remaining scientific work is now:

1. execute the larger confirmatory multi-seed campaign rather than treating the three-seed engineering snapshot as confirmation;
2. sweep episodic delay length, distractor strength, capacity and interference regimes;
3. test whether replay improves later retention/generalization beyond equal-budget awake reactivation;
4. quantify PE main effects and PE×reward interactions across independent seeds;
5. replace the exact-context world-model encoder with distributed state representation;
6. test generalization to unseen but structurally related states/actions;
7. implement recursive neural multistep rollouts and compare them with the statistical reference;
8. test decision benefit of the neural model itself, not only the statistical reference;
9. prove deterministic coupled pause/resume equivalence including all Stage-6 state;
10. obtain independent/human review before any EVID promotion.

Until these requirements are addressed, Stage 6 remains an active research stage rather than a completed scientific result.

## 12. Dissertation linkage

Current additive supplement:

`research/publications/2026-09-15_stage6-memory-world-model_v1.5-addendum/`

Key appendices:

- A — contracts and claim boundaries,
- B — experiment/ablation matrix,
- C — literature synthesis,
- D — reproducibility and EVID rules,
- E — functional protocols and continuation bundle,
- F — experimental spiking transition-model candidate.

Historical dissertation files and binary exports remain immutable. The supplement is an additive revision, not a retroactive rewrite of old evidence.
