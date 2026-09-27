"""Compressed local SSD offload for non-canonical Playground telemetry."""

from __future__ import annotations

import gzip
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path

from .._isolation import PlaygroundIsolation
from ..persist.session_recorder import DEFAULT_SESSION_ROOT

_SAFE = re.compile(r"[^A-Za-z0-9_.-]+")


class SSDOffloader:
    """Write cold event batches/snapshots under playground_sessions only."""

    def __init__(
        self,
        *,
        enabled: bool,
        run_key: str,
        snapshot_interval: int,
        root: Path = DEFAULT_SESSION_ROOT,
    ) -> None:
        if snapshot_interval < 1:
            raise ValueError("snapshot_interval must be positive")
        safe_key = _SAFE.sub("_", run_key).strip("._-")[:96] or "pan"
        base = PlaygroundIsolation.assert_safe_write(root / "pan_offload" / safe_key)
        self.enabled = enabled
        self.root = base
        self.snapshot_interval = snapshot_interval
        self.files_written = 0
        self.bytes_written = 0
        self.event_batches = 0
        self.snapshots = 0

    def _write_gzip_json(self, path: Path, payload: object) -> None:
        if not self.enabled:
            return
        target = PlaygroundIsolation.assert_safe_write(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(target, "wt", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, sort_keys=True)
        self.files_written += 1
        try:
            self.bytes_written += target.stat().st_size
        except OSError:
            pass

    def flush_events(
        self,
        *,
        tick: int,
        events: Sequence[Mapping[str, object]],
    ) -> None:
        if not self.enabled or not events:
            return
        payload = [dict(event) for event in events]
        self._write_gzip_json(self.root / f"events_{tick:08d}.json.gz", payload)
        self.event_batches += 1

    def maybe_snapshot(
        self,
        *,
        tick: int,
        payload: Mapping[str, object],
    ) -> None:
        if not self.enabled or (tick + 1) % self.snapshot_interval != 0:
            return
        self._write_gzip_json(
            self.root / f"snapshot_{tick:08d}.json.gz",
            dict(payload),
        )
        self.snapshots += 1

    def summary(self) -> dict[str, object]:
        return {
            "classification": "PLAYGROUND_SSD_OFFLOAD",
            "scientific_evidence": False,
            "enabled": self.enabled,
            "mode": "SYNC_COMPRESSED_REFERENCE",
            "root": str(self.root) if self.enabled else None,
            "files_written": self.files_written,
            "bytes_written": self.bytes_written,
            "event_batches": self.event_batches,
            "snapshots": self.snapshots,
            "async_status": "NOT_IMPLEMENTED_IN_REFERENCE_BACKEND",
        }
