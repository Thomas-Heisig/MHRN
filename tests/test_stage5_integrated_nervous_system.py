"""Stage-5 contract and scientific-boundary regression tests."""

from src.embodiment.integrated_nervous_system import (
    STAGE5_REFERENCE_EXPERIMENT,
    integrated_nervous_system_contract,
    reference_interoception_probe,
)


def test_stage5_contract_covers_all_integrated_layers() -> None:
    contract = integrated_nervous_system_contract()
    assert contract["stage"] == 5
    assert set(contract["layers"]) == {
        "sensorik",
        "interozeption",
        "aktorik",
        "feedback",
        "ressourcenhaushalt",
    }
    assert all(layer["implemented"] for layer in contract["layers"].values())


def test_stage5_runtime_projection_uses_existing_full_stack_apis() -> None:
    runtime = integrated_nervous_system_contract()["runtime_projection"]
    assert runtime == {
        "state": "/api/embodiment/state",
        "pipeline": "/api/embodiment/pipeline",
        "metrics": "/api/embodiment/metrics",
        "history": "/api/embodiment/history",
        "connections": "/api/embodiment/connections",
        "sensors": "/api/embodiment/sensors",
    }


def test_stage5_reference_interoception_probe_is_deterministic_and_bounded() -> None:
    first = reference_interoception_probe()
    second = reference_interoception_probe()
    assert first == second
    assert first["frame"]["tick"] == 1
    assert first["drives"]["drives"]["resource_pressure"] is not None
    assert first["regulatory"]["values"]["energy_reserve"] is not None
    functional = first["functional"]
    for key in ("valence", "activation", "safety"):
        value = functional[key]
        assert value is None or -1.0 <= value <= 1.0


def test_stage5_boundaries_prevent_overclaiming() -> None:
    boundaries = integrated_nervous_system_contract()["boundaries"]
    assert boundaries["productive_external_actuation_enabled"] is False
    assert boundaries["real_device_verified"] is False
    assert boundaries["long_horizon_verified"] is False
    assert boundaries["biological_interoception_claim"] is False
    assert boundaries["biological_metabolism_claim"] is False
    assert boundaries["conscious_experience_claim"] is False
    assert boundaries["automatic_evidence_promotion"] is False


def test_stage5_experiment_traceability_is_data_only() -> None:
    experiment = integrated_nervous_system_contract()["experiment"]
    assert experiment["path"] == STAGE5_REFERENCE_EXPERIMENT
    assert experiment["research_question"] == "RQ-EMB-001"
    assert experiment["hypotheses"] == ["H-EMB-001-A", "H-EMB-001-B"]
    assert experiment["status"] == "DATA"
    assert experiment["automatic_evidence_promotion"] is False
