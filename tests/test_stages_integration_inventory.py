"""The integration inventory reports gaps rather than silently closing them."""

from pathlib import Path

from scripts.audit_stages_0_6 import audit
from scripts.check_doc_consistency import check_markdown_links

ROOT = Path(__file__).resolve().parents[1]


def test_stage_inventory_preserves_research_boundaries() -> None:
    report = audit(ROOT)
    assert [stage["stage"] for stage in report["stages"]] == list(range(7))
    assert report["missing_declared_module_or_test_paths"] == []
    assert report["scientific_evidence_promotion"] is False
    assert report["neural_memory_complete"] is False
    six = report["stages"][-1]
    assert six["status"] != "reached"
    assert (
        next(item for item in six["criteria"] if item["id"] == "semantic_memory")[
            "status"
        ]
        == "planned"
    )
    assert any("checkpoint" in todo.lower() for todo in six["open_todos"])


def test_new_publication_addendum_links_exist() -> None:
    paths = (
        ROOT
        / "research/publications/2026-09-14_stages0-6-integration_v1.5-addendum/README.md",
        ROOT / "research/specifications/STAGE6_REPLAY_FORMAT.md",
        ROOT / "docs/07-changelog/2026-09-14_STAGES_0_6_INTEGRATION.md",
    )
    assert not check_markdown_links(paths)
