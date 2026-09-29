"""Playground-to-MHRN promotion contract tests."""

from __future__ import annotations

from src.embodiment.neural_io_contracts import BoundaryFrame as CanonicalBoundaryFrame
from src.playground.integration import integration_catalog, transfer_element
from src.playground.neural_io.contracts import BoundaryFrame as PlaygroundBoundaryFrame


def test_playground_neural_io_contracts_are_canonical_reexports() -> None:
    assert PlaygroundBoundaryFrame is CanonicalBoundaryFrame


def test_integration_catalog_is_non_evidentiary_and_directional() -> None:
    catalog = integration_catalog()
    assert catalog["classification"] == "PLAYGROUND_TO_MHRN_INTEGRATION_CATALOG"
    assert catalog["scientific_evidence"] is False
    assert catalog["runtime_source_mutation"] is False
    assert (
        catalog["dependency_rule"]
        == "PLAYGROUND_USES_MHRN_MHRN_DOES_NOT_IMPORT_PLAYGROUND"
    )
    candidates = {item["element_id"]: item for item in catalog["candidates"]}
    assert candidates["neural_io_contracts"]["status"] == "INTEGRATED"
    assert candidates["old_frontend_views"]["status"] == "RETAINED_NOT_CORE"
    assert "science-snn" in candidates["old_frontend_views"]["old_routes"]


def test_transfer_endpoint_is_idempotent_verification_not_runtime_code_mutation() -> None:
    result = transfer_element({"element_id": "neural_io_contracts"})
    assert result["status"] == "INTEGRATED"
    assert result["applied"] is True
    assert result["same_contract_object"] is True
    assert result["runtime_source_mutation"] is False


def test_blocked_transfer_returns_declared_gate() -> None:
    result = transfer_element({"element_id": "learning_synapse"})
    assert result["applied"] is False
    assert result["status"] == "BLOCKED_CONTRACT_FREEZE"
    assert result["next_gate"] == "MHRN_LEARNING_SYNAPSE_CONTRACT"
