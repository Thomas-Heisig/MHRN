# Diese Arbeitsfassung zitieren

Heisig, T. (2026). *Rekursive Epistemik in verkörperten spikenden neuronalen Architekturen* (Edition 1.8, Arbeitsmanuskript). MHRN.

Maschinenlesbare Metadaten für die Publikation: [`CITATION.cff`](CITATION.cff).

Die Software und die wissenschaftliche Arbeit bleiben zwei getrennte zitierbare Objekte:

- Repository-Root `CITATION.cff`: MHRN-Software, Autor **Thomas Heisig**, Lizenz **MIT**.
- Edition-1.8-`CITATION.cff`: Publikationsbundle der Edition 1.8, ebenfalls Autor **Thomas Heisig**, Lizenz **MIT**; die eigentliche Arbeitsfassung ist dort als `preferred-citation` vom Typ `unpublished` angegeben.

CFF 1.2 erlaubt auf oberster Ebene nur `software` oder `dataset`. Deshalb beschreibt die editionsspezifische Datei den versionierten Publikationsordner als `dataset` und verweist für die zu zitierende Arbeit auf `preferred-citation`. Das ist eine Metadatenmodellierung, keine Behauptung, das Manuskript selbst sei ein Datensatz.

Beim Zitieren zusätzlich den exakten Git-Commit, Kapitel/Abschnitt und das Abrufdatum nennen. Für Vorfassungen deren Edition und Ursprungspfad nennen. Es wird kein DOI und kein Peer Review behauptet.


## Autorenschaft und Verantwortlichkeit

**Autor:** Thomas Heisig  
**Wissenschaftlich verantwortliche Person:** Thomas Heisig

KI-Systeme wurden als Recherche-, Synthese-, Kritik-, Programmier- und Formulierungswerkzeuge eingesetzt. Sie werden nicht als Autoren, Primärquellen oder Evidenzinstanzen geführt. Die Verantwortung für Quellenprüfung, Auswahl, Interpretation, Grenzen der Claims und die veröffentlichte Fassung liegt beim menschlichen Autor.

### CRediT-Beitragsrollen

Für Thomas Heisig werden für Edition 1.8 folgende Rollen ausgewiesen:

- Conceptualization
- Methodology
- Software
- Investigation
- Data curation
- Formal analysis
- Validation
- Visualization
- Project administration
- Writing – original draft
- Writing – review & editing

Die CRediT-Rollen beschreiben Beiträge und ersetzen keine venue-spezifischen Autorenschaftskriterien.

## Zitations- und Quellenregel

Die wissenschaftliche Textschicht verwendet Autor-Jahr-Zitation nach APA 7. Primärliteratur wird für ursprüngliche empirische, methodische oder theoretische Befunde bevorzugt. Review, Survey und Synthese werden als Sekundärliteratur gekennzeichnet. Richtlinien und Standards werden separat ausgewiesen und erzeugen keine Evidenz für MHRN-Mechanismen.

Die maschinenlesbare Quellenklassifikation steht in `sources/references.json`; die lesbare Ausgabe mit vollständigen Autorlisten und Quellenstatus steht in `REFERENCES.md`.
