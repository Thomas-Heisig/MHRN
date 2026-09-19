# Current Scientific State

**Stand:** 18. September 2026

Dieses Dokument ist der kurze Einstieg in den aktuellen wissenschaftlichen Zustand. Historische DATA, EVID-Entscheidungen und eingefrorene Publikationen bleiben unverändert in ihren datierten Verzeichnissen.

Die Dashboard-Archivierung ist metadata-only: Einzelne Experimente und
Experimentreihen können aus der Arbeitsansicht ausgeblendet und wiederhergestellt
werden, ohne kanonische DATA-, Manifest- oder Workflow-Artefakte zu verschieben
oder wissenschaftlich umzuschreiben.

## Aktuelle Publikation

- **Recursive Epistemics / Rekursive Epistemik, Edition 1.8 — current WIP**
- Einstieg: `research/publications/2026-09-17_recursive-epistemics_v1.8/MANUSCRIPT.md`
- unmittelbarer Vorgänger: Edition 1.7
- frozen empirical baseline: Edition 1.5 / `EXP-EMP-20260913-A3`
- 1.8 nutzt die für 2.0 geplante elfteilige Struktur, ohne Softwareversion oder Evidenzstatus hochzustufen
- offene menschliche wissenschaftliche Reviews: `EXP-GEN-0041`,
  `EXP-S1-TOPO-V3-R1-20260918` und `EXP-S6-SEM-CL-003`
- CL-003 besitzt jetzt einen begrenzten Review-Kandidaten; die Entscheidung ist weiterhin `PENDING`
- unabhängige Replikation: unvollständig
- automatische EVID-Promotion: deaktiviert

## Forschungs- und Dokumentgovernance

`docs/` und `research/` werden durch `scripts/audit_document_governance.py` nach Typ, Status, Autorität, Mutabilität, Zitierregel und Evidenzrolle geprüft. Edition 1.8 ergänzt einen deterministischen Publikationsbuilder, vollständiges gepinntes Datei-/Abschnittsinventar, Research-Object-Projektionen, Creation-/Edition-/Experimentgenealogien, Vorgängerforschungs-Mapping und Quellenmetadaten. Diese Projektionen ersetzen keine Primärartefakte und zertifizieren keine semantische Vollständigkeit.

## Stage 0 — korrigierter wissenschaftlicher Reifestand

Die bisherige Scientific-Timeline-Projektion von 50 % war gegenüber dem aktuellen Repository veraltet. Für die Einzelzell-Konformität existieren inzwischen `RQ-EVAL-006` sowie die drei expliziten Hypothesen `H-EVAL-006-A/B/C`, ein vor der Ausführung eingefrorenes konfirmatorisches Protokoll (`PREREG-EVAL-006-V2`) und quellengebundene Confirmatory-DATA aus `EXP-STAGE0-20260916-MODEL-CONFORMANCE-V2`.

Der eng definierte `single_neuron_scientific_readiness`-Vertrag steht weiterhin auf **100 %**. Dieser Wert beschreibt nur die Erfüllung seines scoped Readiness-Vertrags. Für die breitere Scientific-Maturity-Timeline gelten zusätzlich Human-EVID und unabhängige Replikation. Nach dem kanonischen Gewichtungsmodell ergibt sich aktuell:

- RQ/H: **met** = 15 %;
- eingefrorenes Protokoll: **met** = 20 %;
- source-bound DATA: **met** = 20 %;
- Human-reviewed EVID: **met** = 20 % von 20 % (Human Review und kanonische EvidenceEngine-Promotion über `EVID-2026-18` abgeschlossen);
- externer Referenzvergleich / unabhängige Replikation: **partial** = 7,5 % von 15 %;
- Attribution: **met** = 10 %.

Die Human Review des scoped Claims ist inzwischen abgeschlossen und unterstützt die enge Konformitätsaussage. Eine EVID-Promotion wurde trotzdem **nicht** erzwungen: Der historische Stage-0-Lauf besitzt kein EvidenceEngine-kompatibles `manifest.json` mit aufgezeichneter Validity, Clean-Tree-Status, `provenance_digests` und `source_freeze_sha`. Diese fehlenden historischen Provenienzfelder werden nicht rückwirkend erfunden.

Damit beträgt die aktuelle **Gesamt-Scientific-Maturity von Stage 0 = 92,5 %**. Der historische V2-Lauf bleibt wegen seines alten Provenienzvertrags selbst nicht promotion-eligible; diese Lücke wurde jedoch prospektiv durch `EXP-STAGE0-20260918-MODEL-CONFORMANCE-V2-PROMO-R1` geschlossen. Nach dokumentiertem Human Review wurde der scoped Claim über den aktuellen EvidenceEngine-Pfad als `EVID-2026-18` registriert. Das 20-%-Kriterium `reviewed_evidence` steht damit auf `met`. Das unabhängige Replikationskriterium bleibt separat `partial` und trägt weiterhin nur 7,5 von 15 Prozentpunkten.

Die Human Review ist unter `research/experiments/EXP-STAGE0-20260916-MODEL-CONFORMANCE-V2/human_scientific_review.json` dokumentiert. Der separate Status `EVIDENCE_PROMOTION_STATUS.json` hält fest, dass der Review den scoped Claim unterstützt, die EVID-Promotion wegen der fehlenden historischen EvidenceEngine-Provenienz aber blockiert bleibt. Weder Review noch spätere Promotion dürfen biologische Gleichwertigkeit oder unabhängige Replikation erzeugen.

Diese formale Provenienzlücke wurde inzwischen **prospektiv** adressiert, nicht rückwirkend repariert: `EXP-STAGE0-20260918-MODEL-CONFORMANCE-V2-PROMO-R1` wurde unter `PREREG-EVAL-006-V2-PROMO-R1` mit den vorab deklarierten neuen Seeds `22001–22003` ausgeführt. Der wissenschaftliche Lauf am Freeze-Commit `0376142b16a092c674653ee61c10d8137671eacf` war clean-tree, `validity.valid=true`, ohne Runtime-/Fatal-Fehler und mit vollständigen `provenance_digests` sowie `source_freeze_sha=36764dde292a3934523b21c5d9559319a0d8c9a8763c9ab3dc1c5cbbc246e850`. Alle drei eingefrorenen Hypothesenbedingungen bestanden; der maximale Izhikevich-Lokalfehler betrug `4.5474735088646412e-13`, der maximale LIF-Fehler `7.1054273576010019e-15`.

Der Promotion-Lauf selbst bleibt als ausgeführte DATA unverändert; seine automatische Promotion ist weiterhin deaktiviert. Der Human Review durch Thomas Heisig vom 18.09.2026 wurde zusätzlich in das vom EvidenceEngine verlangte kanonische `human_review.json` abgebildet. Die anschließende getrennte Promotion erzeugte `EVID-2026-18` für `CLAIM-EVAL-006`. Diese Registrierung ändert weder die historische V1-Negativspur noch die Unabhängigkeitsgrenze: `independent_authorship_replication=false` bleibt bestehen.

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

## Aktuelle Review- und Replikationslage

### Determinismus / `RQ-DET-001`

Der historische Lauf `EXP-BATCH-20260914074039-03` ist nach dem aktuellen semantischen Vertrag ein direkter Test von `RQ-DET-001 / H-SNN-003-A`. Für drei Seeds stimmen die A/B-Replikapaare innerhalb von `recurrence_off` und `recurrence_on` in den registrierten Antwortgrößen überein. Der Befund ist damit ein positiver Same-Seed-Determinismusbefund **innerhalb dieses kleinen Protokolls**.

Er bleibt dennoch **nicht EVID**, weil der historische Lauf mit `git dirty: true` erzeugt wurde. Die semantische Korrektur heilt keine Provenienzlücke. Der nächste wissenschaftlich saubere Schritt ist deshalb ein clean-tree, hash-gebundener Replikationslauf mit denselben vorab fixierten Bedingungen und anschließender Human-EVID-Entscheidung.

Zusätzlich gilt die AIRR-Regel: Bei semantischem `MISMATCH` wird öffentliches/report-level `ai_confidence` deterministisch auf `0.0` gesetzt; der ursprüngliche Modellwert bleibt nur im append-only Auditpfad erhalten. AIRR bleibt Interpretation, nicht Evidenzinstanz.

### Topologie / `H-SNN-003-B`

`EXP-GEN-0047` bleibt als methodisch wichtiger Vorgänger erhalten: technisch reproduzierbar und semantisch `DIRECT_MATCH`, aber wegen drei Neuronen, zwei Feed-forward-Synapsen und fehlender kausaler Geometrie-zu-Graph-Kopplung `INADEQUATE_TO_TEST_HYPOTHESIS`. Die damaligen identischen Resultate über 1D/2D/3D/5D sind deshalb weder Topologie-Nullbefund noch Widerlegung eines 5D-Effekts.

Der nachfolgende, vor Ausführung präregistrierte Lauf `EXP-S1-TOPO-V2-20260918` / `topology_propagation_v2` adressiert **`RQ-SNN-003 / H-SNN-003-B` als Stage-1-Topologiefrage**, nicht die stärkere dimensionsspezifische 5D-Hypothese. Das Design verwendet 64 Neuronen und 246 Kanten je Evaluationsbedingung, identische Gewichte/Delays/Stimulation, sechs vorab definierte Topologien, getrennte Kalibrier- und Evaluations-Seeds sowie ein Activity-Adequacy-Gate. Das Gate bestand bereits bei Synapsengewicht 55.0; anschließend wurden 120 Evaluationsläufe über 20 gepaarte Seeds ausgeführt. Designintegrität und deterministische lokale Neuberechnung bestanden.

Unter diesem eingefrorenen Regime wurden präregistrierte Unterschiede in `active_fraction` und/oder `first_output_latency_censored` zwischen mehreren Topologiepaaren beobachtet; die Holm-korrigierten exakten gepaarten Sign-Tests tragen die primäre Inferenz. Die deterministischen Bootstrap-95%-Intervalle beschreiben die gepaarten Medianunterschiede zusätzlich, sind bei vollständig identischen gepaarten Differenzen aber erwartungsgemäß degeneriert und daher kein eigenständiger zusätzlicher Evidenzbeitrag.

Für `active_fraction` liegt eine klare **Messbereichsgrenze im getesteten Regime** vor: 1d, 2d und 3d erreichen in der Evaluation jeweils eine Median-Aktivierungsfraktion von 1,0; die Kontraste 1d→2d und 2d→3d besitzen deshalb Median-Differenz 0, Bootstrap-CI [0,0] und Sign-Test p=1. Das ist kein belastbarer Nachweis der Gleichheit dieser Topologien, sondern zeigt, dass dieser Endpunkt bei den drei Bedingungen im gewählten Stimulus-/Gewichtsregime sättigt. Die diskriminierende Information von `active_fraction` beginnt erst bei den Kontrasten zu 5d beziehungsweise innerhalb der 5d-/Kontrollfamilie.

Der Name `first_output_latency_censored` darf nicht als tatsächliche Zensierung der beobachteten 1d-Latenzen missverstanden werden. Das Präregistrat setzt ein Evaluationsfenster von 128 Ticks; nur ein vollständig ausbleibender Output wird mit dem Sentinel `129 = ticks + 1` kodiert. Die gespeicherten Evaluationsdaten enthalten keine solche Sentinel-Kodierung. Der 1d-Median von 19 Ticks ist daher ein beobachteter, nicht zensierter Wert. Die Latenzkontraste tragen in diesem Datensatz den breiteren und über alle fünf Primärkontraste konsistenten Unterschied.

Alle sechs Bedingungen besitzen dasselbe globale Kantenbudget von 246. Unterschiede zwischen 1d/2d/3d/5d/`5d_shuffled`/`random_graph` sind deshalb **keine simple Dichte- oder Sparsity-Differenz**, sondern entstehen aus der unterschiedlichen Anordnung der gematchten Kanten unter den jeweiligen Konstruktionsregeln. Der zulässige Befund bleibt eng: **Die konkrete Netzwerktopologie beeinflusst in diesem kontrollierten 64-Neuronen-Regime die Propagationsdynamik.** Der Laufstatus lautet `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`; die begrenzte Interpretation ist human-reviewed akzeptiert, bleibt aber DATA und erzeugt keine automatische EVID-Promotion.

Die anschließende interne Replikationslinie wurde bewusst als neue DATA erzeugt. `EXP-S1-TOPO-V3-20260918` führte zwar erfolgreich 120 Läufe aus und zeigte bereits dieselbe Richtung, musste aber für die konfirmatorische Interpretation verworfen werden, weil der Runner die Holm-Korrektur fälschlich in zwei Familien zu je fünf Tests statt in der präregistrierten einen Familie von zehn zeitaufgelösten Primärtests anwendete. Die Rohdaten und Originalstatistik bleiben unverändert als Auditspur erhalten.

Die korrigierte Neuausführung `EXP-S1-TOPO-V3-R1-20260918` verwendet neue Seeds 6201–6220 und hält 64 Neuronen, 246 Kanten, Synapsengewicht 55.0, Stimulus und 128-Tick-Fenster konstant. Die eine Holm-Familie über alle zehn Primärtests ist nun korrekt implementiert und deterministisch verifiziert. Beide vorab definierten Ceiling-Resolution-Kriterien bestehen: `activation_auc_0_32` trennt 1d→2d mit Median-Δ +4,4140625 (CI95 [4,3671875; 4,4296875], Holm-p ≈ 1,91×10^-5) und 2d→3d mit +1,4609375 (CI95 [1,3671875; 1,4921875], Holm-p ≈ 1,91×10^-5). Die Halbaktivierungslatenz fällt entsprechend von Median 10 auf 6 auf 4 Ticks; die beiden low-dimensionalen Kontraste sind signifikant. Damit ist gezeigt, dass die terminale `active_fraction=1.0`-Sättigung von V2 die zeitliche Propagationsdynamik zwischen 1d/2d/3d verdeckte, nicht dass diese Topologien dynamisch gleich waren.

Zusätzlich repliziert R1 alle fünf V2-Kontraste der `first_output_latency_censored` auf neuen Seeds mit derselben negativen right-minus-left-Richtung und Holm-korrigierter Signifikanz. Die Median-Latenzen bleiben 19, 9, 6, 5, 2 und 2 Ticks für 1d, 2d, 3d, 5d, `5d_shuffled` und `random_graph`. Der zulässige Status lautet deshalb `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL` auf DATA-Ebene. Dies ist eine **interne Replikation innerhalb derselben Code-/Modellfamilie**, keine unabhängige externe Replikation und keine EVID-Promotion.

Davon getrennt bleibt `RQ-5D-005 / H-5D-005-A` offen/untested. Für einen dimensionsspezifischen 5D-Claim gelten weiterhin die stärkeren Mindestanforderungen von mindestens 1.000 Neuronen pro Bedingung, im Mittel mindestens 10 eingehenden Synapsen, explizit distanzabhängiger Konnektivität, degree-/density-matched Kontrollen, Multi-Neuron-Stimulus, unabhängigen Seeds und sauberer Source-/Graph-Provenienz. Dass `5d_shuffled` und `random_graph` im Stage-1-Lauf teils frühere Output-Latenzen zeigten, unterstreicht gerade, dass aus `H-SNN-003-B` **keine 5D-Überlegenheit** abgeleitet werden darf.

### Stage-6-Kompressionshypothese — nächster vorbereiteter empirischer Schritt

`LP-20260917194217 / OBJ-MEM-COMPRESSION-001` ist human-origin, genehmigt und weiterhin **proposal-only**. Es wurde nicht ausgeführt und besitzt keine Runtime-Autorität. Die neue Frage prüft **Kompression, nicht allgemeine Lernleistung**: `semantic_prototype_replay_10pct_budget` soll bei einem Zehntel des Speicherbudgets mindestens 95 % der Retention von `raw_replay_full_budget` erreichen. Kontrollen sind `no_replay`, `random_prototype_10pct` und `learning_off`.

Die vorab festzulegende Rollenentscheidung lautet: Erfolg stützt eine begrenzte Kompressionsrolle von SemanticMemory unter diesem Protokoll; Misserfolg stützt diese Rolle nicht. Generalisierung, Langzeitgedächtnis und Weltmodell-Brücke bleiben davon getrennte spätere Hypothesen und dürfen den Kompressionstest nicht post hoc retten.

Das historisch genehmigte `LP-20260917194217` bleibt unverändert: seine ursprüngliche Genehmigung enthält noch den damaligen Source-Platzhalter und darf nicht nachträglich umgeschrieben werden. Die Quellprovenienz ist stattdessen in der neuen Proposal-Revision `LP-20260917194217-R1` konkret gebunden: `CL-002-EVID` verweist auf das human-reviewte `EVID.json` mit SHA-256 `c7b1124256fd8018839a8c5c29b30493b68d16bc223d0a3258bcbaca55b1752e`; `CL-003-DATA` verweist auf `results.json` mit SHA-256 `4e74021c0ef838371a3a01061ae1c2dcebb2031b54c15c6169e38c1972d06290`. Beide Sources stehen dort auf `VERIFIED`. Weil sich der Proposal-Inhalt geändert hat, ist R1 **nicht durch die historische Approval gedeckt und benötigt eine neue explizite menschliche Genehmigung**. Vor einer Ausführung bleiben zusätzlich Seed-/Taskplan, Analysevertrag, Ausführungsautorisation und Freeze vollständig zu binden. Approval ist keine Ausführung, DATA oder EVID.

Der nächste methodische Schritt ist die Präregistrierungsvorbereitung von R1. Vor einem `FROZEN`-Status sind kanonische RQ/H-Zuordnung, Speicherbudget-Definition, Seed-/Taskplan, Retentionsaggregation, Äquivalenz-/Inferenzregel, Ausschluss-/Failure-Regeln, Analysevertrag und Source-/Config-Hashes zu binden; R1-Human-Approval und Ausführungsautorisation bleiben separate Gates.

### Methodische Gesamtfolge

Die jüngsten Reviews machen eine für MHRN zentrale Trennung verbindlich:

`semantischer Match ≠ technische Reproduzierbarkeit ≠ Testadäquanz ≠ Provenienz ≠ EVID`.

Ein Experiment kann korrekt registriert und technisch reproduzierbar sein und dennoch die Zielhypothese nicht beantworten. Umgekehrt kann ein positiver technischer Befund wegen mangelhafter Provenienz von einer Evidenzpromotion ausgeschlossen bleiben. Diese Trennung ist inzwischen Teil des kanonischen Forschungsprozesses.

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
