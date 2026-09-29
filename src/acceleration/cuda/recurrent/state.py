"""Serialization helpers for the bounded recurrent backend."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
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
    result["synapses"] = asdict(inputs.synapses) if inputs.synapses is not None else None
    return result


def _tuple_int(values: object, *, field: str) -> tuple[int, ...]:
    if not isinstance(values, (list, tuple)):
        raise ValueError(f"{field} must be a list/tuple")
    return tuple(int(value) for value in values)


def _tuple_float(values: object, *, field: str) -> tuple[float, ...]:
    if not isinstance(values, (list, tuple)):
        raise ValueError(f"{field} must be a list/tuple")
    return tuple(float(value) for value in values)


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
        supplied_seed = raw_synapses.get("seed", seed)
        if int(supplied_seed) != seed:
            raise ValueError("backend seed must match synapse seed")
        synapses = SynapseConfig(
            stdp=bool(raw_synapses.get("stdp", True)),
            stp=bool(raw_synapses.get("stp", True)),
            reward_modulated=bool(raw_synapses.get("reward_modulated", True)),
            seed=seed,
            learning_rate=float(raw_synapses.get("learning_rate", 0.2)),
            weight_decay=float(raw_synapses.get("weight_decay", 0.001)),
            weight_max=float(raw_synapses.get("weight_max", 20.0)),
            eligibility_tau=float(raw_synapses.get("eligibility_tau", 100.0)),
            credit_window=int(raw_synapses.get("credit_window", 64)),
            td_lambda=float(raw_synapses.get("td_lambda", 0.9)),
            gamma=float(raw_synapses.get("gamma", 0.99)),
        )
    try:
        inputs = RecurrentInputs(
            n_neurons=int(config["n_neurons"]),
            ticks=int(config["ticks"]),
            offsets=_tuple_int(config["offsets"], field="offsets"),
            sources=_tuple_int(config["sources"], field="sources"),
            delays=_tuple_int(config["delays"], field="delays"),
            weights=_tuple_float(config["weights"], field="weights"),
            external=_tuple_float(config["external"], field="external"),
            voltage=_tuple_float(config["voltage"], field="voltage"),
            adaptation=_tuple_float(config["adaptation"], field="adaptation"),
            model=str(config.get("model", "lif")),
            dt_ms=float(config.get("dt_ms", 1.0)),
            synapses=synapses,
            rewards=_tuple_float(config.get("rewards", ()), field="rewards"),
        )
    except KeyError as exc:
        raise ValueError(f"missing recurrent config field: {exc.args[0]}") from exc
    validate_recurrent_inputs(inputs)
    return inputs


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
        "voltage": [float(value) for value in voltage_raw[start:stop]],
        "adaptation": [float(value) for value in adaptation_raw[start:stop]],
        "spikes": [int(value) for value in spikes_raw[start:stop]],
    }
