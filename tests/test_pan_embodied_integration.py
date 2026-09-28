"""The Builder must execute the same physical world as live PAN sessions."""

from src.playground import PlaygroundConfig
from src.playground.pan.sandbox import EmbodiedEnvironment, StickFigureSandbox
from src.playground.service import run


def payload(**overrides: object) -> dict[str, object]:
    return {
        "closed_loop_preset": "pan_full_balanced",
        "n_neurons": 32,
        "edge_budget": 64,
        "ticks": 128,
        "behavior_episode_ticks": 8,
        "persist": False,
        "parity_reference_commit": "c99ad712a5ef129ad15fa3ad8eccc614568b7eab",
        "episode_termination_enabled": False,
        **overrides,
    }


def test_shared_environment_preserves_physics_and_time_step() -> None:
    world = StickFigureSandbox()
    env = EmbodiedEnvironment(PlaygroundConfig.from_mapping(payload()))
    for tick in range(80):
        action = tick % 4
        world.apply_action(action)
        expected = world.step(dt=0.001)
        observed = env.advance(action, dt_seconds=0.001)
        assert observed["joints"] == expected["joints"]
        assert observed["receptors"] == expected["receptors"]
    assert env.summary()["ticks"] == 80


def test_builder_executes_actions_in_real_world_and_replays_deterministically() -> None:
    config = payload(freeze_actions=True, frozen_action_sequence=[0] * 16)
    first = run(config)
    again = run(config)
    alternate = run(payload(freeze_actions=True, frozen_action_sequence=[1] * 16))
    assert first["sandbox"] == again["sandbox"]
    assert first["sandbox"]["ticks"] == 128
    assert first["sandbox"]["dt_seconds"] == 0.001
    assert (
        first["sandbox"]["world"]["joints"] != alternate["sandbox"]["world"]["joints"]
    )
    assert first["sandbox"]["frames"][7]["pan_action"] == 0
    assert first["sandbox"]["frames"][6]["pan_action"] is None


def test_posture_credit_and_disabled_sandbox_are_explicit() -> None:
    enabled = run(payload(posture_reward_enabled=True))
    disabled = run(payload(posture_reward_enabled=False))
    absent = run(payload(sandbox_enabled=False))
    assert enabled["sandbox"]["posture_credit_updates"] == 128
    assert enabled["sandbox"]["reward_total"] != 0
    assert disabled["sandbox"]["posture_credit_updates"] == 0
    assert disabled["sandbox"]["reward_total"] == 0
    assert "sandbox" not in absent
    assert enabled["sandbox"]["policy_reward"] == "target_task_only"


def test_episode_reset_is_bounded_and_retains_terminal_frame() -> None:
    env = EmbodiedEnvironment(
        PlaygroundConfig.from_mapping(
            payload(episode_termination_enabled=True, episode_max_ticks=16)
        )
    )
    for _ in range(160):
        env.advance(0, dt_seconds=0.001)
    assert env.terminals == 10
    assert len(env.frames) == 128
    assert env.last_frame["terminal"] == "TIMEOUT"
    assert env.world.joints["hip"].y == 1.0
