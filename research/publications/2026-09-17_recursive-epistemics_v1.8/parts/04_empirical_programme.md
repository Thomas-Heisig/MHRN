# Teil IV — Empirisches Forschungsprogramm

## 14. Verbindlicher Forschungszyklus

Das empirische Programm folgt dem Zyklus `RQ → H → benötigte Fähigkeit → minimale Implementierung → technische Validierung → Präregistrierung/Freeze → autorisierte Ausführung → DATA → präregistrierte Analyse → Human Review → EVID → begrenzter Claim → Folgefrage`. RQ-Status, Hypothesenstatus, DATA, EVID und Claim-Status sind unterschiedliche Zustandsräume.

Edition 1.8 erzeugt deshalb aus einem Run niemals automatisch Evidenz. Der Publikationsbuilder liest Register und Ergebnisse, darf aber keine Experimente starten und keine EVID-Entscheidung schreiben. Diese Trennung ist technisch prüfbar und soll verhindern, dass ein komfortabler Viewer oder Runner wissenschaftliche Autorität vortäuscht.

## 15. Experimentfamilien

Das historische Brain-5D-Framework enthielt bereits thematische Familien für Geometrie, Stabilität, Plastizität, Gedächtnis, Continual Learning, Language Organ/Knowledge Intake, Embodiment, Emergenz, Storage/Twin-Fidelity und Scaling. Edition 1.8 erhält diese Forschungsräume, ersetzt ihre alten Kurzkennungen aber nicht rückwirkend durch neue IDs. Die kanonischen aktuellen RQs und Hypothesen werden unverändert aus `research/registry/` projiziert.

Für jede Familie gelten Kontrollen, die den jeweils plausibelsten Confound adressieren: dimensionsgematchte Nullmodelle für Geometrie; recurrence-on/off und topology controls für Netzwerke; learning-on/off, Frozen, Sham und Shuffle für Plastizität; Retrieval-off und state-permuted Bedingungen für Gedächtnis; Open-/Closed-loop sowie sensor-loss/no-effect für Embodiment; action-conditioned und corrupted-model Kontrollen für Weltmodelle.

## 16. Statistik und experimentelle Einheit

Viele Ticks oder Spikes sind keine unabhängigen Stichproben. Für zahlreiche Vergleiche ist der unabhängig initialisierte Seed beziehungsweise Lauf die experimentelle Einheit; Zeitfenster desselben Laufs sind wiederholte Messungen. Vor einem konfirmatorischen Lauf werden Primärendpunkte, Kontraste, Seeds, Ausschlusskriterien, Testfamilie und Erfolgsregel eingefroren. Explorative Nachanalysen sind zulässig, müssen aber als explorativ markiert werden.

## 17. Negative und Nullbefunde

Ein negatives Ergebnis ist kein defektes Experiment, wenn Protokoll, Instrumentierung und Ausführung valide sind. Es begrenzt den Hypothesenraum. CL-002 und CL-003 zeigen diese Regel exemplarisch: Die semantische Verdichtung erhält Struktur, aber ihre behauptete Mehrleistung gegenüber gematchtem Raw-Replay wurde unter den geprüften Protokollen nicht präregistriert bestätigt. CL-003 bleibt bis Human Review **DATA**, nicht EVID.

## 18. Spiegelmechanismen und Handlungsvorhersage

Die Arbeit zu Spiegelmechanismen wird als Stage-6-naher Forschungsstrang integriert. Der prüfbare Kern ist nicht das Etikett „Spiegelneuron“, sondern die Frage, ob Beobachtungs- und Ausführungsrepräsentationen partiell überlappen, ob Kontext und Zielrelevanz diese Überlappung modulieren und ob ein Prediction-Error-Mechanismus einen kausalen Zusatznutzen liefert. Stage 4 liefert sensorische Pfade, Stage 5 Eigenaktionen/Outcome, Stage 6 Vorhersage; Stage 7 Selbst/Fremd-Unterscheidung ist erst nach eigener Kausalprüfung zulässig.

## 19. Replikation

Interne Multi-Seed-Wiederholung ist wichtig, ersetzt aber keine unabhängige Replikation. Replikation muss Code-/Umgebungsprovenienz, unabhängige Ausführung und ein vorher definiertes Vergleichskriterium besitzen. Scientific Maturity darf deshalb auch bei technisch grünem System unter 100 % bleiben.

## 19.1 Historische Experimentlinie und was sie tatsächlich geleistet hat

Die empirische Arbeit von MHRN ist nicht erst mit CL-001 begonnen. Die Vorgängerfassungen und Supplements enthalten eine längere Sequenz von Verifikation, Diagnose, Ablation und konfirmatorisch angelegten Experimenten. Für Edition 1.8 werden diese Ergebnisse in einer gemeinsamen Leselogik zusammengeführt.

### Einzelzelle: von Softwaretest zu externer Referenzkonformität

Der frühere Einzelzellstand bestand zunächst vor allem aus deterministischen Softwareverträgen. Die V2-Konformitätskampagne verschob die Frage auf einen stärkeren Prüfpunkt: Stimmen lokale Übergänge, Schwellen- und Resetsemantik mit einer externen Referenzimplementierung überein? Die Antwort war für den eingefrorenen Umfang positiv. Gleichzeitig blieb der ältere freie 1000-Tick-Izhikevich-Negativbefund erhalten. Daraus folgt eine methodische Erkenntnis: Ein Referenzvergleich muss explizit sagen, ob lokale Gleichungssemantik oder globale freie Trajektorie geprüft wird.

### Science Suite / EXP-GEN-0036: Diagnose statt pauschaler Fachbeweis

`EXP-GEN-0036` führte 180 Runs über zehn Seeds aus und deckte sieben Protokollgruppen ab: `ping`, `temporal`, `stdp`, `learning`, `time`, `5d` und `regulation`. Der wichtigste Erkenntnisgewinn lag nicht in einer einzigen Fachhypothese, sondern in der Trennung von **Artefaktvollständigkeit**, **interner Konsistenz** und **fachlicher Testadäquanz**.

Die erste automatische Zusammenfassung ließ bei mehreren Bedingungen leere SNN-Spalten erscheinen. Die Human Review zeigte, dass diese Bedingungen nicht fehlten; ihre Metriken waren nur anderer Art. Damit wurde ein Reporting-/AIRR-Fehler identifiziert und die falsche Missing-DATA-Interpretation korrigiert. Für die Forschungsgovernance ist dies bedeutsam: Berichtsprojektion ist ein eigener Fehlerkanal und darf nicht mit fehlender Ausführung gleichgesetzt werden.

Für `PING` zeigte sich ein klarer mechanistischer Recurrence-Effekt im kleinen kontrollierten Netz. Für die 5D-Teilstudie ergab die Review dagegen **NOT TESTED**: Die Koordinaten wurden variiert, die Dynamik war aber nicht ausreichend geometrieabhängig konstruiert. Das Experiment war damit für den behaupteten Geometrieeffekt nicht sensitiv genug. Ein solcher Befund ist methodisch stärker als ein falsch formulierter Nullbefund, weil er die nächste Präregistrierung konkret verbessert.

### EXP-GEN-0045/0046: Reproduzierbarkeit wird selbst zum Forschungsobjekt

Die nach der ersten 1.8-Synthese hinzugekommenen Experimente `EXP-GEN-0045` und `EXP-GEN-0046` verschieben Determinismus von einer allgemeinen Engineeringannahme zu einer explizit gespeicherten DATA-Frage. EXP-GEN-0045 prüft Same-Seed-Tonic-Replikapaare; drei von drei getesteten Seeds erzeugten identische Spike-Sequenzen. EXP-GEN-0046 prüft vier Recurrence-Bedingungen mit jeweils paarigen Replikaten und drei Seeds, insgesamt zwölf Runs bei 256 Ticks. Die jeweiligen Replica-Paare reproduzieren dieselben deskriptiven Netzwerkmetriken.

Der Erkenntniswert liegt auf zwei Ebenen. Erstens wird die technische Reproduzierbarkeit der untersuchten kleinen SNN-Trajektorien konkret dokumentiert. Zweitens zeigt EXP-GEN-0046 erneut den starken Unterschied zwischen Recurrence-off und Recurrence-on: 3 gegenüber 33 Spikes, 2 gegenüber 33 synaptischen Ereignissen, 0 gegenüber 10 recurrent events und propagation depth 1 gegenüber 61. Dieser Unterschied ist im registrierten kleinen Simulationsaufbau mechanistisch sichtbar.

Wissenschaftlich bleiben beide Läufe unterhalb einer EVID-Entscheidung. EXP-GEN-0046 ist explorativ, semantisch noch nicht automatisch klassifiziert und blockiert deshalb eine Evidence-Readiness-Promotion. Sein AIRR bleibt post-hoc Interpretation mit Human Review `PENDING`; die AI-Konfidenz wurde aufgrund eines Schemafehlers konservativ auf 0.0 normalisiert. Edition 1.8 übernimmt daher ausschließlich die gespeicherten DATA und deren explizite Statusgrenzen.

### Stage 4 / MSBA: fünf spezifische Forschungsfragen statt ein pauschaler Multimodalitätsclaim

Die Stage-4-E01–E05-Linie zerlegt Spezialisierung in fünf enger gefasste Fragen. Dadurch wurde vermieden, aus einem funktionierenden multimodalen Stack sofort „emergente Arealbildung“ abzuleiten.

`E01` verglich modalitätsspezifische Kosten bei matched tasks; die Referenzmodalitäten erreichten dieselbe mittlere Task-Accuracy, während die modellierten Kosten Digital < Audio < Vision lagen. `E02` zeigte im gespeicherten synthetischen Datensatz einen Vorteil der adaptiven Ressourcenallokation gegenüber fixer und zufälliger Allokation. `E03` erreichte mit adaptiver visueller ROI/Foveation dieselbe Task-Accuracy wie Full-Image bei geringerem modelliertem Energieverbrauch. `E04` zeigte im digitalen Integritätspfad keine gespeicherten Checksum- oder Exact-Payload-Mismatches. `E05` zeigte unter Modalitätsverlust eine höhere Task-Recovery der adaptiven Referenzkompensation als bei fixer Allokation.

Diese Befunde sind DATA und stützen jeweils den engen technischen Prüfgegenstand. Sie tragen weder einen allgemeinen Vorteil spezialisierter Areale noch emergente Spezialisierung oder physikalische Energieeffizienz.

### Stage 5 / Embodiment: 360 kontrollierte Runs, aber noch kein Realweltbeweis

Der Stage-5-Referenzversuch umfasst 360 kontrollierte Runs in einer synthetischen deterministischen Umgebung. Die sechs Bedingungen prüfen autorisierte und unautorisierte Wirkungspfade, Aktorfehler, Sensorausfall, Open-Loop-Replay und Sensorreproduzierbarkeit. Der Lauf stützt auf DATA-Ebene `H-EMB-001-A`: Die registrierte Sensor–SNN–Aktor–Feedback-Kette kann unter den kontrollierten Bedingungen zielgerichtete Wirkungen erzeugen und nicht autorisierte bzw. fehlerhafte Pfade abgrenzen.

Nicht abgeschlossen ist `H-EMB-001-B`. Dafür braucht es identische externe Störung und einen direkt gematchten Vergleich zwischen Closed Loop, yoked Replay und unterbrochener Rückmeldung. Der existierende Open-Loop-Pfad ist ein wichtiger Kontrollbaustein, aber kein Ersatz für dieses strengere Design. Reale Hardware bleibt ein separater safety-gated Forschungszweig.

### Stage 6 / Continual Learning: der bisher stärkste Fall empirischer Architekturselektion

CL-001 bis CL-003 bilden derzeit die methodisch wichtigste Kette, weil die Experimente die Architekturposition tatsächlich verändert haben.

CL-001 zeigte Semantic+Replay > No-Replay. Der Befund war positiv, aber kausal unzureichend aufgelöst. CL-002 ersetzte die schwache Baseline durch gematchtes Raw-Replay. Unter diesem Protokoll wurde kein konfirmatorischer Zusatznutzen semantischer Prototypen bestätigt; H1 wurde in der menschlichen Projekt-EVID für CL-002 als falsifiziert klassifiziert. CL-003 prüfte die verbleibende Dosisalternative mit 84 Runs. Die primären Kontraste C1, C2 und C4 scheiterten an den präregistrierten Erfolgsregeln; C3 zeigte dagegen, dass Semantic gegenüber einem Random-Prototype-Control deutlich bessere Struktur trägt.

Daraus entstand eine konkrete Architekturregel: Raw-Replay ist die kanonische Referenz. `SemanticMemory` bleibt technisch vorhanden, wird aber nicht mehr allein aufgrund theoretischer Plausibilität als zentraler Kernmechanismus behandelt. Weitere Rollenprüfungen dürfen nicht seriell zur Rettung eines negativen Befunds erzeugt werden. Genau eine weitere theoretisch begründete Rolle ist nur dann zulässig, wenn sie vorab begründet und präregistriert wird; andernfalls wird der Mechanismus dezentriert oder geparkt.

## 19.2 Was als EVID gilt — und was ausdrücklich nicht

Die Forschungsarbeit hat aus den Vorgängerexperimenten eine strengere Evidenzhierarchie entwickelt:

- **Engineering verification** zeigt, dass ein Mechanismus oder Vertrag technisch funktioniert.
- **DATA** sind persistierte, quellengebundene Messergebnisse eines definierten Runs.
- **Interpretation** ordnet DATA in eine Forschungsfrage ein und kann falsch sein.
- **Human Review** kann Fehler in Instrumentierung, Bericht oder Schlussfolgerung identifizieren.
- **EVID** ist eine explizite Reviewentscheidung mit Provenienz und Claim-Grenze.
- **Independent replication** ist ein weiterer Reifeschritt und wird nicht durch mehrere Seeds derselben Pipeline ersetzt.

Diese Trennung wurde nicht abstrakt erfunden, sondern aus konkreten Fehlerfällen gelernt: dem zu groben Stage-0-Langzeitvergleich, der Summary-Fehlprojektion in EXP-GEN-0036, der inadäquaten 5D-v1-Operationalisierung und der Baseline-Verwechslung in der frühen Continual-Learning-Linie.

## 19.3 Experimentelle Stop-Regeln als Bestandteil der Theorie

Ein wiederkehrendes Problem explorativer Forschung ist die Möglichkeit, einen Mechanismus durch ständig neue Rollenannahmen gegen negative Befunde zu immunisieren. MHRN behandelt deshalb Stop-Regeln zunehmend als Teil der wissenschaftlichen Theorie.

Für `SemanticMemory` bedeutet dies: Ein negativer Zusatznutzen gegenüber Raw-Replay darf zur Reduktion des Mechanismus führen. Für 5D bedeutet es: Ein nicht testadäquates Protokoll wird nicht als Nullbefund wiederholt, sondern zunächst neu operationalisiert. Für biophysikalische Erweiterungen bedeutet es: HH, Multi-Compartment, NMDA, Astrozyten, Gap Junctions oder quantale Freisetzung werden nur als fragegetriebene Modellvarianten aufgenommen, nicht als kumulative Biologie-Checkliste.

Damit wird der Forschungsprozess selbst selektiv: Nicht jede technisch mögliche Erweiterung erhält automatisch einen Platz im Kern.

## 19.6 Neural-Symbiosis- und MSBA-Forschungsprogramm

Die Architekturarbeit an Neural Symbiosis erzeugt ein eigenes falsifizierbares Programm, dessen Hypothesen nicht mit der bloßen Existenz der Pipeline verwechselt werden dürfen. Relevante Fragen sind beispielsweise, ob task-relevante periphere Areale gegenüber informationsgematchten irrelevanten Kontrollen stärkeren effektiven Gateway-Einfluss erwerben, ob verrauschte Areale selektiv unterdrückt werden, ob Gateway-Struktur nach Kontrolle roher Aktivität mit prädiktiver Information variiert und ob nach Sensorläsion adaptive Umleitung gegenüber Frozen- oder Random-Kontrollen tatsächlich Leistung erhält.

Für solche Studien sind mindestens Frozen-, Random-, Shuffle-/Timing- und informationszerstörte Kontrollen erforderlich. Eine Korrelation zwischen Gateway-Gewicht und Leistung reicht nicht für einen kausalen Tool-/Area-Use-Claim. Produktive Aktivierung bleibt bis zu experimenteller Validierung gesperrt.

Das MSBA-Programm E01–E05 operationalisiert einen Teil dieses Raums bereits für Audio, Vision und Digital. Die bisherigen synthetischen DATA werden in Teil III und X bilanziert; ihre stärkere wissenschaftliche Prüfung verlangt weiterhin spezialisierte-vs.-generalistische matched controls, Cross-Modal-Transfer, Läsionsstudien, reale Ressourcenmessung und unabhängige Review. Increased-dimensional MSBA-Projektionen müssen außerdem strukturierte, reduzierte, randomisierte und geshuffelte Mappingkontrollen enthalten und dürfen nicht als Kerndimensionalitätsstudie ausgegeben werden.

## 19.7 Externe Mechanismusvorarbeiten für Stage 6

Die kanonische Related-Work-Arbeit präzisiert mehrere externe Referenzlinien. Arbeiten zu hippocampal-kortikaler Semantization und continual learning motivieren Replay-/Konsolidierungsfragen, ohne einen MHRN-SemanticMemory-Mechanismus zu validieren [@DALBA2025] [@SHI2025]. Eine aktuelle SNN-Predictive-Coding-Übersicht zeigt, dass Prediction Error auf unterschiedliche Weise neuronal repräsentiert werden kann; ein Telemetriefeld gleichen Namens ist daher noch kein Predictive-Coding-Mechanismus [@NDRI2026]. Spiking-World-Model-Arbeit mit expliziter modellbasierter Kontrolle setzt eine deutlich stärkere Referenz als ein passiver One-Step-Predictor [@SUN2025]. Multi-Zeitskalen-Plastizität mit astrozyteninspiriertem Gating zeigt einen externen Mechanismuskandidaten für Stabilitäts-/Plastizitätsfragen, ist aber kein Wirksamkeitsnachweis der MHRN-Regelung [@DONG2026].

Diese Literatur wird in 1.8 bewusst als **externer Präzedenz-/Vergleichsraum** integriert. Sie kann die Form einer MHRN-Forschungsfrage verbessern, aber weder DATA erzeugen noch eine interne Hypothese bestätigen.

## 19.8 Determinismus-Registry, AIRR und Testadäquanz

Zwei Entscheidungen vom 17. September 2026 präzisieren die Verwendung der jüngsten SNN-DATA. Erstens bleibt der historische Lauf `EXP-BATCH-20260914074039-02` unverändert `RQ-SNN-002` zugeordnet. Seine beobachtete Condition `same_seed_tonic_replica_pair` ist für diese historische Registrierung ein semantischer Mismatch und darf nicht post hoc umetikettiert werden. Der technische Befund kann als Determinismusdiagnostik zitiert werden, aber nur gemeinsam mit dieser Provenienzgrenze.

`RQ-DET-001` besitzt nun einen expliziten Determinismusvertrag: entweder isolierte Same-Seed/Same-Input-Tonic-Replikapaare oder die expliziten `recurrence_off/on_replica_a/b`-Bedingungen. `RQ-SNN-002` behält dagegen seinen Recurrence-off/on-Vertrag; der bestehende saubere Lauf `EXP-SNN-002-R2` erfüllt diesen mit zehn Seeds. Ein neuer Lauf wird nicht allein erzeugt, um einen Registry-/Pipelinefehler kosmetisch zu reparieren.

AIRR bleibt Interpretation-only. Bei semantischem `MISMATCH` wird die öffentliche/reportseitige `ai_confidence` deterministisch auf `0.0` gesetzt; die ursprüngliche Modellselbsteinschätzung bleibt nur im append-only AIAR-Auditdatensatz. Ein isolierter Tonic-Test ist außerdem ausdrücklich **kein Netzwerkbefund** und seine Laufzeit darf nicht als Netzwerkperformance interpretiert werden.

Die zweite Entscheidung betrifft `EXP-GEN-0047` und `H-SNN-003-B`. Die sechs Conditions `1d`, `2d`, `3d`, `5d`, `5d_shuffled` und `random_graph` sind semantisch korrekt und der Lauf ist technisch reproduzierbar. Dennoch ist `topology_propagation_v1` **INADEQUATE_TO_TEST_HYPOTHESIS**: Nur drei Neuronen und zwei feed-forward Synapsen tragen die Dynamik; bei den nicht-randomisierten Bedingungen verändert sich die Koordinate, aber nicht ausreichend der kausale Übertragungsmechanismus. Daher sind identische Ergebnisse über 1D/2D/3D/5D weder ein Topologie-Nullbefund noch eine Widerlegung eines 5D-Effekts.

Die einzige deskriptive Abweichung des v1-Laufs — eine um einen Tick frühere First-Response-Latency im `random_graph` — ist konfundiert mit einer geänderten Kantenanordnung und darf nicht zum Dimensionseffekt hochgestuft werden. Auch `stopped_on_quiescence=false` ist kein Fehler: Der Runner setzt `min_ticks=max_ticks` und erzwingt damit das vollständige Beobachtungsfenster.

Für `topology_propagation_v2` gilt deshalb ein stärkerer prospektiver Vertrag: mindestens 1.000 Neuronen pro Condition, im Mittel mindestens zehn eingehende Synapsen, gematchte globale Struktur/Parameter/Stimulusenergie, explizite Kopplung von Geometriedistanz an Konnektivitätswahrscheinlichkeit und/oder Delay, die sechs genannten Kontrollen einschließlich degree-/density-matched Random Graph, multi-neuronaler Input, First-Arrival-/Reach-Verteilungen als Primärgrößen, Activity-Adequacy-Gate, mehrere unabhängige Seeds, vorab eingefrorene Inferenzregel und clean-tree Provenienz. Diese Werte sind Mindestschwellen für die nächste Testgeneration, keine Behauptung allgemeiner Suffizienz.

## 19.9 Genehmigter Stage-6-Kompressionsvorschlag

Mit `LP-20260917194217` liegt ein **genehmigter, aber nicht ausgeführter** human-origin Lernvorschlag vor. Die Forschungsfrage ist enger als der bisherige CL-003-Vergleich: Kann semantische Prototypkonsolidierung bei **10 % des Raw-Replay-Speicherbudgets** mindestens 95 % der Retention eines Raw-Replay-Baselines mit vollem Speicherbudget erreichen?

Der Vorschlag bindet `semantic_prototype_replay_10pct_budget` gegen `raw_replay_full_budget` und nennt als Kontrollen `no_replay`, `random_prototype_10pct` und `learning_off`. Die Evaluation soll auf Holdout-Daten nach sequentiellen Tasks erfolgen. Die Erfolgsmetrik ist `retention_ratio_at_1_10_storage >= 0.95` der Raw-Replay-Retention.

Der aktuelle Status ist strikt prospektiv: `authority=proposal_only`, `executed=false`, `runtime_authority=none`. Die menschliche Genehmigung autorisiert daher weder eine Ergebnisbehauptung noch DATA/EVID. Die referenzierten Quellen sind inzwischen digestscharf gebunden: `CL-002-EVID` → SHA-256 `c7b1124256fd8018839a8c5c29b30493b68d16bc223d0a3258bcbaca55b1752e` und `CL-003-DATA` → SHA-256 `4e74021c0ef838371a3a01061ae1c2dcebb2031b54c15c6169e38c1972d06290`; beide Source-Trust-Einstufungen stehen auf `VERIFIED`. Vor einer wissenschaftlich tragfähigen Ausführung bleiben Seed-/Taskplan, Analysevertrag, Ausführungsautorisation und Freeze entsprechend dem Research-Driven-Development-Prozess verbindlich zu fixieren.

## 19.4 Aktuelle Human Reviews: Determinismus und Testadäquanz

Die aktuelle Review-Linie schärft zwei bereits ausgeführte Experimente, ohne historische DATA umzuschreiben.

Für `RQ-DET-001 / H-SNN-003-A` wurde der historische Lauf `EXP-BATCH-20260914074039-03` menschlich post-hoc geprüft. Die vier Replica-Bedingungen sind nach dem heutigen semantischen Vertrag ein `DIRECT_MATCH`: innerhalb jeder Recurrence-Konfiguration stimmen Replica A und B für die Seeds 101, 102 und 103 in den aufgezeichneten Antwortsummen überein. Ohne Rekurrenz wurden je Lauf 3 Spikes, 2 synaptische Ereignisse, 0 recurrent events und propagation depth 1 beobachtet; mit Rekurrenz 33 Spikes, 33 synaptische Ereignisse, 10 recurrent events und propagation depth 61. Das ist ein positiver Determinismusbefund **innerhalb des getesteten Same-Seed-Protokolls**.

Die wissenschaftliche Grenze bleibt jedoch bestehen: der historische Lauf wurde mit `git dirty: true` erzeugt. Die nachträgliche semantische Korrektur beseitigt diesen Provenienzblock nicht. Deshalb bleibt eine clean-tree-Replikation mit eingefrorenen Source-/Config-Hashes Voraussetzung für eine reguläre EVID-Prüfung. Auch `stopped_on_quiescence=false` ist hier kein Fehlschlag: im festen Beobachtungsfenster bedeutet das Feld lediglich, dass der Lauf nicht vorzeitig wegen Quieszenz beendet wurde.

Für `RQ-SNN-003 / H-SNN-003-B` wurde `EXP-GEN-0047` ebenfalls methodisch neu eingeordnet. Die sechs Bedingungen `1d`, `2d`, `3d`, `5d`, `5d_shuffled` und `random_graph` sind semantisch die beabsichtigten Bedingungen und damit `DIRECT_MATCH`. Trotzdem ist `topology_propagation_v1` als `INADEQUATE_TO_TEST_HYPOTHESIS` klassifiziert. Der Aufbau verwendete nur drei Neuronen und zwei Feed-forward-Synapsen; bei den nicht-randomisierten Bedingungen blieben Gewichte, Delays und explizite Kette gleich, während die Koordinaten die Dynamik nicht hinreichend beeinflussten. Die identischen Kernantworten — 3 Spikes, 2 synaptische Ereignisse, 3 aktivierte Neuronen, 0 recurrent events, depth 1 — dürfen daher **nicht** als Evidenz dafür gelesen werden, dass Topologie oder Dimensionalität keinen Effekt besitzen. Der Einzelunterschied der first-response latency im Random-Graph-Arm ist zudem mit einer geänderten Kantenanordnung konfundiert.

Aus beiden Reviews folgt ein allgemeiner methodischer Vertrag: **semantischer Match, technische Reproduzierbarkeit, Testadäquanz, Provenienz und EVID sind getrennte Prüfachsen**. Ein `DIRECT_MATCH` kann wissenschaftlich blockiert bleiben; ein technisch sauberer Lauf kann für die Zielhypothese `NOT_TESTED` sein; und eine nachträgliche Registry-Korrektur darf weder Dirty-Tree-Provenienz noch unzureichendes Versuchsdesign rückwirkend heilen.
