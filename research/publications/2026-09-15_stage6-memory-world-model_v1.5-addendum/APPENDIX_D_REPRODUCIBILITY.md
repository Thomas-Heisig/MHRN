# Anhang D — Reproduzierbarkeit, Provenienz und EVID-Promotion

## D.1 Schichten der Aussage

Stage-6-Ergebnisse werden in vier Ebenen getrennt:

1. **Contract verified** — Unit-/Integrationtests bestätigen einen Softwarevertrag.
2. **DATA produced** — ein registrierter Versuch wurde vollständig ausgeführt und erzeugt primäre Messdaten.
3. **Analysis complete** — vorab definierte Statistik, Kontrollen und Sensitivitätsprüfungen liegen vor.
4. **EVID accepted** — die Evidenz erfüllt die registrierten Promotionsregeln und wurde nicht durch Leakage, Confounds oder Provenienzfehler disqualifiziert.

Ein grüner CI-Lauf kann Ebene 1 belegen, niemals automatisch Ebene 4.

## D.2 Mindestprovenienz je Stage-6-Versuch

Jeder Run muss mindestens enthalten:

- Commit-SHA und Dirty-State,
- Protokoll- und Schema-Version,
- Seed und Randomisierungsquelle,
- Konfiguration inklusive Memory-/Prediction-/Reward-Kontrollen,
- Modellzustand oder dessen kryptographischen Digest vor frozen evaluation,
- Train-/Validation-/Test-Zuordnung,
- Tick-/Episode-/Kandidatenbudget,
- Hardware-/Runtime-Metadaten soweit leistungsrelevant,
- Rohmesswerte vor Aggregation,
- explizites `accepted_evidence: false`, bis ein separates Gate die Promotion erlaubt.

## D.3 Frozen world-model evaluation

Für Mehrschritt- und Entscheidungsnutzen gilt:

- Weltmodelllernen ist im Testfenster deaktiviert.
- Kandidaten einer Episode haben denselben Horizont und dasselbe Auswertungsbudget.
- Unbekannte Übergänge werden als fehlende Coverage ausgewiesen, nicht als Nullfehler.
- Auswahlregeln sind deterministisch und vorab festgelegt.
- Der Offline-Evaluator darf das Modell nicht mutieren.
- Empfehlungen lösen keine externe Handlung aus.

## D.4 Memory experiments

Für neuronalen Recall darf das Ziel nicht direkt aus dem gespeicherten sensorischen Payload als Antwort gelesen werden. Der experimentelle Informationspfad muss dokumentieren, welche Daten dem Probe-Decoder tatsächlich zugänglich sind. Read-off, Write-off und Cue-/Episode-Shuffle sind getrennte Kontrollen und dürfen nicht in einem Sammelschalter vermischt werden.

## D.5 Replay experiments

Replay-Bedingungen müssen ihre effektiven Updatebudgets protokollieren. `ordered`, `shuffled`, `off` und `extra-awake` werden mit vergleichbaren Gesamtbudgets ausgewertet. Ein Vorteil allein gegenüber `off`, aber nicht gegenüber gleich budgetiertem Zusatztraining, trägt keine starke Konsolidierungsbehauptung.

## D.6 Prediction Error

Umwelt-Prediction-Error, Activity-Prediction-Error und Reward werden als getrennte Signale protokolliert. Für `S6-PE-001` muss die Manipulation eines Signals nachweislich die anderen Signalzähler und -werte unverändert lassen, sofern die Versuchskondition dies verlangt.

## D.7 Statistik

Confirmatorische Experimente registrieren vor Ausführung:

- primären Endpunkt,
- Richtung oder zweiseitige Hypothese,
- Seedzahl bzw. Powerbegründung,
- Ausschlusskriterien,
- geplantes Konfidenzintervall und Effektmaß,
- Behandlung multipler primärer Tests.

Als Standardziel werden mindestens 20 unabhängige Initialisierungsseeds angesetzt, sofern eine Poweranalyse keine andere Zahl begründet. Einzel-Seed-Werte bleiben neben Aggregaten veröffentlicht.

## D.8 Negativbefunde

Null- und Negativbefunde bleiben Bestandteil der Dissertation. Insbesondere dürfen folgende Ergebnisse nicht durch bloße Architekturänderungen „weginterpretiert“ werden:

- kein Memory-Vorteil nach Distraktoren,
- keine held-out Semantisierung,
- Replay nicht besser als gleich budgetiertes Wachtraining,
- Prediction Error ohne gerichteten Nutzen,
- Mehrschrittmodell ohne Vorteil gegenüber Persistenz/Shuffles,
- gute Vorhersage ohne messbaren Entscheidungsnutzen.

Diese Befunde wären wissenschaftlich informativ und können die Stage-6-Hypothesen falsifizieren oder begrenzen.

## D.9 Externe Replikation

Eine spätere starke Aussage benötigt neben interner Seed-Replikation einen reproduzierbaren Run auf einem unabhängigen Checkout bzw. idealerweise durch eine externe Person/Umgebung. Externe Replikation ist getrennt von CI-Wiederholungen auf demselben Quellstand zu dokumentieren.
