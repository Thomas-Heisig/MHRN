"""Static regression checks for the dashboard polling governor."""

from pathlib import Path

STATIC = Path(__file__).resolve().parents[1] / "src" / "dashboard" / "static"


def test_polling_governor_is_installed_before_frontend_initializers() -> None:
    index = (STATIC / "frontend" / "index.js").read_text(encoding="utf-8")
    install = index.index("installPollingGovernor();")
    init = index.index("function init()")
    assert install < init
    assert "./core/polling-governor.js" in index


def test_polling_governor_coalesces_and_throttles_intervals() -> None:
    source = (STATIC / "frontend" / "core" / "polling-governor.js").read_text(
        encoding="utf-8"
    )
    assert "const buckets = new Map()" in source
    assert "document.hidden" in source
    assert "bucket.cycles % 4" in source
    assert "index * 25" in source
    assert "window.clearInterval" in source
    assert "logicalIntervals" in source
