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
