# Current Scientific State

**Stand:** 15. September 2026

Dieses Dokument ist der kurze Einstieg in den aktuellen wissenschaftlichen Zustand des Repositories. Historische DATA und Publikationsstände bleiben in ihren datierten Verzeichnissen unverändert.

## Aktuelle Publikation

- **Recursive Epistemics / Rekursive Epistemik, Fassung 1.6**
- Einstieg: `research/publications/2026-09-15_recursive-epistemics_v1.6/README.md`
- empirische Basis: Fassung 1.5 / `EXP-EMP-20260913-A3`
- menschliches wissenschaftliches Review: ausstehend
- automatische EVID-Promotion: deaktiviert

## Zwei Entwicklungsachsen

### Engineering

Quelle: `src/dashboard/development_timeline.py`

Bewertet Implementierung, Integration, technische Verifikation, Runtime und Persistenz. Engineering-Reife ist keine wissenschaftliche Evidenz.

### Wissenschaft

Quelle: `src/dashboard/static/scientific-progress.json`

Bewertet je Stufe 0–10:

- registrierte Forschungsfrage/Hypothese,
- eingefrorenes Protokoll,
- quellengebundene DATA,
- menschlich reviewte EVID,
- unabhängige Replikation,
- Attribution/Related Work.

Der Score ist eine Projektsteuerungsheuristik und keine Kognitions-, Intelligenz- oder Bewusstseinskennzahl.

## Aktueller Schwerpunkt

Stage 6 – Gedächtnis und Weltmodell.

### Semantization / Continual Learning

- `EXP-S6-SEM-CL-001`: positiver präregistrierter Mechanismusbefund gegenüber einer naiven Online-Baseline ohne Replay. Unter seinem eigenen eingefrorenen Protokoll verbesserten semantische Konsolidierung plus begrenztes Replay finale Accuracy und Vergessen deutlich.
- `EXP-S6-SEM-CL-002`: präregistrierter, vollständig gepaarter Negativbefund für die spezifischere Hypothese eines Vorteils semantischer Prototypen gegenüber gleich objekt- und updatebudgetiertem Raw-Replay. Alle drei konjunktiven Erfolgskriterien verfehlten die vorab festgelegten Mindestwirkungen. H1 gilt unter diesem Protokoll als falsifiziert.
- Der kleine B3-vs-B4-Accuracy-Unterschied in CL-002 ist statistisch positiv, aber mit rund 0,18 Prozentpunkten weit unter der präregistrierten Mindestwirkung von 3 Prozentpunkten und daher kein positiver konfirmatorischer Semantikbefund.
- CL-002 beweist nicht rückwirkend, dass CL-001 „nur Replay“ war, weil die Replay-/Updateregime beider Experimente verschieden sind. Belastbar ist derzeit nur: Ein spezifischer Vorteil semantischer Verdichtung gegenüber Raw-Replay ist nicht nachgewiesen.

Die DATA/EVID-Trennung bleibt erhalten. CL-002 liegt als DATA unter `research/experiments/EXP-S6-SEM-CL-002/results/`; die menschliche Projektinterpretation liegt unter `research/experiments/EXP-S6-SEM-CL-002/EVID.md` und `EVID.json`.

Weitere offene Stage-6-Punkte sind insbesondere:

- Replikation und Dosis-/Budget-Ablation der Semantization, ohne CL-002 post hoc zu verändern,
- neuronale und abladierbare Prediction-Error-Dynamik,
- mehrschrittiges aktionskonditioniertes Weltmodell,
- gekoppelte Persistenz/Restore-Identität,
- Vergleich gegen einen echten Standard-SNN-Continual-Learning-Baseline-Stack,
- unabhängige externe Replikation.

## Integrität

- `research/INTEGRITY_AND_ATTRIBUTION.md`
- `research/RELATED_WORK.md`
- `docs/05-quality/RESEARCH_INTEGRITY_GATE.md`
- `docs/08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md`

Diese Instrumente reduzieren Fehlattribution und unmarkiertes Text-Recycling. Sie zertifizieren keine Plagiatsfreiheit; vor formaler externer Einreichung bleiben menschliche Quellenprüfung und geeignete externe Similarity-Prüfung erforderlich.
