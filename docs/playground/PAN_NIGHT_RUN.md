# PAN Playground meta night run

**Status:** PLAYGROUND / exploratory / non-canonical / no DATA / no EVID.

The meta night run is a bounded strategy-learning environment for PAN. Its
purpose is to test whether PAN can learn *where/how to act* (find, store, link)
without counting the external knowledge store itself as neural memory.

## Components

- `MetaTaskGenerator`: deterministic, learnable `find_source`,
  `store_info`, and `link_info` tasks.
- `KnowledgeBase`: dependency-free hashing-vector index plus bounded
  read-only file index.
- `MetaReward`: rewards source/category/relation strategy and execution
  success; it does not reward factual memorization.
- Context policies use current PAN action-population activity as features; reward
  updates a small linear policy over that neural activity rather than a global
  most-frequent-action table.
- `NightRunDaemon`: bounded episode loop, signals, JSONL logging, resumable
  checkpoints and automatic descriptive analysis.
- `NightRunManager`: at most one active in-process Dashboard night run.

## Strategy learning boundary

Task target labels are removed from the vector sent into PAN. Tasks contain
learnable cues (profile/contact, address/location, date/meeting,
definition/method) rather than the literal target category.

Knowledge payloads remain external. PAN stores only policy values, activity
traces and runtime state. The local KnowledgeBase is therefore not evidence of
SNN memory.

## Dashboard API

```text
GET  /api/playground/night
POST /api/playground/night/start
POST /api/playground/night/stop

POST /api/playground/live/<id>/strategy
POST /api/playground/live/<id>/reward
```

The Dashboard Playground exposes **11 · Meta-Nachtlauf** with hours,
maximum episodes, checkpoint interval, seed, Start, Stop and live status.

## Files per night run

Each run is written below `playground_sessions/night_runs/PGNIGHT-*`:

- `episodes.jsonl` — one bounded event record per episode;
- `status.json` — latest operational status;
- `checkpoint.json` — resumable PAN state + policies + KnowledgeBase;
- `knowledge_base.json` — external knowledge/index snapshot;
- `summary.json` — final operational summary;
- `analysis.json` — descriptive morning analysis.

The default checkpoint interval is 600 seconds.

## Start

```bash
python -m src.playground.night_run --hours 8 --max-episodes 10000
```

For a shorter acceptance run:

```bash
python -m src.playground.night_run --hours 0.05 --max-episodes 100
```

## Resume

```bash
python -m src.playground.night_run \
  --hours 8 \
  --max-episodes 10000 \
  --resume playground_sessions/night_runs/PGNIGHT-...
```

The resume checkpoint restores neuron state, pending synaptic currents, tick,
spike totals, global policy state, context policies, reward histories,
KnowledgeBase and task counter.

## Morning analysis

```bash
python scripts/analyze_pan_night.py --session last
```

The report includes episode count, mean reward, first-half/second-half reward,
reward delta and positive-reward fraction.

A rising reward is a Playground observation only. It is **not** DATA, EVID,
proof of cognition, or proof of generalization.

## Current external-source boundary

The Python daemon accepts an optional `gateway_query` callback. The Dashboard
manager currently runs the safe local sources `vector_db` and `file_index`.
It does not create a duplicate Ollama/HTTP client and does not autonomously
browse the Internet.

Gateway/LLM round-trip should be wired through the existing MHRN Gateway /
Neural-Symbiosis boundary, not by adding a second external-I/O architecture.


## Night profile after the live-run diagnosis

The default overnight profile intentionally differs from the older interactive
batch defaults:

```text
neuron_model: pan_adex_5d
pan_bias_current: 15.0
weight: 3.0
clock_mode: dual
growth_enabled: true
growth_activity_threshold: 0.05
thalamic_relay_threshold: 0.0
execution_mode: HYBRID_AUTO
```

The lower synaptic weight is an engineering response to the observed highly
synchronous Playground run. It is **not** a biological optimum or a validated
scientific parameter.

The live GrowthEngine also receives bounded structural edge headroom above the
initial topology size. Without that headroom, a topology initialized exactly at
`edge_budget` could never add a new edge even when growth thresholds were met.

The resumable checkpoint now includes neuron state, pending synaptic currents,
the mutated edge/weight/delay graph, PAN population feedback state, execution
switcher state, GrowthEngine EMA/coactivation/log state, context policies,
KnowledgeBase state and the pending growth events since the last barrier.

## Gateway boundary

The repository's existing `GatewayRuntime` remains experiment-only and
fail-closed; it is not a general unrestricted LLM query endpoint. The night
manager therefore uses local `vector_db` and `file_index` sources by
default. A gateway source is offered only when an explicit authorized
`gateway_query` callback is supplied to `NightRunDaemon`.

No direct Ollama client and no autonomous web access are introduced by the
night-run stack.
