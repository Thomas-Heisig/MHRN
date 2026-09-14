"""Normalize Stage-4 signal-processing test references after integration patching."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "tests/test_signal_processing.py"
NEW = "tests/test_signal_processing_contracts.py"


def replace_reference(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if OLD not in text:
        return False
    path.write_text(text.replace(OLD, NEW), encoding="utf-8")
    return True


def main() -> int:
    targets = (
        ROOT / "src" / "dashboard" / "development_timeline.py",
        ROOT / "scripts" / "apply_stage4_integration.py",
    )
    changed = [str(path.relative_to(ROOT)) for path in targets if replace_reference(path)]
    print("Stage-4 signal-processing references normalized:", changed or "already canonical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
