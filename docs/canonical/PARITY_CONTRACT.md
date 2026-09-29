# Canonical Parity and Determinism Contract

Status: canonical engineering contract, Wave 3  
Date: 2026-09-29  
Scientific evidence: none created by this document  
Contract version: mhrn-parity-v1

## Purpose

Parity is a versioned verification surface, not a claim that two implementations are scientifically interchangeable. Canonical code lives under src/verification/parity and src/runtime/determinism.

Playground may execute comparison runs, but it is no longer the authority for D1/D2/D3 semantics.

## D1 — discrete event parity

D1 compares ordered spike/event sequences.

For the canonical contract:

- zero mismatches are allowed for exact D1;
- empty evidence fails closed;
- event order is part of the comparison.

A digest may summarize a sequence, but the underlying event contract remains explicit.

## D2 — continuous state parity

D2 compares registered continuous state vectors using preregistered tolerances.

The default Wave-3 compatibility thresholds preserve the existing CUDA reference limits:

- voltage max absolute error: 1e-4;
- weight max absolute error: 1e-4.

The numeric comparator rejects:

- unequal vector lengths;
- empty vectors;
- NaN;
- positive or negative infinity.

This explicitly prevents NaN from disappearing through nan-aware aggregation.

## D3 — behavioral and causal parity

D3 is split conceptually:

- D3a: frozen boundary/action/reward control;
- D3b: live backend-produced actions in a deterministic frozen world;
- D3c: full causal environment trajectory parity.

Wave 3 provides exact action/target/reward comparison and optional body-trajectory digest comparison. D3c remains dependent on the Frozen Environment Contract and is not claimed as completed by Wave 3.

## Execution Fingerprint

An execution fingerprint is SHA-256 over canonical serialized identity inputs:

- seed;
- canonical configuration hash;
- backend name;
- backend version;
- tick count;
- parity contract version.

Stable JSON serialization uses sorted keys, compact separators and disallows NaN/Inf. Wall-clock time, dict insertion order and process-local object identity are excluded.

The fingerprint identifies the declared execution configuration. It is not a digest of scientific truth and does not replace a full state digest or checkpoint.

## Determinism primitives

Wave 3 makes three primitives canonical:

1. Counter RNG release_uniform(seed, tick, edge), independent of traversal/thread scheduling.
2. Same-tick ordered update rule: pre then post when source_id <= target_id, otherwise post then pre.
3. Delay ring semantics: ring size max_delay + 1, immutable send-time emissions and deterministic modulo slot selection.

The Playground plasticity oracle imports these primitives from src/runtime/determinism.

## Fail-closed rule

If required comparison state is missing, non-finite, empty or structurally incompatible, parity fails. It must never silently downgrade scope or substitute another backend.

## Research boundary

RQ-CUDA-PAR-001 asks whether CPU and CUDA are actually equivalent under a preregistered model domain. RQ-CUDA-PAR-002 asks whether the verification method itself reliably identifies the specified divergence classes.

Wave 3 implements the method contract. Both research questions remain open until their prospective DATA requirements are satisfied.
