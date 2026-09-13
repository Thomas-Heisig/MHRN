"""Apply the Stage-2 closure / Stage-3 development metadata patch.

This script is intentionally narrow and assertion-heavy. It exists so the
large canonical files can be updated atomically on the feature branch by CI.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def replace(path: str, old: str, new: str, *, count: int = 1) -> None:
    file = ROOT / path
    text = file.read_text(encoding="utf-8")
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{path}: expected {count} occurrence(s), got {actual}: {old!r}")
    file.write_text(text.replace(old, new, count), encoding="utf-8")


def prepend_after(path: str, marker: str, addition: str) -> None:
    file = ROOT / path
    text = file.read_text(encoding="utf-8")
    if addition.strip() in text:
        return
    if marker not in text:
        raise SystemExit(f"{path}: marker not found: {marker!r}")
    file.write_text(text.replace(marker, marker + addition, 1), encoding="utf-8")


def update_timeline() -> None:
    path = "src/dashboard/development_timeline.py"
    replace(
        path,
        '                "The scoped four-neuron ring does not establish target-scale tractability or stability for arbitrary recurrent networks.",\n',
        '                "Stage 2 is technically complete at the scoped deterministic recurrence boundary; target-scale tractability remains a separate benchmark question.",\n',
    )
    replace(
        path,
        '            (\n                "Benchmark recurrent stability and throughput at the declared 1,000-10,000 neuron Stage-2 scale.",\n            ),\n',
        '            (),\n',
    )
    replace(
        path,
        '                    tests=("tests/test_stdp_integration.py",),\n                ),\n',
        '                    tests=("tests/test_stdp_integration.py",),\n                    verification=(\n                        "research/generated/verification/plastic_neural_tissue_reference.json",\n                    ),\n                ),\n',
    )
    replace(
        path,
        '                    tests=("tests/test_learning_engine.py",),\n                ),\n',
        '                    tests=(\n                        "tests/test_reward.py",\n                        "tests/test_learning_experiment.py",\n                    ),\n                    verification=(\n                        "research/generated/verification/plastic_neural_tissue_reference.json",\n                    ),\n                ),\n',
    )
    replace(
        path,
        '                    tests=("tests/test_homeostasis.py",),\n                ),\n',
        '                    tests=("tests/test_homeostasis_engine.py",),\n                    verification=(\n                        "research/generated/verification/plastic_neural_tissue_reference.json",\n                    ),\n                ),\n',
    )
    replace(
        path,
        '                    verification=(\n                        "research/generated/verification/structural_e2e.json",\n                    ),\n                ),\n                CriterionSpec(\n                    "long_run_stability_verified",\n                    "Long-run stability verification",\n                    tests=(\n                        "tests/test_v06_contract.py",\n                        "tests/test_research_data_v2.py",\n                    ),\n                    verification=(\n                        "research/generated/verification/determinism_infrastructure.json",\n                    ),\n                ),\n',
        '                    verification=(\n                        "research/generated/verification/structural_e2e.json",\n                        "research/generated/verification/plastic_neural_tissue_reference.json",\n                    ),\n                ),\n                CriterionSpec(\n                    "integrated_plasticity_reference",\n                    "Integrated plasticity reference and persisted adaptive state",\n                    tests=(\n                        "tests/test_stage3_plastic_neural_tissue.py",\n                        "tests/test_checkpoint_v4.py",\n                    ),\n                    verification=(\n                        "research/generated/verification/plastic_neural_tissue_reference.json",\n                    ),\n                ),\n',
    )
    replace(
        path,
        '            ("tests/test_v06_contract.py", "tests/test_research_data_v2.py"),\n            ("src/experiments/learning_lab.py",),\n',
        '            (\n                "tests/test_stdp_integration.py",\n                "tests/test_reward.py",\n                "tests/test_learning_experiment.py",\n                "tests/test_homeostasis_engine.py",\n                "tests/test_structural_e2e.py",\n                "tests/test_structural_determinism.py",\n                "tests/test_checkpoint_v4.py",\n                "tests/test_stage3_plastic_neural_tissue.py",\n            ),\n            (\n                "src/experiments/learning_lab.py",\n                "scripts/run_stage3_reference.py",\n                "research/generated/verification/plastic_neural_tissue_reference.json",\n            ),\n',
    )
    replace(
        path,
        '            (\n                "Scaling beyond the measured runtime remains a future benchmark question.",\n            ),\n            ("R2 productive-learning evidence closure",),\n            ("Run preregistered learning-on/off and holdout experiments.",),\n',
        '            (\n                "The scoped reference does not establish the declared 10,000-100,000 neuron Stage-3 target scale.",\n                "Engineering verification does not promote productive-learning DATA to scientific EVID.",\n            ),\n            ("R2 productive-learning evidence closure",),\n            (\n                "Run preregistered independent learning-on/off, sham/information-destroyed and held-out experiments with human evidence review.",\n            ),\n',
    )


def update_version() -> None:
    replace("pyproject.toml", 'version = "0.6.0a1"', 'version = "0.6.0a2"')
    replace("src/version.py", "0.6.0a1", "0.6.0a2", count=3)
    replace("src/version.py", "0.6.0-alpha.1", "0.6.0-alpha.2", count=1)
    replace(
        "start.cmd",
        'if /I "!MHRN_VERSION!"=="0.6.0a1" set "MHRN_DISPLAY_VERSION=0.6.0-alpha.1"',
        'if /I "!MHRN_VERSION!"=="0.6.0a2" set "MHRN_DISPLAY_VERSION=0.6.0-alpha.2"',
    )
    replace("src/profiles/service.py", '"runtime_version": "0.6.0a1"', '"runtime_version": "0.6.0a2"')
    replace("README.md", "version-0.6.0a1-orange", "version-0.6.0a2-orange")
    replace("HF_README.md", "version = {0.6.0a1}", "version = {0.6.0a2}")
    replace("docs/README.md", "package version: `0.6.0a1`", "package version: `0.6.0a2`")
    replace("docs/08-roadmap/ROADMAP.md", "**Baseline:** `mhrn-core 0.6.0a1`", "**Baseline:** `mhrn-core 0.6.0a2`")
    replace("docs/08-roadmap/TODO.md", "**Baseline:** `mhrn-core 0.6.0a1`", "**Baseline:** `mhrn-core 0.6.0a2`")

    current_path = ROOT / "releases" / "current.json"
    current = json.loads(current_path.read_text(encoding="utf-8"))
    current.update(
        {
            "version": "0.6.0-alpha.2",
            "pep440": "0.6.0a2",
            "title": "Plastic Neural Tissue Verification",
            "as_of": "2026-09-13",
            "milestone_status": "stage3_engineering_reached",
        }
    )
    scope = list(current.get("scope", []))
    new_scope = "scoped Stage-3 plastic neural tissue verification with explicit scientific-evidence separation"
    if new_scope not in scope:
        scope.append(new_scope)
    current["scope"] = scope
    completed = list(current.get("completed", []))
    for item in (
        "Stage-2 stable recurrent SNN engineering contract closed with deterministic long-run and restore/replay verification",
        "Stage-3 STDP, three-factor plasticity, homeostasis, structural plasticity and adaptive-state persistence reference integrated",
    ):
        if item not in completed:
            completed.append(item)
    current["completed"] = completed
    current["research_boundary"] = (
        "Stage-2/3 engineering completion and a green gate do not constitute scientific evidence; "
        "controlled learning experiments, held-out evaluation, review and replication remain open."
    )
    current["note"] = (
        "Stand 2026-09-13: v0.6.0a2 closes the scoped Stage-2 recurrent-SNN engineering boundary "
        "and reaches the Stage-3 plastic-neural-tissue engineering contract. Target-scale benchmarks "
        "and R2 productive-learning evidence closure remain scientific/empirical follow-up work."
    )
    current_path.write_text(json.dumps(current, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_docs() -> None:
    roadmap = """

## 2026-09-13 Stage 2 closure and Stage 3 plastic neural tissue

- Closed Stage 2 at the scoped engineering boundary after the merged recurrent
  reference contract proved sustained bounded activity, deterministic replay,
  long-run execution and restart/restore continuity. The declared 1,000-10,000
  neuron scale remains a separate performance benchmark, not a completion
  blocker for recurrence mechanics.
- Added the Stage-3 plastic-neural-tissue contract and deterministic reference
  runner covering STDP, signed eligibility, delayed reward/three-factor
  plasticity, homeostasis, structural plasticity and checkpointed adaptive
  state.
- Added matched `learning_on`, `learning_off` and `sham_replay` controls plus a
  deterministic replay identity check. The reference is engineering
  verification only and cannot create or promote scientific EVID.
- Advanced the development version to `mhrn-core 0.6.0a2`.
- R2 productive-learning evidence closure, held-out independent runs and
  target-scale plastic-network benchmarks remain open research work.
"""
    prepend_after("docs/08-roadmap/ROADMAP.md", "**Updated:** 2026-09-13\n", roadmap)

    todo = """

## 2026-09-13 Stage 2 / Stage 3 development boundary

- [x] Close the scoped Stage-2 recurrent-SNN engineering contract with long-run,
  deterministic replay and restore verification.
- [x] Add a Stage-3 contract joining STDP, three-factor learning, homeostasis,
  structural plasticity and checkpointed adaptive state.
- [x] Add deterministic learning-on/off/sham controls and a generated
  verification artifact without automatic EVID promotion.
- [ ] Close R2 productive-learning evidence with preregistered independent
  runs, held-out evaluation and human evidence review.
- [ ] Benchmark plastic-network stability/throughput at the declared Stage-3
  target scale separately from the mechanism contract.
"""
    prepend_after("docs/08-roadmap/TODO.md", "**Current release-blocking backlog:** **0**\n", todo)

    change = """

### Stage 2 recurrence closure / Stage 3 plastic neural tissue

- Closed the scoped Stage-2 engineering boundary using the merged recurrent SNN
  long-run/replay/restore contract while keeping target-scale performance a
  separate benchmark question.
- Added `PLASTIC_NEURAL_TISSUE_CONTRACT.md`, a deterministic Stage-3 reference
  runner and regression coverage for STDP, reward-modulated three-factor
  learning, homeostasis, structural plasticity and checkpointed adaptive state.
- Added `learning_on`, `learning_off` and `sham_replay` controls and explicitly
  prohibited automatic scientific evidence promotion from the engineering
  verification artifact.
- Advanced the active development version to `0.6.0a2` / `0.6.0-alpha.2`.
"""
    prepend_after("CHANGELOG.md", "## Unreleased\n", change)


if __name__ == "__main__":
    update_timeline()
    update_version()
    update_docs()
