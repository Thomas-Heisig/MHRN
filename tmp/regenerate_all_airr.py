"""
Regeneriere AIRR-Berichte für alle Batch-Experimente mit dem gefixten normalize_output.

Löscht alte fehlgeschlagene Analyse-Records und Reports und lässt die AIRR-Pipeline
für jedes Experiment neu durchlaufen.
"""
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.research_assistant.airr import AIRRPipeline
from src.research_assistant.ollama_backend import OllamaBackend

RESEARCH_ROOT = Path("research")
BATCH_PREFIX = "EXP-BATCH-20260914074039"

# ── Backend konfigurieren ──
backend = OllamaBackend(
    model="qwen2.5-coder:7b",
    endpoint="http://127.0.0.1:11434/api/generate",
    temperature=0.0,
    top_p=1.0,
    max_tokens=4096,
    timeout=300.0,
)

pipeline = AIRRPipeline(RESEARCH_ROOT)

# ── Alle Batch-Experimente finden ──
experiments = sorted([
    d.name for d in RESEARCH_ROOT.joinpath("experiments").iterdir()
    if d.is_dir() and d.name.startswith(BATCH_PREFIX)
])

print(f"Gefundene Batch-Experimente: {len(experiments)}")
print()

for i, exp_id in enumerate(experiments, 1):
    exp_dir = RESEARCH_ROOT / "experiments" / exp_id
    analysis_dir = exp_dir / "analysis"
    reports_dir = exp_dir / "reports"

    # Alte Analyse-Records löschen (nur die fehlgeschlagenen mit system-fallback)
    deleted_analysis = 0
    if analysis_dir.exists():
        for f in sorted(analysis_dir.glob("AIAR-*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                provider = data.get("model", {}).get("provider", "")
                if provider == "system-fallback":
                    f.unlink()
                    deleted_analysis += 1
            except Exception:
                pass

    # Alte Reports löschen
    deleted_reports = 0
    if reports_dir.exists():
        for f in list(reports_dir.glob("AIRR-*.md")) + list(reports_dir.glob("AIRR-*.json")):
            f.unlink()
            deleted_reports += 1

    print(f"[{i}/{len(experiments)}] {exp_id}: gelöscht {deleted_analysis} Analyse-Records, {deleted_reports} Reports")

    # AIRR neu generieren
    try:
        report = pipeline.analyze(exp_id, backend)
        print(f"  ✅ AIRR generiert: {report.report_id}")
    except Exception as e:
        print(f"  ❌ Fehler: {type(e).__name__}: {e}")

print()
print("Fertig.")
