"""Idempotently bind Stage 5 timeline criteria to the Stage-5 verification contract."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIMELINE = ROOT / "src/dashboard/development_timeline.py"
TESTS = ROOT / "tests/test_development_timeline.py"
VERIFY = "research/generated/verification/integrated_nervous_system_reference_alpha3.json"

NEW_STAGE5 = '''        StageSpec(
            5,
            "integrated_artificial_nervous_system",
            "Integriertes künstliches Nervensystem",
            "Nervensystem",
            (
                "Sensorik, Interozeption und Aktorik",
                "Feedbackschleifen",
                "Embodiment und Ressourcenhaushalt",
            ),
            {"neurons": "10^6-10^7", "synapses": "10^8-10^9"},
            (
                CriterionSpec(
                    "sensor_contracts",
                    "Sensor input contracts",
                    paths=(
                        "src/embodiment/models.py",
                        "src/embodiment/connections.py",
                        "src/embodiment/integrated_nervous_system.py",
                    ),
                    tests=("tests/test_stage5_integrated_nervous_system.py",),
                    verification=(
                        "research/generated/verification/integrated_nervous_system_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "interoception",
                    "Interoception",
                    paths=("src/embodiment/interoception.py",),
                    tests=("tests/test_stage5_integrated_nervous_system.py",),
                    verification=(
                        "research/generated/verification/integrated_nervous_system_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "authorized_actuation",
                    "Authorized actuator path",
                    paths=("src/embodiment/controlled.py", "src/embodiment/audit.py"),
                    tests=(
                        "tests/test_embodiment_lab.py",
                        "tests/test_stage5_integrated_nervous_system.py",
                    ),
                    verification=(
                        "research/generated/verification/integrated_nervous_system_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "closed_loop_environment",
                    "Closed-loop environment",
                    paths=(
                        "src/experience/engine.py",
                        "src/embodiment/deterministic.py",
                    ),
                    tests=(
                        "tests/test_experience_engine.py",
                        "tests/test_embodiment_lab.py",
                        "tests/test_stage5_integrated_nervous_system.py",
                    ),
                    verification=(
                        "research/generated/verification/integrated_nervous_system_reference_alpha3.json",
                    ),
                ),
                CriterionSpec(
                    "resource_accounting",
                    "Resource accounting",
                    paths=(
                        "src/embodiment/interoception.py",
                        "src/embodiment/msba.py",
                    ),
                    tests=(
                        "tests/test_interoception.py",
                        "tests/test_stage5_integrated_nervous_system.py",
                    ),
                    verification=(
                        "research/generated/verification/integrated_nervous_system_reference_alpha3.json",
                    ),
                ),
            ),
            (
                "src/embodiment",
                "src/experience",
                "src/embodiment/integrated_nervous_system.py",
                "src/dashboard/static/frontend/modules/integrated-nervous-system.js",
            ),
            (
                "tests/test_stage5_integrated_nervous_system.py",
                "tests/test_stage5_frontend_contract.py",
                "tests/test_embodiment_lab.py",
                "tests/test_experience_engine.py",
                "tests/test_interoception.py",
            ),
            (
                "research/experiments/EXP-STAGE5-20260914-INTEGRATED-NERVOUS-SYSTEM",
            ),
            ("RQ-EMB-001", "RQ6", "RQ7", "RQ8", "RQ9"),
            (
                "The verified reference environment is synthetic and deterministic; real-device and long-horizon embodiment claims remain out of scope.",
                "Host telemetry is digital interoception, not biological interoception or metabolism.",
                "H-EMB-001-A is DATA-supported only; H-EMB-001-B remains untested by the Stage-5 reference protocol.",
                "No automatic EVID promotion or consciousness claim follows from Stage-5 completion.",
            ),
            (
                "R3 scientific evidence closure remains separate from scoped Stage-5 engineering completion.",
                "H-EMB-001-B still requires matched disturbance, yoked replay and interrupted-feedback tracking metrics.",
            ),
            (
                "Run independent confirmatory closed-loop replication before any EVID promotion.",
                "Preregister and execute the matched-disturbance H-EMB-001-B protocol.",
                "Validate real-device adapters and long-horizon operation as separate safety-gated studies.",
            ),
        ),
'''


def patch_timeline() -> bool:
    text = TIMELINE.read_text(encoding="utf-8")
    if VERIFY in text:
        return False
    start = text.index('        StageSpec(\n            5,\n            "integrated_artificial_nervous_system",')
    end = text.index('        StageSpec(\n            6,\n            "memory_world_model",', start)
    TIMELINE.write_text(text[:start] + NEW_STAGE5 + text[end:], encoding="utf-8")
    return True


def patch_tests() -> bool:
    text = TESTS.read_text(encoding="utf-8")
    changed = False
    old = '[(True, 4, 5, 4.95), (False, 4, 5, 5.0)]'
    new = '[(True, 5, 6, 5.56), (False, 5, 6, 5.69)]'
    if old in text:
        text = text.replace(old, new, 1)
        changed = True
    marker = '    assert any("100k-neuron/10M-edge" in item for item in stage_four["known_limits"])\n'
    addition = '''\n    stage_five = next(stage for stage in payload["stages"] if stage["stage"] == 5)\n    assert stage_five["status"] == "reached"\n    assert stage_five["implementation_score"] == 1.0\n    assert stage_five["verification_score"] == 1.0\n    assert all(item["status"] == "verified" for item in stage_five["criteria"])\n    assert any("H-EMB-001-B" in item for item in stage_five["known_limits"])\n'''
    if addition.strip() not in text and marker in text:
        text = text.replace(marker, marker + addition, 1)
        changed = True
    if changed:
        TESTS.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    changed = [patch_timeline(), patch_tests()]
    print("Stage-5 timeline integration updated." if any(changed) else "Stage-5 timeline integration already current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
