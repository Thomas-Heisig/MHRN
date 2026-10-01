# PAN Hyperstate Contract — Draft v0.1

**Contract ID:** `mhrn-pan-hyperstate-v0.1-draft`  
**Status:** DRAFT_NOT_FROZEN  
**Research question:** RQ-PAN-SEM-001  
**Scientific evidence:** none created by this contract  
**CUDA/PAN acceptance:** not established

## Purpose

Wave 5A separates PAN semantics from the Playground implementation before any
further CUDA/PAN promotion. The contract records the state surface, update
ordering and current reference coefficients used by the exploratory PAN
runtime. It does not declare those mechanisms biologically valid, scientifically
supported or backend-equivalent.

The canonical dependency direction is:

```text
src.homeostasis.pan_contract
        ↑
Playground PAN reference

canonical MHRN core  -X->  src.playground
```

## State surface

The draft continuation-critical neuron state is:

- `pan_health`
- `pan_amplitude`
- `pan_energy`
- `pan_activity_ema`
- `pan_consolidation`
- `pan_alive`
- `pan_information_proxy`
- `pan_x_hd`
- `pan_neuron_id`

The executable contract validates finite numeric state, bounded normalized
fields, stable neuron identity and exact hypervector width.

## Update order

The draft order is frozen for engineering comparison only:

1. activity EMA;
2. energy recovery / spike cost;
3. information proxy;
4. stress and health;
5. consolidation;
6. amplitude;
7. hyperstate vector;
8. apoptosis eligibility;
9. population reduction;
10. feedback history.

Any future reordering requires a contract-version change.

## Reference coefficients

The current exploratory coefficients are represented by
`PANFormulaParameters` in `src/homeostasis/pan_contract.py`. Playground no
longer owns those numbers independently.

This extraction is intentionally a semantic inventory, not a validation result.
The current coefficients remain subject to RQ-PAN-SEM-001 review and may be
rejected or revised before a frozen v1 contract exists.

## What is not canonical yet

The following remain outside the frozen contract:

- scientific meaning of the hypervector axes;
- validity of the local surprise proxy as an information-theoretic measure;
- biological interpretation of health, energy or consolidation;
- apoptosis policy as a scientific mechanism;
- feedback projection semantics;
- growth / pruning / neurogenesis semantics;
- CUDA equivalence of PAN update rules;
- checkpoint integration of the full PAN state;
- structural mutation semantics.

## Hardware gate

Physical FE-3/CUDA acceptance remains a separate prior gate. Wave 5A may define
and test a backend-neutral PAN contract while hardware acceptance is pending,
but PAN must not be marked integrated or accepted until the required hardware
and semantic gates both pass.

## Promotion ladder

```text
Wave 5A
  draft state/update contract
        ↓
PAN_CONTRACT_FREEZE_REVIEW
        ↓
frozen PAN semantic contract
        ↓
CPU reference implementation against frozen contract
        ↓
CUDA PAN implementation against same contract
        ↓
D1/D2 PAN parity
        ↓
checkpoint/restore continuation parity
        ↓
only then preregistered scientific PAN studies
```

## Evidence boundary

A passing contract self-check means only that the engineering state schema is
internally consistent. It does not create DATA, EVID, a CLAIM, a biological
equivalence statement or a cognitive interpretation.
