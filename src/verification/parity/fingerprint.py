"""Stable execution fingerprints independent of wall-clock and dict order."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping


def _canonical_bytes(value: object) -> bytes:
    try:
        encoded = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "fingerprint input must be canonical JSON-serializable"
        ) from exc
    return encoded.encode("utf-8")


def config_fingerprint(config: Mapping[str, object]) -> str:
    return hashlib.sha256(_canonical_bytes(dict(config))).hexdigest()


def execution_fingerprint(
    *,
    seed: int,
    config_hash: str,
    backend_name: str,
    backend_version: str,
    ticks: int,
    contract_version: str = "mhrn-parity-v1",
) -> str:
    if type(seed) is not int or seed < 0:
        raise ValueError("seed must be a non-negative int")
    if type(ticks) is not int or ticks < 1:
        raise ValueError("ticks must be a positive int")
    for name, value in (
        ("config_hash", config_hash),
        ("backend_name", backend_name),
        ("backend_version", backend_version),
        ("contract_version", contract_version),
    ):
        if not value:
            raise ValueError(f"{name} must not be empty")
    payload = {
        "backend_name": backend_name,
        "backend_version": backend_version,
        "config_hash": config_hash,
        "contract_version": contract_version,
        "seed": seed,
        "ticks": ticks,
    }
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()
