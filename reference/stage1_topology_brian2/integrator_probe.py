"""Brian2-only one-neuron probe reproducing the canonical MHRN tick semantics."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from brian2 import Network, NeuronGroup, defaultclock, ms, prefs, start_scope


@dataclass(frozen=True)
class ProbeResult:
    v: float
    u: float
    threshold_adaptation: float
    firing_rate_estimate: float
    spiked: bool

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def _build_probe() -> tuple[NeuronGroup, Network]:
    start_scope()
    prefs.codegen.target = "numpy"
    defaultclock.dt = 1 * ms

    group = NeuronGroup(
        1,
        model="""
        v : 1
        u : 1
        input_current : 1
        threshold_adaptation : 1
        firing_rate_estimate : 1
        spike_seen : integer
        """,
        threshold="v >= 30 + threshold_adaptation",
        reset="""
        v = -65
        u = u + 8
        threshold_adaptation = threshold_adaptation + 0.01
        spike_seen = 1
        """,
        dt=1 * ms,
        name="reference_probe",
    )
    group.v = -65.0
    group.u = -13.0
    group.input_current = 0.0
    group.threshold_adaptation = 0.0
    group.firing_rate_estimate = 0.0
    group.spike_seen = 0

    # Reset the per-tick spike flag before each update.
    group.run_regularly(
        "spike_seen = 0",
        dt=1 * ms,
        when="start",
        order=-10,
        name="mhrn_reset_spike_flag",
    )

    # Canonical MHRN membrane update: two half-Euler v updates followed by u Euler.
    group.run_regularly(
        """
        v = v + 0.5 * (0.04*v*v + 5*v + 140 - u + input_current)
        v = v + 0.5 * (0.04*v*v + 5*v + 140 - u + input_current)
        u = u + 0.02 * (0.2*v - u)
        """,
        dt=1 * ms,
        when="groups",
        order=-1,
        name="mhrn_two_half_euler",
    )

    # Canonical MHRN post-spike/post-tick sequence:
    # firing-rate update -> adaptation decay -> homeostasis update/clamp.
    group.run_regularly(
        """
        firing_rate_estimate = exp(-0.001)*firing_rate_estimate + spike_seen*(1-exp(-0.001))*1000
        threshold_adaptation = threshold_adaptation * 0.999
        threshold_adaptation = clip(threshold_adaptation + 0.001*(firing_rate_estimate - 10), -10, 10)
        """,
        dt=1 * ms,
        when="after_resets",
        order=1,
        name="mhrn_post_tick",
    )

    return group, Network(group, *group.contained_objects)


def _snapshot(group: NeuronGroup) -> ProbeResult:
    return ProbeResult(
        v=float(group.v[0]),
        u=float(group.u[0]),
        threshold_adaptation=float(group.threshold_adaptation[0]),
        firing_rate_estimate=float(group.firing_rate_estimate[0]),
        spiked=bool(group.spike_seen[0]),
    )


def run_trajectory(input_currents: list[float]) -> list[ProbeResult]:
    """Run a persistent one-neuron trajectory for the supplied per-tick currents."""

    group, net = _build_probe()
    results: list[ProbeResult] = []
    for current in input_currents:
        group.input_current = float(current)
        net.run(1 * ms)
        results.append(_snapshot(group))
    return results


def run_one_tick(input_current: float) -> ProbeResult:
    """Run exactly one 1-ms tick using explicit MHRN-compatible update ordering."""

    return run_trajectory([float(input_current)])[0]
