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

The Playground exposes 16 ideas, all with
`DRAFT_IDEA_NOT_PREREGISTERED` status. The final four are:

13. hardware-native emergence;
14. behavioral emergence;
15. hybrid cognition using the existing Gateway/Neural-Symbiosis boundary;
16. layer emergence/specialization.

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
