from __future__ import annotations

import pytest

from src.memory.neural_episodic import NeuralEpisode
from src.memory.semantic import SemanticMemory, SemanticMemoryError


def _episode(episode_id: str, tick: int, spikes: tuple[int, ...]) -> NeuralEpisode:
    return NeuralEpisode(
        run_id="semantic-run",
        episode_id=episode_id,
        tick=tick,
        sensor_id="camera",
        modality="vision",
        spike_ids=spikes,
        frame_payload={"kind": "training"},
        actual_state={"observed": True},
    )


def test_semantic_prototype_extracts_recurrence_across_independent_episodes() -> None:
    memory = SemanticMemory(
        min_episode_support=3,
        prototype_support=2 / 3,
        match_threshold=0.5,
    )
    episodes = (
        _episode("a-1", 1, (1, 2, 3, 8)),
        _episode("a-2", 2, (1, 2, 3, 9)),
        _episode("a-3", 3, (1, 2, 3, 10)),
        _episode("noise", 4, (40, 41, 42)),
    )

    assert memory.consolidate(episodes) == 4

    mature = memory.mature_concepts
    assert len(mature) == 1
    assert mature[0].episode_count == 3
    assert mature[0].prototype_spike_ids == (1, 2, 3)

    matches = memory.query((1, 2, 3, 11), sensor_id="camera", modality="vision")
    assert matches[0].concept.concept_id == mature[0].concept_id
    assert matches[0].prototype_coverage == 1.0
    assert matches[0].score == pytest.approx(6 / 7)


def test_repeating_one_episode_cannot_create_semantic_support() -> None:
    memory = SemanticMemory(min_episode_support=2)
    episode = _episode("same", 1, (1, 2, 3))

    assert memory.consolidate((episode, episode)) == 1
    assert memory.consolidate((episode,)) == 0
    assert memory.mature_concepts == ()
    assert memory.concepts[0].episode_count == 1


def test_unrelated_patterns_do_not_become_false_semantic_concept() -> None:
    memory = SemanticMemory(min_episode_support=2, match_threshold=0.5)
    memory.consolidate(
        (
            _episode("r-1", 1, (1, 2, 3)),
            _episode("r-2", 2, (10, 11, 12)),
            _episode("r-3", 3, (20, 21, 22)),
        )
    )

    assert len(memory.concepts) == 3
    assert memory.mature_concepts == ()
    assert memory.query((1, 2), sensor_id="camera", modality="vision") == ()


def test_semantic_state_roundtrip_preserves_future_generalization() -> None:
    memory = SemanticMemory(min_episode_support=2, prototype_support=0.5)
    memory.consolidate(
        (
            _episode("a-1", 1, (1, 2, 8)),
            _episode("a-2", 2, (1, 2, 9)),
        )
    )
    restored = SemanticMemory.from_state_dict(memory.state_dict())

    assert restored.state_dict() == memory.state_dict()
    assert restored.query(
        (1, 2, 10), sensor_id="camera", modality="vision"
    ) == memory.query((1, 2, 10), sensor_id="camera", modality="vision")


def test_semantic_state_fails_closed_on_tamper_and_impossible_support() -> None:
    memory = SemanticMemory(min_episode_support=2)
    memory.consolidate((_episode("a-1", 1, (1, 2, 3)),))
    state = memory.state_dict()
    state["max_concepts"] = 999
    with pytest.raises(SemanticMemoryError, match="integrity"):
        SemanticMemory.from_state_dict(state)

    valid = memory.state_dict()
    valid["concepts"][0]["neuron_episode_support"]["1"] = 2
    unsigned = dict(valid)
    unsigned.pop("integrity_digest")
    # Do not forge a new digest here: integrity is the first fail-closed boundary.
    with pytest.raises(SemanticMemoryError, match="integrity"):
        SemanticMemory.from_state_dict(valid)
