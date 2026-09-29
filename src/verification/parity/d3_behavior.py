"""D3 behavioral and causal trajectory parity."""

from __future__ import annotations

from collections.abc import Sequence

from .contract import ParityClass, ParityResult


def exact_behavior_parity(
    *,
    reference_actions: Sequence[object],
    candidate_actions: Sequence[object],
    reference_targets: Sequence[object],
    candidate_targets: Sequence[object],
    reference_rewards: Sequence[object],
    candidate_rewards: Sequence[object],
    reference_body_digest: object | None = None,
    candidate_body_digest: object | None = None,
) -> ParityResult:
    actions_exact = list(reference_actions) == list(candidate_actions)
    targets_exact = list(reference_targets) == list(candidate_targets)
    rewards_exact = list(reference_rewards) == list(candidate_rewards)
    body_compared = (
        reference_body_digest is not None or candidate_body_digest is not None
    )
    body_exact = (
        reference_body_digest == candidate_body_digest if body_compared else True
    )
    non_empty = bool(reference_actions) and bool(candidate_actions)
    return ParityResult(
        ParityClass.D3C if body_compared else ParityClass.D3,
        passed=non_empty
        and actions_exact
        and targets_exact
        and rewards_exact
        and body_exact,
        details={
            "actions_exact": actions_exact,
            "targets_exact": targets_exact,
            "rewards_exact": rewards_exact,
            "body_compared": body_compared,
            "body_exact": body_exact,
            "empty_evidence": not non_empty,
        },
    )


def metric_behavior_parity(
    *,
    reference_spike_count: int,
    candidate_spike_count: int,
    reference_success_fraction: float,
    candidate_success_fraction: float,
    spike_limit: float = 0.005,
    success_limit: float = 0.02,
) -> ParityResult:
    denominator = max(abs(reference_spike_count), 1)
    spike_error = abs(candidate_spike_count - reference_spike_count) / denominator
    success_error = abs(candidate_success_fraction - reference_success_fraction)
    return ParityResult(
        ParityClass.D3,
        passed=(
            spike_error <= spike_limit + 1.0e-12
            and success_error <= success_limit + 1.0e-12
        ),
        details={
            "spike_count_relative_error": spike_error,
            "spike_count_relative_error_limit": spike_limit,
            "success_fraction_abs_error": success_error,
            "success_fraction_abs_error_limit": success_limit,
        },
    )
