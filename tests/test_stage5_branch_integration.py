"""Prevent the parallel Stage-5 and reader entrypoints from replacing each other."""

from pathlib import Path

from src.embodiment.integrated_nervous_system import integrated_nervous_system_contract

ROOT = Path(__file__).resolve().parents[1]


def test_reader_and_stage5_bootstrap_survive_branch_integration() -> None:
    source = (ROOT / "src/dashboard/static/frontend/index.js").read_text(
        encoding="utf-8"
    )
    for name, module in (
        ("initIntegratedNervousSystem", "integrated-nervous-system"),
        ("initPublicationScholarTools", "publication-scholar-bootstrap"),
        ("initCognition", "cognition"),
    ):
        assert source.count(f"{name}();") == 1
        assert f'from "./modules/{module}.js"' in source
        assert (ROOT / f"src/dashboard/static/frontend/modules/{module}.js").is_file()


def test_stage5_contract_keeps_existing_runtime_and_evidence_boundaries() -> None:
    contract = integrated_nervous_system_contract()
    for layer in contract["layers"].values():
        assert all((ROOT / path).exists() for path in layer["paths"])
    assert contract["boundaries"]["productive_external_actuation_enabled"] is False
    assert contract["boundaries"]["automatic_evidence_promotion"] is False
    assert contract["boundaries"]["long_horizon_verified"] is False
