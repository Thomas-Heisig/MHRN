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
        "cuda_execution",
        "CUDA Execution Infrastructure",
        "READY_AFTER_BACKEND_CONTRACT",
        ("src/playground/cuda/",),
        ("src/acceleration/cuda/",),
        "EXECUTION_BACKEND_CONTRACT",
        notes="Driver/NVRTC/ABI/parity are candidates; PAN semantics remain separate.",
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
        "BLOCKED_FROZEN_ENVIRONMENT",
        ("src/playground/closed_loop.py", "src/playground/pan/sandbox.py"),
        ("src/experience/", "src/embodiment/"),
        "MHRN_FROZEN_ENVIRONMENT_CONTRACT",
        notes="Promote boundary/world contracts before Playground-specific body implementations.",
    ),
    PromotionCandidate(
        "pan_hyperstate",
        "PAN Hyperstate",
        "BLOCKED_PAN_SEMANTICS",
        ("src/playground/pan/",),
        ("src/homeostasis/", "src/self_organization/"),
        "RQ-PAN-SEM-001",
        notes="Health/Energy/Apoptosis/Growth require a frozen state/update contract first.",
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
    }
