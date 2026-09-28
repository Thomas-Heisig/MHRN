# Actual cue interventions and pair-STDP controls

`target_cue_control` selects `aligned`, `randomized` or `absent` in the Builder and configuration export. Randomization changes the emitted input cue using an independent seeded stream, while the reward evaluator retains the same target. Absence suppresses cue current and therefore the explicit observed context. These controls apply to real runs, not merely to shuffled decoder labels.

`POST /api/playground/research/cue-controls` and the Builder control button run six matched conditions: all three cue modes with pair-STDP enabled and disabled. They preserve STP in both cases, freeze structural/cortical learning and weight decay, remove policy bias current, reward feedback and body/action feedback, and use stochastic paired evaluator targets to reduce cycle/time confounding. The full shared configuration and overrides accompany results. The endpoint shares the existing worker and request bounds and limits networks to 256 neurons / 4096 edges.

## Observed bounded result

Three seeds (12345, 42, 777), 64 neurons, 256 edges and 2000 ticks were tested. Each condition had 11 chronological held-out episodes per seed (33 total). Aggregate decoder accuracies:

| Pair-STDP | Aligned input | Randomized input | Absent input |
| --- | --- | --- | --- |
| Disabled | 100% | 27.3% | 18.2% |
| Enabled | 100% | 21.2% | 21.2% |

Chance is 25% for these four targets. These small exploratory samples show that the existing driven neural activity can carry cue information even with frozen weights. They do **not** demonstrate a learned representation or a pair-STDP advantage: aligned decoding is already perfect without that learning rule. They also do not prove that the policy uses a neural decoder. The policy reference remains explicitly cue-conditioned.

The transfer experiment remains open. It requires resuming a trained neural checkpoint on novel cues and comparing its reward/learning curve with matched fresh-network initialization. Training a new external classifier on the same recordings would not establish neural transfer, so it is not reported as such.

Validation: deterministic emitted-cue tests preserve evaluator labels, six-condition integration tests, no-cue/randomized-feature negative controls, finite/coverage/budget guards and browser endpoint/configuration wiring. Scientific promotion remains disabled.
