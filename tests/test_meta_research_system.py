from src.research.meta_system import build_crosswalk, load_directions, render


def test_exactly_eleven_research_directions():
    directions = load_directions()
    assert [direction["id"] for direction in directions] == [
        f"DIR-{index:02d}" for index in range(1, 12)
    ]


def test_taxonomies_are_explicitly_separate():
    crosswalk = build_crosswalk()
    assert "direction != stage" in crosswalk["invariants"]
    assert "direction != manuscript_part" in crosswalk["invariants"]


def test_meta_questions_are_registered_without_evidence_promotion():
    rows = {
        question["research_question"]: question
        for question in build_crosswalk()["questions"]
    }
    for question_id in (
        "RQ-EPIST-002",
        "RQ-ETH-001",
        "RQ-META-001",
        "RQ-META-002",
        "RQ-META-003",
    ):
        assert question_id in rows
        assert rows[question_id]["direction"] == "DIR-11"


def test_generator_is_deterministic():
    assert render() == render()


def test_unmapped_domain_stays_visible():
    assert all("direction" in question for question in build_crosswalk()["questions"])
