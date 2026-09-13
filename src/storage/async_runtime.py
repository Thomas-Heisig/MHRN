"""Bounded asynchronous journal writer for MHRN runtime persistence."""

from __future__ import annotations

import time
from dataclasses import dataclass
from queue import Full, Queue
from threading import Event, Lock, Thread
from typing import Final

from .delta_journal import DeltaJournal, DeltaRecord
from .fast_delta_journal import FastDeltaJournal
from .incremental_runtime import IncrementalStorageSession
from .runtime import (
    RuntimeNetworkLike,
    StepResultLike,
    StorageRuntimeConfig,
    StorageSession,
)

_STOP: Final[object] = object()


@dataclass(frozen=True, slots=True)
class AsyncStorageConfig:
    """Configuration for bounded asynchronous persistence."""

    queue_size: int = 1000
    drop_on_overflow: bool = False
    enqueue_timeout_s: float = 0.25
    neuron_state_interval_ticks: int = 1
    fsync_on_commit: bool = True

    def __post_init__(self) -> None:
        if self.queue_size <= 0:
            raise ValueError("queue_size must be positive")
        if self.enqueue_timeout_s < 0.0:
            raise ValueError("enqueue_timeout_s must be non-negative")
        if self.neuron_state_interval_ticks <= 0:
            raise ValueError("neuron_state_interval_ticks must be positive")


@dataclass(frozen=True, slots=True)
class StorageTelemetrySnapshot:
    """Immutable storage runtime telemetry."""

    queue_depth: int
    queue_capacity: int
    batches_enqueued: int
    batches_written: int
    deltas_written: int
    bytes_written: int
    dropped_batches: int
    write_latency_ms: float
    commit_latency_ms: float
    journal_size_bytes: int
    worker_failed: bool


@dataclass(frozen=True, slots=True)
class _Batch:
    tick: int
    deltas: tuple[DeltaRecord, ...]


class AsyncStorageSession:
    """Persist typed delta batches on a bounded background worker thread."""

    def __init__(
        self,
        network: RuntimeNetworkLike,
        runtime_config: StorageRuntimeConfig,
        async_config: AsyncStorageConfig,
    ) -> None:
        self.network = network
        self.runtime_config = runtime_config
        self.async_config = async_config
        if runtime_config.capture_policy == "dirty_tracking":
            self._collector: StorageSession = IncrementalStorageSession(
                network,
                runtime_config,
                neuron_state_interval_ticks=async_config.neuron_state_interval_ticks,
            )
        else:
            self._collector = StorageSession(network, runtime_config)
        self._queue: Queue[_Batch | object] = Queue(maxsize=async_config.queue_size)
        self._thread: Thread | None = None
        self._stop = Event()
        self._failure: BaseException | None = None
        self._lock = Lock()
        self._attached = False
        self._batches_enqueued = 0
        self._batches_written = 0
        self._deltas_written = 0
        self._bytes_written = 0
        self._dropped_batches = 0
        self._write_latency_ms = 0.0
        self._commit_latency_ms = 0.0

    def __enter__(self) -> AsyncStorageSession:
        self.start()
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()

    @property
    def attached(self) -> bool:
        return self._attached

    @property
    def telemetry(self) -> StorageTelemetrySnapshot:
        with self._lock:
            journal_size = (
                self.runtime_config.journal_path.stat().st_size
                if self.runtime_config.journal_path.exists()
                else 0
            )
            return StorageTelemetrySnapshot(
                queue_depth=self._queue.qsize(),
                queue_capacity=self.async_config.queue_size,
                batches_enqueued=self._batches_enqueued,
                batches_written=self._batches_written,
                deltas_written=self._deltas_written,
                bytes_written=self._bytes_written,
                dropped_batches=self._dropped_batches,
                write_latency_ms=self._write_latency_ms,
                commit_latency_ms=self._commit_latency_ms,
                journal_size_bytes=journal_size,
                worker_failed=self._failure is not None,
            )

    def start(self) -> None:
        if self._attached:
            return
        self._prepare_collector()
        self._stop.clear()
        self._thread = Thread(
            target=self._worker_main,
            name="brain5d-storage",
            daemon=True,
        )
        self._thread.start()
        self.network.add_post_step_hook(self.capture)
        self._attached = True

    def _prepare_collector(self) -> None:
        self._collector.prepare_snapshot()
        self._collector.prime()

    def capture(self, result: StepResultLike) -> None:
        self._raise_worker_failure()
        deltas = self._collector.collect_deltas(result)
        if not deltas:
            return
        batch = _Batch(int(result.tick), deltas)
        if self.async_config.drop_on_overflow:
            try:
                self._queue.put_nowait(batch)
            except Full:
                with self._lock:
                    self._dropped_batches += 1
                return
        else:
            self._queue.put(
                batch,
                timeout=self.async_config.enqueue_timeout_s or None,
            )
        with self._lock:
            self._batches_enqueued += 1

    def flush(self) -> None:
        self._queue.join()
        self._raise_worker_failure()

    def close(self) -> None:
        if self._attached:
            self.network.remove_post_step_hook(self.capture)
            self._attached = False
        if self._thread is None:
            return
        self.flush()
        self._queue.put(_STOP)
        self._thread.join()
        self._thread = None
        self._raise_worker_failure()

    def _raise_worker_failure(self) -> None:
        if self._failure is not None:
            raise RuntimeError(
                "asynchronous storage worker failed"
            ) from self._failure

    def _worker_main(self) -> None:
        try:
            with FastDeltaJournal(
                self.runtime_config.journal_path,
                base_tick=self.network.current_tick,
                fsync_on_commit=self.async_config.fsync_on_commit,
            ) as journal:
                scan = journal.validate()
                if scan.has_uncommitted_tail:
                    journal.truncate_uncommitted_tail()
                while not self._stop.is_set():
                    item = self._queue.get()
                    try:
                        if item is _STOP:
                            if journal.dirty_entry_count:
                                self._record_commit(journal)
                            return
                        if not isinstance(item, _Batch):
                            raise TypeError("invalid async storage queue item")
                        self._write_batch(journal, item)
                    finally:
                        self._queue.task_done()
        except BaseException as exc:
            self._failure = exc

    def _write_batch(self, journal: DeltaJournal, batch: _Batch) -> None:
        started = time.perf_counter()
        written_bytes = 0
        for delta in batch.deltas:
            journal.append(delta)
            written_bytes += len(delta.payload)
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        if (
            (batch.tick + 1) % self.runtime_config.commit_interval_ticks == 0
            and journal.dirty_entry_count
        ):
            self._record_commit(journal)
        with self._lock:
            self._batches_written += 1
            self._deltas_written += len(batch.deltas)
            self._bytes_written += written_bytes
            self._write_latency_ms = elapsed_ms

    def _record_commit(self, journal: DeltaJournal) -> None:
        started = time.perf_counter()
        journal.commit()
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        with self._lock:
            self._commit_latency_ms = elapsed_ms
