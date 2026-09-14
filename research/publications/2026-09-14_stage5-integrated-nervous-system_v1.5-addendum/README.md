# Nachtrag zu Fassung 1.5 — Stage 5: Integriertes künstliches Nervensystem

**Datum:** 14. September 2026  
**Bezug:** `2026-09-13_recursive-epistemics_v1.5`  
**Status:** datierter wissenschaftlicher Nachtrag; die manifestgebundene Originalfassung 1.5 und ihre Binärexporte bleiben unverändert.

## Anlass

Nach Redaktionsschluss der Fassung 1.5 wurde die fünfte Entwicklungsstufe des MHRN-Programms technisch zusammengeführt: Sensorik, digitale Interozeption, autorisierte Aktorik, Rückkopplung und Ressourcenregulation werden nun als ein gemeinsamer, überprüfbarer Engineering-Vertrag behandelt und im Frontend über die bestehenden Embodiment-Live-APIs projiziert.

## Technischer Stand

Die Integration verbindet:

- typisierte und einzeln aktivierbare Sensorgrenzen;
- Host-/Systemtelemetrie als digitale Interozeption mit expliziter Unsicherheit;
- autorisierte Aktorik mit Acceptance- und Effect-Receipts;
- die `ExperienceEngine` als Sensor–SNN–Action–Observation/Reward-Schleife;
- begrenzte Ressourcen-/Energiegrößen aus Interozeption und MSBA;
- eine Stage-5-Frontendkarte, die `/api/embodiment/state`, `/api/embodiment/pipeline` und `/api/embodiment/connections` auswertet.

Der zusätzliche Integrationsvertrag `src/embodiment/integrated_nervous_system.py` ist read-only. Er schaltet keine produktive externe Aktorik frei.

## Experimenteller Bezug

Die datierte Stage-5-Referenz ist
`EXP-STAGE5-20260914-INTEGRATED-NERVOUS-SYSTEM`.

Sie verwendet den aktuellen `EXP-EMB-0001`-Protokollrunner mit sechs Bedingungen (`authorized`, `unauthorized`, `actuator_failure`, `sensor_loss`, `open_loop_replay`, `sensor_reproducibility`) und 20 unabhängigen Läufen × 3 Wiederholungen = **360 kontrollierten Runs**.

Der Runner prüft eine synthetische deterministische Closed-Loop-Umgebung. Die Ergebnisse werden ausschließlich als **DATA** gespeichert. `evidence_eligible=false`; es erfolgt **keine automatische EVID-Freigabe**.

## Forschungsfrage RQ-EMB-001

`RQ-EMB-001` fragt, ob MHRN in einer Sensor-Aktor-Schleife sinnvoll bzw. zielgerichtet agieren kann.

### H-EMB-001-A

Der Stage-5-Lauf liefert technischen DATA-Support dafür, dass die registrierte deterministische Sensor–SNN–Aktor–Feedback-Kette unter kontrollierten Bedingungen zielgerichtete Wirkungen erzeugen und nicht autorisierte bzw. fehlerhafte Wirkpfade abgrenzen kann. Dies ist **keine akzeptierte EVID** und keine Generalisierung auf reale Geräte.

### H-EMB-001-B

Die zweite Hypothese verlangt unter identischer externer Störung einen Vergleich von geschlossenem Kreis, yoked Replay und unterbrochener Rückmeldung anhand von `tracking_rmse_rad` und Sensorkonsequenzen. Diese Hypothese wird durch die Stage-5-Referenz **nicht** abgeschlossen. Der vorhandene Open-Loop-Replay-Pfad ist eine Kontrollbedingung, aber kein Ersatz für das geforderte matched-disturbance-Design.

## Einordnung der Interozeption und des Ressourcenhaushalts

Die technische Interozeption bildet CPU-, Speicher-, Temperatur-, Netzwerk-, Batterie- und weitere Systemsignale in typisierte Vital-/Regulationsgrößen mit Unsicherheitsangaben ab. Bezeichnungen wie `energy_reserve`, `resource_pressure` oder `thermal_threat` sind technische Kontrollvariablen. Sie sind **keine Behauptung biologischer Homologie**, kein Stoffwechselmodell und kein Hinweis auf subjektives Empfinden.

## Frontend und Full Stack

Die Stage-5-Ansicht verwendet ausschließlich bereits veröffentlichte Runtime-Verträge. Sie zeigt Sensorik, Interozeption, Aktorik, Feedback und Ressourcenstatus nebeneinander und hält die Grenze sichtbar, dass Live-Status, Engineering-Verifikation und wissenschaftliche Evidenz unterschiedliche Ebenen sind.

## Verbleibende wissenschaftliche Arbeit

1. unabhängige Replikation des Closed-Loop-Protokolls;
2. präregistrierter Versuch für `H-EMB-001-B` mit identischer externer Störung, yoked Replay und unterbrochener Rückmeldung;
3. längere Laufzeiten und Stör-/Recovery-Serien;
4. Real-Device-Versuche mit expliziter Hardware-, Sicherheits- und Autorisierungsgrenze;
5. getrennte Messung physischer Ressourcen/Energie statt ausschließlich technischer Kostenmodelle;
6. menschliche Prüfung vor jeder EVID-Promotion.

## Wissenschaftlich zulässige Schlussfolgerung

MHRN besitzt nach dem Stage-5-Abgleich einen reproduzierbaren technischen Integrationspfad für Sensorik, digitale Interozeption, autorisierte Aktorik, synthetische Feedbackschleifen und Ressourcenregulation. Der aktuelle Referenzversuch kann die Engineering-Funktion dieser Kette kontrolliert prüfen. Daraus folgen **keine** Aussagen über biologische Gleichwertigkeit, Bewusstsein, stabile autonome Realwelt-Handlung oder eine bereits bestätigte allgemeine Embodiment-Hypothese.
