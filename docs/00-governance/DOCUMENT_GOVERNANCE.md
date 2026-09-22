# Dokument- und Forschungsgovernance

**Gültig ab:** 15. September 2026  
**Geltungsbereich:** `docs/**` und `research/**`

## Zweck

MHRN trennt ab dieser Fassung systematisch zwischen aktueller normativer Dokumentation, laufender wissenschaftlicher Arbeit, unveränderlichen Versuchsdaten, generierten Projektionen und historischen Fassungen. Ein Dateipfad allein darf nicht mehr als Aussage über wissenschaftliche Autorität interpretiert werden.

Jede Datei unter `docs/` und `research/` muss durch den maschinenlesbaren Governance-Audit einer Klasse zugeordnet werden. Nicht klassifizierbare Dateien lassen den Audit fehlschlagen.

## Pflichtfelder der Dateideklaration

Für jede Datei werden mindestens folgende Eigenschaften deterministisch abgeleitet oder explizit überschrieben:

| Feld | Bedeutung |
|---|---|
| `path` | repository-relativer Pfad |
| `domain` | `docs` oder `research` |
| `kind` | Dokumenttyp, z. B. policy, registry, publication, experiment, generated, source, data |
| `status` | `current`, `current_wip`, `frozen`, `historical`, `generated`, `experimental`, `superseded` oder `archive` |
| `authority` | wissenschaftliche/technische Autoritätsklasse |
| `mutability` | `editable`, `append_only` oder `immutable` |
| `citation` | wie die Datei zitiert werden darf |
| `evidence_role` | ob die Datei DATA/EVID tragen darf oder nur Interpretation/Navigation ist |
| `rationale` | warum diese Klassifikation gilt |

## Autoritätshierarchie

Für den aktuellen Projektstand gilt in absteigender Priorität:

1. Code, Schemas und maschinenlesbare Verträge auf `develop`; freigegebene Release-Snapshots auf `main`.
2. Kanonische Registry-Objekte unter `research/registry/` und `research/schemas/`.
3. Unveränderliche DATA/EVID- und Experimentartefakte mit Provenienz.
4. Aktuelle Quality-/Methodenverträge unter `docs/05-quality/` und aktuelle Roadmaps.
5. Die aktuelle WIP-Publikation laut `research/publications/catalog.json`.
6. Generierte Projektionen und Reports.
7. Historische, superseded und archivierte Dokumente.

Eine spätere Rangstufe darf eine frühere nicht rückwirkend umschreiben.

## Publikationsregeln

- `Recursive Epistemics 1.5` bleibt als **frozen empirical baseline** unverändert erreichbar.
- `1.6` ist die unmittelbare integrative Vorgängerfassung von `1.7`.
- `1.7` ist die aktuelle fortgeschriebene WIP-Fassung und wird im Publication Viewer direkt über `MANUSCRIPT.md` geöffnet.
- Eine WIP-Fassung darf neue Interpretation, Literatur, Nebenarbeiten und offene Hypothesen aufnehmen, aber keine historischen DATA/EVID-Entscheidungen verändern.
- Jede neue Hauptfassung nennt Vorgänger, empirische Baseline und ihren eigenen Review-/EVID-Status.

## Forschungsintegrität

Freier Wissenstransfer und strikte Attribution sind kein Widerspruch. Die Herkunft von Methoden, Ideen, Textbestandteilen, Daten und Code muss sichtbar bleiben, weil wissenschaftliche Nachprüfbarkeit sonst verloren geht. Ein interner Audit kann Attributions- und Text-Recycling-Risiken reduzieren, aber keine externe Plagiatsfreiheit zertifizieren.

## Physisches Aufräumen

Historische oder experimentelle Dateien werden nicht allein wegen einer unübersichtlichen Verzeichnisstruktur verschoben, wenn dadurch Pfade, Digests, Manifeste, Zitate oder Reproduzierbarkeit beschädigt würden. Die erste Bereinigungsstufe ist deshalb **semantisch und maschinenlesbar**: Klassifikation, Navigation und Fail-Closed-Audit. Physische Migrationen erfolgen nur mit Redirect-/Alias- und Provenienzvertrag.
