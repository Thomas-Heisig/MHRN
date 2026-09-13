"""Tool for the research chat to update the active YAML configuration file.

This module provides a bounded, auditable mechanism for the research AI to
modify configuration values in the active config file (poc_alpha5_live.yaml).
All changes are validated, logged, and require explicit AI tool invocation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import yaml

# ── Allow-list of config keys the AI may modify ──────────────────────────
#
# Each entry maps a dot-separated config path to a short description.
# Only keys listed here can be changed via the research chat.
ALLOWED_CONFIG_KEYS: dict[str, str] = {
    "initial_neurons": "Number of neurons to create at startup",
    "max_neurons": "Maximum neurons allowed (neurogenesis cap)",
    "dimensions": "5D grid dimensions as list of 5 ints, e.g. [10,10,10,10,10]",
    "seed": "Random seed for deterministic reproducibility",
    "simulation.ticks": "Number of simulation ticks to run (0 = unlimited)",
    "simulation.dt_ms": "Simulation timestep in milliseconds",
    "neuron.a": "Neuron model parameter a (membrane recovery rate)",
    "neuron.b": "Neuron model parameter b (spike sensitivity)",
    "neuron.c": "Neuron model parameter c (reset potential)",
    "neuron.d": "Neuron model parameter d (recovery reset)",
    "network.initial_connections_per_neuron": "Initial synaptic connections per neuron",
    "network.neighbour_radius": "Neighbourhood radius for connection formation",
    "network.weight_min": "Minimum synaptic weight",
    "network.weight_max": "Maximum synaptic weight",
    "homeostasis.enabled": "Enable/disable homeostasis regulation",
    "homeostasis.target_rate_hz": "Target firing rate for homeostasis",
    "stdp.enabled": "Enable/disable STDP learning",
    "eligibility.enabled": "Enable/disable eligibility traces",
    "reward.enabled": "Enable/disable reward-modulated learning",
    "self_organization.enabled": "Enable/disable structural self-organization",
    "self_organization.pruning_enabled": "Enable/disable synapse pruning",
    "self_organization.pruning_weight_threshold": "Weight below which synapses are pruned",
    "state_mode": "Runtime state mode (operator or research)",
    "observability": "Observability intensity (minimal, normal, full)",
    "topology.input.dimension": "Input coordinate dimension",
    "topology.input.coordinate": "Input coordinate value",
    "topology.output.dimension": "Output coordinate dimension",
    "topology.output.coordinate": "Output coordinate value",
    "energy.initial": "Initial energy level per neuron",
    "energy.spike_cost": "Energy cost per spike",
    "simulation.max_delay": "Maximum synaptic delay in ticks",
    "research_chat.temperature": "LLM temperature for research chat",
    "research_chat.max_tokens": "Maximum tokens for LLM responses",
    "research_chat.max_context_chars": "Maximum context characters for LLM",
    "research_chat.web_search_enabled": "Enable web search in research chat",
    "research_chat.vision_enabled": "Enable vision in research chat",
    "research_chat.tools_enabled": "Enable tool calling in research chat",
}

# ── Validation rules ─────────────────────────────────────────────────────

Validator = Callable[[Any], bool]

_VALIDATORS: dict[str, Validator] = {
    "initial_neurons": lambda v: isinstance(v, int) and 1 <= v <= 10_000_000,
    "max_neurons": lambda v: isinstance(v, int) and 1 <= v <= 10_000_000,
    "dimensions": lambda v: (
        isinstance(v, list)
        and len(v) == 5
        and all(isinstance(d, int) and 1 <= d <= 100 for d in v)
    ),
    "seed": lambda v: isinstance(v, int) and 0 <= v <= 2**31 - 1,
    "simulation.ticks": lambda v: isinstance(v, int) and 0 <= v <= 10_000_000,
    "simulation.dt_ms": lambda v: isinstance(v, (int, float)) and 0.1 <= v <= 100.0,
    "simulation.max_delay": lambda v: isinstance(v, int) and 1 <= v <= 1000,
    "network.initial_connections_per_neuron": lambda v: isinstance(v, int)
    and 0 <= v <= 1000,
    "network.neighbour_radius": lambda v: isinstance(v, (int, float))
    and 0.1 <= v <= 100.0,
    "network.weight_min": lambda v: isinstance(v, (int, float)) and 0.0 <= v <= 10.0,
    "network.weight_max": lambda v: isinstance(v, (int, float)) and 0.0 <= v <= 10.0,
    "homeostasis.target_rate_hz": lambda v: isinstance(v, (int, float))
    and 0.1 <= v <= 1000.0,
    "self_organization.pruning_weight_threshold": lambda v: isinstance(v, (int, float))
    and 0.0 <= v <= 1.0,
    "energy.initial": lambda v: isinstance(v, (int, float)) and 0.0 <= v <= 10.0,
    "energy.spike_cost": lambda v: isinstance(v, (int, float)) and 0.0 <= v <= 1.0,
    "research_chat.temperature": lambda v: isinstance(v, (int, float))
    and 0.0 <= v <= 2.0,
    "research_chat.max_tokens": lambda v: isinstance(v, int) and 64 <= v <= 32_768,
    "research_chat.max_context_chars": lambda v: isinstance(v, int)
    and 4_000 <= v <= 120_000,
}

_BOOL_KEYS = {
    "homeostasis.enabled",
    "stdp.enabled",
    "eligibility.enabled",
    "reward.enabled",
    "self_organization.enabled",
    "self_organization.pruning_enabled",
    "research_chat.web_search_enabled",
    "research_chat.vision_enabled",
    "research_chat.tools_enabled",
}


def validate_config_change(key: str, value: Any) -> str | None:
    """Validate a proposed config change. Returns None if valid, error string otherwise."""
    if key not in ALLOWED_CONFIG_KEYS:
        return f"Key '{key}' is not in the allowed config keys list."
    if key in _BOOL_KEYS:
        if not isinstance(value, bool):
            return f"Key '{key}' requires a boolean value (true/false)."
        return None
    validator = _VALIDATORS.get(key)
    if validator is not None and not validator(value):
        return (
            f"Value {value!r} is invalid for key '{key}'. "
            f"Description: {ALLOWED_CONFIG_KEYS[key]}"
        )
    return None


def apply_config_change(config_path: Path, key: str, value: Any) -> tuple[bool, str]:
    """Apply a validated config change to the YAML file.

    Returns (success, message).
    """
    error = validate_config_change(key, value)
    if error is not None:
        return False, error

    try:
        with open(config_path, encoding="utf-8") as f:
            config: dict[str, Any] = yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError) as exc:
        return False, f"Failed to read config: {exc}"

    parts = key.split(".")
    current = config
    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]
    old_value = current.get(parts[-1], "<not set>")
    current[parts[-1]] = value

    # Write back — preserve flow style for lists
    try:
        class _FlowListDumper(yaml.SafeDumper):
            """Dumper that preserves flow style for list values."""
            pass

        _FlowListDumper.add_representer(
            list,
            lambda dumper, data: dumper.represent_sequence(
                "tag:yaml.org,2002:seq", data, flow_style=True
            ),
        )

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(
                config, f,
                Dumper=_FlowListDumper,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )
    except (OSError, yaml.YAMLError) as exc:
        return False, f"Failed to write config: {exc}"

    return True, (
        f"Updated '{key}' from {old_value!r} to {value!r} in {config_path.name}. "
        f"This change will take effect after a restart."
    )


def get_config_value(config_path: Path, key: str) -> tuple[bool, Any]:
    """Read a config value. Returns (found, value)."""
    try:
        with open(config_path, encoding="utf-8") as f:
            config: dict[str, Any] = yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError):
        return False, None
    parts = key.split(".")
    current = config
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current


# ── Ollama-compatible tool definition ────────────────────────────────────


def tool_definition() -> list[dict[str, object]]:
    """Return the Ollama-compatible tool definition for config management."""
    return [
        {
            "type": "function",
            "function": {
                "name": "update_config",
                "description": (
                    "Update a configuration value in the active MHRN config file "
                    "(poc_alpha5_live.yaml). Use this to change simulation parameters "
                    "such as neuron count, grid dimensions, learning settings, etc. "
                    "The change takes effect after a restart. Only pre-approved keys "
                    "can be modified."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "type": "string",
                            "description": (
                                "Dot-separated config key path. "
                                f"Allowed keys: {', '.join(sorted(ALLOWED_CONFIG_KEYS.keys()))}"
                            ),
                        },
                        "value": {
                            "type": ["number", "string", "boolean", "array"],
                            "description": "The new value for the config key.",
                        },
                    },
                    "required": ["key", "value"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_config",
                "description": (
                    "Read a configuration value from the active MHRN config file "
                    "(poc_alpha5_live.yaml). Use this to check current settings "
                    "before suggesting changes."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "type": "string",
                            "description": "Dot-separated config key path to read.",
                        },
                    },
                    "required": ["key"],
                },
            },
        },
    ]


# ── Tool execution ───────────────────────────────────────────────────────


def execute_tool(
    config_path: Path,
    tool_name: str,
    arguments: dict[str, Any],
) -> str:
    """Execute a tool call and return the result as a string for the LLM."""
    if tool_name == "update_config":
        key = arguments.get("key", "")
        value = arguments.get("value")
        _success, message = apply_config_change(config_path, key, value)
        return message
    if tool_name == "read_config":
        key = arguments.get("key", "")
        found, value = get_config_value(config_path, key)
        if found:
            return f"Current value of '{key}': {value!r}"
        return f"Key '{key}' not found in config."
    return f"Unknown tool: {tool_name}"
