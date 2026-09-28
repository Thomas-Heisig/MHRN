# PAN Builder embodiment and activity probe

The Builder now advances the actual `StickFigureSandbox` when `sandbox_enabled` is true. Batch and live execution share `EmbodiedEnvironment` for physics, posture scoring, reward events and episode resets. The batch physics step is exactly `dt_ms / 1000` seconds; the live wrapper retains its existing 0.01-second step.

Receptor, synthetic audio and delayed echo values project to contiguous neuron groups with `neural_io_input_current` gain. They add to other inputs, so these groups are not claimed to be disjoint cue channels. The previously selected action drives the body until the next configured action boundary; disabling the action loop leaves muscles undriven. Posture/event channel currents enter the following tick. Enabled reward-modulated STDP also receives posture reward through eligible synapses inside the configured credit window. Target-policy rewards and success statistics remain separate from posture reward.

Results include `sandbox` backend, actual tick count, time step, reward total, termination count, credit-update count and the last 128 physical frames. The Run page draws the body and offers frame replay; persisted session replay uses the same result renderer. This embodiment backend is CPU reference code. CUDA diagnostics do not change its backend.

## Activity decoding

Every complete episode produces one vector of neuron spike counts. An offline nearest-centroid probe trains on the first two thirds of episodes and evaluates only on the final third. Labels are never included in its input features or supplied to neuron dynamics by the probe. It includes majority/chance baselines and 64 training-label permutations. Missing classes, non-finite data and excessive probe budgets produce an explicit unavailable status instead of a positive result.

This measures decodability, not learned neural cue interpretation. The result flags explicit policy-current feedback as a confound. Label permutation is not a randomized-input intervention. Transfer needs matched trained-network checkpoints and fresh-network learning curves; it is not inferred from classification accuracy. The research-candidate catalog records these controls.

## Local validation (RTX 3060 host, 2026-09-28)

135 backend/integration tests passed. The seven Chromium workspace scenarios passed (six existing scenarios together, followed by the new physical-body replay scenario). Black/Ruff and Mypy checks for changed Python modules passed; the new probe passes strict Pyright. The repository CI retains its configured full checks.

The three 256-neuron / 2048-edge / 2000-tick default runs still score 21/31, 23/31 and 20/31 target successes for seeds 12345, 42 and 777. Each advances the body for 2000 ticks. The probe decodes 11/11 held-out episodes in these runs, but policy feedback is active and the cue is directly driven into neural inputs. This is explicitly not evidence that plasticity learned a neural representation, transfer, cognition or physical task mastery.
