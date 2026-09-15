# Current Scientific State

**Stand:** 15. September 2026

Dieses Dokument ist der kurze Einstieg in den aktuellen wissenschaftlichen Zustand. Historische DATA, EVID-Entscheidungen und frozen Publikationen bleiben in ihren datierten Verzeichnissen unverändert.

## Aktuelle Publikation

- **Recursive Epistemics / Rekursive Epistemik, Fassung 1.7 — current WIP**
- Viewer-Einstieg: `research/publications/2026-09-15_recursive-epistemics_v1.7/MANUSCRIPT.md`
- unmittelbarer Vorgänger: Fassung 1.6
- frozen empirical baseline: Fassung 1.5 / `EXP-EMP-20260913-A3`
- menschliches wissenschaftliches Review: ausstehend
- unabhängige Replikation: unvollständig
- automatische EVID-Promotion: deaktiviert

Stabile Links:

- `research/publications/CURRENT.md`
- `research/publications/FROZEN_V1.5.md`

## Dokumentgovernance

`docs/` und `research/` werden ab 1.7 als wissenschaftliche Informationsarchitektur behandelt. Jede reale Datei wird durch `scripts/audit_document_governance.py` nach Typ, Status, Autorität, Mutabilität, Zitierregel und Evidenzrolle klassifiziert. Hochautoritative Pfade besitzen explizite Overrides in `research/document_governance_overrides.json`.

Historische Dateien werden nicht bloß zur optischen Bereinigung verschoben, wenn dadurch Digests oder Reproduzierbarkeit beschädigt würden.

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

Stage 6 — Gedächtnis und Weltmodell.

Seit dem aktuellen `main` liegt mit `EXP-S6-SEM-CL-001` ein **positiver, präregistrierter Mechanismusbefund** zur semantischen Prototypkonsolidierung mit begrenztem Replay auf Split-MNIST vor. Gegenüber der gematchten Bedingung ohne semantischen Speicher stieg die finale mittlere Genauigkeit von 0,1883 auf 0,4093 (Δ +0,2210), während das mittlere Forgetting von 0,9764 auf 0,6975 sank (Reduktion 0,2789). Beide präregistrierten Primärkriterien bestanden; automatische EVID-Promotion bleibt deaktiviert und menschliches Review ist weiterhin erforderlich.

Der Befund ist bewusst eng begrenzt: Er isoliert einen Semantization-/Consolidation-Mechanismus mit spike-kodierter Repräsentation und einfachem Online-Readout. Er belegt weder eine Überlegenheit des vollständigen rekurrenten MHRN-SNN noch biologische Äquivalenz, Generalisierung über Split-MNIST, Neuheit des allgemeinen Semantization-Konzepts oder ein validiertes generatives Weltmodell.

Offen bleiben insbesondere:

- unabhängige Replikation von `EXP-S6-SEM-CL-001`,
- budget-gematchter Vergleich gegen Raw-Exemplar-Replay und etablierte Continual-Learning-Baselines,
- Replay- und Prototyp-Ablationen sowie schwierigere Benchmarks,
- end-to-end Prüfung mit dem rekurrenten MHRN-SNN,
- neuronale und abladierbare Prediction-Error-Dynamik,
- mehrschrittiges aktionskonditioniertes Weltmodell,
- gekoppelte Persistenz/Restore-Identität,
- confirmatory SNN-involved DATA,
- menschliche EVID-Entscheidung und unabhängige Replikation.

Die Draft-Präregistrierung `EXP-S6-SEM-VS-RAW-001` bleibt als separater Forschungsstrang offen und darf vor ihrer expliziten Ausführungsautorisierung nicht als Ergebnis oder EVID behandelt werden.

## Potenzielle Beiträge / Neuheitsstatus

Fassung 1.7 markiert drei Kandidaten für eine gezielte Prior-Art-Prüfung:

1. Logical Identity / Physical Slot / Synaptic Reduction / Execution Scheduling;
2. Proposal → Approval → Mutation → Journal → Undo;
3. Content Gateway / Compute Backend.

Dies sind dokumentierbare MHRN-Mechanismen beziehungsweise Architekturentscheidungen. Ihre externe wissenschaftliche Neuheit ist **nicht festgestellt**.

## Integrität

- `research/INTEGRITY_AND_ATTRIBUTION.md`
- `research/RELATED_WORK.md`
- `docs/05-quality/RESEARCH_INTEGRITY_GATE.md`
- `docs/00-governance/DOCUMENT_GOVERNANCE.md`
- `docs/08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md`

Diese Instrumente reduzieren Fehlattribution und unmarkiertes Text-Recycling. Sie zertifizieren keine Plagiatsfreiheit oder Neuheit; vor formaler externer Einreichung bleiben menschliche Quellenprüfung, Prior-Art-Prüfung und geeignete externe Similarity-Prüfung erforderlich.
