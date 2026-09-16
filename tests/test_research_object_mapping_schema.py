import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = REPO_ROOT / "research" / "schemas" / "research_object_mapping.schema.json"


def test_minimal_research_object_mapping_contract_stays_small_and_explicit() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    required = {
        "id",
        "axis",
        "stage",
        "object_type",
        "evidence_mode",
        "parent_ids",
        "publication_refs",
        "status",
    }

    assert set(schema["required"]) == required
    assert required.issubset(schema["properties"])
    assert schema["additionalProperties"] is True
