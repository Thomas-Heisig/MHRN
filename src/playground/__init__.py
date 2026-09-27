"""MHRN Playground: isolated exploratory model/topology workbench.

Nothing produced here is scientific DATA or EVID. Any observation that should
enter the research workflow must be reformulated as a new hypothesis and
re-executed through the canonical preregistered research path.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from .builder.composer import PlaygroundComposer
from .builder.network_builder import TopologyBuilder
from .builder.session import PlaygroundSession
from .models import PlaygroundConfig
from .neural_io import NeuralIOInterface
from .pan import PANRuntime, pan_research_candidates
from .persist.session_recorder import record_session
from .service import catalog, replay, robustness, run, sessions


class Playground:
    """Convenience facade matching the interactive Playground API."""

    def __init__(self, **config: object) -> None:
        self.config = PlaygroundConfig.from_mapping(config)
        self.result: dict[str, object] | None = None

    def run(self, ticks: int | None = None) -> dict[str, object]:
        config = replace(self.config, ticks=ticks) if ticks is not None else self.config
        config.validate()
        self.result = PlaygroundSession(config).run()
        return self.result

    def robustness(self) -> dict[str, object]:
        return robustness(self.config.to_dict())

    def record(self, path: str | Path | None = None) -> Path:
        if self.result is None:
            raise RuntimeError("run the playground session before recording it")
        session_id = str(self.result["session_id"])
        if path is None:
            return record_session(session_id, self.result)
        target = Path(path)
        return record_session(target.stem or session_id, self.result, target.parent)


__all__ = [
    "Playground",
    "PlaygroundComposer",
    "PlaygroundConfig",
    "PlaygroundSession",
    "PANRuntime",
    "NeuralIOInterface",
    "TopologyBuilder",
    "catalog",
    "replay",
    "robustness",
    "pan_research_candidates",
    "run",
    "sessions",
]
