"""ExecutionBackend facade for the bounded Wave-4 CUDA reference."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.runtime.backend import (
    BackendCapabilities,
    BackendState,
    ExecutionBackend,
    RunResult,
    StepResult,
)
from src.verification.parity import config_fingerprint, execution_fingerprint

from .plasticity.contracts import PLASTICITY_SEMANTICS
from .recurrent.backend import execute_recurrent
from .recurrent.state import (
    prefix_inputs,
    recurrent_inputs_from_mapping,
    recurrent_inputs_to_mapping,
    stable_digest,
    step_payload,
)


class CUDABackend:
    """Bounded replay adapter over the hardware-verified recurrent kernel."""

    backend_name = "cuda"
    backend_version = "wave4-bounded-replay-v1"

    def __init__(self) -> None:
        self._config: dict[str, object] | None = None
        self._seed = 0
        self._tick = 0

    def initialize(self, config: Mapping[str, object], seed: int) -> None:
        inputs = recurrent_inputs_from_mapping(config, seed=seed)
        self._config = recurrent_inputs_to_mapping(inputs)
        self._seed = seed
        self._tick = 0

    def _require_config(self) -> dict[str, object]:
        if self._config is None:
            raise RuntimeError("backend is not initialized")
        return self._config

    def _execute_prefix(self, total_ticks: int) -> Mapping[str, object]:
        config = self._require_config()
        inputs = recurrent_inputs_from_mapping(config, seed=self._seed)
        result = execute_recurrent(prefix_inputs(inputs, total_ticks))
        outputs = result.get("outputs")
        if not isinstance(outputs, Mapping):
            raise RuntimeError("CUDA recurrent execution returned no outputs")
        return outputs

    def _step_from_outputs(
        self, outputs: Mapping[str, object], tick: int
    ) -> StepResult:
        config = self._require_config()
        payload = step_payload(
            outputs,
            tick=tick,
            n_neurons=int(config["n_neurons"]),
        )
        spikes_raw = payload["spikes"]
        if not isinstance(spikes_raw, list):
            raise ValueError("spike payload must be a list")
        spikes = tuple(
            index for index, value in enumerate(spikes_raw) if int(value) == 1
        )
        return StepResult(
            tick=tick + 1,
            spikes=spikes,
            state_digest=stable_digest(payload),
            metrics={
                "voltage": payload["voltage"],
                "adaptation": payload["adaptation"],
                "spike_count": len(spikes),
            },
        )

    def step(self, tick: int) -> StepResult:
        if tick != self._tick:
            raise ValueError("tick must equal the backend continuation cursor")
        config = self._require_config()
        if tick >= int(config["ticks"]):
            raise ValueError("configured tick limit reached")
        outputs = self._execute_prefix(tick + 1)
        self._tick = tick + 1
        return self._step_from_outputs(outputs, tick)

    def run(self, ticks: int) -> RunResult:
        if type(ticks) is not int or ticks < 1:
            raise ValueError("ticks must be a positive int")
        config = self._require_config()
        total = self._tick + ticks
        if total > int(config["ticks"]):
            raise ValueError("requested run exceeds configured tick limit")
        start = self._tick
        outputs = self._execute_prefix(total)
        steps = tuple(
            self._step_from_outputs(outputs, tick) for tick in range(start, total)
        )
        self._tick = total
        return RunResult(
            ticks_requested=ticks,
            steps=steps,
            final_state=self.snapshot(),
            execution_fingerprint=execution_fingerprint(
                seed=self._seed,
                config_hash=config_fingerprint(config),
                backend_name=self.backend_name,
                backend_version=self.backend_version,
                ticks=total,
            ),
        )

    def snapshot(self) -> BackendState:
        config = self._require_config()
        payload: dict[str, Any] = {
            "backend": self.backend_version,
            "seed": self._seed,
            "tick": self._tick,
            "config": config,
            "replay_required": True,
        }
        return BackendState(
            tick=self._tick,
            payload=payload,
            state_digest=stable_digest(payload),
        )

    def restore(self, state: BackendState) -> None:
        payload = dict(state.payload)
        if payload.get("backend") != self.backend_version:
            raise ValueError("checkpoint backend version mismatch")
        raw_config = payload.get("config")
        raw_seed = payload.get("seed")
        if not isinstance(raw_config, Mapping) or type(raw_seed) is not int:
            raise ValueError("checkpoint is missing canonical config/seed")
        self.initialize(raw_config, raw_seed)
        if state.tick > int(self._require_config()["ticks"]):
            raise ValueError("checkpoint tick exceeds configured limit")
        self._tick = state.tick

    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            supports_recurrent=True,
            supports_plasticity=True,
            supports_pan_hyperstate=False,
            supports_structural_plasticity=False,
            max_neurons=4096,
            max_ticks=2000,
            max_edges=65536,
            deterministic=True,
            plasticity_semantics=PLASTICITY_SEMANTICS,
            execution_mode="BOUNDED_REPLAY_REFERENCE",
        )


def execution_backend_contract_check() -> bool:
    backend: ExecutionBackend = CUDABackend()
    return isinstance(backend, ExecutionBackend)
