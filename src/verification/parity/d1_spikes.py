"""D1 exact spike/event parity."""

from __future__ import annotations

from collections.abc import Sequence

from .contract import ParityClass, ParityResult


def exact_spike_parity(
    reference: Sequence[object],
    candidate: Sequence[object],
    *,
    require_non_empty: bool = True,
) -> ParityResult:
    mismatches = sum(
        1
        for index in range(max(len(reference), len(candidate)))
        if (reference[index] if index < len(reference) else None)
        != (candidate[index] if index < len(candidate) else None)
    )
    empty = not reference and not candidate
    return ParityResult(
        ParityClass.D1,
        passed=(not require_non_empty or not empty) and mismatches == 0,
        details={
            "allowed_spike_mismatches": 0,
            "spike_mismatches": mismatches,
            "empty_evidence": empty,
        },
    )
