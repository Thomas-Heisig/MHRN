"""Canonical deterministic codecs/decoders for MHRN neural I/O.

Promoted from the Playground reference implementation on 2026-09-29.
The functions are deterministic engineering contracts; using them does not
create scientific DATA or EVID.
"""

from __future__ import annotations

import json
import math
from collections.abc import Sequence
from typing import cast

from .neural_io_contracts import (
    BoundaryFrame,
    CodecContract,
    DecodeResult,
    PopulationLayout,
    SpikeEvent,
    SpikeFrame,
    event_digest,
    readout_digest,
)

DEFAULT_SYMBOL_VOCABULARY: tuple[str, ...] = (
    "QUERY",
    "RESPONSE",
    "SUCCESS",
    "FAILURE",
    "CONTINUE",
    "STOP",
    "UNKNOWN",
    "REQUEST_TOOL",
    "REQUEST_MEMORY",
    "REQUEST_VISION",
    "REQUEST_LLM",
)

CODEC_CATALOG: tuple[dict[str, object], ...] = (
    {
        "id": "population_latency_v1",
        "available": True,
        "input_kind": "scalar",
        "reconstruction_class": "BOUNDED_LOSS",
    },
    {
        "id": "vector_population_v1",
        "available": True,
        "input_kind": "numeric_vector",
        "reconstruction_class": "BOUNDED_LOSS",
    },
    {
        "id": "sparse_symbol_v1",
        "available": True,
        "input_kind": "symbol",
        "reconstruction_class": "IDENTITY_ONLY",
    },
    {
        "id": "bit_exact_v1",
        "available": False,
        "input_kind": "bytes",
        "reconstruction_class": "EXACT",
        "status": "planned_reference_not_implemented",
    },
    {
        "id": "hash_fingerprint_v0",
        "available": False,
        "input_kind": "bytes",
        "reconstruction_class": "IDENTITY_ONLY",
        "status": "negative_control_not_productive_codec",
    },
)

DECODER_CATALOG: tuple[dict[str, object], ...] = (
    {
        "id": "population_rate_v1",
        "available": True,
        "output_kind": "rate_vector",
    },
    {
        "id": "sparse_symbol_v1",
        "available": True,
        "output_kind": "symbol",
    },
)


def _decode_boundary_payload(boundary: BoundaryFrame) -> object:
    content_type = boundary.content_type
    raw = boundary.payload
    if content_type.startswith("text/plain"):
        return raw.decode("utf-8")
    if content_type == "application/json":
        return json.loads(raw.decode("utf-8"))
    return raw


def _make_spike_frame(
    *,
    boundary: BoundaryFrame,
    contract: CodecContract,
    layout: PopulationLayout,
    start_tick: int,
    events: Sequence[SpikeEvent],
    empty_reason: str | None = None,
) -> SpikeFrame:
    ordered = tuple(
        sorted(
            events,
            key=lambda event: (event.tick_offset, event.source_channel),
        )
    )
    digest = event_digest(ordered)
    frame_id = f"mhrn-spike-{digest[:16]}"
    return SpikeFrame(
        schema_version=1,
        spike_frame_id=frame_id,
        source_frame_id=boundary.frame_id,
        source_frame_sha256=boundary.payload_sha256,
        correlation_id=boundary.correlation_id,
        codec_id=contract.codec_id,
        codec_version=contract.codec_version,
        codec_contract_sha256=contract.contract_sha256,
        source_population_id=layout.layout_id,
        population_layout_sha256=layout.layout_sha256,
        start_tick=start_tick,
        end_tick=start_tick + max(contract.window_ticks - 1, 0),
        events=ordered,
        event_sha256=digest,
        empty_reason=empty_reason if not ordered else None,
    )


def _scalar(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("population_latency_v1 requires one numeric scalar")
    converted = float(value)
    if not math.isfinite(converted):
        raise ValueError("I/O scalar must be finite")
    if not 0.0 <= converted <= 1.0:
        raise ValueError("population_latency_v1 input must be in [0,1]")
    return converted


def encode_input(
    *,
    boundary: BoundaryFrame,
    codec_id: str,
    layout: PopulationLayout,
    window_ticks: int,
) -> tuple[CodecContract, SpikeFrame]:
    """Encode an exact boundary payload into one deterministic SpikeFrame."""

    if window_ticks < 1:
        raise ValueError("window_ticks must be positive")
    value = _decode_boundary_payload(boundary)

    if codec_id == "population_latency_v1":
        scalar = _scalar(value)
        size = layout.population_size
        if size < 2:
            raise ValueError("population_latency_v1 requires at least two channels")
        contract = CodecContract.create(
            codec_id=codec_id,
            input_kind="scalar",
            output_kind="spikes",
            coding_scheme="population_latency",
            population_size=size,
            population_layout_sha256=layout.layout_sha256,
            window_ticks=window_ticks,
            reconstruction_class="BOUNDED_LOSS",
        )
        sigma = 0.18
        threshold = 0.10
        events: list[SpikeEvent] = []
        for channel in range(size):
            preferred = channel / max(size - 1, 1)
            activation = math.exp(-((scalar - preferred) ** 2) / (2.0 * sigma**2))
            if activation < threshold:
                continue
            tick_offset = round((1.0 - activation) * max(window_ticks - 1, 0))
            events.append(SpikeEvent(channel, tick_offset))
        if not events:
            preferred_channel = round(scalar * (size - 1))
            events.append(SpikeEvent(preferred_channel, 0))
        return contract, _make_spike_frame(
            boundary=boundary,
            contract=contract,
            layout=layout,
            start_tick=boundary.admitted_tick,
            events=events,
        )

    if codec_id == "vector_population_v1":
        if not isinstance(value, list):
            raise ValueError("vector_population_v1 requires a JSON numeric list")
        vector = cast(list[object], value)
        if len(vector) > layout.population_size:
            raise ValueError("input vector exceeds afferent population size")
        contract = CodecContract.create(
            codec_id=codec_id,
            input_kind="numeric_vector",
            output_kind="spikes",
            coding_scheme="per_channel_latency",
            population_size=layout.population_size,
            population_layout_sha256=layout.layout_sha256,
            window_ticks=window_ticks,
            reconstruction_class="BOUNDED_LOSS",
        )
        events = []
        for channel, item in enumerate(vector):
            scalar = _scalar(item)
            if scalar <= 0.0:
                continue
            tick_offset = round((1.0 - scalar) * max(window_ticks - 1, 0))
            events.append(SpikeEvent(channel, tick_offset))
        return contract, _make_spike_frame(
            boundary=boundary,
            contract=contract,
            layout=layout,
            start_tick=boundary.admitted_tick,
            events=events,
            empty_reason="BELOW_THRESHOLD",
        )

    if codec_id == "sparse_symbol_v1":
        if not isinstance(value, str):
            raise ValueError("sparse_symbol_v1 requires a text symbol")
        if layout.population_size < len(DEFAULT_SYMBOL_VOCABULARY):
            raise ValueError(
                "sparse_symbol_v1 requires at least "
                f"{len(DEFAULT_SYMBOL_VOCABULARY)} input channels"
            )
        try:
            channel = DEFAULT_SYMBOL_VOCABULARY.index(value)
        except ValueError as exc:
            raise ValueError(f"symbol not in fixed MHRN vocabulary: {value}") from exc
        contract = CodecContract.create(
            codec_id=codec_id,
            input_kind="symbol",
            output_kind="spikes",
            coding_scheme="fixed_sparse_vocabulary",
            population_size=layout.population_size,
            population_layout_sha256=layout.layout_sha256,
            window_ticks=window_ticks,
            reconstruction_class="IDENTITY_ONLY",
        )
        return contract, _make_spike_frame(
            boundary=boundary,
            contract=contract,
            layout=layout,
            start_tick=boundary.admitted_tick,
            events=[SpikeEvent(channel, 0)],
        )

    raise ValueError(f"unsupported MHRN input codec: {codec_id}")


def decode_output(
    *,
    decoder_id: str,
    layout: PopulationLayout,
    spike_counts: Sequence[int],
    ticks: int,
    dt_ms: float,
) -> DecodeResult:
    """Decode egress population activity without inventing missing output."""

    if len(spike_counts) != layout.population_size:
        raise ValueError("output spike count width does not match layout")
    total = sum(spike_counts)
    duration_s = max(ticks * dt_ms / 1000.0, 1e-12)

    if decoder_id == "population_rate_v1":
        rates = [count / duration_s for count in spike_counts]
        payload: object = [round(value, 6) for value in rates]
        status = "VALID" if total > 0 else "INSUFFICIENT_ACTIVITY"
        if total == 0:
            payload = None
        return DecodeResult(
            schema_version=1,
            decoder_id=decoder_id,
            decoder_version="1.0",
            source_population_id=layout.layout_id,
            start_tick=0,
            end_tick=max(ticks - 1, 0),
            status=status,
            decoded_value=payload,
            reconstruction_class="APPROXIMATE",
            ambiguity_score=None,
            determinism_class="DETERMINISTIC_REFERENCE",
            readout_sha256=readout_digest(
                {"counts": list(spike_counts), "ticks": ticks, "dt_ms": dt_ms}
            ),
        )

    if decoder_id == "sparse_symbol_v1":
        if layout.population_size < len(DEFAULT_SYMBOL_VOCABULARY):
            raise ValueError(
                "sparse_symbol_v1 decoder requires at least "
                f"{len(DEFAULT_SYMBOL_VOCABULARY)} output channels"
            )
        if total == 0:
            status = "INSUFFICIENT_ACTIVITY"
            decoded: object = None
            ambiguity = None
        else:
            relevant = list(spike_counts[: len(DEFAULT_SYMBOL_VOCABULARY)])
            peak = max(relevant)
            winners = [index for index, count in enumerate(relevant) if count == peak]
            if peak <= 0:
                status = "INSUFFICIENT_ACTIVITY"
                decoded = None
                ambiguity = None
            elif len(winners) > 1:
                status = "AMBIGUOUS"
                decoded = None
                ambiguity = len(winners) / len(DEFAULT_SYMBOL_VOCABULARY)
            else:
                status = "VALID"
                decoded = DEFAULT_SYMBOL_VOCABULARY[winners[0]]
                ambiguity = 0.0
        return DecodeResult(
            schema_version=1,
            decoder_id=decoder_id,
            decoder_version="1.0",
            source_population_id=layout.layout_id,
            start_tick=0,
            end_tick=max(ticks - 1, 0),
            status=status,
            decoded_value=decoded,
            reconstruction_class="IDENTITY_ONLY",
            ambiguity_score=ambiguity,
            determinism_class="DETERMINISTIC_REFERENCE",
            readout_sha256=readout_digest(
                {"counts": list(spike_counts), "vocabulary": DEFAULT_SYMBOL_VOCABULARY}
            ),
        )

    raise ValueError(f"unsupported MHRN output decoder: {decoder_id}")
