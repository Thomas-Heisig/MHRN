from __future__ import annotations

import pytest

from src.memory.spiking_world_model import (
    SpikingContext,
    SpikingTransitionWorldModel,
    SpikingWorldModelError,
)


def test_spiking_world_model_learns_context_to_state_via_synapses() -> None:
    model = SpikingTransitionWorldModel(seed=17, training_repetitions=4)
    left = SpikingContext("position:1", "left")
    right = SpikingContext("position:1", "right")

    model.observe(left, "position:0")
    model.observe(right, "position:2")

    left_weights = model.synaptic_weights(left)
    right_weights = model.synaptic_weights(right)
    assert left_weights["position:0"] > left_weights["position:2"]
    assert right_weights["position:2"] > right_weights["position:0"]
    assert model.context_count == 2
    assert model.state_count == 2


def test_spiking_world_model_prediction_requires_output_spike() -> None:
    model = SpikingTransitionWorldModel(seed=23, training_repetitions=4)
    left = SpikingContext("position:1", "left")
    right = SpikingContext("position:1", "right")
    model.observe(left, "position:0")
    model.observe(right, "position:2")

    left_prediction = model.predict(left)
    right_prediction = model.predict(right)

    assert left_prediction.predicted_state == "position:0"
    assert right_prediction.predicted_state == "position:2"
    assert left_prediction.output_spike_ids
    assert right_prediction.output_spike_ids
    assert left_prediction.latency_steps is not None
    assert right_prediction.latency_steps is not None
    assert left_prediction.scientific_status == (
        "experimental_exact_context_neural_candidate"
    )


def test_spiking_world_model_unknown_context_does_not_guess() -> None:
    model = SpikingTransitionWorldModel(seed=5)

    prediction = model.predict(SpikingContext("unknown", "right"))

    assert prediction.predicted_state is None
    assert prediction.output_spike_ids == ()
    assert prediction.latency_steps is None


def test_spiking_inference_does_not_change_weights() -> None:
    model = SpikingTransitionWorldModel(seed=29, training_repetitions=4)
    context = SpikingContext("position:2", "right")
    model.observe(context, "position:3")
    before = model.synaptic_weights(context)

    model.predict(context)

    assert model.synaptic_weights(context) == before


def test_spiking_world_model_capacity_and_input_contracts() -> None:
    with pytest.raises(SpikingWorldModelError, match="positive integer"):
        SpikingTransitionWorldModel(max_contexts=0)
    with pytest.raises(SpikingWorldModelError, match="non-empty"):
        SpikingContext("", "right")

    model = SpikingTransitionWorldModel(max_contexts=1, max_states=1)
    model.observe(SpikingContext("s0", "right"), "s1")
    with pytest.raises(SpikingWorldModelError, match="context capacity"):
        model.observe(SpikingContext("s1", "right"), "s1")
    with pytest.raises(SpikingWorldModelError, match="next-state capacity"):
        model.observe(SpikingContext("s0", "left"), "s2")
