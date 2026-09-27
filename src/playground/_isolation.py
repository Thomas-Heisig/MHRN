"""Hard boundary between exploratory Playground I/O and canonical science."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_WRITE_ROOTS = (
    REPO_ROOT / "research",
    REPO_ROOT / "src" / "research",
)

FORBIDDEN_READ_ROOTS = (REPO_ROOT / "research" / "experiments",)


class PlaygroundIsolationError(RuntimeError):
    """Raised when Playground code crosses a canonical research boundary."""


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


class PlaygroundIsolation:
    """Context marker plus explicit path guards used by all Playground I/O."""

    def __enter__(self) -> "PlaygroundIsolation":
        self._previous = os.environ.get("MHRN_PLAYGROUND")
        os.environ["MHRN_PLAYGROUND"] = "1"
        return self

    def __exit__(self, *_exc: object) -> None:
        previous = getattr(self, "_previous", None)
        if previous is None:
            os.environ.pop("MHRN_PLAYGROUND", None)
        else:
            os.environ["MHRN_PLAYGROUND"] = previous

    @staticmethod
    def assert_safe_write(path: Path) -> Path:
        resolved = path.expanduser().resolve()
        for forbidden in FORBIDDEN_WRITE_ROOTS:
            if _is_within(resolved, forbidden.resolve()):
                raise PlaygroundIsolationError(
                    f"Playground write blocked for canonical path: {resolved}"
                )
        return resolved

    @staticmethod
    def assert_safe_read(path: Path) -> Path:
        resolved = path.expanduser().resolve()
        for forbidden in FORBIDDEN_READ_ROOTS:
            if _is_within(resolved, forbidden.resolve()):
                raise PlaygroundIsolationError(
                    "Playground may not consume canonical experiment evaluation data"
                )
        return resolved

    @classmethod
    def write_text(cls, path: Path, content: str) -> Path:
        target = cls.assert_safe_write(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target


def playground_manifest() -> dict[str, object]:
    """Return mandatory governance flags attached to every Playground result."""

    return {
        "class": "PLAYGROUND",
        "scientific_evidence": False,
        "data": False,
        "evidence_eligible": False,
        "registry_visible": False,
        "maturity_contributing": False,
        "promotion_path": "none",
        "note": "Exploratory session. Not part of scientific evaluation.",
    }
