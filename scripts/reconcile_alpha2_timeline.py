from __future__ import annotations

import json
import re
from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing replacement anchor: {label}")
    return text.replace(old, new, 1)


def replace_stage(text: str, number: int, next_number: int | None, block: str) -> str:
    start = re.search(rf"^        StageSpec\(\n            {number},", text, re.MULTILINE)
    if start is None:
        raise RuntimeError(f"missing StageSpec {number}")
    if next_number is None:
        end = re.search(r"^    \)\n\n\ndef _safe_json", text[start.start() :], re.MULTILINE)
    else:
        end = re.search(
            rf"^        StageSpec\(\n            {next_number},",
            text[start.start() + 1 :],
            re.MULTILINE,
        )
    if end is None:
        raise RuntimeError(f"missing end for StageSpec {number}")
    offset = start.start() + (0 if next_number is None else 1)
    end_pos = offset + end.start()
    if next_number is None:
        return text[: start.start()] + block + "\n" + text[end_pos:]
    return text[: start.start()] + block + "\n" + text[end_pos:]


def reconcile_profiles() -> None:
    path = "src/profiles/service.py"
    text = read(path)
    if "from src.version import MHRN_VERSION" not in text:
        text = replace_once(
            text,
            "from typing import Any, cast\n",
            "from typing import Any, cast\n\nfrom src.version import MHRN_VERSION\n",
            "profile version import",
        )
    text = text.replace('"runtime_version": "0.6.0a2"', '"runtime_version": MHRN_VERSION')
    text = text.replace('runtime_version: str = "0.6.0a1"', "runtime_version: str = MHRN_VERSION")
    if 'runtime_version: str = "0.6.0a1"' in text:
        raise RuntimeError("stale active alpha1 profile runtime default remains")
    write(path, text)


def reconcile_timeline() -> None:
    path = "src/dashboard/development_timeline.py"
    text = read(path)
    text = replace_once(
        text,
        '    if any(item["status"] == "experimental" for item in criteria):\n        return "active"\n',
        '    if any(item["status"] in {"experimental", "verified"} for item in criteria):\n        return "active"\n',
        "partial verified stage status",
    )

    stage6 = '''        StageSpec(
            6,
            "memory_world_model",
            "Gedächtnis und Weltmodell",
            "Weltmodell",
            (
                "Episodisches und semantisches Gedächtnis",
                "zeitliche Modelle",
                "Vorhersage und Prediction Error",
            ),
            {"neurons": "10^7-10^8", "synapses": "10^9-10^10"},
            (
                CriterionSpec(
                    "temporal_memory",
                    "Temporal state memory",
                    paths=("src/research/temporal.py",),
                    tests=("tests/test_temporal.py",),
                ),
                CriterionSpec(
                    "episodic_memory",
                    "Bounded working and episodic memory foundation",
                    paths=("src/memory/store.py", "src/memory/layer.py"),
                    tests=("tests/test_memory_layer.py", "tests/test_experience_engine.py"),
                ),
                CriterionSpec("semantic_memory", "Semantic memory", planned=True),
                CriterionSpec(
                    "world_model_prediction",
                    "Observation-only one-step world-model prediction foundation",
                    paths=(
                        "src/memory/world_model.py",
                        "src/experience/composition.py",
                        "src/research/cognition_experiments.py",
                    ),
                    tests=(
                        "tests/test_memory_layer.py",
                        "tests/test_cognition_operational_experiments.py",
                    ),
                ),
            ),
            (
                "src/research/temporal.py",
                "src/memory",
                "src/experience/composition.py",
                "src/research/cognition_experiments.py",
            ),
            (
                "tests/test_temporal.py",
                "tests/test_memory_layer.py",
                "tests/test_cognition_operational_experiments.py",
                "tests/test_experience_engine.py",
            ),
            (
                "research/experiments/EXP-EMP-20260910/016-memory_delayed_information_v1",
                "research/experiments/EXP-EMP-20260910/017-world_model_prediction_v1",
            ),
            ("RQ-MEM-002", "RQ-WM-001"),
            (
                "Bounded working/episodic memory is not semantic memory.",
                "The current predictor is observation-only and one-step, not a complete multi-step world model.",
                "The registered cognition campaign is an exploratory component screen with snn_involved=false and is not accepted EVID.",
                "Coupled cognition state is not yet in the canonical runtime checkpoint boundary; pause/resume identity is unproven.",
            ),
            (
                "Couple cognition state to the canonical snapshot/checkpoint boundary and prove pause/resume identity.",
                "Semantic memory remains unimplemented.",
                "Confirmatory SNN-involved memory/world-model evidence remains open.",
            ),
            (
                "Integrate coupled cognition persistence with runtime checkpoints.",
                "Add a provenance-bound semantic-memory and recall contract.",
                "Run confirmatory held-out SNN-involved controls with human evidence review.",
            ),
        ),'''

    stage7 = '''        StageSpec(
            7,
            "self_model_embodied_identity",
            "Selbstmodell und verkörperte Identität",
            "Selbstmodell",
            (
                "Eigenzustand und Umwelt unterscheiden",
                "Handlungsursachen und eigene Sensorik/Aktorik modellieren",
                "dauerhafter interner Zustand",
            ),
            {"neurons": "10^7-10^8+", "synapses": "not specified"},
            (
                CriterionSpec(
                    "versioned_technical_identity",
                    "Versioned technical identity and snapshot binding",
                    paths=("src/profiles/service.py",),
                    tests=("tests/test_profiles.py",),
                ),
                CriterionSpec(
                    "operational_behavior_state",
                    "Persistent operational behavior-state foundation",
                    paths=(
                        "src/profiles/behavior.py",
                        "src/experience/composition.py",
                        "src/research/cognition_experiments.py",
                    ),
                    tests=(
                        "tests/test_memory_layer.py",
                        "tests/test_cognition_operational_experiments.py",
                    ),
                ),
                CriterionSpec("self_model_backend", "Persistent self-model state", planned=True),
                CriterionSpec("causal_action_attribution", "Causal action attribution", planned=True),
                CriterionSpec(
                    "sensor_actuator_confidence",
                    "Sensor and actuator inventory/confidence inputs",
                    paths=("src/embodiment/models.py", "src/embodiment/connections.py"),
                ),
                CriterionSpec("self_model_restore", "Self-model restore identity", planned=True),
            ),
            (
                "src/profiles/service.py",
                "src/profiles/behavior.py",
                "src/experience/composition.py",
                "src/embodiment/models.py",
                "src/embodiment/connections.py",
            ),
            (
                "tests/test_profiles.py",
                "tests/test_memory_layer.py",
                "tests/test_cognition_operational_experiments.py",
            ),
            ("research/experiments/EXP-EMP-20260910/018-behavior_profile_control_v1",),
            ("RQ-PROFILE-001", "RQ6", "RQ7"),
            (
                "Versioned Wesen identity and an operational behavior profile are technical foundations, not a self-model.",
                "Causal self/other attribution and canonical coupled-state restore identity are not implemented.",
                "No consciousness inference is permitted from identity, profile or behavior-state persistence.",
            ),
            (
                "Connect Profile + State loading to the canonical runtime restore hook.",
                "Implement observer-only causal action attribution before recursive feedback.",
                "Keep autonomous identity mutation locked until bounded mutation, journal and rollback gates exist.",
            ),
            (
                "Prove coupled profile/state restore and pause/resume identity.",
                "Add controlled self-versus-external action-attribution experiments.",
            ),
        ),'''

    stage8 = '''        StageSpec(
            8,
            "autonomous_lifelong_development",
            "Autonome lebenslange Entwicklung",
            "Autonome Entwicklung",
            (
                "Continual Learning",
                "autonome Reorganisation",
                "wiederverwendbare Kompetenzen und angepasste Lernstrategien",
            ),
            {"neurons": "10^8-10^9", "synapses": "10^10-10^11"},
            (
                CriterionSpec("continual_learning", "Continual learning", planned=True),
                CriterionSpec("autonomous_reorganization", "Autonomous reorganization", planned=True),
                CriterionSpec("strategy_adaptation", "Learning-strategy adaptation", planned=True),
            ),
            ("src/dashboard/static/development-frontier-placeholders.json",),
            ("tests/test_development_frontier_contract.py",),
            (
                "research/experiments/EXP-LIFE-0001-R1",
                "research/experiments/STAGES_8_10_EXPERIMENT_BACKLOG.md",
                "research/frontiers/STAGES_8_10_FOUNDATIONS.md",
            ),
            ("RQ-LIFE-001", "RQ-GEN-001", "RQ-STRUCT-001", "RQ-HOM-002", "RQ-REPL-001"),
            (
                "Stage-8 theory/design/experiment-planning foundations do not raise implementation maturity.",
                "EXP-LIFE-0001-R1 is an exploratory interference precursor, not evidence of autonomous lifelong learning.",
            ),
            ("E8-A through E8-G remain planned research work.",),
            (
                "Run continuously trained shared-network sequential retention without learned-state resets.",
                "Require rollback, resource-matched controls and independent replication before stronger claims.",
            ),
        ),'''

    stage9 = '''        StageSpec(
            9,
            "integrated_artificial_cognition",
            "Hochintegrierte künstliche Kognition",
            "Integrierte Kognition",
            (
                "Aufmerksamkeit, Motivation und Planung",
                "langfristige Erinnerung",
                "integrierte multimodale Verarbeitung und Konsolidierung",
            ),
            {"neurons": "10^8-10^9+", "synapses": "not specified"},
            (
                CriterionSpec("attention_and_planning", "Attention and planning", planned=True),
                CriterionSpec("integrated_multimodal_processing", "Integrated multimodal processing", planned=True),
                CriterionSpec("consolidation", "Sleep or consolidation phases", planned=True),
            ),
            ("src/dashboard/static/development-frontier-placeholders.json",),
            ("tests/test_development_frontier_contract.py",),
            (
                "research/experiments/STAGES_8_10_EXPERIMENT_BACKLOG.md",
                "research/frontiers/STAGES_8_10_FOUNDATIONS.md",
            ),
            ("RQ-CNS-103", "RQ-CNS-105", "RQ-CNS-110", "RQ-CNS-111", "RQ-CNS-112", "RQ-CNS-116", "RQ-MEM-002", "RQ-WM-001"),
            (
                "Stage-9 material is a research architecture and placeholder contract, not an observed integrated cognitive capability.",
                "Attention, motivation and planning remain operational constructs rather than subjective-state claims.",
            ),
            ("E9-A through E9-G remain planned research work.",),
            (
                "Implement and ablate bounded attention, planning, multimodal integration and consolidation under matched budgets.",
                "Require independent replication for each claimed functional capability.",
            ),
        ),'''

    stage10 = '''        StageSpec(
            10,
            "consciousness_research",
            "Bewusstseinsforschung",
            "Forschungsfrontier",
            (
                "Ausschließlich Forschungsstufe",
                "operationale Kriterien, Interventionen und Reproduzierbarkeit",
                "Ethik- und Abbruchkriterien",
            ),
            {"neurons": "biological reference: ~86 billion", "synapses": "biological reference: ~10^14-10^15"},
            (
                CriterionSpec("operational_criteria", "Predefined operational criteria", planned=True),
                CriterionSpec("independent_replication", "Independent replication", planned=True),
                CriterionSpec("ethics_and_stop_criteria", "Ethics and stop criteria", planned=True),
            ),
            (
                "src/dashboard/static/development-frontier-placeholders.json",
                "src/research/cognition_governance.py",
            ),
            ("tests/test_development_frontier_contract.py",),
            (
                "research/experiments/STAGES_8_10_EXPERIMENT_BACKLOG.md",
                "research/frontiers/STAGES_8_10_FOUNDATIONS.md",
                "research/protocols/COGNITION_CONSCIOUSNESS.md",
                "research/ethics/AI_WELFARE_POLICY.md",
            ),
            ("RQ-CNS-101", "RQ-CNS-108", "RQ-CNS-109", "RQ-CNS-113", "RQ-CNS-114", "RQ-EPI-101", "RQ-EPI-102", "RQ-WEL-101", "RQ-WEL-102", "RQ-WEL-103"),
            (
                "Stage 10 is a research-quality frontier and never automatically establishes consciousness, sentience or moral status.",
                "Theory, literature, ethics and experiment designs do not count as implementation or evidence for consciousness.",
            ),
            ("E10-A through E10-H remain planned research/governance work.",),
            (
                "Preregister contrasting operational predictions and causal interventions.",
                "Require ethics/stop governance and independent adversarial replication before interpretation.",
            ),
        ),'''

    text = replace_stage(text, 6, 7, stage6)
    text = replace_stage(text, 7, 8, stage7)
    text = replace_stage(text, 8, 9, stage8)
    text = replace_stage(text, 9, 10, stage9)
    text = replace_stage(text, 10, None, stage10)

    text = text.replace(
        '("tests/test_msba.py", "tests/test_signal_processing.py"),',
        '(\n                "tests/test_msba.py",\n                "tests/test_signal_processing.py",\n                "tests/test_gateway_runtime.py",\n                "tests/test_msba_experiment_runner.py",\n            ),',
        1,
    )
    write(path, text)


def reconcile_docs() -> None:
    path = "docs/08-roadmap/TODO.md"
    text = read(path)
    old = """- [ ] Connect coupled cognition state to the canonical runtime snapshot/\n  checkpoint boundary and prove pause/resume equivalence.\n- [ ] Add registered delayed-information control runs and dashboard/File Viewer\n  inspection; engineering implementation is not scientific evidence.\n"""
    new = """- [ ] Connect coupled cognition state to the canonical runtime snapshot/\n  checkpoint boundary.\n- [ ] Prove deterministic pause/resume equivalence for the complete coupled\n  cognition state.\n- [x] Execute registered exploratory component controls for delayed information\n  (`016-memory_delayed_information_v1`) and one-step world-model prediction\n  (`017-world_model_prediction_v1`); these runs remain DATA, not automatic EVID.\n- [ ] Add explicit File Viewer drill-down for the existing cognition campaign,\n  including bounded inspection of compressed raw-run data.\n"""
    text = replace_once(text, old, new, "cognition TODO split")
    marker = "## 2026-09-12 Scientific metrics workbench\n"
    section = """## 2026-09-13 Alpha.2 timeline and frontier reconciliation\n\n- [x] Keep the canonical development version at `0.6.0a2` / `0.6.0-alpha.2` and derive active profile runtime defaults from `src.version`.\n- [x] Reconcile Stage 6 with bounded working/episodic memory, one-step transition prediction and the executed exploratory cognition controls; semantic memory and canonical coupled-state restore remain open.\n- [x] Reconcile Stage 7 with versioned Wesen identity, snapshot binding and the operational Behavior Profile while keeping causal self-attribution and a genuine self-model unimplemented.\n- [x] Bind Stages 8-10 to merged theory, literature, experiment backlog and frontend placeholder contracts without raising their `planned`/0 % implementation maturity.\n- [x] Keep historical experiment manifests immutable; recorded `0.6.0a1` provenance is not rewritten after the Alpha.2 advance.\n\n"""
    text = replace_once(text, marker, section + marker, "TODO reconciliation section")
    text = text.replace(
        "**Engineering implementation TODO:** none.  \n",
        "**Release-blocking engineering implementation TODO:** none.  \n**Non-blocking integration TODO:** coupled cognition checkpoint binding, complete-state pause/resume identity, and cognition-campaign File Viewer drill-down.  \n",
        1,
    )
    write(path, text)

    path = "docs/08-roadmap/ROADMAP.md"
    text = read(path)
    marker = "## 2026-09-12 Scientific metrics workbench\n"
    section = """## 2026-09-13 Stage 6/7 reconciliation and Stages 8-10 frontier foundation\n\n- Stage 6 now reflects bounded working/episodic memory, the observation-only `TransitionWorldModel`, ExperienceEngine composition and the registered exploratory 2026-09-10 cognition campaign. Delayed-information and one-step prediction controls were executed; semantic memory, canonical coupled-state checkpointing and SNN-level confirmatory evidence remain open.\n- Stage 7 now reflects versioned technical Wesen identity, digest/revision/lineage, snapshot binding and the persistent operational Behavior Profile. These are foundations only: causal self/other attribution and a genuine operational self-model remain unimplemented.\n- Stages 8-10 now reference their merged research foundation, experiment backlog, literature provenance and frontend placeholder contract. Their maturity intentionally remains `planned`/0 %; planning material is not implementation or EVID.\n- The development version remains `mhrn-core 0.6.0a2`; historical experiment manifests retain the version recorded when they actually ran.\n\n"""
    text = replace_once(text, marker, section + marker, "ROADMAP reconciliation section")
    old = """- Open: coupled runtime snapshot boundary, delayed-cue controls, frozen-model\n  and no-memory comparisons, held-out episodes and independent replication.\n"""
    new = """- Executed exploratory component controls include delayed-cue memory read/write/time-shuffle conditions and adaptive/frozen/persistence/no-model one-step prediction conditions. These are DATA-level screens, not SNN-level cognition evidence.\n- Open: coupled runtime snapshot/checkpoint boundary, full-state pause/resume identity, explicit File Viewer raw-run drill-down, semantic memory, SNN-level held-out confirmatory studies, human review and independent replication.\n"""
    text = replace_once(text, old, new, "ROADMAP memory open items")
    write(path, text)

    path = "docs/08-roadmap/RESEARCH_ROADMAP.md"
    text = read(path)
    text = replace_once(text, "**Updated:** 2026-09-04", "**Updated:** 2026-09-13", "research roadmap date")
    text = replace_once(text, "**Engineering baseline:** `mhrn-core 0.6.0a1`", "**Engineering baseline:** `mhrn-core 0.6.0a2`", "research roadmap baseline")
    anchor = "- a dashboard that exposes research state without treating presentation as evidence.\n"
    addition = """- bounded working/episodic memory and observation-only one-step transition prediction with registered exploratory component controls;\n- versioned technical Wesen identity, operational Behavior Profile state and an experiment-only governed Neural Symbiosis Gateway lifecycle;\n- theory, literature, experiment-planning and frontend-placeholder foundations for Stages 8-10 that remain explicitly `planned` and do not raise capability maturity.\n"""
    text = replace_once(text, anchor, anchor + addition, "research readiness additions")
    write(path, text)


def reconcile_release() -> None:
    path = Path("releases/current.json")
    current = json.loads(path.read_text(encoding="utf-8"))
    if current["pep440"] != "0.6.0a2" or current["version"] != "0.6.0-alpha.2":
        raise RuntimeError("canonical current release is not alpha2")
    frontier_scope = "planned research foundations, experiment backlog, literature provenance and frontend placeholder contracts for stages 8-10 without maturity promotion"
    if frontier_scope not in current["scope"]:
        current["scope"].append(frontier_scope)
    for item in (
        "registered exploratory delayed-information and one-step world-model component controls executed with immutable campaign artifacts",
        "Stages 8-10 research foundation, experiment backlog, frontier literature and planned-only frontend placeholder contract integrated",
    ):
        if item not in current["completed"]:
            current["completed"].append(item)
    old_open = "add registered delayed-information control runs and File Viewer inspection"
    new_open = "add explicit File Viewer drill-down for the existing registered cognition campaign artifacts, including bounded inspection of compressed raw-run data"
    current["open"] = [new_open if item == old_open else item for item in current["open"]]
    if len(current["open"]) != 4:
        raise RuntimeError("unexpected current release open-item count")
    current["research_boundary"] = "Stage-2/3 engineering completion, Stage-6/7 component foundations, frontier planning and a green engineering gate do not constitute scientific evidence; controlled SNN-involved experiments, held-out evaluation, review and replication remain open."
    current["note"] = "Stand 2026-09-13: v0.6.0a2 closes the scoped Stage-2 recurrent-SNN boundary, reaches the Stage-3 plastic-neural-tissue engineering contract, records implemented Stage-6/7 foundations, and integrates research-only foundations for Stages 8-10. Target-scale benchmarks, coupled cognition checkpoint identity and scientific evidence closure remain open."
    path.write_text(json.dumps(current, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def reconcile_tests() -> None:
    path = "tests/test_profiles.py"
    text = read(path)
    if "from src.version import MHRN_VERSION" not in text:
        text = replace_once(text, "import pytest\n\nfrom src.profiles import (", "import pytest\n\nfrom src.version import MHRN_VERSION\nfrom src.profiles import (", "profile test version import")
    anchor = '    profile = service.create(name="Wesen Alpha")\n    assert profile["profile_id"] == "WESEN-0001"\n'
    replacement = '    profile = service.create(name="Wesen Alpha")\n    assert MHRN_VERSION == "0.6.0a2"\n    assert service.runtime_version == MHRN_VERSION\n    assert profile["runtime"]["runtime_version"] == MHRN_VERSION\n    assert profile["provenance"]["runtime_version"] == MHRN_VERSION\n    assert profile["profile_id"] == "WESEN-0001"\n'
    text = replace_once(text, anchor, replacement, "profile alpha2 assertions")
    write(path, text)

    path = "tests/test_development_timeline.py"
    text = read(path)
    text = replace_once(text, "(False, 5, 6, 5.19)", "(False, 5, 6, 5.75)", "fresh timeline score")
    anchor = "def test_runtime_override_and_snapshot_fallback_are_distinct() -> None:\n"
    addition = '''def test_memory_identity_foundations_are_counted_without_overclaiming() -> None:
    with patch("src.dashboard.development_timeline.evaluate_test_baseline", return_value=_baseline(stale=True)):
        payload = build_development_timeline(ROOT)
    stage_six = next(stage for stage in payload["stages"] if stage["stage"] == 6)
    assert stage_six["implementation_score"] == 0.562
    assert stage_six["status"] == "active"
    assert next(item for item in stage_six["criteria"] if item["id"] == "semantic_memory")["status"] == "planned"
    stage_seven = next(stage for stage in payload["stages"] if stage["stage"] == 7)
    assert stage_seven["implementation_score"] == 0.417
    assert stage_seven["status"] == "active"
    assert next(item for item in stage_seven["criteria"] if item["id"] == "self_model_backend")["status"] == "planned"
    assert next(item for item in stage_seven["criteria"] if item["id"] == "causal_action_attribution")["status"] == "planned"


def test_partial_verified_stage_is_active_not_planned() -> None:
    with patch("src.dashboard.development_timeline.evaluate_test_baseline", return_value=_baseline(stale=False)):
        payload = build_development_timeline(ROOT)
    stage_six = next(stage for stage in payload["stages"] if stage["stage"] == 6)
    assert stage_six["implementation_score"] == 0.75
    assert stage_six["verification_score"] == 0.75
    assert stage_six["status"] == "active"


'''
    text = replace_once(text, anchor, addition + anchor, "timeline foundation tests")
    write(path, text)

    path = "tests/test_release_registry.py"
    text = read(path)
    old = '    assert current["open"]\n    assert "scientific evidence" in current["research_boundary"]\n'
    new = '    assert len(current["open"]) == 4\n    assert len(current["scope"]) == 9\n    assert any("stages 8-10" in item for item in current["scope"])\n    assert any("File Viewer drill-down" in item for item in current["open"])\n    assert not any("add registered delayed-information control runs" in item for item in current["open"])\n    assert "scientific evidence" in current["research_boundary"]\n'
    text = replace_once(text, old, new, "release registry assertions")
    write(path, text)

    write(
        "tests/test_development_frontier_contract.py",
        '''from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from src.dashboard.development_timeline import build_development_timeline
from src.dashboard.verification import BaselineEvaluation

ROOT = Path(__file__).resolve().parents[1]


def _baseline() -> BaselineEvaluation:
    return BaselineEvaluation(True, False, 1, 0, 0, 0, None, None, None, None)


def test_frontier_contract_is_research_only_and_references_real_files() -> None:
    contract = json.loads((ROOT / "src/dashboard/static/development-frontier-placeholders.json").read_text(encoding="utf-8"))
    assert contract["status"] == "PLANNED_RESEARCH_ONLY"
    assert set(contract["stages"]) == {"8", "9", "10"}
    for stage in contract["stages"].values():
        assert (ROOT / stage["research_document"]).is_file()
        assert (ROOT / stage["experiment_backlog"]).is_file()


def test_frontier_foundations_do_not_raise_timeline_maturity() -> None:
    with patch("src.dashboard.development_timeline.evaluate_test_baseline", return_value=_baseline()):
        timeline = build_development_timeline(ROOT)
    for number in (8, 9, 10):
        stage = next(item for item in timeline["stages"] if item["stage"] == number)
        assert stage["implementation_score"] == 0.0
        assert stage["status"] == "planned"
        assert all(item["status"] == "planned" for item in stage["criteria"])
''',
    )


def main() -> None:
    reconcile_profiles()
    reconcile_timeline()
    reconcile_docs()
    reconcile_release()
    reconcile_tests()


if __name__ == "__main__":
    main()
