"""Brian2 pre-freeze parity checks for the Stage-1 topology reference.

This package is intentionally isolated from MHRN runtime modules. It validates the
frozen translation of the canonical neuron update before any reference DATA runner
is implemented or authorized.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import brian2 as b2

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "audits" / "stage1_reference_preflight_parity.json"


@dataclass
class CanonicalState:
    v: float = -65.0
    u: float = -13.0
    threshold_adaptation: float = 0.0
    firing_rate_estimate: float = 0.0
    spiked: bool = False


def canonical_step(
    state: CanonicalState,
    *,
    input_current: float,
    dt_ms: float = 1.0,
    a: float = 0.02,
    b: float = 0.2,
    c: float = -65.0,
    d: float = 8.0,
    threshold: float = 30.0,
    threshold_adaptation_rate: float = 0.01,
    threshold_adaptation_decay: float = 0.999,
    target_rate_hz: float = 10.0,
    firing_rate_tau_ms: float = 1000.0,
    homeostasis_learning_rate: float = 0.001,
) -> CanonicalState:
    v = float(state.v)
    u = float(state.u)
    adaptation = float(state.threshold_adaptation)

    half_dt = 0.5 * dt_ms
    v += half_dt * (0.04 * v * v + 5.0 * v + 140.0 - u + input_current)
    v += half_dt * (0.04 * v * v + 5.0 * v + 140.0 - u + input_current)
    u += dt_ms * a * (b * v - u)

    spiked = v >= threshold + adaptation
    if spiked:
        v = c
        u = u + d
        adaptation += threshold_adaptation_rate

    alpha = 1.0 - math.exp(-dt_ms / firing_rate_tau_ms)
    instantaneous_rate = 1000.0 / dt_ms if spiked else 0.0
    firing_rate = (
        (1.0 - alpha) * float(state.firing_rate_estimate)
        + alpha * instantaneous_rate
    )
    adaptation += homeostasis_learning_rate * (firing_rate - target_rate_hz)
    adaptation = max(-10.0, min(10.0, adaptation))
    adaptation *= threshold_adaptation_decay

    return CanonicalState(
        v=v,
        u=u,
        threshold_adaptation=adaptation,
        firing_rate_estimate=firing_rate,
        spiked=spiked,
    )


def brian2_step(state: CanonicalState, *, input_current: float) -> CanonicalState:
    b2.start_scope()
    b2.defaultclock.dt = 1.0 * b2.ms

    group = b2.NeuronGroup(
        1,
        """
        v : 1
        u : 1
        I : 1
        threshold_adaptation : 1
        firing_rate_estimate : 1
        spiked_flag : integer
        """,
        threshold="False",
        method="euler",
    )
    group.v = state.v
    group.u = state.u
    group.I = input_current
    group.threshold_adaptation = state.threshold_adaptation
    group.firing_rate_estimate = state.firing_rate_estimate
    group.spiked_flag = 0

    # Manual discrete state transition reproducing the frozen MHRN update order.
    group.run_regularly(
        """
        v = v + 0.5*(0.04*v*v + 5*v + 140 - u + I)
        v = v + 0.5*(0.04*v*v + 5*v + 140 - u + I)
        u = u + 0.02*(0.2*v - u)
        spiked_flag = int(v >= 30 + threshold_adaptation)
        u = u + spiked_flag*8
        v = (1-spiked_flag)*v + spiked_flag*(-65)
        threshold_adaptation = threshold_adaptation + spiked_flag*0.01
        firing_rate_estimate = (1-(1-exp(-1.0/1000.0)))*firing_rate_estimate + (1-exp(-1.0/1000.0))*spiked_flag*1000
        threshold_adaptation = threshold_adaptation + 0.001*(firing_rate_estimate - 10)
        threshold_adaptation = clip(threshold_adaptation, -10, 10)
        threshold_adaptation = threshold_adaptation*0.999
        """,
        dt=1.0 * b2.ms,
        when="groups",
        order=0,
    )
    network = b2.Network(group)
    network.run(1.0 * b2.ms)

    return CanonicalState(
        v=float(group.v[0]),
        u=float(group.u[0]),
        threshold_adaptation=float(group.threshold_adaptation[0]),
        firing_rate_estimate=float(group.firing_rate_estimate[0]),
        spiked=bool(int(group.spiked_flag[0])),
    )


def assert_close(left: CanonicalState, right: CanonicalState, *, atol: float) -> None:
    for field in ("v", "u", "threshold_adaptation", "firing_rate_estimate"):
        a = float(getattr(left, field))
        b = float(getattr(right, field))
        if not math.isclose(a, b, rel_tol=0.0, abs_tol=atol):
            raise AssertionError(f"{field}: canonical={a} brian2={b} atol={atol}")
    if left.spiked != right.spiked:
        raise AssertionError(
            f"spike mismatch: canonical={left.spiked} brian2={right.spiked}"
        )


def main() -> int:
    subthreshold_currents = [0.0, 5.0, 10.0, 20.0]
    single_tick: list[dict[str, float | bool]] = []
    for current in subthreshold_currents:
        canonical = canonical_step(CanonicalState(), input_current=current)
        brian = brian2_step(CanonicalState(), input_current=current)
        assert_close(canonical, brian, atol=1e-12)
        single_tick.append(
            {
                "input_current": current,
                "v": canonical.v,
                "u": canonical.u,
                "threshold_adaptation": canonical.threshold_adaptation,
                "firing_rate_estimate": canonical.firing_rate_estimate,
                "spiked": canonical.spiked,
            }
        )

    # Multi-tick trajectory includes at least one spike and exercises adaptation
    # plus the low-pass homeostasis term.
    canonical_state = CanonicalState()
    brian_state = CanonicalState()
    trajectory: list[dict[str, float | bool | int]] = []
    inputs = [100.0] + [0.0] * 11
    saw_spike = False
    for tick, current in enumerate(inputs):
        canonical_state = canonical_step(canonical_state, input_current=current)
        brian_state = brian2_step(brian_state, input_current=current)
        assert_close(canonical_state, brian_state, atol=1e-12)
        saw_spike = saw_spike or canonical_state.spiked
        trajectory.append(
            {
                "tick": tick,
                "input_current": current,
                "v": canonical_state.v,
                "u": canonical_state.u,
                "threshold_adaptation": canonical_state.threshold_adaptation,
                "firing_rate_estimate": canonical_state.firing_rate_estimate,
                "spiked": canonical_state.spiked,
            }
        )
    if not saw_spike:
        raise AssertionError("multi-tick preflight did not exercise a spike")

    payload = {
        "schema_version": 1,
        "status": "PASS",
        "framework": "Brian2",
        "framework_version": b2.__version__,
        "single_tick_absolute_tolerance": 1e-12,
        "single_tick_cases": single_tick,
        "multi_tick_cases": trajectory,
        "mhrn_runtime_imported": False,
        "purpose": "pre-freeze translation parity only; not scientific DATA or EVID",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
