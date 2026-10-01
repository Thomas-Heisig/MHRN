"""Versioned D1/D2/D3 parity contract."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum


class ParityClass(StrEnum):
    D1 = "D1"
    D2 = "D2"
    D3 = "D3"
    D3A = "D3a"
    D3B = "D3b"
    D3C = "D3c"


@dataclass(frozen=True, slots=True)
class ParityContract:
    version: str = "mhrn-parity-v1"
    allowed_spike_mismatches: int = 0
    voltage_max_abs_error: float = 1.0e-4
    weight_max_abs_error: float = 1.0e-4
    spike_count_relative_error: float = 0.005
    success_fraction_abs_error: float = 0.02
    require_non_empty: bool = True

    def to_mapping(self) -> dict[str, object]:
        return {
            "version": self.version,
            "scientific_evidence": False,
            "classes": {
                "D1": {
                    "allowed_spike_mismatches": self.allowed_spike_mismatches,
                    "exact_event_order": True,
                },
                "D2": {
                    "voltage_max_abs_error": self.voltage_max_abs_error,
                    "weight_max_abs_error": self.weight_max_abs_error,
                    "fail_closed_non_finite": True,
                },
                "D3": {
                    "spike_count_relative_error": self.spike_count_relative_error,
                    "success_fraction_abs_error": self.success_fraction_abs_error,
                    "causal_live_parity_requires_D3c": True,
                },
            },
        }


@dataclass(frozen=True, slots=True)
class ParityResult:
    parity_class: ParityClass
    passed: bool
    details: Mapping[str, object] = field(default_factory=dict)
    reference_fingerprint: str = ""
    candidate_fingerprint: str = ""

    def to_mapping(self) -> dict[str, object]:
        return {
            "parity_class": self.parity_class.value,
            "passed": self.passed,
            "scientific_evidence": False,
            "reference_fingerprint": self.reference_fingerprint,
            "candidate_fingerprint": self.candidate_fingerprint,
            **dict(self.details),
        }


def default_parity_contract() -> ParityContract:
    return ParityContract()
