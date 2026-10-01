# CPU Self-Parity Protocol v1

**Protocol ID:** `cpu_self_parity_v1`  
**Preregistration:** `PREREG-CPU-PAR-001`  
**Research question:** `RQ-CPU-PAR-001`  
**Hypothesis:** `H-CPU-PAR-001-A`  
**Status:** frozen design; execution not yet authorized  
**Backend scope:** CPU only  
**Scientific evidence:** none created by this protocol document

## Purpose

Test exact deterministic self-parity of the canonical CPU network path before using CPU results as the reference arm of later cross-backend studies.

This study is intentionally narrower than CPU/CUDA parity. It does not test performance, PAN, learning quality, structural plasticity, cognition or biological validity.

## Frozen construction contract

Each seed creates one independent network realization with:

- point-neuron CPU execution only;
- 256 neurons;
- fixed five-dimensional coordinate bounds `(8, 8, 8, 8, 8)`;
- 8 directed outgoing connection attempts per neuron from the seeded construction RNG;
- self-connections disabled;
- parallel connections disabled;
- integer delays in the frozen range 1..7 ticks;
- `dt = 1 ms`;
- 1000 simulation ticks;
- one deterministic external drive schedule derived only from the frozen protocol and seed;
- structural mutation disabled;
- STDP disabled;
- reward learning disabled;
- PAN hyperstate disabled.

The execution runner must materialize the resolved configuration and its SHA-256 before the first scientific run. Any implementation detail required to resolve the above contract must be frozen before execution authorization and may not be selected after inspecting outcomes.

## Paired-repeat design

For every frozen seed `910001..910020`:

1. construct a fresh CPU network as replicate A;
2. execute the complete 1000-tick protocol;
3. discard process-local object identity;
4. construct a fresh CPU network as replicate B from the same frozen inputs;
5. execute the complete 1000-tick protocol;
6. compare the two runs.

No checkpoint from replicate A may initialize replicate B.

## Primary outcomes

Both are co-primary:

1. exact ordered spike-event sequence equality;
2. exact canonical final-state digest equality.

A primary mismatch on any seed is a failure of exact CPU self-parity for this protocol. The analysis must report the first mismatching tick and mismatch class where available.

## Secondary diagnostics

- per-tick spike digest;
- terminal pending-event/delay-queue digest;
- execution fingerprint repeatability;
- first differing canonical state field for a mismatch.

Wall-clock timing, object addresses, log timestamps and telemetry collection latency are explicitly excluded from the scientific state digest.

## Governance

- structural approval mode for this study: `DISABLED`;
- no runtime policy changes;
- no post-hoc seed replacement;
- no early stopping;
- AI may assist interpretation only;
- DATA do not become EVID without Human Review;
- the protocol must bind the exact source commit/config digest before execution.

## Interpretation boundary

A complete exact match would support only the bounded statement that the specified CPU protocol is self-reproducible over the 20 frozen seeds. It would not establish CUDA parity or general determinism outside the registered configuration space.
