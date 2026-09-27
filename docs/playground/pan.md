# PAN in the MHRN Playground

**Classification: PLAYGROUND_PAN — exploratory only.**

PAN is implemented as an optional exploratory state layer on top of the
existing bounded Playground simulator. It does not create a second canonical
MHRN engine and it does not write into the scientific registry.

## Hyperstate

PAN uses a configurable hyperstate with 5..32 dimensions. The first ten
descriptive axes are:

1. intrinsic simulation time
2. excitability proxy
3. plasticity activity
4. local information proxy
5. health
6. neuromodulation proxy
7. energy budget
8. embodied-position projection
9. consolidation proxy
10. network-coupling proxy

Dimensions above ten are intentionally unassigned latent axes.

### Important information-boundary note

Dimension 4 is **not PID**. The current Playground implementation uses a local
surprise proxy and reports:

- `information_axis: local_surprise_proxy_not_PID`
- `pid_status: NOT_IMPLEMENTED`

A scientific PID claim requires an explicit definition of sources/target,
estimator validation, bias analysis and a new preregistered canonical run.

## PAN runtime

The optional PAN layer adds bounded exploratory state variables per neuron:

- health
- spike amplitude
- energy
- activity EMA
- consolidation
- alive/apoptotic state
- hyperstate vector

The simulator can project the previous population hyperstate back into neuron
input through a seeded feedback matrix. This is a Playground closed loop only;
it is not a validated MHRN world model.

## PAN building blocks

Neuron:

- `pan_adex_5d`: AdEx membrane dynamics with the PAN hyperstate layer.

Synapse:

- `pan_stp_stdp`: exploratory release-state depression/recovery plus pair
  STDP.

The same PAN layer can also be enabled with other existing Playground neuron
models via `pan_enabled=true`.

## Research candidates

The Playground exposes PAN observations only as
`DRAFT_IDEA_NOT_PREREGISTERED` candidates. Current candidates include:

- health-modulated homeostatic recovery after perturbation
- hyperstate feedback versus matched no-feedback recurrence
- replacement of the surprise proxy by a formally specified information/PID
  measure
- health/energy/apoptosis transition dynamics under matched stress

These are **not hypotheses in the MHRN Research Registry**.

The only allowed route into science is:

```text
Playground observation
-> research candidate
-> new hypothesis
-> new preregistration
-> freeze
-> new canonical DATA run
-> Human Review
-> optional EVID
```

No Playground result is promoted, copied or counted automatically.
