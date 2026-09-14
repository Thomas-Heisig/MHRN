# Nachtrag zu Fassung 1.5: Integration der Entwicklungsstufen 0-6

**Recursive Epistemics in Embodied Spiking Neural Architectures**

Thomas Heisig / MHRN. Redaktioneller Nachtrag vom 14. September 2026, KI-unterstuetzt; menschliche wissenschaftliche Pruefung ausstehend. Geltungsbereich: integrierte Softwarevertraege und Messmethodik, keine neue akzeptierte EVID und kein Bewusstseinsnachweis.

Dieser Nachtrag ergaenzt [Dissertationsmanuskript und Forschungsarbeit 1.5](../2026-09-13_recursive-epistemics_v1.5/README.md). Er ersetzt weder deren datierte Messkampagne noch die unveraenderten PDF-/DOCX-Exporte. Die bestehenden Nachtraege zu [Stage 4](../2026-09-14_stage4-specialized-areas_v1.5-addendum/README.md) und [Stage 5](../2026-09-14_stage5-integrated-nervous-system_v1.5-addendum/README.md) bleiben gueltige historische Bezuege.

## 1. Gegenstand und Provenienz

Die Zusammenfuehrung verwendet main `a72081ba6722343b0d4795ceee08f2e06ea9684c`, die Stage-5-Fortsetzung `68fb1a312e835ca90d1891dc006ff5900c44cbf9` und den Stage-6A-Stand `82bd5236d7db6d0252b7f5c9641023152b1d5edc`. Der Merge `68b3170426f68987effeeb2c3e2c7eb0b1e1a64e` bewahrt beide Entwicklungslinien. Spaetere Korrekturen dieses Nachtrags werden durch den Integrationscommit und dessen CI identifiziert, nicht durch eine Behauptung, dass alle frueheren Runs auf neuem Code ausgefuehrt worden seien.

Die Einheit des Audits ist ein deklarierter Softwarevertrag: Eingaben, Zustaende, Ausgaben, Fehlerverhalten und Fortsetzung. Die Einheit wissenschaftlicher Evidenz ist dagegen ein vorab festgelegter Vergleich unter geeigneten Kontrollen mit nachvollziehbaren Messwerten und unabhaengiger Bewertung. Weder das Vorhandensein einer Datei noch ein erfolgreicher Merge identifiziert beide Einheiten miteinander.

## 2. Kumulativer Stand der Stufen 0-5

Stage 0 liefert versionierte Einzelzellmodelle, deterministische Integration sowie Spike-, Reset- und Erholungsverhalten. Stage 1 verbindet diese Primitive ueber Synapsen und eine sparse Topologie. Stage 2 erweitert den Vertrag um Rekurrenz und reproduzierbare Fortsetzung. Diese Ergebnisse begrenzen die Aussage auf getestete numerische Modelle und Netzkonfigurationen; biologische Vollstaendigkeit oder beliebige Langzeitstabilitaet folgen daraus nicht.

Stage 3 verbindet zeitabhaengige und drei-faktorielle Plastizitaet mit Homeostase und strukturellen Anpassungen. Die technische Existenz einer Gewichtsaktualisierung beweist weder nuetzliches Lernen noch Transfer. Der wissenschaftliche Abschluss verlangt geeignete learning-on/off-, Sham- und gehaltene Testbedingungen mit unabhaengigen Wiederholungen. Das offene R2-Arbeitspaket wird nicht durch Engineering-Fortschritt geschlossen.

Stage 4 trennt Modalitaeten, Adapter, Projektionsbehandlungen und Gateway-Zustaende. Aggregierte Topologiebudgets sind keine gemessene dynamische Ausfuehrung an derselben Groesse. Die E01-E05-Daten und produktive Gateway-Aktivierung unterliegen weiterhin getrennten Freigaben. Stage 5 integriert technische Interozeption, autorisierte Aktorik und beobachtetes Feedback in einer begrenzten deterministischen Umgebung. Host-Telemetrie wird nicht als biologischer Stoffwechsel interpretiert. H-EMB-001-B erfordert weiterhin gematchte Stoerungsbedingungen, Yoked-Replay und unterbrochenes Feedback; der Integrationsschritt ist kein Ersatz fuer diesen Versuch.

## 3. Stage 6A: Beobachter statt implizitem Lernorgan

Der aktuelle Gedaechtnisspeicher ist eine begrenzte Sammlung expliziter Ereignisse. Der Einschritt-Praediktor verwendet beobachtete Uebergaenge und eine Persistenzreferenz. Beide liegen neben dem neuronalen Kern. Diese Architektur erlaubt kontrollierte Vergleichsmessungen, rechtfertigt aber nicht die Bezeichnung eines neuronalen semantischen Gedaechtnisses oder eines handlungssteuernden, mehrschrittig gelernten Weltmodells.

Episodenlesen, Episodenschreiben, Vorhersageausgabe und Praediktorlernen sind vier unabhaengige Operationen. Ihre vollstaendige faktorielle Kombination ergibt 16 Konfigurationen. Insbesondere impliziert deaktiviertes Episodenschreiben kein eingefrorenes Modell; deaktiviertes Lesen impliziert weder Loeschung noch Lernstopp. Die API legt beide Praediktorflags offen und respektiert die Lesesperre auch fuer den zuletzt gespeicherten Vorhersagedatensatz. Der LLM-Assistent erhaelt durch diese Aenderungen keine Schreibrechte an kanonischen neuronalen Zustaenden.

## 4. Messmethodik: Typen, Abdeckung und zeitliche Ordnung

Numerische Ziele werden je Feld durch ihren absoluten Fehler ausgewertet: `e_j = abs(yhat_j - y_j)`. Kategoriale Ziele werden durch einen Fehlindikator verglichen. Ein Wahrheitswert ist keine Zahl und die Zeichenkette `"false"` ist nicht gleich dem JSON-Wert `false`. Ein Ziel mit fehlender Vorhersage ist nicht automatisch fehlerfrei. Die Abdeckung ist das Verhaeltnis tatsaechlich verglichener zu unterstuetzten beobachteten Zielfeldern; fehlen Zielfelder insgesamt, ist sie nicht definiert und wird als JSON-null, nicht als numerische Null oder Eins ausgegeben.

Jedes optionale numerische Feld besitzt einen eigenen Beobachtungszaehler. Andernfalls wuerden Episoden ohne dieses Feld seinen Mittelwert systematisch verfalschen. Das Ausweisen eines gemischten Mittels aus numerischen Einheiten und kategorialen Indikatoren bleibt ausschliesslich Legacy-Telemetrie; dieser Wert ist keine wissenschaftliche Genauigkeit. Die aktuelle Oberflaeche zeigt deshalb die getrennten Fehlerkomponenten und exportiert hoechstens die gerade abgefragten 20 Datensaetze. Der Export ist weder eine vollstaendige Rohdatenbasis noch akzeptierte EVID.

Die Auswertung erfolgt prequenziell: Zuerst wird die Vorhersage aus dem bis dahin bekannten Zustand erstellt, danach wird die neue Beobachtung bewertet, erst anschliessend darf das Modell aktualisiert werden. Das verhindert innerhalb dieses Referenzpfads, dass die zu bewertende Zielbeobachtung bereits zur eigenen Vorhersagebildung verwendet wird. Externe Datenleckage, abhaengige Wiederholungen oder eine fehlerhafte Versuchsaufteilung werden dadurch nicht automatisch ausgeschlossen.

## 5. Persistenz, Wiederaufbau und Reproduzierbarkeit

Die v2-Persistenz speichert die FIFO-Reihenfolge explizit, damit Kapazitaetsverdraengung nach einem Laden dieselbe Fortsetzung ermoeglicht. Ein v1-Aggregat kann verlorene Kategorien-Typen und Einfuegereihenfolge nicht eindeutig liefern. Eine stille Migration waere daher eine unbelegte Rekonstruktion.

Der neue [explizite Wiederaufbau](../../specifications/STAGE6_REPLAY_FORMAT.md) nimmt ausschliesslich eine vollstaendig deklarierte Ereignis- und Steuerhistorie ab Reset mit erwartetem SHA-256 entgegen. Er schreibt in einen neuen Ordner und erzeugt einen Provenienznachweis einschliesslich Implementierungs- und Zustandshashes. Die Vollstaendigkeit bleibt eine Deklaration des Lieferanten und muss ausserhalb der Software belegt werden. Begrenzte Episodenlisten und Dashboard-Exporte sind nicht als Ersatz zulaessig. Dieses Verfahren ist ein statistischer Referenz-Wiederaufbau, kein neuronales Replay, keine synaptische Konsolidierung und kein Restore des gesamten laufenden Systems.

## 6. Verifikation und negative Befunde

Der erste gemeinsame Integrationslauf `34877066028` bestand 1406 schnelle Python-Tests und verfehlte einen AIRR-Fallback-Test; 32 langsame Tests waren nicht ausgefuehrt. Zusaetzlich scheiterte die Formatierung an fuenf Dateien. Diese negativen Ausgangsbefunde bleiben dokumentiert. Die Korrektur markiert ein fehlendes oder leeres Analyse-Assessment als nicht verfuegbare Analyse, statt eine formal normalisierte Antwort als wissenschaftlich brauchbare Interpretation auszugeben. Das bestehende Verbot vom Modell erfundener quantitativer Statistiken bleibt unveraendert.

Neue Regressionen pruefen den Referenz-Wiederaufbau, unabhaengige Schalter, Verweigerung ungueltiger Historien, echte HTTP-Lesesperren, feldweise Fehler und beide Browser-Servervarianten. Der Browser verwendet explizit synthetische Referenzdaten im Testserver; daraus ergibt sich keine SNN-Leistungsbehauptung. Der autoritative Verifikationsstand ist die abgeschlossene CI des exakten Endcommits. Ein laufender, alter oder uebersprungener Check wird nicht als aktueller Erfolg ausgegeben.

## 7. Verbleibendes Forschungs- und Entwicklungsprogramm

Vor einem Abschluss von Stage 6 fehlen die Einbindung des gekoppelten Kognitionszustands in den kanonischen Runtime-Checkpoint mit Fortsetzungsidentitaet, ein expliziter neuraler Erinnerungs-/Konsolidierungsmechanismus, semantische Generalisierung, ein gelerntes Mehrschritt-Weltmodell und eine kontrollierte lernwirksame Nutzung von Vorhersagefehlern. Jede dieser Erweiterungen benoetigt ein eigenes Zustands-, Ressourcen- und Abbruchmodell; ein zusaetzlicher Cache oder eine Statistikklasse reicht dafuer nicht aus.

Fuer RQ-MEM-002 und RQ-WM-001 sind gehaltene Aufgaben, getrennte Trainings-/Testphasen, Informationszerstoerungs-, Persistenz-, Fixed-/Random- und Lernabschaltkontrollen sowie SNN-involvierte Ausfuehrungen mit unabhaengigen Seeds erforderlich. Dieses Dokument spezifiziert Folgeanforderungen; es behauptet keine hier neu durchgefuehrte konfirmatorische Kampagne. Eine Annahmeentscheidung, ethische Freigabe oder Bewusstseinszuschreibung verbleibt ausserhalb automatischer Engineering-Gates.

## Quellen im Repository

[Integrationsaudit](../../../docs/07-changelog/2026-09-14_STAGES_0_6_INTEGRATION.md), [Stage-6-Vertrag](../../specifications/STAGE6_REFERENCE_CONTRACT.md), [Replayformat](../../specifications/STAGE6_REPLAY_FORMAT.md), Implementierungen `src/memory/{store,world_model,layer,prediction_metrics,replay}.py`, `src/dashboard/server.py` und `src/experience/composition.py`. Testquellen und kanonische offene Punkte werden durch `python -m scripts.audit_stages_0_6` als read-only Inventar mit Quellcommit und Source-Digest ausgegeben. Diese technischen Quellen tragen die hier beschriebenen Codeaussagen; sie ersetzen keine externe wissenschaftliche Begutachtung.
