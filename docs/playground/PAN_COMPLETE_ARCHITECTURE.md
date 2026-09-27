# PAN-5D complete Playground architecture

**Status:** PLAYGROUND / exploratory / non-canonical / no DATA / no EVID.

This document is the implementation-status companion to the PAN design. It
separates runnable reference mechanisms from hardware target plans and reuses
the existing MHRN Gateway / Neural Symbiosis contracts instead of creating
parallel LLM or data interfaces.

## 1. Implemented runnable reference path

The Playground can currently compose and execute:

- PAN hyperstate (5..32 dimensions);
- geometric 5D topology with xyz plus toroidal a/b axes;
- settings-derived gate schematics;
- continuous or deterministic interleaved dual event/continuous scheduling;
- bounded synaptogenesis, path formation, pruning and fixed-capacity slot
  reactivation;
- functional thalamic-style relay/attention gating;
- fixed cortical layer assignment (default six layers) with plastic layer gains;
- reward-modulated behavioral policy learning;
- existing Neural I/O codec/lifecycle contracts;
- existing NetworkAreaAdapter / Gateway Runtime / MSBA interface architecture;
- optional compressed Playground SSD offload;
- CUDA memory-layout estimation.

A Playground run may therefore both **run and learn**. The behavioral learner
updates policy parameters from scalar reward and feeds the learned policy back
into the action/output population as a bounded current bias.

It stores policy parameters, activity traces and reward history. It does not
persist exact external payloads as learned facts.

## 2. Existing interface architecture is reused

No new LLM-specific or Internet-specific PAN interface is created.

The architectural route remains:

```text
PAN / MHRN activity
  -> existing Gateway action boundary
  -> NetworkAreaAdapter / Neural Symbiosis
  -> MSBA modality (audio | vision | digital)
  -> exact external boundary/tool plane
  -> external service, data source or model
  -> exact response boundary
  -> declared codec
  -> spike representation
  -> PAN / MHRN activity
```

The exact payload remains outside the SNN. In the Playground the external
round-trip itself remains disabled; Neural I/O is a bounded reference path.

## 3. Cognitive organization

### Functional thalamic gating

The Playground implementation provides relay, inhibition and attention gains.
It is a functional control abstraction and explicitly **not** a biological
thalamus reproduction.

### Cortical organization

Neurons can be assigned to 2..12 initial layers (default 6). Layer labels are
conditions. Their gains can adapt with reward/activity. This is an engineering
model of layered organization, not evidence that cortical layers emerged.

### Behavioral learning

The current learner is a deterministic bounded reward-modulated policy
reference with configurable:

- number of actions;
- target action;
- learning rate;
- epsilon exploration;
- episode duration;
- output-current policy bias.

The purpose is to make "behavior instead of payload storage" executable and
testable in the Playground.

## 4. Hardware status

Two selectable profiles exist:

| Profile | Status |
| --- | --- |
| `reference_cpu` | runnable Python reference |
| `cuda_8gb_balanced_plan` | architecture/capacity target only |

The 8-GB profile records the planning assumptions:

- 256 registers per neuron (target);
- about 12,288 register-limited active neurons (estimate);
- about 50 million recommended synapses (estimate);
- 8 GiB nominal / about 6.9 GiB usable-VRAM planning assumption.

These are **not benchmark results**.

The following remain NOT IMPLEMENTED:

- register-native CUDA neuron kernels;
- PTX-native gates;
- persistent gate kernels;
- CUDA Dynamic Parallelism neurogenesis;
- direct SM-topology coupling;
- thermal feedback as PAN health.

Therefore the phrase "CUDA core is the neuron" is a target architecture
hypothesis, not a property of the current runtime.

## 5. Research candidates

The Playground exposes 18 ideas, all with
`DRAFT_IDEA_NOT_PREREGISTERED` status. The final six are:

13. hardware-native emergence;
14. behavioral emergence;
15. hybrid cognition using the existing Gateway/Neural-Symbiosis boundary;
16. layer emergence/specialization;
17. mode-switch consistency;
18. hybrid execution performance.

Nothing in this file registers a hypothesis under `research/`.

## 6. How to run a learning session

In the Dashboard Playground:

1. enable PAN if PAN state dynamics are desired;
2. optionally choose Dual clock and generative growth;
3. enable **Thalamic Gating**;
4. enable **Cortical Organization** and keep six layers;
5. enable **Behavior lernen**;
6. set actions, target action, learning rate and episode ticks;
7. optionally enable Neural I/O to exercise the existing codec/lifecycle path;
8. start the Playground.

The result exposes:

- `behavioral_learning`
- `thalamic_gating`
- `cortical_organization`
- `interfaces`
- `hardware`
- `gates`
- `growth`
- `clock`
- `storage`

The session is still PLAYGROUND and cannot become DATA or EVID automatically.

## 7. Claim boundary

Implemented software can demonstrate that the reference mechanisms execute,
update state and learn the bounded Playground policy task.

It does **not** demonstrate higher cognition, biological equivalence, general
intelligence, CUDA-native emergence, or superiority over simpler baselines.
Those require separately preregistered experiments and canonical DATA.


## 8. Switchable execution: EVENT_ONLY / TICK_ONLY / HYBRID_AUTO

The Playground now exposes a separate execution-policy layer above the existing
clock/event batching machinery.

### Modes

| Mode | Playground reference semantics |
| --- | --- |
| `EVENT_ONLY` | step only neurons with current external, synaptic or PAN-feedback drive |
| `TICK_ONLY` | step every live neuron on every simulation tick |
| `HYBRID_AUTO` | switch between the two engines using moving spike activity, hysteresis and minimum dwell time |

The public settings are:

- `execution_mode`
- `execution_initial_mode`
- `execution_theta_high`
- `execution_theta_low`
- `execution_hysteresis`
- `execution_min_dwell`
- `execution_activity_window`
- `execution_transition_mode`
- `execution_sync_on_switch`
- `execution_log_transitions`
- `execution_log_state_hash`

The Dashboard defaults to `HYBRID_AUTO`; the Python configuration default
remains `TICK_ONLY` for backward-compatible behavior of existing sessions.

### Transition protocol

The current Python backend uses a **shared state** rather than two separately
materialized neuron states. A mode transition therefore changes execution
policy without copying `V/w/H` or other state.

With `execution_sync_on_switch=true`, a deterministic SHA-256 integrity digest
of scalar neuron state plus pending synaptic buffers is calculated immediately
before and after the policy switch. The transition reports PASS only if the
shared state is unchanged by the transition itself.

This checks **transition integrity**, not trajectory equivalence.

```text
EVENT_ONLY vs TICK_ONLY:
  mathematical_equivalence: NOT_CLAIMED
  transition_check: SHARED_STATE_INTEGRITY_ONLY
  trajectory_tolerance_claim: NONE
```

### Important performance boundary

The reference `EVENT_ONLY` implementation performs sparse **neuron stepping**,
but some global maintenance remains dense, including selected plasticity,
trace, PAN and synaptic bookkeeping.

Therefore the current backend does **not** claim `O(events)` end-to-end
runtime, a 25% crossover, or the example millisecond timings from the design
proposal. Those are hypotheses for later profiling.

The result object exposes:

```text
result["execution"] = {
  configured_mode,
  current_engine,
  mode_history,
  transitions,
  transition_count,
  ticks_in_event,
  ticks_in_tick,
  time_in_event,
  time_in_tick,
  avg_activity,
  activity_trend,
  consistency_check,
  equivalence: "NOT_MATHEMATICALLY_EQUIVALENT",
  performance_claim: "NOT_BENCHMARKED"
}
```

Two additional non-registered ideas are exposed:

- `PAN-CANDIDATE-MODE-SWITCH-CONSISTENCY`
- `PAN-CANDIDATE-HYBRID-PERFORMANCE`

The Playground therefore exposes 18 PAN research candidates, all
`DRAFT_IDEA_NOT_PREREGISTERED`.


## 9. Live PAN session and minimal embodied sandbox

The Playground now has a stateful in-process live-session path in addition to
the original bounded batch runner.

### Reanimated PAN-AdEx bootstrap

The `pan_adex_5d` reference model now uses:

- `v_rest = -65 mV`
- `v_t = -55 mV`
- `threshold = -20 mV`
- `reset = -60 mV`
- configurable `pan_bias_current` with a default of `15.0`

The general `adex` Playground model is unchanged. The bootstrap bias is
applied only to `pan_adex_5d`.

The default thalamic relay threshold is `0.0` so enabling functional
thalamic gating cannot create an initial activity deadlock by itself.

### Activity-guarded behavioral learning

Behavioral policy updates now require a configurable minimum activity
(`behavior_min_activity`). Silent episodes receive zero reward and do not
update policy parameters.

The default target mode is `cycle`, which rotates the target through the
configured action space. A fixed target remains available explicitly.

This prevents the previous trivial condition in which a silent network always
selected action zero while action zero was also the fixed target.

### Stateful API

The Dashboard process can host persistent Playground sessions:

```text
POST /api/playground/live/create
POST /api/playground/live/<id>/input
POST /api/playground/live/<id>/step
GET  /api/playground/live/<id>
POST /api/playground/live/<id>/sandbox
POST /api/playground/live/<id>/stop
```

A live session preserves neuron state, pending synaptic currents, learning
state, execution-mode state and recent spike history across calls.

This is an **in-process reference daemon**, not a background system service.
It survives multiple API calls while the Dashboard process remains alive.

### Minimal embodied sandbox

The live session can be coupled to a deterministic 2-D point-mass/spring
stick figure with:

- nine point joints;
- eight spring links;
- four bounded actuator channels;
- nine receptor values;
- ground contact and gravity;
- delayed echo feedback;
- a synthetic motion/contact audio-level proxy.

The current sandbox does **not** yet implement waveform audio/FFT or
ReservoirPy. It also does not create a direct Ollama HTTP client. LLM
communication is deliberately routed through the project's existing Gateway /
Neural Symbiosis boundary when that integration is enabled.

All live/sandbox state remains:

```text
classification: PLAYGROUND
scientific_evidence: false
evidence_eligible: false
registry_visible: false
promotion_path: none
```
