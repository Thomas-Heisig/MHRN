"""Serialization helpers for the bounded recurrent backend."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, replace

from ..plasticity.reference import SynapseConfig
from .backend import RecurrentInputs, validate_recurrent_inputs


def stable_digest(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def canonical_int(value: object, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer")
    return value


def canonical_float(value: object, *, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be numeric")
    return float(value)


def recurrent_inputs_to_mapping(inputs: RecurrentInputs) -> dict[str, object]:
    result: dict[str, object] = {
        "n_neurons": inputs.n_neurons,
        "ticks": inputs.ticks,
        "offsets": list(inputs.offsets),
        "sources": list(inputs.sources),
        "delays": list(inputs.delays),
        "weights": list(inputs.weights),
        "external": list(inputs.external),
        "voltage": list(inputs.voltage),
        "adaptation": list(inputs.adaptation),
        "model": inputs.model,
        "dt_ms": inputs.dt_ms,
        "rewards": list(inputs.rewards),
    }
    result["synapses"] = (
        asdict(inputs.synapses) if inputs.synapses is not None else None
    )
    return result


def _tuple_int(values: object, *, field: str) -> tuple[int, ...]:
    if not isinstance(values, (list, tuple)):
        raise ValueError(f"{field} must be a list/tuple")
    return tuple(
        canonical_int(value, field=f"{field}[{index}]")
        for index, value in enumerate(values)
    )


def _tuple_float(values: object, *, field: str) -> tuple[float, ...]:
    if not isinstance(values, (list, tuple)):
        raise ValueError(f"{field} must be a list/tuple")
    return tuple(
        canonical_float(value, field=f"{field}[{index}]")
        for index, value in enumerate(values)
    )


def recurrent_inputs_from_mapping(
    config: Mapping[str, object],
    *,
    seed: int,
) -> RecurrentInputs:
    if type(seed) is not int or not 0 <= seed <= 0xFFFFFFFF:
        raise ValueError("seed must be uint32")
    raw_synapses = config.get("synapses")
    synapses: SynapseConfig | None = None
    if raw_synapses is not None:
        if not isinstance(raw_synapses, Mapping):
            raise ValueError("synapses must be a mapping or null")
        supplied_seed = canonical_int(
            raw_synapses.get("seed", seed), field="synapses.seed"
        )
        if supplied_seed != seed:
            raise ValueError("backend seed must match synapse seed")
        synapses = SynapseConfig(
            stdp=bool(raw_synapses.get("stdp", True)),
            stp=bool(raw_synapses.get("stp", True)),
            reward_modulated=bool(raw_synapses.get("reward_modulated", True)),
            seed=seed,
            learning_rate=canonical_float(
                raw_synapses.get("learning_rate", 0.2),
                field="synapses.learning_rate",
            ),
            weight_decay=canonical_float(
                raw_synapses.get("weight_decay", 0.001),
                field="synapses.weight_decay",
            ),
            weight_max=canonical_float(
                raw_synapses.get("weight_max", 20.0),
                field="synapses.weight_max",
            ),
            eligibility_tau=canonical_float(
                raw_synapses.get("eligibility_tau", 100.0),
                field="synapses.eligibility_tau",
            ),
            credit_window=canonical_int(
                raw_synapses.get("credit_window", 64),
                field="synapses.credit_window",
            ),
            td_lambda=canonical_float(
                raw_synapses.get("td_lambda", 0.9),
                field="synapses.td_lambda",
            ),
            gamma=canonical_float(
                raw_synapses.get("gamma", 0.99),
                field="synapses.gamma",
            ),
        )
    try:
        inputs = RecurrentInputs(
            n_neurons=canonical_int(config["n_neurons"], field="n_neurons"),
            ticks=canonical_int(config["ticks"], field="ticks"),
            offsets=_tuple_int(config["offsets"], field="offsets"),
            sources=_tuple_int(config["sources"], field="sources"),
            delays=_tuple_int(config["delays"], field="delays"),
            weights=_tuple_float(config["weights"], field="weights"),
            external=_tuple_float(config["external"], field="external"),
            voltage=_tuple_float(config["voltage"], field="voltage"),
            adaptation=_tuple_float(config["adaptation"], field="adaptation"),
            model=str(config.get("model", "lif")),
            dt_ms=canonical_float(config.get("dt_ms", 1.0), field="dt_ms"),
            synapses=synapses,
            rewards=_tuple_float(config.get("rewards", ()), field="rewards"),
        )
    except KeyError as exc:
        raise ValueError(f"missing recurrent config field: {exc.args[0]}") from exc
    validate_recurrent_inputs(inputs)
    return inputs


def set_external_tick_config(
    config: dict[str, object],
    *,
    tick: int,
    currents: Sequence[float],
) -> None:
    """Replace exactly one external-current row in a canonical replay config."""

    n = canonical_int(config.get("n_neurons"), field="n_neurons")
    ticks = canonical_int(config.get("ticks"), field="ticks")
    if type(tick) is not int or not 0 <= tick < ticks:
        raise ValueError("tick is outside configured replay range")
    if len(currents) != n:
        raise ValueError("external-current row must match n_neurons")
    raw_external = config.get("external")
    if not isinstance(raw_external, (list, tuple)):
        raise ValueError("external must be a list/tuple")
    if len(raw_external) != n * ticks:
        raise ValueError("external has invalid configured shape")
    external = [
        canonical_float(value, field=f"external[{index}]")
        for index, value in enumerate(raw_external)
    ]
    row = [
        canonical_float(value, field=f"currents[{index}]")
        for index, value in enumerate(currents)
    ]
    start = tick * n
    external[start : start + n] = row
    config["external"] = external


def prefix_inputs(inputs: RecurrentInputs, ticks: int) -> RecurrentInputs:
    if not 1 <= ticks <= inputs.ticks:
        raise ValueError("prefix ticks outside configured range")
    n = inputs.n_neurons
    return replace(
        inputs,
        ticks=ticks,
        external=inputs.external[: ticks * n],
        rewards=inputs.rewards[:ticks] if inputs.synapses is not None else (),
    )


def step_payload(
    outputs: Mapping[str, object],
    *,
    tick: int,
    n_neurons: int,
) -> dict[str, object]:
    start, stop = tick * n_neurons, (tick + 1) * n_neurons
    voltage_raw = outputs.get("voltage")
    adaptation_raw = outputs.get("adaptation")
    spikes_raw = outputs.get("spikes")
    if not isinstance(voltage_raw, list):
        raise ValueError("voltage output must be a list")
    if not isinstance(adaptation_raw, list):
        raise ValueError("adaptation output must be a list")
    if not isinstance(spikes_raw, list):
        raise ValueError("spikes output must be a list")
    return {
        "tick": tick,
        "voltage": [
            canonical_float(value, field="voltage output")
            for value in voltage_raw[start:stop]
        ],
        "adaptation": [
            canonical_float(value, field="adaptation output")
            for value in adaptation_raw[start:stop]
        ],
        "spikes": [
            canonical_int(value, field="spike output")
            for value in spikes_raw[start:stop]
        ],
    }
