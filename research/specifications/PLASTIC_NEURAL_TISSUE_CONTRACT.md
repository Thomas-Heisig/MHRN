# Stage 3 — Plastic Neural Tissue Contract

## Purpose

Stage 3 verifies the engineering mechanisms that allow a recurrent MHRN network to adapt while remaining bounded and reproducible: pair-based STDP, signed eligibility traces, reward-modulated three-factor plasticity, firing-rate/energy homeostasis, structural growth/pruning and persistence of learning/homeostatic state.

This is an **engineering verification boundary**. It is not a claim of biological tissue equivalence and it does not automatically promote experimental DATA to scientific EVID.

## Required mechanisms

1. **STDP**
   - pre-before-post produces bounded potentiation;
   - post-before-pre produces bounded depression;
   - disabled learning leaves weights unchanged;
   - topology refresh does not lose the learning state of surviving synapses.
2. **Three-factor plasticity**
   - signed eligibility is generated from spike timing;
   - positive and negative reward modulate eligible weights in the expected direction;
   - delayed rewards use the decayed eligibility trace;
   - weights remain inside declared bounds;
   - reward learning requires eligibility.
3. **Productive-learning control chain**
   - `learning_on` changes eligible weights and changes a fresh-network probe response;
   - `learning_off` preserves the initial weights;
   - `sham_replay` destroys the eligibility/reward causal link and therefore must not produce reward-mediated updates;
   - an independently reconstructed deterministic replay produces the same result.
4. **Homeostasis**
   - firing-rate feedback is bounded;
   - energy recovery is bounded;
   - deterministic iteration is retained.
5. **Structural plasticity**
   - proposals flow through the canonical Coordinator -> Approval -> Plasticity -> Manipulator -> Journal path;
   - pruning/growth decisions and final topology are deterministic for equal initial state, configuration and RNG state.
6. **Persistence**
   - homeostasis and learning state survive the checkpoint-v4 round trip.

## Reference execution

The canonical runner is:

```text
python scripts/run_stage3_reference.py
```

It combines the existing mechanism-level test suites with the deterministic `configs/learning_experiment.yaml` learning protocol and writes:

```text
research/generated/verification/plastic_neural_tissue_reference.json
```

The JSON artifact must have `status: verified` and every proof flag must be `true` before the Stage-3 engineering criteria may be shown as verified.

## Relationship to scientific experiments

The engineering reference deliberately does **not** create an `EVID-*` record. Scientific evaluation remains separate and requires, at minimum:

- preregistered learning-on/off and appropriate information-destroyed controls;
- held-out evaluation that is not used to tune the learning rule;
- independent seeds/runs rather than repeated inspection of one deterministic trajectory;
- source/protocol/configuration provenance;
- human evidence review and explicit claim promotion.

A negative scientific result remains a valid outcome even when the engineering contract passes.

## Scale boundary

The development timeline lists a Stage-3 target order of 10,000–100,000 neurons and 10^5–10^7 synapses. The reference contract is intentionally smaller so mechanism correctness can be checked deterministically and cheaply.

Therefore:

- passing this contract does **not** establish target-scale performance;
- it does **not** establish stability for arbitrary reward formulations, topology, delays or plasticity rates;
- scale/throughput and long-horizon plastic-network stability remain separate benchmark questions.

## Completion rule

Stage 3 is technically reached when all repository criteria for STDP, three-factor learning, homeostasis, structural plasticity and checkpointed plastic state resolve as verified and the generated Stage-3 reference artifact passes.

Scientific readiness is scored separately. `R2 productive-learning evidence closure` remains open until controlled, reviewed experimental evidence exists.
