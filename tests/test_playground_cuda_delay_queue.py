"""Resident delay queue semantics and restoration are independent of weight updates."""

from __future__ import annotations

import ctypes
import os
from copy import deepcopy

import pytest

from src.playground.cuda.delay_queue import DeviceDelayQueue
from src.playground.cuda.membrane import cuda_membrane_session
from src.playground.cuda.runtime import CudaDriverError, DeviceAllocation, DriverModule
from src.playground.pan.runtime import PANRuntime
from src.playground.registry.neuron_models import get_neuron_model


class FakeDriver:
    def __init__(self, fail=False):
        self.allocations = []
        self.freed = []
        self.copies = 0
        self.fail = fail

    def kernel(self, loaded, name):
        return loaded

    def alloc_device(self, size):
        if self.fail and len(self.allocations) == 3:
            raise CudaDriverError("allocation")
        x = DeviceAllocation(len(self.allocations) + 1, size)
        self.allocations.append(x)
        return x

    def free_device(self, x):
        self.freed.append(x)

    def copy_host_to_device(self, *args, **kwargs):
        self.copies += 1


def test_queue_validation_precedes_transfer_and_partial_allocation_cleans():
    loaded = DriverModule(ctypes.c_void_p(1), ctypes.c_void_p(2), ctypes.c_void_p(3), 0)
    failing = FakeDriver(True)
    with pytest.raises(CudaDriverError):
        DeviceDelayQueue(failing, loaded, 2, 4)
    assert failing.freed == list(reversed(failing.allocations))
    driver = FakeDriver()
    queue = DeviceDelayQueue(driver, loaded, 2, 4)
    try:
        for events in (
            [(True, 1, 1.0)],
            [(0, 0, 1.0)],
            [(0, 65, 1.0)],
            [(2, 1, 1.0)],
            [(0, 1, float("nan"))],
            [(0, 1, True)],
        ):
            with pytest.raises(ValueError):
                queue.enqueue(0, events)
        for tick in (True, -1, 2**32, 1.5):
            with pytest.raises(ValueError):
                queue.consume(tick)
        rows = [[0.0, 0.0] for _ in range(65)]
        for value in (float("inf"), True, "1"):
            bad = deepcopy(rows)
            bad[0][0] = value
            with pytest.raises(ValueError):
                queue.restore(bad)
        with pytest.raises(ValueError):
            queue.restore(rows[:-1])
        assert driver.copies == 1
    finally:
        queue.close()
    assert driver.freed == list(reversed(driver.allocations))


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
def test_resident_queue_wrap_order_restore_and_overflow(tmp_path, monkeypatch):
    monkeypatch.setenv("TMP", str(tmp_path))
    pan = PANRuntime(
        n_neurons=129,
        dimensions=5,
        seed=42,
        feedback_gain=0.1,
        health_decay=0.001,
        apoptosis_threshold=0.1,
        closed_loop=True,
        coordinates=[[0.0]] * 129,
        degree=[1] * 129,
    )
    model = get_neuron_model("pan_adex_5d")
    expected = [[0.0] * 129 for _ in range(65)]
    with cuda_membrane_session(
        model.name, [model.parameters] * 129, 1.0, pan_runtime=pan
    ) as stepper:
        queue = stepper.delay_queue
        for tick in range(150):
            assert queue.consume(tick) == expected[tick % 65]
            expected[tick % 65] = [0.0] * 129
            events = [
                (tick % 129, 64, 2.0),
                (tick % 129, 64, -0.7),
                (128, 1, 0.2 + tick / 100),
                (128, 2, -0.15),
            ]
            queue.enqueue(tick, events)
            for target, delay, amplitude in events:
                expected[(tick + delay) % 65][target] += amplitude
            if tick % 17 == 0:
                assert queue.snapshot() == expected
            if tick == 37:
                snapshot = queue.snapshot()
                queue.restore([[0.0] * 129 for _ in range(65)])
                queue.restore(snapshot)
        assert queue.snapshot() == expected
        queue.restore([[0.0] * 129 for _ in range(65)])
        queue.enqueue(2**32 - 1, [(128, 64, 3.0)])
        assert queue.snapshot()[(2**32 - 1 + 64) % 65][128] == 3.0
        queue.restore([[0.0] * 129 for _ in range(65)])
        with pytest.raises(ValueError, match="non-finite"):
            queue.enqueue(0, [(0, 1, 1e308), (0, 1, 1e308)])


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
def test_resident_queue_preserves_builder_execution_transition(tmp_path, monkeypatch):
    from src.playground.builder.session import PlaygroundSession
    from src.playground.cuda.builder_parity import compare_builder_runs
    from src.playground.models import PlaygroundConfig

    monkeypatch.setenv("TMP", str(tmp_path))
    options = {
        "closed_loop_preset": "pan_full_balanced",
        "n_neurons": 32,
        "edge_budget": 64,
        "ticks": 128,
        "persist": False,
        "execution_mode": "HYBRID_AUTO",
        "execution_initial_mode": "EVENT_ONLY",
        "execution_theta_high": 0.01,
        "execution_theta_low": 0.0,
        "execution_hysteresis": 0.0,
        "execution_min_dwell": 1,
    }
    runs = [
        PlaygroundSession(
            PlaygroundConfig.from_mapping({**options, "neuron_backend": backend}),
            capture_research_state=True,
        ).run()
        for backend in ("cpu", "cuda_pan")
    ]
    assert compare_builder_runs(*runs)["passed"]
    transitions = [run["execution"]["transitions"] for run in runs]
    assert transitions[0] and transitions[1]
    assert [(x["tick"], x["from"], x["to"]) for x in transitions[0]] == [
        (x["tick"], x["from"], x["to"]) for x in transitions[1]
    ]
    for entries in transitions:
        assert all(x["shared_state_integrity"] == "PASS" for x in entries)
