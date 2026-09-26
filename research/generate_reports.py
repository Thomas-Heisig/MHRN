#!/usr/bin/env python3
"""MHRN Scientific Evidence Framework — deterministic report generator."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.research.literature_registry import LiteratureRegistry
from src.research.meta_system import write_all as write_meta_reports
from src.research.registry import ResearchRegistry
from src.research.report_builder import ReportBuilder

def main() -> None:
    print("Loading research registry...")
    registry = ResearchRegistry()
    registry.load_all()

    print(f"  Questions:  {len(registry.questions)}")
    print(f"  Hypotheses: {len(registry.hypotheses)}")
    print(f"  Claims:     {len(registry.claims)}")
    print(f"  Sources:    {len(registry.sources)}")

    print("\nGenerating reports...")
    paths = ReportBuilder(registry).write_all()
    lit_path = LiteratureRegistry(registry).write_literature_matrix()
    paths.update(write_meta_reports())

    print("\nReports generated:")
    for name, path in sorted(paths.items()):
        size = path.stat().st_size
        print(f"  {name:30s} -> {path.relative_to(Path.cwd())} ({size} bytes)")
    print(f"  {'LITERATURE_MATRIX.md':30s} -> {lit_path.relative_to(Path.cwd())} ({lit_path.stat().st_size} bytes)")
    print("\nDone.")

if __name__ == "__main__":
    main()
