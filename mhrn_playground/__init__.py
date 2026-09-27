"""Public namespace for the non-canonical MHRN Playground.

Implementation remains isolated in src.playground to match the repository's
internal package layout. External callers should prefer mhrn_playground.
"""

from src.playground import (
    NeuralIOInterface,
    PANRuntime,
    Playground,
    PlaygroundComposer,
    PlaygroundConfig,
    PlaygroundSession,
    TopologyBuilder,
    catalog,
    pan_research_candidates,
    replay,
    robustness,
    run,
    sessions,
)

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
    "run",
    "sessions",
    "pan_research_candidates",
]
