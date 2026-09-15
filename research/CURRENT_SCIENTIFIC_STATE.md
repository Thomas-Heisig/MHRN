# Current Scientific State

**Stand:** 15. September 2026

Dieses Dokument ist der kurze Einstieg in den aktuellen wissenschaftlichen Zustand des Repositories. Historische DATA, EVID-Entscheidungen und eingefrorene Publikationsstände bleiben in ihren datierten Verzeichnissen unverändert.

## Aktuelle Publikation

- **Recursive Epistemics / Rekursive Epistemik, Fassung 1.7 — current WIP**
- Einstieg: `research/publications/2026-09-15_recursive-epistemics_v1.7/MANUSCRIPT.md`
- unmittelbarer Vorgänger: Fassung 1.6
- frozen empirical baseline: Fassung 1.5 / `EXP-EMP-20260913-A3`
- menschliches wissenschaftliches Review: ausstehend
- unabhängige Replikation: unvollständig
- automatische EVID-Promotion: deaktiviert

## Dokumentgovernance

Ab Fassung 1.7 werden `docs/` und `research/` durch `scripts/audit_document_governance.py` nach Typ, Status, Autorität, Mutabilität, Zitierregel und Evidenzrolle geprüft. Engineering-Reife bleibt von wissenschaftlicher Evidenz getrennt.

## Aktueller Schwerpunkt

Stage 6 — Gedächtnis und Weltmodell.

### Semantization / Continual Learning

- `EXP-S6-SEM-CL-001`: positiver präregistrierter Mechanismusbefund gegenüber einer naiven Online-Baseline ohne Replay unter seinem eigenen eingefrorenen Protokoll.
- `EXP-S6-SEM-CL-002`: präregistrierter, vollständig gepaarter Negativbefund für die spezifischere Hypothese eines Vorteils semantischer Prototypen gegenüber gleich objekt- und updatebudgetiertem Raw-Replay. Alle drei konjunktiven Erfolgskriterien verfehlten die vorab festgelegten Mindestwirkungen; H1 gilt unter diesem Protokoll als falsifiziert.
- Der kleine B3-vs-B4-Accuracy-Unterschied in CL-002 lag bei rund 0,18 Prozentpunkten und damit weit unter der präregistrierten Mindestwirkung von 3 Prozentpunkten. Er ist deshalb kein positiver konfirmatorischer Semantikbefund.
- CL-002 beweist nicht rückwirkend, dass CL-001 ausschließlich durch Replay erklärt wird, weil die Replay- und Updateregime beider Experimente verschieden sind. Belastbar ist derzeit nur: Ein spezifischer Vorteil semantischer Verdichtung gegenüber Raw-Replay ist nicht nachgewiesen.
- `EXP-S6-SEM-CL-003`: Runner, Freeze-Manifest und Dose-Response-Vorbereitung sind in `main` integriert. Das ist ein präparativer Stand, keine Experimentausführung und keine neue EVID.

CL-002-DATA liegen unter `research/experiments/EXP-S6-SEM-CL-002/results/`; die menschliche Projektinterpretation liegt unter `research/experiments/EXP-S6-SEM-CL-002/EVID.md` und `EVID.json`.

Offen bleiben insbesondere:

- Replikation und Dosis-/Budget-Ablation ohne post-hoc Änderung von CL-002,
- kontrollierte Ausführung und Auswertung von CL-003 erst nach den vorgesehenen Freigaben,
- neuronale und abladierbare Prediction-Error-Dynamik,
- mehrschrittiges aktionskonditioniertes Weltmodell,
- gekoppelte Persistenz/Restore-Identität,
- Vergleich gegen einen echten Standard-SNN-Continual-Learning-Baseline-Stack,
- end-to-end Prüfung mit dem rekurrenten MHRN-SNN,
- unabhängige externe Replikation.

## Potenzielle Beiträge / Neuheitsstatus

Fassung 1.7 führt drei Kandidaten für gezielte Prior-Art-Prüfung:

1. Logical Identity / Physical Slot / Synaptic Reduction / Execution Scheduling;
2. Proposal → Approval → Mutation → Journal → Undo;
3. Content Gateway / Compute Backend.

Dies sind dokumentierte MHRN-Mechanismen beziehungsweise Architekturentscheidungen. Ihre externe wissenschaftliche Neuheit ist nicht festgestellt.

## Integrität

- `research/INTEGRITY_AND_ATTRIBUTION.md`
- `research/RELATED_WORK.md`
- `docs/05-quality/RESEARCH_INTEGRITY_GATE.md`
- `docs/00-governance/DOCUMENT_GOVERNANCE.md`
- `docs/08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md`

Vor formaler externer Einreichung bleiben menschliche Quellenprüfung, Prior-Art-Prüfung und geeignete externe Similarity-Prüfung erforderlich.
