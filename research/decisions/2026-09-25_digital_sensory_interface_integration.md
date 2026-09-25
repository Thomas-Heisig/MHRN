# Digital Sensory Interface — kanonische Integrationsentscheidung

**Datum:** 2026-09-25  
**Status:** accepted architecture/research-programme integration; no DATA, no EVID  
**Scope:** MHRN Gateway Neural Interface, Neural Symbiosis/MSBA, Stages 4–6, Edition 1.8  
**Stage policy:** no new stage and no new research direction

## Decision

The digital interface is integrated into MHRN as a **sensorimotor modality**, not as an external memory substitute, RAG layer or hidden cognitive controller.

The canonical principle is:

> MHRN does not need to internalize arbitrary external content. It must learn how externally available information is transduced, requested, temporally integrated and used for action through the same causal learning framework applied to other sensory modalities.

This decision **does not change the canonical neuron model, SNN core or 11-direction research structure**. It specifies how the existing digital modality is interpreted and tested.

## Architectural placement

| Layer | Role of the digital interface |
| --- | --- |
| Stage 4 | digital sensory transduction, population layout, coding/decoding, modality-specific pathway |
| Stage 5 | query as authorized action; external response as sensory consequence; closed-loop correlation and no-effect/timeout controls |
| Stage 6 | context, delayed credit, prediction error, source transfer and internal state models; external payload storage is not equated with neural memory |
| Stage 7+ | self/other or agency claims remain separate and require their own causal tests |

The existing `MHRN_GATAWAY_NEURAL_INTERFACE.md`, `NEURAL_SYMBIOSIS.md` and MSBA contracts remain authoritative. This decision adds a concrete digital-sensory profile rather than creating a parallel architecture.

## 100 x 100 shared logical bus profile

The first candidate profile is:

```text
profile_id: DIGITAL-SENSORY-BUS-100X100-v0
layout_kind: GRID_2D
shape: 100 x 100
population_size: 10,000 logical channels
role: experimental shared logical query/response address space
status: architecture candidate, not implemented capability claim
```

"Shared" means **the same declared logical address space and representation contract** is available to efferent query patterns and afferent response patterns. It does not require simultaneous use of the same physical neurons or permit unlabelled superposition.

The minimum causal phase contract is:

```text
IDLE
  -> QUERY_EMIT
  -> WAIT_RESPONSE
  -> RESPONSE_ADMIT | TIMEOUT
  -> INTEGRATE
  -> IDLE
```

Every request/response episode must bind at least:

- direction;
- correlation ID;
- logical bus layout/version;
- codec contract/version;
- query-emission tick;
- response-admission tick or timeout;
- source/tool identity and provenance;
- lifecycle/phase state.

This phase separation is a safety and identifiability requirement. Whether timing/gating can later be learned is a separate scientific question.

## Query as action

A digital query is treated as an **efferent action**. The exact query syntax remains outside the canonical SNN and is produced through the declared decoder/boundary contract.

The returned tool/API/database/LLM result is treated as a new **afferent sensory event** and is re-encoded through the declared digital sensory codec.

Therefore:

```text
SNN state
  -> query-pattern/readout
  -> deterministic/versioned decoder
  -> external query/tool action
  -> external response
  -> deterministic/versioned encoder
  -> response SpikeFrame/SpikeFrameSet
  -> SNN
```

The external system is part of the environment. Its content is not silently promoted to neural memory or scientific evidence.

## Efference copy and prediction

An efference copy is the copy of the **issued query/action**, not the answer itself.

The stronger predictive loop is:

```text
issued query/action
  -> efference copy
  -> internal predictor + context
  -> predicted response representation

actual external response
  -> sensory encoding
  -> actual response representation

predicted vs. actual
  -> prediction error
  -> bounded learning/credit path
```

A direct copy of the query into the response channel must not be described as an expected answer unless a registered predictor transforms it into a response prediction.

## Information storage boundary

The interface clarifies, but does not abolish, memory:

1. **External content** may remain outside the SNN and be re-observed when needed.
2. **Transient neural state** remains necessary for context, temporal integration and request/response binding.
3. **Learned structural/procedural state** may reside in synaptic weights, topology, gateway influence, routing and prediction dynamics.
4. Existing Stage-6 episodic/replay mechanisms remain research mechanisms and are not removed by this decision.

The research question shifts from "how much external content can be stored in the SNN?" toward "what reusable neural organization permits efficient access to and use of changing external information?"

## Interface validation gates

Before a strong digital-sense claim, the following must be separated:

### Gate A — representation/binding integrity

A structured relation must survive encode -> neural representation -> decode under predefined role/binding controls. A 100 x 100 grid is not assumed to solve relational binding by itself.

### Gate B — source transfer

Develop with source A; test on a schema-compatible source B containing new content. Source A and its development content are unavailable during the holdout test.

### Gate C — query as learned action

Compare learned query timing/selection against at least fixed-timing, random-query and no-query controls under matched query/resource budgets.

### Gate D — modality routing

Manipulate which modality carries task-relevant information and compare learned/adaptive routing against fixed, random and shuffled-routing controls.

### Gate E — delayed credit

Bind request-specific eligibility to delayed response/outcome without allowing an external model or decoder to write synaptic updates directly.

## New canonical research questions

This integration extends the existing Gateway research family with:

- `RQ-GW-008` / `H-GW-008-A`: source transfer / content independence;
- `RQ-GW-009` / `H-GW-009-A`: query as learned action;
- `RQ-GW-010` / `H-GW-010-A`: adaptive modality routing.

These are **prospective, untested** research objects. They create no DATA or EVID.

## Scientific claim boundary

This integration permits the future claim form:

> A spiking system learned to use a bounded digital sensory channel under preregistered transfer, action-selection and routing controls.

It does **not** permit claims that:

- the 100 x 100 profile is an optimal or universal neural code;
- a VSA/binding solution has already been demonstrated;
- external tools/LLMs are part of the MHRN neural core;
- exact external payloads are stored neurally;
- query generation is already learned;
- digital and physical sensors have identical physics;
- the interface demonstrates cognition, understanding, agency, self-model or consciousness;
- a conventional encoder/decoder becomes unnecessary.

## Dissertation role

Edition 1.8 treats the interface as a cross-stage architectural and research-programme axis:

- genealogy: transition from generic digital gateway to digital sensory loop;
- research object: Stage-4 transduction + Stage-5 action/feedback + Stage-6 temporal credit/prediction;
- empirical programme: the three falsifiable core experiments plus representation/binding prerequisite;
- infrastructure: versioned codecs, layouts, correlation, lifecycle, provenance and deterministic decoder/encoder boundaries;
- integrity: novelty and utility remain open until prior-art review and controlled experiments;
- synthesis/open landscape: the digital interface is a candidate route for learned information use, not an established cognitive capability.
