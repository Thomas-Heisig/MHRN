"""Core data contracts for the non-canonical MHRN playground."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping, TypeAlias

Coordinate: TypeAlias = tuple[float, ...]
Edge: TypeAlias = tuple[int, int]

_NAME_RE = re.compile(r"[^A-Za-z0-9_.-]+")


@dataclass(frozen=True, slots=True)
class Topology:
    """Neutral topology returned by every playground topology generator."""

    name: str
    dimensions: int
    edges: tuple[Edge, ...]
    coordinates: tuple[Coordinate, ...]
    metadata: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class PlaygroundConfig:
    """Validated bounded configuration for one exploratory playground session."""

    name: str = "playground_session"
    neuron_model: str = "izhikevich_rs"
    synapse_model: str = "static"
    plasticity_rule: str = "none"
    topology: str = "mhrn_5d"
    stimulus: str = "deterministic"
    readout: str = "population_vector"
    n_neurons: int = 128
    edge_budget: int = 512
    ticks: int = 256
    seed: int = 12345
    dimensions: int = 5
    dt_ms: float = 1.0
    weight: float = 8.0
    delay_ticks: int = 1
    stimulus_current: float = 12.0
    stimulus_rate_hz: float = 20.0
    radius: float = 0.35
    k_neighbors: int = 8
    rewiring_probability: float = 0.15
    modules: int = 4
    ensemble_runs: int = 1
    persist: bool = False
    pan_enabled: bool = False
    pan_dimensions: int = 5
    pan_closed_loop: bool = True
    pan_feedback_gain: float = 0.05
    pan_health_decay: float = 0.001
    pan_apoptosis_threshold: float = 0.1
    geometry_lambda_a: float = 0.5
    geometry_lambda_b: float = 0.5
    geometry_sigma: float = 0.1
    geometry_p0: float = 0.3
    geometry_mode: str = "shortcut_union"
    geometry_delay_velocity: float = 0.25

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> "PlaygroundConfig":
        """Build a config from untrusted API/CLI input and validate all bounds."""

        defaults = cls()

        def text(name: str, default: str) -> str:
            value = payload.get(name, default)
            if not isinstance(value, str):
                raise ValueError(f"{name} must be a string")
            value = value.strip()
            if not value:
                raise ValueError(f"{name} must not be empty")
            return value

        def integer(name: str, default: int) -> int:
            value = payload.get(name, default)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be an integer")
            converted = int(value)
            if float(value) != float(converted):
                raise ValueError(f"{name} must be an integer")
            return converted

        def number(name: str, default: float) -> float:
            value = payload.get(name, default)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric")
            return float(value)

        raw_name = text("name", defaults.name)
        safe_name = _NAME_RE.sub("_", raw_name).strip("._-")[:80] or defaults.name
        config = cls(
            name=safe_name,
            neuron_model=text("neuron_model", defaults.neuron_model),
            synapse_model=text("synapse_model", defaults.synapse_model),
            plasticity_rule=text("plasticity_rule", defaults.plasticity_rule),
            topology=text("topology", defaults.topology),
            stimulus=text("stimulus", defaults.stimulus),
            readout=text("readout", defaults.readout),
            n_neurons=integer("n_neurons", defaults.n_neurons),
            edge_budget=integer("edge_budget", defaults.edge_budget),
            ticks=integer("ticks", defaults.ticks),
            seed=integer("seed", defaults.seed),
            dimensions=integer("dimensions", defaults.dimensions),
            dt_ms=number("dt_ms", defaults.dt_ms),
            weight=number("weight", defaults.weight),
            delay_ticks=integer("delay_ticks", defaults.delay_ticks),
            stimulus_current=number("stimulus_current", defaults.stimulus_current),
            stimulus_rate_hz=number("stimulus_rate_hz", defaults.stimulus_rate_hz),
            radius=number("radius", defaults.radius),
            k_neighbors=integer("k_neighbors", defaults.k_neighbors),
            rewiring_probability=number(
                "rewiring_probability", defaults.rewiring_probability
            ),
            modules=integer("modules", defaults.modules),
            ensemble_runs=integer("ensemble_runs", defaults.ensemble_runs),
            persist=bool(payload.get("persist", defaults.persist)),
            pan_enabled=bool(payload.get("pan_enabled", defaults.pan_enabled)),
            pan_dimensions=integer("pan_dimensions", defaults.pan_dimensions),
            pan_closed_loop=bool(
                payload.get("pan_closed_loop", defaults.pan_closed_loop)
            ),
            pan_feedback_gain=number(
                "pan_feedback_gain", defaults.pan_feedback_gain
            ),
            pan_health_decay=number(
                "pan_health_decay", defaults.pan_health_decay
            ),
            pan_apoptosis_threshold=number(
                "pan_apoptosis_threshold", defaults.pan_apoptosis_threshold
            ),
            geometry_lambda_a=number(
                "geometry_lambda_a", defaults.geometry_lambda_a
            ),
            geometry_lambda_b=number(
                "geometry_lambda_b", defaults.geometry_lambda_b
            ),
            geometry_sigma=number("geometry_sigma", defaults.geometry_sigma),
            geometry_p0=number("geometry_p0", defaults.geometry_p0),
            geometry_mode=text("geometry_mode", defaults.geometry_mode),
            geometry_delay_velocity=number(
                "geometry_delay_velocity", defaults.geometry_delay_velocity
            ),
        )
        config.validate()
        return config

    def validate(self) -> None:
        if not 2 <= self.n_neurons <= 1024:
            raise ValueError("n_neurons must be between 2 and 1024")
        max_edges = min(20_000, self.n_neurons * (self.n_neurons - 1))
        if not self.n_neurons <= self.edge_budget <= max_edges:
            raise ValueError(f"edge_budget must be between n_neurons and {max_edges}")
        if not 1 <= self.ticks <= 2048:
            raise ValueError("ticks must be between 1 and 2048")
        if not 1 <= self.dimensions <= 32:
            raise ValueError("dimensions must be between 1 and 32")
        if not 0.05 <= self.dt_ms <= 5.0:
            raise ValueError("dt_ms must be between 0.05 and 5.0")
        if not 0.0 <= self.weight <= 100.0:
            raise ValueError("weight must be between 0 and 100")
        if not 1 <= self.delay_ticks <= 64:
            raise ValueError("delay_ticks must be between 1 and 64")
        if not 0.0 <= self.stimulus_current <= 500.0:
            raise ValueError("stimulus_current must be between 0 and 500")
        if not 0.0 <= self.stimulus_rate_hz <= 1000.0:
            raise ValueError("stimulus_rate_hz must be between 0 and 1000")
        if not 0.001 <= self.radius <= 2.0:
            raise ValueError("radius must be between 0.001 and 2.0")
        if not 1 <= self.k_neighbors <= min(64, self.n_neurons - 1):
            raise ValueError("k_neighbors outside allowed range")
        if not 0.0 <= self.rewiring_probability <= 1.0:
            raise ValueError("rewiring_probability must be between 0 and 1")
        if not 1 <= self.modules <= min(32, self.n_neurons):
            raise ValueError("modules outside allowed range")
        if not 1 <= self.ensemble_runs <= 8:
            raise ValueError("ensemble_runs must be between 1 and 8")
        if not 5 <= self.pan_dimensions <= 32:
            raise ValueError("pan_dimensions must be between 5 and 32")
        if not 0.0 <= self.pan_feedback_gain <= 5.0:
            raise ValueError("pan_feedback_gain must be between 0 and 5")
        if not 0.0 <= self.pan_health_decay <= 1.0:
            raise ValueError("pan_health_decay must be between 0 and 1")
        if not 0.0 <= self.pan_apoptosis_threshold <= 1.0:
            raise ValueError("pan_apoptosis_threshold must be between 0 and 1")
        if not 0.0 <= self.geometry_lambda_a <= 10.0:
            raise ValueError("geometry_lambda_a must be between 0 and 10")
        if not 0.0 <= self.geometry_lambda_b <= 10.0:
            raise ValueError("geometry_lambda_b must be between 0 and 10")
        if not 0.001 <= self.geometry_sigma <= 2.0:
            raise ValueError("geometry_sigma must be between 0.001 and 2")
        if not 0.0 <= self.geometry_p0 <= 1.0:
            raise ValueError("geometry_p0 must be between 0 and 1")
        if self.geometry_mode not in {"mixed_additive", "shortcut_union"}:
            raise ValueError(
                "geometry_mode must be mixed_additive or shortcut_union"
            )
        if not 0.001 <= self.geometry_delay_velocity <= 10.0:
            raise ValueError(
                "geometry_delay_velocity must be between 0.001 and 10"
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "neuron_model": self.neuron_model,
            "synapse_model": self.synapse_model,
            "plasticity_rule": self.plasticity_rule,
            "topology": self.topology,
            "stimulus": self.stimulus,
            "readout": self.readout,
            "n_neurons": self.n_neurons,
            "edge_budget": self.edge_budget,
            "ticks": self.ticks,
            "seed": self.seed,
            "dimensions": self.dimensions,
            "dt_ms": self.dt_ms,
            "weight": self.weight,
            "delay_ticks": self.delay_ticks,
            "stimulus_current": self.stimulus_current,
            "stimulus_rate_hz": self.stimulus_rate_hz,
            "radius": self.radius,
            "k_neighbors": self.k_neighbors,
            "rewiring_probability": self.rewiring_probability,
            "modules": self.modules,
            "ensemble_runs": self.ensemble_runs,
            "persist": self.persist,
            "pan_enabled": self.pan_enabled,
            "pan_dimensions": self.pan_dimensions,
            "pan_closed_loop": self.pan_closed_loop,
            "pan_feedback_gain": self.pan_feedback_gain,
            "pan_health_decay": self.pan_health_decay,
            "pan_apoptosis_threshold": self.pan_apoptosis_threshold,
            "geometry_lambda_a": self.geometry_lambda_a,
            "geometry_lambda_b": self.geometry_lambda_b,
            "geometry_sigma": self.geometry_sigma,
            "geometry_p0": self.geometry_p0,
            "geometry_mode": self.geometry_mode,
            "geometry_delay_velocity": self.geometry_delay_velocity,
        }
