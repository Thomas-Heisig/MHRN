import pytest

from src.research.connectome_embodiment import _simulate


def test_invalid_schedule_is_rejected_before_simulation():
    with pytest.raises(ValueError, match="schedule"):
        _simulate({}, 1, 30, "closed_loop", external_torque_schedule=(0.0,))
    with pytest.raises(ValueError, match="schedule"):
        _simulate({}, 1, 30, "closed_loop", external_torque_schedule=(float("nan"),) * 30)


def test_zero_schedule_preserves_unperturbed_control():
    a = _simulate({}, 2, 40, "closed_loop", perturb=False)
    b = _simulate({}, 2, 40, "closed_loop", external_torque_schedule=(0.0,) * 40)
    assert a.error is b.error is None
    assert a.metrics == b.metrics
    assert a.motor_tape == b.motor_tape
