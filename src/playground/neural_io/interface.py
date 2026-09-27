"""Runtime bridge between exact Playground I/O and neural populations."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Sequence

from src.embodiment.msba import SymbolFrame

from .codecs import decode_output, encode_input
from .contracts import (
    BoundaryFrame,
    InterfacePhase,
    NeuralRole,
    CodecContract,
    PopulationLayout,
    SpikeFrame,
    canonical_payload_bytes,
)


def _role(value: str) -> NeuralRole:
    try:
        return NeuralRole(value)
    except ValueError as exc:
        raise ValueError(f"unsupported neural I/O role: {value}") from exc


def _phase(value: str) -> InterfacePhase:
    try:
        return InterfacePhase(value)
    except ValueError as exc:
        raise ValueError(f"unsupported neural I/O phase: {value}") from exc


@dataclass(slots=True)
class NeuralIOInterface:
    """Bounded Playground implementation of the postulated neural I/O contract."""

    n_neurons: int
    input_channels: int
    output_channels: int
    input_codec: str
    output_decoder: str
    input_payload: object
    window_ticks: int
    input_current: float
    ticks: int
    dt_ms: float
    seed: int
    input_role: str
    output_role: str
    initial_phase: str
    correlation_id: str
    modality: str
    source_id: str
    _output_counts: list[int] = field(init=False, repr=False)
    _phase_history: list[dict[str, object]] = field(init=False, repr=False)
    _current_phase: InterfacePhase = field(init=False, repr=False)
    _input_schedule: dict[int, tuple[int, ...]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.input_channels + self.output_channels > self.n_neurons:
            raise ValueError("I/O populations must not overlap")
        if self.window_ticks > self.ticks:
            raise ValueError("I/O window_ticks must not exceed session ticks")

        input_ids = tuple(range(self.input_channels))
        output_ids = tuple(range(self.n_neurons - self.output_channels, self.n_neurons))
        self.input_layout = PopulationLayout.create(
            layout_id="playground.gateway.input",
            role=_role(self.input_role),
            neuron_ids=input_ids,
        )
        self.output_layout = PopulationLayout.create(
            layout_id="playground.gateway.output",
            role=_role(self.output_role),
            neuron_ids=output_ids,
        )

        payload_bytes, content_type = canonical_payload_bytes(self.input_payload)
        symbol = SymbolFrame(
            payload=payload_bytes,
            codec=self.input_codec,
            sequence=0,
            provenance="PLAYGROUND_NEURAL_IO",
        )
        correlation = self.correlation_id.strip()
        if not correlation:
            basis = f"{self.seed}:{symbol.checksum}:playground-neural-io".encode()
            correlation = "pgio-" + hashlib.sha256(basis).hexdigest()[:16]
        self.correlation_id = correlation
        frame_basis = (
            f"{symbol.checksum}:{correlation}:{self.modality}:{self.source_id}".encode()
        )
        frame_id = "pg-boundary-" + hashlib.sha256(frame_basis).hexdigest()[:16]
        self.boundary = BoundaryFrame(
            schema_version=1,
            frame_id=frame_id,
            stream_id="playground-neural-io",
            sequence=0,
            direction="AFFERENT",
            kind=self.modality,
            content_type=content_type,
            schema_id=None,
            symbol_frame=symbol,
            correlation_id=correlation,
            priority=0,
            source_id=self.source_id,
            provenance="PLAYGROUND_USER_INPUT",
            arrival_time_ns=None,
            admitted_tick=0,
        )
        self.codec_contract, self.input_spike_frame = encode_input(
            boundary=self.boundary,
            codec_id=self.input_codec,
            layout=self.input_layout,
            window_ticks=self.window_ticks,
        )
        schedule: dict[int, list[int]] = {}
        for event in self.input_spike_frame.events:
            tick = self.input_spike_frame.start_tick + event.tick_offset
            schedule.setdefault(tick, []).append(event.source_channel)
        self._input_schedule = {
            tick: tuple(sorted(channels)) for tick, channels in schedule.items()
        }

        self._output_counts = [0 for _ in range(self.output_channels)]
        self._current_phase = _phase(self.initial_phase)
        self._phase_history = [{"tick": 0, "phase": self._current_phase.value}]

    input_layout: PopulationLayout = field(init=False)
    output_layout: PopulationLayout = field(init=False)
    boundary: BoundaryFrame = field(init=False)
    codec_contract: CodecContract = field(init=False)
    input_spike_frame: SpikeFrame = field(init=False)

    def _set_phase(self, tick: int, phase: InterfacePhase) -> None:
        if phase == self._current_phase:
            return
        self._current_phase = phase
        self._phase_history.append({"tick": tick, "phase": phase.value})

    def currents_for_tick(self, tick: int) -> list[float]:
        """Project encoded afferent events onto dedicated input neurons."""

        if self._current_phase == InterfacePhase.QUERY and tick >= self.window_ticks:
            self._set_phase(tick, InterfacePhase.WAIT)

        values = [0.0 for _ in range(self.n_neurons)]
        for local_channel in self._input_schedule.get(tick, ()):
            neuron_id = self.input_layout.neuron_order[local_channel]
            values[neuron_id] += self.input_current
        return values

    def observe(self, tick: int, spiked_neurons: Sequence[int]) -> None:
        """Collect egress activity from the dedicated output population."""

        reverse = {
            neuron_id: local
            for local, neuron_id in enumerate(self.output_layout.neuron_order)
        }
        output_activity = False
        for neuron_id in spiked_neurons:
            local = reverse.get(neuron_id)
            if local is None:
                continue
            self._output_counts[local] += 1
            output_activity = True
        if (
            output_activity
            and tick >= self.window_ticks
            and self._current_phase in {InterfacePhase.QUERY, InterfacePhase.WAIT}
        ):
            self._set_phase(tick, InterfacePhase.RESPONSE)

    def finalize(self) -> dict[str, object]:
        """Return a public summary with no raw boundary payload."""

        if self._current_phase in {InterfacePhase.QUERY, InterfacePhase.WAIT}:
            self._set_phase(max(self.ticks - 1, 0), InterfacePhase.TIMEOUT)

        decoded = decode_output(
            decoder_id=self.output_decoder,
            layout=self.output_layout,
            spike_counts=self._output_counts,
            ticks=self.ticks,
            dt_ms=self.dt_ms,
        )
        associated = self.n_neurons - self.input_channels - self.output_channels
        return {
            "classification": "PLAYGROUND_NEURAL_IO",
            "scientific_evidence": False,
            "data": False,
            "evidence_eligible": False,
            "registry_visible": False,
            "maturity_contributing": False,
            "boundary_principle": "Payload != Neural Representation",
            "architecture_principle": ("Codec != GatewayTopology != GatewayLearning"),
            "exact_boundary": self.boundary.public_metadata(),
            "input": {
                "role": self.input_layout.role.value,
                "layout": self.input_layout.to_json(),
                "codec_contract": self.codec_contract.to_json(),
                "spike_frame": self.input_spike_frame.to_json(),
                "injection_current": self.input_current,
            },
            "output": {
                "role": self.output_layout.role.value,
                "layout": self.output_layout.to_json(),
                "spike_counts": list(self._output_counts),
                "decode_result": decoded.to_json(),
                "tool_plane_execution": False,
                "actuator_execution": False,
                "note": (
                    "Decoded output remains inside the Playground; external "
                    "tools/actuators are never executed by this interface."
                ),
            },
            "roles": {
                self.input_layout.role.value: self.input_channels,
                NeuralRole.ASSOCIATIVE.value: associated,
                self.output_layout.role.value: self.output_channels,
            },
            "lifecycle": {
                "correlation_id": self.correlation_id,
                "phase_history": list(self._phase_history),
                "final_phase": self._current_phase.value,
                "contract": ["QUERY", "WAIT", "RESPONSE", "TIMEOUT"],
                "implementation_status": "REFERENCE_STATE_MACHINE_ONLY",
                "gateway_action_selection_status": "NOT_IMPLEMENTED",
                "external_round_trip_status": "NOT_IMPLEMENTED",
                "response_observation_semantics": (
                    "Playground egress-population activity only; not an "
                    "external GatewayResponseFrame."
                ),
            },
            "modality": self.modality,
            "network_area_adapter_contract": (
                "src.embodiment.neural_symbiosis.NetworkAreaAdapter"
            ),
            "shared_query_response_layout": {
                "logical_shape": [100, 100],
                "logical_channels": 10_000,
                "status": "EXPERIMENTAL_CONCEPT_NOT_ALLOCATED_IN_PLAYGROUND",
                "note": (
                    "Query/Response may share a logical layout only when "
                    "direction, phase, correlation_id and provenance remain explicit."
                ),
            },
            "learning": {
                "encoder_learning": False,
                "decoder_learning": False,
                "vocabulary_mutation": False,
                "layout_mutation": False,
                "gateway_learning": False,
            },
            "promotion_path": (
                "new hypothesis -> preregistration -> freeze -> new canonical "
                "DATA run -> Human Review -> optional EVID"
            ),
        }
