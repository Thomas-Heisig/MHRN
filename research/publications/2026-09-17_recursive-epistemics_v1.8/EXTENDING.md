# Erweiterungs-, Quellen- und Editionsvertrag

Edition 1.8 ist die lebende, elfteilige Arbeitsfassung. Die Zielgliederung 2.0 wird bereits umgesetzt, ohne eine wissenschaftliche Fertigstellung, ein Software-Release 2.0 oder eine formale akademische Anerkennung zu behaupten.

## Ein neuer Forschungsbaustein

Jeder Baustein erhaelt eine stabile Kennung, Forschungsachse, Thema, Entwicklungsphase, Provenienzklasse, Evidenzmodus, Status, Quellreferenzen und ein Revisionskriterium. Bei empirischen Arbeiten werden RQ, H, Protokoll, Run, DATA, Review, EVID und Claim nicht in ein gemeinsames Statusfeld gepresst. Kanonische Registrierungen erfolgen weiterhin in `research/registry/`; Publikationsregister sind lesbare Projektionen, keine Ersatzregister.

Die bearbeitbaren Texte stehen in `parts/`. Reihenfolge und Titel stehen in `edition.json`. Neue Unterkapitel werden in dem zugehoerigen Teil ergaenzt; neue Hauptteile verlangen eine begruendete Schema-/Editionsaenderung. Offene Ideen werden mit Status und Aufnahmegrund erhalten. Nicht weiterverfolgte Ideen erhalten eine begruendete Disposition, keinen stillen Loeschvorgang.

## Quellen und Zitation

Die neue Textschicht verwendet ein einheitliches Autor-Jahr-System in Anlehnung an APA 7. `[@SCHLUESSEL]` in den Kapitelquellen wird beim Bauen zu einer Autor-Jahr-Verknuepfung mit `REFERENCES.md`. Alle verwendeten Schluessel muessen in `sources/references.json` stehen. Dort werden Identitaet, Originalquelle, Datum und tatsaechlich gepruefter Leseumfang getrennt erfasst. Ein Metadatencheck ist kein Volltextreview.

Woertliche Zitate benoetigen Anfuehrungszeichen oder Blockzitat, Autor, Jahr und Seite beziehungsweise ueberpruefbaren Abschnitt/Absatz. Eigene Uebersetzungen werden als solche bezeichnet. Paraphrasen behalten die Quelle; inhaltliche Umformulierungen duerfen den Geltungsbereich nicht vergroessern. Sekundaerzitate werden als solche gekennzeichnet. Tabellen, Abbildungen, Daten und Code benoetigen Herkunft und gegebenenfalls Lizenz-/Nutzungspruefung; eine Literaturangabe ersetzt keine Erlaubnis. Eigene Vorarbeiten werden mit Edition, Pfad und Git-Revision zitiert.

Verifizierte Literatur wird nicht rueckwirkend zur Literatur der urspruenglichen Idee erklaert. `ArithSpec` und andere nicht belastbar bestaetigte Norm-/Neuheitsbehauptungen bleiben im bestehenden Quarantaeneprozess. Die historischen Quellenbaende bewahren alte Bibliografien, zertifizieren sie aber nicht. Externe Similarity-Pruefung und menschlicher Quellenabgleich vor Einreichung bleiben offen; dieser Build stellt kein Plagiatsfreiheitszeugnis aus.

## Rekonstruktion und Datenschutz

Zusammenfassungen frueherer Chats bleiben S4. Erst ein ueberprueftes Original kann ein zeitgenoessisches Prozessartefakt S2 begruenden. Der Zeitpunkt der Wiederauffindung ist nicht der Zeitpunkt der Idee. Zitatgenaue Formulierungen und behauptete erste Urheberschaft werden aus Zusammenfassungen nicht erzeugt. Autoranforderung, KI-Vorschlag, tatsaechlicher Commit und Experimentausfuehrung sind verschiedene Ereignisse.

Nur thematisch erforderliche KI-Forschung wird in das oeffentliche Repository uebernommen. Unbeteiligte Personen, Geschaeftskorrespondenz, private Kontaktdaten und nicht erforderliche sensible Selbstauskuenfte werden nicht aus dem Gespraechsarchiv exportiert.

## Reproduzierbarer Build

In einem vollstaendigen Git-Checkout mit Python und PyYAML:

```bash
python scripts/build_publication_edition.py --write
python scripts/build_publication_edition.py --check
python -m pytest tests/test_publication_edition.py -q
python scripts/check_scientific_maturity_integrity.py
python scripts/audit_document_governance.py --write
```

Der Quellstand der Vorgaenger wird durch `baseline_commit` fixiert. Alle damals versionierten Git-Dateien werden mit SHA-256 und Blob-ID erfasst, alle Markdown-Ueberschriften in `docs/` und `research/` indiziert. Dateipfadregeln sind vorlaeufige thematische Zuordnungen und duerfen nicht als vollstaendiger semantischer Review ausgegeben werden. LFS-Zeiger und LFS-Nutzdaten muessen ausdruecklich unterschieden werden. Neue Originalimporte benoetigen eigene Bytes-/Formelpruefung und Quellenrechte.

`MANUSCRIPT.md`, Quellenband, Register und Literaturausgaben werden generiert, nicht von Hand korrigiert. Aenderungen erfolgen in den Inputs und werden dann neu gebaut. Die Pruefroutine vergleicht die generierten Outputs und erkennt veraltete Ableitungen. Historische Publikationen bleiben an ihrem bestehenden Ort; fruehere DATA werden nicht neu berechnet oder ueberschrieben. Registry-Updates duerfen neue Ausgaben erzeugen, aber nicht rueckwirkend die Interpretation alter Experimente aendern.

## Review und Weiterfuehrung

Die 1.8-Struktur benoetigt getrennte technische und wissenschaftliche Reviews. Technisch geprueft werden reproduzierbarer Build, Referenzaufloesung, Zeigerkonsistenz, Erhaltung der Vorgaenger und unveraenderte Statusraeume. Inhaltlich geprueft werden Vollstaendigkeit der Themenzuordnung, Quellenpassung, Gegenargumente und zulaessige Reichweite der Synthese. Eine gruene CI erledigt nur den ersten Bereich.

Bei einem Freeze wird eine neue Edition eroeffnet. `CURRENT.md`, `catalog.json`, `project_identity.json`, Root-README und Viewer bleiben synchron. Die Softwareversion wird nur durch einen eigenstaendigen Software-Release veraendert. Eine neue Publikationsnummer veraendert weder Stage-Scores noch EVID-Entscheidungen.
