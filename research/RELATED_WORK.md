# MHRN Related Work and Mechanism Provenance

**Stand:** 2026-10-04  
**Purpose:** map external scientific precedents to MHRN mechanisms without converting literature claims into MHRN evidence.

This document is an attribution and research-planning artifact. A paper listed here supports only the stated external proposition. It does not validate the MHRN implementation.

## Citation states

- **VERIFIED** — bibliographic identity and the cited proposition were checked against an authoritative publisher/index source.
- **CANDIDATE** — relevant lead, but not citation-ready until bibliographic and claim-level verification is complete.
- **QUARANTINED** — a name/claim was encountered in notes or AI-assisted research but no sufficiently reliable source was resolved. Do not cite it as fact.

## Plasticity, embodiment, and simulation comparability

### VERIFIED — spike-timing plasticity

Bi and Poo (1998) experimentally describe timing-dependent potentiation and
depression in cultured hippocampal neurons; Song, Miller, and Abbott (2000)
analyze competitive outcomes of an STDP rule in a model network. These sources
motivate measuring timing, controls, and resulting function separately. They do
not establish that MHRN's specific `a_plus`, `a_minus`, reward schedule, or
network workload is biologically representative.

### VERIFIED — homeostasis and plasticity stability

Turrigiano (2012) reviews local and global homeostatic synaptic plasticity.
Zenke and Gerstner (2017) discuss compensatory processes operating over
multiple timescales. Together they motivate reporting weight-bound occupancy,
active-weight fraction, functional activity, and intermediate trajectories;
being finite and inside bounds alone is not a functional stability result.

### VERIFIED — learning and embodiment context

McClelland, McNaughton, and O'Reilly (1995) describe complementary learning
systems as a model of hippocampal/neocortical learning and memory. Kirkpatrick
et al. (2017) study catastrophic forgetting in sequential artificial neural
network tasks. Brooks (1991) argues for situated, task-grounded intelligence
without centralized world representations. These are theoretical and
computational precedents for MHRN's learning, retention, and embodiment
questions, not support for any MHRN outcome or a substitute for a registered
SNN experiment.

Bliss and Collingridge (1993) review hippocampal long-term potentiation as a
synaptic memory mechanism. O'Regan and Noe (2001) develop a sensorimotor account
of vision. These sources motivate testable memory and sensorimotor questions,
but do not establish that a particular MHRN weight change stores a memory or
that the current Playground loop is embodied cognition.

### VERIFIED — network organization, emergence, and preregistration

Watts and Strogatz (1998) formalize small-world network properties; Tetzlaff
et al. (2010) study self-organized criticality during development in cultured
neuronal networks and a specific homeostatic growth model. They provide
measurable topology/activity concepts, not evidence for MHRN's five-dimensional
embedding or spontaneous functional modules. No source located here supports a
special 5D performance or cognition advantage; `RQ-5D-*` remains an empirical
comparison question.

Nosek et al. (2018) explain how preregistration separates predictions from
postdictions. This supports the project rule that a frozen protocol precedes
confirmatory runs; it does not resolve MHRN's incomplete holdout runner or
pending human reviews.

### VERIFIED — neural simulation tools and comparison methodology

Brette et al. (2007) review spiking-neuron simulation tools and strategies.
Stimberg, Brette, and Goodman (2019) describe Brian 2; Gewaltig and Diesmann
(2007) describe NEST. Tikidji-Hamburyan et al. (2017) report a comparative
study of brain-network simulation software, while Manninen et al. (2018)
discuss reproducibility, replicability, and comparability of computational
neuroscience tools. These references support careful workload matching and
reporting, not a transferable ranking of raw simulator throughput.

The MHRN Stage-3 benchmark receipts do not yet implement a Brian 2, NEST, or
Norse head-to-head. Such a comparison would first need matched neuron/synapse
semantics, topology, spike/reward schedule, precision, hardware, thread count,
and warm-up/measurement policy. The present deterministic object-graph
benchmark is an MHRN engineering profile only.

### Research-question source map

| MHRN research area | Literature anchors | Boundary |
|---|---|---|
| `RQ-STDP-*`, `RQ-SNN-004/005` | Bi and Poo (1998); Song et al. (2000); Eshraghian et al. (2023) | Timing rules and SNN learning methods; no MHRN efficacy result |
| `RQ-HOM-*`, Stage 3 stability | Turrigiano (2012); Zenke and Gerstner (2017) | Stability mechanisms motivate measurements; do not validate MHRN parameters |
| `RQ-GEN-001`, `RQ-LIFE-001` | McClelland et al. (1995); Kirkpatrick et al. (2017) | External memory/continual-learning context; MHRN holdout evidence remains open |
| `RQ-MEM-001` | Bliss and Collingridge (1993); McClelland et al. (1995) | LTP and complementary-learning context; no MHRN memory claim |
| `RQ-EMB-001` | Brooks (1991); O'Regan and Noe (2001); Stimberg et al. (2019) | Situated control and sensorimotor theory as design context |
| `RQ-SELF-*`, self-organization | Watts and Strogatz (1998); Tetzlaff et al. (2010) | Graph/criticality concepts; not proof of spontaneous MHRN modules |
| `RQ-5D-*` | Watts and Strogatz (1998) | General graph measures only; no external 5D advantage source identified |
| Preregistration / confirmation boundary | Nosek et al. (2018) | Supports a priori protocol/analysis distinction; does not replace human review |
| `RQ-PERF-001`, `RQ-SCALE-001`, Stage-3 scale | Brette et al. (2007); Gewaltig and Diesmann (2007); Stimberg et al. (2019); Tikidji-Hamburyan et al. (2017); Manninen et al. (2018) | Tool design and comparison methods; not a matched MHRN benchmark |

This source-map update closes bibliographic/attribution gaps only. It does not
complete RQ measurement contracts, the reported incomplete conceptual-audit
assessments, outstanding human reviews, independent replication, Alpha.7
release approval, or any EVID decision. Those require their own artifacts and
accountable reviewers; citations cannot substitute.

## 1. Episodic-to-semantic consolidation / complementary learning

### VERIFIED — D'Alba et al. (2025)

D'Alba, F.; et al. **Semantization of memories in a hippocampal-cortical spiking neural network.** *Neurocomputing* 640 (2025), 130323. DOI: `10.1016/j.neucom.2025.130323`.

**Relevant precedent:** an explicitly modeled episodic-to-semantic consolidation process with hippocampal reactivation / sleep-like replay and cortical learning. The work is relevant to MHRN Stage 6 because it demonstrates that a memory module or statistical summary alone is not equivalent to a semantization mechanism.

**MHRN consequence:** Stage 6 must keep `semantic_memory` open until an explicit mechanism, controlled replay/consolidation protocol and appropriate ablations exist. The present bounded episodic store must not be described as completed semantic memory.

### VERIFIED — Shi et al. (2025)

Shi, Y.; et al. **Hybrid neural networks for continual learning inspired by corticohippocampal circuits.** *Nature Communications* 16 (2025), 1272. DOI: `10.1038/s41467-025-56405-9`.

**Relevant precedent:** complementary representations inspired by hippocampal/cortical organization are used for continual learning. This supports treating fast/specific and slower/generalized learning pathways as a research design choice to be tested rather than assumed.

**MHRN consequence:** any future complementary-learning or replay mechanism requires matched baselines and interference/retention measurements. Literature precedent is not evidence that the MHRN mechanism works.

## 2. Predictive coding in spiking networks

### VERIFIED — N'dri et al. (2026)

N'dri, A.; et al. **Predictive coding with spiking neural networks: A survey.** *Neural Networks* 196 (2026), 108371. DOI: `10.1016/j.neunet.2025.108371`.

**Relevant precedent:** the survey distinguishes multiple ways prediction error can be represented in SNNs, including explicit error populations, membrane-potential representations and implicit error coding.

**MHRN consequence:** a telemetry field called `prediction_error` or an observation-only one-step predictor is not, by itself, a predictive-coding mechanism. Stage 6 must name and test the neuronal error representation it actually implements before using stronger predictive-coding language.

## 3. Spiking world models / model-based control

### VERIFIED — Sun et al. (2025)

Sun, Y.; et al. **Spiking world model with multicompartment neurons for model-based reinforcement learning.** *Proceedings of the National Academy of Sciences* 122(50) (2025), e2513319122. DOI: `10.1073/pnas.2513319122`.

**Relevant precedent:** a spiking world-model architecture is used in model-based reinforcement learning with explicit state/dynamics components and planning/control implications. This is materially stronger than passive telemetry or a one-step observational predictor.

**MHRN consequence:** Stage 6 should reserve "world model" claims for a tested internal transition model with action-conditioned or otherwise intervention-relevant predictive structure. A one-step observation predictor remains a foundation/candidate mechanism.

## 4. Multi-timescale plasticity and stability/plasticity control

### VERIFIED — Dong & He (2026 publication)

Dong, X.; He, H. **Astrocyte-gated multi-timescale plasticity for online continual learning in deep spiking neural networks.** *Frontiers in Neuroscience* 19, published 27 January 2026. DOI: `10.3389/fnins.2025.1768235`.

**Relevant precedent:** eligibility-like fast traces are combined with a slower astrocyte-inspired gating process for online continual learning and stability/plasticity regulation.

**MHRN consequence:** MHRN's tick/plasticity/consolidation/development separation is an architectural timescale separation, not evidence that it solves the stability-plasticity dilemma. Astrocyte-inspired gating is a candidate mechanism to compare experimentally, not a required biological truth.

## 5. MHRN mechanism-to-source map

| MHRN topic | External precedent status | What may be claimed now | What remains open |
|---|---|---|---|
| Episodic memory | VERIFIED background | bounded episodic/working-memory foundation exists in MHRN | semantization, replay-mediated consolidation, semantic recall validation |
| Semantic memory | VERIFIED precedent exists externally | planned research target | explicit mechanism + controls + EVID |
| Prediction / prediction error | VERIFIED SNN predictive-coding taxonomy | one-step observation prediction foundation | neuronal prediction-error representation, hierarchy, causal ablation |
| World model | VERIFIED stronger external examples exist | bounded predictor / candidate world-model foundation | multi-step and/or action-conditioned dynamics, planning relevance, held-out validation |
| Multi-timescale learning | VERIFIED external mechanisms exist | MHRN has explicit engineering timescales | causal benefit of slow gating/consolidation under continual-learning controls |
| Replay / sleep-like consolidation | VERIFIED precedent in external work | research requirement/candidate | MHRN implementation and ablation evidence |

## 6. Citation quarantine — do not promote without verification

The following labels appeared in research notes or AI-assisted comparisons but are **not citation-ready in this repository policy until a primary/authoritative source and the exact claimed result are verified**:

- `ArithSpec` with primitives such as `MUL_NORMATIVE`, `MAC`, `ADD_SAT`, `EMIT_01` — **QUARANTINED**. No established scientific/standards source was resolved during the 2026-09-15 audit. Do not call it a reproducibility standard.
- `NeuroEval` as a seven-dimension SNN publication standard — **CANDIDATE/QUARANTINED for normative use**. If a specific project or paper is later resolved, it may be discussed as an external rubric, not automatically as a community standard.
- `DF-ALIF` with the exact basal-dendrite/apical-dendrite claim — **CANDIDATE** pending primary-source verification.
- `Predictive E-prop` (2026) — **CANDIDATE** pending primary-source verification and exact scope.
- `SpikeWorld` (claimed 1.45M-parameter multimodal world model) — **CANDIDATE** pending primary-source verification.
- `ASTRA World Model` / JEPA-spiking claim — **CANDIDATE** pending primary-source verification.
- `Bio-realistic Synthetic Hippocampus` (2025) — **CANDIDATE** pending publisher/source verification before manuscript citation.

Quarantining a lead is not a claim that it is false. It means the project refuses to rely on it until verification is complete.

## 7. Required use in publications

When a manuscript says that an MHRN mechanism is "inspired by", "similar to", "extends", "contrasts with" or "is based on" an external method, the corresponding source must be placed next to the claim and the implementation difference must be described.

For each mechanism section, authors should explicitly separate:

1. **external precedent**;
2. **MHRN implementation**;
3. **MHRN experiment**;
4. **observed result**;
5. **interpretation and limits**.

This structure prevents literature authority, code existence and MHRN evidence from being conflated.
