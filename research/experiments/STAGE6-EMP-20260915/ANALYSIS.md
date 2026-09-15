# Stage 6 empirical DATA summary

Status: descriptive DATA aggregation only; not accepted EVID.

Source commit: `ae51bb508a548389035131290e67d89ddeae4bde`  
DATA SHA-256: `da720d5a3d9841516b71c81eedad53861516ba3dde2f1884c9b0469288d99a71`  
Protocol SHA-256: `45334d943786ae8ad9d2d292e47628b292a367b795decf038ef058cb46df76c8`  
Preregistration SHA-256: `670e8663abb03463b5a783cc178dff55e826cbe0ebcc5980a91c3ac6d7ecd8ff`  
Seeds: `[101, 102, 103]`

| Protocol | Condition | Seeds | Primary descriptive means |
| --- | --- | ---: | --- |
| `s6_epi_001_v1` | `episode_shuffle` | 3 | accuracy=0.444444, retrievals=12, distractor_spikes=101 |
| `s6_epi_001_v1` | `intact` | 3 | accuracy=0.777778, retrievals=12, distractor_spikes=101 |
| `s6_epi_001_v1` | `read_off` | 3 | accuracy=0.444444, retrievals=0, distractor_spikes=101 |
| `s6_epi_001_v1` | `write_off` | 3 | accuracy=0.444444, retrievals=0, distractor_spikes=101 |
| `s6_nwm_001_v1` | `spiking_target_shuffled` | 3 | exact_accuracy=0.1, prediction_coverage=0.5, mean_latency_steps=1, mean_correct_weight_margin=-134.934 |
| `s6_nwm_001_v1` | `spiking_trained` | 3 | exact_accuracy=0.5, prediction_coverage=0.5, mean_latency_steps=1, mean_correct_weight_margin=129.481 |
| `s6_nwm_001_v1` | `spiking_untrained` | 3 | exact_accuracy=0, prediction_coverage=0 |
| `s6_nwm_001_v1` | `statistical_reference` | 3 | exact_accuracy=1, prediction_coverage=1 |
| `s6_pe_001_v1` | `pe_correct__reward_off` | 3 | weight_delta=0.003894, prediction_error_updates=1, reward_calls=0 |
| `s6_pe_001_v1` | `pe_correct__reward_on` | 3 | weight_delta=0.011682, prediction_error_updates=1, reward_calls=1 |
| `s6_pe_001_v1` | `pe_disabled__reward_off` | 3 | weight_delta=0, prediction_error_updates=0, reward_calls=0 |
| `s6_pe_001_v1` | `pe_disabled__reward_on` | 3 | weight_delta=0.00778801, prediction_error_updates=0, reward_calls=1 |
| `s6_pe_001_v1` | `pe_shuffled__reward_off` | 3 | weight_delta=-0.001298, prediction_error_updates=1, reward_calls=0 |
| `s6_pe_001_v1` | `pe_shuffled__reward_on` | 3 | weight_delta=0.00649001, prediction_error_updates=1, reward_calls=1 |
| `s6_rpl_001_v1` | `equal_budget_awake` | 3 | mean_reactivation_fidelity=1, mature_concepts=0 |
| `s6_rpl_001_v1` | `no_replay` | 3 | mature_concepts=0 |
| `s6_rpl_001_v1` | `ordered` | 3 | mean_reactivation_fidelity=1, mature_concepts=2 |
| `s6_rpl_001_v1` | `shuffled` | 3 | mean_reactivation_fidelity=1, mature_concepts=1 |
| `s6_sem_001_v1` | `intact` | 3 | accuracy=0.5, matched_holdout=0, mature_concepts=0 |
| `s6_sem_001_v1` | `label_shuffle` | 3 | accuracy=0.5, matched_holdout=0, mature_concepts=0.666667 |
| `s6_sem_001_v1` | `no_semantic` | 3 | accuracy=0.5, matched_holdout=0, mature_concepts=0 |
| `s6_wm_001_v1` | `frozen_correct` | 3 | exact_final_state_rate=1, mean_absolute_final_state_error=0, completed_rollouts=20 |
| `s6_wm_001_v1` | `frozen_shuffled` | 3 | exact_final_state_rate=0.216667, mean_absolute_final_state_error=1.95, completed_rollouts=20 |
| `s6_wm_001_v1` | `no_model` | 3 | completed_rollouts=0 |
| `s6_wm_001_v1` | `persistence` | 3 | exact_final_state_rate=0.283333, mean_absolute_final_state_error=0.916667, completed_rollouts=0 |
| `s6_wm_002_v1` | `correct` | 3 | utility_ratio=1, achieved_utility=80, recommendations=8 |
| `s6_wm_002_v1` | `disabled` | 3 | utility_ratio=0.6, achieved_utility=48, recommendations=0 |
| `s6_wm_002_v1` | `persistence` | 3 | utility_ratio=0.6, achieved_utility=48, recommendations=0 |
| `s6_wm_002_v1` | `shuffled` | 3 | utility_ratio=0.2, achieved_utility=16, recommendations=8 |

## Interpretation boundary

These values are descriptive outputs from the frozen Stage-6 DATA bundle. They are not automatically inferential statistics, accepted evidence, or a basis for closing `RQ-MEM-002` or `RQ-WM-001`. Confirmatory claims require the preregistered larger independent-seed campaign, uncertainty estimates, failure reporting, and human scientific review.
