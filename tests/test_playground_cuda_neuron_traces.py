"""Resident trace phase ordering and exact CPU continuation."""

from __future__ import annotations

import ctypes
import os
import random

import pytest

from src.playground.cuda.membrane import cuda_membrane_session
from src.playground.cuda.neuron_traces import DeviceNeuronTraces
from src.playground.cuda.runtime import CudaDriverError, DeviceAllocation, DriverModule
from src.playground.pan.runtime import PANRuntime
from src.playground.registry.neuron_models import get_neuron_model


def test_trace_validation_and_partial_allocation_cleanup():
    class Driver:
        def __init__(self, fail=False):
            self.allocated, self.freed, self.copies = [], [], []
            self.fail = fail

        def kernel(self, loaded, name):
            return loaded

        def alloc_device(self, size):
            if self.fail and len(self.allocated) == 2:
                raise CudaDriverError("allocation")
            value = DeviceAllocation(len(self.allocated) + 1, size)
            self.allocated.append(value)
            return value

        def free_device(self, value):
            self.freed.append(value)

        def copy_host_to_device(self, allocation, values):
            self.copies.append(allocation.ptr)

        def copy_device_to_host(self, *args):
            pass

        def launch_kernel(self, *args, **kwargs):
            pass

        def synchronize(self):
            pass

    loaded = DriverModule(ctypes.c_void_p(1), ctypes.c_void_p(2), ctypes.c_void_p(3), 0)
    failing = Driver(True)
    with pytest.raises(CudaDriverError):
        DeviceNeuronTraces(failing, loaded, 2)
    assert failing.freed == list(reversed(failing.allocated))
    driver = Driver()
    traces = DeviceNeuronTraces(driver, loaded, 2)
    try:
        for tick in (True, -1, 1, 2**32, 0.5):
            with pytest.raises(ValueError, match="phase"):
                traces.begin(tick)
        with pytest.raises(ValueError, match="phase"):
            traces.commit(0, [])
        traces.begin(0)
        with pytest.raises(ValueError, match="phase"):
            traces.begin(0)
        for spikes in ([True], [-1], [2], [0, 0], [0.5]):
            with pytest.raises(ValueError):
                traces.commit(0, spikes)
        assert len(driver.copies) == 3
        traces.commit(0, [])
        assert traces.completed_ticks == 1
        with pytest.raises(ValueError, match="phase"):
            traces.commit(0, [])
    finally:
        traces.close()
    assert driver.freed == list(reversed(driver.allocated))


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1", reason="opt-in physical CUDA test"
)
def test_device_owned_trace_order_and_history(tmp_path, monkeypatch):
    monkeypatch.setenv("TMP", str(tmp_path))
    n = 129
    runtime = PANRuntime(
        n_neurons=n,
        dimensions=5,
        seed=42,
        feedback_gain=0.1,
        health_decay=0.0,
        apoptosis_threshold=0.1,
        closed_loop=True,
        coordinates=[[0.0]] * n,
        degree=[1] * n,
    )
    model = get_neuron_model("pan_adex_5d")
    cpu = [0.0] * n
    last = [-10_000_000] * n
    rng = random.Random(42)
    with cuda_membrane_session(
        model.name, [model.parameters] * n, 1.0, pan_runtime=runtime
    ) as stepper:
        traces = stepper.neuron_traces
        copied = []
        original_copy = stepper.driver.copy_host_to_device

        def record_copy(allocation, values, **kwargs):
            copied.append(allocation.ptr)
            return original_copy(allocation, values, **kwargs)

        monkeypatch.setattr(stepper.driver, "copy_host_to_device", record_copy)
        for tick in range(150):
            spikes = [i for i in range(n) if rng.random() < 0.3]
            cpu = [x * 0.95 for x in cpu]
            assert traces.begin(tick) == (cpu, cpu, last)
            for i in spikes:
                cpu[i] += 1.0
                last[i] = tick
            assert traces.commit(tick, spikes) == (cpu, cpu, last)
        assert traces.completed_ticks == 150
        assert copied == [traces.device["spikes"].ptr] * 150
