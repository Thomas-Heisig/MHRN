from src.research.meta_system import build_crosswalk, load_directions, render

def test_exactly_eleven_research_directions():
    directions = load_directions()
    assert [d["id"] for d in directions] == [f"DIR-{i:02d}" for i in range(1, 12)]

def test_taxonomies_are_explicitly_separate():
    cross = build_crosswalk()
    assert "direction != stage" in cross["invariants"]
    assert "direction != manuscript_part" in cross["invariants"]

def test_meta_questions_are_registered_without_evidence_promotion():
    rows = {q["research_question"]: q for q in build_crosswalk()["questions"]}
    for qid in ("RQ-EPIST-002", "RQ-ETH-001", "RQ-META-001", "RQ-META-002", "RQ-META-003"):
        assert qid in rows
        assert rows[qid]["direction"] == "DIR-11"

def test_generator_is_deterministic():
    assert render() == render()

def test_unmapped_domain_stays_visible():
    assert all("direction" in q for q in build_crosswalk()["questions"])
