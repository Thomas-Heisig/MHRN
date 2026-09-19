# Call for Independent Replication — MHRN Stage-1 Experiments

**Open call · 19 September 2026**

MHRN invites independent researchers to reproduce three bounded Stage-1 results from the Multi-Scale Homeostatic Recurrence Network project. The purpose is adversarial, transparent replication: confirming results is welcome, but contradictory, null, partially reproducible and implementation-sensitive outcomes are equally valuable.

The project distinguishes `implementation test != DATA != reviewed EVID != interpretation`. None of the experiments below is presented here as independently replicated merely because the original repository can rerun it.

## Replication targets

| Experiment | Research object | Frozen source / canonical DATA | Current bounded status |
| --- | --- | --- | --- |
| `EXP-S1-TEMP-ORDER-V2-20260919` | `RQ-TEMP-002` / `H-TEMP-002-A` | source `23549a0b75f7019a6146f8513bf6628505acb079`; DATA `aed8e70f9cf227ac07bcec900fc916dcae3a243e` | `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`; Human Review pending; no independent replication |
| `EXP-REC-002-CLEAN-R2-20260919` | `RQ-REC-002` / `H-REC-002-A` | source `947e64c757540ca12bbc5eaad012d5a800f05672`; DATA `df8da50f126f12bdaa9b6d943a6cc68268a42fba` | `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`; Human Review pending; no independent replication |
| `EXP-SNN004-STDP-ASYM-R2-20260919` | `RQ-SNN-004` / `H-SNN-004-A` | source `821d2e0ecf823af3196bda782a69be8260a54943`; DATA `c0fabb0a21dfc5823d102ccaf8726c6b90fd4532` | `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`; Human Review pending; no independent replication |

### 1. Temporal-order task

Canonical materials:
- `research/preregistrations/PREREG-S1-TEMP-ORDER-V2.json`
- `research/experiments/EXP-S1-TEMP-ORDER-V2-20260919/`
- `scripts/run_stage1_temporal_order_v2.py`
- `scripts/verify_stage1_temporal_order_v2.py`

The registered task asks whether a small acyclic six-neuron SNN preserves the temporal order of two distinguishable input channels at designated outputs, and whether deliberately destroying channel identity removes that fixed decoding signal.

A replication should report the intact, identity-destroyed and simultaneous-control results and disclose every departure from the frozen protocol. The original result does **not** establish learning, memory, cognition, biological equivalence, scaling, general temporal reasoning or a 5D advantage.

### 2. Recurrent-delay task

Canonical materials:
- `research/preregistrations/PREREG-REC-002-CLEAN-R2.json`
- `research/experiments/EXP-REC-002-CLEAN-R2-20260919/`
- `scripts/run_rec002_clean_r2.py`
- `scripts/verify_rec002_clean_r2.py`

The registered task tests whether loop delay changes persistence/propagation metrics in the specified small deterministic recurrent SNN at recurrent weight 100 and a 256-tick observation window.

A replication should preserve the registered comparison or clearly preregister any modification. The original result does **not** establish memory, cognition, biological equivalence, scaling, monotonic superiority of larger delays or a 5D advantage.

### 3. Pair-based STDP timing asymmetry

Canonical materials:
- `research/preregistrations/PREREG-SNN004-STDP-ASYM-R2.json`
- `research/experiments/EXP-SNN004-STDP-ASYM-R2-20260919/`
- `scripts/run_snn004_stdp_asym_r2.py`
- `scripts/verify_snn004_stdp_asym_r2.py`

The registered task tests whether the pair-based STDP implementation produces the expected signed and asymmetric weight changes over the frozen pre/post timing curve.

A replication should preserve the timing grid and report all conditions, including `delta_t = 0`. The original result does **not** establish useful learning, task-performance improvement, network-level memory, biological equivalence, scaling or a 5D advantage.

## What qualifies as independent replication

For this call, a strong independent replication should use:

1. an independently controlled execution environment;
2. an independently authored or independently audited execution path;
3. its own preregistration or time-stamped protocol freeze before looking at outcome data;
4. a complete report of software, dependencies, seeds, hardware/runtime details and deviations;
5. publication of confirmatory, contradictory and null outcomes alike.

Using the same repository verbatim is still useful as reproducibility verification, but should be labelled **computational reproduction** rather than independent scientific replication unless the authorship/toolchain independence criterion is also met.

## Submission and attribution

Open a GitHub issue using the **Independent Replication** template and link the external preregistration, code, data and report. Replikators may publish independently. MHRN will link accepted replication records without requiring a positive result and without rewriting the external authors' conclusions.

Suggested archival route:
- preregistration / protocol freeze: OSF Registrations or another time-stamped registry;
- code and release snapshot: GitHub + Zenodo DOI;
- data/report: Zenodo or another DOI-granting repository;
- manuscript/preprint: arXiv when suitable;
- executable reproducibility package: NeuroLibre when suitable.

## Project identity

- Repository: https://github.com/Thomas-Heisig/MHRN
- ORCID: https://orcid.org/0009-0002-9589-1872
- OSF: https://osf.io/p34uq/

This call is an invitation to test the work, not a claim that external replication has already occurred.
