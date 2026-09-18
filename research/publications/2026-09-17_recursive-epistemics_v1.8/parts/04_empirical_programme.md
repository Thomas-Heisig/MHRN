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

Die Arbeit zu Spiegelmechanismen wird als Stage-6-naher Forschungsstrang integriert. Der historische Primärbefund beobachtungs- und handlungsbezogener Aktivität in Affen-Prämotorkortex wird auf die ursprüngliche neurophysiologische Arbeit zurückgeführt ([@DIPELLEGRINO1992]); die breitere Systemeinordnung wird durch Reviewliteratur ergänzt ([@RIZZOLATTI2004]). Eine Verbindung zu Prediction ist als theoretischer Predictive-Coding-Account diskutiert worden ([@KILNER2007]), darf für MHRN aber nicht als bereits gezeigter Mechanismus übernommen werden. Der prüfbare MHRN-Kern ist deshalb nicht das Etikett „Spiegelneuron“, sondern die Frage, ob Beobachtungs- und Ausführungsrepräsentationen partiell überlappen, ob Kontext und Zielrelevanz diese Überlappung modulieren und ob ein Prediction-Error-Mechanismus einen kausalen Zusatznutzen liefert. Stage 4 liefert sensorische Pfade, Stage 5 Eigenaktionen/Outcome, Stage 6 Vorhersage; Stage 7 Selbst/Fremd-Unterscheidung ist erst nach eigener Kausalprüfung zulässig.

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

## 19.4 Neural-Symbiosis- und MSBA-Forschungsprogramm

Die Architekturarbeit an Neural Symbiosis erzeugt ein eigenes falsifizierbares Programm, dessen Hypothesen nicht mit der bloßen Existenz der Pipeline verwechselt werden dürfen. Relevante Fragen sind beispielsweise, ob task-relevante periphere Areale gegenüber informationsgematchten irrelevanten Kontrollen stärkeren effektiven Gateway-Einfluss erwerben, ob verrauschte Areale selektiv unterdrückt werden, ob Gateway-Struktur nach Kontrolle roher Aktivität mit prädiktiver Information variiert und ob nach Sensorläsion adaptive Umleitung gegenüber Frozen- oder Random-Kontrollen tatsächlich Leistung erhält.

Für solche Studien sind mindestens Frozen-, Random-, Shuffle-/Timing- und informationszerstörte Kontrollen erforderlich. Eine Korrelation zwischen Gateway-Gewicht und Leistung reicht nicht für einen kausalen Tool-/Area-Use-Claim. Produktive Aktivierung bleibt bis zu experimenteller Validierung gesperrt.

Das MSBA-Programm E01–E05 operationalisiert einen Teil dieses Raums bereits für Audio, Vision und Digital. Die bisherigen synthetischen DATA werden in Teil III und X bilanziert; ihre stärkere wissenschaftliche Prüfung verlangt weiterhin spezialisierte-vs.-generalistische matched controls, Cross-Modal-Transfer, Läsionsstudien, reale Ressourcenmessung und unabhängige Review. Increased-dimensional MSBA-Projektionen müssen außerdem strukturierte, reduzierte, randomisierte und geshuffelte Mappingkontrollen enthalten und dürfen nicht als Kerndimensionalitätsstudie ausgegeben werden.

## 19.5 Externe Mechanismusvorarbeiten für Stage 6

Die kanonische Related-Work-Arbeit präzisiert mehrere externe Referenzlinien. **Primärliteratur** zu hippocampal-kortikaler Semantization und continual learning motiviert Replay-/Konsolidierungsfragen, ohne einen MHRN-SemanticMemory-Mechanismus zu validieren ([@DALBA2025]; [@SHI2025]). Eine aktuelle **Sekundärquelle/Survey** zu SNN-Predictive-Coding zeigt, dass Prediction Error auf unterschiedliche Weise neuronal repräsentiert werden kann; ein Telemetriefeld gleichen Namens ist daher noch kein Predictive-Coding-Mechanismus ([@NDRI2026]). Eine **Primärarbeit** zu einem Spiking World Model mit modellbasierter Kontrolle setzt eine deutlich stärkere Referenz als ein passiver One-Step-Predictor ([@SUN2025]). Eine weitere **Primärarbeit** zu Multi-Zeitskalen-Plastizität mit astrozyteninspiriertem Gating zeigt einen externen Mechanismuskandidaten für Stabilitäts-/Plastizitätsfragen, ist aber kein Wirksamkeitsnachweis der MHRN-Regelung ([@DONG2026]).

Diese Literatur wird in 1.8 bewusst als **externer Präzedenz-/Vergleichsraum** integriert. Sie kann die Form einer MHRN-Forschungsfrage verbessern, aber weder DATA erzeugen noch eine interne Hypothese bestätigen.

## 19.6 Determinismus-Registry, AIRR und Testadäquanz

Zwei Entscheidungen vom 17. September 2026 präzisieren die Verwendung der jüngsten SNN-DATA. Erstens bleibt der historische Lauf `EXP-BATCH-20260914074039-02` unverändert `RQ-SNN-002` zugeordnet. Seine beobachtete Condition `same_seed_tonic_replica_pair` ist für diese historische Registrierung ein semantischer Mismatch und darf nicht post hoc umetikettiert werden. Der technische Befund kann als Determinismusdiagnostik zitiert werden, aber nur gemeinsam mit dieser Provenienzgrenze.

`RQ-DET-001` besitzt nun einen expliziten Determinismusvertrag: entweder isolierte Same-Seed/Same-Input-Tonic-Replikapaare oder die expliziten `recurrence_off/on_replica_a/b`-Bedingungen. `RQ-SNN-002` behält dagegen seinen Recurrence-off/on-Vertrag; der bestehende saubere Lauf `EXP-SNN-002-R2` erfüllt diesen mit zehn Seeds. Ein neuer Lauf wird nicht allein erzeugt, um einen Registry-/Pipelinefehler kosmetisch zu reparieren.

AIRR bleibt Interpretation-only. Bei semantischem `MISMATCH` wird die öffentliche/reportseitige `ai_confidence` deterministisch auf `0.0` gesetzt; die ursprüngliche Modellselbsteinschätzung bleibt nur im append-only AIAR-Auditdatensatz. Ein isolierter Tonic-Test ist außerdem ausdrücklich **kein Netzwerkbefund** und seine Laufzeit darf nicht als Netzwerkperformance interpretiert werden.

Die zweite Entscheidung betrifft `EXP-GEN-0047` und `H-SNN-003-B`. Die sechs Conditions `1d`, `2d`, `3d`, `5d`, `5d_shuffled` und `random_graph` sind semantisch korrekt und der Lauf ist technisch reproduzierbar. Dennoch ist `topology_propagation_v1` **INADEQUATE_TO_TEST_HYPOTHESIS**: Nur drei Neuronen und zwei feed-forward Synapsen tragen die Dynamik; bei den nicht-randomisierten Bedingungen verändert sich die Koordinate, aber nicht ausreichend der kausale Übertragungsmechanismus. Daher sind identische Ergebnisse über 1D/2D/3D/5D weder ein Topologie-Nullbefund noch eine Widerlegung eines 5D-Effekts.

Die einzige deskriptive Abweichung des v1-Laufs — eine um einen Tick frühere First-Response-Latency im `random_graph` — ist konfundiert mit einer geänderten Kantenanordnung und darf nicht zum Dimensionseffekt hochgestuft werden. Auch `stopped_on_quiescence=false` ist kein Fehler: Der Runner setzt `min_ticks=max_ticks` und erzwingt damit das vollständige Beobachtungsfenster.

`topology_propagation_v2` wurde inzwischen als enger **Stage-1-Test von `H-SNN-003-B`** präregistriert und ausgeführt. Die stärkeren Schwellen von ≥1.000 Neuronen und ≥10 eingehenden Synapsen gehören nicht zu diesem allgemeinen Topologietest, sondern zur getrennten dimensionsspezifischen Prüfung `RQ-5D-005 / H-5D-005-A`. Diese Trennung verhindert, dass ein kleiner, testadäquater Topologiebefund nachträglich zu einem 5D-Vorteilsclaim erweitert wird.

## 19.7 Genehmigter Stage-6-Kompressionsvorschlag

Mit `LP-20260917194217` liegt ein **genehmigter, aber nicht ausgeführter** human-origin Lernvorschlag vor. Die Forschungsfrage ist enger als der bisherige CL-003-Vergleich: Kann semantische Prototypkonsolidierung bei **10 % des Raw-Replay-Speicherbudgets** mindestens 95 % der Retention eines Raw-Replay-Baselines mit vollem Speicherbudget erreichen? Externe Gedächtnis- und Konsolidierungsarbeiten liefern hierfür einen theoretischen und mechanistischen Vergleichsraum ([@MCCLELLAND1995]; [@DALBA2025]; [@SHI2025]), aber die konkrete 10-%-/95-%-Entscheidungsgrenze ist eine **prospektive MHRN-Hypothese** und kein aus der Literatur übernommener Effekt.

Der Vorschlag bindet `semantic_prototype_replay_10pct_budget` gegen `raw_replay_full_budget` und nennt als Kontrollen `no_replay`, `random_prototype_10pct` und `learning_off`. Die Evaluation soll auf Holdout-Daten nach sequentiellen Tasks erfolgen. Die Erfolgsmetrik ist `retention_ratio_at_1_10_storage >= 0.95` der Raw-Replay-Retention. Damit prüft der nächste Zyklus **Kompression bei erhaltener Retention**, nicht eine allgemeine Überlegenheit der Lernleistung.

Die Entscheidungsfolge wird vor DATA festgelegt: **Erreicht** die semantische Prototypkonsolidierung die vorab fixierte Retentionsgrenze bei einem Zehntel des Speicherbudgets, ist damit eine begrenzte Kompressionsrolle von SemanticMemory unter genau diesem Protokoll gestützt. **Verfehlt** sie die Grenze, gilt diese Kompressionsrolle für den getesteten Mechanismus als nicht gestützt; Generalisierung, Langzeitgedächtnis oder eine Weltmodell-Brücke wären dann eigenständige spätere Forschungsfragen und dürfen nicht als nachträgliche Rettung desselben Tests verwendet werden.

Der aktuelle Status ist strikt prospektiv. Das historisch genehmigte `LP-20260917194217` bleibt als Originalartefakt unverändert und besitzt weiterhin `executed=false` sowie keine Runtime-Autorität. Die fehlende Quellbindung wurde **nicht** in dieses genehmigte Artefakt hineingeschrieben. Stattdessen liegt mit `LP-20260917194217-R1` eine neue `proposal_only`-Revision vor: `CL-002-EVID` → SHA-256 `c7b1124256fd8018839a8c5c29b30493b68d16bc223d0a3258bcbaca55b1752e` und `CL-003-DATA` → SHA-256 `4e74021c0ef838371a3a01061ae1c2dcebb2031b54c15c6169e38c1972d06290`; beide Source-Trust-Einstufungen stehen auf `VERIFIED`. Diese Inhaltsänderung erfordert eine **neue explizite Human Approval**; die historische Genehmigung wird nicht übertragen.

Der **nächste empirische Arbeitsschritt ist die Präregistrierung dieses Kompressionsvergleichs**, nicht seine Ausführung. Vor einem `FROZEN`-Status müssen mindestens die kanonische RQ/H-Zuordnung, die exakte Speicherbudget-Messung, Seed-/Taskplan, Retentionsaggregation und Inferenz-/Äquivalenzregel, Ausschluss- und Failure-Regeln, Analysevertrag, Source-/Config-Hashes sowie die R1-Human-Approval gebunden sein. Erst danach kann eine separate Ausführungsautorisation erteilt werden. Diese Trennung folgt der allgemeinen Präregistrierungslogik, Hypothese und Analyseplan vor Sichtung der Ergebnisdaten festzulegen ([@NOSEK2018]).

## 19.8 Aktuelle Human Reviews: Determinismus und Testadäquanz

Die aktuelle Review-Linie schärft zwei bereits ausgeführte Experimente, ohne historische DATA umzuschreiben.

Für `RQ-DET-001 / H-SNN-003-A` wurde der historische Lauf `EXP-BATCH-20260914074039-03` menschlich post-hoc geprüft. Die vier Replica-Bedingungen sind nach dem heutigen semantischen Vertrag ein `DIRECT_MATCH`: innerhalb jeder Recurrence-Konfiguration stimmen Replica A und B für die Seeds 101, 102 und 103 in den aufgezeichneten Antwortsummen überein. Ohne Rekurrenz wurden je Lauf 3 Spikes, 2 synaptische Ereignisse, 0 recurrent events und propagation depth 1 beobachtet; mit Rekurrenz 33 Spikes, 33 synaptische Ereignisse, 10 recurrent events und propagation depth 61. Das ist ein positiver Determinismusbefund **innerhalb des getesteten Same-Seed-Protokolls**.

Die wissenschaftliche Grenze bleibt jedoch bestehen: der historische Lauf wurde mit `git dirty: true` erzeugt. Die nachträgliche semantische Korrektur beseitigt diesen Provenienzblock nicht. Deshalb bleibt eine clean-tree-Replikation mit eingefrorenen Source-/Config-Hashes Voraussetzung für eine reguläre EVID-Prüfung. Auch `stopped_on_quiescence=false` ist hier kein Fehlschlag: im festen Beobachtungsfenster bedeutet das Feld lediglich, dass der Lauf nicht vorzeitig wegen Quieszenz beendet wurde.

Für `RQ-SNN-003 / H-SNN-003-B` wurde `EXP-GEN-0047` ebenfalls methodisch neu eingeordnet. Die sechs Bedingungen `1d`, `2d`, `3d`, `5d`, `5d_shuffled` und `random_graph` sind semantisch die beabsichtigten Bedingungen und damit `DIRECT_MATCH`. Trotzdem ist `topology_propagation_v1` als `INADEQUATE_TO_TEST_HYPOTHESIS` klassifiziert. Der Aufbau verwendete nur drei Neuronen und zwei Feed-forward-Synapsen; bei den nicht-randomisierten Bedingungen blieben Gewichte, Delays und explizite Kette gleich, während die Koordinaten die Dynamik nicht hinreichend beeinflussten. Die identischen Kernantworten — 3 Spikes, 2 synaptische Ereignisse, 3 aktivierte Neuronen, 0 recurrent events, depth 1 — dürfen daher **nicht** als Evidenz dafür gelesen werden, dass Topologie oder Dimensionalität keinen Effekt besitzen. Der Einzelunterschied der first-response latency im Random-Graph-Arm ist zudem mit einer geänderten Kantenanordnung konfundiert.

Aus beiden Reviews folgt ein allgemeiner methodischer Vertrag: **semantischer Match, technische Reproduzierbarkeit, Testadäquanz, Provenienz und EVID sind getrennte Prüfachsen**. Ein `DIRECT_MATCH` kann wissenschaftlich blockiert bleiben; ein technisch sauberer Lauf kann für die Zielhypothese `NOT_TESTED` sein; und eine nachträgliche Registry-Korrektur darf weder Dirty-Tree-Provenienz noch unzureichendes Versuchsdesign rückwirkend heilen.

## 19.9 Die empirischen Forschungszweige als eigenständige Teilstudien

Die bisherigen Experimente werden in Edition 1.8 nicht nur chronologisch berichtet. Für den dissertationsähnlichen Charakter der Gesamtarbeit werden die zentralen empirischen Zweige zusätzlich als **eigenständige Teilstudien** gelesen. Jede Teilstudie unterscheidet Forschungsproblem, RQ/H-Bindung, Design, Befund, Diskussion, Limitation und nächsten Prüfpunkt. Dadurch wird vermieden, dass ein technischer Stage-Fortschritt an die Stelle einer wissenschaftlichen Argumentation tritt.

### 19.9.1 Teilstudie A — Basale Dynamik, Referenzkonformität und Determinismus

**Forschungsproblem.** Ein deterministisch implementiertes Neuronenmodell ist nicht automatisch wissenschaftlich validiert. Zu unterscheiden sind lokale Gleichungs-/Resetsemantik, freie Langzeittrajektorie, Same-Seed-Reproduzierbarkeit und unabhängige Replikation.

**RQ/H-Bezug.** Relevant sind insbesondere `RQ-SNN-002 / H-SNN-002-A` für reproduzierbare Spikefolgen sowie `RQ-DET-001 / H-SNN-003-A` für deterministische Zustands- und Replikationsverträge.

**Methodik.** Verwendet werden Referenzvergleiche gegen externe Implementierungen, eingefrorene Inputs, Same-Seed-Replica-Paare, Zustandsdigests und getrennte Recurrence-Bedingungen. Technische Gleichheit und wissenschaftliche Replikation werden ausdrücklich nicht gleichgesetzt.

**Befund.** Für die geprüften kleinen Protokolle liegen enge Referenzübereinstimmungen beziehungsweise identische Same-Seed-Ausgaben vor. Gleichzeitig zeigen historische Langzeit- und Dirty-Tree-Befunde, dass diese Aussage nicht auf beliebige Zeithorizonte, Netzwerkgrößen oder Umgebungen erweitert werden darf.

**Diskussion.** Der wissenschaftliche Beitrag liegt weniger in einem pauschalen „deterministisch“, sondern in der Zerlegung des Begriffs in prüfbare Ebenen.

**Limitation.** Die zentralen Läufe stammen aus derselben Projekt- und Toolkette. Unabhängige Replikation bleibt ausstehend.

**Zwischenfazit.** Basale Reproduzierbarkeit ist für definierte Operating Envelopes gestützt; eine allgemeine Determinismusgarantie ist nicht gezeigt.

### 19.9.2 Teilstudie B — Rekurrenz, Topologie und 5D-Geometrie

**Forschungsproblem.** Rekurrenz und geometrische Einbettung können Netzwerkdynamik verändern, aber nur dann getrennt interpretiert werden, wenn Konnektivität, Grad, Delays, Stimulus und Aktivität ausreichend kontrolliert sind.

**RQ/H-Bezug.** `RQ-SNN-003 / H-SNN-003-B` adressiert Topologieeffekte ohne vorausgesetzten 5D-Vorteil. `RQ-5D-005 / H-5D-005-A` fragt enger nach einem dimensionsspezifischen Unterschied gegenüber topology-matched niedrigdimensionalen Einbettungen.

**Methodik.** Recurrence-on/off dient als mechanistische Intervention. Der nachfolgende Topologietest `EXP-S1-TOPO-V2-20260918` vergleicht 1D/2D/3D/5D, `5d_shuffled` und `random_graph` bei 64 Neuronen und identischem 246-Kanten-Budget. Gewichte, Delays und Stimulus werden gematcht; vier Kalibrier-Seeds sind von zwanzig Evaluations-Seeds getrennt. Das präregistrierte Activity-Adequacy-Gate darf nur Aktivierbarkeit, nicht Effektstärke, zur Gewichtswahl verwenden. Primärendpunkte sind `active_fraction` und zensierte First-Output-Latenz; gepaarte Sign-Tests werden über alle Primärkontraste Holm-korrigiert, Median-Differenzen erhalten deterministische Bootstrap-95%-Intervalle.

**Befund.** Das Activity-Gate bestand beim niedrigsten Kandidatengewicht 55.0. Alle 120 Evaluationsläufe waren vollständig; 64 Neuronen, 246 Kanten und das eingefrorene Gewicht waren in allen Armen erhalten. Mehrere präregistrierte Primärkontraste unterschieden sich signifikant. Beispielsweise lag die mediane Änderung der aktiven Netzwerkfraktion für 3D→5D bei -0,125 (Bootstrap-CI95 -0,15625 bis -0,1015625; Holm-p ≈ 1,91×10^-5). Bei der First-Output-Latenz lagen die Medianunterschiede 1D→2D bei -10 Ticks, 2D→3D bei -3 Ticks und 3D→5D bei -1 Tick. Der registrierte DATA-Status lautet `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`.

**Diskussion.** Damit besitzt `H-SNN-003-B` erstmals einen testadäquaten positiven Befund im untersuchten Stage-1-Regime: Topologie verändert die Propagationsdynamik. Der Effekt ist jedoch **kein monotones Dimensions- oder 5D-Vorteilsmuster**. `5d_shuffled` und `random_graph` erreichten den Output in diesem Design sogar früher als die reguläre 5D-Anordnung. Das unterstützt die allgemeine Topologiesensitivität, nicht die Überlegenheit einer bestimmten Dimensionalität.

**Limitation.** 64 Neuronen und das deterministische vorwärtsgerichtete Konstrukt sind ein enger Small-SNN-Operating-Envelope. Der Lauf prüft weder Skalierung noch biologische Äquivalenz noch `H-5D-005-A`. Die stärkere 5D-Prüfung benötigt weiterhin ≥1.000 Neuronen, ≥10 mittlere Eingänge pro Neuron, explizit distanzabhängige Konnektivität und streng gematchte Dimensionskontrollen. Der aktuelle Lauf bleibt bis Human Review DATA-only.

**Zwischenfazit.** Rekurrenz ist im getesteten Mechanismus wirksam; `H-SNN-003-B` ist im 64-Neuronen-Stage-1-Regime DATA-seitig gestützt. Die spezifische 5D-Hypothese bleibt offen.

### 19.9.3 Teilstudie C — Plastizität, Lernen und adaptive Stabilität

**Forschungsproblem.** Die Existenz von STDP-, Eligibility-, Drei-Faktor-, Homeostase- oder Strukturplastizitätscode beweist weder nützliches Lernen noch stabile Generalisierung.

**RQ/H-Bezug.** `RQ-SNN-004 / H-SNN-004-A` adressiert die durch STDP verursachte Veränderung der Gewichtsmatrix; `RQ-SNN-005 / H-SNN-005-A` prüft einen funktionalen Lernvorteil gegenüber einem Netzwerk ohne STDP.

**Methodik.** Erforderlich sind learning-on/off-, Frozen-, Sham-/informationszerstörte Kontrollen, gehaltene Testdaten, unabhängige Seeds sowie getrennte Messungen von Gewichtsänderung, Aufgabenleistung, Stabilität und Transfer.

**Befund.** Mehrere Plastizitätsmechanismen sind technisch implementiert und diagnostisch instrumentiert. Daraus folgt noch kein abgeschlossener funktionaler Lernnachweis für die stärkeren Hypothesen.

**Diskussion.** Dieser Zweig markiert exemplarisch die Differenz zwischen Mechanismusimplementierung und kausalem Nutzen. Eine Gewichtsänderung kann korrekt sein und trotzdem keine relevante Lernleistung erzeugen.

**Limitation.** Die stärksten Learning-RQs sind noch nicht durch einen einheitlichen, ausreichend kontrollierten konfirmatorischen Vertrag abgeschlossen.

**Zwischenfazit.** Plastizität ist ein implementierter Mechanismenraum, aber ihre funktionale Rolle bleibt hypothesenspezifisch zu prüfen.

### 19.9.4 Teilstudie D — Spezialisierte Pfade, Neural Symbiosis und MSBA

**Forschungsproblem.** Modalitätsspezifische Pfade können Kosten, Robustheit oder Integrität verändern; daraus folgt jedoch nicht automatisch emergente Spezialisierung oder biologische Arealhomologie.

**RQ/H-Bezug.** Der Zweig wird durch `RQ-MSBA-E01` bis `RQ-MSBA-E05` in mehrere enge Teilfragen zerlegt.

**Methodik.** Die registrierten synthetischen Designs prüfen modalitätsspezifische Kosten, adaptive Ressourcenallokation, visuelle ROI/Foveation, digitale Integrität und Recovery nach Modalitätsverlust.

**Befund.** In mehreren Teilfragen liegen positive DATA innerhalb der modellierten synthetischen Bedingungen vor.

**Diskussion.** Der Erkenntniswert liegt in der Zerlegung eines großen Multimodalitätsclaims in kleinere, direkt prüfbare Funktionen. Dadurch kann positive technische Evidenz bestehen, ohne daraus eine stärkere Theorie neuronaler Arealbildung abzuleiten.

**Limitation.** Modellierte Kosten sind keine physikalischen Energiedaten; synthetische Recovery ist keine allgemeine Realweltrobustheit.

**Zwischenfazit.** Spezialisierte Pfade sind technisch und teilweise experimentell gestützt; emergente Spezialisierung bleibt unbewiesen.

### 19.9.5 Teilstudie E — Kontrolliertes synthetisches Embodiment

**Forschungsproblem.** Eine technisch geschlossene Sensor–Aktor-Kette ist erst dann wissenschaftlich interessant, wenn Wirkung, Autorisierung, Feedback und Störung kausal getrennt werden.

**RQ/H-Bezug.** `RQ-EMB-001` wird durch `H-EMB-001-A` und `H-EMB-001-B` operationalisiert.

**Methodik.** Der Stage-5-Referenzversuch nutzt Sensorik, technische Interozeption, autorisierte/unauthorisierte Aktorpfade, Fehlerbedingungen, Open-Loop-Replay und Feedback in einer deterministischen synthetischen Umgebung.

**Befund.** Die 360-Run-Kampagne liefert DATA-Support für `H-EMB-001-A` innerhalb des kontrollierten Settings. `H-EMB-001-B` ist durch diesen Vertrag nicht getestet.

**Diskussion.** Der geschlossene Pfad zeigt eine begrenzte, kausal instrumentierbare Form verkörperter Interaktion. Gerade die noch offene B-Hypothese verhindert, dass aus dem Engineeringerfolg vorschnell allgemeine Anpassungs- oder Autonomieclaims entstehen.

**Limitation.** Keine reale Hardware, keine Langzeitumgebung, keine unabhängige externe Replikation.

**Zwischenfazit.** Synthetisches Embodiment ist demonstriert; Realwelt- und Störungsadaptivität bleiben offene Forschungsfragen.

### 19.9.6 Teilstudie F — Gedächtnis, Replay, semantische Verdichtung und Weltmodell

**Forschungsproblem.** Retention kann durch generisches Replay, semantische Verdichtung, Retrieval oder echte interne Modellbildung entstehen. Diese Ursachen müssen experimentell getrennt werden.

**RQ/H-Bezug.** Historische Gedächtnisfragen liegen unter anderem in `RQ-MEM-001 / H-MEM-001-A`. Die CL-001–CL-003-Linie operationalisiert den stärkeren Vergleich zwischen Semantic+Replay, Raw Replay und Kontrollbedingungen. `OBJ-MEM-COMPRESSION-001` ist die nächste prospektive Spezialfrage, besitzt aber noch keine endgültig eingefrorene kanonische RQ/H-Bindung.

**Methodik.** Verwendet werden No-Replay-, Raw-Replay-, Semantic-Prototype- und Random-Prototype-Kontrollen, Holdout-Daten, gepaarte Seeds und präregistrierte Erfolgsgrenzen. Für Weltmodellclaims sind zusätzlich action conditioning, Mehrschrittrollouts und corrupted/no-model Kontrollen erforderlich.

**Befund.** Replay trägt die Retention robuster als die bisher behauptete semantische Zusatzleistung. Semantische Prototypen enthalten Struktur, aber ihr Mehrwert gegenüber gematchtem Raw Replay wurde in CL-002/003 nicht bestätigt.

**Diskussion.** Der Zweig zeigt am deutlichsten, wie negative Evidenz Architektur selektiert. Statt SemanticMemory rhetorisch zu retten, wird eine engere Kompressionsfrage formuliert.

**Limitation.** Die Kompressionshypothese ist noch nicht präregistriert und ausgeführt; ein kausales Weltmodell ist nicht gezeigt.

**Zwischenfazit.** Replay ist derzeit die stärkere Referenz. Die nächste zulässige Frage betrifft Kompression bei erhaltener Retention, nicht eine erneute pauschale Überlegenheitsbehauptung.

### 19.9.7 Teilstudienübergreifende Schlussfolgerung

Über alle empirischen Zweige hinweg entsteht ein wiederkehrendes Muster: **technische Verfügbarkeit ist der Beginn einer wissenschaftlichen Frage, nicht deren Antwort**. Ein Mechanismus wird erst dann Teil der tragfähigen Architekturposition, wenn sein kausaler Beitrag gegenüber einer geeigneten einfacheren Referenz sichtbar wird oder seine Spezialrolle durch einen eigenen, vorab begründeten Prüfvertrag getragen ist.

Damit erhält Teil IV den Charakter einer kumulativen empirischen Dissertationseinheit: Die Teilstudien stehen nicht nebeneinander, sondern verändern wechselseitig die Architektur und die Bedingungen der jeweils nächsten Hypothese.
