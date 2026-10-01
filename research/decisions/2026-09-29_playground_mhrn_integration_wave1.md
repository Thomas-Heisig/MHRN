# Decision: Playground -> MHRN Integration Wave 1

**Date:** 2026-09-29  
**Status:** accepted engineering integration decision  
**Evidence status:** engineering provenance only; no DATA/EVID promotion

## Decision

Playground components are promoted into canonical MHRN one contract family at a
time. The dependency direction is fixed:

```text
Playground -> canonical MHRN
canonical MHRN -X-> Playground
```

The first promoted family is the typed neural-I/O boundary contract:

- `BoundaryFrame`
- `CodecContract`
- `PopulationLayout`
- `SpikeEvent` / `SpikeFrame`
- `DecodeResult`
- `NeuralRole` / `InterfacePhase`
- deterministic payload/event/readout digest helpers

Canonical ownership is now
`src/embodiment/neural_io_contracts.py`. The historical
`src/playground/neural_io/contracts.py` path remains as a compatibility
re-export so existing Playground codecs and sessions keep the same class
identity.

## Transfer surface

The Playground Dashboard exposes the integration state through:

- `GET /api/playground/integration`
- `POST /api/playground/integration/transfer`

The transfer action is deliberately **not** a runtime source-code editor. It
verifies already integrated elements or reports the next required gate for a
future reviewed repository change.

## OLD frontend boundary

The OLD workspace remains a compatibility/archive surface. Views stored there
may be referenced in the integration catalog, but they are never promoted
implicitly into MHRN core merely because they remain executable.

## Promotion order after wave 1

1. deterministic neural-I/O codecs after codec/frame-ID semantics freeze;
2. CUDA Driver/NVRTC/ABI/parity behind a canonical ExecutionBackend;
3. learning/plasticity only after the canonical Learning/Synapse contract;
4. closed-loop/environment only after FE-1/FE-2/FE-3 Frozen-Environment gates;
5. PAN hyperstate only after RQ-PAN-SEM-001 semantic freeze.

## Scientific boundary

This decision changes software ownership and interface provenance only. It does
not create a new experiment, scientific DATA, EVID, replication, cognition
claim, PAN validity claim, or CPU/CUDA scientific-equivalence claim.

Future scientific work may use the promoted neural-I/O contract as a shared
measurement boundary, but any resulting claim still requires preregistration,
fresh DATA, controls and Human Review under the existing research governance.
