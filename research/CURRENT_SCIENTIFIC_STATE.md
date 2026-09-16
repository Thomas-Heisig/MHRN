# Current Scientific State

**Stand:** 16. September 2026

Dieses Dokument ist der kurze Einstieg in den aktuellen wissenschaftlichen Zustand des Repositories. Historische DATA, EVID-Entscheidungen und eingefrorene Publikationsstände bleiben in ihren datierten Verzeichnissen unverändert.

## Aktuelle Publikation

- **Recursive Epistemics / Rekursive Epistemik, Fassung 1.7 — current WIP**
- Einstieg: `research/publications/2026-09-15_recursive-epistemics_v1.7/MANUSCRIPT.md`
- unmittelbarer Vorgänger: Fassung 1.6
- frozen empirical baseline: Fassung 1.5 / `EXP-EMP-20260913-A3`
- menschliches wissenschaftliches Review: für CL-003 ausstehend
- unabhängige Replikation: unvollständig
- automatische EVID-Promotion: deaktiviert

## Dokumentgovernance

Ab Fassung 1.7 werden `docs/` und `research/` durch `scripts/audit_document_governance.py` nach Typ, Status, Autorität, Mutabilität, Zitierregel und Evidenzrolle geprüft. Engineering-Reife bleibt von wissenschaftlicher Evidenz getrennt.

## Aktueller Schwerpunkt

Stage 6 — Gedächtnis und Weltmodell.

### Semantization / Continual Learning

- `EXP-S6-SEM-CL-001`: positiver präregistrierter Mechanismusbefund gegenüber einer naiven Online-Baseline ohne Replay unter seinem eigenen eingefrorenen Protokoll.
- `EXP-S6-SEM-CL-002`: präregistrierter, vollständig gepaarter Negativbefund für die spezifischere Hypothese eines Vorteils semantischer Prototypen gegenüber gleich objekt- und updatebudgetiertem Raw-Replay. Die menschliche Projekt-EVID klassifiziert H1 unter diesem Protokoll als falsifiziert.
- CL-002 beweist nicht rückwirkend, dass CL-001 ausschließlich durch Replay erklärt wird, weil die Replay- und Updateregime beider Experimente verschieden sind. Belastbar ist: Ein spezifischer Vorteil semantischer Verdichtung gegenüber Raw-Replay wurde unter CL-002 nicht nachgewiesen.
- `EXP-S6-SEM-CL-003`: am 16. September 2026 genau einmal als autorisierte, freeze- und hash-gebundene Kampagne mit 84 Runs = 12 Seeds × 7 Bedingungen ausgeführt. Die Runner-Klassifikation lautet `H1_negative_H2_negative`.
- In CL-003 bestehen C1, C2 und C4 die präregistrierten Erfolgsregeln nicht. C3 (`S20 − X20`) besteht mit rund +14,9 Prozentpunkten und zeigt auf DATA-Ebene relevante, nicht-zufällige Struktur in der semantischen Repräsentation. Daraus folgt kein bestätigter Vorteil gegenüber Raw-Replay.
- Der deskriptive Semantic-minus-Raw-Trend über 5 %, 20 % und 40 % Replay-Dosis wird nicht als bestätigter Dosis-Effekt interpretiert, weil C4 negativ bleibt.

Die aktuelle DATA-only-Zwischenbilanz lautet deshalb:

> Unter den bisher untersuchten Bedingungen liegt der nachweisbare Beitrag primär im Replay. Die semantische Verdichtung erhält relevante Struktur, zeigt aber bislang keinen präregistriert bestätigten Zusatznutzen gegenüber gematchtem Raw-Replay.

Für CL-003 gilt weiterhin strikt: **DATA, nicht EVID**, bis die Human Review abgeschlossen ist. Die ausführliche Bilanz steht unter `research/publications/2026-09-15_recursive-epistemics_v1.7/STAGE6_CL001_CL003_BALANCE.md`.

### Entscheidungsgate für SemanticMemory

Aus CL-003 folgt kein automatisches CL-004. Nach der Human Review muss zuerst eine explizite Forschungs- und Architekturentscheidung fallen:

- **A:** `SemanticMemory` auf eine spezialisierte Nebenrolle reduzieren; Raw-Replay bleibt Referenz; keine weitere Semantikprüfung.
- **B:** genau **eine** alternative Rolle in genau **einem** neuen, präregistrierten konfirmatorischen Experiment prüfen; bei negativem Ergebnis folgt A.
- **C:** Rollenfrage parken und zunächst andere Stage-6-Mechanismen wie kausalen Prediction Error und World Model untersuchen.

Kompression, Generalisierung, Skalierung und Langzeitgedächtnis werden ausdrücklich **nicht** als automatische Experimentwarteschlange geführt. Eine serielle Rettung des Mechanismus durch jeweils neue Rollenannahmen ist nicht zulässig.

Bis zu einer anderslautenden reviewten Evidenzentscheidung ist `SemanticMemory` ein technisch funktionsfähiger, hinsichtlich eines zusätzlichen Kernnutzens aber nicht abschließend gerechtfertigter Mechanismuskandidat. Für den untersuchten Continual-Learning-Teil von Stage 6 ist Raw-Replay die kanonische Referenz.

Offen bleiben insbesondere:

- Human Review und EVID-Entscheidung zu CL-003,
- anschließende Wahl A/B/C für die Rollenfrage von `SemanticMemory`,
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
