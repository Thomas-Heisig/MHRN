# EXP-S6-SEM-CL-001 — Scientific interpretation

## Status

The preregistered primary decision rule passed.

This is a **positive mechanism-level empirical result** for the current MHRN semantic prototype consolidation implementation under the frozen Split-MNIST protocol. It is not a claim that the complete MHRN architecture is superior to other SNN systems, and it is not a claim of biological equivalence.

## Frozen comparison

- benchmark: Split-MNIST
- scenario: class-incremental, single-head
- tasks: 0/1 -> 2/3 -> 4/5 -> 6/7 -> 8/9
- paired seeds: 101-110
- baseline: deterministic pooled rate-coded spike representation + identical online softmax readout, without semantic memory
- treatment: same representation/readout/update budget, with MHRN `SemanticMemory` prototype consolidation and 20% bounded semantic replay on later tasks
- total readout update budget: matched between conditions

## Primary result

| Endpoint | Baseline | Semantic treatment | Paired effect |
| --- | ---: | ---: | ---: |
| Final average accuracy | 0.1883 | 0.4093 | +0.2210 |
| Mean forgetting | 0.9764 | 0.6975 | -0.2789 |

Accuracy improvement: +0.2210, 95% paired bootstrap CI +0.2076 to +0.2338, exact paired sign-flip p=0.001953.

Forgetting reduction: +0.2789, 95% paired bootstrap CI +0.2621 to +0.2947, exact paired sign-flip p=0.001953.

The preregistered thresholds were +0.03 final-average-accuracy improvement and +0.05 forgetting reduction, with positive lower bootstrap bounds and p < 0.05 for both endpoints. The primary rule therefore passed.

## What can be stated

A defensible statement is:

> Under the preregistered EXP-S6-SEM-CL-001 protocol, adding MHRN semantic prototype consolidation with bounded replay to an otherwise matched spike-coded sequential learner substantially reduced catastrophic forgetting and improved final average Split-MNIST accuracy across ten paired seeds.

This is a scientific result because the mechanism, comparator, task, endpoints, seeds, effect thresholds and decision rule were fixed before the empirical run, and the result can in principle falsify the hypothesis.

## What cannot yet be stated

The experiment does **not** yet demonstrate:

1. superiority of the complete MHRN recurrent SNN over a standard SNN baseline;
2. superiority over established continual-learning methods such as experience replay, EWC, SI, LwF, generative replay or modern SNN continual-learning systems;
3. generalization beyond MNIST/Split-MNIST;
4. biological validity of MHRN semantic consolidation;
5. novelty of semantization as a general concept.

The input representation is spike-coded, but this first benchmark intentionally isolates the semantic-memory mechanism rather than exercising the complete recurrent MHRN network end-to-end.

## Required replication ladder before publication-strength claim

1. exact independent rerun of EXP-S6-SEM-CL-001 without parameter changes;
2. compare against raw exemplar replay with the same memory/update budget;
3. compare against a standard SNN continual-learning baseline;
4. replay-fraction ablation including 0%, 5%, 10%, 20%, 40%;
5. semantic-prototype ablation with matched randomly selected spike prototypes;
6. at least one harder benchmark such as Permuted-MNIST, Fashion-MNIST or a neuromorphic/event dataset;
7. full recurrent-MHRN end-to-end version after the mechanism-level result is replicated.

## Governance

- automatic evidence promotion remains disabled;
- human review is required;
- parameter changes after the first run require a new experiment identifier;
- raw result bundle is retained under `results/`.
