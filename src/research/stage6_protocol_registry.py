"""One-to-many Stage-6 protocol registry without changing the legacy registry.

The historical global registry assumes at most one operational protocol per
research question. Stage 6 deliberately requires several orthogonal protocols
for the same RQ. This module provides a bounded 1:n view over the dedicated
Stage-6 bundle while preserving legacy callers and campaign history.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

STAGE6_PROTOCOL_FILE = Path("protocols/STAGE6_OPERATIONAL_PROTOCOLS.json")
STAGE6_PREREG_FILE = Path("preregistrations/operational/stage6_bundle_v1.json")


class Stage6ProtocolRegistryError(ValueError):
    """Raised when the Stage-6 protocol bundle is inconsistent."""


def _object(path: Path) -> dict[str, Any]:
    try:
        raw: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise Stage6ProtocolRegistryError(f"cannot read Stage-6 artifact: {path}") from error
    if not isinstance(raw, dict):
        raise Stage6ProtocolRegistryError(f"Stage-6 artifact must be an object: {path}")
    return cast(dict[str, Any], raw)


def stage6_protocols(research_root: Path) -> tuple[dict[str, Any], ...]:
    """Return every dedicated Stage-6 protocol in stable declaration order."""

    document = _object(research_root / STAGE6_PROTOCOL_FILE)
    values = document.get("protocols")
    if not isinstance(values, list):
        raise Stage6ProtocolRegistryError("Stage-6 protocols must be a list")
    output: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in cast(list[object], values):
        if not isinstance(raw, dict):
            raise Stage6ProtocolRegistryError("Stage-6 protocol entry must be an object")
        item = cast(dict[str, Any], raw)
        identifier = item.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in seen:
            raise Stage6ProtocolRegistryError("missing or duplicate Stage-6 protocol ID")
        if not isinstance(item.get("research_question"), str):
            raise Stage6ProtocolRegistryError("Stage-6 research_question must be a string")
        if not isinstance(item.get("hypothesis"), str):
            raise Stage6ProtocolRegistryError("Stage-6 hypothesis must be a string")
        seen.add(identifier)
        output.append(item)
    return tuple(output)


def stage6_protocols_for_question(
    research_root: Path,
    question_id: str,
) -> tuple[dict[str, Any], ...]:
    """Return zero or more protocols registered for one Stage-6 RQ."""

    return tuple(
        protocol
        for protocol in stage6_protocols(research_root)
        if protocol.get("research_question") == question_id
    )


def stage6_protocol_by_id(
    research_root: Path,
    protocol_id: str,
) -> dict[str, Any] | None:
    return next(
        (item for item in stage6_protocols(research_root) if item.get("id") == protocol_id),
        None,
    )


def validate_stage6_bundle(research_root: Path) -> dict[str, Any]:
    """Validate protocol/preregistration parity and DATA-only governance."""

    protocol_document = _object(research_root / STAGE6_PROTOCOL_FILE)
    prereg = _object(research_root / STAGE6_PREREG_FILE)
    if protocol_document.get("automatic_evidence_promotion") is not False:
        raise Stage6ProtocolRegistryError("automatic evidence promotion must be disabled")
    freeze = prereg.get("freeze")
    if not isinstance(freeze, dict):
        raise Stage6ProtocolRegistryError("Stage-6 freeze object is missing")
    freeze_values = cast(dict[str, Any], freeze)
    if freeze_values.get("immutable_after_first_run") is not True:
        raise Stage6ProtocolRegistryError("Stage-6 preregistration must be immutable")
    if freeze_values.get("human_review_required") is not True:
        raise Stage6ProtocolRegistryError("Stage-6 preregistration must require human review")

    prereg_protocols = prereg.get("protocols")
    if not isinstance(prereg_protocols, dict):
        raise Stage6ProtocolRegistryError("Stage-6 preregistration protocols are missing")
    registered = {str(item["id"]): item for item in stage6_protocols(research_root)}
    frozen = cast(dict[str, Any], prereg_protocols)
    if set(registered) != set(frozen):
        raise Stage6ProtocolRegistryError("Stage-6 protocol/preregistration IDs differ")
    for protocol_id, protocol in registered.items():
        prereg_item = frozen.get(protocol_id)
        if not isinstance(prereg_item, dict):
            raise Stage6ProtocolRegistryError(f"invalid preregistration: {protocol_id}")
        conditions = protocol.get("conditions")
        frozen_conditions = cast(dict[str, Any], prereg_item).get("conditions")
        if conditions != frozen_conditions:
            raise Stage6ProtocolRegistryError(
                f"condition mismatch between protocol and preregistration: {protocol_id}"
            )
    return {
        "program": protocol_document.get("program"),
        "protocol_count": len(registered),
        "questions": {
            question: len(stage6_protocols_for_question(research_root, question))
            for question in sorted(
                {
                    str(item["research_question"])
                    for item in registered.values()
                }
            )
        },
        "automatic_evidence_promotion": False,
        "human_review_required": True,
    }


__all__ = [
    "STAGE6_PREREG_FILE",
    "STAGE6_PROTOCOL_FILE",
    "Stage6ProtocolRegistryError",
    "stage6_protocol_by_id",
    "stage6_protocols",
    "stage6_protocols_for_question",
    "validate_stage6_bundle",
]
