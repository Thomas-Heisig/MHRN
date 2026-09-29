"""Canonical MHRN neural-I/O boundary contracts.

Promoted from the Playground reference implementation on 2026-09-29. These
contracts define engineering interfaces only and do not create scientific DATA
or EVID.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from src.embodiment.msba import SymbolFrame


class NeuralRole(StrEnum):
    """Orthogonal neuron roles from the MHRN Gateway architecture."""

    ASSOCIATIVE = "ASSOCIATIVE"
    AFFERENT = "AFFERENT"
    EFFERENT = "EFFERENT"
    GATEWAY_AFFERENT = "GATEWAY_AFFERENT"
    GATEWAY_EFFERENT = "GATEWAY_EFFERENT"


class InterfacePhase(StrEnum):
    """Causal phases for query/response I/O."""

    IDLE = "IDLE"
    QUERY = "QUERY"
    WAIT = "WAIT"
    RESPONSE = "RESPONSE"
    TIMEOUT = "TIMEOUT"


def canonical_payload_bytes(payload: object) -> tuple[bytes, str]:
    """Return exact deterministic bytes and a declared content type."""

    if isinstance(payload, bytes):
        return payload, "application/octet-stream"
    if isinstance(payload, str):
        return payload.encode("utf-8"), "text/plain; charset=utf-8"
    try:
        text = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("I/O payload must be bytes, text, or finite JSON") from exc
    return text.encode("utf-8"), "application/json"


def _digest_json(payload: dict[str, object]) -> str:
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True, slots=True)
class BoundaryFrame:
    """Exact boundary-plane frame; raw payload never enters the SNN."""

    schema_version: int
    frame_id: str
    stream_id: str
    sequence: int
    direction: str
    kind: str
    content_type: str
    schema_id: str | None
    symbol_frame: SymbolFrame
    correlation_id: str
    priority: int
    source_id: str
    provenance: str
    arrival_time_ns: int | None
    admitted_tick: int

    @property
    def payload(self) -> bytes:
        return self.symbol_frame.payload

    @property
    def payload_sha256(self) -> str:
        return self.symbol_frame.checksum

    @property
    def payload_size_bytes(self) -> int:
        return len(self.symbol_frame.payload)

    def public_metadata(self) -> dict[str, object]:
        """Return metadata only: exact payload bytes are intentionally omitted."""

        return {
            "schema_version": self.schema_version,
            "frame_id": self.frame_id,
            "stream_id": self.stream_id,
            "sequence": self.sequence,
            "direction": self.direction,
            "kind": self.kind,
            "content_type": self.content_type,
            "schema_id": self.schema_id,
            "payload_size_bytes": self.payload_size_bytes,
            "payload_sha256": self.payload_sha256,
            "correlation_id": self.correlation_id,
            "priority": self.priority,
            "source_id": self.source_id,
            "provenance": self.provenance,
            "arrival_time_ns": self.arrival_time_ns,
            "admitted_tick": self.admitted_tick,
            "raw_payload_persisted": False,
        }


@dataclass(frozen=True, slots=True)
class PopulationLayout:
    """Explicit mapping between logical channels and MHRN neuron IDs."""

    schema_version: int
    layout_id: str
    layout_version: str
    layout_kind: str
    role: NeuralRole
    logical_neuron_ids: tuple[int, ...]
    neuron_order: tuple[int, ...]
    coordinates: tuple[tuple[float, ...], ...] | None
    layout_sha256: str

    @classmethod
    def create(
        cls,
        *,
        layout_id: str,
        role: NeuralRole,
        neuron_ids: tuple[int, ...],
        coordinates: tuple[tuple[float, ...], ...] | None = None,
    ) -> "PopulationLayout":
        payload: dict[str, object] = {
            "schema_version": 1,
            "layout_id": layout_id,
            "layout_version": "1.0",
            "layout_kind": "SPARSE",
            "role": role.value,
            "logical_neuron_ids": list(range(len(neuron_ids))),
            "neuron_order": list(neuron_ids),
            "coordinates": (
                [list(point) for point in coordinates]
                if coordinates is not None
                else None
            ),
        }
        return cls(
            schema_version=1,
            layout_id=layout_id,
            layout_version="1.0",
            layout_kind="SPARSE",
            role=role,
            logical_neuron_ids=tuple(range(len(neuron_ids))),
            neuron_order=neuron_ids,
            coordinates=coordinates,
            layout_sha256=_digest_json(payload),
        )

    @property
    def population_size(self) -> int:
        return len(self.neuron_order)

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "layout_id": self.layout_id,
            "layout_version": self.layout_version,
            "layout_kind": self.layout_kind,
            "role": self.role.value,
            "population_size": self.population_size,
            "logical_neuron_ids": list(self.logical_neuron_ids),
            "neuron_order": list(self.neuron_order),
            "layout_sha256": self.layout_sha256,
        }


@dataclass(frozen=True, slots=True)
class CodecContract:
    """Versioned codec contract for one MHRN neural-I/O lane."""

    schema_version: int
    codec_id: str
    codec_version: str
    input_kind: str
    output_kind: str
    coding_scheme: str
    population_size: int
    population_layout_sha256: str
    window_ticks: int
    reconstruction_class: str
    determinism_class: str
    channel_policy: str
    contract_sha256: str

    @classmethod
    def create(
        cls,
        *,
        codec_id: str,
        input_kind: str,
        output_kind: str,
        coding_scheme: str,
        population_size: int,
        population_layout_sha256: str,
        window_ticks: int,
        reconstruction_class: str,
    ) -> "CodecContract":
        payload: dict[str, object] = {
            "schema_version": 1,
            "codec_id": codec_id,
            "codec_version": "1.0",
            "input_kind": input_kind,
            "output_kind": output_kind,
            "coding_scheme": coding_scheme,
            "population_size": population_size,
            "population_layout_sha256": population_layout_sha256,
            "window_ticks": window_ticks,
            "reconstruction_class": reconstruction_class,
            "determinism_class": "DETERMINISTIC_REFERENCE",
            "channel_policy": "DEDICATED_POPULATION",
        }
        return cls(
            schema_version=1,
            codec_id=codec_id,
            codec_version="1.0",
            input_kind=input_kind,
            output_kind=output_kind,
            coding_scheme=coding_scheme,
            population_size=population_size,
            population_layout_sha256=population_layout_sha256,
            window_ticks=window_ticks,
            reconstruction_class=reconstruction_class,
            determinism_class="DETERMINISTIC_REFERENCE",
            channel_policy="DEDICATED_POPULATION",
            contract_sha256=_digest_json(payload),
        )

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "codec_id": self.codec_id,
            "codec_version": self.codec_version,
            "input_kind": self.input_kind,
            "output_kind": self.output_kind,
            "coding_scheme": self.coding_scheme,
            "population_size": self.population_size,
            "population_layout_sha256": self.population_layout_sha256,
            "window_ticks": self.window_ticks,
            "reconstruction_class": self.reconstruction_class,
            "determinism_class": self.determinism_class,
            "channel_policy": self.channel_policy,
            "contract_sha256": self.contract_sha256,
        }


@dataclass(frozen=True, slots=True)
class SpikeEvent:
    source_channel: int
    tick_offset: int

    def to_json(self) -> dict[str, int]:
        return {
            "source_channel": self.source_channel,
            "tick_offset": self.tick_offset,
        }


@dataclass(frozen=True, slots=True)
class SpikeFrame:
    """Atomic neural representation produced by exactly one codec/layout."""

    schema_version: int
    spike_frame_id: str
    source_frame_id: str
    source_frame_sha256: str
    correlation_id: str
    codec_id: str
    codec_version: str
    codec_contract_sha256: str
    source_population_id: str
    population_layout_sha256: str
    start_tick: int
    end_tick: int
    events: tuple[SpikeEvent, ...]
    event_sha256: str
    empty_reason: str | None

    @property
    def event_count(self) -> int:
        return len(self.events)

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "spike_frame_id": self.spike_frame_id,
            "source_frame_id": self.source_frame_id,
            "source_frame_sha256": self.source_frame_sha256,
            "correlation_id": self.correlation_id,
            "codec_id": self.codec_id,
            "codec_version": self.codec_version,
            "codec_contract_sha256": self.codec_contract_sha256,
            "source_population_id": self.source_population_id,
            "population_layout_sha256": self.population_layout_sha256,
            "start_tick": self.start_tick,
            "end_tick": self.end_tick,
            "events": [event.to_json() for event in self.events],
            "event_count": self.event_count,
            "event_sha256": self.event_sha256,
            "empty_reason": self.empty_reason,
        }


@dataclass(frozen=True, slots=True)
class DecodeResult:
    """Bounded readout result: insufficient activity never invents output."""

    schema_version: int
    decoder_id: str
    decoder_version: str
    source_population_id: str
    start_tick: int
    end_tick: int
    status: str
    decoded_value: Any
    reconstruction_class: str
    ambiguity_score: float | None
    determinism_class: str
    readout_sha256: str

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "decoder_id": self.decoder_id,
            "decoder_version": self.decoder_version,
            "source_population_id": self.source_population_id,
            "start_tick": self.start_tick,
            "end_tick": self.end_tick,
            "status": self.status,
            "decoded_value": self.decoded_value,
            "reconstruction_class": self.reconstruction_class,
            "ambiguity_score": self.ambiguity_score,
            "determinism_class": self.determinism_class,
            "readout_sha256": self.readout_sha256,
        }


def event_digest(events: tuple[SpikeEvent, ...]) -> str:
    return _digest_json(
        {"events": [[event.tick_offset, event.source_channel] for event in events]}
    )


def readout_digest(payload: object) -> str:
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
