"""Optimized append/commit hot path for the asynchronous runtime journal.

Recovery and explicit validation continue to use :class:`DeltaJournal`'s full
CRC scan.  During a live run, however, the writer already knows the last
sequence, tick and dirty-entry count, so re-reading the whole journal before and
after every commit is unnecessary.
"""

from __future__ import annotations

import os

from .crc import compute_crc32
from .delta_journal import (
    COMMIT_MAGIC,
    COMMIT_MARKER_SIZE,
    COMMIT_STRUCT,
    ENTRY_FLAG_NONE,
    ENTRY_HEADER_STRUCT,
    ENTRY_MAGIC,
    CommitMarker,
    DeltaJournal,
    DeltaRecord,
    UncommittedTailError,
)


class FastDeltaJournal(DeltaJournal):
    """DeltaJournal with O(1) live commits and buffered appends.

    The on-disk format is identical to :class:`DeltaJournal`.  Full scans are
    still performed when a journal is opened or explicitly validated.  This
    class only removes redundant scans/flushes while the writer owns the file.
    """

    def append(self, delta: DeltaRecord) -> int:
        """Append one record without flushing the OS buffer per delta."""
        handle = self._require_handle()
        if self._preexisting_uncommitted_tail:
            raise UncommittedTailError(
                "journal contains a pre-existing uncommitted tail"
            )
        if delta.tick < self._last_tick:
            raise ValueError(
                f"tick must be monotonic: {delta.tick} < {self._last_tick}"
            )
        sequence = self._last_sequence + 1
        crc = compute_crc32(
            self._entry_crc_input(
                sequence,
                delta.tick,
                delta.delta_type,
                ENTRY_FLAG_NONE,
                delta.payload,
            )
        )
        raw_header = ENTRY_HEADER_STRUCT.pack(
            ENTRY_MAGIC,
            sequence,
            delta.tick,
            int(delta.delta_type),
            ENTRY_FLAG_NONE,
            len(delta.payload),
            crc,
        )
        handle.seek(0, os.SEEK_END)
        handle.write(raw_header)
        handle.write(delta.payload)
        self._last_sequence = sequence
        self._last_tick = delta.tick
        self._dirty_entry_count += 1
        self._scan = None
        return sequence

    def commit(self) -> CommitMarker | None:
        """Write one commit marker using in-memory counters, then flush once."""
        if self._dirty_entry_count == 0:
            return None
        handle = self._require_handle()
        sequence = self._last_sequence
        tick = self._last_tick
        committed_entry_count = sequence
        crc = compute_crc32(
            self._commit_crc_input(sequence, tick, committed_entry_count)
        )
        raw = COMMIT_STRUCT.pack(
            COMMIT_MAGIC,
            sequence,
            tick,
            committed_entry_count,
            crc,
            b"\x00" * 4,
        )
        handle.seek(0, os.SEEK_END)
        offset = handle.tell()
        handle.write(raw)
        handle.flush()
        if self.fsync_on_commit:
            os.fsync(handle.fileno())
        marker = CommitMarker(
            sequence=sequence,
            tick=tick,
            committed_entry_count=committed_entry_count,
            offset=offset,
            end_offset=offset + COMMIT_MARKER_SIZE,
        )
        self._dirty_entry_count = 0
        self._scan = None
        return marker


__all__ = ["FastDeltaJournal"]
