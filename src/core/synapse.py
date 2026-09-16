"""Deterministic synapse primitive with pair-STDP and reward eligibility.

The production learning pipeline lives in :mod:`src.learning.learning_engine` and
keeps its own eligibility state. This primitive therefore remains a standalone,
serializable building block: callers may use pair-STDP directly, accumulate a
signed timing eligibility trace for later reward modulation, or keep both paths
disabled. The two eligibility implementations must not be mixed implicitly.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field, fields
from typing import Any, Callable, cast

A_PLUS: float = 0.1
A_MINUS: float = 0.12
TAU_PLUS: float = 20.0
TAU_MINUS: float = 20.0
W_MIN: float = 0.0
W_MAX: float = 1.0
ELIGIBILITY_DECAY: float = 0.95


@dataclass(frozen=True, slots=True)
class SynapseConfig:
    """Configuration for the standalone synaptic plasticity primitive.

    ``meta_state`` is stored on :class:`Synapse`; lower values bias the
    pair-STDP kernel toward LTP and higher values bias it toward LTD. This is
    an explicit engineering convention, not a biological claim.

    ``enable_triplet`` is a serialization-compatible reserved flag. A triplet
    weight-update rule is not implemented yet, so plasticity operations fail
    fast when the flag is enabled instead of silently behaving like pair-STDP.
    """

    a_plus: float = A_PLUS
    a_minus: float = A_MINUS
    tau_plus: float = TAU_PLUS
    tau_minus: float = TAU_MINUS
    w_min: float = W_MIN
    w_max: float = W_MAX
    eligibility_decay: float = ELIGIBILITY_DECAY
    reward_learning_rate: float = 0.01
    reset_eligibility_after_reward: bool = True
    enable_triplet: bool = False
    enable_metaplasticity: bool = False

    def __post_init__(self) -> None:
        if self.a_plus < 0.0 or self.a_minus < 0.0:
            raise ValueError("STDP amplitudes must be >= 0")
        if self.tau_plus <= 0.0 or self.tau_minus <= 0.0:
            raise ValueError("STDP time constants must be > 0")
        if self.w_min > self.w_max:
            raise ValueError("w_min must be <= w_max")
        if not 0.0 <= self.eligibility_decay <= 1.0:
            raise ValueError("eligibility_decay must be in [0, 1]")
        if self.reward_learning_rate < 0.0:
            raise ValueError("reward_learning_rate must be >= 0")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SynapseConfig":
        names = {item.name for item in fields(cls)}
        return cls(**{key: value for key, value in data.items() if key in names})


@dataclass(slots=True)
class Synapse:
    """One bounded synaptic connection with explicit plasticity state.

    ``eligibility`` is signed: positive values support reward-gated LTP and
    negative values support reward-gated LTD. Direct pair-STDP does not consume
    that trace; reward application may reset it according to the config.
    """

    target_id: int
    weight: float
    delay: int
    eligibility: float = 0.0
    last_pre_spike: int = -1
    last_post_spike: int = -1
    pre_trace: float = 0.0
    post_trace: float = 0.0
    meta_state: float = 0.5
    update_count: int = 0
    created_tick: int = 0
    _config: SynapseConfig | None = field(default=None, repr=False, init=False)
    _enabled: bool = field(default=True, repr=False, init=False)
    _dirty_callback: Callable[[], None] | None = field(
        default=None, repr=False, init=False
    )

    def __post_init__(self) -> None:
        if self.delay < 1:
            raise ValueError(f"Delay must be >= 1, got {self.delay}")
        if not math.isfinite(self.weight):
            raise ValueError("Weight must be finite")
        if self.weight < 0.0:
            raise ValueError("Weight must be non-negative")
        if not math.isfinite(self.eligibility):
            raise ValueError("Eligibility must be finite")
        if not 0.0 <= self.meta_state <= 1.0:
            raise ValueError("meta_state must be in [0, 1]")
        if self._config is None:
            self._config = SynapseConfig()

    def set_dirty_callback(self, callback: Callable[[], None] | None) -> None:
        self._dirty_callback = callback

    def mark_dirty(self) -> None:
        if self._dirty_callback is not None:
            self._dirty_callback()

    @property
    def config(self) -> SynapseConfig:
        if self._config is None:
            self._config = SynapseConfig()
        return self._config

    def _require_supported_stdp_mode(self) -> None:
        if self.config.enable_triplet:
            raise NotImplementedError(
                "Triplet-STDP is reserved but not implemented; "
                "disable enable_triplet or implement an explicit triplet rule"
            )

    def set_config(self, config: SynapseConfig) -> None:
        if not config.w_min <= self.weight <= config.w_max:
            raise ValueError("Current weight is outside the requested config bounds")
        self._config = config
        self.mark_dirty()

    def update_eligibility(self, _tick: int) -> None:
        """Decay signed reward eligibility by one simulation update."""
        if not self._enabled:
            return
        self.eligibility *= self.config.eligibility_decay
        if abs(self.eligibility) < 1e-15:
            self.eligibility = 0.0
        self.mark_dirty()

    def _timing_kernel(self, dt: float) -> float:
        """Return the signed pair-STDP timing kernel before weight soft-bounds."""
        if dt == 0.0 or abs(dt) > 100.0:
            return 0.0
        if dt > 0.0:
            return (
                self.config.a_plus
                * (1.0 - self.meta_state)
                * math.exp(-dt / self.config.tau_plus)
            )
        return (
            -self.config.a_minus
            * self.meta_state
            * math.exp(dt / self.config.tau_minus)
        )

    def record_pre_spike(self, tick: int) -> None:
        """Record a pre-spike and accumulate post-before-pre eligibility."""
        self._require_supported_stdp_mode()
        if self.last_post_spike >= 0 and tick > self.last_post_spike:
            self.eligibility += self._timing_kernel(self.last_post_spike - tick)
        self.last_pre_spike = tick
        self.mark_dirty()

    def record_post_spike(self, tick: int) -> None:
        """Record a post-spike and accumulate pre-before-post eligibility."""
        self._require_supported_stdp_mode()
        if self.last_pre_spike >= 0 and tick > self.last_pre_spike:
            self.eligibility += self._timing_kernel(tick - self.last_pre_spike)
        self.last_post_spike = tick
        self.mark_dirty()

    def decay_traces(self) -> None:
        """Decay stored pre/post traces deterministically.

        Record methods populate these traces only when triplet mode is enabled,
        but restored non-zero traces are also allowed to decay after a mode
        change instead of becoming immortal hidden state.
        """
        tau_pre = self.config.tau_plus
        tau_post = self.config.tau_minus
        old_pre = self.pre_trace
        old_post = self.post_trace
        self.pre_trace *= 1.0 - 1.0 / tau_pre
        self.post_trace *= 1.0 - 1.0 / tau_post
        if self.pre_trace != old_pre or self.post_trace != old_post:
            self.mark_dirty()

    def _weight_scale(self, *, is_ltp: bool) -> float:
        """Return a directional soft-bound scale in ``[0, 1]``."""
        w_min = self.config.w_min
        w_max = self.config.w_max
        width = w_max - w_min
        if width <= 0.0:
            return 0.0
        if is_ltp:
            return max(0.0, min(1.0, (w_max - self.weight) / width))
        return max(0.0, min(1.0, (self.weight - w_min) / width))

    def compute_stdp_update(self, dt: float) -> float:
        """Compute one bounded pair-STDP update for ``dt = post - pre``."""
        self._require_supported_stdp_mode()
        raw = self._timing_kernel(dt)
        if raw == 0.0:
            return 0.0
        return raw * self._weight_scale(is_ltp=raw > 0.0)

    def apply_stdp(self, dt: float) -> float:
        """Apply one direct pair-STDP update without consuming reward eligibility."""
        if not self._enabled:
            return 0.0
        delta = self.compute_stdp_update(dt)
        if delta == 0.0:
            return 0.0
        old_weight = self.weight
        self.weight = max(
            self.config.w_min,
            min(self.config.w_max, self.weight + delta),
        )
        actual = self.weight - old_weight
        if actual != 0.0:
            self.update_count += 1
            if self.config.enable_metaplasticity:
                self._update_meta_state(actual)
            self.mark_dirty()
        return actual

    def _update_meta_state(self, delta: float) -> None:
        """Move metaplasticity toward the opposite future plasticity direction."""
        self.meta_state += 0.01 * (-delta)
        self.meta_state = max(0.0, min(1.0, self.meta_state))

    def compute_reward_update(self, reward: float) -> float:
        """Apply a three-factor reward update using signed eligibility.

        This helper belongs to the standalone primitive only. The production
        ``LearningEngine`` has its own eligibility state and must not mirror its
        trace into this field.
        """
        if not self._enabled or reward == 0.0 or self.eligibility == 0.0:
            return 0.0
        raw = self.config.reward_learning_rate * reward * self.eligibility
        raw *= self._weight_scale(is_ltp=raw > 0.0)
        old_weight = self.weight
        self.weight = max(
            self.config.w_min,
            min(self.config.w_max, self.weight + raw),
        )
        actual = self.weight - old_weight
        if actual != 0.0:
            self.update_count += 1
            if self.config.enable_metaplasticity:
                self._update_meta_state(actual)
            if self.config.reset_eligibility_after_reward:
                self.eligibility = 0.0
            self.mark_dirty()
        return actual

    def enable(self) -> None:
        self._enabled = True
        self.mark_dirty()

    def disable(self) -> None:
        self._enabled = False
        self.mark_dirty()

    @property
    def is_enabled(self) -> bool:
        return self._enabled

    def reset_traces(self) -> None:
        self.eligibility = 0.0
        self.pre_trace = 0.0
        self.post_trace = 0.0
        self.last_pre_spike = -1
        self.last_post_spike = -1
        self.mark_dirty()

    def copy(self) -> "Synapse":
        synapse = Synapse(
            target_id=self.target_id,
            weight=self.weight,
            delay=self.delay,
            eligibility=self.eligibility,
            last_pre_spike=self.last_pre_spike,
            last_post_spike=self.last_post_spike,
            pre_trace=self.pre_trace,
            post_trace=self.post_trace,
            meta_state=self.meta_state,
            update_count=self.update_count,
            created_tick=self.created_tick,
        )
        synapse._config = self.config
        synapse._enabled = self._enabled
        return synapse

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 2,
            "target_id": self.target_id,
            "weight": self.weight,
            "delay": self.delay,
            "eligibility": self.eligibility,
            "last_pre_spike": self.last_pre_spike,
            "last_post_spike": self.last_post_spike,
            "pre_trace": self.pre_trace,
            "post_trace": self.post_trace,
            "meta_state": self.meta_state,
            "update_count": self.update_count,
            "created_tick": self.created_tick,
            "enabled": self._enabled,
            "config": self.config.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Synapse":
        config_data = data.get("config")
        config = (
            SynapseConfig.from_dict(cast(dict[str, Any], config_data))
            if isinstance(config_data, dict)
            else SynapseConfig()
        )
        synapse = cls(
            target_id=int(data["target_id"]),
            weight=float(data["weight"]),
            delay=int(data["delay"]),
            eligibility=float(data.get("eligibility", 0.0)),
            last_pre_spike=int(data.get("last_pre_spike", -1)),
            last_post_spike=int(data.get("last_post_spike", -1)),
            pre_trace=float(data.get("pre_trace", 0.0)),
            post_trace=float(data.get("post_trace", 0.0)),
            meta_state=float(data.get("meta_state", 0.5)),
            update_count=int(data.get("update_count", 0)),
            created_tick=int(data.get("created_tick", 0)),
        )
        synapse.set_config(config)
        synapse._enabled = bool(data.get("enabled", True))
        return synapse

    def __str__(self) -> str:
        return (
            f"Synapse(target={self.target_id}, weight={self.weight:.4f}, "
            f"delay={self.delay}, eligibility={self.eligibility:.4f}, "
            f"updates={self.update_count})"
        )

    def __repr__(self) -> str:
        return self.__str__()


def create_synapse(
    target_id: int,
    weight: float = 0.5,
    delay: int = 1,
    config: SynapseConfig | None = None,
) -> Synapse:
    """Create a bounded synapse using the supplied configuration."""
    selected = config or SynapseConfig()
    synapse = Synapse(
        target_id=target_id,
        weight=max(selected.w_min, min(selected.w_max, weight)),
        delay=max(1, delay),
    )
    synapse.set_config(selected)
    return synapse


def create_random_synapse(
    target_id: int,
    rng: Any,
    weight_range: tuple[float, float] = (0.0, 1.0),
    delay_range: tuple[int, int] = (1, 5),
) -> Synapse:
    """Create a synapse from a caller-owned deterministic RNG."""
    weight = rng.uniform(weight_range[0], weight_range[1])
    delay = rng.randint(delay_range[0], delay_range[1])
    return create_synapse(target_id, weight, delay)


__all__ = [
    "A_MINUS",
    "A_PLUS",
    "ELIGIBILITY_DECAY",
    "TAU_MINUS",
    "TAU_PLUS",
    "W_MAX",
    "W_MIN",
    "Synapse",
    "SynapseConfig",
    "create_random_synapse",
    "create_synapse",
]
