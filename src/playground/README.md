# MHRN Playground — NON-SCIENTIFIC EXPLORATION ONLY

> **This subsystem is not scientific DATA, not EVID, not a registry source and
> not a contributor to Scientific Maturity.** Every observation must be
> reformulated, preregistered and re-executed through the canonical research
> workflow before it can support a scientific claim.

Every run is forced to:

- `class: PLAYGROUND`
- `scientific_evidence: false`
- `data: false`
- `evidence_eligible: false`
- `registry_visible: false`
- `maturity_contributing: false`
- `promotion_path: none`
- `note: "Exploratory session. Not part of scientific evaluation."`

## Isolation

All Playground-owned persistence passes through `PlaygroundIsolation`.
Writes into `research/` or `src/research/` are rejected with
`PlaygroundIsolationError`. Sessions live only under
`playground_sessions/`, which is ignored by Git.

The canonical Registry and Stage-1 maturity files are not modified or extended
to know about Playground sessions; tests prove that Playground execution leaves
those artifacts byte-identical and that unrelated JSON is ignored by the
typed ResearchRegistry loader.

## Public namespace

Internal implementation follows the repository package layout under
`src.playground`. External callers should use:

```python
from mhrn_playground import Playground
```

The installed CLI entry point is:

```bash
mhrn-playground catalog
```

## Neuron building blocks

- Izhikevich RS, FS, intrinsically bursting, chattering, low-threshold
  spiking, resonator, sensory and motor
- LIF
- AdEx
- Hodgkin-Huxley Na/K/Ca
- multi-compartment linear dendrites
- multi-compartment with NMDA plateau

No model is recommended by the Playground.

## Network and geometry building blocks

Classical / graph:

- ring, 2D grid, 3D grid
- random, dense, bipartite
- feedforward and explicit input-hidden-output
- recurrent and reservoir/liquid-state style
- small-world, scale-free, modular, recurrent modular
- recurrent small-world and hierarchical

Geometry:

- **native MHRN 5D** using `(x,y,z,d4,d5)` and
  `src.core.spatial_index.pack_coords`
- native MHRN 5D distance connectivity
- native MHRN 5D k-neighbour connectivity
- shuffled 5D control
- generic N-D grid, distance and k-neighbour variants for **1..32 dimensions**
- experimental MHRN-style N-D variants above 5D using explicit tuple IDs only

The >5D MHRN-style modes deliberately do not claim that the canonical packed
Brain5D storage contract already supports more than five dimensions.

## Synapses and plasticity

Synapses include static, pair-STDP, triplet-STDP, quantal/STP,
eligibility-trace, three-factor and delay-plastic variants.

Plasticity includes pair-STDP, triplet-STDP, metaplasticity,
eligibility-trace, three-factor, homeostatic scaling, structural plasticity
and delay plasticity.

All are bounded exploratory kernels, not canonical scientific mechanisms.

## Descriptive analyses

Each run can expose:

- ISI, CV(ISI), burst intervals
- first-spike latency, persistence and propagation proxies
- synchrony, Fano factor, population spectrum
- degree distribution, hubs, clustering, path length, components and cycles
- edge-distance distributions
- weight change, potentiation/depression, saturation and structural edits
- PCA explained variance, effective dimensionality and dimension variance
- raw N-D occupancy distribution without good/bad or quality semantics
- runtime, neuron-update and spike throughput
- seed-to-seed ensemble variation

The robustness suite adds coordinate shuffle, random-graph control,
dimension ablation, neuron-dropout and stimulus-perturbation controls. These
comparisons are still non-preregistered Playground observations.

## Resource and API limits

One UI/API configuration is bounded to:

- 1,024 neurons
- 20,000 directed edges
- 2,048 ticks
- 1..32 dimensions
- up to 8 seed-ensemble runs

Dashboard API execution is additionally bounded to:

- at most **2 concurrent** simulation requests
- at most **20 run/robustness requests per 60-second window**

Persisted sessions are bounded to:

- **50 MiB per session**
- **30-day retention**
- **200 session files maximum**

Pruning affects only files under the dedicated Playground session directory.

## Dashboard

The dashboard exposes a separate **Playground** area. Its persistent banner
states that the mode is exploratory, non-scientific and has no EVID binding.
The Builder repeats that model and topology choices have no scientific
priority. MHRN 5D is the default only because it mirrors the project
architecture, not because the UI ranks it as superior.

## CLI examples

```bash
mhrn-playground list-models
mhrn-playground list-topologies
mhrn-playground run --topology mhrn_5d --neurons 128 --edges 512
mhrn-playground run --topology generic_nd --dimensions 8
mhrn-playground robustness --topology mhrn_5d
mhrn-playground replay PG-...
mhrn-playground visualize PG-... --projection 5d
```


## PAN master documentation

The consolidated PAN entry point is:

- `docs/playground/PAN_COMPLETE_DOCUMENTATION.md`

It combines architecture, implemented mechanisms, current implementation
results, geometry, literature context, scientific boundaries, open questions
and all eight Research Candidates.

## PAN exploratory layer

The Playground contains an optional PAN hyperstate layer with bounded health,
energy, aging/apoptosis, variable spike amplitude, closed-loop hyperstate
feedback and 5..32D state vectors.

This is classified as `PLAYGROUND_PAN`. It is not DATA, not EVID and does not
change Scientific Maturity. The current information axis is a local surprise
proxy, **not PID**. Potentially useful observations are exposed only as
`DRAFT_IDEA_NOT_PREREGISTERED` research candidates.

See `docs/playground/pan.md` for the full boundary and transition contract.


## PAN research context and glossary

The literature/background layer is descriptive only and is kept outside the
canonical Research Registry.

- `docs/playground/PAN_5D_RESEARCH_CONTEXT.md` — verified component literature,
  integration gaps, bounded novelty wording and testable research directions.
- `docs/playground/GLOSSARY.md` — terminology for PAN, HDC/VSA, PID, homeostasis,
  aging/apoptosis and the two distinct SADP meanings.

The literature context reports a targeted-search result, not a proof of novelty.


## Independent geometric space

The Playground now distinguishes PAN state dimensions `Ds` from an independent
geometric space `Dg`.

The `geometric_5d` topology uses normalized Cartesian `x,y,z` coordinates
plus two cyclic torus coordinates `a,b`. It supports a literal additive
mixed metric and a separate shortcut-union mode. Conduction delays use xyz
distance only.

Dynamic positioning, PID-driven geometry, neurogenesis, adaptive myelination
and Klein-bottle identification remain explicitly unimplemented research
candidates.

See `docs/playground/geometry.md`.


## Neural input / output interface

The Playground implements a bounded reference form of the already documented
MHRN Gateway Neural Interface.

Core contract:

```text
Exact Boundary
-> Codec
-> AFFERENT / GATEWAY_AFFERENT
-> SNN
-> EFFERENT / GATEWAY_EFFERENT
-> Decoder
-> Playground Output
```

Raw payload bytes remain outside the SNN and are never persisted in the
Playground result. The interface records only checksum/provenance metadata.

Tools and actuators are never executed from this Playground interface.

See:

- `docs/playground/neural_io.md`
- `docs/playground/neural_io_examples.md`


## Generative PAN runtime

The isolated Playground now contains a settings-derived PAN gate schematic,
a deterministic dual event/continuous reference scheduler, bounded
event-driven structural growth, a CUDA-memory budget estimator and optional
compressed SSD offload.

Important implementation boundaries:

- generative neurogenesis uses fixed-capacity reactivation of apoptotic slots;
  it does not expand the runtime population beyond configured `n_neurons`;
- the 2 GiB default CUDA budget is an estimator in the Python reference
  backend, not a claim that a CUDA allocation of that size was executed;
- SSD offload is synchronous and remains below
  `playground_sessions/pan_offload/`;
- persistent CUDA kernels, Dynamic Parallelism, SM-topology coupling and
  thermal-feedback coupling are not implemented;
- gate emergence, dual-mode consistency, generative growth and memory scaling
  remain `DRAFT_IDEA_NOT_PREREGISTERED` research candidates.

The existing Playground safety limits remain unchanged: 1,024 neurons and
20,000 directed edges per UI/API configuration.


## Runnable PAN learning stack

The Playground now contains a runnable reference learning path in addition to
the existing PAN state/growth work:

- functional thalamic-style relay/attention gating;
- 2..12 conditioned cortical layers (default 6) with optional plastic gains;
- reward-modulated behavioral policy learning;
- policy feedback into output/action populations;
- explicit reuse of the existing `NetworkAreaAdapter`, Gateway Runtime, MSBA
  and Neural I/O contracts.

No duplicate `llm_interface.py` or `data_interface.py` is introduced.
Language models, databases, files, web/API sources and other external systems
remain behind the existing digital/peripheral boundary.

A learning run can be configured through `PlaygroundConfig` or the Dashboard:

```python
from mhrn_playground import Playground

pg = Playground(
    pan_enabled=True,
    cortical_layers_enabled=True,
    cortical_layer_count=6,
    cortical_plasticity=True,
    thalamic_gating_enabled=True,
    behavior_learning_enabled=True,
    behavior_action_count=4,
    behavior_target_action=0,
    behavior_episode_ticks=16,
    behavior_learning_rate=0.05,
)
result = pg.run(256)
```

Inspect `result["behavioral_learning"]`,
`result["cortical_organization"]` and `result["thalamic_gating"]`.

The optional `cuda_8gb_balanced_plan` hardware profile is a capacity target,
not a CUDA execution backend. Register-native/PTX kernels and Dynamic
Parallelism remain NOT IMPLEMENTED.

See `docs/playground/PAN_COMPLETE_ARCHITECTURE.md`.


## Switchable execution modes

The Playground supports a separate execution policy:

- `EVENT_ONLY`: sparse neuron stepping for currently driven neurons;
- `TICK_ONLY`: all live neurons are stepped every tick;
- `HYBRID_AUTO`: activity-driven switching with hysteresis and minimum dwell.

The Dashboard uses `HYBRID_AUTO` as the interactive default. The Python
configuration default remains `TICK_ONLY` to preserve earlier Playground
session behavior.

Transitions use the same shared state. Optional transition hashes verify that
the policy switch itself did not mutate state. They do **not** prove that event
and tick trajectories are mathematically equivalent.

`EVENT_ONLY` is not yet an end-to-end O(events) backend: global plasticity and
maintenance bookkeeping can still be dense. Performance is therefore
`NOT_BENCHMARKED`.
