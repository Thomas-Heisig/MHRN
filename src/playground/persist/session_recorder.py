"""Non-canonical session persistence for the Playground."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Mapping

from .._isolation import PlaygroundIsolation

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SESSION_ROOT = REPO_ROOT / "playground_sessions"

MAX_SESSION_BYTES = 50 * 1024 * 1024
RETENTION_DAYS = 30
MAX_SESSION_FILES = 200


def _prune_sessions(root: Path, now: float | None = None) -> None:
    """Delete only expired/overflow Playground JSON sessions."""

    PlaygroundIsolation.assert_safe_write(root)
    if not root.exists():
        return
    current = time.time() if now is None else now
    cutoff = current - RETENTION_DAYS * 24 * 60 * 60
    files = [path for path in root.glob("*.json") if path.is_file()]
    for path in files:
        try:
            if path.stat().st_mtime < cutoff:
                path.unlink()
        except OSError:
            continue
    remaining = sorted(
        (path for path in root.glob("*.json") if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for path in remaining[MAX_SESSION_FILES:]:
        try:
            path.unlink()
        except OSError:
            continue


def record_session(
    session_id: str,
    payload: Mapping[str, object],
    root: Path = DEFAULT_SESSION_ROOT,
) -> Path:
    root = PlaygroundIsolation.assert_safe_write(root)
    root.mkdir(parents=True, exist_ok=True)
    _prune_sessions(root)
    content = json.dumps(
        dict(payload),
        indent=2,
        ensure_ascii=False,
        sort_keys=True,
    )
    byte_count = len(content.encode("utf-8"))
    if byte_count > MAX_SESSION_BYTES:
        raise ValueError(
            f"Playground session exceeds {MAX_SESSION_BYTES} byte persistence limit"
        )
    target = root / f"{session_id}.json"
    written = PlaygroundIsolation.write_text(target, content)
    _prune_sessions(root)
    return written


def list_sessions(root: Path = DEFAULT_SESSION_ROOT) -> list[dict[str, object]]:
    root = PlaygroundIsolation.assert_safe_read(root)
    if not root.exists():
        return []
    _prune_sessions(root)
    result: list[dict[str, object]] = []
    files = sorted(
        (path for path in root.glob("*.json") if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for path in files[:100]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        result.append(
            {
                "session_id": data.get("session_id", path.stem),
                "name": (
                    data.get("config", {}).get("name")
                    if isinstance(data.get("config"), dict)
                    else None
                ),
                "created_at": data.get("created_at"),
                "path": (
                    str(path.relative_to(REPO_ROOT))
                    if path.is_relative_to(REPO_ROOT)
                    else str(path)
                ),
                "class": (
                    data.get("manifest", {}).get("class")
                    if isinstance(data.get("manifest"), dict)
                    else None
                ),
            }
        )
    return result
