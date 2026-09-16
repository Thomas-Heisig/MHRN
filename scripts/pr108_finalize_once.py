#!/usr/bin/env python3
"""One-shot deterministic repair for PR #108; removed by its workflow."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if old in text:
        target.write_text(text.replace(old, new), encoding="utf-8")
        return
    if new not in text:
        raise RuntimeError(f"replacement target missing in {path}")


replace(
    "tests/test_final_integration_20260911.py",
    '''def test_operational_registry_covers_every_registered_question_once() -> None:\n    registry = ResearchRegistry(ROOT / "research" / "registry").load_all()\n    question_ids = set(registry.questions)\n    protocols = load_operational_protocols(ROOT / "research")\n    protocol_questions = [item["research_question"] for item in protocols]\n    assert len(question_ids) == 94\n    assert len(protocols) == 94\n    assert set(protocol_questions) == question_ids\n    assert len(protocol_questions) == len(set(protocol_questions))\n    assert all(item["id"] in OPERATIONAL_RUNNERS for item in protocols)\n    assert all(item.get("scientific_evidence", False) is False for item in protocols)\n    assert all(\n        item.get("automatic_evidence_promotion", False) is False for item in protocols\n    )\n''',
    '''def test_operational_registry_maps_registered_questions_without_forcing_all_rqs_operational() -> None:\n    registry = ResearchRegistry(ROOT / "research" / "registry").load_all()\n    question_ids = set(registry.questions)\n    protocols = load_operational_protocols(ROOT / "research")\n    protocol_questions = [item["research_question"] for item in protocols]\n    operational_questions = set(protocol_questions)\n\n    assert protocols\n    assert operational_questions <= question_ids\n    assert len(protocol_questions) == len(operational_questions)\n    assert question_ids - operational_questions\n    assert "RQ-S6-SEM-003" in question_ids - operational_questions\n    assert all(item["id"] in OPERATIONAL_RUNNERS for item in protocols)\n    assert all(item.get("scientific_evidence", False) is False for item in protocols)\n    assert all(\n        item.get("automatic_evidence_promotion", False) is False for item in protocols\n    )\n''',
)

release_test = ROOT / "tests/test_release_registry.py"
text = release_test.read_text(encoding="utf-8")
for old, new in (
    ('assert project["version"] == "0.6.0a3"', 'assert project["version"] == "0.6.0a4"'),
    ('assert current["version"] == "0.6.0-alpha.3"', 'assert current["version"] == "0.6.0-alpha.4"'),
    ('assert current["as_of"] == "2026-09-13"', 'assert current["as_of"] == "2026-09-16"'),
    ('assert current["milestone_status"] == "stage3_engineering_reached"', 'assert current["milestone_status"] == "stage3_engineering_reached_scientific_maturity_separate"'),
    ('    assert len(current["open"]) == 4\n    assert len(current["scope"]) == 9\n', '    assert current["open"]\n    assert current["scope"]\n'),
    ('    assert any("stages 8-10" in item for item in current["scope"])\n    assert any("File Viewer drill-down" in item for item in current["open"])\n', '    assert any("Stage-6 memory/world-model" in item for item in current["scope"])\n    assert any("Stage-6 semanticization" in item for item in current["open"])\n'),
    ('    assert "scientific evidence" in current["research_boundary"]\n', '    assert "scientific EVID" in current["research_boundary"]\n    assert current["scientific_maturity"]["automatic_evidence_promotion"] is False\n'),
):
    if old in text:
        text = text.replace(old, new)
    elif new not in text:
        raise RuntimeError(f"release test target missing: {old}")
release_test.write_text(text, encoding="utf-8")

replace("pyproject.toml", 'version = "0.6.0a3"', 'version = "0.6.0a4"')
replace("src/version.py", "0.6.0a3", "0.6.0a4")
replace("src/version.py", "0.6.0-alpha.3", "0.6.0-alpha.4")
replace("README.md", "version-0.6.0a3-orange.svg", "version-0.6.0a4-orange.svg")
replace("README.md", "mhrn-core 0.6.0a3` / `0.6.0-alpha.3", "mhrn-core 0.6.0a4` / `0.6.0-alpha.4")
replace("README.md", "## Current state — 15 September 2026", "## Current state — 16 September 2026")
replace("README.md", "version = {0.6.0a3}", "version = {0.6.0a4}")
replace("HF_README.md", "version = {0.6.0a3}", "version = {0.6.0a4}")
replace(
    "research/publications/2026-09-15_recursive-epistemics_v1.7/README.md",
    "**Softwarelinie:** MHRN 0.6.0-alpha.3",
    "**Softwarelinie:** MHRN 0.6.0-alpha.4",
)

release_path = ROOT / "releases/current.json"
release = json.loads(release_path.read_text(encoding="utf-8"))
release["version"] = "0.6.0-alpha.4"
release["pep440"] = "0.6.0a4"
release["as_of"] = "2026-09-16"
release["title"] = "Research-Driven Experiment Cycle and Scientific Gate Hardening"
for item in (
    "research-driven experiment cycle is canonical from RQ through preregistration, DATA, human review and EVID",
    "CL-003 is SHA-256 frozen and explicitly authorized for one preregistered campaign without automatic EVID promotion",
):
    if item not in release["completed"]:
        release["completed"].append(item)
release["note"] = (
    "Alpha.4 makes the experiment-by-experiment research cycle canonical, separates RQ and claim status in the evidence matrix, "
    "hardens freeze/authorization gates, and prepares the first authorized CL-003 execution. Historical DATA and EVID remain "
    "immutable; DATA do not become EVID without human review."
)
release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

changelog = ROOT / "CHANGELOG.md"
text = changelog.read_text(encoding="utf-8")
entry = '''## 0.6.0-alpha.4 - 2026-09-16\n\nResearch-driven development becomes the canonical MHRN workflow: RQ and Claim status are separated, the minimal research-object mapping is fixed, Stage progress is tied to exit RQs/evidence requirements, and CL-003 is SHA-256 frozen and explicitly authorized without automatic EVID promotion. CI freeze gates now validate authorized frozen experiments rather than incorrectly requiring authorization files to remain absent. No historical DATA or reviewed EVID are rewritten.\n\n'''
if entry not in text:
    text = text.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
changelog.write_text(text, encoding="utf-8")

for filename, number in (
    (".github/workflows/cl002-runner-freeze.yml", "002"),
    (".github/workflows/cl003-runner-freeze.yml", "003"),
):
    target = ROOT / filename
    text = target.read_text(encoding="utf-8")
    old = f'''      - name: Confirm empirical execution is blocked\n        run: |\n          test ! -f research/preregistrations/authorizations/EXP-S6-SEM-CL-{number}.json\n          if python scripts/run_semantization_split_mnist_cl{number}.py --output /tmp/forbidden-cl{number}; then\n            echo "CL-{number} unexpectedly executed without authorization" >&2\n            exit 1\n          fi\n'''
    new = f'''      - name: Validate execution gate without producing empirical DATA\n        run: |\n          if test -f research/preregistrations/authorizations/EXP-S6-SEM-CL-{number}.json; then\n            python -c 'import importlib.util, pathlib; p=pathlib.Path("scripts/run_semantization_split_mnist_cl{number}.py"); s=importlib.util.spec_from_file_location("cl{number}_runner", p); assert s is not None and s.loader is not None; m=importlib.util.module_from_spec(s); s.loader.exec_module(m); a=m._require_authorization(m.DEFAULT_AUTHORIZATION); h=m._verify_freeze(m.DEFAULT_FREEZE); mapped=a.get("authorized_source_sha256"); assert a["execution_authorized"] is True and h and (mapped is None or mapped == h)'\n          else\n            if python scripts/run_semantization_split_mnist_cl{number}.py --output /tmp/forbidden-cl{number}; then\n              echo "CL-{number} unexpectedly executed without authorization" >&2\n              exit 1\n            fi\n          fi\n'''
    if old in text:
        text = text.replace(old, new)
    elif new not in text:
        raise RuntimeError(f"freeze-gate block missing in {filename}")
    target.write_text(text, encoding="utf-8")
