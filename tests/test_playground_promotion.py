"""Playground-to-MHRN promotion contract tests."""

from __future__ import annotations

from src.embodiment.neural_io_adapter import NeuralIOAreaAdapter
from src.embodiment.neural_io_codecs import encode_input as canonical_encode_input
from src.embodiment.neural_io_contracts import BoundaryFrame as CanonicalBoundaryFrame
from src.playground.integration import integration_catalog, transfer_element
from src.playground.neural_io.adapter import PlaygroundIOAreaAdapter
from src.playground.neural_io.codecs import encode_input as playground_encode_input
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
    assert candidates["execution_backend"]["status"] == "INTEGRATED"
    assert candidates["parity_determinism"]["status"] == "INTEGRATED"
    assert candidates["cuda_execution"]["status"] == "INTEGRATED"
    assert (
        candidates["closed_loop"]["status"] == "FE_CONTRACT_EXECUTABLE_CUDA_D3_PENDING"
    )
    assert candidates["closed_loop"]["next_gate"] == "FE3_CPU_CUDA_CAUSAL_PARITY"
    assert candidates["old_frontend_views"]["status"] == "RETAINED_NOT_CORE"
    assert "science-snn" in candidates["old_frontend_views"]["old_routes"]


def test_transfer_endpoint_is_idempotent_verification_not_runtime_code_mutation() -> (
    None
):
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


def test_playground_neural_io_codecs_are_canonical_reexports() -> None:
    assert playground_encode_input is canonical_encode_input
    result = transfer_element({"element_id": "neural_io_codecs"})
    assert result["status"] == "INTEGRATED"
    assert result["applied"] is True
    assert result["same_codec_function"] is True


def test_playground_adapter_wraps_canonical_network_area_adapter() -> None:
    assert issubclass(PlaygroundIOAreaAdapter, NeuralIOAreaAdapter)
    adapter = PlaygroundIOAreaAdapter()
    assert adapter.area_id == "playground.io.reference"
    assert adapter.process({"value": 1}, 0) == {"value": 1}
    result = transfer_element({"element_id": "neural_io_adapter"})
    assert result["status"] == "INTEGRATED"
    assert result["applied"] is True
    assert result["playground_wrapper_subclasses_canonical"] is True
    assert result["network_area_adapter_contract"] is True


def test_wave3_execution_backend_and_parity_are_canonical_consumers() -> None:
    backend = transfer_element({"element_id": "execution_backend"})
    assert backend["status"] == "INTEGRATED"
    assert backend["applied"] is True
    assert backend["backend_neutral_state"] is True

    parity = transfer_element({"element_id": "parity_determinism"})
    assert parity["status"] == "INTEGRATED"
    assert parity["applied"] is True
    assert parity["same_parity_function"] is True
    assert parity["same_counter_rng_function"] is True

    cuda = transfer_element({"element_id": "cuda_execution"})
    assert cuda["status"] == "INTEGRATED"
    assert cuda["applied"] is True
    assert cuda["same_recurrent_execute_function"] is True
    assert cuda["execution_backend_contract"] is True
    assert cuda["execution_mode"] == "BOUNDED_REPLAY_REFERENCE"
    assert cuda["plasticity_semantics"] == "NON_CANONICAL_DRAFT"
    assert cuda["d3_complete"] is False
    assert cuda["next_gate"] == "WAVE5_RESIDENT_PAN_AND_ENVIRONMENT"
