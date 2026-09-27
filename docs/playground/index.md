# MHRN Playground

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
