# MHRN Related Work and Mechanism Provenance

**Stand:** 2026-09-15  
**Purpose:** map external scientific precedents to MHRN mechanisms without converting literature claims into MHRN evidence.

This document is an attribution and research-planning artifact. A paper listed here supports only the stated external proposition. It does not validate the MHRN implementation.

## Citation states

- **VERIFIED** — bibliographic identity and the cited proposition were checked against an authoritative publisher/index source.
- **CANDIDATE** — relevant lead, but not citation-ready until bibliographic and claim-level verification is complete.
- **QUARANTINED** — a name/claim was encountered in notes or AI-assisted research but no sufficiently reliable source was resolved. Do not cite it as fact.

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
