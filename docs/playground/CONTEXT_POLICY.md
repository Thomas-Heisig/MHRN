# Cue-conditioned reference policy

The Builder previously selected actions and applied rewards to one global policy,
even though the learner already supported contextual policies for meta tasks.
The closed-loop Builder now activates a context from the **emitted target cue**
and combines a context bias with learned weights over population activity.

Each transient cue is remembered only within its episode. Without a cue (encoding
`none`, zero cue current, or a latency pulse not yet emitted), no hidden evaluator
target is supplied to the policy. Aliased cues remain aliased. A cue is an explicit
symbolic observation from the environment; this does **not** demonstrate learned
neural decoding, biological learning, or generalization to unseen observations.

New closed-loop context values start optimistically at 1.0. Otherwise a zero
reward and zero prediction provide no error, allowing deterministic ties to keep
selecting a failed action indefinitely. Updates fit bounded scalar rewards using
normalized LMS over `[1, activity]`; no action is populated from the correct label.
Only the chosen context/action row changes. Epsilon exploration remains active.

For delayed rewards, the Builder queues the action-time context and activity
snapshot. Delivery updates that original decision, even after the next episode
has activated another context. Silence receives no learning credit. The existing
meta-task context API retains zero initialization by default.

The target generator now honors `behavior_target_mode=fixed`, and the two/one
action sanity presets configure the actual closed-loop action space consistently.
The single-action result is a trivial sanity check, not evidence of learning.

## Measurements on 2026-09-28

Full `pan_full_balanced`, 256 neurons, 2048 edges, 2000 ticks, persistence disabled:

| Seed | Original global policy | Context policy | Contexts |
| --- | ---: | ---: | ---: |
| 12345 | 7/31 (22.6%) | 21/31 (67.7%) | 4 |
| 42 | 8/31 (25.8%) | 23/31 (74.2%) | 4 |
| 777 | 7/31 (22.6%) | 20/31 (64.5%) | 4 |

The cue-removed control (seed 12345) remains at 7/31 (22.6%), with no contexts.
With 32 neurons and 64 edges, `g1_two_action_simple` reaches 96% over 125
episodes; `g2_one_action_trivial` reaches 100%. These are fixed-seed engineering
checks with small sample sizes, not population-level performance claims.

Regression tests cover arbitrary cue/action mappings learned from reward, isolated
context updates, delayed activity snapshots, silent/absent cues, all three cue
encodings, real end-to-end runs and existing checkpoint/meta-task behavior.
