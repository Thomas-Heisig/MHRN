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
- `GET /api/playground/cuda/status`
- `POST /api/playground/cuda/compile`
- `POST /api/playground/cuda/reference`
- `POST /api/playground/cuda/preflight`
- `POST /api/playground/cuda/smoke`
- `POST /api/playground/cuda/rng-parity`

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

The Playground exposes the engineering CUDA progression directly in the frontend:

- CUDA-1.0: PTX assembly, driver loading and occupancy/cooperative-launch preflight.
- CUDA-1.1: CPU determinism plus the D1/D2/D3 parity contract.
- CUDA-1.2: the 17-parameter gate ABI, fail-closed host-buffer validation and single-tick kernel launch path.
- CUDA-1.3: CPU gate-ABI reference, non-trivial one-tick CPU/GPU D2 comparison, repeatability check and epsilon-greedy hash/RNG action parity.
- CUDA-1.4 through CUDA-1.6 remain explicitly marked as not implemented for multi-tick state/delays, GPU plasticity and GPU closed-loop sandbox execution.

The CPU Playground already contains sandbox physics, sensors, actuators, posture analysis and reward triggers. Their appearance in the CUDA console describes GPU-porting status; it does not imply that those application layers already execute on CUDA.

A hosted GitHub runner can validate the CPU contracts and assemble PTX with `ptxas`, but a real kernel execution requires a local NVIDIA device. The CUDA-1.3 Hardware-D2 button therefore reports unavailable/error status when the dashboard server cannot access the NVIDIA driver or toolkit instead of treating code generation as execution.
