# MHRN Playground

## PAN master documentation

- [PAN complete documentation](PAN_COMPLETE_DOCUMENTATION.md) — consolidated
  architecture, implementation results, scientific boundaries, geometry,
  literature, diagnostics, open design questions and Research Candidates 1–8.


**Status: exploratory only. Not DATA. Not EVID. Not maturity-contributing.**

The Playground is the dedicated non-canonical construction and exploration
surface. It is intentionally separated from the research registry,
preregistration, Human Review and EvidenceEngine paths.

## Governance contract

Every result carries:

```text
class: PLAYGROUND
scientific_evidence: false
data: false
evidence_eligible: false
registry_visible: false
maturity_contributing: false
promotion_path: none
note: Exploratory session. Not part of scientific evaluation.
```

The only scientific transition is:

```text
Playground observation
→ new hypothesis
→ new preregistration
→ freeze
→ new canonical DATA run
→ Human Review
→ optional EVID promotion
```

## Geometry classes

The Playground explicitly separates:

1. **Classical graph topology**
2. **Generic N-D geometry** from 1 to 32 dimensions
3. **Native MHRN 5D** using `x,y,z,d4,d5` plus the canonical
   `pack_coords` representation
4. **Experimental MHRN N-D (>5D)** using explicit tuple coordinates and no
   claim of canonical packed-ID compatibility

The native 5D mode is not labelled superior. It is the architecture default
because it matches MHRN's current core coordinate contract.

## Building blocks

Neuron families include all current Izhikevich functional presets, LIF,
AdEx, HH Na/K/Ca and multi-compartment neurons with optional NMDA plateau.

Network families include feedforward, recurrent, reservoir, bipartite,
dense, random, small-world, scale-free, modular, hierarchical, native MHRN
5D and generic/experimental N-D distance/k-neighbour variants.

Plasticity includes pair/triplet STDP, metaplasticity, eligibility,
three-factor learning, homeostatic scaling, structural and delay plasticity.

## Evaluation

All evaluations are descriptive Playground diagnostics:

- spike timing, ISI/CV, bursts, latency and persistence
- synchrony, Fano and spectrum
- network degree, clustering, paths, components, hubs and cycles
- geometry and edge-distance distributions
- raw N-D occupancy distributions with no quality scale
- plasticity/weight/structural changes
- PCA/effective dimensionality
- runtime and throughput
- seed ensemble variation
- bounded robustness controls

No Playground metric is consumed by the dissertation map, evidence matrix,
registry builder or Stage maturity arithmetic.

## Resource limits

Core configuration limits: 1,024 neurons, 20,000 edges, 2,048 ticks,
1..32 dimensions and at most 8 ensemble runs.

Dashboard API limits: two concurrent simulation requests and 20 run/robustness
requests per 60-second window.

Session persistence: 50 MiB per JSON session, 30-day retention, maximum 200
session files. Session cleanup is confined to `playground_sessions/`.

## Interfaces

Dashboard:

- Builder
- Run & visualization
- Sessions
- Building-block catalog
- Robustness controls

API:

- `GET /api/playground/catalog`
- `GET /api/playground/sessions`
- `GET /api/playground/sessions/{id}`
- `POST /api/playground/run`
- `POST /api/playground/robustness`

Public Python namespace:

```python
from mhrn_playground import Playground
```

Installed CLI:

```bash
mhrn-playground catalog
```

Internal repository modules remain under `src.playground` because this
repository explicitly defines `src` as an actual package namespace.


## PAN-5D context

- [PAN-5D research context](PAN_5D_RESEARCH_CONTEXT.md) — verified component
  literature, integration gaps, bounded novelty wording and research candidates.
- [Glossary](GLOSSARY.md) — PAN/HDC/PID/homeostasis/aging terminology and
  explicit distinction between Spike-Amplitude-Dependent and
  Spike-Agreement-Dependent Plasticity.

These pages are Playground documentation and are not canonical evidence.


## Geometric space

- [Geometry](geometry.md) — independent Ds/Dg contracts, xyz+toroidal
  `geometric_5d`, connection modes, xyz-only delays, diagnostics, literature
  boundaries and Research Candidates 5–8.


## Neural input / output

- [Neural I/O Interface](neural_io.md) — exact BoundaryFrame, codec plane,
  AFFERENT/GATEWAY_AFFERENT input populations, EFFERENT/GATEWAY_EFFERENT
  output populations, decoding and QUERY/WAIT/RESPONSE/TIMEOUT lifecycle.
- [Neural I/O examples](neural_io_examples.md) — scalar, vector and symbolic
  Playground examples.

The exact payload stays outside the SNN and is not persisted in Playground
session results.


## CUDA-1 Playground console

The Playground exposes the engineering CUDA path without promoting it to
scientific evidence.

- CUDA-1.0: PTX assembly, driver loading and occupancy preflight.
- CUDA-1.1: CPU determinism, freeze contracts and D1/D2/D3 definitions.
- CUDA-1.2: explicit 17-parameter gate ABI, bounded buffers and kernel launch.
- CUDA-1.3: fail-closed CPU gate reference versus GPU output, repeatability,
  half-open epsilon-greedy RNG mapping and VRAM cleanup instrumentation.
- CUDA-1.4 through CUDA-1.6 remain pending for multi-tick state/delays, GPU
  plasticity and GPU closed-loop sandbox execution.

CUDA-1.3 rejects NaN/Inf, float32 overflow, invalid uint32/uint64 ABI values,
empty or length-mismatched parity evidence, illegal CUDA block sizes and
host/device copy-size mismatches before launch. Hardware completion still
requires a real NVIDIA run; hosted CI validates CPU contracts and PTX assembly.


## MHRN integration / promotion

The Playground exposes a controlled integration surface:

- `GET /api/playground/integration` — current promotion catalog.
- `POST /api/playground/integration/transfer` — verify an integrated element
  or return the required next promotion gate.

The action never rewrites repository source at runtime. Actual promotion occurs
through reviewed repository changes. The first completed transfer is the
neural-I/O contract family, now canonical under
`src/embodiment/neural_io_contracts.py`; the former Playground contract
module is a compatibility re-export.


### Promotion wave 2

Deterministic codecs/decoders and the framework-neutral neural-I/O area adapter
are now canonical MHRN components. Playground imports them through compatibility
layers. The visible integration panel verifies function identity and the
`NetworkAreaAdapter` protocol without editing source code at runtime.


## Wave 3 — ExecutionBackend and parity/determinism

The Playground remains operational, but execution/parity semantics now come from canonical MHRN modules:

- src/runtime/backend.py — backend-neutral execution protocol;
- src/runtime/determinism — Counter-RNG, same-tick ordering and delay-ring contracts;
- src/verification/parity — D1/D2/D3 comparison and execution fingerprints.

Historical Playground import paths remain available where required, but they delegate to the canonical implementations.

The integration panel reports ExecutionBackend and Parity/Determinism as integrated. CUDA execution itself remains a Wave-4 repository migration and is not performed by the dashboard transfer button.
