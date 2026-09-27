"""Read-only replay of persisted non-canonical playground sessions."""

from __future__ import annotations

import json
from pathlib import Path

from .._isolation import PlaygroundIsolation
from .session_recorder import DEFAULT_SESSION_ROOT


def replay_session(
    session_id: str, root: Path = DEFAULT_SESSION_ROOT
) -> dict[str, object]:
    if not session_id.replace("-", "").replace("_", "").isalnum():
        raise ValueError("invalid playground session id")
    path = PlaygroundIsolation.assert_safe_read(root / f"{session_id}.json")
    if not path.exists():
        raise FileNotFoundError(f"playground session not found: {session_id}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("invalid playground session payload")
    manifest = data.get("manifest", {})
    if not isinstance(manifest, dict) or manifest.get("class") != "PLAYGROUND":
        raise ValueError("refusing to replay non-playground payload")
    return data
