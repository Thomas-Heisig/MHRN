from pathlib import Path
import json
import yaml
from src.research.meta_system import MetaSystem, validate_direction_registry

ROOT=Path(__file__).resolve().parents[1]

def test_direction_registry_fails_closed_until_source_bound():
    data=yaml.safe_load((ROOT/"research/registry/directions.yaml").read_text(encoding="utf-8"))
    lock=json.loads((ROOT/"research/registry/directions.lock.json").read_text(encoding="utf-8"))
    validate_direction_registry(data,lock)
    assert data["expected_count"]==11
    assert data["status"]=="awaiting_canonical_source"
    assert data["directions"]==[]
    assert data["assignments"]=={}

def test_meta_designs_never_authorize_execution_or_evidence():
    m=MetaSystem(ROOT)
    assert m.studies
    assert all(s["execution_authorized"] is False for s in m.studies)
    assert all(s["scientific_evidence"] is False for s in m.studies)

def test_crosswalk_covers_every_registered_question():
    m=MetaSystem(ROOT)
    assert {r["research_question"] for r in m.rows}==set(m.questions)

def test_meta_questions_are_registered_and_literature_bound():
    m=MetaSystem(ROOT)
    for qid in ("RQ-META-003","RQ-META-004","RQ-META-005"):
        assert qid in m.questions
        assert m.questions[qid]["literature"]
        assert set(m.questions[qid]["literature"]) <= set(m.sources)

def test_render_is_deterministic_and_keeps_taxonomies_separate():
    a=MetaSystem(ROOT).render()
    b=MetaSystem(ROOT).render()
    assert a==b
    assert "Stage 0-10 is a maturity/development axis" in a["STAGE_MATRIX.md"]
    assert "not a research-direction taxonomy" in a["DISSERTATION_MAP.md"]
