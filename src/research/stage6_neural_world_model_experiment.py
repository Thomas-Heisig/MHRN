"""S6-NWM-001: compare a learned spiking transition candidate with controls."""

from __future__ import annotations

from typing import Any, Mapping

from src.memory import ActionConditionedWorldModel, StateAction
from src.memory.spiking_world_model import SpikingContext, SpikingTransitionWorldModel
from src.research.stage6_experiments import Stage6Run, _digest

Config = Mapping[str, Any]


def _next(position: int, action: str) -> int:
    return min(4, position + 1) if action == "right" else max(0, position - 1)


def _state(position: int) -> str:
    return f"position:{position}"


def _context(position: int, action: str) -> SpikingContext:
    return SpikingContext(_state(position), action)


def _statistical_reference() -> ActionConditionedWorldModel:
    model = ActionConditionedWorldModel(max_contexts=32)
    for position in range(5):
        for action in ("left", "right"):
            model.update(
                {"position": position},
                StateAction(action, {}),
                {"position": _next(position, action)},
            )
    return model


def run_s6_nwm_001(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """Evaluate exact-context neural transition recall against explicit controls."""

    del config
    conditions = (
        "spiking_trained",
        "spiking_untrained",
        "spiking_target_shuffled",
        "statistical_reference",
    )
    contexts = tuple(
        (position, action) for position in range(5) for action in ("left", "right")
    )
    runs: list[Stage6Run] = []

    for seed in seeds:
        for condition in conditions:
            exact = 0
            predictions = 0
            output_spikes = 0
            latencies: list[int] = []
            if condition == "statistical_reference":
                statistical = _statistical_reference()
                before = _digest(statistical.state_dict())
                for position, action in contexts:
                    rollout = statistical.rollout(
                        {"position": position},
                        (StateAction(action, {}),),
                        max_steps=1,
                    )
                    final = rollout.final_state
                    statistical_prediction = (
                        None if final is None else int(final["position"])
                    )
                    predictions += int(statistical_prediction is not None)
                    exact += int(statistical_prediction == _next(position, action))
                after = _digest(statistical.state_dict())
                learned_weight_margin = None
            else:
                spiking = SpikingTransitionWorldModel(
                    seed=seed,
                    max_contexts=16,
                    max_states=8,
                    training_repetitions=4,
                )
                if condition != "spiking_untrained":
                    for position, action in contexts:
                        target = _next(position, action)
                        if condition == "spiking_target_shuffled":
                            target = 4 - target
                        spiking.observe(_context(position, action), _state(target))
                before_weights = {
                    f"{position}:{action}": spiking.synaptic_weights(
                        _context(position, action)
                    )
                    for position, action in contexts
                }
                before = _digest(before_weights)
                margins: list[float] = []
                for position, action in contexts:
                    prediction = spiking.predict(_context(position, action))
                    spiking_prediction = prediction.predicted_state
                    predictions += int(spiking_prediction is not None)
                    output_spikes += len(prediction.output_spike_ids)
                    if prediction.latency_steps is not None:
                        latencies.append(prediction.latency_steps)
                    exact += int(spiking_prediction == _state(_next(position, action)))
                    weights = spiking.synaptic_weights(_context(position, action))
                    if weights:
                        correct_weight = weights.get(
                            _state(_next(position, action)), 0.0
                        )
                        alternatives = [
                            value
                            for key, value in weights.items()
                            if key != _state(_next(position, action))
                        ]
                        margins.append(correct_weight - max(alternatives, default=0.0))
                after_weights = {
                    f"{position}:{action}": spiking.synaptic_weights(
                        _context(position, action)
                    )
                    for position, action in contexts
                }
                after = _digest(after_weights)
                learned_weight_margin = sum(margins) / len(margins) if margins else None

            runs.append(
                Stage6Run(
                    "S6-NWM-001",
                    condition,
                    seed,
                    {
                        "contexts": len(contexts),
                        "exact_predictions": exact,
                        "exact_accuracy": exact / len(contexts),
                        "prediction_coverage": predictions / len(contexts),
                        "output_spikes": output_spikes,
                        "mean_latency_steps": (
                            sum(latencies) / len(latencies) if latencies else None
                        ),
                        "mean_correct_weight_margin": learned_weight_margin,
                        "exact_context_encoder": True,
                        "held_out_context_generalization": False,
                        "teacher_forced_training": condition.startswith("spiking_")
                        and condition != "spiking_untrained",
                        "snn_involved": condition.startswith("spiking_"),
                        "scientific_evidence": False,
                        "claim_scope": "experimental_exact_context_neural_world_model_data_only",
                    },
                    before,
                    after,
                )
            )
    return runs


RUNNERS = {"s6_nwm_001_v1": run_s6_nwm_001}

__all__ = ["RUNNERS", "run_s6_nwm_001"]
