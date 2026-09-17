# Current Scientific State

**Stand:** 17. September 2026

Dieses Dokument ist der kurze Einstieg in den aktuellen wissenschaftlichen Zustand. Historische DATA, EVID-Entscheidungen und eingefrorene Publikationen bleiben unverändert in ihren datierten Verzeichnissen.

## Aktuelle Publikation

- **Recursive Epistemics / Rekursive Epistemik, Edition 1.8 — current WIP**
- Einstieg: `research/publications/2026-09-17_recursive-epistemics_v1.8/MANUSCRIPT.md`
- unmittelbarer Vorgänger: Edition 1.7
- frozen empirical baseline: Edition 1.5 / `EXP-EMP-20260913-A3`
- 1.8 nutzt die für 2.0 geplante elfteilige Struktur, ohne Softwareversion oder Evidenzstatus hochzustufen
- menschliches wissenschaftliches Review: für CL-003 ausstehend
- unabhängige Replikation: unvollständig
- automatische EVID-Promotion: deaktiviert

## Forschungs- und Dokumentgovernance

`docs/` und `research/` werden durch `scripts/audit_document_governance.py` nach Typ, Status, Autorität, Mutabilität, Zitierregel und Evidenzrolle geprüft. Edition 1.8 ergänzt einen deterministischen Publikationsbuilder, vollständiges gepinntes Datei-/Abschnittsinventar, Research-Object-Projektionen, Creation-/Edition-/Experimentgenealogien, Vorgängerforschungs-Mapping und Quellenmetadaten. Diese Projektionen ersetzen keine Primärartefakte und zertifizieren keine semantische Vollständigkeit.

## Aktueller Schwerpunkt: Stage 6

### Semantization / Continual Learning

- `EXP-S6-SEM-CL-001`: positiver Mechanismusbefund gegenüber No-Replay unter seinem eingefrorenen Protokoll.
- `EXP-S6-SEM-CL-002`: kein bestätigter Vorteil semantischer Prototypen gegenüber gematchtem Raw-Replay; H1 wurde unter diesem Protokoll in der menschlichen Projekt-EVID als falsifiziert klassifiziert.
- `EXP-S6-SEM-CL-003`: genau einmal autorisierte, freeze- und hash-gebundene Kampagne mit 84 Runs = 12 Seeds × 7 Bedingungen; Runner-Klassifikation `H1_negative_H2_negative`.
- C1, C2 und C4 erfüllen die präregistrierten Erfolgsregeln nicht. C3 (`S20 − X20`) ist positiv und zeigt relevante nicht-zufällige Struktur, aber keinen bestätigten Vorteil gegenüber Raw-Replay.

Die aktuelle DATA-only-Zwischenbilanz lautet:

> Unter den bisher untersuchten Bedingungen liegt der nachweisbare Beitrag primär im Replay. Die semantische Verdichtung erhält relevante Struktur, zeigt aber bislang keinen präregistriert bestätigten Zusatznutzen gegenüber gematchtem Raw-Replay.

CL-003 bleibt **DATA, nicht EVID**, bis die Human Review abgeschlossen ist. Die historische Detailbilanz bleibt unter `research/publications/2026-09-15_recursive-epistemics_v1.7/STAGE6_CL001_CL003_BALANCE.md` erreichbar und wird von 1.8 nicht umgeschrieben.

### Entscheidungsgate für SemanticMemory

Aus CL-003 folgt kein automatisches CL-004. Nach Human Review gilt weiterhin:

- **A:** spezialisierte Nebenrolle; Raw-Replay bleibt Referenz; keine weitere Semantikprüfung.
- **B:** genau eine theoretisch begründete alternative Rolle in genau einem neuen präregistrierten konfirmatorischen Experiment; bei negativem Ergebnis folgt A.
- **C:** Rollenfrage parken, bis Prediction Error oder World Model eine konkrete funktionale Notwendigkeit erzeugen.

Eine serielle Rettung durch immer neue Rollenannahmen ist nicht zulässig.

## Weitere priorisierte Forschung

- Stage 0: Modell-/Integrator-/Parameterkonformität und externe Referenzreplikation.
- Stages 2/3: Rekurrenz, Störungsrobustheit, held-out Plastizität, Langzeit-/Ressourcenstabilität.
- Stage 4: modality-specific vs. general controls, Cross-Modal-Transfer, Läsion/Shuffle/Frozen.
- Stage 5: Closed Loop, Real Device, Sensor Loss und Actuator No Effect unter Safety-Gates.
- Stage 6: neuronaler Prediction Error, Mehrschritt-/action-conditioned World Model, decision benefit.
- Spiegel-/Handlungsprädiktion: Stage-4/5/6-Querschnitt; Stage 7 erst bei kausaler Self/Other-Differenzierung.
- 5D: gematchte Dimensions-/Geometrieablation; keine etablierte Überlegenheit.
- biophysikalische Detailmodelle: nur als fragegetriebene Varianten/Ablationen.
- Safety: Zielprovenienz, Misgeneralization, Corrigibility, Interruptibility, Specification Gaming und Post-Objective Transition.
- Prior Art, unabhängige Replikation und externer Quellen-/Similarity-Audit.

## Potenzielle Beiträge / Neuheitsstatus

Edition 1.8 behandelt unter anderem folgende Punkte als **Kandidaten**, nicht als bewiesene Neuheit:

1. Logical Identity / Physical Slot / Synaptic Reduction / Execution Scheduling;
2. Proposal → Approval → Mutation → Journal → Undo;
3. Content Gateway / Compute Backend;
4. source-bound DATA/EVID-Grenzen;
5. rekursive Epistemik als explizit provenance- und gatewayorientierte Verbindung von Forschungsobjekt und Forschungsprozess.

Die externe wissenschaftliche Neuheit bleibt `requires_prior_art_review`.

## Integrität

- `research/publications/2026-09-17_recursive-epistemics_v1.8/REFERENCES.md`
- `research/publications/2026-09-17_recursive-epistemics_v1.8/EXTENDING.md`
- `research/INTEGRITY_AND_ATTRIBUTION.md`
- `research/RELATED_WORK.md`
- `docs/05-quality/RESEARCH_INTEGRITY_GATE.md`
- `docs/00-governance/DOCUMENT_GOVERNANCE.md`

Vor formaler externer Einreichung bleiben menschliche Quellenprüfung, systematische Prior-Art-Prüfung, externe Similarity-Prüfung und fachliche Review erforderlich.
