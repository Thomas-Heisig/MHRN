from __future__ import annotations

import math

import pytest

from src.memory import (
    ActionConditionedWorldModel,
    ActionSequenceCandidate,
    OfflineDecisionEvaluator,
    StateAction,
    WorldModelEvaluationError,
)


def _action(name: str) -> StateAction:
    return StateAction(name, {})


def _trained_model() -> ActionConditionedWorldModel:
    model = ActionConditionedWorldModel(max_contexts=16)
    start = {"node": "start", "utility": 0}
    left = {"node": "left", "utility": 1}
    right = {"node": "right", "utility": 1}
    good = {"node": "goal-good", "utility": 10}
    bad = {"node": "goal-bad", "utility": 2}
    model.update(start, _action("left"), left)
    model.update(left, _action("advance"), good)
    model.update(start, _action("right"), right)
    model.update(right, _action("advance"), bad)
    return model


def _utility_score(rollout: object) -> float:
    final_state = getattr(rollout, "final_state")
    assert final_state is not None
    return float(final_state["utility"])


def test_offline_evaluator_selects_higher_scored_complete_rollout() -> None:
    model = _trained_model()
    before = model.state_dict()
    evaluator = OfflineDecisionEvaluator(model, _utility_score, max_steps=2)
    candidates = (
        ActionSequenceCandidate("left-path", (_action("left"), _action("advance"))),
        ActionSequenceCandidate(
            "right-path", (_action("right"), _action("advance"))
        ),
    )

    recommendation = evaluator.evaluate(
        {"node": "start", "utility": 0}, candidates
    )

    assert recommendation.selected_label == "left-path"
    assert recommendation.scientific_status == (
        "offline_reference_evaluator_not_actuation_authority"
    )
    assert all(item.eligible for item in recommendation.evaluations)
    assert model.state_dict() == before


def test_unknown_rollout_is_ineligible_and_never_selected() -> None:
    model = _trained_model()
    evaluator = OfflineDecisionEvaluator(model, _utility_score, max_steps=2)
    candidates = (
        ActionSequenceCandidate("known", (_action("left"), _action("advance"))),
        ActionSequenceCandidate("unknown", (_action("jump"), _action("advance"))),
    )

    result = evaluator.evaluate({"node": "start", "utility": 0}, candidates)

    assert result.selected_label == "known"
    unknown = next(item for item in result.evaluations if item.label == "unknown")
    assert unknown.eligible is False
    assert unknown.score is None
    assert unknown.reason == "unknown_transition"


def test_no_complete_rollout_returns_no_recommendation() -> None:
    evaluator = OfflineDecisionEvaluator(
        ActionConditionedWorldModel(), _utility_score, max_steps=1
    )
    candidate = ActionSequenceCandidate("unknown", (_action("jump"),))

    result = evaluator.evaluate({"node": "start", "utility": 0}, (candidate,))

    assert result.selected_label is None
    assert result.evaluations[0].eligible is False


def test_equal_scores_use_candidate_label_as_deterministic_tie_break() -> None:
    model = ActionConditionedWorldModel()
    start = {"node": "start", "utility": 0}
    same = {"node": "same", "utility": 5}
    model.update(start, _action("a"), same)
    model.update(start, _action("b"), same)
    evaluator = OfflineDecisionEvaluator(model, _utility_score, max_steps=1)

    result = evaluator.evaluate(
        start,
        (
            ActionSequenceCandidate("zeta", (_action("a"),)),
            ActionSequenceCandidate("alpha", (_action("b"),)),
        ),
    )

    assert result.selected_label == "alpha"


def test_candidate_horizons_must_be_matched() -> None:
    evaluator = OfflineDecisionEvaluator(_trained_model(), _utility_score)

    with pytest.raises(WorldModelEvaluationError, match="horizons must be matched"):
        evaluator.evaluate(
            {"node": "start", "utility": 0},
            (
                ActionSequenceCandidate("short", (_action("left"),)),
                ActionSequenceCandidate(
                    "long", (_action("left"), _action("advance"))
                ),
            ),
        )


def test_duplicate_candidate_labels_are_rejected() -> None:
    evaluator = OfflineDecisionEvaluator(_trained_model(), _utility_score)

    with pytest.raises(WorldModelEvaluationError, match="labels must be unique"):
        evaluator.evaluate(
            {"node": "start", "utility": 0},
            (
                ActionSequenceCandidate("same", (_action("left"),)),
                ActionSequenceCandidate("same", (_action("right"),)),
            ),
        )


def test_invalid_scores_are_rejected() -> None:
    model = _trained_model()
    candidate = ActionSequenceCandidate(
        "known", (_action("left"), _action("advance"))
    )

    for value in (math.nan, math.inf, True):
        evaluator = OfflineDecisionEvaluator(model, lambda _: value)  # type: ignore[arg-type]
        with pytest.raises(WorldModelEvaluationError, match="score must be finite"):
            evaluator.evaluate({"node": "start", "utility": 0}, (candidate,))


def test_empty_candidate_set_and_over_budget_horizon_are_rejected() -> None:
    evaluator = OfflineDecisionEvaluator(_trained_model(), _utility_score, max_steps=1)

    with pytest.raises(WorldModelEvaluationError, match="at least one candidate"):
        evaluator.evaluate({"node": "start", "utility": 0}, ())
    with pytest.raises(WorldModelEvaluationError, match="exceeds evaluation budget"):
        evaluator.evaluate(
            {"node": "start", "utility": 0},
            (
                ActionSequenceCandidate(
                    "too-long", (_action("left"), _action("advance"))
                ),
            ),
        )
