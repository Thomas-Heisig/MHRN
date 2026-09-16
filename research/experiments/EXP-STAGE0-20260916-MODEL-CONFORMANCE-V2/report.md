# EXP-STAGE0-20260916-MODEL-CONFORMANCE-V2

**Status:** confirmatory DATA complete  
**Preregistration:** `PREREG-RQ-EVAL-006-V2`  
**RQ:** `RQ-EVAL-006`  
**Hypotheses:** `H-EVAL-006-A`, `H-EVAL-006-B`, `H-EVAL-006-C`

## Result

All endpoints frozen before the confirmatory run were satisfied on the disjoint validation seeds `21001`, `21002`, `21003`.

### Izhikevich-2003

The matched one-step split-Euler transition agreed with Brian2 for all 192 confirmatory samples. Spike decisions were identical. The worst observed pre-reset voltage error was `6.821210263296962e-13`, well below the frozen `1e-8` threshold. Pre/post-reset recovery and post-reset voltage errors were also below `1e-12`.

This supports **local transition, threshold and reset conformance**. It does not erase the historical V1 free-running 1000-tick negative. V1 remains a documented result showing that microscopic floating-point differences can amplify in a nonlinear free-running trajectory until later spike timing diverges.

### LIF-current-v1

For the canonical alternative-model setting `refractory_ticks=0`, all three 1000-tick/5-cell comparisons had identical spike events. Worst membrane error was `7.105427357601002e-15`.

For the optional nonzero refractory extension, all nine frozen mapping runs passed. At `dt_ms=1.0`, the validated semantic mapping is:

| MHRN | Brian2 |
| ---: | ---: |
| `refractory_ticks=1` | `2 ms` |
| `refractory_ticks=2` | `3 ms` |
| `refractory_ticks=3` | `4 ms` |

Equal numeric values are therefore not equivalent refractory semantics.

## Homeostasis operating envelope

The preceding bounded diagnostic established a configuration-specific LIF operating envelope for the 10 Hz controller. With the declared parameters, currents 16, 18, 20, 22 and 25 converged to 10 Hz without threshold-offset saturation. At current 30, the +10 mV actuator bound saturated and the target was not reachable.

This is an operating-envelope result, not a universal current boundary and not a biological equivalence claim.

## Model-axis rule

Izhikevich remains the canonical default. `lif-current-v1` is a validated selectable alternative and may be introduced as an additional treatment arm in scientifically eligible experiments. Such use must record the complete `NeuronConfig`, model provenance and a model-specific additional hypothesis/contrast. Existing primary hypotheses must not be rewritten after data inspection.

## Evidence boundary

This experiment is **DATA**. Brian2 is an external software reference, but this run is not an independently authored replication and is not automatically promoted to EVID. Human evidence review remains a separate repository gate.

## Provenance

- GitHub Actions run: `35149828152`
- Job: `104975033645`
- Artifact: `10468901959`
- Artifact SHA-256: `1c7e430fa75edb02ef7bfbaacf86cc85699d7a9ab5a6154bb81ce2da7bb0c89c`
- Frozen execution commit: `e84ee7efa56a9bf8d341e661325f79c82530f7bb`
- Brian2: `2.10.1`
- Python: `3.13.15`
