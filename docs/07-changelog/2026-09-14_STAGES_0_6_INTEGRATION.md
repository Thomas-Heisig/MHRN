# Stages 0-6: Integration, Funktionen und verbleibende Grenzen

Stand: 14. September 2026. Dieser Bericht ist ein Code- und Integrationsaudit, keine wissenschaftliche Annahmeentscheidung.

## Zusammengefuehrte Historien

Ausgangsbasis ist `a72081ba6722343b0d4795ceee08f2e06ea9684c` (main nach Reader-PR #84). Der Integrationszweig bewahrt die beiden Stage-5-Historien einschliesslich der Nachtraege bis `68fb1a312e835ca90d1891dc006ff5900c44cbf9` sowie Stage 6A bis `82bd5236d7db6d0252b7f5c9641023152b1d5edc`. Der gemeinsame Merge `68b3170426f68987effeeb2c3e2c7eb0b1e1a64e` enthaelt beide Elternhistorien; kein Force-Push und kein Austausch gegen einen alten Dateibaum.

PR #79, #82 und #84 sind vorherige Integrationen. PR #83 ist der Stage-6A-Entwurf; seine Codehistorie ist im gemeinsamen Zweig enthalten. Massgeblich fuer den abschliessenden main-Stand sind der Integrations-PR und dessen exakte Commit-Pruefungen, nicht der Ahead/Behind-Wert eines stehen gebliebenen Arbeitszweigs.

## Stand je Entwicklungsstufe

| Stufe | Vorhandener, begrenzter Funktionsumfang | Nicht dadurch belegt / noch offen |
| --- | --- | --- |
| 0 | Versionierte Neuronenmodelle, Membranintegration, Spike/Reset/Erholung, Modellprovenienz und deterministische Fortsetzung. | Biologische Gleichwertigkeit und vollstaendige Ionenkanal-/Morphologiemodelle sind keine Folgerung aus diesen Softwaretests. |
| 1 | Gekoppelte Neuronen, Synapsen, Spike-Ausbreitung und raeumlicher Sparse-Index. | Kleine Netztests ersetzen keine Laufzeit-/Speicherbenchmarks an der Zielgroesse. |
| 2 | Rekurrente Ausfuehrung, deterministische Runtime, Replay und Restore-Vertraege. | Stabilitaet ist nur fuer die getesteten Konfigurationen gezeigt, nicht fuer beliebige Netze oder Kognition. |
| 3 | STDP, Drei-Faktor-Plastizitaet, Homeostase, Wachstum/Pruning und persistierter adaptiver Zustand. | R2: produktives Lernen gegen learning-off, Sham/informationszerstoerte und gehaltene Testdaten; unabhaengige wissenschaftliche Pruefung. |
| 4 | Auditive, visuelle und digitale Vertraege; experimentelle Gateways; Provenienz und Kontrollbedingungen. | Aggregierte 100k/10M-Budgets sind kein dynamisch ausgefuehrtes Netz dieser Groesse. Produktive Gateway-Aktivierung bleibt gesperrt; E01-E05 bleiben DATA bis zur separaten Bewertung. |
| 5 | Sensorik, technische Interozeption, autorisierte Aktorik, Feedbackschleife und Ressourcenhaushalt; beide parallelen Implementierungszweige erhalten. | H-EMB-001-B: gematchte Stoerungen, Yoked-Replay und unterbrochenes Feedback; reale Geraete, lange Laufzeiten und unabhaengige Replikation. |
| 6 | Begrenzter Episoden-/Arbeitsspeicher, statistischer Einschritt-Praediktor, typgetreue Kategorien, Feldzaehler, FIFO-Fortsetzung und vier unabhaengige Schalter. | Neuronales semantisches/episodisches Gedaechtnis, Konsolidierung, gelerntes Mehrschritt-Weltmodell, lernwirksame Vorhersagefehler, kanonischer Runtime-Checkpoint und SNN-involvierte Evidenz. |

Die Timeline-Kategorie `reached` bezeichnet den begrenzten Engineering-Vertrag. Prozentwerte sind aggregierte Indikatoren, keine Wahrscheinlichkeit fuer biologische Gleichwertigkeit, Intelligenz oder Bewusstsein. Stage 6 wird durch diesen Nachtrag nicht auf fertig gesetzt; Stage 8-10 bleiben geplant.

## In diesem Integrationsschritt ergaenzte Funktionen

- Das Kognitions-API respektiert `read_enabled` auch fuer `latest_prediction`. Vorhersagehistorie und Modellinhalt sind bei gesperrtem Lesen nicht abrufbar. Die Lesesperre loescht keine bereits frueher exportierten Daten und ist keine Benutzer-Authentifizierung.
- Vorhersageantworten enthalten feldweise numerische Fehler, kategoriale Abweichungen und Abdeckung. Bestehende Speicherbytes, `PredictionRecord` und Schema-IDs werden nicht fuer eine Anzeigeaenderung umgeschrieben.
- Die vorhandene Kognitionsansicht zeigt diese Feldwerte, die unabhaengigen Praediktorschalter und einen begrenzten JSON-Export. Bei Fehlern bleiben weder ein falscher Erfolgsstatus noch ein bestaetigter Schreibvorgang stehen.
- Ein expliziter Wiederaufbau aus vollstaendig deklarierten, SHA-256-gebundenen Rohereignissen erzeugt neue v2-Referenzdateien. Alte v1-Aggregate oder ein begrenzter Episodenexport sind kein zulaessiger Ersatz.
- Die Entwicklungstimeline laedt unabhaengig vom Gate-Panel; parallele Anfragen werden zusammengefasst und kurzfristige Wiederholungen begrenzt.
- Fehlendes oder leeres AIRR-`assessment` bleibt als `analysis_unavailable` sichtbar. Eine formal aufgefuellte Antwort ist keine erfolgreiche Modellanalyse. Das Verbot modellgenerierter quantitativer Statistik bleibt bestehen.

## Pruefung und Reproduktion

Der erste gemeinsame Lauf `34877066028` auf dem Merge vor diesen Korrekturen ergab **1406 bestandene, 1 fehlgeschlagenen und 32 abgewaehlte langsame Tests**. Der Fehler betraf den AIRR-Fallback; daneben wurden fuenf Formatierungsabweichungen gefunden. Das sind datierte Ausgangsergebnisse, keine Freigabe des Endstands. Der lokale Quellbaum muss fuer Source-Digest-Tests eingecheckt sein: absichtlich schmutzige Baeume werden auch bei passendem Digest als veraltet behandelt.

```bash
python -m pytest -q -m 'not slow'
python -m pytest -q -m slow
node --test tests/frontend/*.test.mjs
npm run test:e2e
python scripts/check_doc_consistency.py --check-tests
python -m scripts.audit_stages_0_6
```

Die neuen Browserfaelle verwenden einen ausschliesslich im Testserver vorhandenen Referenz-Fixture auf beiden Servervarianten; sie fuehren die echten Kognitions-Endpunkte aus und behaupten keine neuronale Leistung. Formatierung, Typpruefungen, Sicherheit, Build und Wissenschaftsgate bleiben eigenstaendige Anforderungen der unveraenderten Voll-CI. Ein uebersprungener Lauf ist kein bestandener Lauf.

[Dissertationsnachtrag](../../research/publications/2026-09-14_stages0-6-integration_v1.5-addendum/README.md) und [Wiederaufbauformat](../../research/specifications/STAGE6_REPLAY_FORMAT.md) beschreiben die Aussagegrenzen und Bedienung. Historische DATA, EVID, Manuskripte und PDF/DOCX-Ausgaben werden nicht nachtraeglich neu gestempelt.
