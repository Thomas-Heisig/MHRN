"""Controlled Playground -> MHRN promotion registry.

Canonical MHRN modules must never import this Playground-side orchestration.
A transfer action verifies or prepares a promotion; it never edits repository
source code at runtime.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class PromotionCandidate:
    element_id: str
    label: str
    status: str
    source_paths: tuple[str, ...]
    target_paths: tuple[str, ...]
    next_gate: str
    old_routes: tuple[str, ...] = ()
    notes: str = ""

    def to_mapping(self) -> dict[str, object]:
        return asdict(self)


_CANDIDATES: tuple[PromotionCandidate, ...] = (
    PromotionCandidate(
        "neural_io_contracts",
        "Neural I/O Contracts",
        "INTEGRATED",
        ("src/playground/neural_io/contracts.py",),
        ("src/embodiment/neural_io_contracts.py",),
        "CANONICAL_IMPORT_IDENTITY",
        notes=(
            "BoundaryFrame, CodecContract, PopulationLayout, SpikeFrame and "
            "DecodeResult are canonical MHRN contracts; Playground is a compatibility re-export."
        ),
    ),
    PromotionCandidate(
        "neural_io_codecs",
        "Neural I/O Codecs",
        "INTEGRATED",
        ("src/playground/neural_io/codecs.py",),
        ("src/embodiment/neural_io_codecs.py",),
        "CANONICAL_CODEC_IDENTITY",
        notes=(
            "Deterministic input codecs and output decoders are canonical MHRN "
            "implementations; Playground is a compatibility re-export."
        ),
    ),
    PromotionCandidate(
        "neural_io_adapter",
        "Neural I/O Area Adapter",
        "INTEGRATED",
        ("src/playground/neural_io/adapter.py",),
        ("src/embodiment/neural_io_adapter.py",),
        "NETWORK_AREA_ADAPTER_PROTOCOL",
        notes=(
            "The framework-neutral NetworkAreaAdapter implementation is owned by "
            "MHRN; Playground keeps only an identity wrapper."
        ),
    ),
    PromotionCandidate(
        "execution_backend",
        "ExecutionBackend Contract",
        "INTEGRATED",
        ("src/playground/cuda/",),
        ("src/runtime/backend.py",),
        "CANONICAL_EXECUTION_BACKEND_PROTOCOL",
        notes=(
            "Backend-neutral initialize/step/run/snapshot/restore/capabilities "
            "contract is canonical in MHRN. CUDA implementation follows in Wave 4."
        ),
    ),
    PromotionCandidate(
        "parity_determinism",
        "Parity / Determinism",
        "INTEGRATED",
        (
            "src/playground/cuda/builder_parity.py",
            "src/playground/cuda/synapses.py",
        ),
        (
            "src/verification/parity/",
            "src/runtime/determinism/",
        ),
        "WAVE4_CUDA_BACKEND",
        notes=(
            "D1/D2/D3 contracts, stable execution fingerprints, Counter-RNG, "
            "same-tick ordering and delay-ring semantics are canonical MHRN "
            "contracts; Playground delegates to them."
        ),
    ),
    PromotionCandidate(
        "cuda_execution",
        "CUDA Execution Backend",
        "INTEGRATED",
        ("src/playground/cuda/",),
        ("src/acceleration/cuda/",),
        "WAVE5_RESIDENT_PAN_AND_ENVIRONMENT",
        notes=(
            "Driver/NVRTC, recurrent reference, technical plasticity kernels and "
            "the bounded replay CUDABackend are canonical MHRN infrastructure. "
            "Plasticity semantics remain NON_CANONICAL_DRAFT; D3/live environment "
            "and PAN hyperstate remain later gates."
        ),
    ),
    PromotionCandidate(
        "learning_synapse",
        "Learning / Synapse Semantics",
        "BLOCKED_CONTRACT_FREEZE",
        ("src/playground/cuda/synapses.py",),
        ("src/learning/",),
        "MHRN_LEARNING_SYNAPSE_CONTRACT",
        notes="CPU and CUDA learning semantics must be frozen before promotion.",
    ),
    PromotionCandidate(
        "closed_loop",
        "Closed Loop / Environment",
        "FE3_LIVE_ADAPTER_IMPLEMENTED_HARDWARE_ACCEPTANCE_PENDING",
        ("src/playground/closed_loop.py", "src/playground/pan/sandbox.py"),
        ("src/experience/", "src/verification/frozen_environment/"),
        "PHYSICAL_FE3_HARDWARE_ACCEPTANCE",
        notes=(
            "The canonical Frozen-Environment contract now has a backend-neutral "
            "live-input adapter and a versioned FE-3 deterministic-target manifest. "
            "CPU/self controls are executable and the physical hardware runner can "
            "compare CPUReferenceBackend with CUDABackend. Physical RTX acceptance "
            "must still be executed before FE-3 is marked accepted."
        ),
    ),
    PromotionCandidate(
        "pan_hyperstate",
        "PAN Hyperstate",
        "SEMANTIC_CONTRACT_DRAFT",
        ("src/playground/pan/",),
        (
            "src/homeostasis/pan_contract.py",
            "src/self_organization/",
        ),
        "PAN_CONTRACT_FREEZE_REVIEW",
        notes=(
            "Wave 5A has extracted the current PAN state surface, coefficients and "
            "update ordering into a backend-neutral draft contract. The Playground "
            "runtime consumes that contract without changing the algorithm. PAN is "
            "not canonical or evidence-eligible until RQ-PAN-SEM-001 is reviewed "
            "and the contract is frozen."
        ),
    ),
    PromotionCandidate(
        "old_frontend_views",
        "OLD Frontend Views",
        "RETAINED_NOT_CORE",
        ("src/dashboard/static/frontend/",),
        (),
        "EXPLICIT_REACTIVATION_ONLY",
        (
            "science-cellmodel",
            "science-snn",
            "science-recurrent",
            "wesen-snn",
            "wesen-recurrent",
            "control-snn",
            "control-recurrent",
        ),
        "OLD remains a compatibility/archive surface and is not promoted by default.",
    ),
)


def integration_catalog() -> dict[str, object]:
    return {
        "classification": "PLAYGROUND_TO_MHRN_INTEGRATION_CATALOG",
        "scientific_evidence": False,
        "runtime_source_mutation": False,
        "dependency_rule": "PLAYGROUND_USES_MHRN_MHRN_DOES_NOT_IMPORT_PLAYGROUND",
        "candidates": [candidate.to_mapping() for candidate in _CANDIDATES],
    }


def transfer_element(payload: Mapping[str, object]) -> dict[str, object]:
    raw_id = payload.get("element_id")
    if not isinstance(raw_id, str) or not raw_id:
        raise ValueError("element_id must be a non-empty string")
    candidate = next((item for item in _CANDIDATES if item.element_id == raw_id), None)
    if candidate is None:
        raise ValueError(f"unknown Playground integration element: {raw_id}")

    detail: dict[str, object]

    if candidate.element_id == "neural_io_contracts":
        from src.embodiment.neural_io_contracts import (
            BoundaryFrame as CanonicalBoundary,
        )
        from src.playground.neural_io.contracts import (
            BoundaryFrame as PlaygroundBoundary,
        )

        connected = CanonicalBoundary is PlaygroundBoundary
        detail = {"same_contract_object": connected}
    elif candidate.element_id == "neural_io_codecs":
        from src.embodiment.neural_io_codecs import encode_input as canonical_encode
        from src.playground.neural_io.codecs import encode_input as playground_encode

        connected = canonical_encode is playground_encode
        detail = {"same_codec_function": connected}
    elif candidate.element_id == "neural_io_adapter":
        from src.embodiment.neural_io_adapter import (
            NeuralIOAreaAdapter,
            neural_io_adapter_contract_check,
        )
        from src.playground.neural_io.adapter import PlaygroundIOAreaAdapter

        connected = (
            issubclass(PlaygroundIOAreaAdapter, NeuralIOAreaAdapter)
            and neural_io_adapter_contract_check()
        )
        detail = {
            "playground_wrapper_subclasses_canonical": issubclass(
                PlaygroundIOAreaAdapter, NeuralIOAreaAdapter
            ),
            "network_area_adapter_contract": neural_io_adapter_contract_check(),
        }
    elif candidate.element_id == "execution_backend":
        from src.runtime.backend import BackendState, ExecutionBackend

        connected = (
            ExecutionBackend.__module__ == "src.runtime.backend"
            and BackendState.__module__ == "src.runtime.backend"
        )
        detail = {
            "protocol_module": ExecutionBackend.__module__,
            "state_module": BackendState.__module__,
            "backend_neutral_state": connected,
        }
    elif candidate.element_id == "parity_determinism":
        from src.playground.cuda.builder_parity import (
            compare_builder_runs as playground_compare,
        )
        from src.playground.cuda.synapses import release_uniform as playground_rng
        from src.runtime.determinism import release_uniform as canonical_rng
        from src.verification.parity import compare_builder_runs as canonical_compare

        connected = (
            playground_compare is canonical_compare and playground_rng is canonical_rng
        )
        detail = {
            "same_parity_function": playground_compare is canonical_compare,
            "same_counter_rng_function": playground_rng is canonical_rng,
        }
    elif candidate.element_id == "cuda_execution":
        from src.acceleration.cuda import CUDABackend, execution_backend_contract_check
        from src.acceleration.cuda.plasticity.contracts import PLASTICITY_SEMANTICS
        from src.acceleration.cuda.recurrent import (
            execute_recurrent as canonical_execute,
        )
        from src.playground.cuda.recurrent import (
            execute_recurrent as playground_execute,
        )

        connected = (
            playground_execute is canonical_execute
            and execution_backend_contract_check()
            and CUDABackend().capabilities().supports_recurrent
        )
        detail = {
            "same_recurrent_execute_function": playground_execute is canonical_execute,
            "execution_backend_contract": execution_backend_contract_check(),
            "execution_mode": CUDABackend().capabilities().execution_mode,
            "plasticity_semantics": PLASTICITY_SEMANTICS,
            "d3_complete": False,
        }
    elif candidate.element_id == "pan_hyperstate":
        from src.homeostasis.pan_contract import (
            PAN_CONTRACT_ID,
            PAN_CONTRACT_STATUS,
            pan_contract_check,
        )

        connected = False
        detail = {
            "pan_contract_id": PAN_CONTRACT_ID,
            "pan_contract_status": PAN_CONTRACT_STATUS,
            "pan_contract_self_check": pan_contract_check(),
        }
    else:
        connected = False
        detail = {}

    if candidate.status == "INTEGRATED":
        return {
            "classification": "PLAYGROUND_TO_MHRN_TRANSFER_VERIFICATION",
            "scientific_evidence": False,
            "element_id": raw_id,
            "status": "INTEGRATED" if connected else "BROKEN_COMPATIBILITY",
            "applied": connected,
            "runtime_source_mutation": False,
            "canonical_target": candidate.target_paths[0],
            "compatibility_source": candidate.source_paths[0],
            "next_gate": candidate.next_gate,
            **detail,
        }

    return {
        "classification": "PLAYGROUND_TO_MHRN_TRANSFER_PLAN",
        "scientific_evidence": False,
        "element_id": raw_id,
        "status": candidate.status,
        "applied": False,
        "runtime_source_mutation": False,
        "source_paths": list(candidate.source_paths),
        "target_paths": list(candidate.target_paths),
        "old_routes": list(candidate.old_routes),
        "next_gate": candidate.next_gate,
        "message": (
            "Promotion requires a repository change and its declared gate; "
            "the dashboard never rewrites source code at runtime."
        ),
        **detail,
    }
