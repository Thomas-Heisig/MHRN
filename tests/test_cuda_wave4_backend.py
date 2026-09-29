"""Wave-4 canonical CUDA backend and cross-backend parity gates."""

from __future__ import annotations

import os

import pytest

from src.acceleration.cuda import CUDABackend, execution_backend_contract_check
from src.acceleration.cuda.plasticity.contracts import (
    LEARNING_CONTRACT_STATUS,
    PLASTICITY_SEMANTICS,
)
from src.acceleration.cuda.recurrent import (
    CPUReferenceBackend,
    recurrent_fixture,
    recurrent_inputs_to_mapping,
)
from src.playground.cuda import recurrent as playground_recurrent
from src.playground.cuda import synapses as playground_synapses
from src.runtime.backend import ExecutionBackend
from src.verification.parity import (
    config_fingerprint,
    exact_spike_parity,
    state_vector_parity,
)


def test_cuda_backend_satisfies_execution_protocol_and_declares_draft_plasticity() -> (
    None
):
    backend = CUDABackend()
    assert isinstance(backend, ExecutionBackend)
    assert execution_backend_contract_check()
    capabilities = backend.capabilities()
    assert capabilities.supports_recurrent is True
    assert capabilities.supports_plasticity is True
    assert capabilities.supports_pan_hyperstate is False
    assert capabilities.supports_structural_plasticity is False
    assert capabilities.max_neurons == 4096
    assert capabilities.max_ticks == 2000
    assert capabilities.max_edges == 65536
    assert capabilities.deterministic is True
    assert capabilities.plasticity_semantics == "NON_CANONICAL_DRAFT"
    assert capabilities.execution_mode == "BOUNDED_REPLAY_REFERENCE"
    assert PLASTICITY_SEMANTICS == "NON_CANONICAL_DRAFT"
    assert LEARNING_CONTRACT_STATUS == "ALIGNMENT_PENDING"


def test_playground_recurrent_and_plasticity_paths_are_compatibility_consumers() -> (
    None
):
    from src.acceleration.cuda.plasticity.reference import SynapseConfig
    from src.acceleration.cuda.recurrent import execute_recurrent

    assert playground_recurrent.execute_recurrent is execute_recurrent
    assert playground_synapses.SynapseConfig is SynapseConfig


def test_backend_snapshot_is_data_only_and_restoreable_without_device_handles() -> None:
    inputs = recurrent_fixture(n_neurons=8, ticks=4, model="lif")
    config = recurrent_inputs_to_mapping(inputs)
    backend = CUDABackend()
    backend.initialize(config, 12345)
    snapshot = backend.snapshot()
    assert snapshot.tick == 0
    assert snapshot.payload["replay_required"] is True
    assert "ptr" not in repr(snapshot.payload).lower()
    restored = CUDABackend()
    restored.restore(snapshot)
    assert restored.snapshot().state_digest == snapshot.state_digest


def test_execution_fingerprint_is_backend_specific_while_config_identity_is_shared() -> (
    None
):
    config = recurrent_inputs_to_mapping(
        recurrent_fixture(n_neurons=8, ticks=4, model="lif")
    )
    cpu = CPUReferenceBackend()
    cuda = CUDABackend()
    cpu.initialize(config, 12345)
    cuda.initialize(config, 12345)
    assert config_fingerprint(config) == config_fingerprint(
        dict(cuda.snapshot().payload["config"])
    )
    # Execution fingerprints include backend identity by Wave-3 contract.
    from src.verification.parity import execution_fingerprint

    config_hash = config_fingerprint(config)
    cpu_fp = execution_fingerprint(
        seed=12345,
        config_hash=config_hash,
        backend_name=cpu.backend_name,
        backend_version=cpu.backend_version,
        ticks=4,
    )
    cuda_fp = execution_fingerprint(
        seed=12345,
        config_hash=config_hash,
        backend_name=cuda.backend_name,
        backend_version=cuda.backend_version,
        ticks=4,
    )
    assert cpu_fp != cuda_fp


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1",
    reason="opt-in physical CUDA cross-backend acceptance",
)
def test_physical_cpu_cuda_cross_backend_d1_d2_parity() -> None:
    inputs = recurrent_fixture(n_neurons=129, ticks=100, model="pan_adex_5d")
    config = recurrent_inputs_to_mapping(inputs)
    cpu = CPUReferenceBackend()
    cuda = CUDABackend()
    cpu.initialize(config, 12345)
    cuda.initialize(config, 12345)

    reference = cpu.run(100)
    candidate = cuda.run(100)

    reference_events = tuple(
        (step.tick, neuron) for step in reference.steps for neuron in step.spikes
    )
    candidate_events = tuple(
        (step.tick, neuron) for step in candidate.steps for neuron in step.spikes
    )
    assert exact_spike_parity(reference_events, candidate_events).passed

    reference_voltage = [
        float(value)
        for step in reference.steps
        for value in step.metrics["voltage"]  # type: ignore[union-attr]
    ]
    candidate_voltage = [
        float(value)
        for step in candidate.steps
        for value in step.metrics["voltage"]  # type: ignore[union-attr]
    ]
    assert state_vector_parity(
        reference_voltage,
        candidate_voltage,
        tolerance=1.0e-4,
    ).passed

    # Backend identity is provenance and therefore intentionally differs.
    assert reference.execution_fingerprint != candidate.execution_fingerprint
