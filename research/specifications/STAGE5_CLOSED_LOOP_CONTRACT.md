# Stage 5: closed-loop integrity and failure controls

Status: engineering hardening increment; scientific evidence closure open.
Baseline: `8a8422687c7a879550a9f4fc3a484bcfcbfa0533`.
Canonical stage: `integrated_artificial_nervous_system`.

## Purpose and non-claims

A causal perception-action-feedback loop is a prerequisite for meaningful memory
and world-model experiments. This contract prevents bookkeeping errors and
unverified actuator effects from being mistaken for successful learning.
It adds no autonomous permissions, no LLM-to-core write path and no physical
actuator activation. It does not establish the million-neuron scale displayed
as an indicative timeline range.

## Invariants

| Boundary | Required invariant | Executable check |
| --- | --- | --- |
| Sensor | Requested tick, source identity and modality match before injection | `test_stage5_integration.py` |
| Encoder | Non-negative integer neuron IDs and finite current values | `test_stage5_integration.py` |
| Cycle | At most one pending cycle; consume before downstream effects; monotonically increasing attempted ticks per episode | `test_stage5_loop_contract.py` and integration suite |
| Actuator | Command target matches descriptor and actual adapter | integration suite and existing safety suite |
| Budget | Attempts, including failed and rejected dispatches, consume per-tick budget before external I/O | guard and integration suites |
| Failure | Unknown effects remain `effect_observed=null`; exceptions latch emergency stop | integration suite |
| Human control | Only explicit human approval clears emergency stop; reset expires old overrides | integration suite |
| Resources | Tick budget uses constant space; pending overrides have explicit capacity | guard and integration suites |
| Learning | Only verified environment outcomes supply finite rewards | experience suite and engine validation |

The runtime must serialize calls. These guards are not locks and do not provide
physical exactly-once delivery. In-memory ordering is scoped to one episode;
restart-safe command IDs, durable in-flight receipts and cross-episode replay
protection require a separate transport/checkpoint contract. Sensor/frame
identity matching is not cryptographic authentication. Audit-log rotation is
separate from bounded rate-limit bookkeeping.

## State and failure semantics

`prepare(t)` reserves the cycle before sampling/injection. A second prepare cannot
overwrite it. `complete(t)` consumes it before decoding, prediction, dispatch,
reward updates or memory observers. A failed attempt cannot be repeated at the
same tick. Partial neural injection and externally applied actions are not
rolled back; reset or a later tick is explicit, and the receipt records uncertainty.

Before an authorized dispatch the actuator attempt budget is charged. Rejection
does not refund it. An actuator, audit or feedback exception stops further
actuation until human clearance. Missing feedback is not a demonstrated lack of
effect, is not a successful action, and must not receive an invented reward.

## Research programme to run after engineering verification

Use the existing Stage-5 parent questions `RQ6`, `RQ7`, `RQ8`, `RQ9`; review the
registry-to-protocol mapping before a confirmatory run. The following are proposed
subprotocols, not executed experiments or additional accepted research questions.

| Protocol | Controls | Primary outcomes |
| --- | --- | --- |
| Sensor/feedback integrity | intact, dropped, stale, modality-shuffled and yoked feedback; matched input budget | invalid-frame rejection, false reward count, task outcome |
| Actuation failures | accepted, unauthorized, wrong target, adapter rejection, raised exception, lost feedback | dispatch attempts, blocked actions, observed/unknown effect counts |
| Closed-loop causal contribution | action-conditioned feedback versus replayed/yoked feedback and fixed action controls | held-out task success, action-to-state attribution, recovery time |
| Interoception/resources | intact, delayed, shuffled and unavailable resource signals | calibrated resource use, bounded operation, recovery, task trade-off |
| Deterministic continuation | uninterrupted versus explicit checkpoint/restart, including in-flight operations | state/receipt digests and task continuation; hardware effects excluded |

Predeclare seeds, task splits, duration, noise/failure schedules, update and energy
budgets, primary metric and uncertainty analysis. Independent seeds, not repeated
ticks, are the statistical units. Separate real energy measurements from model
cost proxies. Store code/config hashes, environment version, commands, receipts,
resource budgets, outcomes and missing-data reasons. Human review is mandatory
before DATA-to-EVID promotion. Failure and negative results remain reportable.

## Full-stack follow-up, not implied complete

The current increment hardens existing backend paths. Expose cycle admission,
blocked-action reason, pending override count and unknown effect distinctly in
the existing embodiment API/UI, rather than adding a second control panel.
The UI must distinguish unknown effects from `false`, show latched emergency
stops, and never treat browser state as authorization. Add API-contract and
Playwright failure-path checks when that view is wired.

Next closure steps are real-SNN closed-loop runs, interoception/resource ablations,
checkpoint integration, frontend end-to-end checks, independent replication and
scientific review. None is replaced by passing deterministic adapter tests.
