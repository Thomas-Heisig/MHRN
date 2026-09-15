from __future__ import annotations

import pytest

from src.memory.multistep_world_model import (
    ActionConditionedWorldModel,
    MultistepWorldModelError,
    StateAction,
)


def _move(delta: int) -> StateAction:
    return StateAction("move", {"delta": delta})


def test_action_conditioned_prediction_distinguishes_alternatives() -> None:
    model = ActionConditionedWorldModel()
    state = {"position": 0}
    model.update(state, _move(1), {"position": 1})
    model.update(state, _move(-1), {"position": -1})

    forward, forward_support, _ = model.predict(state, _move(1))
    backward, backward_support, _ = model.predict(state, _move(-1))

    assert forward == {"position": 1}
    assert backward == {"position": -1}
    assert forward_support == backward_support == 1


def test_rollout_chains_predicted_state_over_multiple_actions() -> None:
    model = ActionConditionedWorldModel()
    model.update({"position": 0}, _move(1), {"position": 1})
    model.update({"position": 1}, _move(1), {"position": 2})
    model.update({"position": 2}, _move(-1), {"position": 1})

    result = model.rollout(
        {"position": 0}, (_move(1), _move(1), _move(-1)), max_steps=3
    )

    assert not result.terminated_early
    assert [step.predicted_state for step in result.steps] == [
        {"position": 1},
        {"position": 2},
        {"position": 1},
    ]
    assert result.final_state == {"position": 1}


def test_rollout_stops_when_a_transition_is_unknown() -> None:
    model = ActionConditionedWorldModel()
    model.update({"position": 0}, _move(1), {"position": 1})

    result = model.rollout({"position": 0}, (_move(1), _move(1)))

    assert result.terminated_early
    assert len(result.steps) == 2
    assert result.steps[-1].predicted_state is None
    assert result.steps[-1].uncertainty == 1.0


def test_counterfactual_reports_action_specific_next_states() -> None:
    model = ActionConditionedWorldModel()
    state = {"position": 4}
    left = _move(-1)
    right = _move(1)
    model.update(state, left, {"position": 3})
    model.update(state, right, {"position": 5})

    alternatives = model.counterfactual(state, (left, right))

    assert sorted(alternatives.values(), key=lambda item: item["position"]) == [
        {"position": 3},
        {"position": 5},
    ]


def test_majority_transition_and_uncertainty_are_deterministic() -> None:
    model = ActionConditionedWorldModel()
    state = {"mode": "a"}
    action = StateAction("toggle", {})
    model.update(state, action, {"mode": "b"})
    model.update(state, action, {"mode": "b"})
    model.update(state, action, {"mode": "c"})

    predicted, support, uncertainty = model.predict(state, action)

    assert predicted == {"mode": "b"}
    assert support == 2
    assert uncertainty == pytest.approx(1.0 / 3.0)


def test_state_restore_preserves_fifo_behavior_and_rollout() -> None:
    model = ActionConditionedWorldModel(max_contexts=2)
    model.update({"position": 0}, _move(1), {"position": 1})
    model.update({"position": 1}, _move(1), {"position": 2})
    restored = ActionConditionedWorldModel.from_state_dict(model.state_dict())

    assert restored.state_dict() == model.state_dict()
    assert restored.rollout({"position": 0}, (_move(1), _move(1))).final_state == {
        "position": 2
    }

    restored.update({"position": 2}, _move(1), {"position": 3})
    assert restored.predict({"position": 0}, _move(1))[0] is None


def test_rollout_budget_and_json_contract_are_enforced() -> None:
    model = ActionConditionedWorldModel()
    with pytest.raises(MultistepWorldModelError, match="rollout budget"):
        model.rollout({"position": 0}, (_move(1), _move(1)), max_steps=1)
    with pytest.raises(MultistepWorldModelError, match="finite JSON"):
        model.update({"value": float("nan")}, _move(1), {"value": 1})
