# Synaptic transfer on novel cue channels

The Builder research button and `POST /api/playground/research/synaptic-transfer` run pretraining followed by two matched novel-cue runs. One receives trained synaptic weights and delays; the other starts fresh. The schema `PAN_SYNAPTIC_TRANSFER_V1` rejects non-finite values, invalid indices/delays, duplicate edges and incompatible topology/model/population before application. It is a synaptic snapshot, not a resumable full-system checkpoint.

Four-action inputs move from channels 0–3 to disjoint channels 4–7. Evaluator labels and randomness are matched. Membrane, PAN hyperstate, eligibility, STP, pending events, policy and environment reset. Policy current, policy learning, reward/body feedback, structural learning and weight decay are disabled. Pair-STDP and STP run in both novel-cue conditions. Complete configurations, transferred state and spike digests accompany results. Limits are 256 neurons / 4096 edges and the shared request/worker bounds.

An external nearest-centroid probe fits increasing prefixes of the first two thirds of recorded episodes and scores a fixed final third. This is a **probe calibration curve**, not a neural task-learning curve: neural activity comes from one complete run per condition. Insufficient class coverage is reported rather than scored. No scientific promotion or neural transfer claim is emitted.

## Bounded measurements

Three seeds (12345, 42, 777), 64 neurons, 256 edges, 2000 ticks per stage; 11 held-out episodes per seed. Pretraining changed all 256 weights. At eight calibration episodes, trained/fresh accuracies were 100/100%, 81.8/72.7%, and 54.5/63.6%. At twelve they were 100/100%, 100/100%, and 90.9/100%. At sixteen both reached 100% for every seed. Four calibration episodes lacked class coverage. There is **no consistent pretrained advantage** in this small ceiling-limited experiment.

A frozen-pretraining negative control produces identical full spike digests and decoder curves after transfer and fresh initialization. Tests also verify actual changed weights and reject incompatible/invalid snapshots. Browser coverage checks the integrated endpoint and its explicit interpretation. Reward-learning transfer, complete checkpoint resumption and a policy driven by learned neural decoding remain separate work.
