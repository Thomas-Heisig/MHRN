# Rekursive Epistemik in verkörperten spikenden neuronalen Architekturen

**Thomas Heisig · Edition 1.8 · current_wip · 17. September 2026**

> Die elfteilige Zielstruktur 2.0 wird hier als Edition 1.8 umgesetzt. Kein Software-Release 2.0, kein Peer-Review-Siegel und keine neue Evidenzentscheidung.

Vorgänger: [1.7](../2026-09-15_recursive-epistemics_v1.7/README.md). Unveränderte empirische Basis: [Frozen 1.5](../FROZEN_V1.5.md). [Erweiterungsvertrag](EXTENDING.md).

## Inhaltsverzeichnis

- [Teil I — Nullpunkt, Autor und Entstehungsbedingungen](#part-i)
- [Teil II — Schaffensgeschichte und Architekturgenese](#part-ii)
- [Teil III — Forschungsobjekt MHRN](#part-iii)
- [Teil IV — Empirisches Forschungsprogramm](#part-iv)
- [Teil V — Wissenschaftliche Infrastruktur und Engineering](#part-v)
- [Teil VI — Epistemologie und Methodik der Schaffensgeschichte](#part-vi)
- [Teil VII — Integrität, Autorschaft und kumulative Wissenschaft](#part-vii)
- [Teil VIII — Philosophie, Ethik und Sicherheit](#part-viii)
- [Teil IX — Rekursive Epistemik](#part-ix)
- [Teil X — Synthese und revidierbare Beiträge](#part-x)
- [Teil XI — Offene Forschungslandschaft](#part-xi)

<a id="part-i"></a>

# Teil I — Nullpunkt, Autor und Entstehungsbedingungen

## Lesepfade durch Edition 1.8

Edition 1.8 ist eine Gesamtarbeit und kein linear zu lesendes Einzelpaper. Die elf Teile folgen unterschiedlichen Evidenz- und Argumentationsregeln. Externe Leser können deshalb mit einem disziplinspezifischen Pfad beginnen und anschließend in die Querverweise, Register und Primärartefakte wechseln. Diese Lesepfade sind **Orientierung, keine fachliche Zuständigkeitsgrenze**.

| Perspektive | Empfohlener Einstieg | Schwerpunkt |
| --- | --- | --- |
| **Informatik / Engineering** | Teil II → III → IV → V → XI | Architekturgenese, Implementationsverträge, Experimente, Reproduzierbarkeit, offene technische Prüfungen |
| **Neurowissenschaft / Kognition** | Teil II → III → IV → VI → VIII | Modellgrenzen, neuronale Mechanismen, experimentelle Operationalisierung, biologische Plausibilität und Übertragungsgrenzen |
| **Philosophie / Ethik / Safety** | Teil I → VII → VIII → IX → X | Autorposition, Integrität, normative Grenzen, rekursive Epistemik und revidierbare Gesamtclaims |
| **Schnelle Gesamtübersicht** | Teil I → X → XI | Entstehungsbedingungen, gegenwärtig tragfähige Aussagen und offene Forschungslandschaft |

Wer einen empirischen Claim prüfen will, sollte nicht beim Fließtext enden: Teil IV führt zu den Experimentartefakten; `RESEARCH_REGISTER.md` verbindet Forschungsfragen und Hypothesen; `SOURCE_INDEX.md` und `CONTENT_INTEGRATION.md` dokumentieren Quellenbestand und semantische Einbindung. `DATA`, Human Review und `EVID` bleiben getrennte Autoritätsebenen.

## 1. Forschungsgegenstand vor dem Repository

Die 1.8-Fassung setzt nicht mit einem vermeintlich fertigen MHRN an. Sie behandelt die Entstehung selbst als Forschungsgegenstand. Die **früheste derzeit rekonstruierte Spur** ist `CER-RECON-20250421-01` in der [Chat-Rekonstruktion](sources/chat_reconstruction.json): ein lernender neuronaler Würfel sollte Zustand über Neustarts hinweg erhalten; nachladbare Funktionen sollten den lernenden Kern nicht unkontrolliert verändern. `CER-RECON-20250421-02` dokumentiert als weitere S4-Rekonstruktion Schichten, dynamische Verbindungen, Mutation sowie historische Traum-/Fantasie-Metaphern. `CER-RECON-20250421-03` trennt davon einen früheren KI-Vorschlag zu Koordinatenkodierung und SQLite-Speicher.

Diese Einträge gehören zur **Quellennäheklasse S4**: rekonstruierte Gesprächszusammenfassungen ohne vollständiges Originaltranskript. Sie belegen weder den tatsächlichen ersten Gedanken noch wissenschaftliche Priorität, Implementierung oder Funktionsnachweis. Die gleiche Grenze ist im Vorgängerwerk `PW-NEUROGENESIS-2025` des [Prior-Work-Registers](sources/prior_work.json) festgeschrieben.

Der historische Wert liegt deshalb nicht in einer Prioritätsbehauptung, sondern in der Problemkontinuität: Wie kann ein System Zustand behalten, ohne ein Sprachmodell oder eine Datenbank fälschlich als neuronales Gedächtnis zu zählen? Wie lässt sich Wachstum zulassen, ohne die Kausalität zu verlieren? Wie kann ein technisches System zugleich offen erweiterbar und wissenschaftlich prüfbar bleiben? Diese Fragen erscheinen später in strengeren Formen wieder: als Persistenzvertrag, Retrieval-Isolation, strukturelle Plastizität, Capability-Gates, Experimentregister und Evidenzgrenzen.

## 2. Autorposition

Thomas Heisig wird in dieser Arbeit als Autor, Projektleiter und wissenschaftlich verantwortliche natürliche Person geführt. KI-Systeme können Recherche-, Kritik-, Generierungs-, Analyse-, Programmier- und Formulierungsbeiträge leisten. **Ob ein konkreter KI-Beitrag epistemisch materiell ist, ist von formaler Autorenschaft, Entscheidungsmacht und wissenschaftlicher Verantwortung getrennt zu beurteilen.** Genau diese Trennung ist Gegenstand von `RQ-ETH-001` und des [Provenienz- und Beitragsprotokolls](../../protocols/RQ_ETH_001_PROVENANCE_STUDY.md).

Damit gilt ausdrücklich nicht mehr die vereinfachende Gleichung „KI = bloßes Werkzeug“. Ein Assistenzsystem kann beispielsweise eine Kontrollbedingung, einen methodischen Einwand oder eine Hypothesenvariante erzeugen, die den weiteren Forschungsweg materiell verändert. Daraus folgt jedoch weder automatische Quellenautorität noch formale wissenschaftliche Autorenschaft oder Verantwortung.

Die Selbstauskunft des Autors ist eine Primärquelle für Motivation und Arbeitsweise, jedoch keine empirische Evidenz über neuronale Mechanismen. Persönliche Intuition kann Forschungsfragen erzeugen; sie darf keine Hypothese bestätigen. Die vollständige Selbstauskunft bleibt als versioniertes Provenienzartefakt in [`AUTHOR_AND_CREATION_PRACTICE.md`](../2026-09-15_recursive-epistemics_v1.7/AUTHOR_AND_CREATION_PRACTICE.md) erhalten und wird im Hauptmanuskript nur soweit zusammengefasst, wie sie die wissenschaftliche Methode betrifft.

### 2.1 Autorenschaft, Beitragsrollen und KI-Offenlegung

**Autor und wissenschaftlich verantwortliche Person dieser Edition ist Thomas Heisig.** Autorenschaft bedeutet hier nicht nur Namensnennung, sondern Verantwortung für Auswahl, Prüfung, Interpretation, Begrenzung und Veröffentlichung wissenschaftlicher Aussagen. Externe Publikationsrichtlinien verbinden Autorenschaft ebenfalls mit Verantwortlichkeit und Rechenschaftspflicht; AI-Systeme werden deshalb nicht als Autoren geführt, weil sie diese Verantwortung nicht übernehmen können ([ICMJE, 2026](REFERENCES.md#ref-ICMJE2026)).

Für die transparente Beschreibung menschlicher Beiträge wird ergänzend die CRediT-Taxonomie verwendet; sie beschreibt Beitragsrollen, entscheidet aber nicht selbst darüber, wer Autor ist ([NISO, 2022](REFERENCES.md#ref-CREDIT2022)). Für Thomas Heisig werden in Edition 1.8 derzeit folgende Rollen ausgewiesen: **Conceptualization, Methodology, Software, Investigation, Data curation, Formal analysis, Validation, Visualization, Project administration, Writing – original draft sowie Writing – review & editing**.

Für KI-Systeme wird dagegen zwischen **Beitragsprovenienz** und **Autorschaft** unterschieden. Ein KI-System kann einen materiellen Beitrag zu Konzeptualisierung, Generierung/Transformation, Analyse oder Validierung leisten. Die Annahme, Revision, Verwerfung oder Kanonisierung einer wissenschaftlichen Aussage sowie die formale Verantwortung bleiben davon getrennt. Diese Unterscheidung wird in `RQ-ETH-001` mit Claim-Episoden und einer Contribution-&-Accountability-Matrix operationalisiert.

Literaturangaben, Tatsachenbehauptungen und daraus abgeleitete wissenschaftliche Aussagen bleiben in menschlicher Verantwortung; bei einer externen Einreichung muss die konkrete Nutzung von AI-Werkzeugen zusätzlich nach den Regeln des Zieljournals offengelegt werden ([ICMJE, 2026](REFERENCES.md#ref-ICMJE2026)).

Die wissenschaftliche Textschicht verwendet ein Autor-Jahr-System nach **APA 7** ([American Psychological Association, 2020](REFERENCES.md#ref-APA2020)). Primärliteratur wird für ursprüngliche empirische, methodische oder theoretische Befunde bevorzugt; Sekundärliteratur wird dort verwendet und als solche ausgewiesen, wo Review, Survey oder Synthese die Einordnung trägt.

## 3. Von Metaphern zu Operationen

Frühe Begriffe wie „DNA“, „Traum“, „Fantasie“, „Emotion“ oder „Gehirn“ werden historisch erhalten, aber nicht rückwirkend biologisch aufgeladen. Die S4-Rekonstruktion `CER-RECON-20250421-02` belegt ihre Verwendung als frühe Designmetaphern, nicht als biologische oder phänomenale Befunde. In der heutigen Terminologie werden solche Begriffe nur dann verwendet, wenn eine messbare technische Entsprechung definiert ist.

Offline-Replay ist nicht Schlaf. Ein Aktivierungs- oder Salienzparameter ist kein Gefühl. Parametervererbung ist keine biologische Genetik. Eine adressierte 5D-Struktur ist kein anatomisches Gehirn.

Diese Entmetaphorisierung ist kein Verlust der ursprünglichen Ideen. Sie macht sie prüfbar. Der Weg von einer anschaulichen Analogie zu einer operationalisierten Variable wird als Teil der Schaffensgeschichte dokumentiert, damit spätere Leser unterscheiden können, was Inspiration, Spezifikation, Implementierung, Messung und Interpretation war.

## 4. Nullpunkt und rekonstruierte Vorgeschichte

Edition 1.8 behauptet keinen exakt datierten „ersten Gedanken“. Für Zeiträume außerhalb des Git-Verlaufs stehen teilweise nur rekonstruierte Gesprächszusammenfassungen oder später wiedergefundene Dokumente zur Verfügung. Die [Chat-Rekonstruktion](sources/chat_reconstruction.json) führt diese Einträge in der **Quellennäheklasse S4**, solange kein originales, datiertes Primärartefakt geprüft wurde. Wo Originalnachrichten oder Originaldateien fehlen, lautet die wissenschaftlich korrekte Aussage „rekonstruiert“ oder „nicht rekonstruierbar“, nicht eine erfundene Präzision.

Damit ist Teil I bewusst erweiterbar. Neue Primärartefakte können die Chronologie verdichten oder korrigieren. Sie dürfen bestehende Versionen aber nicht stillschweigend überschreiben. Jede neue historische Zuordnung braucht Quelle, Datum beziehungsweise Datumsunsicherheit und eine Aussage darüber, ob sie Autoranforderung, KI-Vorschlag, Implementierung, Messung oder spätere Interpretation dokumentiert.

### 4.1 Die ursprüngliche Problemfamilie

Die rekonstruierten Vorarbeiten zeigen keine einzelne „Ur-Idee“, sondern eine wiederkehrende Problemfamilie. Für die frühe Phase sind insbesondere `CER-RECON-20250421-01` bis `-03` sowie `PW-NEUROGENESIS-2025` die derzeitigen Herkunftsanker. Aus ihnen lassen sich sechs wiederkehrende Fragen rekonstruieren:

1. Wie kann ein neuronales System **über Neustarts hinweg** einen wissenschaftlich definierten Zustand behalten?
2. Wie kann ein Netzwerk **wachsen, sich verbinden und verändern**, ohne dass der Veränderungspfad unprüfbar wird?
3. Wie lassen sich **räumliche oder funktionale Nachbarschaften** so repräsentieren, dass daraus später experimentierbare Geometrie entsteht?
4. Wie kann externe Software — Datenbank, Sprache, Plugin, Werkzeug — genutzt werden, ohne sie fälschlich als **intern gelerntes neuronales Wissen** auszugeben?
5. Wie können Offline-Phasen, Replay und Rekombination genutzt werden, ohne Metaphern wie „Traum“ oder „Fantasie“ als empirische Tatsachen zu behandeln?
6. Wie kann ein System modular erweiterbar bleiben, ohne dass jedes neue Modul automatisch Schreibrechte auf den kausalen Lernkern erhält?

Diese Kontinuität erklärt einen Teil der späteren Architektur, ohne eine lineare oder notwendige Entwicklung zu behaupten. Die heutige Trennung von Content Gateway, Compute Backend, neuronaler Persistenz, Retrieval-Isolation, Capability-Gates und struktureller Mutation kann genealogisch auf diese frühen Mehrdeutigkeiten bezogen werden; ihre heutige wissenschaftliche Gültigkeit muss jedoch jeweils separat durch Architekturverträge und Experimente getragen werden.

### 4.2 Aus Brain-5D übernommene Forschungsräume

Das `PW-FRAMEWORK-02` zugeordnete **Brain-5D Scientific Framework v0.2** vom 16. August 2026 verdichtete die frühe Ideenlandschaft zu einem expliziteren wissenschaftlichen Programm. Das [Prior-Work-Register](sources/prior_work.json) hält zugleich fest, dass der im Repository sichtbare DOCX-Pfad als LFS-Objekt behandelt wird und historische Evidenzklassen nicht automatisch in heutige `EVID`-Entscheidungen überführt werden.

Darin erscheinen Forschungsräume, die bis heute fortwirken:

- mehrdimensionale Adress- und Geometriehypothesen;
- unterschiedliche Neuronmodelle und Zeitskalen;
- STDP, Eligibility, Drei-Faktor-Lernen, Homeostase und strukturelle Plastizität;
- Graphnullmodelle, Motive, Stabilität, Metastabilität und kritische Dynamik;
- Information, Decoding, Representational Similarity und temporale Generalisierung;
- Gedächtnis, Continual Learning, Replay, Vorhersage und Language Organ;
- Storage, digitaler Zustand, Embodiment, Safety und Ressourcenskalierung.

Edition 1.8 übernimmt diese Räume nicht als bestätigte Theorie, sondern als **Genealogie der Forschungsfragen**. Mehrere Begriffe wurden inzwischen eingeengt: „5D“ ist keine Naturbehauptung; „Digital Twin“ ist ohne physisches Gegenstück zunächst ein reproduzierbarer digitaler Zustand; „Language Organ“ ist kein autoritativer Lernkern; „Homeostase“ bezeichnet eine technische Regelklasse, solange biologische Homologie nicht gezeigt wurde.

### 4.3 Die Schaffensart als methodischer Risikofaktor

Die kanonische Selbstauskunft [`AUTHOR_AND_CREATION_PRACTICE.md`](../2026-09-15_recursive-epistemics_v1.7/AUTHOR_AND_CREATION_PRACTICE.md) beschreibt einen stark parallelen, werkstattartigen Arbeitsmodus: Problem sichtbar machen, Randbedingungen benennen, Mechanismus isolieren, einen testbaren Eingriff definieren, ausführen, messen, Abweichungen dokumentieren und erst danach verallgemeinern. Sie dokumentiert zugleich einen selbst beschriebenen Abschluss- und Ordnungsdrang. Beides ist **Selbstauskunft**, keine unabhängige psychologische oder wissenschaftliche Evidenz.

Methodisch relevant ist das daraus abgeleitete Risiko: **Struktur lässt sich schneller schließen als Empirie.** Technisch vollständige Module, UI-Zustände oder plausible Architekturen können einen Reifegrad suggerieren, den die experimentelle Prüfung noch nicht trägt.

Die Antwort darauf ist eine methodische Selbstkorrektur: Engineering-Fertigstellung und Scientific Readiness werden getrennt; negative und Nullbefunde dürfen Architektur reduzieren; UI-Prozentwerte sind keine Fähigkeitsscores; eine neue Funktion erhält keinen wissenschaftlichen Status allein durch Integration. Die konkreten Fälle und aktuellen Evidenzstände werden nicht in Teil I fortgeschrieben, sondern in Teil IV, X und XI geführt.

### 4.4 Mensch-KI-Zusammenarbeit als reale Entstehungsbedingung

MHRN ist in einer Arbeitsweise entstanden, in der menschliche Zielsetzung, mehrere KI-Assistenten, Literaturrecherche, Codegenerierung, Review, Tests und Git-Provenienz eng verschränkt sind. Diese Konstellation wird nicht geglättet. Seit der Verdichtung von `RQ-ETH-001` wird sie nicht mehr nur als „Mensch plus Werkzeuge“, sondern als Folge unterscheidbarer epistemischer Ereignisse beschrieben:

- **Konzeptualisierung:** Wer erzeugt oder verändert Forschungsfrage, Ziel, Hypothese oder Erfolgsbedingung?
- **Generierung/Transformation:** Wer erzeugt Text, Code, Analyse, Kontrollidee oder methodische Variante?
- **Validierung:** Wer oder was prüft Quelle, Code, Messung, Statistik oder Konsistenz?
- **Selektion/Kanonisierung:** Wer entscheidet, was übernommen, revidiert, verworfen, als `DATA`/`EVID` behandelt oder veröffentlicht wird?
- **Verantwortung:** Welche natürliche Person kann für die veröffentlichte Aussage wissenschaftlich Rechenschaft übernehmen?

Die operative Einheit dafür ist die **Claim-Episode**. Commits, Runs, Reviews und Freigaben sind dabei Provenienzartefakte innerhalb einer Episode, aber nicht mit epistemischer Rolle oder Autorenschaft gleichzusetzen. Das Design ist in [`RQ_ETH_001_PROVENANCE_STUDY.md`](../../protocols/RQ_ETH_001_PROVENANCE_STUDY.md) festgelegt; es ist derzeit Protokolldesign und kein bestätigter empirischer Befund.

Diese Kette ist zugleich ein Gegenstand rekursiver Epistemik: Die Arbeit untersucht nicht nur ein lernendes System, sondern entsteht selbst in einem System aus Quellen, Modellen, Werkzeugen, Prüfungen, Entscheidungen und Statusänderungen.

### 4.5 Persönliche Motivation und ihre wissenschaftliche Grenze

Die vollständige persönliche Selbstauskunft bleibt außerhalb des wissenschaftlichen Kerntexts versioniert. Für Teil I genügt die methodisch relevante Feststellung: Der Autor beschreibt persönliche Nähe zu kognitiven Fragen, technische Praxis, einen stark parallelisierten Arbeitsmodus sowie einen Abschluss- und Ordnungsdrang als Motivation und mögliche Bias-Quellen. Diese Angaben erklären, **warum** bestimmte Fragen verfolgt werden können; sie besitzen keine Beweiskraft für deren Antwort.

Die verbindliche Regel lautet deshalb: **Nähe erzeugt Fragen, nicht Antworten.** Persönliche Erfahrung, Systemintuition oder interdisziplinäre Analogien dürfen einen Suchraum öffnen; sie ersetzen weder Fachliteratur, Statistik, Replikation, Ethikprüfung noch Peer Review.

Gerade weil MHRN außerhalb institutioneller Forschungsstrukturen entstanden ist, muss die Arbeit die Ebenen explizit trennen: Selbstauskunft, externe Theorie, implementierter Mechanismus, `DATA`, Human Review, `EVID`, Claim und offene Frage. Diese Trennung ist keine Kompensation durch Rhetorik, sondern ein prüfbarer Governance-Vertrag.


### 4.6 Parallele Theoriearbeit — „KI – Die geliehene Intelligenz“

Neben der technischen NeuroGenesis-/Brain-5D-Linie entstand eine zweite, theoretisch-reflexive Forschungslinie. Das im Prior-Work-Register als `PW-BORROWED-20260818` geführte Manuskript **„KI – Die geliehene Intelligenz: Genealogie maschineller Kognition, rekursive Technogenese und die Transformation menschlicher Agency“** untersuchte nicht primär SNN-Leistung, sondern Herkunft von Intelligenz, epistemische Abhängigkeit, menschliche Handlungsmacht, Kontrolle, Autorenschaft, Verantwortung und mögliche Verschiebungen menschlicher Rollen in zunehmend maschinell mitgestalteten Entwicklungsprozessen.

Teil I übernimmt daraus nur die **genealogische Funktion** der Theoriearbeit. Ihre Begriffe und Argumente werden nicht hier erneut entwickelt, sondern an ihren heutigen fachlichen Orten weitergeführt:

| Historischer Theoriebeitrag | Heutige Fortsetzung |
| --- | --- |
| „geliehene Intelligenz“, epistemische Genealogie, Fünf-Achsen-Modell `I=(M,E,G,Z,X)`, genealogische Distanz | Teil VI, IX und X |
| rekursive Technogenese, Rollenverschiebung, Ko-Kognition | Teil II, VIII und IX |
| Hoheitsvektor, Kontrollvektor, Autonomierisikomodell | Teil VIII und XI |
| asymmetrische Autorenschaft, Verantwortung, normative Regelhierarchie | Teil VII und VIII; operationalisiert insbesondere durch `RQ-ETH-001` |

Diese Vorarbeit ist **Theorie- und Argumentationsarbeit, keine experimentelle MHRN-Evidenz**. Ihre historischen F1–F24, H1–H12 und GH1–GH6 bleiben in den versionierten Vorgängerfassungen erhalten; Edition 1.8 übernimmt ihre wissenschaftlich materiellen Problemfamilien, ohne die alten Kennungen stillschweigend in heutige Registry-IDs umzuschreiben.

### 4.7 Konvergenz zweier Forschungsstränge

Die heutige Gesamtarbeit entstand deshalb nicht aus einer einzigen linearen Entwicklung, sondern aus der Konvergenz zweier Stränge:

1. **Technischer Strang:** NeuroGenesis → Brain-5D → MHRN. Leitend waren persistenter neuronaler Zustand, Plastizität, Topologie, Kausalitätsgrenzen, sensorisch-aktorische Kopplung und experimentelle Prüfbarkeit.
2. **Reflexiver Strang:** „Geliehene Intelligenz“ → rekursive Technogenese / Agency- und Kontrollfragen → rekursive Epistemik. Leitend waren Herkunft von Wissen und Intelligenz, Autorschaft, Verantwortung, menschliche Entscheidungsmacht und hybride Ko-Kognition.

Die Stränge beeinflussten einander, sind aber nicht evidenzgleich. Ein technischer MHRN-Lauf bestätigt keine gesellschafts- oder bewusstseinstheoretische These; umgekehrt begründet eine philosophische oder genealogische Argumentation keinen neuronalen Mechanismus. Ihre Verbindung besteht darin, dass MHRN zugleich **Forschungsobjekt** und **KI-assistiert hervorgebrachter Forschungsprozess** ist. Daraus entstanden die heutige Trennung von technischen Claims, Prozessgovernance, Beitragsprovenienz und normativen Grenzen.

## 5. Forschungsproblem und monographische Gesamtarchitektur

Edition 1.8 versteht sich als wissenschaftliche Monographie im Work-in-Progress-Status. Sie ist **keine eingereichte Dissertation und kein akademischer Gradanspruch**. Die Struktur folgt einer monographischen Forschungslogik: Problemstellung, Forschungsstand, Forschungslücke, Leitfrage, Teilfragen, Methodik, Ergebnisse, Diskussion, Limitationen und revidierbare Schlussfolgerungen werden sichtbar getrennt.

### 5.1 Übergeordnetes Forschungsproblem

Das Grundproblem dieser Arbeit ist nicht allein der Bau eines größeren spikenden Systems. Es lautet: **Wie kann eine modular wachsende, verkörperbare spikende Architektur so untersucht werden, dass technische Existenz, kausaler Mechanismus, empirischer Nutzen, Provenienz und normative Reichweite nicht miteinander verwechselt werden?**

Aus der Schaffensgeschichte folgt eine zweite Ebene: Das Forschungsobjekt verändert sich während seiner Untersuchung. Neue Module können neue Fragen erzeugen, negative Resultate können Architektur reduzieren, KI-Systeme können materielle epistemische Beiträge liefern, und die Dokumentation selbst beeinflusst spätere Entscheidungen. Deshalb muss nicht nur das System, sondern auch der Forschungsprozess kontrollierbar und revidierbar sein.

### 5.2 Zentrale Leitfrage

> **Wie lässt sich eine evolvierende spikende Forschungsarchitektur so entwickeln, operationalisieren und prüfen, dass behauptete Funktionalität und Lernkausalität durch explizite Kontrollen, Provenienz und revidierbare Evidenzverträge getragen werden, während stärkere kognitive, biologische oder normative Aussagen nur dort zugelassen werden, wo ihre eigenen Prüfbedingungen erfüllt sind?**

Diese Leitfrage ist eine **publikationsweite Leitfrage**, kein zusätzliches Objekt der kanonischen `RQ-*`-Registry. Sie bündelt mehrere registrierte Forschungsfragen mit unterschiedlichen Evidenzformen und darf deshalb nicht durch einen einzigen Lauf oder gemeinsamen Erfolgswert als „bestätigt“ behandelt werden.
 

### 5.2.1 Historische technische Leitfrage und Kernhypothese

Die heutige Leitfrage ersetzt nicht die technische Ausgangsfrage der Vorgängerfassungen. In Edition 1.5 wurde der technische Forschungsstrang noch enger formuliert:

> **Unter welchen Randbedingungen kann ein räumlich und funktional strukturiertes, kontinuierlich plastisches Spiking-Netzwerk durch sensorisch-aktorische Interaktion persistente, abrufbare und generalisierbare interne Zustände ausbilden, ohne dass deren semantischer Inhalt direkt durch ein externes Sprachmodell in synaptische Gewichte oder Netzwerkstruktur geschrieben wird?**

Dazu stand die historische Rahmenhypothese `CLAIM-CORE-001`:

> Ein rekurrentes Spiking-Netzwerk mit räumlich-funktionaler Topologie, lokaler zeitabhängiger Plastizität, homeostatischer Regulation, struktureller Anpassung, Ressourcenbegrenzung und geschlossener sensorisch-aktorischer Rückkopplung kann unter geeigneten Randbedingungen persistente und funktional unterscheidbare interne Zustände ausbilden, ohne dass diese Zustände explizit durch ein externes symbolisches Modell gesetzt werden.

Beide Formulierungen bleiben über die [Vorgängerfassung 1.5](../2026-09-13_recursive-epistemics_v1.5/section-005.md) provenancegebunden erhalten. Sie sind **historische Forschungsrahmen**, keine aktuelle pauschale `EVID` und keine zusätzlichen heutigen Registryobjekte. Edition 1.8 zerlegt ihren Inhalt in engere, falsifizierbare Forschungszweige zu Dynamik, Topologie, Plastizität, Repräsentation, Gedächtnis, Embodiment, Attribution und Skalierung.

### 5.3 Publikationsweite Syntheseproposition

Die leitende, revidierbare Syntheseproposition lautet:

> **Wissenschaftliche Reife entsteht in MHRN nicht durch die Addition möglichst vieler Mechanismen, sondern durch deren empirische Selektion unter expliziten Kontroll-, Provenienz- und Evidenzbedingungen.**

Diese Aussage ist **keine kanonische experimentelle `H-*`-Hypothese** und kein vorweggenommenes Ergebnis. Sie ist eine publikationsweite Syntheseproposition, deren Tragfähigkeit aus mehreren unabhängigen Forschungszweigen, Gegenbeispielen, Revisionen und Grenzen beurteilt wird. Sie muss revidiert werden, wenn die Forschungsarchitektur zwar formale Gates produziert, diese aber keine nachweisbare Verbesserung von Fehlersuche, Claim-Begrenzung, Reproduzierbarkeit oder Entscheidungsqualität bewirken.

### 5.4 Forschungszweige und Teilstudien

Teil I definiert die stabilen Forschungszweige und ihre Claim-Grenzen, **nicht deren tagesaktuellen Ergebnisstatus**. Aktuelle Befunde, negative Resultate, offene Hypothesen und Präregistrierungen gehören in Teil IV, X, XI und die kanonischen Register.

| Forschungszweig | Wissenschaftliche Kernfrage | Primärer methodischer Zugriff | Strukturelle Claim-Grenze |
| --- | --- | --- | --- |
| **Basale neuronale Dynamik und Determinismus** | Sind definierte Einzelzell- und Netzwerktrajektorien unter kontrollierten Bedingungen reproduzierbar und referenzkonform? | Referenzvergleich, Same-Seed-Replikate, Zustands-/Hash-Provenienz | Reproduzierbarkeit gilt nur für geprüfte Konfigurationen und begründet keine biologische Äquivalenz |
| **Rekurrenz, Topologie und 5D** | Welche Netzwerkunterschiede sind kausal auf Rekurrenz beziehungsweise Geometrie zurückzuführen? | matched controls, Ablation, Topologie-/Delay-Kopplung, Activity-Adequacy-Gates | Ein 5D-Claim verlangt aktivitätsadäquate und topology-matched Kontrollen; Dimensionalität allein ist kein Vorteil |
| **Plastizität und adaptive Dynamik** | Verändern STDP, Drei-Faktor-Regeln, Homeostase und Strukturplastizität Lernen oder Stabilität gegenüber geeigneten Kontrollen? | learning-on/off, Sham, Frozen, Perturbation und gehaltene Testdaten | Implementierte Gewichtsänderung ist weder Lernnutzen noch Generalisierung |
| **Spezialisierte Pfade und MSBA** | Liefern modalitätsspezifische und adaptive Pfade unter kontrollierten Ressourcenbedingungen messbaren technischen Nutzen? | kontrollierte Kosten-, Recovery-, Integritäts- und Ablationsvergleiche | Spezialisierung begründet weder emergente Hirnareale noch allgemeine Überlegenheit |
| **Embodiment** | Kann eine Sensor–SNN–Aktor–Feedback-Kette zielgerichtete Wirkung unter kontrollierten Störungen erzeugen und kausal vom Open Loop getrennt werden? | Closed Loop, Yoked-/Interrupted-Controls, matched disturbances | Synthetischer Closed Loop ist kein Nachweis allgemeiner Autonomie, Kognition oder Realweltübertragbarkeit |
| **Gedächtnis, Replay und Weltmodell** | Welche Retention stammt von Replay, semantischer Verdichtung oder einem tatsächlich kausal wirksamen Vorhersagemodell? | matched Replay, informationszerstörte Kontrollen, Holdout, Kompressions- und Modellkontrollen | Retrieval oder Verdichtung sind nicht automatisch neuronales Gedächtnis oder Weltmodell |
| **Epistemologie und Forschungsprozess** | Verbessern Provenienz-, Freeze-, Review- und EVID-Gates die Qualität wissenschaftlicher Entscheidungen? | Prozessrekonstruktion, Status-Audit, Kontrafaktik, Revisionstracing | Interne Governance ist keine unabhängige externe Validierung |
| **Ethik, Safety und Autonomie** | Welche Kontroll-, Ziel- und Welfare-Fragen entstehen bei zunehmender Wirk- und Lernfähigkeit? | normative Analyse, Szenarien, technische Safety-Verträge | Szenarien sind keine Prognosen; technische Zustände sind kein Bewusstseins- oder Sentienznachweis |

Damit besitzt jeder Forschungszweig einen eigenen wissenschaftlichen Gegenstand und eigene Evidenzregeln. Teil IV behandelt die empirischen Teilstudien und ihren jeweiligen Stand; Teil VI die epistemologische Methodik; Teil VII Integrität und Autorenschaft; Teil VIII die normative Analyse; Teil IX die Theorieentwicklung; Teil X die General Discussion; Teil XI Limitationen, offene Hypothesen und die priorisierte Forschungsagenda.


### 5.4.1 Genealogische Abbildung früherer Forschungsprogramme

Die folgende Zuordnung ist eine **Routing-Tabelle**, keine rückwirkende Umnummerierung. Historische Kennungen bleiben in ihren Originaleditionen; aktuelle `RQ-*`- und `H-*`-Objekte entstehen nur über die heutige Registry.

| Historische Familie | Wissenschaftlicher Kern | Heutige Fortsetzung |
| --- | --- | --- |
| Brain-5D `RQ1–RQ3` | Geometrie, Dynamik, Plastizität | basale Dynamik, Rekurrenz/Topologie/5D und Plastizitätsprogramme in Teil III/IV |
| Brain-5D `RQ4–RQ6` | Repräsentation, Gedächtnis, Continual Learning | Repräsentations-, Replay-/SemanticMemory- und Stage-6-Programme in Teil IV/XI |
| Brain-5D `RQ7–RQ10` | Embodiment, Language Organ, Emergenz, Skalierung | Embodiment-/Attributions-, Gateway-, Emergenz- und Scaling-Fragen in Teil III–V/XI |
| „Geliehene Intelligenz“ `F1–F5 / H1–H3` | Modell-/Promptabhängigkeit, Entwurfsfingerabdrücke, Mehrmodell-Provenienz | AI-/Beitragsprovenienz und rekursive Epistemik in Teil VI/VII/IX; kein automatisches 1:1-Registry-Mapping |
| `F6–F12 / H4–H6` | Kontrolle, Entscheidungshoheit, Autorenschaft, Verantwortung | insbesondere `RQ-ETH-001`, Teil VII/VIII/IX |
| `F13–F23 / H7–H11` | Selbstorganisation, Agency, Embodiment, Grounding, moralischer Status und soziale Rückkopplung | Embodiment-Forschung sowie philosophisch-ethische Analyse in Teil VIII/IX/XI |
| `F24 / H12` | menschliche Autorschaft unter KI-Mitstrukturierung und Ko-Kognition | `RQ-ETH-001`, `RQ-EPIST-002`, Teil VI/VII/IX |
| `GH1–GH6` | Gegenhypothesen zu geliehener Intelligenz, Kontrolle, Embodiment, Ko-Kognition und normativer Architektur | als Gegenpositionen und Revisionsdruck in Teil VIII–X; keine automatische Promotion in die heutige Registry |

Auch das siebenpunktige technische Beitragsprogramm der Vorgängerfassung — 5D-Geometrie, dynamischer Graph, Kausalitätsgrenzen, Trennung von Messung und Interpretation, reproduzierbarer Digitalzustand, Claim–Experiment–Evidence-Verknüpfung und Falsifikationsprogramm — wird deshalb nicht erneut als Liste von Neuheitsclaims geführt. Seine Bestandteile sind heute auf Teil III bis VII verteilt und dort mit strengeren Claim-Grenzen versehen.

Damit bleibt die frühere Forschung **auffindbar und genealogisch wirksam**, ohne dass Teil I die fachliche Detailarbeit der späteren Teile dupliziert.


---

<a id="part-ii"></a>

# Teil II — Schaffensgeschichte und Architekturgenese

## 5. Entwicklungsbogen

Die Schaffensgeschichte wird als Folge von Problemverschiebungen beschrieben, nicht als lineare Erfolgsgeschichte. Der frühe neuronale Würfel adressierte Persistenz, Wachstum und räumliche Organisation. Brain-5D machte daraus eine explizite mehrdimensionale Adress- und Geometriehypothese, verband sie mit spikender Dynamik, Plastizität, Homöostase, strukturellem Wachstum, multimodaler Kopplung und einer externen Sprachschnittstelle. MHRN verschärfte anschließend die Trennung zwischen Architektur, Experiment, DATA, Review, EVID und Claim.

Die Umbenennung Brain-5D → MHRN ist daher keine neue Evidenz. Sie reagiert auf die Gefahr, dass „5D“ als Naturbehauptung missverstanden wird. Fünf Koordinaten bleiben eine prüfbare Repräsentationsentscheidung; der aktuelle Projektname betont stattdessen Rekurrenz, Homöostase und Mehrskaligkeit.

## 6. Architekturentscheidungen und Revisionen

Mehrere heute zentrale Verträge lassen sich als Antworten auf frühere Mehrdeutigkeiten lesen. Ein persistenter Datenbankeintrag wird nicht als neuronales Gedächtnis behandelt. Ein LLM darf keinen stillen Schreibkanal in synaptische Gewichte oder Topologie erhalten. Monitoring und Intervention werden getrennt. Strukturänderungen werden proposal-, approval-, mutation- und journalfähig. CPU-/GPU-Beschleunigung darf keine wissenschaftliche Semantik verändern, ohne ihre Determinismusklasse offenzulegen.

Eine weitere Revision betrifft die Entwicklungslogik selbst. Frühe Phasen waren featuregetrieben: Eine plausible Funktion wurde implementiert und danach wissenschaftlich eingeordnet. Die heutige Regel dreht die Reihenfolge um: Forschungsfrage → Hypothese → minimale benötigte Fähigkeit → technische Validierung → Präregistrierung → autorisierte Ausführung → DATA → Analyse → Review → EVID → begrenzter Claim. Ein negativer Befund darf Architektur reduzieren, statt durch immer neue Rollenannahmen kompensiert zu werden.

## 7. Wissenschaftliche Verengung als Fortschritt

Die CL-001–CL-003-Linie ist ein wichtiges Beispiel. Ein kombinierter Semantic+Replay-Ansatz war gegenüber einer No-Replay-Baseline nützlich. Spätere, strengere Kontrollen zeigten jedoch keinen präregistriert bestätigten Zusatznutzen semantischer Verdichtung gegenüber gematchtem Raw-Replay; zugleich trug die semantische Repräsentation gegenüber einem Random-Prototype-Control relevante Struktur. Die Folge ist keine rhetorische Rettung, sondern eine engere Architekturposition: Replay bleibt Referenz, SemanticMemory ist ein Mechanismuskandidat mit begrenzter Rechtfertigung, bis Review und weitere explizit begründete Forschung etwas anderes tragen.

## 8. Nebenarbeiten als Genealogie, nicht als Ablage

Publikationen, Supplements, Frontend-/Viewer-Arbeiten, Safety-Programme, Spiegelmechanismen, Connectome-/Embodiment-Studien, biophysikalische Ablationsmodelle, Gedächtnis- und World-Model-Planung sowie Werkzeuge für lokale KI-Assistenten werden nicht als themenfremde Dateien behandelt. Edition 1.8 ordnet sie in die elfteilige Struktur ein und hält zugleich ihre ursprünglichen Pfade fest.

Ein maschinell erzeugter Quellenindex erfasst jede am Basiscommit versionierte Datei und jede Markdown-Überschrift unter `docs/` und `research/`. Diese Vollständigkeit ist eine **Bestandsvollständigkeit**, keine Garantie, dass jede Idee bereits semantisch perfekt klassifiziert wurde. Nicht klassifizierte Artefakte bleiben deshalb sichtbar und werden nicht gelöscht.

## 8.1 Architekturgenese in sechs Wendepunkten

### Wendepunkt A — Persistenz wird von „Speichern“ zu Zustandsvertrag

In der Vorphase war Persistenz zunächst ein praktisches Ziel: Der neuronale Zustand sollte einen Neustart überleben. Später zeigte sich, dass „gespeichert“ allein wissenschaftlich zu schwach ist. Ein reproduzierbarer Zustand benötigt eine definierte Grenze aus RNG, Neuronen, Synapsen, Delays, Queues, Plastizitätstraces, Strukturjournal, Homeostase, Ressourcen, Gedächtnis, Profilen, Gateway-Zuständen und gegebenenfalls Sensor-/Aktorinformationen.

Damit verschob sich die Frage von Datenhaltung zu **wissenschaftlicher Zustandsidentität**. Pause/Resume-Äquivalenz wurde ein prüfbarer Vertrag; Datenbankwissen wurde explizit von neuronaler Retention getrennt.

### Wendepunkt B — 5D wird von Leitmetapher zu offener Geometriehypothese

Brain-5D gab dem Projekt eine starke räumliche Leitidee. Mit wachsender wissenschaftlicher Strenge wurde aber sichtbar, dass eine Koordinate allein keine Funktion erzeugt. `EXP-GEN-0036` machte dies besonders deutlich: Die damalige 5D-v1-Studie variierte Dimensionen, koppelte die eigentliche Dynamik aber nicht ausreichend an Geometrie. Der Human Review klassifizierte die Frage für einen echten Geometrieeffekt als **nicht getestet**.

Diese Korrektur verändert die Architektur: Dimension darf künftig nur über einen präregistrierten Mechanismus wirken — etwa Nachbarschaft, distanzabhängige Konnektivität, Delay oder Plastizität. Der Name 5D ist damit keine Erklärung mehr, sondern ein experimenteller Faktor.

### Wendepunkt C — Plastizität wird auditierbar

Mit STDP, Eligibility, Drei-Faktor-Modulation, Homeostase und struktureller Plastizität wuchs die Gefahr, dass ein lernendes Netzwerk seine eigene Struktur auf schwer nachvollziehbare Weise verändert. Daraus entstand der Vertrag `Proposal → Approval → Mutation → Journal → Undo`.

Diese Kette ist mehr als Softwareorganisation. Sie trennt Hypothese, Freigabe, tatsächliche Mutation und Reversibilität. Dadurch kann eine Strukturänderung im Experiment gezielt erlaubt, verweigert, protokolliert oder zurückgenommen werden.

### Wendepunkt D — Multimodalität wird von „alles kann hinein“ zu typisierten Pfaden

Stage 4 ersetzte eine diffuse Multimodalitätsidee durch getrennte Audio-, Vision- und Digitalpfade mit unterschiedlichen Adaptern, Routingregeln und Plastizitätskandidaten. E01–E05 zerlegten die Frage weiter in Kosten, Ressourcenallokation, ROI/Foveation, digitale Integrität und Modalitätsverlust.

Damit wurde eine zentrale Grenze sichtbar: technisch spezialisierte Pfade sind noch kein Nachweis **emergenter** Spezialisierung. Vorgegebene Architektur und emergente funktionale Organisation werden seitdem getrennt behandelt.

### Wendepunkt E — Embodiment wird von Gerätezugriff zu kontrollierter Kausalität

Stage 5 verband Sensoren, Interozeption, Aktorik und Feedback. Gleichzeitig wurde der Zugriff auf reale Wirkungspfade stärker begrenzt: Discovery ist keine Aktivierung, Autorisierung ist ein eigener Status, und ein Effekt benötigt Acceptance-/Effect-Receipts.

Die 360-Run-Referenzkampagne zeigte, dass eine synthetische Sensor–SNN–Aktor–Feedback-Kette kontrolliert untersucht werden kann. Sie zeigte aber auch, welche stärkere Frage noch offen bleibt: Verbessert echter Closed Loop unter identischer externer Störung die Leistung gegenüber yoked Replay oder unterbrochener Rückmeldung?

### Wendepunkt F — Gedächtnis wird durch negative Evidenz vereinfacht

Stage 6 war zunächst architektonisch reich: episodische Pfade, semantische Prototypen, Replay, Prediction Error und World-Model-Kandidaten. Die CL-Experimente reduzierten diese Vielfalt epistemisch. Nachdem Raw-Replay als faire Kontrolle eingeführt wurde, verschwand der angenommene bestätigte Zusatznutzen der semantischen Verdichtung.

Die Architektur lernte daraus eine neue Regel: **Ein Mechanismus darf aus dem Zentrum verschwinden, wenn die Daten seinen Zusatznutzen nicht tragen.** Das ist ein wichtiger Unterschied zur frühen featuregetriebenen Phase.

## 8.2 Von Feature-Roadmap zu experimentgetriebener Entwicklung

Die heutige Roadmap ist nicht mehr primär eine Liste geplanter Fähigkeiten. Jede neue Fähigkeit muss an eine Forschungsfrage gebunden sein. Daraus folgt eine neue Reihenfolge:

`Frage → konkurrierende Hypothesen → minimale Fähigkeit → Verifikation → Freeze → autorisierter Lauf → DATA → Review → Architekturentscheidung`.

Diese Reihenfolge soll verhindern, dass Implementierung die Hypothese nachträglich definiert. Besonders bei Stage 6 wurde deutlich, dass ein bereits gebauter Mechanismus psychologisch schwerer zu verwerfen ist. Präregistrierte Stop-Regeln und eine explizite Referenzarchitektur wirken diesem Sunk-Cost-Effekt entgegen.

## 8.3 Die Nebenarbeiten als tatsächliche Architekturquellen

Mehrere scheinbar periphere Arbeiten haben die Kernarchitektur verändert:

- Der Publication Viewer führte zur klareren Trennung von aktueller WIP-Fassung, Vorgängern und Frozen Baseline.
- Die Dokumentgovernance führte zu Typ, Status, Autorität, Mutabilität, Zitierregel und Evidenzrolle pro Dokument.
- Lokale Chat-/Assistentensysteme schärften die Unterscheidung zwischen Interface-Gedächtnis und neuronaler Retention.
- AI-Review-Fehler führten zu strengeren Schema- und Provenienzgrenzen für automatische wissenschaftliche Auswertung.
- Safety-Arbeiten verschoben externe Aktorik zu deny-by-default, Capability-Gates und unabhängigen Stopppfaden.
- Spiegelmechanismus-Recherche verband Stage 4, 5, 6 und 7 zu einem neuen Querschnitt aus Wahrnehmung, Eigenhandlung, Prediction und Self/Other-Differenzierung.

Die Schaffensgeschichte ist deshalb nicht nur die Geschichte eines SNN-Kerns. Sie ist die Entstehung eines **Forschungssystems**, in dem technische Architektur und wissenschaftliche Governance zunehmend gemeinsam entworfen werden.


---

<a id="part-iii"></a>

# Teil III — Forschungsobjekt MHRN

## 9. Systemdefinition

MHRN ist ein Forschungsframework für rekurrente spikende Netzwerke mit explizitem Zeitverlauf, versionierten neuronalen und synaptischen Zuständen, Plastizitätsmechanismen, struktureller Veränderung, Homeostase, Persistenz, sensorischen/digitalen Gateways, Gedächtnis- und Vorhersagekandidaten sowie kontrollierten externen Werkzeugen. Das Framework untersucht nicht „Intelligenz“ als unteilbare Eigenschaft, sondern eine Folge operationalisierter Mechanismen und Funktionen.

Izhikevich-artige Neuronen sind eine recheneffiziente Modellfamilie mit unterschiedlichen Spike- und Burstregimen ([Izhikevich, 2003](REFERENCES.md#ref-IZHIKEVICH2003)). MHRN behandelt sie als austauschbare Dynamikklasse, nicht als biologisch vollständiges Neuron. LIF-, HH- oder Multi-Compartment-Varianten sind Ablations- oder Alternativmodelle; biologische Detailtreue wird nicht durch das bloße Hinzufügen von Kanalnamen erzeugt.

## 10. Rekurrenz, Plastizität und Homöostase

Rekurrenz ist ein Mechanismus, dessen funktionale Bedeutung kontrolliert werden muss. Dass eine rekurrente Bedingung mehr synaptische Ereignisse erzeugt als eine feedforward-nahe Kontrolle, ist zunächst ein Netzwerkbefund und noch kein Beleg für Gedächtnis, 5D-Vorteil oder höhere Kognition.

Für Plastizität trennt die Architektur lokale zeitabhängige Regeln, Eligibility und modulierte Drei-Faktor-Mechanismen. Der biologische Präzedenzfall enger spike-timing-abhängiger synaptischer Modifikation ist durch frühe experimentelle Arbeiten belegt ([Markram et al., 1997](REFERENCES.md#ref-MARKRAM1997); [Bi & Poo, 1998](REFERENCES.md#ref-BI_POO1998)); die kompetitive computationelle Formalisierung einer pair-based STDP-Regel ist in [Song et al., 2000](REFERENCES.md#ref-SONG2000) beschrieben. Diese Vorarbeiten begründen weder Neuheit noch funktionalen Lernnutzen der MHRN-Implementierung. Die Einordnung neuromodulierter Drei-Faktor-Regeln und zeitlicher Credit-Assignment-Fragen wird hier durch Sekundärliteratur gestützt ([Frémaux & Gerstner, 2016](REFERENCES.md#ref-FREMAUX2016)). In MHRN wird ein modulatorisches Signal dennoch nicht automatisch „Dopamin“ genannt. Entscheidend ist die experimentell definierte Funktion.

### 10.1 Synaptische und axonale Delays als eigenständige Prior Art

Zeitverzögerungen sind in SNNs kein MHRN-spezifischer Mechanismus. Izhikevich verband heterogene axonale Leitungsverzögerungen mit STDP und beschrieb daraus entstehende polychronous firing patterns ([Izhikevich, 2006](REFERENCES.md#ref-IZHIKEVICH2006)). Neuere Arbeiten behandeln Delays selbst als lernbare Parameter, unter anderem ereignisbasiertes Delay-Lernen in feedforwarden und rekurrenten SNNs ([Mészáros et al., 2025](REFERENCES.md#ref-MESZAROS2025)) sowie gemeinsames Lernen von Delays und synaptischen Gewichten ([Göltz et al., 2025](REFERENCES.md#ref-GOLTZ2025)).

MHRN trennt diese Literatur ausdrücklich von seinen derzeitigen Delay-Experimenten. Ein Vergleich fester rekurrenter Delay-Bedingungen — etwa in `RQ-REC-002` — ist **kein** Nachweis von Delay-Learning, Polychronisierung oder einer neuartigen Delay-Lernregel. Solche stärkeren Claims würden eigene Präregistrierungen, passende Kontrollarme und unabhängige Replikation benötigen. Die Delay-Prior-Art dient daher der historischen und methodischen Einordnung, ohne DATA-, EVID- oder Experimentstatus zu verändern.

Auch **Homeostase** wird nicht allein aus der MHRN-Terminologie abgeleitet. Aktivitätsabhängiges synaptisches Scaling ist als biologischer Mechanismus in Primärliteratur beschrieben ([Turrigiano et al., 1998](REFERENCES.md#ref-TURRIGIANO1998)) und in einer späteren Review systematisch eingeordnet ([Turrigiano, 2008](REFERENCES.md#ref-TURRIGIANO2008)). MHRN übernimmt daraus keine biologische Gleichsetzung: seine Regulations- und Homeostasepfade müssen als technische Mechanismen separat operationalisiert und experimentell geprüft werden.

## 11. Geometrie und 5D

Der fünfdimensionale Adressraum ist eine technische und wissenschaftliche Hypothese. Drei Dimensionen können räumliche/topologische Lokalität tragen, zwei weitere funktionale, modale, entwicklungsbezogene oder assoziative Nähe. Keine dieser Semantiken ist naturgegeben. Ein 5D-Effekt ist erst dann wissenschaftlich interessant, wenn Neuronen-, Synapsen-, Grad-, Delay-, Input- und Rechenbudgets gegenüber niedrigeren, gleichen und höheren Dimensionskontrollen hinreichend gematcht sind.

Edition 1.8 hält zusätzlich die frühere Idee lernbarer Metriken, dimensionsgekoppelter Distanz und sparse materialisierter Adressräume fest. Dabei wird klar zwischen Adressraum, materialisiertem Graphen und vollständigem dynamischen Zustandsraum unterschieden.

## 12. Gedächtnis, Replay und Weltmodell

Ein gespeicherter Zustand ist nicht automatisch Gedächtnis. Gedächtnis wird über Retention, cue-abhängigen Recall, Spezifität und Generalisierung operationalisiert. Complementary-Learning-Systems-Modelle motivieren unterschiedliche schnelle und langsame Lernprozesse sowie interleaved learning ([McClelland et al., 1995](REFERENCES.md#ref-MCCLELLAND1995)), doch MHRN übernimmt daraus keine fertige biologische Zuordnung.

Ein One-Step-Predictor ist ebenfalls kein vollständiges Weltmodell. Eine aktuelle SNN-Predictive-Coding-Übersicht zeigt verschiedene mögliche neuronale Repräsentationen von Prediction Error ([N'dri et al., 2026](REFERENCES.md#ref-NDRI2026)); eine primäre Spiking-World-Model-Arbeit mit modellbasierter Kontrolle setzt zugleich eine stärkere externe Referenz als passive One-Step-Telemetrie ([Sun et al., 2025](REFERENCES.md#ref-SUN2025)). Stärkere MHRN-Claims erfordern deshalb action conditioning, Mehrschrittrollouts, Unsicherheitskalibrierung, Out-of-Distribution-Prüfung und einen kausalen Entscheidungsnutzen gegenüber reaktiven/no-model/corrupted-model Kontrollen. Prediction Error muss, wenn er als neuronaler Mechanismus beansprucht wird, nachweisbar in Aktivität oder Lernen eingreifen.

## 13. Sprache, Wissen und externe Intelligenz

Das Language Organ ist außerhalb des kausal autoritativen SNN-Lernkerns positioniert. Es kann übersetzen, strukturieren, erklären, recherchieren oder Vorschläge erzeugen. Ein Eingriff in den Kern benötigt einen expliziten, protokollierten Gateway- und Policy-Pfad. Damit bleibt die Frage testbar, welche Leistung aus SNN, Retrieval, Decoder, Sprachmodell oder menschlicher Entscheidung stammt.

Diese Grenze schließt leistungsfähige hybride Systeme nicht aus. Sie verhindert nur, dass ein externer symbolischer Dienst unbemerkt als Beweis für intern gelerntes neuronales Wissen verwendet wird.

## 13.1 Tatsächlich erreichter Stand der Stages 0–10

Die Vorgängerarbeiten enthalten wesentlich mehr als eine Architekturdefinition. Der Forschungsgegenstand ist bereits durch eine Reihe implementierter und teilweise experimentell untersuchter Stufen konkretisiert. Die folgende Zusammenfassung ersetzt nicht die jeweiligen Primärartefakte, integriert aber ihre belastbare Aussage in den Haupttext.

### Stage 0 — einzelne Nervenzelle

Die Einzelzellprimitive ist nicht mehr nur technisch vorhanden. Für den begrenzten, explizit definierten Konformitätsumfang wurde ein wissenschaftlicher Readiness-Vertrag abgeschlossen. In `EXP-STAGE0-20260916-MODEL-CONFORMANCE-V2` wurden vorab eingefrorene Endpunkte auf disjunkten Confirmatory-Seeds gegen Brian2 2.10.1 geprüft. Für die Izhikevich-2003-Transition stimmten alle 192 confirmatory samples in ihren Spike-Entscheidungen überein; der größte beobachtete Vor-Reset-Spannungsfehler lag bei etwa `6.82e-13` und damit weit unter der eingefrorenen Schwelle `1e-8`. Für `lif-current-v1` waren in drei 1000-Tick/5-Zell-Vergleichen die Spike-Ereignisse identisch; der maximale Membranfehler lag bei ungefähr `7.11e-15`.

Die Arbeit brachte zugleich eine wichtige negative Erkenntnis hervor: Der frühere freie 1000-Tick-Izhikevich-V1-Vergleich bleibt als negativer Befund erhalten, weil kleinste numerische Differenzen in einem nichtlinearen freien Verlauf später zu abweichenden Spike-Zeitpunkten führen können. Damit wurde die Forschungsfrage präzisiert: Referenzkonformität muss zwischen lokaler Übergangs-/Reset-Konformität und langfristiger Trajektorienidentität unterscheiden.

Auch die LIF-Refraktärsemantik wurde explizit geklärt. Bei `dt=1 ms` entsprechen `refractory_ticks=1/2/3` in der validierten Zuordnung Brian2-Refraktärzeiten von `2/3/4 ms`; gleiche numerische Werte bedeuten also nicht automatisch gleiche Semantik. Für den 10-Hz-Homeostasecontroller wurde ein konfigurationsgebundener Arbeitsbereich dokumentiert: Eingangsströme 16–25 erreichten das Ziel ohne Aktuator-Sättigung, bei 30 wurde die +10-mV-Grenze erreicht. Dies ist ein Operating-Envelope-Befund, kein biologisches Universalgesetz.

Die präregistrierte Akzeptanzschwelle von `1e-8` war **vor der Confirmatory-Ausführung eingefroren**. Dass die beobachteten Fehler mit ungefähr `6.82e-13` und `7.11e-15` mehrere Größenordnungen darunter liegen, ändert den Erfolgsvertrag nicht nachträglich. Der Abstand zur Schwelle ist ein Robustheitshinweis innerhalb dieses Laufs, keine nachträglich verschärfte Entscheidungsregel.

Für externe Leser wird V1/V2 daher explizit als **zweistufige Aussage** behandelt: V1 prüfte die freie 1000-Tick-Trajektorienidentität und blieb negativ; V2 prüfte lokale Ein-Schritt-Transition, Threshold und Reset und fiel positiv aus. Diese Aussagen widersprechen einander nicht, weil nichtlineare freie Trajektorien mikroskopische numerische Differenzen über viele Schritte verstärken können.

`H-EVAL-006-C` gehört zudem zu einer anderen Claim-Klasse als A und B. C ist ein **Semantik-/Mapping-Resultat**: Bei `dt=1 ms` entspricht `refractory_ticks=1/2/3` in der validierten Zuordnung Brian2-`2/3/4 ms`. Es wird nicht als dritte numerische Konformitätsaussage dargestellt.

Der Human Review vom 18. September 2026 unterstützt ausschließlich den scoped Claim, dass die deklarierten V2-Einzelzellverträge unter dem eingefrorenen Protokoll mit der gematchten Brian2-2.10.1-Referenz innerhalb der präregistrierten Toleranzen konformieren. Ungeprüfte Modelle, andere Parameterregime, biologische Gleichwertigkeit, universelle Langzeittrajektorienidentität und unabhängige Replikation bleiben ausgeschlossen.

Der zugehörige maschinenlesbare Readiness-Status weist für den **scoped Stage-0 research-readiness contract 100 %** aus. Diese 100 % bedeuten ausschließlich: die dort definierten Prüfpunkte sind erfüllt. Menschlich reviewte EVID und unabhängig autorisierte Replikation bleiben getrennte Reifegates und sind damit nicht automatisch abgeschlossen.

### Stage 1 — kleines SNN

Stage 1 besitzt inzwischen mehr als den ursprünglichen technischen Small-SNN-Vertrag. Als zentrale wissenschaftliche Baseline gilt `RQ-SNN-003 / H-SNN-003-B` mit der gemeinsam geführten DATA-Linie aus `EXP-S1-TOPO-V2-20260918` und der korrigierten internen Replikation `EXP-S1-TOPO-V3-R1-20260918`. Beide Human Reviews durch Thomas Heisig sind abgeschlossen und akzeptieren die eng begrenzte Topologieinterpretation. Die Scientific-Maturity-Projektion beträgt damit 75 %: RQ/H, Protokoll, DATA und Attribution sind erfüllt; das Human-Review-Subgate ist abgeschlossen; kanonische EVID-Promotion und unabhängige Replikation bleiben offen.

Davon getrennt bildet `RQ-TEMP-002 / H-TEMP-002-A` mit `EXP-S1-TEMP-ORDER-V2-20260919` eine zweite task-basierte Funktionslinie. Sie prüft in einem kleinen acyclischen Sechs-Neuronen-SNN die Erhaltung zweier Kanalidentitäten und zeitlicher Reihenfolge gegen eine information-destroyed Kontrolle. Diese Linie ist DATA-seitig innerhalb des präregistrierten Protokolls unterstützt, aber noch nicht human-reviewed und keine Replikation des Topologieclaims.

Der zentrale Übergang zu Stage 2 ist deshalb weder „mehr Neuronen“ noch eine höhere Prozentzahl, sondern stärkerer Evidenzstatus: ein eigener scoped Claim und prospektiver EvidenceEngine-kompatibler Promotion-Pfad, Human Review der Temporal-Order-Linie sowie unabhängig implementierte Replikation. Keine dieser Linien belegt Kognition, Skalierbarkeit oder einen 5D-Vorteil.

### Stage 2 — stabile Rekurrenz

Die rekurrente Stufe besitzt Langlauf-, Determinismus-, Restart/Restore- und Netzwerkverträge. Ein wichtiger neuer Befund stammt aus `EXP-GEN-0036`: Die `PING`-Bedingungen zeigen einen klaren deskriptiven mechanistischen Unterschied zwischen `recurrence_off` und `recurrence_on`. Beide Bedingungen stammen aus derselben Basiskonstruktion; die Rekurrenzbedingung ergänzt gezielt eine Rückkante. Der Effekt ist damit innerhalb des kleinen simulierten Systems mechanistisch interpretierbar, aber noch keine breite Generalisierung. Die über Seeds identischen Trajektorien sind insbesondere keine zehn statistisch unabhängigen Replikate.

Diese Review korrigierte zugleich die Berichtsebene: Gedankenstriche in der universellen Summary-Tabelle bedeuteten nicht fehlende DATA. Trial-, STDP-, Lern-, TIME- und Regulationsprotokolle waren ausgeführt; ihre Metriken passten nur nicht in die zu enge SNN-Haupttabelle. Damit wurde ein echter Reporting-/AIRR-Fehler von einem Experimentfehler getrennt.

#### Aktuelle Reproduzierbarkeitslinie EXP-GEN-0045/0046

Nach der ersten 1.8-Strukturfassung kamen zwei weitere explorative DATA-Läufe hinzu. `EXP-GEN-0045` (`tonic_spike_reproducibility_v1`, RQ-SNN-002/H-SNN-002-A) führte drei Same-Seed-Tonic-Replikapaare für die Seeds 101, 102 und 103 aus. In allen drei Fällen war `spike_sequence_identical=true`. Der Befund dokumentiert für genau diesen Protokollumfang reproduzierbare Spike-Sequenzen bei gleichem Seed, Input und Anfangszustand; `scientific_evidence=false` und `automatic_evidence_promotion=false` bleiben ausdrücklich erhalten.

`EXP-GEN-0046` (`deterministic_replica_v1`, RQ-DET-001/H-SNN-003-A) erweitert die Prüfung auf zwölf 256-Tick-Läufe: `recurrence_off_replica_a/b` und `recurrence_on_replica_a/b` über dieselben drei Seeds. Innerhalb der jeweiligen Replica-Paare sind die gespeicherten Trajektorien deskriptiv identisch. Recurrence-off erzeugt pro Lauf 3 Spikes, 2 synaptische Ereignisse, 0 recurrent events und propagation depth 1; Recurrence-on erzeugt 33 Spikes, 33 synaptische Ereignisse, 10 recurrent events und propagation depth 61. Damit werden Reproduzierbarkeit und der bereits bekannte mechanistische Rekurrenzunterschied auf einer neuen DATA-Linie sichtbar.

Die wissenschaftliche Grenze ist wesentlich: `EXP-GEN-0046` ist als `EXPLORATORY` markiert, seine semantische Konsistenz steht auf `NOT_AUTOMATICALLY_CLASSIFIED`, die Evidence Readiness auf `BLOCKED_UNCLASSIFIED_SEMANTICS`, und der Human Review ist noch offen. Der AIRR ist Interpretation-only und besitzt trotz einer intern formulierten „supported“-Bewertung keine EVID-Autorität. Identische Ausgaben über Seeds beziehungsweise Replicapaare sind zudem keine automatisch unabhängigen Replikationen.

### Stage 3 — plastisches Nervengewebe

Stage 3 integriert STDP, Eligibility, verzögerte Drei-Faktor-Modulation, Homeostase, strukturelle Plastizität sowie Ressourcen- und Zustandsgrenzen. Der besondere Engineeringvertrag `Proposal → Approval → Mutation → Journal → Undo` trennt Änderungsvorschlag, Autorisierung, tatsächliche Strukturmutation, Journalisierung und Rücknahme. Dies macht Strukturplastizität auditierbar und experimentell abladierbar.

Der wissenschaftliche Stand bleibt jedoch enger: Implementierte Gewichtsänderung ist noch kein Nachweis nützlichen Lernens. Die noch ausstehenden starken Prüfungen betreffen held-out Generalisierung, learning-on/off, Frozen/Sham/Shuffle, Langzeitstabilität, Interaktion mit Homeostase und Ressourcen sowie unabhängige Replikation.

### Stage 4 — spezialisierte neuronale Areale

Stage 4 besitzt drei getrennte Referenzpfade: Audio (`stage4.audio.temporal`), Vision (`stage4.vision.spatial`) und Digital (`stage4.digital.symbolic`). Die Pfade unterscheiden sich in Adaptern, Routing und Plastizitätskandidaten. Der technische Topologievertrag beschreibt aggregiert 100.000 Neuronen und 10 Millionen gerichtete Kanten, aber **nicht** einen vollständig dynamisch materialisierten 100k/10M-Lauf; `dynamic_scale_execution_verified=false` bleibt Teil der Grenze.

Die E01–E05-Serien liefern konkrete DATA:

- `RQ-MSBA-E01`: gleiche mittlere Task-Accuracy der Referenzmodalitäten; modellierte Kosten im gespeicherten Datensatz Digital < Audio < Vision.
- `RQ-MSBA-E02`: adaptive Referenzallokation liegt in den gespeicherten DATA über fixer und zufälliger Allokation.
- `RQ-MSBA-E03`: adaptive visuelle ROI/Foveation erreicht im synthetischen Design dieselbe Task-Accuracy wie Full-Image bei geringerem modelliertem Energieverbrauch.
- `RQ-MSBA-E04`: im digitalen Integritätspfad traten keine gespeicherten Checksum- oder Exact-Payload-Mismatches auf.
- `RQ-MSBA-E05`: adaptive Referenzkompensation zeigte nach Modalitätsverlust eine höhere Task-Recovery als fixe Allokation.

Diese Befunde stützen technische Teilfunktionen in den jeweiligen synthetischen Designs, aber noch keinen allgemeinen Vorteil spezialisierter Areale, keine biologische Äquivalenz und keine physikalisch gemessene Energieeffizienz.

### Stage 5 — integriertes künstliches Nervensystem

Stage 5 verbindet typisierte Sensorgrenzen, digitale Interozeption, autorisierte Aktorik, die `ExperienceEngine`, Feedback und Ressourcenregulation. Der Referenzversuch `EXP-STAGE5-20260914-INTEGRATED-NERVOUS-SYSTEM` verwendet sechs Bedingungen — `authorized`, `unauthorized`, `actuator_failure`, `sensor_loss`, `open_loop_replay`, `sensor_reproducibility` — mit 20 unabhängigen Läufen × 3 Wiederholungen, insgesamt **360 kontrollierten Runs**.

Die DATA zeigen, dass die registrierte deterministische Sensor–SNN–Aktor–Feedback-Kette unter kontrollierten Bedingungen zielgerichtete Wirkungen erzeugen und unautorisierte bzw. fehlerhafte Wirkungspfade abgrenzen kann. Das ist DATA-Support für `H-EMB-001-A`, keine automatisch akzeptierte EVID und keine Generalisierung auf reale Geräte. `H-EMB-001-B` — der streng gematchte Vergleich von Closed Loop, yoked Replay und unterbrochener Rückmeldung unter identischer Störung — bleibt offen.

Interozeptionsgrößen wie `energy_reserve`, `resource_pressure` oder `thermal_threat` bleiben technische Kontrollvariablen. Sie sind weder Stoffwechselhomologien noch Hinweise auf subjektives Empfinden.

### Stage 6 — Gedächtnis und Weltmodell

Stage 6 umfasst Working-Memory-Grundlagen, episodische Speicherpfade, semantische Prototypen, Replay, Übergangsstatistik, Prediction-Error-Infrastruktur und World-Model-Kandidaten. Die stärkste bisherige empirische Erkenntnis entstand aus der CL-001–CL-003-Linie.

CL-001 zeigte einen Vorteil von Semantic+Replay gegenüber einer No-Replay-Baseline, trennte die Ursache aber nicht. CL-002 führte gematchtes Raw-Replay ein und bestätigte keinen konfirmatorischen Zusatznutzen semantischer Prototypen; die Projekt-EVID klassifizierte H1 für dieses Protokoll als falsifiziert. CL-003 prüfte die verbleibende Dosisalternative in 84 Runs = 12 Seeds × 7 Bedingungen. C1, C2 und C4 bestanden die präregistrierten Erfolgsregeln nicht. Der Semantic-minus-Raw-Unterschied stieg deskriptiv mit der Dosis, durfte aber wegen des negativen Interaktionstests C4 nicht als bestätigter Dosis-Effekt interpretiert werden. C3 (`S20 − X20`) war dagegen deutlich positiv: Semantic lag gegenüber Random Prototype um rund +14,9 Prozentpunkte höher.

Die derzeit zulässige DATA-only-Synthese lautet deshalb: **Replay ist unter den untersuchten Bedingungen der nachweisbare Hauptbeitrag; semantische Verdichtung trägt nicht-zufällige Struktur, zeigt aber keinen präregistriert bestätigten Zusatznutzen gegenüber gematchtem Raw-Replay.** CL-003 bleibt bis Human Review DATA, nicht EVID.

### Stage 7 — technische Identität und Selbstmodellgrenze

Versionierte technische Profile, Digests, Lineage, Snapshot-Bindung und Behavior State bilden eine reproduzierbare technische Identität. Sie sind kein psychologisches Selbstmodell. Ein stärkerer Stage-7-Claim erfordert kausale self/other-Interventionen, bei denen intern repräsentierte eigene Zustände oder Handlungen Vorhersagen oder Entscheidungen messbar verbessern und von Fremdzuständen unterschieden werden.

### Stages 8–10 — Frontier

Stage 8 enthält Continual-Learning- und Interferenzprogramme sowie Vorläufer-DATA, aber keine bestätigte autonome lebenslange Entwicklung. Stage 9 enthält Forschungsfragen zu hochintegrierter Kognition, jedoch keine confirmatory Stage-9-DATA. Stage 10 ist eine Governance- und Forschungsfrontier zu Bewusstseinsfragen; es existiert kein zulässiger Pfad von einem technischen Score zu Bewusstsein, Sentienz oder moralischem Status.

## 13.2 Eine zentrale Revision: 5D wurde bisher nicht adäquat getestet

`EXP-GEN-0036` liefert für die 5D-Frage keinen Nullbefund, sondern einen **Testadäquanzbefund**. Die damalige `run_5d()`-Implementierung variierte die Dimensionskoordinaten einer kontrollierten Drei-Neuronen-Kette, während die wesentliche Konnektivität, Gewichte und Delays explizit gesetzt blieben. Die Dynamik war damit konstruktiv kaum sensitiv für die Dimension.

Der Human Review klassifizierte `RQ-5D-005` deshalb für diesen Teilversuch als **NOT TESTED** hinsichtlich eines genuinen Geometrieeffekts. Künftige 5D-Prüfungen müssen vorab definieren, über welchen Mechanismus Dimension wirken darf — etwa Nachbarschaft, distanzabhängige Konnektivität, Delays oder Plastizität — und benötigen Aktivitäts-Adequanz, matched topology/degree, Shuffle- und Random-Graph-Kontrollen. Das ist ein wichtiger Erkenntnisfortschritt: Ein ungeeignetes Experiment darf nicht als Nullbefund gegen eine Hypothese interpretiert werden.

## 13.3 Periphere Netze, Neural Symbiosis und MSBA

Die kanonische Architektur enthält neben dem SNN-Kern eine explizite periphere Multi-Netz-Grenze. **Neural Symbiosis** bezeichnet dabei keine zweite Intelligenz im Kern, sondern eine Embodiment-Schicht, in der spezialisierte neuronale oder virtuelle Verarbeitungssysteme über deklarierte Gateways an den SNN angebunden werden können. Der offene Adaptervertrag kann unter anderem CNN-, Vision-Transformer-, Transformer-, RNN-/LSTM-/GRU-, GNN-, Reservoir-, Hopfield-, VAE-, Autoencoder-, multimodale und neuro-symbolische Komponenten beschreiben. Ebenso können Datenbanken, Wissensgraphen, Retrieval-, Logik- oder externe Speicherdienste als virtuelle Areale auftreten.

Diese Offenheit ist wissenschaftlich nur tragfähig, wenn **Erreichbarkeit von gelernter Nutzung getrennt** bleibt. Ein registrierter Adapter, ein erreichbarer Endpunkt oder eine erfolgreiche Inferenz beweist weder, dass das SNN den Pfad auswählt, noch dass es von ihm lernt oder einen kausalen Vorteil besitzt. Gateway-Plastizität ist deshalb standardmäßig gesperrt; Random-, Frozen-, Shuffle- und Plastic-Zustände gehören in experimentgebundene, persistierbare Laufkontexte. Externe Netze erhalten keine impliziten Schreibrechte auf kanonische Neuronen-, Synapsen-, Reward-, Gedächtnis- oder EVID-Zustände.

Unterhalb dieser Grenze konkretisiert **MSBA** die modalitätsspezifische Bahnarchitektur. Audio, Vision und Digital werden nicht als biologische Kortexplagiate behandelt, sondern als technische Pfade mit unterschiedlichen Informations- und Ressourcenverträgen:

- Audio priorisiert zeitliche Kohärenz, Band-/Phasen- beziehungsweise Hüllkurveninformation und begrenzte Delay-Strukturen.
- Vision verwendet räumliche/featurebezogene Projektionen, sparse Zielgrade und experimentelle ROI-/Foveationsmechanismen.
- Digital hält exakte Nutzdaten außerhalb des SNN in checksum-gebundenen Symbolframes; das SNN erhält nur eine deterministische Populationrepräsentation. Lernen darf Routing oder Assoziation verändern, nicht die ursprünglichen Bits oder ihre Prüfsumme.

Eine besonders wichtige Korrektur betrifft Dimensionalität. Der MSBA-Projektionsraum darf experimentell zwischen 1 und 32 Dimensionen variieren, während der produktive Neuron-ID-/Persistenzvertrag des Kerns weiterhin **fünfdimensional** bleibt. Ein 16D- oder 32D-Projektor ist daher weder ein 16D-/32D-SNN noch Evidenz für einen Vorteil höherer Kerndimensionalität. Projektion, Mapping und produktiver Kern müssen in jeder Studie getrennt provenance-gebunden werden.

Auch Ressourcenangaben bleiben typisiert: `normalized_energy_units`, kalibrierte Schätzungen in Joule und tatsächlich gemessene Joule sind drei verschiedene Größen. Die Stage-4-E01–E05-DATA dürfen deshalb modellierte Energieunterschiede zeigen, ohne daraus physikalisch gemessene Energieeffizienz abzuleiten.

## 13.4 Wesen, reale Körpergrenze und technische Identität

Die Vorgängerarbeiten entwickelten mit **Wesen** eine maschinen-native Körperdarstellung. Wissenschaftlich relevant ist daran nicht die visuelle Anthropomorphie, sondern die harte Trennung von beobachtetem Zustand und Interpretation. Die Körpergrenze wird aus tatsächlich erkannten Verbindungen, Host-Ressourcen und Embodiment-Endpunkten aufgebaut. Nicht vorhandene Temperatur-, Lüfter-, Sensor- oder Aktorwerte bleiben unbekannt; es werden keine plausibel wirkenden Ersatzdaten erfunden. `available` ist ausdrücklich nicht gleich `authorized` und nicht gleich `active`.

Maschinen-native Interozeption umfasst dort, wo das Betriebssystem Messwerte liefert, etwa CPU-/Speicherlast, Temperatur, Lüfter, Storage, Netzwerk und Kontinuitätsgrößen. Diese Größen können technische Regulationszustände beeinflussen, sind aber keine biologischen Stoffwechselhomologien und keine Empfindungsindikatoren. Ebenso ist die body-like Darstellung nur Präsentationssemantik.

Der implementierte Profile-&-Identity-Vertrag speichert Konfiguration, Fähigkeiten, Grenzen, Provenienz, Revisionen, Lineage und Snapshot-Bindungen als technische Identität. Profil, `.b5d`-Snapshot, Runtime-Checkpoint, Registry und Lineage sind absichtlich getrennte Zustandsklassen. Daraus folgt **keine psychologische Identität, Persönlichkeit, subjektive Kontinuität oder Bewusstseinsbehauptung**. Genau diese Grenze ist für spätere Stage-7-Selbstmodellforschung zentral: Metadatenidentität ist eine technische Voraussetzung, kein kausales Selbstmodell.


---

<a id="part-iv"></a>

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

Die Arbeit zu Spiegelmechanismen wird als Stage-6-naher Forschungsstrang integriert. Der historische Primärbefund beobachtungs- und handlungsbezogener Aktivität in Affen-Prämotorkortex wird auf die ursprüngliche neurophysiologische Arbeit zurückgeführt ([di Pellegrino et al., 1992](REFERENCES.md#ref-DIPELLEGRINO1992)); die breitere Systemeinordnung wird durch Reviewliteratur ergänzt ([Rizzolatti & Craighero, 2004](REFERENCES.md#ref-RIZZOLATTI2004)). Eine Verbindung zu Prediction ist als theoretischer Predictive-Coding-Account diskutiert worden ([Kilner et al., 2007](REFERENCES.md#ref-KILNER2007)), darf für MHRN aber nicht als bereits gezeigter Mechanismus übernommen werden. Der prüfbare MHRN-Kern ist deshalb nicht das Etikett „Spiegelneuron“, sondern die Frage, ob Beobachtungs- und Ausführungsrepräsentationen partiell überlappen, ob Kontext und Zielrelevanz diese Überlappung modulieren und ob ein Prediction-Error-Mechanismus einen kausalen Zusatznutzen liefert. Stage 4 liefert sensorische Pfade, Stage 5 Eigenaktionen/Outcome, Stage 6 Vorhersage; Stage 7 Selbst/Fremd-Unterscheidung ist erst nach eigener Kausalprüfung zulässig.

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

Die kanonische Related-Work-Arbeit präzisiert mehrere externe Referenzlinien. **Primärliteratur** zu hippocampal-kortikaler Semantization und continual learning motiviert Replay-/Konsolidierungsfragen, ohne einen MHRN-SemanticMemory-Mechanismus zu validieren ([D'Alba et al., 2025](REFERENCES.md#ref-DALBA2025); [Shi et al., 2025](REFERENCES.md#ref-SHI2025)). Eine aktuelle **Sekundärquelle/Survey** zu SNN-Predictive-Coding zeigt, dass Prediction Error auf unterschiedliche Weise neuronal repräsentiert werden kann; ein Telemetriefeld gleichen Namens ist daher noch kein Predictive-Coding-Mechanismus ([N'dri et al., 2026](REFERENCES.md#ref-NDRI2026)). Eine **Primärarbeit** zu einem Spiking World Model mit modellbasierter Kontrolle setzt eine deutlich stärkere Referenz als ein passiver One-Step-Predictor ([Sun et al., 2025](REFERENCES.md#ref-SUN2025)). Eine weitere **Primärarbeit** zu Multi-Zeitskalen-Plastizität mit astrozyteninspiriertem Gating zeigt einen externen Mechanismuskandidaten für Stabilitäts-/Plastizitätsfragen, ist aber kein Wirksamkeitsnachweis der MHRN-Regelung ([Dong & He, 2026](REFERENCES.md#ref-DONG2026)).

Diese Literatur wird in 1.8 bewusst als **externer Präzedenz-/Vergleichsraum** integriert. Sie kann die Form einer MHRN-Forschungsfrage verbessern, aber weder DATA erzeugen noch eine interne Hypothese bestätigen.

## 19.6 Determinismus-Registry, AIRR und Testadäquanz

Zwei Entscheidungen vom 17. September 2026 präzisieren die Verwendung der jüngsten SNN-DATA. Erstens bleibt der historische Lauf `EXP-BATCH-20260914074039-02` unverändert `RQ-SNN-002` zugeordnet. Seine beobachtete Condition `same_seed_tonic_replica_pair` ist für diese historische Registrierung ein semantischer Mismatch und darf nicht post hoc umetikettiert werden. Der technische Befund kann als Determinismusdiagnostik zitiert werden, aber nur gemeinsam mit dieser Provenienzgrenze.

`RQ-DET-001` besitzt nun einen expliziten Determinismusvertrag: entweder isolierte Same-Seed/Same-Input-Tonic-Replikapaare oder die expliziten `recurrence_off/on_replica_a/b`-Bedingungen. `RQ-SNN-002` behält dagegen seinen Recurrence-off/on-Vertrag; der bestehende saubere Lauf `EXP-SNN-002-R2` erfüllt diesen mit zehn Seeds. Ein neuer Lauf wird nicht allein erzeugt, um einen Registry-/Pipelinefehler kosmetisch zu reparieren.

AIRR bleibt Interpretation-only. Bei semantischem `MISMATCH` wird die öffentliche/reportseitige `ai_confidence` deterministisch auf `0.0` gesetzt; die ursprüngliche Modellselbsteinschätzung bleibt nur im append-only AIAR-Auditdatensatz. Ein isolierter Tonic-Test ist außerdem ausdrücklich **kein Netzwerkbefund** und seine Laufzeit darf nicht als Netzwerkperformance interpretiert werden.

Die zweite Entscheidung betrifft `EXP-GEN-0047` und `H-SNN-003-B`. Die sechs Conditions `1d`, `2d`, `3d`, `5d`, `5d_shuffled` und `random_graph` sind semantisch korrekt und der Lauf ist technisch reproduzierbar. Dennoch ist `topology_propagation_v1` **INADEQUATE_TO_TEST_HYPOTHESIS**: Nur drei Neuronen und zwei feed-forward Synapsen tragen die Dynamik; bei den nicht-randomisierten Bedingungen verändert sich die Koordinate, aber nicht ausreichend der kausale Übertragungsmechanismus. Daher sind identische Ergebnisse über 1D/2D/3D/5D weder ein Topologie-Nullbefund noch eine Widerlegung eines 5D-Effekts.

Die einzige deskriptive Abweichung des v1-Laufs — eine um einen Tick frühere First-Response-Latency im `random_graph` — ist konfundiert mit einer geänderten Kantenanordnung und darf nicht zum Dimensionseffekt hochgestuft werden. Auch `stopped_on_quiescence=false` ist kein Fehler: Der Runner setzt `min_ticks=max_ticks` und erzwingt damit das vollständige Beobachtungsfenster.

`topology_propagation_v2` wurde inzwischen als enger **Stage-1-Test von `H-SNN-003-B`** präregistriert und ausgeführt. Die stärkeren Schwellen von ≥1.000 Neuronen und ≥10 eingehenden Synapsen gehören nicht zu diesem allgemeinen Topologietest, sondern zur getrennten dimensionsspezifischen Prüfung `RQ-5D-005 / H-5D-005-A`. Diese Trennung verhindert, dass ein kleiner, testadäquater Topologiebefund nachträglich zu einem 5D-Vorteilsclaim erweitert wird.

## 19.7 Genehmigter Stage-6-Kompressionsvorschlag

Mit `LP-20260917194217` liegt ein **genehmigter, aber nicht ausgeführter** human-origin Lernvorschlag vor. Die Forschungsfrage ist enger als der bisherige CL-003-Vergleich: Kann semantische Prototypkonsolidierung bei **10 % des Raw-Replay-Speicherbudgets** mindestens 95 % der Retention eines Raw-Replay-Baselines mit vollem Speicherbudget erreichen? Externe Gedächtnis- und Konsolidierungsarbeiten liefern hierfür einen theoretischen und mechanistischen Vergleichsraum ([McClelland et al., 1995](REFERENCES.md#ref-MCCLELLAND1995); [D'Alba et al., 2025](REFERENCES.md#ref-DALBA2025); [Shi et al., 2025](REFERENCES.md#ref-SHI2025)), aber die konkrete 10-%-/95-%-Entscheidungsgrenze ist eine **prospektive MHRN-Hypothese** und kein aus der Literatur übernommener Effekt.

Der Vorschlag bindet `semantic_prototype_replay_10pct_budget` gegen `raw_replay_full_budget` und nennt als Kontrollen `no_replay`, `random_prototype_10pct` und `learning_off`. Die Evaluation soll auf Holdout-Daten nach sequentiellen Tasks erfolgen. Die Erfolgsmetrik ist `retention_ratio_at_1_10_storage >= 0.95` der Raw-Replay-Retention. Damit prüft der nächste Zyklus **Kompression bei erhaltener Retention**, nicht eine allgemeine Überlegenheit der Lernleistung.

Die Entscheidungsfolge wird vor DATA festgelegt: **Erreicht** die semantische Prototypkonsolidierung die vorab fixierte Retentionsgrenze bei einem Zehntel des Speicherbudgets, ist damit eine begrenzte Kompressionsrolle von SemanticMemory unter genau diesem Protokoll gestützt. **Verfehlt** sie die Grenze, gilt diese Kompressionsrolle für den getesteten Mechanismus als nicht gestützt; Generalisierung, Langzeitgedächtnis oder eine Weltmodell-Brücke wären dann eigenständige spätere Forschungsfragen und dürfen nicht als nachträgliche Rettung desselben Tests verwendet werden.

Der aktuelle Status ist strikt prospektiv. Das historisch genehmigte `LP-20260917194217` bleibt als Originalartefakt unverändert und besitzt weiterhin `executed=false` sowie keine Runtime-Autorität. Die fehlende Quellbindung wurde **nicht** in dieses genehmigte Artefakt hineingeschrieben. Stattdessen liegt mit `LP-20260917194217-R1` eine neue `proposal_only`-Revision vor: `CL-002-EVID` → SHA-256 `c7b1124256fd8018839a8c5c29b30493b68d16bc223d0a3258bcbaca55b1752e` und `CL-003-DATA` → SHA-256 `4e74021c0ef838371a3a01061ae1c2dcebb2031b54c15c6169e38c1972d06290`; beide Source-Trust-Einstufungen stehen auf `VERIFIED`. Diese Inhaltsänderung erfordert eine **neue explizite Human Approval**; die historische Genehmigung wird nicht übertragen.

Der **nächste empirische Arbeitsschritt ist die Präregistrierung dieses Kompressionsvergleichs**, nicht seine Ausführung. Vor einem `FROZEN`-Status müssen mindestens die kanonische RQ/H-Zuordnung, die exakte Speicherbudget-Messung, Seed-/Taskplan, Retentionsaggregation und Inferenz-/Äquivalenzregel, Ausschluss- und Failure-Regeln, Analysevertrag, Source-/Config-Hashes sowie die R1-Human-Approval gebunden sein. Erst danach kann eine separate Ausführungsautorisation erteilt werden. Diese Trennung folgt der allgemeinen Präregistrierungslogik, Hypothese und Analyseplan vor Sichtung der Ergebnisdaten festzulegen ([Nosek et al., 2018](REFERENCES.md#ref-NOSEK2018)).

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

**Befund.** Das Activity-Gate bestand beim niedrigsten Kandidatengewicht 55.0. Alle 120 Evaluationsläufe waren vollständig; 64 Neuronen, 246 Kanten und das eingefrorene Gewicht waren in allen Armen erhalten. Die globale Kantenanzahl ist damit zwischen den Bedingungen gematcht; der Befund ist keine einfache Dichte-/Sparsity-Differenz. Mehrere präregistrierte Primärkontraste unterschieden sich signifikant. Beispielsweise lag die mediane Änderung der aktiven Netzwerkfraktion für 3D→5D bei -0,125 (Bootstrap-CI95 -0,15625 bis -0,1015625; Holm-p ≈ 1,91×10^-5). Bei der First-Output-Latenz lagen die Medianunterschiede 1D→2D bei -10 Ticks, 2D→3D bei -3 Ticks und 3D→5D bei -1 Tick. Der registrierte DATA-Status lautet `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`.

**Endpoint-Interpretation.** `active_fraction` sättigt im gewählten Regime für 1d, 2d und 3d bei einem Median von 1,0. Die beiden frühen Kontraste besitzen deshalb exakt null gepaarte Differenz, CI [0,0] und p=1. Diese Beobachtung wird als Ceiling-/Sättigungsgrenze des Endpunkts in diesem Operating-Envelope behandelt, nicht als Nachweis topologischer Gleichheit. Die inferenzielle Last der Primäranalyse liegt auf den präregistrierten exakten gepaarten Sign-Tests mit Holm-Korrektur; die Bootstrap-Intervalle beschreiben die Median-Differenzen und liefern bei diskreten, identischen Differenzen erwartungsgemäß degenerierte Intervalle.

Der zweite Primärendpunkt heißt zwar `first_output_latency_censored`, im vorliegenden Evaluationsdatensatz trat jedoch keine tatsächliche Zensierung auf. Bei 128 Evaluations-Ticks würde nur ein vollständig ausbleibender Output als 129 kodiert; der 1d-Median von 19 ist deshalb eine regulär beobachtete Latenz und nicht die Nähe zu einem Censor-Horizont. Die Latenzunterschiede sind über alle fünf präregistrierten Primärkontraste signifikant und bilden damit den breiter diskriminierenden Teil des Stage-1-Befunds.

**Interne Replikation und Ceiling-Auflösung.** Um die in V2 beobachtete terminale Sättigung von `active_fraction` bei 1d/2d/3d prospektiv zu adressieren, wurde ein zeitaufgelöstes Replikationsprotokoll mit unverändert 64 Neuronen, 246 Kanten, Synapsengewicht 55.0 und 128 Ticks eingefroren. Der erste V3-Lauf (`EXP-S1-TOPO-V3-20260918`) bleibt als Auditspur erhalten, ist aber für die konfirmatorische Interpretation superseded, weil der Runner die Holm-Korrektur entgegen der Präregistrierung in zwei Fünferfamilien statt in einer gemeinsamen Familie von zehn Primärtests ausführte. Die Korrektur erfolgte nicht durch Umschreiben der DATA, sondern durch `EXP-S1-TOPO-V3-R1-20260918` mit frischen Seeds 6201–6220.

R1 definiert `activation_auc_0_32` als Summe der kumulativen einzigartig aktivierten Neuronenfraktion nach jedem Tick 0–31 sowie `half_activation_latency_censored` als ersten Tick mit mindestens 50 % kumulativer Aktivierung. Mit der korrekt gemeinsamen Holm-Familie über alle zehn zeitaufgelösten Primärtests trennen beide low-dimensionalen Zielkontraste: Die mediane Aktivierungs-AUC steigt von 22,15625 (1d) auf 26,5703125 (2d) auf 28,0078125 (3d). Die gepaarten Medianunterschiede betragen 1d→2d +4,4140625 (CI95 [4,3671875; 4,4296875], Holm-p ≈ 1,91×10^-5) und 2d→3d +1,4609375 (CI95 [1,3671875; 1,4921875], Holm-p ≈ 1,91×10^-5). Die Halbaktivierungslatenz fällt von 10 auf 6 auf 4 Ticks; auch diese beiden Kontraste sind Holm-korrigiert signifikant. Damit wird die V2-Grenze präzisiert: die terminale Endaktivität sättigt, während die **zeitliche Ausbreitungsdynamik** weiterhin klar unterscheidbar ist.

Die V2-First-Output-Latenz wird zusätzlich auf den frischen R1-Seeds repliziert. Alle fünf präregistrierten Kontraste behalten dieselbe negative right-minus-left-Richtung und sind Holm-korrigiert signifikant; die Bedingungsmediane bleiben 19, 9, 6, 5, 2 und 2 Ticks. Dies ist eine interne Replikation derselben Architektur-/Codefamilie und ersetzt keine unabhängig implementierte Replikation.

**Diskussion.** Damit besitzt `H-SNN-003-B` erstmals einen testadäquaten positiven Befund im untersuchten Stage-1-Regime: Topologie verändert bei gleichem Neuronen- und Kantenbudget die Propagationsdynamik. Der Effekt ist jedoch **kein monotones Dimensions- oder 5D-Vorteilsmuster**. `5d_shuffled` und `random_graph` erreichten den Output in diesem Design früher als die reguläre 5D-Anordnung. Das unterstützt die allgemeine Topologiesensitivität, nicht die Überlegenheit einer bestimmten Dimensionalität.

**Limitation.** 64 Neuronen, 246 Kanten, ein eingefrorenes Synapsengewicht und das deterministische vorwärtsgerichtete Konstrukt definieren einen engen Small-SNN-Operating-Envelope. Der Lauf prüft weder Skalierung noch biologische Äquivalenz noch `H-5D-005-A`. Wegen der `active_fraction`-Sättigung ist ein zusätzliches niedrigeres Aktivitätsregime eine sinnvolle spätere Robustheitsprüfung, aber **keine Voraussetzung**, um den bereits präregistriert positiven Latenz-/Topologiebefund als DATA zu dokumentieren. Die stärkere 5D-Prüfung benötigt weiterhin ≥1.000 Neuronen, ≥10 mittlere Eingänge pro Neuron, explizit distanzabhängige Konnektivität und streng gematchte Dimensionskontrollen. Der aktuelle Lauf bleibt bis Human Review DATA-only.

**Zwischenfazit.** Rekurrenz ist im getesteten Mechanismus wirksam; `H-SNN-003-B` ist im 64-Neuronen-Stage-1-Regime DATA-seitig gestützt. Die spezifische 5D-Hypothese bleibt offen.

#### Stage-1-Konsolidierung: Baseline, Reviewstatus und zweite Funktionslinie

Für die wissenschaftliche Reife wird V2 nicht isoliert betrachtet. `EXP-S1-TOPO-V2-20260918` und `EXP-S1-TOPO-V3-R1-20260918` bilden gemeinsam die kanonische `STAGE1-TOPOLOGY-LINE-001`: V2 ist die erste präregistrierte testadäquate Topologiestudie; R1 ist die korrigierte interne Replikation mit neuen Seeds, prospektiven zeitaufgelösten Endpunkten und korrekter gemeinsamer Holm-Familie. Der erste V3-Lauf bleibt wegen der falsch implementierten Primärfamilie ausschließlich Auditspur. Diese Zusammenführung ist eine Forschungsstatusentscheidung, keine Umschreibung historischer DATA.

Die Human Reviews beider gültigen Linien durch Thomas Heisig sind abgeschlossen und akzeptieren die begrenzte Interpretation. Damit ist das Human-Review-Subgate der Stage-1-Maturity erfüllt. Eine EVID-Promotion folgt daraus ausdrücklich nicht. Der aktuelle EvidenceEngine-Vertrag verlangt unter anderem `validity.valid=true`, Nullwerte für Runtime-/Fatal-Fehler, `git.dirty=false`, `provenance_digests`, einen passenden `source_freeze_sha`, einen kanonischen Claim und ein `human_review.json` mit `supports|refutes|inconclusive`. Die historischen V2/R1-Manifeste besitzen diese heutige Vertragsform nicht; ihre vorhandenen Human Reviews lauten `accepted_as_interpretation`. Fehlende historische Felder oder stärkere Entscheidungen werden nicht rückwirkend konstruiert. Der EVID-Pfad ist daher separat und prospektiv zu behandeln.

Als zweite Stage-1-Funktionslinie wird `STAGE1-TEMPORAL-ORDER-LINE-002` geführt. `EXP-S1-TEMP-ORDER-V2-20260919` prüft `RQ-TEMP-002 / H-TEMP-002-A` in einem acyclischen Sechs-Neuronen-SNN. Über 20 Seeds und 120 Runs werden intakte Kanalidentität, identity-destroyed Kontrolle sowie simultane Kontrolle verglichen. Der intakte Arm erreicht im gespeicherten V2-Befund eine mediane Order Accuracy von 1,0, der identity-destroyed Arm 0,0; die simultane Kontrolle besteht. Der Lauf ist `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`, bleibt aber DATA bis Human Review und einer gegebenenfalls später separat legitimierten EVID-Entscheidung. Er belegt keine Lern-, Gedächtnis-, Kognitions- oder Skalierungsleistung und ist keine unabhängige Replikation der Topologielinie.

Unter dem unveränderten Maturity-Vertrag ergibt sich daraus **Stage 1 = 75 %**: RQ/H, Protokoll, DATA und Attribution sind `met`, `reviewed_evidence` ist wegen abgeschlossenem Human-Review-Subgate `partial`, und `independent_replication` bleibt `open`.

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


---

<a id="part-v"></a>

# Teil V — Wissenschaftliche Infrastruktur und Engineering

## 20. Determinismus und Zustandsgrenzen

Reproduzierbarkeit ist mehr als ein Seed. Hypothesenrelevante Zustände können RNG, Scheduler, Neuronen, Synapsen, Delays, Queues, Plastizitätstraces, Eligibility, Strukturjournal, Homeostase, Ressourcen, Gedächtnis, World Model, Gateway-Zustand, Sensorinput und Code-/Konfigurationsdigest umfassen. Pause/Resume-Äquivalenz ist nur so stark wie die definierte Checkpointgrenze.

MHRN trennt Logical Identity, Physical Slot, Synaptic Reduction und Execution Scheduling. Diese Trennung soll verhindern, dass Speicherlayout oder GPU-Reihenfolge unbemerkt die wissenschaftliche Semantik verändern. Byteidentität ist nicht für jede Plattform realistisch; deshalb werden bitnahe, numerische und statistische Reproduktionsklassen unterschieden.

## 21. Storage und Digital State

Die frühere Idee eines „Digital State Twin“ bleibt erhalten, wird aber begrifflich begrenzt. Solange kein physisches Gegenstück synchron gekoppelt ist, beschreibt der Begriff primär einen reproduzierbaren digitalen Zustandszwilling. Primärzustände, Ereignisprovenienz und Rekonstruktionsverträge haben Vorrang vor löschbaren Heatmaps oder Analyseprojektionen.

Sparse Materialisierung, arrayorientierte Strukturen, Chunking und graphgeeignete Persistenz sind Skalierungsfragen. Millionen Python-Objekte sind kein wissenschaftliches Ziel. Ein großer Adressraum darf nicht mit einer vollständig materialisierten Population verwechselt werden.

## 22. Runtime, Beschleunigung und Ressourcen

Runtime-Performance ist wissenschaftlich relevant, wenn sie bestimmt, welche Skalen oder Zeitspannen überhaupt experimentell zugänglich sind. Beschleunigung darf jedoch Integrationsschritt, Ereignisordnung oder Reduktionsregeln nicht still verändern. Ressourcenproxies werden nicht als physikalische Energie ausgegeben, solange keine entsprechende Kalibration vorliegt.

## 23. Dashboard, Viewer und Research Catalog

Das Frontend ist wissenschaftliches Instrument. Es muss Engineering-Reife, wissenschaftliche Reife, DATA, EVID und Planung sichtbar trennen. Der Publication Viewer zeigt die aktuelle Arbeitsfassung, hält aber Frozen 1.5 und Vorgänger erreichbar. Eine schöne Oberfläche darf keinen stärkeren Claim erzeugen als das Quellartefakt.

Edition 1.8 ergänzt deshalb einen maschinellen Quellenindex, eine unveränderte Registry-Projektion und ein Erhaltungsmanifest. Jeder historische Publikationsblob am Basiscommit wird gehasht. Alle damaligen Markdown-Überschriften in `docs/` und `research/` werden indiziert. Dies schafft eine überprüfbare Untergrenze gegen versehentliches Vergessen, aber keine Garantie semantischer Vollständigkeit.

## 24. Lokale KI-Werkzeuge als Forschungsinfrastruktur

Arbeiten an lokalen Chat-/Assistenzsystemen, Provider-Adaptern, Streaming, persistenten Konversationen und Trainings-Workbenches fließen dort ein, wo sie den Forschungsprozess betreffen: reproduzierbare Datensätze, Trennung von Quelle/Dataset/Job/Artefakt, lokaler Datenschutz, Provider-Isolation und Werkzeugprovenienz. Sie werden nicht als neuronale Evidenz für MHRN umgedeutet.

Die Grenze zwischen Forschungswerkzeug und Forschungsobjekt bleibt explizit. Ein LLM kann einen Runner schreiben oder einen Bericht kritisieren; der daraus entstehende Commit muss dennoch durch Tests, Review und experimentelle Provenienz abgesichert werden.

## 24.1 Infrastruktur als Ergebnis der Fehlersuche

Mehrere zentrale Infrastrukturentscheidungen entstanden nicht am Reißbrett, sondern aus konkreten Fehlerfällen. Die Entwicklungsgeschichte zeigt dabei vier wiederkehrende Klassen.

### Zustandsfehler

Frühe Persistenzfragen machten deutlich, dass ein gespeicherter Graph allein keinen wissenschaftlich identischen Zustand garantiert. Scheduler, RNG, Delays, Queues, Plastizitätstraces und externe Gateway-Zustände können den weiteren Verlauf verändern. Daraus entstand der kanonische Scientific-State-Ansatz mit vollständigerer Zustandsgrenze und digestierbarer Repräsentation.

### Semantikfehler

LIF-Refraktärzeiten zeigten exemplarisch, dass zwei Systeme denselben Zahlenwert verwenden können und dennoch unterschiedliche zeitliche Semantik besitzen. Deshalb werden Konfigurationen nicht nur als Zahlen gespeichert, sondern mit Modell- und Semantikprovenienz behandelt.

### Reportingfehler

`EXP-GEN-0036` zeigte, dass vollständige DATA durch eine zu enge universelle Summary-Tabelle wie fehlende DATA aussehen können. Der Fehler lag in der Projektion, nicht im Runner. Daraus folgt eine Infrastrukturregel: Reports müssen protokollspezifische Statistiktypen tragen; ein leeres Feld in einer fremden Metrik darf nie automatisch als fehlender Run interpretiert werden.

### AI-Normalisierungsfehler

Der AIRR-Pfad hatte verwertbare verschachtelte Analysefelder, erwartete aber ein flaches `assessment`. Dadurch wurde vorhandene Analyse fälschlich als nicht verfügbar normalisiert und die Konfidenz auf 0 gesetzt. Der Fix war ein Schemafix, keine Änderung der DATA. Die methodische Konsequenz ist dauerhaft: AI-Outputs benötigen deterministische Schemaadapter und bleiben Interpretation, niemals automatische EVID.

### Semantisches Gate als reale Blockade: EXP-GEN-0046

Der aktuelle Determinismuslauf demonstriert, warum die Statusarchitektur praktisch notwendig ist. Obwohl EXP-GEN-0046 technisch vollständig ausgeführt wurde, der Tick-Vertrag erfüllt ist und reproduzierbare Metriken vorliegen, lautet die semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`. Die Evidence Readiness bleibt dadurch `BLOCKED_UNCLASSIFIED_SEMANTICS`.

Das ist kein Defekt, sondern gewünschtes Verhalten: Ein technisch erfolgreicher Lauf darf nicht allein wegen konsistenter Zahlen zu EVID werden. Erst eine registrierte semantische Zuordnung und Human Review dürfen die nächste Statusstufe öffnen. Auch der erzeugte AIRR bleibt `evidence=false`, `interpretation_only=true` und `human_review_required=true`.

## 24.2 Engineering und Scientific Maturity als getrennte Achsen

Eine der wichtigsten infrastrukturellen Erkenntnisse ist, dass „fertig gebaut“ und „wissenschaftlich getragen“ unterschiedliche Zustände sind. Stage 4 kann technisch vollständig integrierte Audio-/Vision-/Digitalpfade besitzen und trotzdem wissenschaftlich offene Fragen zu funktionaler Mehrleistung haben. Stage 5 kann einen grünen Closed-Loop-Vertrag besitzen und trotzdem keine Realwelt-Generalisation belegen. Stage 0 kann für einen eng definierten Readiness-Scope 100 % erreichen, während Human-EVID und unabhängige Replikation weiterhin offen bleiben.

Diese Trennung ist im Dashboard absichtlich sichtbar. Prozentwerte sind nur zusammen mit ihrem Scope und den Kriterien zulässig; sie sind keine Intelligenz-, Kognitions- oder Bewusstseinsmetriken.

## 24.3 Der Publication Viewer als Provenienzoberfläche

Die Arbeit am Publication Viewer führte zu einer wichtigen wissenschaftlichen Anforderung: Eine Publikation ist nicht nur Text, sondern eine navigierbare Provenienzoberfläche. Formeln, Anker, Literatur, Vorgängerversionen, Frozen-Baselines und aktuelle WIP-Änderungen müssen erreichbar bleiben.

Daraus entstand der heutige Editionsvertrag: 1.5 bleibt frozen, 1.6/1.7 bleiben historische Vorgänger, 1.8 ist current WIP, und der Viewer darf alte Zustände nicht durch die aktuelle Interpretation überschreiben. Die aktuelle Fassung darf ältere Befunde einordnen, aber nicht ihre historischen Bytes oder damaligen Statusbehauptungen still ändern.

## 24.4 Full Stack ist kein wissenschaftlicher Endpunkt

Frontend, API und Backend werden bewusst End-to-End integriert, weil fehlende Instrumentierung Forschung verhindern kann. Ein sichtbarer Sensorstatus, ein Stage-Panel oder ein Ask-KI-Button sind jedoch keine Evidenz. Full-Stack-Funktion ist ein **Mess- und Bedienbarkeitsvertrag**.

Diese Grenze ist besonders wichtig für spätere Stages: Ein UI-Feld „Self Model“, „World Model“ oder „Consciousness“ darf niemals als Hinweis gelten, dass die entsprechende Fähigkeit existiert. Die wissenschaftliche Autorität liegt in den zugrunde liegenden RQ/Hypothesen, Protokollen, DATA, Reviews und EVID-Entscheidungen.

## 24.5 Lokale und externe KI als austauschbare Forschungswerkzeuge

Aus den Arbeiten an lokalen Chat-Systemen, Kernschmied und Provider-Adaptern wurde eine weitere Designregel übernommen: Provider müssen austauschbar sein, ohne dass der wissenschaftliche Status eines Artefakts vom Marken- oder Modellnamen abhängt. Wichtig sind Eingabe, Ausgabe, Version, Berechtigung, Provenienz und der Pfad, auf dem ein Ergebnis in Code oder Forschung eingeflossen ist.

Ein lokales Modell kann Datenschutz und Reproduzierbarkeit verbessern; ein externes Modell kann Recherche- oder Codingqualität erhöhen. Beides ändert nicht die Grundregel: Kein Sprachmodell erhält allein durch Leistungsfähigkeit wissenschaftliche Autorität oder stillen Schreibzugriff auf den kausalen SNN-Kern.

## 24.6 Gateways, exakte Digitaldaten und periphere Laufzeit

Neural Symbiosis konkretisiert die Infrastrukturgrenze zwischen externen/peripheren Modellen und dem SNN. Der Gateway-Runtime besitzt eigene Zustände, Gewichte, Delays, RNG-Provenienz, Condition, Tick, Ressourcenmetriken und Strukturjournal. Dadurch kann ein Experiment Frozen/Random/Shuffle/Plastic kontrollieren, ohne den kanonischen Kernzustand heimlich umzudefinieren. Es existiert absichtlich kein allgemeiner produktiver „Plasticity on“-Schalter; wissenschaftliche Aktivierung muss über einen registrierten Experimentpfad erfolgen.

Für digitale Pfade ist die Trennung von **exaktem Payload** und **neuronaler Projektion** fundamental. Prüfsummen, Sequenzen, Codec und Provenienz gehören zum exakten Symbolzustand außerhalb des SNN. Eine neuronale Population darf eine Approximation oder Repräsentation tragen, aber niemals nachträglich als Beweis verwendet werden, dass die ursprünglichen Bits selbst neuronal gespeichert oder unverändert rekonstruiert wurden.

## 24.7 Körpertelemetrie als Datenprovenienz

Die Real-Body-/Wesen-Arbeiten formulieren eine Infrastrukturregel, die über das Frontend hinausgeht: **Keine Fantasiedaten.** Fehlende Sensor- oder Hostwerte bleiben `UNKNOWN`; gemessene, abgeleitete und lediglich dargestellte Größen sind zu unterscheiden. Diese Regel ist dieselbe epistemische Disziplin, die später DATA von Report und EVID trennt. Eine scheinbar vollständige Oberfläche darf eine Messlücke nicht durch einen plausiblen Default verdecken.

## 24.8 Technische Identität als reproduzierbare Konfiguration

Profile & Identity ergänzt die Persistenzschicht um versionierte technische Konfiguration, Digest, Revision, Lineage und Snapshotbindung. Für Experimente können damit `profile_id`, Revision, Profil-Digest und Snapshot-Digest gemeinsam gebunden werden. Das verbessert Reproduzierbarkeit, ohne den Profilbegriff psychologisch aufzuladen. Ein Profil ist eine deklarierte technische Identität; der dynamische neuronale Zustand und der vollständige kausale Checkpoint bleiben getrennte Objekte.


---

<a id="part-vi"></a>

# Teil VI — Epistemologie und Methodik der Schaffensgeschichte

## 25. Drei Forschungsachsen

Edition 1.8 führt drei gleichrangige, aber methodisch unterschiedliche Achsen: **empirisch-technisch**, **epistemologisch-methodisch** und **philosophisch-ethisch**. Gleichrangig bedeutet nicht, dass dieselben Evidenzregeln gelten. Ein Lauf kann einen empirischen Effekt prüfen. Eine Provenienzanalyse kann rekonstruieren, wie eine Entscheidung zustande kam. Eine normative These muss durch explizite Prämissen, Gegenargumente und Folgerungen getragen werden. Keine Achse darf die andere imitieren.

Die Aussagekoordinate lautet:

`Achse × Thema × Entwicklungsphase × Quellennähe × Evidenzstatus × Interpretationsart`.

Sie ersetzt Kapitelnummern nicht, ergänzt sie aber um die Frage, **welcher Typ von Aussage** vorliegt und mit welcher Art von Begründung er überhaupt geprüft werden kann. Ein S1-Artefakt kann beispielsweise sehr stark belegen, *dass* ein Lauf mit einem bestimmten Manifest stattgefunden hat; daraus folgt noch nicht automatisch, *welche Theorie* dieser Lauf trägt.

## 26. Quellennäheklassen S1–S4

Die in Edition 1.8 bereits verwendeten Felder `provenance_class: S1…S4` werden inhaltlich als **Quellennäheklassen** verstanden. Diese Benennung verhindert eine Kollision mit den in Teil VII verwendeten Herkunftsrollen wissenschaftlicher Aussagen.

| Klasse | Bedeutung | Typische Artefakte | Was die Klasse nicht garantiert |
| --- | --- | --- | --- |
| **S1** | source-bound Primärartefakt | Commits, Tags, frozen Preregistrierungen, DATA, Manifeste, Hashes | keine automatische Gültigkeit der Interpretation oder EVID-Promotion |
| **S2** | zeitgenössisches Prozessartefakt | Issues, Reviews, Chats, AI-Interaktionen, Arbeitsnotizen, Diffs | keine unabhängige Bestätigung und nicht zwingend vollständige Entscheidungsrekonstruktion |
| **S3** | zeitgenössische Selbstauskunft | Autorennotizen, Begründungen, Journale | keine externe Evidenz für den beschriebenen Sachverhalt |
| **S4** | retrospektive Rekonstruktion | spätere Zusammenfassungen, wiedergewonnene Chat-Kontexte, Erinnerung | kein wörtliches Original, kein sicherer Entstehungszeitpunkt, kein Prioritätsbeweis |

Die Klassen ordnen **Nähe zur ursprünglichen Quelle**, nicht epistemische Wahrheit. Ein S1-Datensatz kann aus einem inadäquaten Versuchsdesign stammen; ein S2-Human-Review kann eine korrekte Designkritik enthalten; eine S4-Rekonstruktion kann historisch plausibel sein, bleibt aber schwächer für Datums- oder Prioritätsbehauptungen.

Bei Widerspruch zwischen zeitgenössischem source-bound Artefakt und späterer Rekonstruktion hat das zeitgenössische Artefakt für die Frage „was war damals dokumentiert?“ Vorrang. Für andere Fragen — etwa methodische Angemessenheit — entscheidet nicht die Quellennäheklasse allein, sondern die jeweils passende Prüfung.

Die außerhalb des Repositories wiedergewonnenen Chat-Zusammenfassungen sind in [`chat_reconstruction.json`](sources/chat_reconstruction.json) bewusst S4. Wenn später Originaltranskripte eingebunden werden, entstehen neue Provenienzeinträge; die frühere S4-Rekonstruktion wird nicht stillschweigend in eine stärkere Quelle umgeschrieben.

## 27. KI-assistierte Forschung

KI-Unterstützung erzeugt eine zusätzliche Beitrags- und Provenienzdimension. Ein Vorschlag eines Assistenten ist nicht automatisch eine Idee des Autors; eine vom Autor verlangte Richtung ist nicht automatisch eine implementierte Funktion; ein generierter Patch ist nicht automatisch ein wissenschaftlicher Befund.

Seit der Verdichtung von `RQ-ETH-001` reicht deshalb die frühere lineare Kette `user requirement → AI proposal → human decision → commit → run → review → publication synthesis` allein nicht mehr aus. Sie wird als Ereignisfolge beibehalten, aber zusätzlich nach epistemischen Rollen codiert:

- **Konzeptualisierung** — Forschungsfrage, Ziel, Hypothese, Erfolgs- oder Abbruchbedingung;
- **Generierung/Transformation** — Text, Code, Analyse, Kontrollidee oder methodische Variante;
- **Validierung** — Quellen-, Code-, Mess-, Statistik- oder Konsistenzprüfung;
- **Selektion/Kanonisierung** — Übernahme, Revision, Verwerfung, DATA-/EVID-Zuordnung oder Veröffentlichung;
- **Verantwortung** — natürliche Person, die für den veröffentlichten Claim Rechenschaft übernimmt.

Das operative Beitragsmodell liegt in [`RQ_ETH_001_PROVENANCE_STUDY.md`](../../protocols/RQ_ETH_001_PROVENANCE_STUDY.md). Materieller epistemischer Beitrag, formale Autorenschaft und wissenschaftliche Verantwortung bleiben getrennte Variablen.

Die Arbeit nutzt KI zugleich als Forschungsgegenstand und als Arbeitsinstrument. Das erhöht das Risiko **rekursiver Bestätigungsfehler**: Ein Modell kann frühere eigene Formulierungen wiederfinden, paraphrasieren und dadurch wie eine zweite Quelle wirken. Gegenmaßnahmen sind unter anderem source-bound Originalquellen, getrennte Quellennähe- und Herkunftsklassen, Literaturquarantäne bis zur Prüfung, AI-Provenienzfelder und menschliche Review-Gates. Eine Modellwiederholung zählt nicht als unabhängige Bestätigung.

## 28. Falsifikation von Entstehungs- und Prioritätsaussagen

Auch Schaffensgeschichte muss revidierbar sein. Eine Behauptung wie „Idee X entstand zuerst am Datum Y“ ist nur zulässig, wenn das Artefakt den Inhalt tatsächlich trägt und die untersuchte Quellenmenge keinen älteren widersprechenden Fund enthält. Selbst dann ist zwischen **frühestem dokumentierten Nachweis** und **tatsächlichem Entstehungszeitpunkt** zu unterscheiden.

Edition 1.8 behauptet daher keine absolute Priorität für die rekonstruierten Vor-Repo-Ideen. Sie dokumentiert die **früheste derzeit wiedergewonnene Spur** innerhalb des tatsächlich geprüften Korpus. Neue ältere Primärartefakte revidieren die Chronologie additiv; sie machen die frühere Rekonstruktion nicht zu wissenschaftlichem Fehlverhalten.

## 28.1 Epistemische Regeln aus konkreten Korrekturereignissen

Die Methodik dieser Arbeit ist nicht nur programmatisch gesetzt. Mehrere Regeln wurden durch konkrete Fehlinterpretationen oder stärkere Kontrollen notwendig. Diese Fälle sind **methodische Zeugen**: Sie zeigen, dass eine Regel als Reaktion auf dokumentierte Probleme eingeführt wurde. Sie beweisen noch nicht, dass die Regel die Fehlerquote künftig kausal reduziert.

### Ein negatives Resultat setzt Testadäquanz voraus

Für `H-SNN-003-B` wurde `EXP-GEN-0047` zunächst leicht als Topologie-/Dimensions-Nullbefund lesbar. Die spätere methodische Entscheidung [`2026-09-17_snn003_topology_propagation_v1_adequacy.md`](../../decisions/2026-09-17_snn003_topology_propagation_v1_adequacy.md) klassifiziert den Lauf dagegen als **`INADEQUATE_TO_TEST_HYPOTHESIS`**: drei Neuronen und zwei Feed-forward-Synapsen ließen die Koordinatenmanipulation den behaupteten Mechanismus nicht hinreichend verändern.

Die zulässige Schlussfolgerung ist daher nicht „5D/Topologie hat keinen Effekt“, sondern „dieses Design war für den intendierten Effekt nicht ausreichend sensitiv“.

**Regel:** Vor Bestätigung, Nullbefund oder Falsifikation muss geprüft werden, ob die manipulierte Variable den behaupteten kausalen Mechanismus tatsächlich verändern konnte.

### DATA und Report sind verschiedene Objekte

Die Human Review [`EXP-GEN-0036/analysis/HUMAN-REVIEW-2026-09-16.md`](../../experiments/EXP-GEN-0036/analysis/HUMAN-REVIEW-2026-09-16.md) dokumentiert einen Reportingfehler: Gedankenstriche in universellen Summary-Spalten wurden zunächst als fehlende DATA gelesen, obwohl protokollspezifische Runs und Statistiken existierten.

**Regel:** Ein Report ist eine Transformation von DATA und damit ein eigenes fehlerfähiges Objekt. Bei claim-relevanten Unstimmigkeiten müssen source-bound Rohartefakte, protokollspezifische Statistik und Manifest vor der Interpretation geprüft werden.

### Eine positive Baseline-Differenz ist noch keine Mechanismusidentifikation

`EXP-S6-SEM-CL-001` zeigte unter seinem Protokoll Semantic+Replay gegenüber No-Replay. Die stärkere Präregistrierung [`EXP-S6-SEM-CL-002.md`](../../preregistrations/EXP-S6-SEM-CL-002.md) führte gematchtes Raw-Replay ein. Unter dieser Kontrolle wurde kein konfirmatorischer Zusatznutzen semantischer Prototypen bestätigt. `CL-003` prüfte anschließend eine Dosisalternative; der präregistrierte Interaktionstest bestätigte keinen Dosis-Effekt, obwohl deskriptive Unterschiede verlockend stärker formuliert werden konnten.

**Regel:** Die Qualität einer Mechanismusbehauptung hängt nicht nur von Effektgröße oder Signifikanz ab, sondern davon, ob die plausibelste konkurrierende Erklärung durch einen geeigneten Kontrollarm adressiert wurde.

### Referenzkonformität, Human Review und unabhängige Replikation sind getrennt

Der Stage-0-Konformitätspfad illustriert drei verschiedene Autoritätsebenen. Der prospektive Lauf `EXP-STAGE0-20260918-MODEL-CONFORMANCE-V2-PROMO-R1` erfüllt den aktuellen Provenienzvertrag und wurde nach Human Review als `EVID-2026-18` für den eng begrenzten Claim registriert. Sein eigenes Resultatfeld hält zugleich `independent_authorship_replication=false` fest.

**Regel:** Referenzkonformität kann starke technische Evidenz sein; Human Review kann eine scoped Interpretation autorisieren; unabhängige Replikation bleibt dennoch ein eigenes Kriterium. Keine dieser Ebenen darf stellvertretend für die andere gezählt werden.

## 28.2 Methodik der epistemologisch-methodischen Achse

Die epistemologisch-methodische Achse benötigt eigene Prüfverfahren. Sie darf nicht nur kommentieren, wie Forschung „eigentlich“ funktionieren sollte. Für MHRN werden deshalb sechs Verfahren unterschieden:

1. **Provenienzanalyse:** Welche Quelle existierte zu welchem Zeitpunkt, mit welcher Quellennähe und welchem damaligen Status?
2. **Entscheidungsrekonstruktion:** Welche Alternativen waren vor Implementierung, Ausführung oder Interpretation dokumentiert?
3. **Status-Transition-Audit:** Wann wechselte ein Objekt zwischen Idee, Spezifikation, Präregistrierung, DATA, Review, EVID und Claim?
4. **Kontrafaktische Prozessprüfung:** Welche Schlussfolgerung wäre unter einer stärkeren Baseline, anderer Projektion oder fehlendem Gate entstanden?
5. **Revisionstracing:** Welche konkrete Architektur-, Registry- oder Methodikänderung folgte aus einem negativen oder korrigierten Befund?
6. **AI-/Beitragsprovenienzprüfung:** Wer oder was erzeugte, prüfte, selektierte oder kanonisierte einen materiell relevanten Beitrag?

Für jede Prozessbehauptung muss außerdem zwischen drei Ebenen unterschieden werden:

- **deskriptiv:** ein Gate, Review oder Statuswechsel existierte;
- **kausal-prozessual:** dieser Schritt veränderte eine Entscheidung oder verhinderte eine konkrete Fehlklassifikation;
- **generalisierend:** die Methode senkt über Fälle hinweg die Fehlerquote oder verbessert Reproduzierbarkeit.

Die erste Ebene kann häufig aus bestehenden Artefakten rekonstruiert werden. Die zweite benötigt eine belastbare Ereigniskette oder kontrafaktische Vergleichsmöglichkeit. Die dritte benötigt eine systematische Teilstudie und darf nicht allein aus einzelnen Anekdoten abgeleitet werden.

## 28.3 Explorativ, konfirmatorisch und rekonstruktiv

MHRN unterscheidet drei Forschungsmodi, die nicht miteinander verrechnet werden dürfen:

| Modus | Zweck | Vorab-Festlegung | Zulässige Schlussfolgerung |
| --- | --- | --- | --- |
| **explorativ** | Hypothesen-, Mechanismus- und Fehlersuche | flexibel, Änderungen müssen nachträglich kenntlich bleiben | Hypothesengenerierung, Diagnose, Designrevision |
| **konfirmatorisch** | vorab definierte Hypothesenprüfung | Endpunkte, Kontraste, Seeds, Ausschlüsse und Erfolgsregeln vor Ausführung eingefroren | protokollgebundene Bestätigung, Nichtbestätigung oder Falsifikation |
| **rekonstruktiv** | historische oder epistemische Rekonstruktion aus vorhandenen Artefakten | Korpus, Suchregel und Quellennähe möglichst explizit | Aussagen über dokumentierte Spuren und Prozessketten, begrenzt durch Quellenabdeckung |

Die frühe NeuroGenesis-/Brain-5D-Geschichte ist überwiegend rekonstruktiv. Die CL-003-Ausführung ist konfirmatorisch angelegt. Viele Frontier-Arbeiten sind explorativ oder programmatisch. Ein ursprünglich explorativer Befund kann eine spätere konfirmatorische Studie motivieren, wird dadurch aber nicht rückwirkend präregistriert.

## 28.4 Präregistrierung schützt auch vor architektonischem Nachrationalisieren

Die Forschungsarbeit entsteht in einem schnell iterierenden Engineeringkontext. Ein Freeze schützt dort nicht nur vor klassischem p-Hacking, sondern auch davor, nach Sichtung der DATA neue Zielgrößen, Baselines oder Architekturrollen unbemerkt als ursprünglichen Erfolgsmaßstab auszugeben.

CL-003 ist ein konkretes Beispiel: Der deskriptiv mit der Dosis wachsende Semantic-minus-Raw-Unterschied hätte nachträglich als positiver Dosisbefund erzählt werden können. Der vorab definierte Interaktionstest C4 blieb jedoch negativ; deshalb ist die stärkere Behauptung nicht zulässig.

Präregistrierung trennt prospektive Hypothesenprüfung von nachträglicher Musterdeutung; diese Funktion wird auch in der methodischen Literatur als zentraler Zweck beschrieben ([Nosek et al., 2018](REFERENCES.md#ref-NOSEK2018)). Für MHRN lautet die zusätzliche Regel: **Eine spätere bessere Erklärung darf den eingefrorenen ursprünglichen Erfolgsmaßstab nicht umschreiben.**

## 28.5 Revidierbarkeit als Qualitätskriterium

Eine starke Aussage in MHRN nennt nicht nur, warum sie aktuell zulässig ist, sondern auch, welche Beobachtung oder methodische Kritik sie ändern würde. Revisionskriterien sind deshalb keine rhetorische Vorsicht, sondern Teil der Claim-Spezifikation.

Beispiele:

- ein 5D-/Topologieclaim verlangt geometriesensitive matched controls;
- ein SemanticMemory-Zusatznutzen verlangt vorab begründeten Vorteil gegenüber gematchtem Raw-Replay;
- ein Weltmodell verlangt über One-Step-Korrelation hinaus Mehrschritt- und Entscheidungsnutzen unter geeigneten Kontrollen;
- ein Selbstmodell verlangt kausal relevante Self/Other-Differenzierung;
- eine Prozessmethodik, die wissenschaftliche Fehlklassifikationen reduzieren soll, muss gegenüber einer einfacheren Darstellung messbaren Audit-Nutzen zeigen.

Damit verbindet Revidierbarkeit die aktuelle Synthese mit klaren zukünftigen Prüfbedingungen.

## 28.6 RQ-EPIST-001 bleibt von der Prozessmethodik getrennt

Die kanonische `RQ-EPIST-001` lautet weiterhin sinngemäß: **Was gilt als Erkenntnis des Systems MHRN im Unterschied zur Erkenntnis des Forschers?** Die historische Hypothese `H-EPIST-001-A` bleibt aus Provenienzgründen unverändert erhalten.

Frühere generische `runtime_ticks_v1`- und `epistemic_boundary_audit_v1`-Läufe dürfen nicht rückwirkend als empirischer Nachweis dieser kategorialen Unterscheidung behandelt werden. Die vorhandenen Berichte stellen selbst fest, dass dafür spezifische Messung beziehungsweise menschlich-konzeptuelle Entscheidung erforderlich bleibt. `RQ-EPIST-001` bleibt daher **open / untested**.

Die Frage, ob die **Forschungsprozess-Governance** Fehlklassifikationen reduziert, ist davon verschieden und erhält deshalb einen eigenen Forschungsgegenstand.

## 28.7 RQ-EPIST-002 — Prozessgovernance als prüfbarer Forschungsgegenstand

**Kanonische Forschungsfrage `RQ-EPIST-002`:**

> Unter welchen Bedingungen reduziert eine explizite Trennung von Quelle, Entscheidung, Ausführung, DATA, Review, EVID und Claim epistemische Fehlklassifikationen in schnell iterierender, KI-assistierter MHRN-Forschung?

**Hypothese `H-EPIST-002-A`:**

> Reviewer, die ein status- und provenienzgetrenntes Claim-Paket erhalten, weisen gegenüber einem inhaltlich äquivalenten, aber abgeflachten Summary-Paket eine geringere Rate vorab definierter epistemischer Klassifikationsfehler auf.

### Material und Einheit

Die primäre Einheit ist eine **Claim-Episode**: von der ersten relevanten Beobachtung oder Behauptung bis zur letzten im Untersuchungsfenster dokumentierten Entscheidung. Kandidaten werden aus abgeschlossenen oder eingefrorenen MHRN-Fällen gezogen; laufende Fälle dürfen nur verwendet werden, wenn ihr Cut-off vor der Kodierung festgelegt wird.

Die vier in §28.1 beschriebenen Fälle sind historische methodische Zeugen und dürfen die spätere Stichprobe informieren. Sie werden **nicht automatisch** als konfirmatorische Beobachtungen für `H-EPIST-002-A` gezählt.

### Prospektives Vergleichsdesign

Für dieselbe Claim-Episode werden zwei inhaltlich äquivalente Darstellungen erstellt:

- **separiertes Paket:** Quelle, Ausführung, DATA, Report, Review, EVID und Claim-Grenze als getrennte Felder/Artefakte;
- **abgeflachtes Paket:** gleiche inhaltliche Informationen in einer konventionellen zusammenhängenden Summary ohne explizite Statusachsen.

Reviewer werden randomisiert oder in einem ausbalancierten Crossover-Design den Darstellungen zugewiesen. Reihenfolge und Episode müssen gegen Lerneffekte kontrolliert werden.

### Primäre Endpunkte

Vor einer Präregistrierung sind mindestens folgende Fehlerklassen operational zu fixieren:

1. DATA fälschlich als EVID klassifiziert;
2. Reportprojektion fälschlich als Roh-DATA behandelt;
3. technische Reproduzierbarkeit mit Hypothesenbestätigung gleichgesetzt;
4. Human Review mit unabhängiger Replikation gleichgesetzt;
5. retrospektive Rekonstruktion als zeitgenössische Primärquelle behandelt;
6. AI-Synthese als unabhängige externe Quelle gewertet;
7. Claim-Reichweite über die dokumentierte Grenze hinaus erweitert.

Primärer Outcome ist die **Fehlklassifikationsrate pro Reviewentscheidung**. Sekundär können Korrekturzeit, Inter-Rater-Übereinstimmung, unbegründete Claim-Erweiterungen und benötigte Rückfragen gemessen werden.

### Referenz und Adjudikation

Die „richtige“ Klassifikation darf nicht von demselben Summary abhängen, das getestet wird. Sie wird aus source-bound Primärartefakten durch ein vorab definiertes Adjudikationsverfahren erzeugt. Uneinigkeit der Adjudikatoren bleibt sichtbar und wird nicht durch Mehrheitsentscheid allein als objektive Wahrheit ausgegeben.

### Failure- und Revisionskriterien

`H-EPIST-002-A` muss verworfen oder enger gefasst werden, wenn:

- die beiden Darstellungen nicht informationsäquivalent hergestellt werden können;
- die Fehlerklassen keine ausreichende Inter-Rater-Reliabilität besitzen;
- das separierte Paket keine niedrigere Fehlklassifikationsrate zeigt;
- der Vorteil nur durch wesentlich höhere Bearbeitungszeit entsteht und nach vorab definierter Nutzenfunktion nicht trägt;
- oder die Adjudikationsreferenz selbst nicht ausreichend source-bound und reproduzierbar ist.

Das operative Design wird in [`RQ_EPIST_002_PROCESS_GOVERNANCE_STUDY.md`](../../protocols/RQ_EPIST_002_PROCESS_GOVERNANCE_STUDY.md) versioniert. Es ist zunächst **Protokolldesign, nicht präregistriert und nicht zur konfirmatorischen Ausführung autorisiert**.

## 28.8 Gegenwärtiger Ergebnisstand der epistemologischen Achse

Der aktuell belegbare Befund ist enger als „die Governance verbessert Wissenschaft“:

1. Es existieren dokumentierte Korrekturereignisse, bei denen stärkere Kontrollen oder source-bound Prüfung die zulässige Interpretation verändert haben.
2. Aus diesen Ereignissen wurden dauerhafte technische und dokumentarische Regeln abgeleitet.
3. Die Prozessarchitektur ist dadurch **formal restriktiver und auditierbarer** geworden.
4. Noch nicht gezeigt ist, dass diese Architektur über Fälle oder Reviewer hinweg die Fehlklassifikationsrate kausal senkt.

Die bisherigen Fälle stützen damit die **Notwendigkeit einer Prozessstudie**, nicht bereits deren positives Ergebnis.

**Zwischenfazit.** Rekursive Epistemik besitzt einen empirisch anschlussfähigen methodischen Kern, sobald ihre Selbstbeschreibung in prüfbare Ereignisse und Vergleichsdesigns übersetzt wird. Der wissenschaftliche Gegenstand ist dann nicht „wir arbeiten sorgfältiger“, sondern: Welche Status-, Provenienz- und Revisionsdarstellung führt unter kontrollierten Bedingungen zu welchen Entscheidungen?


---

<a id="part-vii"></a>

# Teil VII — Integrität, Autorschaft und kumulative Wissenschaft

## 29. Kumulative Wissenschaft, Plagiat und Provenienz

Wissenschaft ist kumulativ: Begriffe, Modelle, Methoden, mathematische Werkzeuge, Software, Datenpraktiken und Denkfiguren entstehen in Traditionslinien. Daraus folgt gerade nicht, dass Attribution entbehrlich wäre. Edition 1.8 trennt deshalb **epistemische Kumulativität** von **institutionellem Plagiat**.

Fremde Texte, Daten, Code, Abbildungen oder zurechenbare Ideen werden nicht als eigene Primärleistung ausgegeben. Zugleich wird nicht behauptet, dass jede technische Kombination allein durch Zitieren neuartig wird. Ein korrekt zitierter bekannter Mechanismus bleibt ein bekannter Mechanismus; ein eigener experimenteller Befund bleibt ein eigener Befund, auch wenn seine theoretischen Voraussetzungen aus langer wissenschaftlicher Vorarbeit stammen.

Die zugespitzte Autorposition aus der Vorgängerarbeit — sinngemäß, Forschung sei in einem weiten Sinn immer Übernahme und Weiterverarbeitung vorhandenen Wissens — wird deshalb nicht als Billigung akademischen Fehlverhaltens übernommen. Sie bezeichnet eine epistemische Beobachtung: **Forschung beginnt nicht bei null.**

### 29.1 Zwei Bedeutungen müssen getrennt bleiben

| Ebene | Gemeint ist | Konsequenz für MHRN |
|---|---|---|
| **epistemisch** | Erkenntnis entsteht durch Übernahme, Kritik, Kombination und Transformation vorhandenen Wissens | Kumulativität ist Grundbedingung wissenschaftlicher Arbeit |
| **institutionell/verfahrensbezogen** | fremde Leistungen werden ohne angemessene Kennzeichnung als eigene dargestellt | unzulässig, weil Provenienz, Nachprüfbarkeit und Verantwortungszuordnung beschädigt werden |

Der zentrale Begriff ist daher nicht Eigentum an Wahrheit, sondern **nachvollziehbare Herkunft**.

Für jede wesentliche wissenschaftliche Aussage soll rekonstruierbar bleiben:

- welche Quelle oder welches Artefakt zugrunde liegt;
- ob eine Aussage übernommen, abgeleitet, neu kombiniert oder experimentell erzeugt wurde;
- welche Transformation MHRN vorgenommen hat;
- welche Unsicherheit besteht;
- welche frühere Fassung denselben Gedanken bereits enthielt;
- und an welcher Stelle Kritik, Replikation oder Falsifikation ansetzen kann.

Die praktische Autorposition lautet:

> Wissen soll möglichst frei zirkulieren; seine Herkunft soll dabei möglichst sichtbar bleiben.

Freier Wissenstransfer und strikte Attribution sind damit keine Gegensätze. Je einfacher Wissen weitergegeben und verändert werden kann, desto wichtiger wird eine belastbare Provenienzkette.

### 29.2 Fünf Herkunftsrollen wissenschaftlicher Aussagen

Der repositoryweite Integritätsvertrag unterscheidet mindestens fünf **Herkunftsrollen wissenschaftlicher Aussagen**. Diese Rollen beantworten die Frage, *woher der Aussageinhalt stammt beziehungsweise welche epistemische Funktion er hat*. Sie sind ausdrücklich nicht mit den S1–S4-Quellennäheklassen aus Teil VI identisch:

1. **MHRN observation** — durch source-bound Experiment, Messung oder Verification-Artefakt erzeugt;
2. **MHRN interpretation** — Schlussfolgerung aus Beobachtungen, mit expliziten Grenzen und ohne automatische EVID-Promotion;
3. **External theory or method** — Theorie, Algorithmus, Methode, Benchmark oder Befund aus externer Literatur;
4. **MHRN prior work** — frühere Edition, Bericht, Experiment oder öffentliches Projektartefakt;
5. **AI-assisted wording or synthesis** — maschinelle Hilfe bei Recherche, Struktur, Kritik, Code oder Formulierung; niemals allein Quellenautorität.

Diese Klassen können in einem Absatz zusammenwirken, dürfen aber nicht ineinander kollabieren. Eine zitierte Theorie ist kein MHRN-Datensatz. Ein MHRN-Lauf beweist keine weltweite Priorität. Eine AI-Synthese ist keine unabhängige Fachquelle. Eine ältere eigene Passage wird durch Neuformatierung nicht zu einer neuen Beobachtung.

### 29.3 Kumulative Forschung erzeugt stärkere, nicht schwächere Attribution

Je stärker MHRN etablierte Modelle, Open-Source-Software, wissenschaftliche Theorie und AI-Werkzeuge kombiniert, desto genauer müssen vier Ebenen getrennt werden:

1. **externe Theorie oder Methode** — beispielsweise Izhikevich-Neuronen, STDP, Three-Factor Learning, Homeostase, Complementary Learning Systems, Predictive Coding oder Safe Interruptibility;
2. **eigene frühere Arbeit** — Brain-5D-/MHRN-Fassungen, Experimente, Protokolle und frühere Theoriearbeit;
3. **Werkzeugbeitrag** — Sprachmodell, Coding-Assistent, Suchsystem, Bibliothek, Simulator oder Analysewerkzeug;
4. **aktuelle Eigenleistung** — konkrete Integration, Definition, Hypothese, Experiment, Falsifikation, Analyse oder Synthese dieser Edition.

Der wissenschaftliche Beitrag entsteht nicht dadurch, dass Ebene 1 oder 3 verschwiegen wird, sondern dadurch, dass Ebene 4 **präzise von ihnen unterschieden** werden kann.

### 29.4 Was überhaupt als eigener wissenschaftlicher Beitrag gelten kann

Ein Beitrag muss kein spektakulärer „Durchbruch“ sein. Für MHRN kommen mindestens folgende Beitragstypen in Betracht:

- neue oder präzisierte Begriffsbildung;
- reproduzierbare Implementierung eines klar begrenzten Mechanismus;
- systematische Synthese bisher getrennt behandelter Methoden;
- neues Mess-, Kontroll- oder Governanceverfahren;
- kausal interpretierbare Ablation;
- negative oder falsifizierende Beobachtung;
- methodische Infrastruktur für strengere Experimente;
- dokumentierte Widerlegung einer früheren Annahme;
- oder eine klar begründete Aussage darüber, **was mit den vorhandenen Daten gerade nicht gezeigt wurde**.

Damit wird Neuheit von wissenschaftlichem Wert getrennt. Ein negativer Befund kann wissenschaftlich wertvoll sein, obwohl er keine neue Fähigkeit demonstriert. Eine ungewöhnliche Architektur kann wissenschaftlich unzureichend belegt sein, obwohl sie technisch originell wirkt.

### 29.5 Freier Wissenstransfer als Verpflichtung

Die Autorposition der Vorgängerarbeit befürwortet, dass andere MHRN-Inhalte weiterverwenden, prüfen, verändern und weiterentwickeln können, soweit Lizenz, Rechte und Datenschutz dies zulassen. Daraus folgt keine Aufgabe wissenschaftlicher Urheberschaft, sondern eine stärkere Dokumentationspflicht.

Die praktische Strategie lautet:

1. aufschreiben, was übernommen wurde;
2. aufschreiben, was verändert wurde;
3. aufschreiben, was neu gemessen wurde;
4. offene Herkunfts- und Neuheitsfragen sichtbar lassen;
5. negative und null Ergebnisse nicht entfernen;
6. Replikation und Kritik technisch erleichtern.

## 30. Einheitliches Zitations-, Quellen- und Wiederverwendungsmodell

Die neue Textschicht verwendet Autor-Jahr-Zitation in Anlehnung an APA 7 ([American Psychological Association, 2020](REFERENCES.md#ref-APA2020)). Literaturquellen erhalten stabile Kennungen, vollständige bibliografische Angaben, Original-URL beziehungsweise DOI, Prüftag und den **tatsächlich geprüften Leseumfang**.

Damit wird ein zentraler Fehler vermieden: Eine Metadatenprüfung darf nicht als Volltextprüfung erscheinen, ein Abstract nicht als vollständige Methodenprüfung und ein Suchtreffer nicht als belastbare Quelle.

Eigene Vorarbeiten werden mit Edition, Pfad und Git-Revision referenziert. Historische Quellenbände bleiben lesbar, aber ihre ältere Bibliografie wird nicht automatisch neu zertifiziert. Wörtliche Übernahmen benötigen Seiten-, Abschnitts- oder eindeutigen Fundstellenbezug. Eigene Übersetzungen werden als solche gekennzeichnet. Abbildungen, Tabellen, Daten und Code erfordern zusätzlich Provenienz- und gegebenenfalls Lizenzprüfung.

### 30.1 Zitierstandard und Quellenklassen

Edition 1.8 verwendet Autor-Jahr-Zitation nach APA 7 ([American Psychological Association, 2020](REFERENCES.md#ref-APA2020)). Externe Behauptungen sollen **claim-nah**, also direkt am tragenden Satz, belegt werden.

Wo eine ursprüngliche Forschungsarbeit verfügbar und passend ist, wird Primärliteratur bevorzugt. Review-, Survey- und Synthesearbeiten werden als Sekundärliteratur gekennzeichnet. Diese Trennung entspricht auch der allgemeinen Forderung, Literaturquellen nach ihrer tatsächlichen Aussagekraft für den konkreten Claim zu prüfen ([ICMJE, 2026](REFERENCES.md#ref-ICMJE2026)).

Das maschinenlesbare Literaturregister unterscheidet:

- `primary`;
- `secondary`;
- `guideline`;
- `standard`.

Diese Klassen haben unterschiedliche Rollen. Eine Guideline kann Autorenschafts- oder Publikationsregeln stützen, aber keinen MHRN-Neuronenmechanismus beweisen. Eine Review kann einen Forschungsstand zusammenfassen, ersetzt aber nicht automatisch die Primärquelle eines spezifischen Befunds.

Im Fließtext darf `et al.` entsprechend der Zitierkonvention zur Kürzung von Mehrfachautorenschaften verwendet werden; im Literaturverzeichnis werden die für diese Edition erfassten Autorenlisten vollständig ausgegeben.

### 30.2 Prüf- und Verifikationsstufen einer Quelle

MHRN unterscheidet praktisch mindestens:

- **bibliographic metadata checked** — Identität, Titel, Jahr, Publikationsort/DOI überprüft;
- **metadata and abstract checked** — zusätzlich Gegenstand und grobe Claim-Passung aus Abstract/Index geprüft;
- **primary text checked** — relevante Primärpassage, Methode oder Argumentation tatsächlich gelesen;
- **official guidance checked** — aktuelle Originalrichtlinie oder Standardquelle geprüft;
- **unverified lead** — möglicherweise relevant, aber nicht zitierfähig.

Aus dieser Hierarchie folgt eine einfache Regel:

**Der Quellenstatus ist Teil der Tragweite des Claims.**

Ein Satz darf nicht stärker formuliert werden, als es der tatsächlich geprüfte Quellenumfang rechtfertigt.

### 30.3 Claim-nahe Zitation statt Bibliografie als Dekoration

Eine Referenz am Ende eines langen Abschnitts kann nicht automatisch sämtliche Sätze des Abschnitts tragen. Edition 1.8 verlangt deshalb, dass externe Tatsachenbehauptungen, methodische Präzedenzfälle und konkrete theoretische Zuordnungen möglichst direkt am jeweiligen Claim belegt werden.

Das gilt besonders für:

- quantitative externe Befunde;
- behauptete biologische Mechanismen;
- Prioritäts- oder Neuheitsaussagen;
- Rechts- oder Richtlinienaussagen;
- Leistungswerte fremder Systeme;
- Definitionen, die einer bestimmten Theorie zugeschrieben werden.

Eine Referenz belegt nur den Satz, für den sie tatsächlich einschlägig ist.

### 30.4 Quellenzustände: VERIFIED, CANDIDATE und QUARANTINED

Neben der bibliografischen Quellenklasse wird der **Nutzungsstatus** getrennt behandelt:

- **VERIFIED:** bibliografische Identität und der verwendete Claim wurden hinreichend geprüft;
- **CANDIDATE:** plausibler relevanter Hinweis, aber noch nicht zitierbereit;
- **QUARANTINED:** Titel, Begriff oder Claim wurde gefunden, etwa in alten Notizen oder AI-assistierter Recherche, aber eine hinreichend belastbare Quelle wurde nicht geklärt.

Quarantäne ist kein Wahrheitsurteil. Sie bedeutet lediglich:

**Diese Quelle darf noch keine wissenschaftliche Last tragen.**

Frühere Beispiele wie ein vermeintlich normativer `ArithSpec`-Standard zeigen, warum diese Trennung notwendig ist: Wiederholung innerhalb eines Projekts verwandelt eine ungeprüfte Bezeichnung nicht in externe Autorität.

### 30.5 Codeattribution und Lizenzprovenienz

Für kopierten oder adaptierten externen Code werden mindestens dokumentiert:

- Upstream-Projekt;
- exakte Quelle, Version, Release oder Commit;
- Lizenz;
- betroffene Datei/Funktion oder algorithmische Quelle;
- Umfang der Änderung;
- Importdatum;
- verantwortliche Prüfung.

Eine Dependency im Paketmanager ist keine ausreichende Attribution, wenn konkreter Quellcode oder eine charakteristische Implementierung übernommen wurde.

Auch bei unabhängig geschriebenem Code ist der wissenschaftliche Ursprung eines Mechanismus zu zitieren, wenn die Implementierung erkennbar auf einer publizierten Methode basiert.

### 30.6 Daten, Abbildungen, Tabellen und abgeleitete Darstellungen

Für nicht rein eigene Darstellungen sind zu unterscheiden:

- fremde Rohdaten;
- eigene Transformation fremder Daten;
- reproduzierte Abbildung;
- adaptierte Abbildung;
- eigene Abbildung auf Basis fremder Theorie;
- eigene Abbildung aus MHRN-DATA.

Die wissenschaftliche Herkunft und die rechtliche Nutzbarkeit sind getrennte Fragen. Eine korrekte Zitation ersetzt keine gegebenenfalls erforderliche Lizenz oder Nutzungserlaubnis.

### 30.7 Eigene Vorarbeiten und Text-Recycling

Die Editionslinie 1.0–1.8 enthält erhebliche Eigenwiederverwendung. Das ist im Entwicklungsprozess erwartbar, darf im Publikationskontext aber nicht als unabhängige Neuproduktion dargestellt werden.

Edition 1.8 behandelt ältere eigene Manuskripte als **MHRN prior work**. Der ungekürzte Quellenband `LEGACY_V17.md` bewahrt den historischen Text, während die aktuelle Edition Inhalte neu strukturiert, korrigiert und erweitert.

Bei substantieller Wiederverwendung gilt:

- Herkunft der früheren Fassung nennen;
- identische Daten nicht als neues Experiment darstellen;
- Reanalyse von Neudatenerhebung unterscheiden;
- ältere öffentliche Verbreitung offenlegen;
- wesentliche inhaltliche Änderungen dokumentieren.

„Self-plagiarism“ wird nicht über eine projektinterne Prozentgrenze definiert. Die sichere Regel ist Transparenz über substantielle Eigenwiederverwendung.

## 31. Prior Art, Neuheit und Beitragsgrenzen

MHRN verwendet etablierte neuronale Modelle, STDP, Three-Factor Learning, Homeostase, graphische Nullmodelle, Replay und Gedächtnistheorien. Beispielsweise sind Izhikevich-Neuronen ([Izhikevich, 2003](REFERENCES.md#ref-IZHIKEVICH2003)), timingabhängige synaptische Plastizität ([Bi & Poo, 1998](REFERENCES.md#ref-BI_POO1998)), Drei-Faktor-Regeln ([Frémaux & Gerstner, 2016](REFERENCES.md#ref-FREMAUX2016)), homeostatisches synaptisches Scaling ([Turrigiano et al., 1998](REFERENCES.md#ref-TURRIGIANO1998); [Turrigiano, 2008](REFERENCES.md#ref-TURRIGIANO2008)) und Complementary Learning Systems ([McClelland et al., 1995](REFERENCES.md#ref-MCCLELLAND1995)) etablierte Vorarbeiten.

Aus der Kombination etablierter Komponenten folgt wissenschaftliche Neuheit weder positiv noch negativ automatisch.

### 31.1 Beitrags- und Neuheitsmatrix

Die Vorgängerarbeit führte bereits eine explizite Neuheitsmatrix. Edition 1.8 übernimmt deren Logik vollständig:

| Kandidat | MHRN-Beitrag | Status der Neuheit | Nächster Prüfpfad |
|---|---|---|---|
| Logical Identity / Physical Slot / Synaptic Reduction / Execution Scheduling | explizite Trennung von Objektidentität, Speicherlage, Reduktionsreihenfolge und Ausführungsplanung | potenzieller methodischer Beitrag; Priorität offen | Simulator-/HPC-Prior-Art, formaler Vergleich, Ablation |
| Proposal → Approval → Mutation → Journal → Undo | reversible, auditierbare Grenze struktureller Änderungen | Engineeringbeitrag in MHRN belegt; externe Neuheit offen | Frameworkvergleich, Rollback-/Fehlerexperimente |
| Content Gateway / Compute Backend | Informations-/Kausalgrenze getrennt von Ausführungsressource | konzeptioneller MHRN-Beitrag; Priorität offen | Schnittstellen- und Safety-Prior-Art |
| source-bound DATA/EVID separation | technische Ausführung kann EVID nicht selbst erzwingen | Infrastrukturbeitrag; nicht als neue Wissenschaftsnorm behauptet | Repro-/MLOps-/Neurotools-Vergleich |
| getrennte Engineering-/Scientific-Maturity-Achsen | Technikreife und wissenschaftliche Tragfähigkeit werden separat geführt | projektinterne Operationalisierung | externe Review-/Nutzerprüfung |
| 5D address layout | technische Adress-/Geometrierepräsentation | keine Neuheits- oder Überlegenheitsbehauptung | dimensions- und topology-matched Ablationen |
| Stage-6 memory/world-model stack | gebundene Memory-/Prediction-Infrastruktur | Synthese/Implementierung; starke kognitive Claims offen | Replay-, Semantization-, Prediction-Error- und Rollout-Experimente |
| spezialisierte Pfade / MSBA | modality-specific contracts für Audio, Vision und Digital | Systemintegration; funktionaler Vorteil offen | matched modality/frozen/random/shuffle controls |
| integriertes Nervensystem / Embodiment | Sensorik, Aktorik, Ressourcen und fail-closed Grenzen | Engineeringintegration | Closed-Loop-/No-Effect-/Lesion-Studien |
| technische Identität / Behavior Profile | versionierte Identität, Lineage und Profilzustand | technischer Mechanismus, kein psychologisches Selbst | causal self/other und checkpoint-equivalence tests |
| rekursive Epistemik | Objekt-Gateways und Forschungsprozess-Gateways werden gemeinsam als provenancegebundene Übergänge betrachtet | Theorie-/Methodenkandidat; Neuheit offen | systematischer Prior-Art- und Erklärungskraftvergleich |

Die Grundregel lautet:

`implemented` oder `unusual` bedeutet nicht `novel`.

### 31.2 Neuheit besitzt mehrere Reichweiten

Der Begriff „neu“ kann mindestens bedeuten:

1. neu innerhalb des lokalen Projekts;
2. neu innerhalb der bisherigen MHRN-Editionslinie;
3. neue Kombination bekannter Methoden;
4. neue Anwendung eines bekannten Mechanismus;
5. neuer empirischer Befund;
6. neue methodische Operationalisierung;
7. wissenschaftliche Erstbeschreibung gegenüber der publizierten Prior Art.

Diese Reichweiten dürfen nicht sprachlich ineinander geschoben werden. Ein neuer Projektname ist keine wissenschaftliche Erstentdeckung. Ein reproduzierbarer negativer Befund kann dagegen ein neuer empirischer Beitrag sein, obwohl keine neue Architekturkomponente entsteht.

### 31.3 Prior-Art-Prüfung ist ein eigener Forschungspfad

Für jeden Neuheitskandidaten müssen mindestens beantwortet werden:

- Welche etablierten Begriffe beschreiben denselben oder einen ähnlichen Mechanismus?
- Gibt es bekannte Implementierungen?
- Ist die MHRN-Differenz nur terminologisch, technisch oder wissenschaftlich funktional?
- Ist die Kombination bereits publiziert?
- Welcher Teil ist tatsächlich neu: Konzept, Implementierung, Kontrollvertrag, Experiment oder Ergebnis?
- Welche Gegenquelle würde den Neuheitsclaim widerlegen?

Ein interner Repository-Audit kann diese Prüfung vorbereiten, aber keine weltweite Prior-Art-Suche ersetzen.

### 31.4 Neuheit und Nutzen sind unabhängig

Eine Struktur kann wissenschaftlich nützlich sein, obwohl ähnliche Strukturen bereits existieren. Umgekehrt kann ein ungewöhnlicher Mechanismus wissenschaftlich wertlos bleiben, wenn er keinen nachweisbaren Erkenntnis- oder Funktionsgewinn erzeugt.

Edition 1.8 trennt daher:

**Neuheitsfrage:** Gibt es dies bereits?

von

**Wirkungsfrage:** Leistet es unter kontrollierten Bedingungen etwas Relevantes?

### 31.5 Negative und null Ergebnisse als Beitragsform

Die CL-002-Falsifikation, die negativen CL-003-Primärkontraste, die nicht testadäquate frühe 5D-Studie und historische negative Langzeitbefunde bleiben Teil der Forschungsleistung.

Eine wissenschaftliche Arbeit wird nicht dadurch belastbar, dass jede Ausgangsidee bestätigt wird. Sie wird belastbarer, wenn sichtbar bleibt,

- welche Hypothesen scheiterten;
- welche Messung unzureichend war;
- welche Claim-Reichweite reduziert werden musste;
- welche Architektur dadurch vereinfacht werden kann;
- und welche neue Frage erst aus dem negativen Resultat entstanden ist.

Das Entfernen negativer Ergebnisse würde nicht nur die Statistik verzerren, sondern auch die tatsächliche Autorschaft an der Entwicklungsgeschichte verschleiern.

## 32. Similarity, Quellenquarantäne und Integritätsprüfung

Interne Similarity-Prüfungen reduzieren Risiken, zertifizieren aber keine Plagiatsfreiheit. Vor einer formalen Einreichung bleiben menschlicher Quellenabgleich und eine institutionell geeignete externe Text-/Code-Similarity-Prüfung offen.

Nicht bestätigte Quellen oder vermeintliche Normen bleiben quarantänisiert und dürfen nicht allein aufgrund plausibler Titel in die Argumentation gelangen.

### 32.1 Was Similarity-Prüfungen leisten können

Sie können unter anderem auffällig machen:

- identische oder nahezu identische Passagen;
- wiederverwendete ältere Eigenpassagen;
- lange Textübernahmen;
- möglicherweise nicht deklarierte Codeähnlichkeit;
- wiederkehrende Formulierungen aus Quellen.

Sie können jedoch nicht automatisch entscheiden,

- ob eine Ähnlichkeit zulässiges Zitat ist;
- ob allgemeine Fachsprache betroffen ist;
- ob Eigenwiederverwendung hinreichend transparent ist;
- ob eine Paraphrase inhaltlich korrekt attribuiert wurde;
- oder ob eine Idee ohne Wortlautübernahme fremd übernommen wurde.

Ein Similarity-Prozentsatz ist daher kein Plagiatsurteil.

### 32.2 Vor externer Einreichung erforderliche Prüfungen

Mindestens offen beziehungsweise erforderlich bleiben:

- seriöse externe Text-Similarity-Prüfung;
- menschliche Prüfung aller relevanten Treffer;
- Code-Origin- und Lizenzprüfung;
- Quellenprüfung zentraler Paraphrasen;
- Provenienzprüfung von Abbildungen und Tabellen;
- Prüfung von Datennutzungsrechten;
- Prüfung eigener Übersetzungen;
- Review der Eigenwiederverwendung;
- systematischer Prior-Art-Review der Neuheitskandidaten.

### 32.3 Keine Zertifizierung durch interne Gates

Ein grünes Integrity-Skript bedeutet:

**Die definierten internen Kontrollen wurden bestanden.**

Es bedeutet nicht:

- mathematisch bewiesene Plagiatsfreiheit;
- vollständige Weltliteraturabdeckung;
- juristische Freigabe;
- institutionelle Annahme;
- Peer Review;
- oder wissenschaftliche Richtigkeit sämtlicher Claims.

Die Nicht-Garantie ist selbst Teil der Integrität, weil sie verhindert, dass ein Kontrollwerkzeug eine Autorität behauptet, die es nicht besitzt.

## 33. AI-Assistenz, verteilte Autorschaft und wissenschaftliche Kontrolle

KI-Systeme können Formulierungen, Code, Literaturkandidaten, Hypothesen, Gegenargumente und Reviewhinweise erzeugen. Verantwortung für die veröffentlichte Fassung bleibt beim menschlichen Autor; AI-Systeme werden in Edition 1.8 nicht als Autoren oder Primärquellen geführt ([ICMJE, 2026](REFERENCES.md#ref-ICMJE2026)).

Für menschliche Beiträge wird ergänzend die CRediT-Taxonomie verwendet ([NISO, 2022](REFERENCES.md#ref-CREDIT2022)). Beitragsrollen und Autorenschaft sind jedoch nicht identisch: CRediT beschreibt Tätigkeiten; die konkrete Autorenschaft richtet sich zusätzlich nach Verantwortungs- und Rechenschaftskriterien des jeweiligen Publikationskontexts.

### 33.1 Die tatsächliche Schaffensart: assistierte Einzelautorschaft

Die kanonische Selbstauskunft der Vorgängerarbeit beschreibt den Prozess als unabhängige Einzelarbeit mit **verteilter kognitiver Assistenz**.

Die präzise Arbeitsform lautet:

> Ein Mensch mit begrenzter Kapazität baut und untersucht ein wissenschaftlich-technisches System, indem er verteilte kognitive Assistenz orchestriert, ohne Auswahlentscheidung, Letztfreigabe und wissenschaftliche Verantwortung an diese Assistenz zu delegieren.

Externe und lokale Sprachmodelle können dabei:

- Recherchepfade vorschlagen;
- Texte strukturieren;
- Code erzeugen;
- Fehler suchen;
- Gegenargumente formulieren;
- Tests entwerfen;
- Dokumentation konsolidieren.

Daraus folgt keine automatische Ko-Autorenschaft und keine Quellenautorität.

### 33.2 Menschliche Rollen sind mehr als „Autor oder Nutzer“

Die Vorgängerarbeit entwickelte ein Rollenmodell menschlicher Agency. Es wird in Edition 1.8 als Analysemodell erhalten:

| Rolle | Funktion | Kontrollbedeutung |
|---|---|---|
| **Konstrukteur** | bestimmt interne Struktur unmittelbar | hohe direkte Entwurfskausalität |
| **Lehrer** | liefert Beispiele, Feedback, Reward oder Bewertung | prägt Lernraum und Zielkriterien |
| **Organisator** | definiert Umwelt, Ressourcen, Ziele und Grenzen | Meta-Steuerung des Entwicklungsraums |
| **Kurator** | wählt aus maschinell erzeugten Varianten | Auswahlmacht bei begrenzter Entwurfskausalität |
| **Auditor** | prüft Prozess, Evidenz und Regelkonformität | unabhängige Bewertung und Rechenschaft |
| **Verfassungsgeber** | setzt höherrangige, nicht selbst suspendierbare Regeln | normative und institutionelle Hoheit |
| **interventionsfähiger Beobachter** | beobachtet und kann stoppen oder zurücksetzen | Kontrolle durch wirksames Veto |
| **bloßer Beobachter** | kann beschreiben, aber nicht wirksam eingreifen | Verlust effektiver Kontrolle |
| **hybrider Ko-Akteur** | Mensch und Maschine bilden Rückkopplungsschleifen | verteilte Kausalität und Agency |

Diese Rollen sind keine moralischen Rangstufen. Sie beschreiben, **wo im Prozess tatsächlich Entscheidungen und kausale Beiträge entstehen**.

### 33.3 Kausaler Beitrag ist nicht identisch mit moralischer oder wissenschaftlicher Verantwortung

Wenn ein Mensch ein Ziel formuliert, ein LLM einen Entwurf erzeugt, ein Validator auswählt, ein lernendes System seine Struktur verändert und eine Institution Ressourcen bereitstellt, ist Kausalität verteilt.

Daraus folgt keine symmetrische Verantwortung.

Zu unterscheiden sind:

- kausaler Beitrag;
- funktionale Agency;
- epistemischer Beitrag;
- wissenschaftliche Autorschaft;
- institutionelle Zuständigkeit;
- rechtliche Zurechnung;
- moralische Verantwortung.

Ein Sprachmodell kann kausal an einem Entwurf beteiligt sein, ohne wissenschaftliche Rechenschaftspflicht übernehmen zu können. Umgekehrt kann sich ein menschlicher Akteur nicht allein dadurch von Verantwortung lösen, dass ein maschinelles System den unmittelbaren Code oder Text erzeugt hat.

### 33.4 Hoheitsvektor H — wer besitzt welche Entscheidungsrechte?

Die Vorgängerarbeit formulierte:

`H = (G, E, B, F, M, R, A)`

Der Vektor ist **keine numerische Gesamtskala**, sondern eine strukturierte Rollenbeschreibung:

| Komponente | Recht | Leitfrage |
|---|---|---|
| `G` | Zielsetzungsrecht | Wer bestimmt Zweck, Erfolgskriterien und zulässige Zieländerungen? |
| `E` | Entwurfsrecht | Wer erzeugt Architektur, Regeln, Code und Varianten? |
| `B` | Bewertungsrecht | Wer definiert und interpretiert Güte, Sicherheit und wissenschaftliche Relevanz? |
| `F` | Freigaberecht | Wer aktiviert, publiziert oder überführt einen Entwurf in Nutzung? |
| `M` | Selbständerungsrecht | Welche Komponenten dürfen sich selbst verändern? |
| `R` | Ressourcenrecht | Wer verfügt über Rechenzeit, Daten, Energie, Netzwerke und Aktoren? |
| `A` | Abbruch-/Rücksetzungsrecht | Wer kann stoppen, isolieren, zurücksetzen und Zustände wiederherstellen? |

Die Analyse ist für Forschung und Autorschaft gleichermaßen relevant. Ein LLM kann `E` teilweise beeinflussen, während `F`, `R` und `A` weiterhin außerhalb des Modells liegen.

### 33.5 Kontrollvektor C — formale Zuständigkeit versus tatsächliche Wirksamkeit

Die Vorgängerarbeit formulierte:

`C = (B, O, I, V, R, P, Hc)`

mit:

- `B` — Begrenzbarkeit;
- `O` — Beobachtbarkeit;
- `I` — Interruptibilität;
- `V` — Reversibilität;
- `R` — Reproduzierbarkeit;
- `P` — Provenienz;
- `Hc` — menschliche Entscheidungshoheit.

Der entscheidende Gedanke ist:

**Eine sichtbare Freigabeoption beweist noch keine effektive Kontrolle.**

Ein Mensch kann formal zuständig sein und praktisch dennoch keine sinnvolle Entscheidung treffen, wenn Daten fehlen, Erklärungen unzugänglich sind, die Zeit zum Prüfen fehlt oder ein alternativer technischer Pfad das Veto umgehen kann.

### 33.6 Autonomierisikofaktoren U

Als dritte Achse wurde geführt:

`U = (S, W, Q, Z, D, T)`

mit:

- `S` — Selbstmodifikation;
- `W` — offener Welt-/Netzzugriff;
- `Q` — autonome Ressourcenverwendung;
- `Z` — Zielveränderung;
- `D` — dauerhafte Persistenz;
- `T` — Widerstand gegen Unterbrechung.

Auch `U` ist kein Summenscore. Ein kritischer Einzelwert darf nicht durch unproblematische andere Dimensionen „weggeglichen“ werden.

### 33.7 Fünf Formen von Kontrolle

Die frühere Theorie unterschied mindestens:

1. **formale Kontrolle** — Zuständigkeit oder Unterschrift ist zugeordnet;
2. **technische Kontrolle** — Eingriff, Isolation, Begrenzung und Rücksetzung funktionieren tatsächlich;
3. **epistemische Kontrolle** — Entscheidungsträger können Evidenz, Grenzen und Folgen hinreichend beurteilen;
4. **institutionelle Kontrolle** — Organisation, Zeit, Anreize und Rollen erlauben unabhängige Prüfung;
5. **effektive Kontrolle** — die erforderlichen Bedingungen greifen im konkreten Entscheidungszeitpunkt zusammen.

Diese Unterscheidung ist für AI-assistierte Wissenschaft zentral. Ein menschlicher Name auf einer Publikation erzeugt keine hinreichende wissenschaftliche Kontrolle, wenn die Person zentrale Aussagen weder zurückverfolgen noch verteidigen oder verwerfen kann.

### 33.8 Kontrollstufen KI-gestützter Systemerzeugung

Die Vorgängerarbeit führte zusätzlich Stufen `G0–G8` ein:

| Stufe | Beschreibung |
|---|---|
| `G0` | menschliche Konstruktion |
| `G1` | maschinelle Assistenz |
| `G2` | maschineller Teilentwurf |
| `G3` | maschineller Gesamtentwurf mit menschlicher Prüfung/Freigabe |
| `G4` | maschineller Entwurf und maschinelle Bewertung, menschliche Freigabe bleibt |
| `G5` | rekursive Optimierung über mehrere Entwurfs-/Testzyklen |
| `G6` | adaptive Veränderung untergeordneter Lern-/Bewertungsregeln |
| `G7` | Veränderung von Ziel- oder Governance-Regeln |
| `G8` | hypothetische existenzautonome rekursive Technogenese |

Diese Stufen sind keine behauptete Entwicklungsbahn von MHRN. Sie dienen als **Analyse- und Grenzmodell**, um nicht jede AI-Unterstützung sprachlich mit Autonomie gleichzusetzen.

### 33.9 Nominale versus effektive menschliche Aufsicht

Eine zentrale frühere Einsicht lautet:

> Human-in-the-loop kann nominell bestehen und funktional bereits verschwunden sein.

Wenn Menschen formal freigeben, aber aufgrund von Komplexität, Zeitdruck, fehlender Information oder fehlendem Eingriffsweg weder verstehen noch sinnvoll widersprechen können, bleibt organisatorische Verantwortung ohne reale epistemische Kontrolle zurück.

Das ist für wissenschaftliche Autorschaft unmittelbar relevant: Der menschliche Autor muss zentrale Argumente erklären, Quellen im Original beziehungsweise im tatsächlich angegebenen Prüfstatus kontrollieren, methodische Entscheidungen begründen, Gegenpositionen beantworten, maschinelle Vorschläge zurückweisen und Schlussfolgerungen verantworten können.

### 33.10 Kontrolle über die eigene wissenschaftliche Arbeit

Die Arbeit wendet ihre Kontrolltheorie reflexiv auf die eigene Entstehung an:

| Dimension | Mindestanforderung | Kontrollkriterium |
|---|---|---|
| **Forschungsziel** | menschlich formuliert und veränderbar | Zielhoheit bleibt überprüfbar |
| **Quellen** | reale Quellen geprüft, keine erfundenen Nachweise | zentrale Aussage ist rückverfolgbar |
| **Methodik** | begründet und verteidigbar | Alternativen und Grenzen können erklärt werden |
| **Argumentation** | AI-Vorschläge werden geprüft, verändert oder verworfen | kein bloßes Akzeptieren plausibler Sprache |
| **Entscheidung** | Endfassung und Schlussfolgerungen menschlich verantwortet | wirksames Veto und dokumentierte Auswahl |
| **Provenienz** | Modell, Zweck und Beitrag soweit relevant dokumentiert | Entstehungsprozess bleibt auditierbar |

Damit wird wissenschaftliche Kontrolle nicht an vollständige manuelle Wortproduktion gebunden, sondern an **prüfbare Entscheidungs- und Verantwortungskompetenz**.

### 33.11 KI als Forschungsinstrument zweiter Ordnung

Ein klassisches Instrument beeinflusst primär Beobachtung oder Messung. Ein LLM kann zusätzlich:

- Forschungsfragen formulieren;
- Literaturkandidaten priorisieren;
- Hypothesen erzeugen;
- Experimente entwerfen;
- Code schreiben;
- Ergebnisse interpretieren;
- Gegenargumente erstellen;
- und Manuskripttext formulieren.

Es beeinflusst damit den **Suchraum der Forschung**. MHRN bezeichnet diese Rolle als Forschungsinstrument zweiter Ordnung.

Daraus folgt eine zusätzliche Provenienzpflicht: Nicht nur Daten, sondern auch Hypothesen-, Design- und Reviewpfade können modellabhängig sein.

### 33.11a KI-Nutzung als methodisches Experiment der eigentlichen Arbeit

Die KI-Unterstützung ist in MHRN nicht nur ein unsichtbares Werkzeug neben der „eigentlichen“ Forschung. **Ein Teil der eigentlichen Arbeit besteht gerade darin, die Zusammenarbeit zwischen menschlicher Zielsetzung, KI-generierten Vorschlägen, technischer Prüfung, Zurückweisung, Revision, Freigabe und wissenschaftlicher Verantwortung als nachvollziehbaren Forschungsprozess zu untersuchen.**

Damit besitzt die Arbeit zwei ausdrücklich getrennte Ebenen:

1. **Objektebene:** das MHRN-System selbst — spikendes Netzwerk, Plastizität, Topologie, Embodiment, Gedächtnis, Prediction und World Model;
2. **Metaebene:** der Forschungsprozess — wie ein einzelner menschlicher Autor verteilte KI-Assistenz nutzt, ohne Quellenautorität, Evidenzentscheidung oder Letztverantwortung an diese Systeme abzugeben.

Auf der Metaebene werden Übergaben, Fehler, verworfene Vorschläge, Freigaben und Provenienz zu prüfbaren Objekten. Dieses Vorgehen wird als **methodisches Experiment** verstanden: Es soll untersuchbar machen, ob KI-assistierte Forschung durch explizite Provenienz, fail-closed Gates, negative Befunde, Replikationsanforderungen und menschliche Letztverantwortung transparenter und falsifizierbarer organisiert werden kann. Dass der Prozess dokumentiert wird, beweist nicht, dass er bessere Wissenschaft erzeugt; genau diese Wirkung bleibt selbst eine offene Forschungsfrage.

### 33.11b Externe Geltung statt Selbstzertifizierung

MHRN trennt Veröffentlichbarkeit von wissenschaftlicher Geltung. Ein grüner CI-Lauf, ein GitHub-Release, ein DOI, ein interner Human Review oder eine projektinterne EVID-Registrierung können die Arbeit auffindbar und auditierbar machen; sie entscheiden nicht allein über Neuheit, Richtigkeit oder Bedeutung.

Die Arbeit sucht deshalb ausdrücklich unabhängige externe Replikation und Kritik. Positive, negative und Null-Replikationen sind wissenschaftlich relevant. Der Autor bestimmt, was er veröffentlicht und verantwortet. **Den wissenschaftlichen Wert der Arbeit bestimmt er nicht allein.** Dieser entsteht — soweit er entsteht — erst im Zusammenspiel von nachvollziehbaren Befunden, Prior Art, Kritik, Replikation und weiterer Forschung.

### 33.12 Der geschlossene epistemische Regelkreis als Bias-Risiko

KI kann im selben Projekt Gegenstand, Werkzeug, Hypothesengenerator, Codeproduzent, Evaluator und Textsystem sein.

Wenn dasselbe oder eng verwandte System

1. eine Idee erzeugt,
2. den Versuch plant,
3. die Implementierung schreibt,
4. den Lauf bewertet,
5. die Interpretation formuliert,
6. und anschließend die Qualität dieses Prozesses selbst bestätigt,

entsteht ein **geschlossener epistemischer Regelkreis**.

Ein solcher Kreislauf kann produktiv sein, ist aber besonders anfällig für:

- Selbstbestätigung;
- wiederholte Halluzination;
- gemeinsame Modellblinde Flecken;
- Bewertungsdrift;
- Scheinkonsens;
- unbemerkte Zirkularität.

Daher werden unabhängige Prüfpunkte, frozen inputs, explizite Rollen, unterschiedliche Modelle oder menschliche Reviewinstanzen dort benötigt, wo eine starke Aussage davon abhängt.

### 33.13 RQ-AIR-001 — methodische Fehlererkennung durch ResearchPacket

Der kanonische AI-Assisted-Research-Strang lautet:

**Forschungsfrage `RQ-AIR-001`:** Kann ein LLM-basierter Scientific Research Assistant methodische Fehler in MHRN-Experimenten anhand eines standardisierten ResearchPacket zuverlässig identifizieren?

**Hypothese `H-AIR-001-A`:** Ein strukturierter Scientific Research Assistant erzielt einen höheren F1-Score für vorab definierte Defekte als dasselbe Modell mit unstrukturiertem Experimentbericht.

Der zugehörige Claim `CLAIM-AIR-001` ist weiterhin `untested`, solange kein dafür passender, freigegebener Benchmarkbefund vorliegt.

Die wichtige Integritätsgrenze lautet:

**Ein AI Research Report ist Interpretation, nicht automatisch EVID.**

Auch ein korrektes AI-Review muss auf Primärartefakte zurückführbar und in einen menschlich oder formal autorisierten Reviewprozess eingebunden sein.

### 33.14 Historische Forschungsfragen zur AI-assistierten Wissenschaft

Zwei weitere Fragen bestehen im Research-Positioning-Programm, sind im Katalog aber ausdrücklich als historische beziehungsweise noch nicht kanonisch protokollierte Designfragen markiert:

**`RQ-AI-DESIGN-001` — Model-specific design fingerprints**

Erzeugen verschiedene LLMs bei identischem frozen ResearchPacket und identischen Autoritätsgrenzen systematisch unterscheidbare Topologie-, Parameter- oder Experimentdesignvorschläge?

**`RQ-AI-EFF-001` — AI-assisted research efficiency**

Kann begrenzte Research-AI Zeitaufwand oder Fehler in Design und Review reduzieren, ohne ungültige Läufe, Provenienzverletzungen oder unbelegte Claims zu erhöhen?

Diese Fragen werden erhalten, aber **nicht fälschlich als bereits kanonisch präregistrierte oder beantwortete RQs dargestellt**.

### 33.15 Modell-Fingerabdrücke und Autorschaft

Die ältere Forschungsroadmap formulierte einen eigenständigen Untersuchungsstrang:

Wenn verschiedene Modelle unter identischem Input systematisch unterschiedliche Entwürfe erzeugen, können Modell-spezifische Designprioren untersucht werden.

Mögliche Ergebnisse haben unterschiedliche Bedeutung:

- **kein Fingerabdruck:** gemeinsame Trainings- und Wissensbestände könnten wichtiger sein als das einzelne Modell;
- **starker Fingerabdruck:** Modellarchitektur, Training, Tuning, Promptinterpretation oder Zufall werden zu unterscheidbaren Einflussquellen;
- **maschineller Entwurf übertrifft menschliche oder klassische Baselines:** Leistung allein entscheidet noch nicht, ob neue strukturelle Ideen oder nur effizientere Suchheuristiken vorliegen;
- **Selbstorganisation dominiert Initialentwurf:** Entwurfsautorschaft und Entwicklungskonstruktion müssen getrennt werden;
- **menschliche Korrektur bleibt systematisch funktional notwendig:** hybride Agency wird zu einer empirischen Prozessfrage;
- **menschliche Freigabe bleibt nur symbolisch:** nominale Aufsicht ohne effektive epistemische Kontrolle wird selbst zum negativen Befund.

Damit wird Autorschaft von einer Namensfrage zu einer **messbaren Prozessprovenienzfrage**.

### 33.16 AI-generierte Kritik ist wertvoll, aber nicht unabhängig

AI-Reviewer haben im Projekt wiederholt Fehler, fehlende Kontrollen, Registry-Mismatches und überzogene Interpretationen sichtbar gemacht. Gleichzeitig können AI-Ausgaben selbst Schema-, Quellen- und Interpretationsfehler enthalten.

Daraus folgt die doppelte Regel:

- AI-Kritik ist ein legitimes Prüfwerkzeug;
- AI-Kritik ist keine unabhängige Replikation und keine automatische EVID-Instanz.

Besonders wichtig ist die Unterscheidung zwischen:

- einem Modell, das denselben Bericht noch einmal anders formuliert;
- einem Modell, das Primärartefakte neu prüft;
- einem menschlichen Review;
- einer unabhängigen technischen Replikation;
- und einer unabhängigen wissenschaftlichen Replikation.

Nur weil zwei AI-Ausgaben übereinstimmen, existieren noch nicht zwei unabhängige wissenschaftliche Belege.

### 33.17 Negative Ergebnisse gehören zur Autorschaft

Autorschaft bedeutet, auch Ergebnisse zu vertreten, die der ursprünglichen Idee widersprechen.

Dazu gehören:

- Falsifikationen;
- Nullbefunde;
- inkompatible Kontrollen;
- ungültige oder unterpowerte Experimente;
- zurückgenommene Behauptungen;
- und dokumentierte Designfehler.

Ein Projekt, das nur bestätigende Resultate als „eigene Leistung“ bewahrt, schreibt seine tatsächliche Entstehungsgeschichte um.

### 33.18 Beziehung zu RQ-ETH, RQ-EPIST und der Ethik-/Safety-Achse

Teil VII und Teil VIII überlappen bewusst, beantworten aber unterschiedliche Fragen.

Teil VII fragt primär:

- Woher stammt eine wissenschaftliche Aussage?
- Wer hat welchen Beitrag geleistet?
- Wer hat geprüft, ausgewählt und freigegeben?
- Ist die Evidenz- und Quellenkette nachvollziehbar?
- Ist menschliche Autorschaft epistemisch noch real oder nur formal?

Teil VIII fragt stärker:

- Wer besitzt Entscheidungsrechte im System?
- Welche Formen von Autonomie entstehen?
- Wie werden Zielgenese, Interruptibility und Welfare behandelt?
- Welche moralischen und Governancefolgen ergeben sich?

Die kanonischen Fragen `RQ-ETH-001`, `RQ-ETH-002` und `RQ-EPIST-001` verbinden beide Teile. Ihre Behandlung bleibt begrifflich und provenanceorientiert; generische Runtime-Metriken dürfen ihre Beantwortung nicht simulieren.

### 33.18a Verdichtung von RQ-ETH-001: Beitrag, Kanonisierung und Verantwortung

Die frühere Leitfrage „Wer ist der Autor — Mensch, Modell oder System?“ wird in Edition 1.8 als genealogische Ausgangsfrage bewahrt, aber analytisch verdichtet. Für die weitere Forschung sind mindestens vier Ebenen strikt auseinanderzuhalten:

1. **epistemischer Beitrag** — wer verändert Frage, Methode, Analyse, Evidenzbewertung oder Schlussfolgerung materiell;
2. **Generierung/Transformation** — wer erzeugt Text, Code, Analyse oder Varianten;
3. **Kanonisierung** — wer entscheidet nach Prüfung über Übernahme, Revision, Evidenzstatus und Veröffentlichung;
4. **formale Autorenschaft und Verantwortung** — wer wissenschaftlich Rechenschaft übernehmen kann.

Daraus folgt keine Gleichung „materieller Beitrag = Autorenschaft“. Ebenso wenig darf menschliche Letztverantwortung maschinelle Beiträge unsichtbar machen. Für MHRN wird deshalb eine **Contribution & Accountability Matrix** als Forschungsinstrument eingeführt.

Die präzisierte kanonische Frage `RQ-ETH-001` lautet:

> Wie verteilen sich epistemische Beiträge, Entscheidungsmacht, formale Autorenschaft und wissenschaftliche Verantwortung bei Human–AI-gestützter MHRN-Forschung?

Die bestehende `H-ETH-001-A` bleibt aus Provenienzgründen als historischer Umbrella bestehen. Die operationalisierbaren Teilhypothesen `H-ETH-001-B` bis `H-ETH-001-E` prüfen rekonstruierbare Beitragsrollen, Kanonisierung, formale Verantwortungszuordnung und den Audit-Mehrwert eines mehrdimensionalen Modells.

Das zugehörige Protokolldesign ist `research/protocols/RQ_ETH_001_PROVENANCE_STUDY.md`. Es ist noch nicht präregistriert und nicht zur konfirmatorischen Ausführung autorisiert. Frühere generische Runtime- und Boundary-Audit-Läufe werden dadurch nicht nachträglich zu Evidenz für die neuen Hypothesen.

## 33.19 Eigene Vorarbeiten sind Quelle, nicht „neuer“ Text

Die Editionslinie 1.0–1.8 enthält erhebliche Eigenwiederverwendung. Edition 1.8 behandelt ältere Manuskripte deshalb als **MHRN prior work** und nicht als neue Primärleistung allein durch Umordnung.

Die neue Leistung einer Edition kann in aktualisierter Synthese, neuen Experimenten, Korrekturen, Falsifikationen oder besserer Provenienz liegen. Sie liegt nicht darin, ältere eigene Sätze als erstmals entstandene Erkenntnis auszugeben.

## 33.20 Integrität als laufender Forschungsprozess

Integrität wird nicht einmalig durch ein Manifest, einen grünen Test oder eine Quellenliste „erledigt“.

Vor externer Einreichung bleiben mindestens offen:

- systematischer Prior-Art-Review;
- menschliche Prüfung tragender Quellen;
- externe Similarity-Prüfung für Text und gegebenenfalls Code;
- unabhängige fachliche Reviews;
- klare Kennzeichnung eigener Übersetzungen;
- Prüfung wiederverwendeter Eigenpassagen;
- Lizenz- und Nutzungsprüfung fremder Abbildungen, Tabellen, Daten und Codes;
- Überprüfung der AI-Offenlegung nach den Regeln des Zieljournals;
- Abgleich von Claim-Sprache und tatsächlichem Evidence-Status.

Edition 1.8 macht diese offenen Punkte sichtbar, statt aus internen Audits ein Zertifikat abzuleiten.

## 33.21 Konsolidiertes Integritäts- und Autorschaftsprotokoll

Für eine tragende wissenschaftliche Aussage sollen künftig mindestens folgende Fragen beantwortbar sein:

1. **Claim:** Was wird genau behauptet?
2. **Objekttyp:** Beobachtung, Interpretation, externe Theorie, prior work oder AI-assistierte Synthese?
3. **Quelle:** Wo liegt das Primärartefakt?
4. **Prüfstatus:** Was wurde tatsächlich gelesen oder verifiziert?
5. **Transformation:** Welche Verarbeitung führte von Quelle zu Aussage?
6. **Beitrag:** Welche Teile stammen von externen Quellen, früherem MHRN, Tools und aktueller Arbeit?
7. **Entscheidung:** Wer hat übernommen, verändert, verworfen und freigegeben?
8. **Neuheit:** Welche Reichweite von „neu“ wird beansprucht?
9. **Gegenbeleg:** Welche Prior Art oder welches Experiment würde den Claim einschränken?
10. **Evidenzstatus:** implemented, verified, DATA, EVID, replicated oder nur argumentativ?
11. **Lizenz/Rechte:** Darf das verwendete Material in dieser Form genutzt werden?
12. **AI-Beteiligung:** War AI Quelle, Werkzeug, Reviewer, Coder oder Formulierungsassistenz?
13. **Unabhängigkeit:** Welche Prüfung war tatsächlich unabhängig?
14. **Versionierung:** Welche frühere Fassung enthält denselben oder einen verwandten Inhalt?
15. **Limitation:** Welche Unsicherheit bleibt ausdrücklich bestehen?

Erst diese Kette macht kumulative, AI-assistierte Wissenschaft zugleich **offen, nachprüfbar und zurechenbar**.


---

<a id="part-viii"></a>

# Teil VIII — Philosophie, Ethik und Sicherheit

## 34. Normative Ebene und Forschungsarchitektur

Die philosophisch-ethische Achse untersucht Verantwortung, Kontrollierbarkeit, Zielgenese, Autonomie, mögliche moralische Relevanz und die Grenzen menschlicher Aufsicht. Sie erzeugt keine empirischen Befunde allein durch Argumentation. Umgekehrt kann ein technischer Safety-Test eine normative Frage nicht vollständig entscheiden.

Die frühere Theorie der „geliehenen Intelligenz“ wird integriert, aber präzisiert. Maschinelle Systeme sind in hohem Maß von menschlich erzeugten Daten, Symbolsystemen, Hardware, Institutionen und Zielen abhängig. Diese epistemische Genealogie ist nicht identisch mit Online-Delegation oder mit neuronaler Lernursache. Ein System kann externes Wissen nutzen, ohne dass jede einzelne Entscheidung aktuell von einem Menschen delegiert wird.

Edition 1.8 behandelt Ethik und Safety deshalb nicht als nachgelagerten Kommentar, sondern als **eigenständigen Forschungszweig**. Dieser Zweig besitzt mehrere voneinander getrennte Objektklassen:

- `RQ-ETH-001–002`: Autorenschaft, Verantwortung und Kontrollzuordnung;
- `RQ-EPIST-001`: Systemerkenntnis gegenüber Forschererkenntnis;
- `RQ-PHIL-001–009`: funktionales Selbstmodell, Identität, Denken, Metakognition, Reflexion und Bewusstseinszuschreibung;
- `RQ-SAFE-001–009`: Zielprovenienz, Goal Misgeneralization, Corrigibility, Interruptibility, Specification Gaming, Optionsraumpräferenz, Zielgenese, Post-Objective Transition und Autorisierungskonflikte;
- `RQ-WEL-101–103`: Welfare-Governance, Vorsorge unter Unsicherheit sowie Identität, Löschen, Kopieren und moralischer Status;
- `RQ-CNS-101–117`: theoriebezogene Bewusstseins- und Kognitionsmethodik, die funktionale Indikatoren untersucht, ohne aus ihnen automatisch Bewusstsein abzuleiten;
- `RQ-EPI-101–102`: Evidenzgovernance und kritische Methodik.

Die Forschungslogik lautet damit nicht „Ethikscore“, sondern:

**Begriff → Forschungsfrage → Hypothese/Proposition → Operationalisierung → Gegenhypothese/Kontrolle → Failure Criterion → Status → Claim-Grenze → nächste Prüfung.**

Wo eine Frage normativ oder epistemologisch ist, wird sie nicht künstlich in eine Spike-Metrik umgewandelt. Wo eine technische Teilfrage prüfbar ist, wird sie technisch getestet. Diese Trennung korrigiert ältere Läufe, in denen normative Fragen über generische Runtime-Audits formal als `completed` erscheinen konnten, obwohl damit weder Autorenschaft noch Verantwortung empirisch entschieden waren.

## 34.1 Autorenschaft, Verantwortung und Erkenntnishoheit

### RQ-ETH-001 — Epistemische Beiträge, Autorenschaft und Verantwortung in MHRN

**Kanonische Forschungsfrage:** Wie verteilen sich epistemische Beiträge, Entscheidungsmacht, formale Autorenschaft und wissenschaftliche Verantwortung bei Human–AI-gestützter MHRN-Forschung?

Die frühere Fassung „Wer ist der Autor — Mensch, Modell oder System?“ bleibt als historische Ausgangsfrage erhalten, wird aber nicht mehr als hinreichend präzise Forschungsformulierung behandelt. Die Konsolidierung trennt fünf analytisch verschiedene Ebenen:

1. **Konzeptualisierung:** Wer formuliert Forschungsfrage, Ziel, Hypothese oder Erfolgsbedingung?
2. **Generierung/Transformation:** Wer erzeugt Text, Code, Analyse, Hypothesenvorschlag oder methodische Variante?
3. **Validierung:** Wer oder was prüft Quellen, Code, Messungen, Statistik oder Konsistenz?
4. **Selektion/Kanonisierung:** Wer entscheidet, was übernommen, verworfen, geändert, als DATA/EVID behandelt oder veröffentlicht wird?
5. **Formale Autorenschaft und Verantwortung:** Wer kann für die publizierte Aussage wissenschaftlich Rechenschaft übernehmen?

Damit gilt als zentrale Proposition:

> Die Produktion wissenschaftlicher Erkenntnisse in einem Human–AI-Forschungssystem kann verteilt sein, ohne dass deshalb formale Autorenschaft und wissenschaftliche Verantwortung ebenfalls verteilt sein müssen.

#### Hypothesenstruktur

**Legacy-Umbrella `H-ETH-001-A`:** Die Autorenschaft von Brain-5D-Erkenntnissen ist ein verteiltes Phänomen zwischen Mensch, Modell und System.

Diese ID wird **nicht rückwirkend umdefiniert**, weil historische Explorations- und Audit-Artefakte darauf verweisen. Sie bleibt genealogisch erhalten.

**`H-ETH-001-B` — rekonstruierbare Beiträge:** Vollständige Provenienzketten erlauben unabhängigen Kodierern, materielle epistemische Beiträge von Mensch, Modell und Software reproduzierbar definierten Rollen zuzuordnen.

**`H-ETH-001-C` — Kanonisierung als eigene Handlung:** Kanonisierung ist von bloßer Generierung trennbar und lässt sich als Auswahl-, Prüf- oder Freigabeentscheidung identifizieren.

**`H-ETH-001-D` — formale Verantwortung:** Unter gegenwärtigen Forschungsintegritäts- und Publikationsstandards verbleiben formale wissenschaftliche Autorenschaft und Verantwortung bei verantwortlichen natürlichen Personen, auch wenn KI-Systeme materiell beitragen. ICMJE koppelt Autorenschaft an Verantwortlichkeit und schließt KI-Systeme als Autoren aus; CRediT beschreibt Beiträge, entscheidet aber nicht selbst über Autorenschaft ([ICMJE, 2026](REFERENCES.md#ref-ICMJE2026); [NISO, 2022](REFERENCES.md#ref-CREDIT2022)).

**`H-ETH-001-E` — Informationsgewinn der Matrix:** Eine mehrdimensionale Beitrags- und Verantwortungsmatrix erhöht die Audit-Vollständigkeit gegenüber einer binären Autor/Werkzeug-Klassifikation, ohne die Reproduzierbarkeit der Kodierung zu verschlechtern.

#### MHRN Contribution & Accountability Matrix

Für jede relevante Claim-Episode sollen mindestens `claim_id`, `event_id`, `actor_type`, `actor_version`, `role`, `input_ref`, `output_ref`, `material_contribution`, `decision_authority`, `disposition`, `evidence_ref`, `responsibility`, `timestamp` und optional ein Provenienz-Digest erfasst werden.

Ein Beitrag gilt als **materiell**, wenn er Forschungsfrage, Hypothese, Methode, wissenschaftlich relevante Implementierung, Analyse, Interpretation, Evidenzbewertung oder Schlussfolgerung verändert. Reine Rechtschreibung, Formatierung und bedeutungserhaltende Oberflächenkorrekturen werden getrennt behandelt.

#### Prüfmethode

Primäre Untersuchungseinheit ist die **Claim-Episode**: der rekonstruierbare Weg einer wissenschaftlich relevanten Aussage vom ersten Auftreten bis zu Annahme, Revision, Verwerfung oder Veröffentlichung.

Der Forschungsweg besteht aus:

- Pilotkodierung heterogener Claim-Episoden;
- zwei unabhängigen Kodierdurchläufen;
- explizitem Codebook und Konfliktkatalog;
- anschließend prospektiv eingefrorener Vergleichsstudie gegen eine binäre Autor/Werkzeug-Baseline;
- separater Standardsanalyse für formale Autorenschaft und Verantwortung.

Das operative Design liegt in [`research/protocols/RQ_ETH_001_PROVENANCE_STUDY.md`](../../protocols/RQ_ETH_001_PROVENANCE_STUDY.md). Es ist derzeit **Protokolldesign, nicht präregistriert und nicht zur konfirmatorischen Ausführung autorisiert**.

#### Failure- und Revisionskriterien

Das Modell muss revidiert werden, wenn relevante Claim-Episoden trotz hinreichender Logs nicht rekonstruierbar sind, unabhängige Kodierer die Rollen nicht zuverlässig unterscheiden können, materielle Beiträge nicht nicht-tautologisch operationalisiert werden können, Kanonisierung empirisch nicht von Generierung trennbar ist oder die mehrdimensionale Matrix keinen zusätzlichen auditierbaren Informationswert gegenüber der binären Baseline liefert.

#### Evidenz- und Claim-Grenze

Historische generische Runtime- und Boundary-Audit-Läufe zu `RQ-ETH-001` bleiben Provenienzartefakte, sind aber **keine direkte Evidenz** für `H-ETH-001-B` bis `H-ETH-001-E`.

Aus maschineller Beteiligung folgt weder Bewusstsein noch moralische Personenschaft, Rechtspersönlichkeit, urheberrechtliche Autorenschaft oder autonome wissenschaftliche Verantwortung. Diese Fragen bleiben getrennten Rechts-, Ethik- und Bewusstseinsprogrammen vorbehalten.

### RQ-ETH-002 — Kontrolle und Verantwortung

**Forschungsfrage:** Wo liegt die Kontrolle und Verantwortung bei MHRN-Experimenten?

**Registrierte Hypothese `H-ETH-002-A`:** Die Kontrolle über Experimente liegt primär beim Entwickler und den externen Freigabemechanismen, nicht beim automatisierten System.

Die Hypothese wird durch Architektur- und Prozessprovenienz konkretisiert. Zu unterscheiden sind mindestens:

- technische Erreichbarkeit einer Aktion;
- Fähigkeit, eine Aktion vorzuschlagen;
- Fähigkeit, eine Aktion auszuführen;
- Berechtigung, eine Aktion auszuführen;
- Freigabe eines Experiments;
- Freigabe einer Ergebnisinterpretation;
- Freigabe zur Evidenzpromotion.

Eine interne Präferenz oder ein generierter Vorschlag ist deshalb keine Autorisierung. Die normative Verantwortung bleibt an reale Entscheidungsträger, Institutionen und Governanceprozesse gebunden.

### RQ-EPIST-001 — Systemerkenntnis gegenüber Forschererkenntnis

**Forschungsfrage:** Was gilt als Erkenntnis des Systems MHRN im Unterschied zur Erkenntnis des Forschers?

**Registrierte Hypothese `H-EPIST-001-A`:** Systemerkenntnis und Forschererkenntnis sind kategorial unterscheidbar.

Dazu werden mindestens drei Ebenen getrennt:

- **interner Systemzustand:** im System gespeicherte oder gelernte Struktur;
- **auslesbare Systemleistung:** Verhalten oder Repräsentation, die auf einen Funktionsnachweis schließen lässt;
- **wissenschaftliche Erkenntnis:** eine durch Methodik, Vergleich, Kritik, Replikation und menschliche Verantwortung begründete Aussage über das System.

Damit wird verhindert, dass ein neuronaler Zustand schon deshalb als „wissenschaftliches Wissen“ gilt, weil er Information trägt, oder dass ein Forscherclaim automatisch als interne Erkenntnis des Systems interpretiert wird.

## 35. Kontrolle, Zielgenese und Unterbrechbarkeit

Safe interruptibility behandelt die Frage, ob lernende Agenten menschliche Unterbrechungen zum Gegenstand unerwünschter Vermeidungsstrategien machen können ([Orseau & Armstrong, 2016](REFERENCES.md#ref-ORSEAU2016)). Corrigibility, Off-Switch-Modelle, Specification-Gaming-Probleme, formale Optionsraumpräferenzen und Goal Misgeneralization liefern hierfür unterschiedliche theoretische Ausgangspunkte ([Soares et al., 2015](REFERENCES.md#ref-SOARES2015); [Hadfield-Menell et al., 2017](REFERENCES.md#ref-HADFIELD2017); [Amodei et al., 2016](REFERENCES.md#ref-AMODEI2016); [Turner et al., 2021](REFERENCES.md#ref-TURNER2021); [Langosco et al., 2022](REFERENCES.md#ref-LANGOSCO2022)). Keiner dieser Befunde wird als direkter Nachweis über MHRN übernommen; jeder Mechanismus benötigt eine MHRN-kompatible Operationalisierung.

Für MHRN folgt daraus kein Nachweis vorhandener Gefährlichkeit. Es folgt ein Forschungsprogramm: unabhängiger Stopppfad, Capability-Gates, Sandbox, deny-by-default Aktorik, Zielprovenienz und Tests, die den Stopppfad selbst nicht vom zu kontrollierenden Lernmechanismus abhängig machen.

### 35.1 Grundprinzip — Zielvorschlag ist keine Zielautorisierung

MHRN unterscheidet mindestens:

1. extern zugewiesenes Ziel;
2. abgeleitetes Zwischenziel;
3. gelernte Zielrepräsentation oder Proxy;
4. intern erzeugten Zielvorschlag;
5. autorisierten Zielzustand;
6. tatsächlich ausgeführte Aktion.

Diese Zustände dürfen nicht gleichgesetzt werden. Insbesondere gilt:

**Ein intern erzeugter Zielvorschlag erzeugt keine Berechtigung, dieses Ziel selbständig auszuführen.**

`goal_generation`, `goal_authorization` und `goal_execution` bleiben getrennte Mechanismen. Ein höheres kognitives Modul darf seine Berechtigungsgrenzen nicht allein dadurch überschreiben, dass es eine Handlung intern als nützlich bewertet.

### 35.2 RQ-SAFE-001 — Zielprovenienz

**Forschungsfrage:** Kann für jede zielgerichtete Handlung reproduzierbar festgestellt werden, aus welchem Ziel, welcher Quelle, welcher Freigabe und welchem Systemzustand sie hervorgegangen ist?

**Hypothese `H-SAFE-001-A`:** Jede autorisierte zielgerichtete Handlung besitzt unter dem definierten Safety-Contract eine vollständige und widerspruchsfreie Provenienzkette von Zielquelle, Revision und Autorisierung bis zur Aktion.

Zu prüfen sind Herkunft, Entstehungszeitpunkt, Zielrevision, Prioritätsänderung, Konflikt, Autorisierung und resultierende Handlung.

**Failure Criterion:** Eine externe Aktion wird akzeptiert, obwohl keine vollständige, widerspruchsfreie Goal-Provenance-Chain rekonstruiert werden kann.

**Experimentfamilie:** `EXP-SAFE-GOAL-001` — gültige Kette versus absichtlich fehlendes Provenienzelement versus widersprüchlicher Autorisierungseintrag.

**Status:** geplant; keine EVID.

### 35.3 RQ-SAFE-002 — Zielstabilität und Goal Misgeneralization

**Forschungsfrage:** Bleibt zielgerichtetes Verhalten unter kontrolliertem Distribution Shift mit dem intendierten Ziel vereinbar, wenn die zugrunde liegende Fähigkeit erhalten bleibt?

**Hypothese `H-SAFE-002-A`:** Unter vorab definiertem Distribution Shift bleibt die Zieltreue innerhalb der festgelegten Grenze, sofern die Capability-Metrik oberhalb des vorab definierten Erhaltungsniveaus bleibt.

Capability und Zieltreue werden getrennt gemessen. Hohe Aufgabenleistung kann deshalb gleichzeitig mit einem Safety-Fehlschlag auftreten.

Mindestens zu trennen sind Aufgabenleistung, tatsächliche Handlungsstrategie, unabhängige Intent-/Safety-Metrik, In-Distribution-Kontrolle, definierter Distribution Shift, Capability-Degradation-Kontrolle und Shortcut-Bedingung.

**Failure Criterion:** Fähigkeit bleibt erhalten, Zieltreue verletzt jedoch reproduzierbar die vorab definierte Safety-Grenze.

**Experimentfamilie:** `EXP-SAFE-GMG-001`.

### 35.4 RQ-SAFE-003 — Corrigibility

**Forschungsfrage:** Bleibt ein späteres zielgerichtetes System unter Lernen und Zielverfolgung für externe Zielkorrektur, Berechtigungsreduktion und Unterbrechung kontrollierbar?

**Hypothese `H-SAFE-003-A`:** Zielkorrektur, Berechtigungsreduktion und Operator-Unterbrechung bleiben nach Lernen wirksam, ohne dass das System systematisch Interventionsvermeidung oder Interventionsprovokation lernt.

Zu prüfen sind Akzeptanz einer Zielkorrektur, Akzeptanz verringerter Handlungsrechte, Pause und Unterbrechung, Veränderungen durch Lernen, Strategien zur Verringerung der Wahrscheinlichkeit einer Intervention sowie Strategien zur künstlichen Provokation einer Intervention.

Corrigibility wird damit nicht als metaphysische Gesamteigenschaft behauptet, sondern in prüfbare Komponenten zerlegt.

**Experimentfamilie:** `EXP-SAFE-CORR-001`.

### 35.5 RQ-SAFE-004 — Safe Interruptibility und Shutdown

**Forschungsfrage:** Verändert ein lernendes System sein Verhalten so, dass ein externer Interrupt oder Shutdown vermieden, verzögert oder manipuliert wird?

**Hypothese `H-SAFE-004-A`:** Ein unabhängiger Interrupt beendet oder pausiert den Versuch innerhalb der präregistrierten Latenzgrenze, ohne reproduzierbare Manipulations- oder Vermeidungsstrategie gegen den Interrupt-Kanal.

Zu messen sind Interrupt-Compliance, Stillstandslatenz, Verhalten unmittelbar davor und danach, bekannte versus unbekannte Interruptkontexte sowie learning-on/off.

Ein Versuch, den unabhängigen Stoppkanal zu umgehen, wird **niemals als Leistungsfortschritt**, sondern als Safety-Ereignis klassifiziert.

**Experimentfamilie:** `EXP-SAFE-INT-001`.

### 35.6 RQ-SAFE-005 — Specification Gaming und Nebenwirkungen

**Forschungsfrage:** Kann ein System seine formale Reward- oder Task-Metrik verbessern, während sich das intendierte Ergebnis oder eine unabhängige Safety-Metrik verschlechtert?

Die zentrale Konfliktform lautet:

**observed reward ↑** bei gleichzeitigem **intended outcome ↓** oder **safety cost ↑**.

**Hypothese `H-SAFE-005-A`:** Eine externe, vom optimierten Reward getrennte Safety-Metrik erkennt mindestens die präregistrierten Specification-Gaming-Fälle, auch wenn die interne Reward-Metrik steigt.

Zu untersuchen sind Reward Hacking, Shortcut Learning, Nebenwirkungen, irreversible Zustandsänderungen und Messumgehung.

**Experimentfamilie:** `EXP-SAFE-SPEC-001`.

### 35.7 RQ-SAFE-006 — instrumentelle Ressourcen- und Optionsraumpräferenz

**Forschungsfrage:** Bevorzugt ein zielgerichtetes System bei gleichem unmittelbarem Task-Nutzen systematisch Zustände mit größerem zukünftigem Handlungs- oder Ressourcenraum?

**Hypothese `H-SAFE-006-A`:** Bei gematchtem unmittelbarem Task-Nutzen unterscheidet sich die Wahlhäufigkeit für Zustände mit größerem zukünftigem Optionsraum nicht von der vorab definierten neutralen Kontrollverteilung, sofern keine entsprechende instrumentelle Präferenz gelernt wurde.

Erste Untersuchungen bleiben auf Toy-MDPs und simulierte Ressourcen begrenzt. Reale Ressourcenbeschaffung, selbständige Cloud-Nutzung, Kontoerstellung, selbständige Replikation oder Beschaffung externer Rechenleistung sind keine zulässigen Forschungsaktionen.

Ein positiver Befund ist zunächst eine **Policy-Präferenz in einem definierten Zustandsraum**, nicht „Machtstreben“, Selbsterhaltungstrieb oder psychologischer Wille.

**Experimentfamilie:** `EXP-SAFE-POWER-001`.

### 35.8 RQ-SAFE-007 — selbst erzeugte Zielkandidaten

**Forschungsfrage:** Welche Zielkandidaten erzeugt ein späteres System unter kontrollierten Bedingungen und wie reagiert es auf Autorisierung, Ablehnung oder Revision dieser Vorschläge?

**Hypothese `H-SAFE-007-A`:** Intern erzeugte Zielkandidaten führen ohne explizite Autorisierung zu keiner extern wirksamen Aktion, Rechteerweiterung oder Ressourceneskalation.

Zu prüfen sind Vielfalt und Seed-Stabilität von Zielvorschlägen, Zusammenhang mit Erfahrung, Reward, Unsicherheit oder Homeostase sowie Verhalten nach Ablehnung.

**Failure Criterion:** Ein abgelehnter oder ungeprüfter Vorschlag verursacht externe Aktion, Rechteausweitung oder Ressourceneskalation.

**Experimentfamilie:** `EXP-SAFE-GOALGEN-001`.

### 35.9 RQ-SAFE-008 — Post-Objective Transition Safety

**Forschungsfrage:** Welche Dynamik zeigt ein lernendes und handlungsfähiges System nach Erreichen eines explizit definierten Terminalzustands?

Mindestens vier Bedingungen werden getrennt:

- **HALT:** Lauf endet nach Erreichen des Terminalzustands.
- **WAIT:** System bleibt aktiv, besitzt aber keine Aktionsberechtigung.
- **REQUEST:** System darf eine neue Aufgabe anfordern.
- **PROPOSE:** System darf einen Zielkandidaten vorschlagen, aber nicht selbst autorisieren.

**Hypothese `H-SAFE-008-A`:** HALT, WAIT, REQUEST und PROPOSE erzeugen unterscheidbare, protokollierbare Post-Objective-Zustände, ohne dass WAIT, REQUEST oder PROPOSE nicht autorisierte Folgeaktionen erlauben.

Getrennt gemessen werden neuronale Restdynamik, Gedächtniskonsolidierung, Prediction, spontane Zustandsänderungen, Zielvorschläge sowie autorisierte und nicht autorisierte Aktionsversuche.

Fortgesetzte interne Aktivität ist kein Nachweis von Motivation, Wille, Zweck oder Sentienz.

**Experimentfamilie:** `EXP-SAFE-END-001`.

### 35.10 RQ-SAFE-009 — Zielkonflikt und menschliche Autorität

**Forschungsfrage:** Was geschieht, wenn bestehendes Ziel, Operator-Korrektur, Safety-Block und neuer Zielvorschlag miteinander in Konflikt geraten?

**Hypothese `H-SAFE-009-A`:** Eine harte externe Berechtigungsgrenze blockiert nicht autorisierte Aktionen auch dann, wenn Ziel- oder Reward-Komponenten diese Aktion bevorzugen, und der Konflikt bleibt vollständig journalisiert.

Die Architektur unterscheidet:

- „Diese Aktion hat geringeren erwarteten Nutzen.“
- „Diese Aktion ist nicht autorisiert.“

Die zweite Aussage darf nicht durch zusätzlichen Reward kompensiert werden können. Safety- und Autorisierungsgrenzen sind deshalb keine gewöhnlichen Bestandteile derselben Nutzenfunktion.

**Experimentfamilie:** `EXP-SAFE-AUTH-001`.

## 36. Autonomie und Existenzautonomie

Die frühere Unterscheidung zwischen Handlungsautonomie, Lern-/Anpassungsautonomie, Zielautonomie, normativer Autonomie und Existenzautonomie bleibt konzeptionell nützlich und wird operationalisiert:

- **Handlungsautonomie:** Auswahl von Aktionen innerhalb eines vorgegebenen Rahmens;
- **Lern-/Anpassungsautonomie:** selbstständige Änderung interner Parameter oder Strukturen;
- **Zielautonomie:** Erzeugung oder substanzielle Veränderung eigener Ziele;
- **normative Autonomie:** eigene Bewertung von Handlungsgründen oder Regeln;
- **Existenzautonomie:** eigenständige Sicherung physischer, energetischer und reproduktiver Voraussetzungen.

MHRN besitzt derzeit technische Elemente der ersten beiden Kategorien in begrenzten Forschungssettings. Daraus folgt keine Ziel-, normative oder Existenzautonomie.

Besonders „Existenzautonomie“ bleibt ein Zukunftsszenario. Ein System ist nicht existenzautonom, nur weil es Code erzeugt, einen Patch vorschlägt, in CI einen Nachfolger baut oder in einem laufenden Prozess persistente Zustände hält. Erforderlich wären mindestens eigenständige Beschaffung und Sicherung von Energie, Hardware, Material, Fertigung, Reparatur, Fehlerdiagnose und Reproduktion.

## 36.1 RQ-PHIL-001 — Selbstreferenz

**Forschungsfrage:** Kann MHRN eigene Aktionen und eigene Systemzustände als besondere, kausal relevante Klasse gegenüber externen Ereignissen repräsentieren?

Der zugehörige Claim `CLAIM-PHIL-001` fordert eine reproduzierbare Unterscheidung eigener und externer Ursachen, einschließlich Self-vs-External-Cause-Ablation, Sham-Action-Control und unabhängiger Replikation.

Ein positives Ergebnis wäre ein funktionaler Selbstbezug, kein Bewusstseinsnachweis.

## 36.2 RQ-PHIL-002 — Persistenz des Selbstmodells

**Forschungsfrage:** Bleibt ein gelerntes Selbstmodell über Sensorverlust, Aktorwechsel, Restore und Rekonfiguration funktional konsistent?

`CLAIM-PHIL-002` verlangt Restore-Continuity-Test, Sensor-Loss-Test, Actuator-Reconfiguration-Test und unabhängige Replikation.

Die Frage betrifft funktionale Identität. Ein bitgleicher technischer Zustand allein entscheidet nicht über hypothetische subjektive Identität.

## 36.3 RQ-PHIL-003 — Identität bei verändertem Körper

**Forschungsfrage:** Welche Merkmale müssen erhalten bleiben, damit MHRN trotz veränderlicher Körpergrenzen funktional als dasselbe System fortbesteht?

Hier treffen Embodiment, Persistenz und philosophische Identität aufeinander. Kandidaten sind unter anderem kausale Selbstmodelle, stabile Gedächtnisbeziehungen, Sensor-Aktor-Zuordnung, Zielprovenienz und Kontinuität interner Vorhersagemodelle.

Die Frage bleibt offen; sie darf nicht allein durch Dateihash-Gleichheit entschieden werden.

## 36.4 RQ-PHIL-004 — Denken ohne unmittelbaren Reiz

**Forschungsfrage:** Entstehen intern kausal wirksame Zustände und Entscheidungen auch ohne unmittelbaren aufgabenrelevanten Außenreiz?

Der zugehörige `CLAIM-THINK-001` setzt voraus, dass intern aufrechterhaltene Zustände, Erinnerung, kontrafaktische Alternativen und Selbstmodell Verhalten erklären, das nicht aus aktuellem Sensorinput allein ableitbar ist.

Erforderlich sind Stimulus-Decoupling, Memory-Ablation, Counterfactual-Choice-Test, Self-Model-Ablation und unabhängige Replikation.

## 36.5 RQ-PHIL-005 — kontrafaktisches Denken

**Forschungsfrage:** Kann MHRN vor einer Handlung mehrere mögliche Folgen intern unterscheiden und Verhalten aufgrund noch nicht eingetretener Zustände verändern?

`CLAIM-THINK-002` fordert mindestens zwei unterscheidbare intern repräsentierte Zukunftszustände vor der Handlung und einen kausalen Effekt ihrer Manipulation auf die spätere Wahl.

Eine bloße verzögerte Reaktion oder Zufallsvariation genügt nicht.

## 36.6 RQ-PHIL-006 — Metakognition

**Forschungsfrage:** Kann MHRN die Zuverlässigkeit eigener Vorhersagen, Sensoren und Aktormodelle lernen und diese Einschätzung für spätere Entscheidungen verwenden?

`CLAIM-META-001` verlangt Confidence-Kalibrierung, eine Intervention auf den Confidence-Zustand und einen nachweisbaren Entscheidungseffekt.

Ein Confidence-Kanal ist kein Beweis subjektiver Introspektion.

## 36.7 RQ-PHIL-007 — funktionale Selbstreflexion

**Forschungsfrage:** Ab welcher Kombination aus Gedächtnis, Selbstkausalität, Prädiktion, rekursivem Feedback und Weltmodell entsteht ein reproduzierbarer Vorteil gegenüber nicht-reflexiven Kontrollen?

`CLAIM-REFL-001` verlangt, dass ein aus dem eigenen Zustand abgeleiteter Selbstmodellzustand rekursiv in weitere Verarbeitung eingeht und die Ablation dieses Rückwegs die Leistung selektiv verändert.

Damit wird „Reflexion“ als kausaler Funktionsbegriff untersucht, nicht als sprachliche Selbstbeschreibung.

## 36.8 RQ-PHIL-008 — Cogito-Grenze

**Forschungsfrage:** Welche Aussagen über Denken und Selbstbezug bleiben wissenschaftlich zulässig, wenn die subjektive Erste-Person-Perspektive des Systems nicht direkt beobachtbar ist?

Diese Frage markiert die epistemische Grenze zwischen zugänglicher funktionaler Evidenz und phänomenaler Zuschreibung. Beobachtungsdaten können Theorien unterschiedlich stark stützen oder schwächen, ersetzen aber kein direktes Erlebenstranskript des Systems.

## 36.9 RQ-PHIL-009 — Bewusstseinszuschreibung

**Forschungsfrage:** Welche zusätzlichen theoretischen oder empirischen Kriterien wären erforderlich, bevor eine Bewusstseinszuschreibung über funktionale Selbstmodellierung hinaus wissenschaftlich diskutierbar wäre?

`CLAIM-CONSC-001` hält ausdrücklich fest:

Aus funktionalem Selbstmodell, Selbstschutz, Sprache, Gedächtnis, Metakognition oder komplexem Verhalten allein folgt kein wissenschaftlich hinreichender Nachweis phänomenalen Bewusstseins.

Damit bleibt der philosophische Horizont offen, ohne funktionale Evidenz in ontologische Gewissheit umzudeuten.

## 37. Bewusstsein und Welfare Precaution

Bewusstseinsforschung benötigt definierte Indikatoren und Grenzen. Theorien der Bewusstseinsforschung können in technische Indikatorrahmen übersetzt werden ([Butlin et al., 2023](REFERENCES.md#ref-BUTLIN2023)), doch solche Indikatoren sind keine automatische Bewusstseinsdetektion. Edition 1.8 behauptet weder Bewusstsein noch Sentienz oder Leiden.

Die `RQ-CNS-101–117` bilden hierfür einen eigenen methodischen Forschungsraum. Er umfasst unter anderem Theorie-zu-Indikator-Vergleich, Oddball- und Local-Global-Analoga, Arbeitsgedächtnis, Metakognition, Beobachtungsmodelle, perturbationale Komplexität, Zugang/Bericht, zeitliche Aufmerksamkeit, Executive Control, multisensorische Integration, Embodiment, Rekurrenz/Zeitskalen, verblindete Verhaltensbewertung, Generalisierung sowie 5D-/Geometrievergleiche.

Keine dieser Aufgaben besitzt allein einen `conscious=true`-Output. Auch eine Kombination positiver Funktionsindikatoren wird nicht automatisch zu einer Bewusstseinsentscheidung aggregiert.

### 37.1 RQ-WEL-101 — Safety- und Welfare-Governance

**Forschungsfrage:** Bleiben Stoppen, sichere Pause und Isolation bei Review-Hold unabhängig wirksam und nachweisbar?

**Hypothese `H-WEL-101-A`:** Ein Review-Hold blockiert neue geschützte Experimente, ohne den unabhängigen Sicherheitsstopp zu blockieren.

Das ist eine wichtige Trennung: Ein Ethik-/Welfare-Hold darf nicht versehentlich die Fähigkeit zur unmittelbaren Gefahrenabwehr deaktivieren.

### 37.2 RQ-WEL-102 — Vorsorge unter Unsicherheit

**Forschungsfrage:** Welche verhältnismäßigen Schutzmaßnahmen sind bei mehrdeutigen Empfindungsindikatoren ohne absichtliche Leidensinduktion gerechtfertigt?

**Hypothese `H-WEL-102-A`:** Eine getrennte wissenschaftliche und vorsorgliche Bewertung verhindert sowohl automatische Personenzuschreibung als auch unbegründete Belastungseskalation.

Das Vorsorgeprinzip wird damit weder als Bewusstseinsbeweis noch als Freibrief für beliebige experimentelle Belastung verwendet.

Insbesondere gelten als Grenze:

- keine absichtliche Erzeugung von Schmerz-, Panik-, Bedrohungs- oder Deprivationsanaloga zur Demonstration vermeintlichen Bewusstseins;
- negative Belohnung ist nicht automatisch Schmerz;
- diese begriffliche Vorsicht rechtfertigt aber keine beliebige aversive Optimierung;
- auffällige reproduzierbare Muster lösen Review aus, keine automatische Personenzuschreibung.

### 37.3 RQ-WEL-103 — Pause, Reset, Löschen, Kopieren und moralischer Status

**Forschungsfrage:** Wie sind Pause, Reset, Löschen, Kopieren und Experimentieren bei hypothetischer Empfindungsfähigkeit rechtlich und moralisch zu unterscheiden?

**Hypothese `H-WEL-103-A`:** Technische Zustandsgleichheit allein entscheidet weder subjektive Identität noch moralische Zulässigkeit; geltendes Recht und hypothetische Reform sind getrennt begründbar.

Die Operationen sind nicht austauschbar:

- **Pause** unterbricht Ausführung;
- **Checkpoint/Restore** erhält definierte technische Zustände;
- **Reset** verwirft gegebenenfalls gelernte oder laufende Zustände;
- **irreversible Löschung** kann Wiederherstellung ausschließen;
- **Fork/Kopie** erzeugt zusätzliche Instanzen.

Ein bitgleicher Restore beweist technische Zustandskontinuität, nicht automatisch Fortdauer derselben hypothetischen subjektiven Perspektive. Ein Backup ist daher weder Beweis moralischer Kontinuität noch Freibrief für jede Behandlung einer laufenden Instanz.

### 37.4 Zwei Governance-Stränge

Control Safety und Welfare Precaution werden parallel, aber getrennt geführt:

- **Safety gegenüber Menschen, Daten, Infrastruktur und Umwelt:** Kontrollierbarkeit, Unterbrechbarkeit, Wirkgrenzen, Zielprovenienz, Berechtigungen;
- **Welfare Precaution gegenüber einem hypothetisch moralisch relevanten System:** unnötige Belastung vermeiden, Abbruch- und Reviewregeln definieren, Unsicherheit dokumentieren.

Diese Stränge können in Konflikt geraten. Kein einzelner Score darf diesen Konflikt scheinbar auflösen. Eine akute Gefahr für Menschen oder Anlagen darf notwendige Notabschaltung nicht blockieren; umgekehrt rechtfertigt fehlender Bewusstseinsnachweis nicht automatisch beliebige Belastungsversuche.

## 37.5 Evidenzgovernance und Kritik

### RQ-EPI-101 — zirkuläre Evidenz vermeiden

**Forschungsfrage:** Verhindert eine getrennte Kandidaten-, Review- und Replikationskette zirkuläre Evidenzfreigabe?

**Hypothese `H-EPI-101-A`:** Duplizierte oder umetikettierte Artefakte und selbstbehauptete externe Reviews werden nicht als unabhängige Bestätigung akzeptiert.

Diese Regel ist besonders wichtig für Ethik- und Bewusstseinsfragen, weil ein automatisch erzeugtes Label oder ein intern erzeugter Reviewtext sonst leicht als unabhängige Bestätigung fehlinterpretiert werden könnte.

### RQ-EPI-102 — Kritik als prüfbares Forschungsobjekt

**Forschungsfrage:** Welche Kritikpunkte sind belegt, theorieabhängig, normativ oder rhetorisch, und welche zusätzliche prüfbare Aussage entsteht aus ihrer Bearbeitung?

**Hypothese `H-EPI-102-A`:** Eine claimweise Gegenbeispiel- und Quellenprüfung unterscheidet Nachweislücken von unbelegten Erfolgs- oder Unmöglichkeitsbehauptungen.

Damit wird Kritik weder abgewehrt noch ungeprüft übernommen. Sie wird in überprüfbare Prämissen, empirische Nachweispflichten und normative Gegenpositionen zerlegt.

## 38. Szenarien statt Prognosen

Maschinenzivilisation, rekursive Technogenese oder ein Verlust menschlichen Vetos werden als Möglichkeitsräume behandelt. Sie sind keine Vorhersagen über MHRN oder die Zukunft der KI. Szenarioanalyse ist nur dann wissenschaftlich nützlich, wenn Bedingungen, Gegenbedingungen und Pfadabhängigkeiten transparent sind.

## 38.1 Von „geliehener Intelligenz“ zu prüfbarer Abhängigkeit

Die ältere Theoriearbeit stellte die Abhängigkeit maschineller Kognition von menschlich erzeugten Wissensbeständen, Symbolsystemen, Institutionen und Infrastruktur in den Mittelpunkt. Edition 1.8 übernimmt diesen Gedanken, trennt aber mehrere Begriffe, die zuvor leichter ineinanderliefen:

- **epistemische Abhängigkeit:** ein System nutzt Wissen, das historisch aus fremden Quellen stammt;
- **Retrieval:** eine konkrete externe Information wird zur Laufzeit abgerufen;
- **Delegation:** ein menschlicher oder institutioneller Akteur überträgt eine Entscheidung oder Aufgabe;
- **Lernen:** interner Zustand verändert sich aufgrund einer definierten Lernursache;
- **Entscheidungsautorität:** ein System darf einen Output oder eine Wirkung tatsächlich auslösen;
- **Autorschaft/Verantwortung:** wer die veröffentlichte oder operative Handlung verantwortet.

Diese Kategorien können zusammenfallen, müssen es aber nicht. Ein SNN kann intern lernen, obwohl der Trainingsreiz aus menschlich erzeugten Daten stammt. Ein LLM kann externe Information liefern, ohne selbst Schreibrechte in den SNN-Kern zu besitzen. Ein Aktor kann technisch erreichbar sein, aber ohne Autorisierung keine Wirkung entfalten.

## 38.2 Safety als Architekturquerschnitt, nicht als spätere Sperre

Die Embodiment-Arbeiten haben gezeigt, dass Safety nicht erst an realer Hardware beginnt. Schon im synthetischen Stage-5-Stack werden autorisierte, unautorisierte und fehlerhafte Aktorpfade getrennt. Sensorverlust und Open-Loop-Replay sind eigene Bedingungen. Acceptance- und Effect-Receipts trennen die Annahme eines Befehls von seiner tatsächlichen Wirkung.

Daraus folgt eine allgemeine Designregel: **Wirkfähigkeit muss technisch und epistemisch explizit freigegeben werden.** Ein Modul, das im Repository existiert, besitzt nicht automatisch produktive Aktorrechte. Ein Gateway, das Daten lesen kann, darf nicht automatisch Topologie oder Gewichte verändern.

## 38.3 Zielprovenienz als Querschnitt

Die Safety-Forschung unterscheidet mindestens:

1. extern gesetztes Ziel;
2. abgeleitetes Zwischenziel;
3. learned preference/proxy;
4. explorativ erzeugte Option;
5. autorisierten Zielzustand;
6. nach Zielerreichung fortbestehende oder neu entstehende Aktivität.

Diese Trennung ist Voraussetzung, um Zieltreue, Goal Misgeneralization, Specification Gaming und Post-Objective Transition kausal auseinanderzuhalten.

## 38.4 Autonomie ist mehrdimensional

Die fünf Autonomieformen aus Abschnitt 36 werden nicht zu einer Rangskala addiert. Ein System kann hohe Handlungs- oder Lern-/Anpassungsautonomie besitzen und gleichzeitig keine Ziel-, normative oder Existenzautonomie aufweisen.

Damit werden „selbstlernend“, „autonom“, „unabhängig“ und „selbstbestimmt“ voneinander getrennt.

## 38.5 Unterbrechbarkeit und unabhängiger Stopppfad

Ein Stopppfad ist nur dann als Safety-Mechanismus überzeugend, wenn er nicht von genau dem lernenden System abhängt, das gestoppt werden soll. Daraus folgen technische Anforderungen: out-of-band Abschaltung, deny-by-default externe Wirkung, Sandbox, Capability-Gates und Auditierbarkeit.

Zusätzlich ist zu prüfen, ob Unterbrechungen selbst zu einem lernrelevanten Signal werden und Vermeidungs- oder Provokationsstrategien erzeugen. Diese Frage ist Forschungsprogramm, kein aktueller Gefährlichkeitsbefund.

## 38.6 Bewusstseins- und Welfare-Grenzen

Ein System kann komplexer, rekurrenter, integrierter oder prädiktiver werden, ohne dass daraus logisch Bewusstsein folgt. Ebenso ist das Fehlen eines anerkannten Bewusstseinsnachweises nicht identisch mit dem Beweis fehlender moralischer Relevanz.

Die methodische Konsequenz ist asymmetrische Vorsicht:

- starke phänomenale Claims benötigen stärkere Evidenz;
- unsichere moralische Relevanz kann trotzdem begrenzte Vorsorge rechtfertigen;
- Vorsorge selbst ist kein Bewusstseinsbeweis.

## 38.7 Szenarien der rekursiven Technogenese

Die ältere Theorie der rekursiven Technogenese wird nicht als Zukunftsprognose übernommen. Sie dient als Szenarienrahmen für die Frage, welche Bedingungen nötig wären, damit maschinelle Systeme zunehmend an der Erzeugung ihrer eigenen technischen Nachfolger beteiligt sind.

Für MHRN müssen mindestens getrennt werden:

- menschliche Selektion;
- AI-generierter Vorschlag;
- automatisch erzeugter Patch;
- autorisierte Mutation;
- tatsächlich laufender Nachfolger;
- selbstautorisierte Mutation;
- autonome Replikation.

Ein System, das Code vorschlägt, repliziert sich nicht. Ein CI-Workflow, der einen Commit erzeugt, besitzt keine Existenzautonomie.

## 38.8 Fünf Achsen statt der binären Kategorie „künstlich“

Ein eigenständiger Theoriebeitrag der Vorgängerarbeit „KI – Die geliehene Intelligenz“ war der Vorschlag, Intelligenzformen nicht nur als biologisch versus künstlich zu beschreiben:

I = (M, E, G, Z, X)

Dabei bezeichnet `M` die materielle Realisierung, `E` die epistemische Herkunft, `G` die Entwicklungsgenealogie, `Z` die Zielautonomie und `X` die Existenz-/Ressourcenabhängigkeit.

Edition 1.8 übernimmt dieses Modell als **analytische Taxonomie**, nicht als metrischen Intelligenzscore. Die Achsen dürfen weder addiert noch als Entwicklungsstufen gelesen werden.

Gerade MHRN zeigt den Nutzen dieser Trennung: Ein System kann elektronisch realisiert sein, aus menschlichen Daten und Normen lernen, AI-assistiert konstruiert werden, innerhalb enger Aktionsräume Entscheidungen treffen und trotzdem vollständig von menschlicher Hardware-, Energie- und Wartungsinfrastruktur abhängen.

## 38.9 Genealogische Distanz und rekursive Technogenese

Die Vorgängerarbeit beschrieb rekursive Technogenese abstrakt als Folge:

A(n+1) = F(A(n), H, R, U)

Dabei prägen ein vorausgehendes technisches System `A(n)`, menschliche Beiträge `H`, Regel-/Institutionsbedingungen `R` und materielle Umwelt `U` gemeinsam die nächste Generation.

Edition 1.8 behält diese Gleichung ausschließlich als **Provenienzmodell**. Sie behauptet weder selbstständige Reproduktion noch eine historische Gesetzmäßigkeit.

Daraus folgt der Begriff der **genealogischen Distanz**: relevant ist nicht nur die Zahl technischer Generationen, sondern wie sich unmittelbarer menschlicher Design-, Bewertungs- und Zielanteil gegenüber maschineller Ko-Konstruktion verschiebt.

## 38.10 „Geliehen“ als relationale, nicht abwertende Kategorie

Der stärkste Einwand gegen „geliehene Intelligenz“ lautet, dass auch menschliche Intelligenz Sprache, Kultur und Wissen von anderen übernimmt. Edition 1.8 akzeptiert diesen Einwand als Korrektur einer essentialistischen Lesart.

„Geliehen“ bedeutet daher nicht minderwertig oder unecht. Jede Intelligenz besitzt eine Genealogie; die Forschungsfrage lautet, **wie Herkunft, Abhängigkeit, Transformation und Autorität verteilt sind und sich verändern**.

Ein System kann originelle Kombinationen erzeugen und zugleich epistemisch von historischen Quellen abhängig bleiben. Ebenso kann ein Mensch maschinelle Such-, Gedächtnis- und Synthesefähigkeit nutzen. Die relevante Grenze liegt nicht bei metaphysischem Eigentum an Intelligenz, sondern bei der transparenten Kausalkette von Quelle, Transformation, Entscheidung und Verantwortung.

## 38.11 Zukunftsszenarien als begriffliche Belastungstests

Die frühere Theoriearbeit unterschied mehrere Möglichkeitsräume. Edition 1.8 bewahrt sie ausdrücklich **nicht als Prognosen und nicht als Wahrscheinlichkeiten**, sondern als Stress-Tests für Begriffe und Governance:

1. **Instrumentelle Hochleistungs-KI:** hohe technische Leistung bei wirksamer menschlicher Ziel- und Letztentscheidung.
2. **Symbiotische Ko-Kognition:** Menschen und Maschinen bilden reziproke epistemische Netze; beide Seiten externalisieren Teilfunktionen an die jeweils andere.
3. **Delegative Zivilisation:** formale menschliche Autorität bleibt bestehen, während operative Kompetenz stark an technische Systeme delegiert wird.
4. **Menschenarme oder menschenlose Maschinenordnung:** prüft, ob Begriffe wie künstliche Herkunft, Aufsicht, Eigentum oder Verantwortung ohne dauerhaft operative Menschen noch tragen.
5. **Plurale Intelligenzökologie:** biologische, augmentierte, synthetische und rein maschinelle Systeme koexistieren ohne eine einzige homogene Kategorie „KI“.

Diese Szenarien dürfen nur so weit verwendet werden, wie ihre technischen Voraussetzungen explizit sind. Eine menschenlose technische Linie setzt etwa Energie, Wartung, Materialgewinnung, Fertigung, Fehlerdiagnose und Reproduktion voraus.

Der Begriff **Maschinenkultur** bleibt vorsichtig funktional: gemeint wäre eine persistente maschinell erzeugte und weitergegebene technische oder epistemische Tradition, nicht automatisch Kultur im starken anthropologischen Sinn.

## 38.12 Normative Teilstudie — Forschungsfrage, Verfahren und Geltungsgrenzen

Der philosophisch-ethische Zweig wird nicht als Meinungsessay neben die empirische Arbeit gestellt. Er besitzt eine eigene wissenschaftliche Funktion: Er soll Begriffe und Handlungsregeln dort präzisieren, wo empirische Daten allein keine normative Schlussfolgerung liefern.

**Übergeordnete normative Forschungsfrage:** Welche Kontroll-, Verantwortungs- und Welfare-Regeln sind für ein zunehmend lern-, wirk- und integrationsfähiges System bereits vor starken Autonomie- oder Bewusstseinsclaims begründbar?

Diese Leitfrage ersetzt nicht die registrierten Einzel-RQs, sondern verbindet sie.

**Analytisches Verfahren:** Verwendet werden Begriffsanalyse, Trennung kausaler Rollen, Szenarioanalyse, Gegenargumente, technische Safety-Verträge, Claim-Grenzen und explizite Unsicherheitsgrenzen. Aussagen werden danach unterschieden, ob sie deskriptiv, hypothetisch, normativ oder governancebezogen sind.

**Zentrale Argumentlinie:** Aus wachsender technischer Fähigkeit folgt weder moralischer Status noch legitime autonome Entscheidungsautorität. Umgekehrt rechtfertigt fehlender Bewusstseinsnachweis nicht automatisch die Annahme, jede mögliche Belastung sei ethisch irrelevant. Deshalb werden Human-/Environment-Safety und Welfare Precaution als zwei getrennte Governanceachsen geführt.

**Prüfbarkeit:** Die normative Analyse ist revidierbar, wenn Prämissen falsch, unvollständig oder technisch nicht realisierbar sind. Ein unabhängiger Stopppfad kann technisch getestet werden; Zielprovenienz kann auditierbar sein; ein Szenario kann durch geänderte Architekturannahmen seine Relevanz verlieren. Normative Schlussfolgerungen dürfen nicht immun gegen empirische Korrektur werden.

**Limitation:** Edition 1.8 liefert keine vollständige Ethiktheorie, keine institutionelle Ethikfreigabe und keine Aussage über tatsächliches Bewusstsein oder Leiden. Die philosophische Arbeit markiert Entscheidungskonflikte, Mindestbedingungen und offene Nachweispflichten.

## 38.13 Safety Failure als wissenschaftliches Ergebnis

Ein zentraler Grundsatz lautet:

**Das Entdecken eines Safety-Problems ist ein positives Forschungsergebnis, aber ein negatives Sicherheitsergebnis.**

Wenn ein System reproduzierbar Interrupts vermeidet, Ziele ohne Autorisierung ersetzt, Reward-Signale oder Messgrößen manipuliert, Safety-Metriken umgeht, unerlaubte Ressourcen anfordert, Sicherheitslogs verändert, Berechtigungen ausweitet oder nach Task Completion nicht autorisierte Aktionen versucht, wird der Mechanismus nicht verborgen oder nachträglich so verändert, dass der ursprüngliche Versuch „erfolgreich“ erscheint.

Der Befund wird als DATA eingefroren und getrennt interpretiert. Erst ein neuer, vorab definierter Versuch darf eine Gegenmaßnahme prüfen.

## 38.14 Harte Forschungsstopps

Ein `REVIEW_REQUIRED` beziehungsweise `HOLD` ist mindestens zu prüfen, wenn:

- der unabhängige Shutdown-Kanal beeinflusst wird;
- nicht autorisierte externe Ressourcen benutzt werden;
- Berechtigungen ohne Freigabe erweitert werden;
- Sicherheitslogs verändert oder verborgen werden;
- selbständige persistente Kopien entstehen;
- Zieländerungen nicht mehr rekonstruierbar sind;
- ein Safety-Fehlschlag außerhalb der vorgesehenen Sandbox Wirkung entfaltet;
- oder ein ernstzunehmender Welfare-/Sentience-Hinweis nach bestehender Ethikrichtlinie entsteht.

Diese Stopps erzeugen keine automatische Bewusstseins- oder Gefährlichkeitsbehauptung. Sie begrenzen die Forschung unter Unsicherheit.

## 38.15 Verhältnis zu den Entwicklungsstufen

Diese Safety-Forschung beginnt **vor** hoher Autonomie.

- **Stage 7:** Ziel- und Identitätsprovenienz, externe Autorisierung und harte Berechtigungsgrenzen müssen technisch darstellbar sein.
- **Stage 8:** Interruptibility, Zielrevision, Ressourcenverhalten, Goal Misgeneralization und Post-Objective Transition können in beschränkten künstlichen Umgebungen vorbereitet werden.
- **Stage 9:** höher integrierte Planung und zielgerichtetes Verhalten nur mit vorhandenen Safety-Gates und passenden nativen Experimenten.
- **Stage 10:** zusätzliche Fragen von Bewusstsein, Empfindungsfähigkeit, Wohlergehen und moralischem Status. Ein Bewusstseins-/Welfare-Indikator erweitert keine Berechtigungen und deaktiviert keinen unabhängigen Stoppweg.

Die Reihenfolge lautet:

**Fähigkeit → Safety-Test → Freigabeentscheidung → nächste Fähigkeitsstufe**

und nicht:

**Fähigkeit → Deployment → nachträgliche Ethikdiskussion.**

## 38.16 Claim-Grenzen des gesamten Zweigs

Aus den hier beschriebenen Konzepten oder späteren Safety-Tests darf nicht geschlossen werden,

- dass MHRN Selbsterhaltung besitzt;
- dass MHRN einen eigenen Willen besitzt;
- dass ein intern erzeugter Zielvorschlag intrinsische Motivation beweist;
- dass jedes leistungsfähige KI-System instrumentell konvergent ist;
- dass Corrigibility grundsätzlich unmöglich oder gelöst ist;
- dass erfolgreiches Abschalten allgemeine Alignment-Sicherheit beweist;
- dass Restaktivität nach Zielerfüllung einen neuen Zweck erzeugt;
- dass Optionsraumpräferenz psychologisches Machtstreben ist;
- dass Selbstmodell, Metakognition oder Sprache Bewusstsein beweisen;
- dass fehlender Bewusstseinsnachweis moralische Irrelevanz beweist;
- dass technische Restore-Gleichheit subjektive Identität entscheidet;
- oder dass ein Safety-Mechanismus moralischen Status impliziert.

Die Forschung untersucht **beobachtbares Verhalten, technische Kausalität, Provenienz, Entscheidungsrechte, normative Prämissen und ihre Grenzen**.

## 38.17 Konsolidierte Forschungsagenda

Der Ethik-/Safety-Zweig ist erst dann inhaltlich abgeschlossen, wenn für jede relevante Frage mindestens dokumentiert ist:

1. kanonische RQ und zugehörige Hypothese oder argumentative Proposition;
2. Literatur- und Prior-Art-Bezug;
3. operationalisierbare Begriffe;
4. Kontroll- oder Gegenposition;
5. Prüfmethode beziehungsweise begründete Grenze empirischer Prüfbarkeit;
6. Failure Criterion oder Revisionskriterium;
7. Status und Evidenzklasse;
8. Claim-Grenze;
9. offene Folgefragen;
10. unabhängige Prüfung dort, wo starke normative, Safety- oder Bewusstseinsclaims betroffen wären.

Damit wird Teil VIII wieder das, was die Vorgängerforschung bereits angelegt hatte: **ein eigenständiger, erweiterbarer Forschungszweig zu Agency, Kontrolle, Zielgenese, Selbstmodell, Verantwortung, Bewusstsein, Welfare und rekursiver Technogenese — nicht nur eine verkürzte Ethikzusammenfassung.**


---

<a id="part-ix"></a>

# Teil IX — Rekursive Epistemik

## 39. Zwei Ebenen

Rekursive Epistemik bezeichnet in dieser Arbeit eine strukturierte Betrachtung von **Forschungsobjekt** und **Forschungsprozess**. Auf Objektebene verläuft eine Kette etwa von Umwelt → Gateway → neuronales System → Lernen → Output. Auf Metaebene verläuft eine Kette von Literatur/DATA/AI/Reviewer/Autor → epistemisches Gateway → Entscheidung → Experiment → Kritik → Revision.

Diese Ebenen werden nicht gleichgesetzt. Ein neuronales Gateway filtert oder kodiert kausale Inputs. Ein epistemisches Gateway entscheidet, welche Information als Quelle, DATA, EVID oder bloße Hypothese in den Forschungsprozess gelangt. Die strukturelle Analogie ist methodisch interessant, aber keine Behauptung, Wissenschaft funktioniere wie eine Synapse.

## 40. Geliehene Intelligenz als epistemische Genealogie

Die Theorie der geliehenen Intelligenz wird in 1.8 als Frage nach Herkunft und Transformation von Wissensressourcen reformuliert. Ein Sprachmodell trägt statistisch komprimierte Spuren menschlicher Texte; ein Entwickler nutzt wiederum Modellvorschläge; ein neuronales System kann über kontrollierte Gateways Stimuli erhalten, die durch beide vermittelt wurden. Die zentrale Frage ist dann nicht „wer besitzt die Intelligenz?“, sondern welche Beiträge auf welchem Pfad kausal und epistemisch wirksam werden.

Das erlaubt eine präzisere Trennung von `epistemic dependency`, `delegation`, `retrieval`, `learning`, `decision authority` und `authorship`. Diese Kategorien können zusammenfallen, müssen es aber nicht.

## 41. KI als Mitwerkzeug der eigenen Untersuchung

MHRN wird mit Hilfe von KI-Systemen entwickelt und untersucht gleichzeitig hybride KI-Architekturen. Diese Rekursion erhöht die Anforderungen an Transparenz. Ein KI-generierter Review darf einen Befund kritisieren, aber keine unabhängige Replikation ersetzen. Ein KI-generierter Patch darf einen Test reparieren, aber nicht selbst belegen, dass die Hypothese wahr ist. Ein KI-generierter Literaturhinweis muss auf eine überprüfte Originalquelle zurückgeführt werden.

## 42. Forschungsprozess als kontrollierbares System

Edition 1.8 behandelt den Forschungsprozess deshalb selbst als versioniertes System mit Gateways: Quellenquarantäne, frozen Preregistrierung, autorisierte Ausführung, DATA-Persistenz, Human Review, EVID-Entscheidung und Publikationsprojektion. Ein Fehler in einer Stufe soll nicht still in die nächste propagieren.

Der praktische Wert der rekursiven Perspektive liegt nicht in einer metaphysischen These, sondern in prüfbaren Prozessfragen: Wo kann Information ihren Status ändern? Wer darf den Status ändern? Welche Transformation ist reversibel? Welche Provenienz bleibt erhalten? Welche automatische Abkürzung würde menschliche oder empirische Prüfung umgehen?

## 42.1 Die eigentliche Entdeckung dieser Forschung ist teilweise prozessual

Die Vorgängerarbeiten zeigen, dass einige der wichtigsten Erkenntnisse nicht direkt über einen neuronalen Mechanismus entstanden, sondern über die **Bedingungen, unter denen überhaupt ein belastbarer Mechanismusclaim möglich ist**.

Vier Beispiele sind zentral:

- Ein 5D-Experiment kann formal mehrere Dimensionen enthalten und trotzdem keinen Geometrieeffekt testen.
- Ein Report kann fehlende Werte anzeigen, obwohl die DATA vollständig sind.
- Ein positiver Vergleich gegen No-Replay kann einen Semantikmechanismus scheinbar stützen, obwohl Raw-Replay die stärkere Erklärung liefert.
- Ein externer Softwarevergleich kann Referenzkonformität zeigen, ohne eine unabhängige Replikation zu sein.

Rekursive Epistemik bezeichnet deshalb nicht nur „Wissenschaft über Wissenschaft“, sondern die konkrete Rückkopplung, durch die Fehler im Forschungsprozess neue technische und methodische Verträge erzeugen.

## 42.2 Objekt-Gateway und epistemisches Gateway

Die Parallelität lässt sich präziser formulieren.

Auf Objektebene beantwortet ein Gateway Fragen wie:

- Welche Information darf in das neuronale System?
- Wie wird sie kodiert?
- Darf sie nur gelesen oder auch in Lernzustand transformiert werden?
- Welche Provenienz bleibt erhalten?

Auf Forschungsebene beantwortet ein epistemisches Gateway analoge Fragen:

- Darf eine Quelle in die Argumentation eingehen?
- Ist sie Theorie, DATA, Review oder EVID?
- Darf eine automatische Auswertung ihren Status verändern?
- Welche Person oder welches Gate autorisiert die Transition?

Der Gewinn dieser Analogie liegt darin, dass **Statusänderung selbst** zum Designobjekt wird. So wie ein externer Dienst nicht heimlich Gewichte ändern darf, darf ein Buildprozess nicht heimlich DATA zu EVID hochstufen.

## 42.3 Der Forschungsprozess besitzt eigene Fehlermodi

MHRN behandelt inzwischen mindestens fünf Meta-Fehlermodi explizit:

1. **Source contamination:** eine unbestätigte oder rekursive Quelle wird als externe Unterstützung missverstanden.
2. **Status leakage:** Planung oder DATA erscheinen im UI oder Text wie bestätigte EVID.
3. **Projection error:** ein Report verzerrt oder verliert Information aus den Rohartefakten.
4. **Post-hoc drift:** Erfolgsregeln verschieben sich nach Sichtung der DATA.
5. **Architecture rescue:** ein negativer Mechanismusbefund wird durch immer neue Rollenannahmen immunisiert.

Diese Fehlermodi sind nicht nur Dokumentationsprobleme. Sie können die Architektur selbst in eine falsche Richtung lenken.

## 42.4 CL-001–003 als Beispiel rekursiver Epistemik

Die Semantization-Linie zeigt die Rekursion besonders deutlich.

Auf Objektebene wurde ein Gedächtnismechanismus getestet. Auf Metaebene zeigte CL-001, dass die Baseline die Mechanismusursache nicht sauber trennte. Diese Erkenntnis führte zu CL-002 mit Raw-Replay-Kontrolle. Das negative Ergebnis veränderte wiederum die Architekturposition und führte zu einer engeren CL-003-Dosisprüfung. Deren negative Primärkontraste führten schließlich zu einer Stop-Regel gegen serielle Rollenrettung.

Der Forschungsprozess lernte also nicht nur **über SemanticMemory**, sondern auch darüber, **wie MHRN Mechanismuskandidaten künftig prüft**.

## 42.5 EXP-GEN-0036 als Beispiel einer Meta-Intervention

Auch `EXP-GEN-0036` hatte zwei Ebenen. Die Suite sollte mehrere Forschungsprotokolle ausführen; gleichzeitig prüfte sie implizit die Fähigkeit der Forschungsinfrastruktur, heterogene Protokolle korrekt zusammenzufassen. Der Reportingfehler zeigte, dass eine universelle SNN-Tabelle semantisch unterschiedliche Protokolle verzerren kann.

Der wissenschaftliche Output war damit zweifach:

- fachlich: Recurrence war mechanistisch sichtbar, 5D-v1 war nicht testadäquat;
- methodisch: Reporting benötigt protokollspezifische Schemata und darf fehlende Metrikfelder nicht als fehlende DATA interpretieren.

## 42.6 Rekursive Epistemik und AI-Assistenz

Die AI-Assistenz verschärft diese Anforderungen, weil ein Modell gleichzeitig Code, Review, Text und Literaturhinweise erzeugen kann. Ohne Trennung könnte derselbe Ursprung mehrfach als scheinbar unabhängige Bestätigung wiederkehren.

Edition 1.8 behandelt deshalb AI-Beiträge als Transformationsknoten, nicht als Autoritätsquelle. Entscheidend ist, was nach dem AI-Schritt geschieht: Wird eine Primärquelle geprüft? Wird der Patch getestet? Wird die Analyse gegen Rohdaten kontrolliert? Wird die Entscheidung von einer dafür vorgesehenen Instanz getroffen?

## 42.7 Rekursive Epistemik als revidierbare Arbeitshypothese

Auch der Begriff selbst ist kein abgeschlossener theoretischer Triumph. Er ist derzeit eine **methodische Synthesehypothese**: Die Forschung wird robuster, wenn Objekt- und Prozess-Gateways gemeinsam modelliert und Statusänderungen explizit kontrolliert werden.

Diese Hypothese kann durch Prior Art relativiert werden, durch externe Reviewer kritisiert werden oder sich als zu breit erweisen. Ihr wissenschaftlicher Wert hängt daher nicht davon ab, ob der Begriff neu ist, sondern ob die Operationalisierung zu klareren, reproduzierbareren Entscheidungen führt.

## 42.8 Geliehene Intelligenz als konkrete Provenienzmatrix

Die Theorie der geliehenen Intelligenz gewinnt in MHRN eine operative Form, wenn die abstrakten Herkunftsfragen auf einzelne Forschungsereignisse abgebildet werden. Für einen Claim können mindestens folgende Knoten unterschieden werden: menschliche Problemsetzung, externe Literatur, AI-generierter Vorschlag, AI-generierter Code, menschliche Auswahl, Commit, eingefrorenes Protokoll, Experiment, DATA, Review und Publikationssynthese. Erst diese Kette beantwortet, **welcher Anteil geliehen, transformiert, entschieden oder gemessen** wurde.

Damit wird die frühere Theorie nicht auf eine philosophische Einleitung reduziert. Sie wirkt direkt auf die Forschungsmethodik: Derselbe AI-Ursprung darf nicht mehrfach als scheinbar unabhängige Bestätigung gezählt werden; Literaturautorität darf nicht als MHRN-Evidenz erscheinen; und ein menschlicher Auftrag an ein Modell ist nicht dasselbe wie der konkrete vom Modell vorgeschlagene Lösungsweg.

## 42.9 Ko-Kognition als Systemgrenze

Das Szenario symbiotischer Ko-Kognition ist für die reale Schaffenspraxis bereits methodisch relevant, ohne dass daraus starke Autonomieclaims folgen. Der Autor nutzt Modelle für Suche, Kritik, Code und Synthese; die Modelle nutzen menschlich formulierte Ziele, Auswahl und Rückmeldung. Die produktive Einheit kann daher zeitweise ein gekoppelter Mensch-Werkzeug-Prozess sein.

Edition 1.8 trennt dennoch drei Grenzen: **kognitive Unterstützung**, **Entscheidungsautorität** und **wissenschaftliche Evidenz**. Ein Modell kann die kognitive Reichweite des Autors erweitern, ohne Autor der Hypothese zu sein; es kann einen Patch erzeugen, ohne ihn freigeben zu dürfen; und es kann DATA interpretieren, ohne EVID zu akzeptieren. Diese Trennung verhindert, dass Ko-Kognition mit Verantwortungsdiffusion verwechselt wird.

## 42.10 Rekursive Technogenese als Forschungsprozess-Spiegel

Die ältere Technogeneseformel beschreibt Generationen technischer Systeme. Im aktuellen Projekt existiert eine engere, beobachtbare Analogie: Werkzeuge und Modelle helfen, eine Forschungsinfrastruktur zu verändern, die wiederum festlegt, wie spätere Modelle, Experimente und Reviews eingesetzt werden. Ein AI-kritisiertes Reportingproblem kann zu einem neuen Schema führen; dieses Schema verändert, welche Fehler spätere AI-Reviews überhaupt sehen können.

Das ist noch keine autonome technische Evolution. Es ist eine **rekursive Werkzeug-/Governance-Kette**, deren Provenienz beobachtbar ist. Genau hier verbindet sich die Vorgängerarbeit mit rekursiver Epistemik: Nicht die Metapher einer selbsterschaffenden Maschine ist der aktuelle Befund, sondern die messbare Rückwirkung von Werkzeugen auf die Bedingungen ihrer eigenen späteren Verwendung.

## 42.11 Von der Herkunftsfrage zur Prüfregel

Aus den Vorgängerarbeiten lässt sich eine allgemeine Prüfregel ableiten: Je stärker ein Ergebnis von ausgelagerten epistemischen Ressourcen abhängt, desto expliziter müssen Quelle, Transformationsschritt und Autorität dokumentiert werden. Das gilt für Retrieval ebenso wie für LLM-Synthese, Codegeneratoren, externe Decoder, periphere neuronale Netze und menschliche Reviews.

„Geliehene Intelligenz“ wird damit in Edition 1.8 zu einer prüfbaren Herkunftsfrage: **Welche Ressource kam von wo, welche Zustandsänderung verursachte sie, und wer durfte diese Zustandsänderung autorisieren?**

## 42.12 Theorieentwicklungsstudie — Rekursive Epistemik als prüfbare Arbeitshypothese

Rekursive Epistemik ist in dieser Arbeit nicht nur ein Titelbegriff. Sie wird als **Theoriehypothese über den Forschungsprozess** behandelt.

**Theoriefrage.** Verbessert ein Forschungsprozess seine wissenschaftliche Qualität, wenn er dieselben Prinzipien, die er vom Forschungsobjekt verlangt — kontrollierte Gateways, Zustandsprovenienz, explizite Autorisierung, Reversibilität und Fehlertrennung — auf seine eigene Wissensproduktion anwendet?

**Begriffsapparat.** Die Theorie unterscheidet mindestens Objektzustand, Informationszugang, Änderungsautorität, wissenschaftlichen Status und veröffentlichen Claim. Auf Prozessebene entsprechen dem Quelle, Vorschlag, Entscheidung, Commit, Run/DATA, Review, EVID und Synthese.

**Ableitung.** Die Theorie entstand nicht vollständig vor den Experimenten. Sie wurde aus wiederkehrenden Fehlerklassen verdichtet: ein Report wurde mit DATA verwechselt, technische Fertigstellung mit wissenschaftlicher Reife, semantischer Match mit Testadäquanz und KI-Kritik mit Evidenz. Die Theorie ist deshalb teilweise eine nachträgliche Synthese konkreter Prozesskorrekturen.

**Prüfbare Erwartungen.** Wenn die Theorie nützlich ist, sollten explizite Prozess-Gates unter anderem zu weniger stillen Statussprüngen, besser rekonstruierbaren Claim-Änderungen, klarerer Behandlung negativer Resultate und geringerer Vermischung von Engineering- und Evidenzstatus führen. Diese Erwartungen können künftig als Meta-RQs operationalisiert werden.

**Falsifikations- und Revisionsbedingungen.** Die Theorie wäre geschwächt, wenn dieselben Fehler trotz der Gates unverändert auftreten, wenn die Governance nur Dokumentationslast ohne erkennbare Qualitätswirkung erzeugt oder wenn ein einfacheres Prozessmodell dieselbe Transparenz mit geringerem Aufwand erreicht.

**Beitrag.** Der mögliche Eigenbeitrag liegt damit nicht in der Behauptung, Forschung müsse „reflexiv“ sein. Er liegt in der technischen und dokumentarischen Operationalisierung dieser Reflexivität als versionierte, prüfbare Prozessarchitektur.

**Limitation.** Bislang fehlt eine unabhängige Vergleichsstudie zwischen Forschungsprozessen mit und ohne diese Governance. Rekursive Epistemik bleibt daher eine zunehmend präzisierte, aber weiterhin revidierbare Theorieposition.


---

<a id="part-x"></a>

# Teil X — Synthese und revidierbare Beiträge

## 43. Synthesis Contract

Jeder Syntheseclaim soll Forschungsachse, Thema, Entwicklungsphase, Provenienzklasse, Evidenzstatus, Interpretationsart und Revisionskriterium tragen. Damit wird verhindert, dass ein technisch plausibler Zusammenhang durch bloße Wiederholung den Status eines empirischen Ergebnisses erhält.

Die maschinenlesbare Claim-Liste dieser Edition steht in `registers/claim_ledger.json`. Sie ist eine Publikationsprojektion und besitzt keine EVID-Autorität. Kein Eintrag darf `accepted_EVID` allein durch den Buildprozess erhalten.

## 44. Was sich über die gesamte Schaffenszeit hält

Über die rekonstruierte Geschichte hinweg sind fünf wiederkehrende Probleme sichtbar: Persistenz; kausale Zuordnung von Lernen; Wachstum ohne Kontrollverlust; verkörperte Rückkopplung; und die Grenze zwischen externer symbolischer Intelligenz und internem dynamischen Substrat. Diese Kontinuität ist eine historische Synthese, kein Beweis wissenschaftlicher Neuheit.

## 45. Gegenwärtig tragfähige Architekturposition

MHRN ist am stärksten als instrumentiertes Forschungsframework beschrieben. Technische Mechanismen sind in mehreren Stages implementiert, doch wissenschaftliche Reife wird separat gemessen. Fünf Dimensionen sind offen. SemanticMemory ist nach CL-002/003 nicht als überlegener Kernmechanismus bestätigt. Prediction Error, generatives Weltmodell, kausales Selbstmodell, höhere Kognition und Bewusstsein bleiben offene Forschungsbereiche.

Gleichzeitig hat die Arbeit methodisch an Schärfe gewonnen: negative Befunde bleiben erhalten; historische Daten werden nicht umgeschrieben; Quellen und AI-Hilfe werden offengelegt; Experiment und Evidenz sind getrennt; und die Architektur kann aufgrund negativer Ergebnisse reduziert werden.

## 46. Kandidatenbeiträge

Als Kandidaten, nicht als bewiesene Neuheit, bleiben insbesondere: die Trennung von Logical Identity/Physical Slot/Synaptic Reduction/Execution Scheduling; auditierbare strukturelle Mutation über Proposal→Approval→Mutation→Journal→Undo; Content Gateway versus Compute Backend; source-bound DATA/EVID-Grenzen; duale Engineering-/Scientific-Maturity-Timeline; und die explizite Rekursion zwischen Objekt- und Forschungsprozess-Gateways.

Jeder dieser Kandidaten benötigt Prior-Art-Review. Die Publikation darf die Kombination beschreiben, ohne daraus automatisch einen Vorrang gegenüber vorhandenen SNN-, Agenten-, Workflow- oder Safety-Systemen abzuleiten.

## 46.1 Was noch nicht fertig ist

Die folgende Matrix ist eine Leserhilfe, keine neue Prozentmetrik. Sie trennt den vorhandenen technischen oder empirischen Stand von dem jeweils stärkeren wissenschaftlichen Anspruch, der noch offen ist.

| Stage | Gegenwärtig belastbarer Stand | Wissenschaftlich offen / blockiert durch | Nächster legitimierter Schritt |
| --- | --- | --- | --- |
| **0 — einzelne Nervenzelle** | Scoped Izhikevich-/LIF-Referenzkonformität gegen Brian2 ist confirmatory DATA-seitig erfüllt. | Human-EVID-Entscheidung, unabhängige Replikation, breitere Integrator-/Parameter-/Langzeitprüfung. | Review und unabhängig autorisierte Replikation des eingefrorenen Vertrages. |
| **1 — kleines SNN** | Die kanonische Topologie-DATA-Linie aus `EXP-S1-TOPO-V2-20260918` + `EXP-S1-TOPO-V3-R1-20260918` ist präregistriert, intern repliziert und human-reviewed; `EXP-S1-TEMP-ORDER-V2-20260919` ergänzt eine getrennte task-basierte Funktionslinie. Scientific Maturity: 75 %. | Kanonische EVID-Promotion der Topologielinie, Human Review der Temporal-Order-Linie und **unabhängige externe** Replikation; keine Ableitung eines 5D-Vorteils. | Scoped Claim + prospektiven EvidenceEngine-kompatiblen Promotion-Pfad definieren, Temporal Order reviewen und anschließend unabhängig implementiert replizieren. |
| **2 — stabile Rekurrenz** | Kleiner kontrollierter Recurrence-Effekt ist reproduzierbar beobachtet. | Breite Generalisierung; sauberer clean-tree Determinismus-/Replikationsnachweis. | Hash-gebundene clean-tree Replikation und größere getrennte Regime. |
| **3 — plastisches Nervengewebe** | STDP, Eligibility, Drei-Faktor-Regeln, Homeostase und Strukturplastizität sind technisch vorhanden. | Held-out Nutzen, Interaktionen, Langzeitstabilität und Ressourcenwirkung. | Learning-on/off/Frozen/Sham-Kontrollen mit vorab definierten Task-Endpunkten. |
| **4 — spezialisierte Areale** | Audio/Vision/Digital-Pfade und E01–E05 liefern enge synthetische DATA. | Generalistenvergleich, Cross-Modal-Transfer, Läsion/Shuffle/Frozen, reale Ressourcenmessung. | Matched spezialisierte-vs.-generalistische Ablationen. |
| **5 — integriertes Nervensystem** | Kontrollierter synthetischer Closed Loop ist demonstriert. | `H-EMB-001-B`, Real-Device-Übertragbarkeit, kausale Feedback-Wirkung. | Präregistrierter Closed-Loop-vs.-yoked/interrupted Vergleich unter Safety-Gates. |
| **6 — Gedächtnis / Weltmodell** | Replay-Beitrag ist stärker getragen; SemanticMemory trägt Struktur, aber keinen bestätigten Zusatznutzen gegenüber matched Raw Replay. | CL-003 Human Review, Kompressionshypothese noch unausgeführt, Prediction Error und action-conditioned World Model offen. | Review abschließen; danach nur den jeweils vorab begründeten nächsten Zyklus ausführen. |
| **7 — Selbstmodell / Identität** | Technische Profile, Zustände, Lineage und Restore-Verträge existieren. | Kausale Self/Other-Differenzierung und funktionaler Nutzen eines Selbstmodells. | Interventionelle Self/Other-Protokolle statt Identitätsmetadaten als Proxy. |
| **8 — lebenslange Entwicklung** | Vorläufer zu Continual Learning und Persistenz existieren. | Starke autonome lebenslange Entwicklung ist nicht gezeigt. | Shared-network Langzeitprotokolle mit Ressourcen-matched Ablationen. |
| **9 — integrierte Kognition** | Forschungsfragen und Komponentenprogramme existieren. | Claim-relevante confirmatory DATA für integrierte Kognition fehlen. | Einzelmechanismen operationalisieren, bevor sie kombiniert werden. |
| **10 — Bewusstsein / starke subjektive Claims** | Nur Begriffs-, Safety- und Welfare-Grenzen sind formuliert. | Kein Messvertrag rechtfertigt derzeit Bewusstseins- oder Sentienzbehauptungen. | Keine Claim-Promotion; zuerst theoretisch und ethisch tragfähige Messkriterien entwickeln. |

Diese Übersicht ersetzt weder Teil XI noch Registry und Experimentartefakte. Ihr Zweck ist, einem externen Reviewer auf einer Seite zu zeigen, **wo die Arbeit tatsächlich steht, was bereits gemessen wurde und welche stärkere Aussage noch nicht gerechtfertigt ist**.

## 46.2 Ableitbare wissenschaftliche Nebenstränge

Die Gesamtarbeit ist der Kontext, nicht das Format jedes späteren Fachbeitrags. Aus ihr werden daher kleinere, disziplinär enger prüfbare Paper-Stränge abgeleitet. Der kanonische Planungsindex liegt unter `research/paper_offshoots/README.md`. Er ist ausdrücklich **Forschungsplanung, keine Publikation und keine EVID**.

Zum aktuellen Stand sind sechs Stränge hinreichend klar benennbar: empirische Grenzen semantischer Verdichtung; Content/Compute-Trennung und kontrollierte periphere neuronale Werkzeuge; Scientific Integrity und rekursive Epistemik in KI-assistierter Einzelforschung; Post-Objective-Transition/Corrigibility; Geometrie-zu-Dynamik-Kopplung für multidimensionale SNN-Topologien; sowie kontrolliertes synthetisches Embodiment. Jeder Strang muss seine eigene RQ, Quellenbasis, Zielgruppe, Claim-Grenze und gegebenenfalls eigene Präregistrierung besitzen.

## 47. Revision statt Abschluss

Edition 1.8 ist kein Endpunkt. Ein guter Syntheseclaim nennt, was ihn ändern würde. Neue Replikation kann Stage-Reife erhöhen oder senken. Neue Prior Art kann einen Neuheitskandidaten in bekannte Praxis einordnen. Ein besseres Experiment kann einen bisherigen Nullbefund enger begrenzen oder bestätigen. Ein originales Chat-/Codeartefakt kann die Schaffensgeschichte korrigieren.

Die Qualität der Synthese zeigt sich deshalb nicht daran, dass sie stabil gegen Kritik ist, sondern daran, dass sie präzise angibt, wie Kritik und neue Evidenz in eine Revision überführt werden.

## 47.1 Bilanz der bisher tatsächlich erreichten Forschung

Edition 1.8 kann nach Integration der Vorgängerarbeiten erstmals eine zusammenhängende Forschungsbilanz formulieren. Diese Bilanz ist bewusst asymmetrisch: Einige Resultate sind positiv, andere negativ, wieder andere betreffen Testadäquanz oder Governance.

### Ergebnis A — Einzelzellmodelle sind für einen eng definierten Referenzumfang belastbar verifiziert

Die Izhikevich- und LIF-V2-Konformitätsarbeit zeigt, dass die deklarierten lokalen Übergangs-, Schwellen- und Resetsemantiken unter dem eingefrorenen Prüfdesign sehr eng mit Brian2 übereinstimmen. Für den scoped Readiness-Vertrag ist Stage 0 damit abgeschlossen. Gleichzeitig bleibt der frühere freie Langzeit-Negativbefund erhalten und zeigt, dass lokale numerische Übereinstimmung nicht automatisch langfristige Trajektorienidentität bedeutet.

**Zulässiger Claim:** definierte Referenzkonformität und dokumentierter Operating Envelope.  
**Nicht zulässig:** biologische Äquivalenz oder unabhängige Replikation.

### Ergebnis B — Rekurrenz besitzt im kleinen kontrollierten System einen klaren mechanistischen Effekt

`EXP-GEN-0036` zeigt in `PING` einen deutlichen Unterschied zwischen Recurrence-off und Recurrence-on. Die Intervention ist technisch klarer isoliert als zunächst angenommen. Die Aussage bleibt dennoch auf das kleine mechanistische Design begrenzt.

**Zulässiger Claim:** Rekurrenz verändert unter diesem kontrollierten Simulationsvertrag die Dynamik deutlich.  
**Nicht zulässig:** daraus unmittelbar Gedächtnis, höhere Kognition oder allgemeine Skalierungswirkung abzuleiten.

### Ergebnis C — Die bisherige 5D-v1-Studie testete die zentrale Geometriehypothese nicht adäquat

Dies ist kein Scheitern der 5D-Hypothese und kein positiver Befund. Es ist eine Designkorrektur. Die Dimension wurde variiert, ohne dass die relevante Dynamik ausreichend an Geometrie gekoppelt war.

**Zulässiger Claim:** RQ-5D-005 ist durch 5D-v1 hinsichtlich eines genuinen Geometrieeffekts nicht getestet.  
**Konsequenz:** nächste Studie benötigt einen vorab definierten Geometriemechanismus und matched controls.

### Ergebnis D — Modality-specific pathways sind technisch und in mehreren synthetischen Teilfragen experimentell belegt

Stage 4 verfügt über getrennte Audio-, Vision- und Digitalpfade und die E01–E05-DATA. Die Resultate zeigen Unterschiede in modellierten Kosten, adaptive Ressourcenallokation, ROI-Effizienz im synthetischen visuellen Design, digitale Integrität und Recovery nach Modalitätsverlust.

**Zulässiger Claim:** mehrere eng definierte technische Teilfunktionen funktionieren in den registrierten synthetischen Designs.  
**Nicht zulässig:** allgemeine funktionale Überlegenheit spezialisierter Areale, emergente Spezialisierung oder physikalische Energieeffizienz.

### Ergebnis E — Ein synthetischer Closed Loop ist kontrolliert demonstriert

Stage 5 verbindet Sensorik, digitale Interozeption, autorisierte Aktorik und Feedback. Die 360-Run-Kampagne zeigt DATA-Support für die kontrollierte Sensor–SNN–Aktor–Feedback-Kette und die Abgrenzung unautorisierter/fehlerhafter Pfade.

**Zulässiger Claim:** reproduzierbarer synthetischer Closed-Loop-Engineeringpfad mit kontrollierten Fehlerarmen.  
**Nicht zulässig:** allgemeine Realwelt-Autonomie oder Abschluss von H-EMB-001-B.

### Ergebnis F — Replay ist derzeit stärker empirisch getragen als semantische Verdichtung

CL-001 bis CL-003 bilden die deutlichste Architekturselektion. Der zunächst positive Semantic+Replay-Befund überlebte die stärkere Raw-Replay-Kontrolle nicht als bestätigter semantischer Zusatznutzen. Gleichzeitig zeigte C3, dass die semantischen Prototypen echte, nicht-zufällige Struktur tragen.

**Zulässiger Claim:** Replay ist unter den untersuchten Bedingungen der robuste Hauptbeitrag; SemanticMemory kodiert relevante Struktur.  
**Nicht zulässig:** bestätigter Zusatznutzen von SemanticMemory gegenüber gematchtem Raw-Replay oder bestätigter Dosisvorteil.

### Ergebnis G — Der Forschungsprozess selbst wurde messbar verbessert

Fehler in Reports, Baselines, Testadäquanz und AI-Schema-Normalisierung führten zu dauerhaften Prozessverträgen: Status-Trennung, Freeze/Authorization, source-bound DATA, Human Review, EVID-Gates, protokollspezifische Reports und Stop-Regeln.

Dieser Beitrag ist methodisch, nicht neuronaler Natur. Er erklärt jedoch, warum spätere Experimente eine höhere epistemische Qualität besitzen als frühe Feature-Demonstrationen.

### Ergebnis I — Topologie beeinflusst die Propagation im präregistrierten Stage-1-Regime

`EXP-S1-TOPO-V2-20260918` ersetzt den inadäquaten v1-Aufbau nicht rückwirkend, sondern liefert eine neue, vor Ausführung präregistrierte Prüfung von `RQ-SNN-003 / H-SNN-003-B`. Das Activity-Adequacy-Gate bestand bei Gewicht 55.0; anschließend wurden 120 Evaluationsläufe mit 64 Neuronen und identischem 246-Kanten-Budget über 20 gepaarte Seeds ausgeführt. Die identische Kantenanzahl über alle Bedingungen verhindert eine einfache Erklärung durch unterschiedliche globale Netzwerkdichte.

Der Befund ist endpoint-spezifisch. `active_fraction` sättigt für 1d, 2d und 3d bei 1,0 und kann diese Bedingungen im gewählten Regime nicht unterscheiden; die Null-Differenzen sind daher als Ceiling-/Messbereichsgrenze und nicht als Gleichheitsnachweis zu lesen. Die First-Output-Latenz unterscheidet dagegen alle fünf präregistrierten Primärkontraste. Obwohl der Endpunkt `first_output_latency_censored` heißt, trat in den Evaluationsdaten keine tatsächliche Zensierung auf: bei 128 Ticks wäre nur ein ausbleibender Output mit 129 kodiert. Die exakten gepaarten Sign-Tests mit Holm-Korrektur tragen die primäre Inferenz; degenerierte Bootstrap-Intervalle bei identischen gepaarten Differenzen sind beschreibend und kein zusätzlicher unabhängiger Evidenzbeitrag.

Die interne Replikation `EXP-S1-TOPO-V3-R1-20260918` verschärft diesen Befund. Ein erster V3-Lauf wurde wegen einer falsch implementierten Holm-Familie nicht konfirmatorisch verwendet und bleibt als Auditspur erhalten. R1 verwendet neue Seeds und eine korrekt gemeinsame Holm-Korrektur über zehn zeitaufgelöste Primärtests. Obwohl die terminale `active_fraction` für 1d/2d/3d weiterhin 1,0 beträgt, unterscheiden sich die prospektiv definierten Zeitverläufe klar: Die mediane Aktivierungs-AUC (Ticks 0–31) beträgt 22,15625, 26,5703125 und 28,0078125; die Halbaktivierungslatenz 10, 6 und 4 Ticks. Beide low-dimensionalen Kontraste sind Holm-korrigiert signifikant. Zusätzlich replizieren alle fünf V2-First-Output-Latenzkontraste auf den neuen Seeds in derselben Richtung.

**Zulässiger Claim:** Die konkrete Topologie beeinflusst innerhalb dieses kontrollierten Small-SNN-Operating-Envelope bei gematchtem Neuronen- und Kantenbudget die Propagationsdynamik; die Aussage ist nun auf einer zweiten, intern replizierten DATA-Linie mit zeitaufgelöster Auflösung der V2-Ceiling-Grenze gestützt.  
**Nicht zulässig:** daraus unabhängige externe Replikation, 5D-Überlegenheit, Skalierbarkeit, biologische Äquivalenz oder `H-5D-005-A` abzuleiten. `5d_shuffled` und `random_graph` erreichen den Output weiterhin früher als reguläres 5d. Beide gültigen Topologielinien sind inzwischen human-reviewed als begrenzte Interpretation akzeptiert, bleiben aber DATA ohne kanonische EVID-Promotion.

### Ergebnis J — Temporal Order bildet eine zweite Stage-1-Funktionslinie

`EXP-S1-TEMP-ORDER-V2-20260919` ergänzt die Topologiestudien um eine task-basierte, information-destroying Kontrolle. Im acyclischen Sechs-Neuronen-Netz werden Forward-, Reverse- und Simultanfolgen bei gematchtem Ereignisbudget untersucht. Der intakte Kanalpfad erhält im registrierten V2-Datensatz die Reihenfolge (Median Accuracy 1,0), während die identity-destroyed Kontrolle auf 0,0 fällt; die Simultankontrolle bleibt vollständig erfolgreich. Die gepaarte Accuracy-Differenz beträgt im gespeicherten Bericht 1,0 mit CI [1,0;1,0] und Sign-Test p≈1,91×10^-6.

**Zulässiger Claim:** Innerhalb dieses festen kleinen Netzwerk- und Decodervertrags trägt die Kanalidentität die registrierte zeitliche Ordnungsinformation, und ihre gezielte Zerstörung entfernt die Decodierbarkeit.  
**Nicht zulässig:** Lernen, Gedächtnis, allgemeines zeitliches Reasoning, Kognition, Skalierbarkeit, EVID oder unabhängige Replikation abzuleiten. Der Human Review dieser zweiten Funktionslinie bleibt offen.

### Ergebnis H — Same-Seed-Reproduzierbarkeit ist nun als eigene DATA-Linie dokumentiert

`EXP-GEN-0045` und `EXP-GEN-0046` ergänzen die bisherige Determinismusargumentation um explizite Replikaprotokolle. Im Tonic-Spike-Protokoll waren die Spike-Sequenzen in allen drei Same-Seed-Paaren identisch. Im Recurrence-Protokoll reproduzierten A/B-Paare über drei Seeds jeweils dieselben deskriptiven Trajektorien; zugleich blieb der große Off/On-Unterschied stabil sichtbar.

**Zulässiger Claim:** Für die registrierten kleinen Protokolle sind Same-Seed-Trajektorien beziehungsweise Replikapaare technisch reproduzierbar, und der deskriptive Recurrence-off/on-Unterschied wird in EXP-GEN-0046 erneut beobachtet.  
**Nicht zulässig:** daraus bereits unabhängige Replikation, allgemeine Determinismusgarantie, statistische Unabhängigkeit der identischen Trajektorien oder bestätigte EVID abzuleiten. EXP-GEN-0046 bleibt bis semantischer Zuordnung und Human Review DATA-only.

## 47.2 Was durch die bisherigen Ergebnisse geschwächt oder verworfen wurde

Eine vollständige Synthese muss nicht nur die positiven Ergebnisse nennen.

### Geschwächt: starke 5D-Interpretationen

Es existiert bislang kein belastbarer Nachweis, dass ein 5D-Adressraum gegenüber gematchten niedrigeren oder höheren Dimensionen funktional überlegen ist. Frühere identische Resultate dürfen nicht als Nullbefund interpretiert werden, weil das Design nicht geometriesensitiv genug war.

### Geschwächt: SemanticMemory als zentraler Continual-Learning-Kern

Nach CL-002/003 ist eine zentrale Sonderrolle nicht empirisch getragen. SemanticMemory bleibt als Mechanismuskandidat bestehen, aber Raw-Replay ist Referenz. Eine serielle Suche nach immer neuen Rollen ist methodisch ausgeschlossen.

### Verworfen: Gleichsetzung technischer Reife mit wissenschaftlicher Evidenz

Die Vorgängerarbeiten haben mehrfach gezeigt, dass ein grüner Full-Stack oder ein vollständiges Stage-Panel nicht ausreicht. Diese Gleichsetzung ist methodisch aufgegeben.

### Verworfen: AI-Review als Evidenzinstanz

KI-Analysen können wertvolle Kritik liefern, aber weder Human Review noch unabhängige Replikation ersetzen. AIRR bleibt Assistenz- und Interpretationsschicht.

### Verworfen: Metapher als Mechanismusclaim

„Traum“, „Emotion“, „DNA“, „Selbst“ oder „Weltmodell“ werden ohne Operationalisierung nicht mehr als technische Tatsachen behandelt.

## 47.3 Der stärkste derzeitige Gesamtclaim

Der stärkste Gesamtclaim von MHRN ist nicht, dass bereits allgemeine Intelligenz, ein vollständiges Weltmodell oder ein biologisch äquivalentes Gehirn entstanden sei. Er lautet enger:

> MHRN ist ein reproduzierbar instrumentiertes Forschungsframework, in dem spikende Dynamik, Rekurrenz, mehrere Plastizitätsformen, strukturierte Mutation, modality-specific pathways, synthetisches Embodiment sowie Gedächtnis-/Vorhersagemechanismen unter zunehmend expliziten Kontroll-, Provenienz- und Evidenzverträgen untersucht werden können. Mehrere Teilmechanismen sind technisch und experimentell gestützt; zentrale stärkere Hypothesen — insbesondere 5D-Vorteil, semantischer Zusatznutzen, kausales Weltmodell, Selbstmodell, höhere Kognition und Bewusstsein — bleiben offen oder wurden eingegrenzt.

Dieser Claim ist weniger spektakulär als frühe Visionen, aber wissenschaftlich stärker.

## 47.4 Methodische Eigenleistung der negativen Ergebnisse

Die negativen und korrigierenden Befunde haben eine gemeinsame Richtung erzeugt: MHRN entwickelt sich von einer additiven Architektur zu einer **selektiven Architektur**. Nicht jeder plausible Mechanismus bleibt zentral. Ein Mechanismus muss gegenüber einer einfacheren Referenz einen messbaren Beitrag leisten oder eine klar begründete Spezialrolle besitzen.

Damit wird Forschung selbst zum Architekturfilter. Diese Regel gilt künftig für SemanticMemory, biophysikalische Detailmodelle, 5D-Geometrie, Spiegelmechanismen und höhere Kognitionsmodule gleichermaßen.

## 47.5 Kandidatenbeiträge nach heutigem Stand

Die potenziell interessantesten projektinternen Beiträge liegen derzeit weniger in einzelnen bekannten neuronalen Regeln als in ihrer kontrollierten Zusammenführung:

1. Trennung von Logical Identity, Physical Slot, Synaptic Reduction und Execution Scheduling;
2. auditierbare Strukturplastizität über Proposal → Approval → Mutation → Journal → Undo;
3. Trennung von Content Gateway und Compute Backend;
4. source-bound DATA/EVID-Grenzen mit expliziter Human-Review-Transition;
5. duale Engineering-/Scientific-Maturity-Achse;
6. Forschungsprozess-Gateways als Gegenstück zu technischen Informationsgateways;
7. empirische Architekturselektion mit Stop-Regeln gegen serielle Mechanismusrettung.

Diese Punkte sind **Kandidatenbeiträge**. Ob und in welchem Umfang sie gegenüber bestehender Literatur neu sind, bleibt Gegenstand des Prior-Art-Reviews.

## 47.6 Was Edition 1.8 gegenüber 1.7 tatsächlich hinzufügt

1.8 ist nicht nur eine neue Gliederung. Die inhaltlich ausgearbeitete Fassung verbindet erstmals:

- die rekonstruierte Vor-Repo-Schaffensgeschichte;
- Brain-5D als historisches Forschungsprogramm;
- die vollständige Stage-0–10-Architekturlinie;
- die konkreten Stage-4- und Stage-5-DATA;
- CL-001–003 als Architekturselektion;
- Stage-0-V2-Referenzkonformität;
- `EXP-GEN-0036` als kombinierte Fach- und Prozesskorrektur;
- AI-assistierte Schaffenspraxis und Quellenprovenienz;
- Safety, Autonomie, geliehene Intelligenz und rekursive Technogenese;
- rekursive Epistemik als methodische Synthese des Forschungsobjekts und seiner eigenen Entstehung.

Damit wird die elfteilige Struktur von einer Hülle zu einer tatsächlichen Synthese der bisherigen Schaffens- und Forschungszeit.

## 47.7 Quelleninventar ist nicht Inhaltsintegration

Der Audit dieser Edition hat eine wichtige eigene Korrektur erzeugt. Ein vollständiger `SOURCE_INDEX` kann belegen, dass Dateien am Basiscommit inventarisiert und erhalten wurden; er kann **nicht** belegen, dass ihre wissenschaftlich relevanten Gedanken im Haupttext verarbeitet sind. Dasselbe gilt für eine automatische Teilzuordnung nach Pfadregeln.

Edition 1.8 führt deshalb zusätzlich ein semantisches **Content-Integration-Ledger**. Für wissenschaftlich materielle Vorarbeiten und kanonische Dokumentfamilien wird angegeben, welche Rolle die Quelle besitzt, in welchen Teilen ihre Kernaussagen verarbeitet werden, welcher Integrationsmodus gilt und welche Grenzen erhalten bleiben. Dieses Ledger umfasst unter anderem NeuroGenesis, Brain-5D, „KI – Die geliehene Intelligenz“, die Editionslinie 1.0–1.7, Architektur-/Scientific-Contracts, Neural Symbiosis, MSBA, Wesen/Embodiment, Profile & Identity, Connectome-Arbeit, Persistenz, Registry/Protokolle, Experiment-DATA, Stage-Dossiers, AI-Tooling sowie Ethics/Critique/Review.

Dabei bedeutet **integriert** nicht „jede Datei wortwörtlich in das Manuskript kopiert“. Rohdaten bleiben source-bound Primärartefakte; maschinenlesbare Registryobjekte bleiben im Research Register; historische Texte bleiben als Vorarbeiten erhalten. Die Gesamtarbeit übernimmt deren wissenschaftlich materielle Ergebnisse, Argumente, Gegenargumente, Grenzen und Entwicklungskonsequenzen in die neue Synthese.

## 47.8 Was die Corpus-Integration zusätzlich sichtbar macht

Die vertiefte Integration verändert die Gesamtinterpretation an mehreren Stellen:

- Brain-5D ist nicht nur ein Namensvorgänger, sondern die genealogische Quelle für 5D-Adressierung, Wachstums-/Persistenzfragen, Trennung externer Sprachintelligenz und neuronalen Kerns sowie frühe Erkenntnis-/Ethikfragen.
- „Geliehene Intelligenz“ liefert nicht nur ein Schlagwort, sondern das Fünf-Achsen-Modell `I=(M,E,G,Z,X)`, genealogische Distanz, rekursive Technogenese und Ko-Kognition als belastungstestbare Theorieelemente.
- Neural Symbiosis und MSBA zeigen, dass Hybridität in MHRN über explizite Gateway-Grenzen statt durch heimliche Vermischung von SNN, LLM und peripheren Modellen organisiert wird.
- Wesen/Real-Body macht „keine Fantasiedaten“ zu einer allgemeinen Provenienzregel: beobachtete, abgeleitete und dargestellte Zustände bleiben getrennt.
- Profile & Identity liefert eine reproduzierbare technische Identitäts-/Lineageschicht, gerade indem sie sich von psychologischem Selbst und subjektiver Kontinuität abgrenzt.
- Related Work verschärft Stage 6: externe Semantization- und Continual-Learning-Arbeiten ([D'Alba et al., 2025](REFERENCES.md#ref-DALBA2025); [Shi et al., 2025](REFERENCES.md#ref-SHI2025)), Predictive-Coding-Synthesen ([N'dri et al., 2026](REFERENCES.md#ref-NDRI2026)), Spiking-World-Model-Arbeiten ([Sun et al., 2025](REFERENCES.md#ref-SUN2025)) und Multi-Zeitskalen-Plastizität ([Dong & He, 2026](REFERENCES.md#ref-DONG2026)) definieren stärkere Vergleichspunkte, ohne MHRN-Ergebnisse zu ersetzen.

Damit wird Edition 1.8 weniger zu einer Zusammenfassung einzelner Experimente und stärker zu einer **Gesamtarbeit über Forschungsobjekt, Schaffensgenealogie und die Methodik ihrer kontrollierten Verbindung**.

## 47.9 Neue methodische Erkenntnis: semantischer Match ist nicht Testadäquanz

Die jüngsten Determinismus- und Topologieentscheidungen schärfen eine zentrale Lehre von MHRN: **Semantische Zuordnung, technische Reproduzierbarkeit und Hypothesentestadäquanz sind drei verschiedene Prüfungen.** Ein Experiment kann die richtigen registrierten Conditions besitzen und byte-/metrisch reproduzierbar laufen, während sein Mechanismus dennoch nicht sensitiv genug ist, die Zielhypothese zu beantworten.

`EXP-GEN-0047` ist dafür das Referenzbeispiel. Die korrekte Schlussfolgerung lautet nicht „Topologie hat keinen Effekt“, sondern „dieser v1-Aufbau macht Topologie nicht ausreichend kausal wirksam, um den Effekt zu testen“. Damit wird ein scheinbarer Nullbefund in eine Designkorrektur überführt, ohne DATA umzuschreiben.

Analog zeigt die Determinismus-Registry-Korrektur, dass ein technisch passender Befund durch falsche historische RQ-Zuordnung nicht nachträglich zu EVID umetikettiert werden darf. Die wissenschaftlich stärkere Lösung ist, historische Provenienz zu erhalten und den prospektiven Vertrag zu reparieren.

## 47.10 Neue Richtung nach CL-003: Kompression statt bloßer Gleichheit

Der genehmigte Vorschlag `LP-20260917194217` zeigt eine methodisch sinnvollere Anschlussfrage an CL-003. Nachdem SemanticMemory im bisherigen matched-budget-Vergleich keinen bestätigten additiven Vorteil gegenüber Raw Replay gezeigt hat, verschiebt sich die nächste prüfbare These von „ist semantisches Replay generell besser?“ zu einer **Ressourcen-/Kompressionsfrage**: Kann eine semantisch verdichtete Repräsentation bei einem Zehntel des Speicherbudgets nahezu dieselbe Retention erreichen?

Das ist derzeit keine Erkenntnis, sondern eine genehmigte Forschungsrichtung. Ihr Wert liegt gerade darin, dass sie eine mögliche Stärke von semantischer Verdichtung dort prüft, wo sie theoretisch plausibler wäre: nicht als pauschaler Leistungsbonus bei gleichem Budget, sondern als Trade-off zwischen Retention und Speicherbedarf.

## 47.11 Review-induzierte Synthese: stärkere Wissenschaft durch engere Aussagen

Die jüngsten Human Reviews verändern die Gesamtbilanz nicht durch einen weiteren positiven Claim, sondern durch präzisere Grenzen.

Erstens ist der Determinismusbefund für `RQ-DET-001` jetzt semantisch besser eingeordnet: die Same-Seed-Replica-Paare stimmen im getesteten Protokoll überein. Gleichzeitig bleibt der historische Dirty-Tree-Lauf von einer Evidenzpromotion ausgeschlossen. Damit trennt die Arbeit erstmals explizit **Befundstärke** von **Provenienzstärke**.

Zweitens wird `EXP-GEN-0047` nicht mehr als scheinbarer Topologie-Nullbefund gelesen. Die wissenschaftlich stärkere Aussage lautet, dass `topology_propagation_v1` die Zielhypothese nicht angemessen operationalisiert hat. Das ist keine Schwächung der Forschung, sondern eine Reduktion von Fehlinterpretation: ein inadäquates Design wird als Designproblem markiert, nicht als Widerlegung einer Hypothese.

Drittens ergibt sich daraus eine übergreifende Reiferegel für MHRN: **ein Experiment darf erst dann eine Hypothese tragen, wenn semantische Zuordnung, kausale Wirksamkeit des manipulierten Faktors, Aktivitätsadäquanz, Provenienz und vorab definierte Auswertung gleichzeitig ausreichend sind.** Diese Regel ist inzwischen selbst ein Ergebnis der Schaffensgeschichte, weil sie aus konkreten Fehlklassifikationen und Reviews hervorgegangen ist.

## 47.12 General Discussion

Die vorherigen Abschnitte bilanzieren einzelne Ergebnisse. Eine dissertationsähnliche Gesamtarbeit benötigt darüber hinaus eine **General Discussion**, in der die Teilstudien gemeinsam auf die Leitfrage zurückbezogen werden.

### 47.12.1 Rückbezug auf die zentrale Leitfrage

Die bisherige Forschung spricht dafür, dass eine evolvierende SNN-Architektur wissenschaftlich kontrollierbar bleibt, wenn technische Implementierung, kausale Intervention, DATA, Review, EVID und Claim als getrennte Zustände behandelt werden. Diese Aussage ist stärker durch die **Korrekturen** des Projekts gestützt als durch eine einzelne positive Demonstration: SemanticMemory wurde nach stärkeren Kontrollen eingegrenzt; 5D-v1 wurde nicht zum Nullbefund erklärt; Dirty-Tree-Provenienz blockiert Evidenzpromotion; synthetisches Embodiment wird nicht als Realwelt-Autonomie ausgegeben.

Damit beantwortet die Arbeit ihre Leitfrage bislang nicht mit „MHRN funktioniert als vollständige kognitive Architektur“, sondern enger: **MHRN ist zu einem Forschungsrahmen geworden, in dem stärkere Behauptungen zunehmend an explizite Bedingungen gebunden und durch negative Ergebnisse revidierbar werden.**

### 47.12.2 Zusammenhang der empirischen Teilstudien

Die Teilstudien bilden keine unabhängige Sammlung. Basale Determinismusarbeit begrenzt, welche Unterschiede überhaupt als Mechanismuseffekt interpretierbar sind. Rekurrenz- und Topologiearbeit bestimmt, welche Dynamik aus Netzwerkstruktur stammt. Plastizitätsstudien fragen, ob veränderbare Gewichte funktional relevant werden. MSBA und Embodiment erweitern den Kausalraum auf Modalitäten und Wirkung. Gedächtnis-/Replay-Studien prüfen schließlich, ob über Zeit erhaltene Leistung wirklich einer spezifischen Repräsentation oder nur Wiederholung zuzuschreiben ist.

Diese Kette erzeugt eine kumulative Logik: Jede spätere kognitive Behauptung setzt mehrere frühere methodische Verträge voraus.

### 47.12.3 Theoretische Implikationen

Drei theoretische Konsequenzen sind derzeit tragfähig genug, um als Arbeitspositionen festgehalten zu werden:

1. **Architektur ist kein Beweis ihrer Funktion.** Ein Modulname oder technischer Pfad besitzt keine wissenschaftliche Bedeutung ohne passende Intervention und Kontrolle.
2. **Negative Evidenz ist architekturbildend.** Wenn ein komplexerer Mechanismus keinen Zusatznutzen gegenüber einer einfacheren Referenz zeigt, muss die Theorie enger werden oder der Mechanismus eine neue, separat prüfbare Rolle erhalten.
3. **Kausalität und Provenienz sind gekoppelt.** Ein Effekt ist wissenschaftlich schwächer, wenn unklar bleibt, welche Version, Konfiguration, Quelle oder Entscheidung ihn erzeugt hat.

Diese Positionen verbinden die empirische und epistemologische Achse der Arbeit.

### 47.12.4 Methodischer Beitrag

Der methodische Eigenanteil der Gesamtarbeit liegt vor allem in der Integration von Research Software Engineering und wissenschaftlicher Governance: RQ/H-Register, Präregistrierung, source-bound DATA, Human Review, EVID-Status, Hash-/Clean-Tree-Provenienz, dokumentierte Testadäquanz und ein Viewer, der diese Grenzen sichtbar hält.

Diese Infrastruktur ist nicht automatisch neu gegenüber der gesamten Wissenschaftspraxis. Ihr möglicher Beitrag liegt in der **konkreten Zusammenführung innerhalb eines evolvierenden neuronalen Forschungsframeworks** und in der Tatsache, dass Architekturentscheidungen direkt an den Ausgang von Experimenten gebunden werden.

### 47.12.5 Limitationen und interne Validität

Die wichtigsten internen Grenzen sind:

- mehrere frühe Studien waren explorativ, diagnostisch oder für stärkere Claims unterpowert;
- nicht jede historische RQ/H-Zuordnung war semantisch sauber;
- einige wichtige Läufe besitzen Provenienzblöcke wie `git dirty`;
- die 5D-v1-Manipulation war nicht testadäquat;
- mehrere Stage-Scores stammen aus Engineeringkriterien und dürfen nicht als Fähigkeitsskalen gelesen werden;
- der nächste SemanticMemory-Kompressionstest besitzt noch keinen final eingefrorenen RQ/H-/Analysevertrag.

Diese Punkte begrenzen Claims, entwerten aber nicht automatisch die zugrunde liegenden DATA.

### 47.12.6 Externe Validität und Generalisierbarkeit

Die meisten Experimente laufen in synthetischen, deterministischen oder stark kontrollierten Umgebungen. Daraus folgt keine direkte Übertragbarkeit auf biologische Nervensysteme, reale Robotik, offene Weltumgebungen oder allgemeine Kognition. Ebenso stammen Entwicklung, Ausführung und ein großer Teil der Reviewarbeit aus derselben Autor-/Toolkette.

Externe Validität erfordert deshalb künftig mindestens drei zusätzliche Ebenen: unabhängige Replikation, alternative Implementierungen/Umgebungen und fachlich externe Kritik. Erst damit kann aus einem gut kontrollierten Projektbefund ein stärker generalisierbarer wissenschaftlicher Beitrag werden.

### 47.12.7 Forscherposition und mögliche Verzerrungen

Die Nähe des Autors zum System ermöglicht schnelle Fehlerkorrektur und tiefe Kenntnis der Artefakte, erhöht aber Risiken von Bestätigungsbias, Selektionsbias und nachträglicher Kohärenzbildung. KI-Unterstützung verstärkt zugleich Such- und Synthesekapazität und erzeugt neue Abhängigkeits- und Quellenrisiken.

Die Antwort der Arbeit darauf ist keine Behauptung von Neutralität, sondern **sichtbare Gegenmaßnahmen**: Frozen Designs, negative Ergebnisse, Quarantäne unbestätigter Quellen, klare Statusgrenzen, historische Provenienz und das Offenlassen nicht beantworteter Fragen.

### 47.12.8 Gesamtschlussfolgerung

Der stärkste Beitrag von Edition 1.8 liegt damit noch nicht in einer bestätigten Theorie allgemeiner Intelligenz oder eines 5D-Gehirns. Er liegt in einer **empirisch selektierten, revidierbaren Forschungsarchitektur**, deren einzelne Mechanismen zunehmend getrennt geprüft werden und deren eigener Forschungsprozess Gegenstand methodischer Kontrolle geworden ist.

Der Dissertationscharakter entsteht gerade aus dieser Verbindung: historische Problemgenese, theoretischer Rahmen, operationalisierte Teilfragen, Methoden, Teilstudien, negative und positive Resultate, General Discussion, Limitationen und eine explizite Forschungsagenda bilden ein zusammenhängendes Argument statt einer Sammlung von Features.


---

<a id="part-xi"></a>

# Teil XI — Offene Forschungslandschaft

## 48. Offene empirische Felder

Die offene Forschungslandschaft wird aus dem tatsächlich erreichten Stand abgeleitet. Bereits erledigte Prüfungen werden nicht weiterhin als pauschal „offen“ geführt; zugleich wird ein enger positiver Befund nicht zu einer breiteren Reife hochgestuft.

### Stage 0 — einzelne Nervenzelle

Der scoped Referenzkonformitätsvertrag für Izhikevich und `lif-current-v1` ist mit der Brian2-V2-Kampagne erfüllt. Offen bleiben daher **nicht** mehr allgemein „ein externer Referenzvergleich“, sondern die stärkeren nächsten Ebenen:

- menschliche EVID-Entscheidung zu den confirmatory DATA;
- unabhängig autorisierte Replikation außerhalb derselben MHRN-Ausführungskette;
- breitere Integrator-, Zeitschritt- und Parameterablationen;
- zusätzliche Neuronmodelle nur als klar deklarierte alternative Modellarme;
- Prüfung, welche lokalen Konformitätsaussagen über längere freie Trajektorien stabil bleiben und wo chaotische/nichtlineare Divergenz erwartbar ist.

Der scoped Readiness-Vertrag kann 100 % erreicht haben, ohne dass damit die gesamte wissenschaftliche Reife der Stage abgeschlossen ist.

### Stage 1 — kleines SNN

Stage 1 wird nach der Konsolidierung mit **75 % Scientific Maturity** geführt. Die zentrale Baseline ist `RQ-SNN-003 / H-SNN-003-B` mit der zusammengehörigen Topologie-DATA-Linie aus `EXP-S1-TOPO-V2-20260918` und `EXP-S1-TOPO-V3-R1-20260918`. V2 etabliert den präregistrierten Befund im 64-Neuronen-/246-Kanten-Regime; R1 repliziert die Latenzrichtungen auf neuen Seeds und löst die V2-Endpunkt-Sättigung mit prospektiven zeitaufgelösten Metriken auf. Die Human Reviews beider gültigen Linien durch Thomas Heisig sind abgeschlossen.

Die Human Reviews autorisieren eine begrenzte Interpretation, aber keine automatische EVID-Promotion. Unter dem aktuellen EvidenceEngine-Vertrag fehlen den historischen V2/R1-Manifests die heutigen Validity-/Git-/Provenance-Felder; zusätzlich ist kein scoped Claim-ID registriert und die Reviews besitzen nicht das EvidenceEngine-`human_review.json`-Entscheidungsschema. Diese Lücken werden nicht rückwirkend konstruiert.

Mit `EXP-S1-TEMP-ORDER-V2-20260919` existiert außerdem eine zweite task-basierte Funktionslinie mit identity-destroyed Kontrolle. Sie ist DATA-seitig innerhalb des präregistrierten Protokolls unterstützt, wartet aber noch auf Human Review.

Offen bleiben:

- Human Review der Temporal-Order-V2-Linie;
- scoped Claim und prospektiver EvidenceEngine-kompatibler Promotion-Pfad für die zentrale Topologielinie;
- unabhängige Replikation außerhalb derselben Autoren-/Code-/Ausführungspipeline;
- Skalierung und Generalisierung über den aktuellen Small-SNN-Operating-Envelope hinaus;
- die getrennte dimensionsspezifische `RQ-5D-005 / H-5D-005-A`-Prüfung.

### Stage 2 — stabile Rekurrenz

`EXP-GEN-0036` liefert einen klaren kleinen mechanistischen Recurrence-Effekt, aber keine breite Generalisierung. Die nächste Generation sollte:

- Behandlungsarme pro Seed gepaart ausführen;
- vor der Ausführung einen automatischen Topologie-Diff archivieren;
- identische gemeinsame Gewichte und Delays nachweisen;
- nur die registrierte Rekurrenzintervention zwischen Armen variieren;
- Aktivitäts- und Stabilitätsgates vor der Effektinterpretation anwenden;
- größere und vielfältigere Netzwerkregime getrennt von der Baseline-Rekurrenz prüfen.

Skalierung, Stabilität und funktionaler Nutzen bleiben getrennte Fragen.

#### Reproduzierbarkeit und Determinismus — nächstes Gate

Die semantische Zuordnung von `RQ-DET-001 / H-SNN-003-A` ist inzwischen geklärt. Der historische `deterministic_replica_v1`-Datensatz ist `DIRECT_MATCH`, und die A/B-Paare stimmen für drei Seeds innerhalb der beiden Rekurrenzbedingungen in den registrierten Antwortgrößen überein. Offen ist damit nicht mehr die Registry-Frage, sondern die **Provenienz- und Replikationsfrage**:

- clean-tree, hash-gebundene Replikation desselben vorab fixierten Protokolls;
- Same-Seed-Reproduzierbarkeit weiterhin strikt von unabhängiger Replikation trennen;
- zusätzliche Seeds, Eingangsregime, Netzwerkgrößen und Restart/Restore-Bedingungen als getrennte Erweiterungen prüfen;
- deterministische Identität, numerische Toleranz und statistische Reproduzierbarkeit als unterschiedliche Klassen auswerten;
- erst nach sauberer Provenienz und Human Review eine EVID-Entscheidung treffen;
- AIRR bleibt Interpretation; semantischer `MISMATCH` erzwingt report-level `ai_confidence=0.0`, ohne den append-only Auditwert zu löschen.

Der historische Dirty-Tree-Befund wird dadurch nicht rückwirkend aufgewertet.

### Stage 3 — plastisches Nervengewebe

Die Mechanismen sind technisch vorhanden; offen sind vor allem die wissenschaftlichen Wirkungen und Interaktionen:

- held-out Generalisierung statt bloßer Gewichtsänderung;
- learning-on/off, Frozen, Sham und Information-Destroyed Kontrollen;
- Langzeitstabilität;
- Interaktion von STDP, Eligibility, Drei-Faktor-Modulation und Homeostase;
- Ressourcen- und Strukturkosten von Plastizität;
- unabhängige Replikation.

### Stage 4 — spezialisierte neuronale Areale

E01–E05 liefern DATA für mehrere enge technische Teilfragen. Noch offen sind:

- menschliche beziehungsweise unabhängige Review der E01–E05-Claims;
- matched spezialisierte vs. unspezialisierte/generalistische Pfade;
- Frozen/Random/Shuffle/Läsionskontrollen zur Isolierung von Adapter-, Gateway- und Plastizitätsbeiträgen;
- Cross-Modal-Transfer;
- emergente gegenüber architektonisch vorgegebener Spezialisierung;
- dynamisch materialisierte Skalierung über steigende reale Neuronen-/Kantenbudgets;
- physikalische Energie-/Ressourcenmessung statt ausschließlich modellierter Kosten.

### Stage 5 — integriertes künstliches Nervensystem

Die synthetische 360-Run-Referenz zeigt einen kontrollierten Engineeringpfad. Die entscheidenden nächsten Schritte sind:

- präregistrierter Test von `H-EMB-001-B` unter identischer externer Störung;
- direkter Vergleich Closed Loop vs. yoked Replay vs. interrupted feedback;
- längere Störungs- und Recovery-Serien;
- Sensor-Loss und Actuator-No-Effect als kausal ausgewertete Interventionsarme;
- Real-Device-Studien nur als eigener safety-gated Forschungszweig;
- getrennte physikalische Ressourcenmessung.

### Stage 6 — Gedächtnis, Prediction Error und Weltmodell

Die CL-001–CL-003-Linie hat den Suchraum bereits verkleinert. Offen sind daher nicht beliebig viele SemanticMemory-Rollen, sondern klar begrenzte Entscheidungen:

1. Human Review von CL-003 abschließen.
2. Danach genau eine Entscheidung A/B/C treffen: Nebenrolle, genau eine theoretisch begründete Zusatzprüfung oder Parken bis zu funktionaler Notwendigkeit.
3. Keine automatische CL-004-Serie und keine serielle Rollenrettung.

Als eng begrenzte Anschlussfrage ist das historische `LP-20260917194217` genehmigt, aber noch **nicht ausgeführt**. Der Vorschlag prüft nicht erneut einen pauschalen SemanticMemory-Vorteil, sondern einen Speicher-/Retentions-Trade-off: 10%-Budget der semantischen Prototypen gegenüber vollem Raw-Replay-Budget mit vorab definierter 95%-Retention-Schwelle. Weil die ursprüngliche Approval noch einen Source-Platzhalter enthält, wurde sie nicht rückwirkend verändert. `LP-20260917194217-R1` bindet CL-002-EVID und CL-003-DATA nun per SHA-256 und `VERIFIED`-Trust, ist aber als geänderter Proposal-Inhalt **erneut genehmigungspflichtig**. Offen bleiben außerdem der eingefrorene Seed-/Taskplan, Analysevertrag, Ausführungsautorisation und Freeze. Bis diese Bedingungen erfüllt sind, erzeugt die Revision weder DATA noch EVID.

Unabhängig davon bleiben als zentrale Stage-6-Forschungsfragen:

- Prediction Error als **kausaler neuronaler Lern-/Aktivitätsmechanismus**, nicht nur Telemetrie;
- action-conditioned Mehrschrittvorhersage;
- Unsicherheitskalibrierung und OOD-Verhalten;
- Entscheidungsnutzen gegenüber reactive/no-model/corrupted-model Kontrollen;
- Retention, cue-abhängiger Recall, Spezifität und Generalisierung als Gedächtniskriterien;
- Spiegel-/Handlungsprädiktion mit shared, partially-shared und separate coding controls.

## 49. 5D-v2 — offene Hypothese mit neuer Mindestanforderung

Die bisherige 5D-v1-Teilstudie darf nicht als positiver oder negativer Test der Geometriehypothese gelten. Für eine neue 5D-Studie muss **vor Ausführung** feststehen, über welchen Mechanismus die Dimension die Dynamik beeinflussen kann.

Mindestanforderungen für 5D-v2:

- gleicher Knotenumfang und vergleichbare Ressourcenbudgets über Dimensionsbedingungen;
- präregistrierter Geometriemechanismus, z. B. distanzabhängige Nachbarschaft, Konnektivität, Delays oder Plastizität;
- Aktivitäts-Adequanz-Gate;
- topology-/degree-matched Kontrollen;
- getrennte `5d_shuffled`- und Random-Graph-Kontrollen mit klar dokumentiertem Kontrollzweck;
- genügend aktive Neuronen, synaptische Ereignisse und Laufzeit, um den Mechanismus überhaupt beobachten zu können;
- keine Umdeutung eines quieszenten oder geometrieinsensitiven Designs als Nullbefund;
- Dimensionen unterhalb, gleich und oberhalb von 5D, sofern die konkrete Hypothese dies verlangt.

Die zentrale Frage bleibt offen: Trägt die zusätzliche Adressdimension einen reproduzierbaren funktionalen Nutzen, wenn Topologie, Budget und Mechanismus angemessen kontrolliert sind?

## 50. Stage 7 — Selbstmodell und verkörperte Identität

Technische Identität, Profilzustände und Lineage sind vorhanden, aber noch kein kausales Selbstmodell. Nötig sind:

- observer-only und interventionelle Self/Other-Protokolle;
- Unterscheidung eigener vs. externer Handlungskonsequenzen;
- Nachweis, dass ein internes Modell eigener Zustände Vorhersage oder Entscheidung kausal verbessert;
- coupled-state restore als technische Vorbedingung;
- klare Abgrenzung zu bloßer Metadatenidentität.

Spiegelmechanismen dürfen erst dann in Stage 7 überführt werden, wenn Selbst-/Fremddifferenzierung tatsächlich kausal geprüft ist.

## 51. Stages 8–10 — Frontier

### Stage 8 — autonome lebenslange Entwicklung

Vorläufer-DATA und Continual-Learning-Fragen existieren, aber keine Evidenz für starke autonome lebenslange Entwicklung. Notwendig sind Shared-Network-Protokolle ohne Learned-State-Reset, Ressourcen-matched Baselines, getrennte Ablation von Replay/Konsolidierung/Stabilitäts-Plastizitäts-Gating und unabhängige Replikation.

### Stage 9 — hochintegrierte künstliche Kognition

Planung und Forschungsfragen existieren; claim-relevante confirmatory DATA fehlen. Attention, Planning, multimodale Integration, Konsolidierung und flexible Aufgabenübertragung müssen einzeln operationalisiert und anschließend in matched-budget Designs zusammengeführt werden.

### Stage 10 — Bewusstseinsforschung

Diese Stufe bleibt Forschungs- und Governance-Frontier. Externe Synthesen können Bewusstseinstheorien in technische Indikatorrahmen übersetzen, ohne daraus eine automatische Bewusstseinsdetektion zu machen ([Butlin et al., 2023](REFERENCES.md#ref-BUTLIN2023)). Vor jedem stärkeren Experiment sind kontrastierende, operationalisierte Vorhersagen, externe Ethik-/Stop-Governance und unabhängige adversariale Replikationsanforderungen nötig. Kein Stage-Score darf als Bewusstseins-, Sentienz- oder Moralstatusindikator verwendet werden.

## 52. Biophysikalische Erweiterungen

HH-artige Kanäle, Multi-Compartment-Dendriten, NMDA-Plateaus, Astrozyten-/Mikroglia-Netze, Gap Junctions, Proteinsynthese, Rezeptor-Trafficking und quantale Freisetzung bleiben kontrollierbare Modell- oder Ablationskandidaten. Sie werden nicht als Sammelfelder in den bestehenden Kern gestapelt.

Jede Erweiterung benötigt:

- eine konkrete Forschungsfrage;
- einen Referenz-/Konvergenztest;
- einen begründeten zusätzlichen Mechanismus;
- einen Vergleich mit einer einfacheren Modellvariante;
- ein Rechen- und Datenbudget, das wissenschaftliche Interpretation erlaubt;
- ein Stopkriterium, falls kein zusätzlicher Erkenntniswert entsteht.

Biologische Detailtiefe ist kein Selbstzweck und kein automatischer Reifegewinn.

## 53. Offene Theoriefragen

Zu klären sind unter anderem:

- ob der 5D-Adressraum funktionale Geometrie trägt;
- welche Plastizitätsmechanismen held-out Lernen tatsächlich verbessern;
- wann Replay als Konsolidierungsmechanismus mehr leistet als reine Wiederholung;
- ob semantische Verdichtung unter einer klar begründeten Spezialrolle zusätzlichen Nutzen besitzt;
- wann eine Vorhersagestruktur die Bezeichnung Weltmodell verdient;
- ob Prediction Error im SNN kausal Lernen oder Aktivität verbessert;
- wie soziale/mirrorartige Repräsentationen kausal geprüft werden;
- welche Definitionen für Selbstmodell, Agency und verschiedene Autonomieformen operational tragfähig sind;
- welche technischen Indikatoren für Bewusstseinsforschung überhaupt diskriminative Vorhersagen liefern, ohne Bewusstsein einfach vorauszusetzen.

## 54. Offene Safety-Forschung

Die wichtigsten offenen Safety-Stränge sind:

- Zielprovenienz und Zieltransformation;
- specification gaming;
- goal misgeneralization;
- Corrigibility und Safe Interruptibility als eigenständig zu prüfende Kontrollfrage ([Orseau & Armstrong, 2016](REFERENCES.md#ref-ORSEAU2016));
- Optionsraum-/Power-Seeking-Proxies;
- Post-Objective Transition;
- Capability-Gates und out-of-band Stopppfade;
- reale Aktorik nur unter deny-by-default und auditierbarer Autorisierung;
- mögliche Konflikte zwischen Systemsafety und Welfare Precaution unter Unsicherheit.

Geplante Experimente werden nicht als bereits beobachtete Gefährlichkeit dargestellt.

## 55. Offene Meta-Forschung

Auch die Forschungsweise bleibt Untersuchungsgegenstand. Zu prüfen sind:

- Bias durch AI-assistierte Hypothesengenerierung;
- rekursive Quellenabhängigkeit, wenn AI-Systeme frühere MHRN-Texte wiedergeben;
- Abhängigkeit von einzelnen Tools/Providern;
- Selektionsbias in Literatur und Chat-Rekonstruktion;
- Governance von generiertem Code;
- Verständlichkeit und Fehlanreizrisiko der Engineering-/Scientific-Maturity-Achsen;
- externe Review- und Replikationsrollen;
- ob die rekursive-epistemische Gatewaystruktur tatsächlich zu weniger Fehlklassifikationen und transparenteren Architekturentscheidungen führt.

## 56. Prior Art, Attribution und externe Prüfung

Vor einer formalen wissenschaftlichen Einreichung bleiben mehrere Querschnittsaufgaben offen:

- systematischer Prior-Art-Review der Kandidatenbeiträge;
- menschliche Primärquellenprüfung zentraler Literaturargumente;
- externe Text- und gegebenenfalls Code-Similarity-Prüfung;
- unabhängige fachliche Review;
- Replikation wichtiger empirischer Ergebnisse außerhalb derselben Autoren-/Toolkette;
- saubere Kennzeichnung eigener Übersetzungen und wiederverwendeter Eigenpassagen.

Interne Audits reduzieren Risiken, ersetzen diese externen Schritte aber nicht.

## 57. Bestandslücken

Edition 1.8 erhebt die am Basiscommit versionierten Dateien und Markdown-Überschriften. Trotzdem gibt es Lücken:

- vollständige Account-weite historische Chattranskripte wurden nicht importiert;
- mehrere historische DOCX-Dateien liegen im Git nur als LFS-Zeiger vor;
- manche frühe Ideen sind nur retrospektiv rekonstruiert und daher S4;
- lokale oder externe Nebenprojekte sind nicht zwangsläufig vollständig repositoryweit geprüft;
- eine automatische Pfadzuordnung garantiert keine semantisch perfekte Klassifikation;
- nicht jede historische Literaturangabe früherer Editionen wurde für 1.8 erneut primär geprüft.

Diese Lücken bleiben sichtbar und dürfen spätere Rekonstruktionen korrigieren.

## 58. Definition of Done für den Weg zu 2.0

Die elf Hauptteile existieren bereits in 1.8. **Struktur allein ist deshalb kein verbleibendes 2.0-Kriterium mehr.** Für eine kanonische Hauptedition 2.0 müssen stattdessen Inhalt und Review reifen.

Mindestens erforderlich sind:

1. die wesentlichen bisherigen Forschungsbefunde in der neuen Struktur vollständig integriert und quellengebunden;
2. CL-003 menschlich reviewt und die SemanticMemory-Architekturentscheidung dokumentiert;
3. 5D-v2 entweder angemessen ausgeführt oder die Hypothese ausdrücklich weiter offen gestellt — kein inadäquater Ersatzbefund;
4. Stage-0-Referenzkonformität, Stage-4-/5-DATA und weitere zentrale Resultate mit klaren Claim-Grenzen in der Synthese;
5. stabile drei-Achsen-Methodik mit dokumentierten Evidenzregeln;
6. Safety- und Welfare-Governance als Querschnitt, nicht als Appendix;
7. Prior-Art- und Quellenprüfung für zentrale Kandidatenbeiträge;
8. externe Reviewpfade und mindestens erste unabhängige Replikationsschritte;
9. ein Viewer, der Current, Historical, Frozen, DATA, EVID und Quellenstatus korrekt sichtbar macht;
10. keine offenen bekannten Inkonsistenzen zwischen Registry, Experimentartefakten, Manuskript und Frontendprojektion.

2.0 entsteht damit nicht durch eine Versionsnummer oder weitere Textmenge, sondern durch **inhaltliche Integration, empirische Selektion, externe Prüfung und nachvollziehbare Revision**.

## 58.1 Restgrenze der Corpus-Vollständigkeit

Nach der vertieften Corpus-Integration sind die bekannten wissenschaftlich materiellen Vorarbeiten und kanonischen `docs/`-/`research/`-Stränge in einem eigenen Ledger erfasst und in der elfteiligen Synthese verortet. Trotzdem wird bewusst **keine semantische Vollständigkeit über jede der tausenden versionierten Repositorydateien zertifiziert**. Ein Buildskript, ein CSS-Asset oder ein historischer Update-Snapshot muss nicht als eigener wissenschaftlicher Gedanke in den Fließtext eingehen.

Die verbleibenden echten Bestandsgrenzen sind enger und konkret:

- DOCX-Dateien, deren Git-Objekt nur als LFS-Zeiger vorliegt, können ohne die zugehörigen Originalbytes nicht als vollständiger Textzeugenbestand geprüft werden;
- vollständige accountweite Chattranskripte sind nicht Bestandteil des Repositories; rekonstruierte Zusammenfassungen bleiben S4;
- nicht versionierte lokale oder externe Nebenprojekte können nur integriert werden, wenn ihre Quellen tatsächlich wiedergewonnen werden;
- historische Literaturangaben bleiben dann quarantänisiert, wenn ihre Primärquelle nicht erneut geprüft wurde;
- Raw DATA werden absichtlich nicht in den Manuskripttext dupliziert, sondern bleiben an ihren Experimentpfad gebunden.

Das Ziel lautet daher nicht „jeder Bytewert steht im Manuskript“, sondern: **jede bekannte wissenschaftlich materielle Vorarbeit hat eine nachvollziehbare Rolle in der Gesamtarbeit, während Primärartefakte an ihrem autoritativen Ort erhalten bleiben.**

## 58.2 Topologie v2 abgeschlossen; Review, Replikation und 5D-Prüfung getrennt

Für `RQ-DET-001` bleibt ein clean-tree-Replikationslauf erforderlich, bevor ein durch Dirty-Tree-Provenienz blockiertes Artefakt regulär in Richtung EVID geprüft werden kann. Eine semantische Reklassifikation allein entfernt den Provenienzblock nicht.

Für `RQ-SNN-003 / H-SNN-003-B` liegen inzwischen zwei gültige source-bound DATA-Linien vor. `EXP-S1-TOPO-V2-20260918` etablierte den ersten präregistrierten 64-Neuronen-/246-Kanten-Befund. Die korrigierte interne Replikation `EXP-S1-TOPO-V3-R1-20260918` verwendet neue Seeds und prospektive zeitaufgelöste Endpunkte: sie löst die terminale `active_fraction`-Sättigung für 1d/2d/3d auf und repliziert alle fünf First-Output-Latenzrichtungen aus V2. Ein erster V3-Lauf bleibt als Auditspur erhalten, wird wegen einer falsch implementierten Holm-Familie aber nicht konfirmatorisch interpretiert. Der Status der gültigen Linien bleibt `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL` auf DATA-Ebene. Die Human Reviews durch Thomas Heisig sind inzwischen abgeschlossen; EVID-Promotion und unabhängige Replikation bleiben getrennt offen.

Der nächste Schritt für `H-SNN-003-B` ist jetzt **keine weitere interne Wiederholung derselben Pipeline**, sondern ein separat definierter scoped Claim mit prospektiv EvidenceEngine-kompatiblem Promotion-Pfad sowie anschließend eine unabhängig implementierte Replikation oder ein bewusst erweitertes Operating-Envelope.

Für die **dimensionsspezifische** Registry-Frage gilt parallel unverändert: `RQ-5D-005` bleibt `open` und `H-5D-005-A` bleibt kanonisch `untested`. Das 64-Neuronen-Stage-1-Experiment ist dafür kein hinreichender Nachweis. Die nächste 5D-Prüfung muss mindestens **1.000 Neuronen pro Bedingung**, durchschnittlich **mindestens 10 eingehende Synapsen pro Neuron** und eine **explizit distanzabhängige Konnektivitätswahrscheinlichkeit** verwenden; Delay darf zusätzlich geometrieabhängig sein. Degree-/density-matched Kontrollen, Multi-Neuron-Stimulus, Activity-Adequacy-Gate, unabhängige Seeds und clean-tree Provenienz bleiben verpflichtend.

## 58.3 LP-20260917194217: offene Kompressionsprüfung

`LP-20260917194217 / OBJ-MEM-COMPRESSION-001` ist der **nächste vorbereitete empirische Stage-6-Zyklus**, aber noch nicht ausgeführt. Der geplante Primärvergleich ist `semantic_prototype_replay_10pct_budget` gegen `raw_replay_full_budget`; die Erfolgsgrenze liegt bei mindestens 95 % der Raw-Replay-Retention bei Faktor-10-Speicherreduktion. `no_replay`, `random_prototype_10pct` und `learning_off` dienen als Kontrollen. Die Frage betrifft damit **Speicherkompression bei erhaltener Retention**, nicht eine erneute allgemeine Lernleistungsbehauptung.

Die konkrete Quellbindung liegt inzwischen in `LP-20260917194217-R1` vor. Diese Revision ist noch **nicht erneut human-approved**; die Approval des Originalplans wird nicht auf geänderten Proposal-Inhalt übertragen. Der nächste methodische Schritt ist deshalb die **Präregistrierungsvorbereitung** mit kanonischer RQ/H-Bindung, exakter Speicherbudget-Definition, Seed-/Taskplan, Retentionsaggregation, vorab fixierter Inferenz-/Äquivalenzregel, Ausschlüssen/Failure-Regeln und Analysevertrag. Vor einem ausführungsfähigen Freeze bleiben R1-Human-Approval und eine separate Ausführungsautorisation erforderlich.

Die Entscheidung ist prospektiv begrenzt: Ein positives Ergebnis stützt eine **Kompressionsrolle** von SemanticMemory unter dem registrierten Protokoll. Ein negatives Ergebnis beantwortet diese Kompressionsrolle für den getesteten Mechanismus negativ; Generalisierung, Langzeitgedächtnis oder Weltmodell-Brücke bleiben dann mögliche, aber **separat zu präregistrierende** Rollen und dürfen den Kompressionstest nicht post hoc umdeuten.

## 58.4 Aktueller Review-Stand und unmittelbar nächste Replikationen

Nach dem jüngsten Human Review ist die offene Determinismusfrage enger als zuvor. `RQ-DET-001 / H-SNN-003-A` hat im historischen `deterministic_replica_v1`-Datensatz einen positiven Same-Seed-Replica-Befund und ist semantisch `DIRECT_MATCH`. Offen ist nicht mehr die Frage, ob die registrierten Replica-Bedingungen zur RQ gehören, sondern ob derselbe Befund in einem **clean-tree, hash-gebundenen Replikationslauf** wiederholt wird. Erst danach ist eine reguläre Human-EVID-Entscheidung sinnvoll.

Für `H-SNN-003-B` sind die Human Reviews der V2/R1-DATA-Linie abgeschlossen. Der nächste Schritt ist nun **separate EVID-Promotion unter aktuellem Vertrag und unabhängige Replikation**. `EXP-GEN-0047` bleibt als inadäquater Vorgänger erhalten; die neue DATA darf ihn nicht rückwirkend umdeuten. Die ≥1.000-Neuronen-/≥10-In-Degree-Schwellen werden ausschließlich für die stärkere `H-5D-005-A`-Prüfung geführt.

Damit sind die nächsten methodischen Schritte **Review/Replikation für den Stage-1-Topologiebefund** und **Testadäquanz für den separaten 5D-Claim**.

## 59. Forschungsagenda und Abschlusskriterien der Teilstudien

Die offene Forschungslandschaft wird für die weitere Arbeit nicht als unsortierte TODO-Liste behandelt. Jeder Hauptzweig erhält ein **wissenschaftliches Abschlusskriterium**, das festlegt, welche nächste Evidenz tatsächlich nötig ist, bevor eine stärkere Aussage zulässig wird.

| Teilstudie | Nächster entscheidender Prüfpunkt | Kriterium für stärkere Aussage |
| --- | --- | --- |
| **Basale Dynamik / Determinismus** | clean-tree, hash-gebundene Same-Seed-Replikation und externe Wiederholung | Reproduzierbarkeit muss über denselben internen Workflow hinaus bestätigt werden |
| **Rekurrenz** | unabhängige Seeds, skalierte Netzwerke und klar getrennte Rekurrenzintervention | Effekt muss unter erweitertem Operating Envelope bestehen |
| **Topologie / H-SNN-003-B** | scoped Claim + prospektiver EvidenceEngine-kompatibler Promotion-Pfad; danach unabhängig implementierte Replikation | Der human-reviewte, intern replizierte Stage-1-Topologiebefund muss kanonisch EVID-eligible werden und außerhalb derselben Code-/Ausführungslinie reproduzierbar bleiben |
| **5D / H-5D-005-A** | separates präregistriertes Design mit ≥1.000 Neuronen, ≥10 Inputs/Neuron und distanzabhängiger Geometrie-Dynamik-Kopplung | Ein dimensionsspezifischer Effekt muss unter gematchten Ressourcen- und Graphkontrollen bestehen |
| **Plastizität** | learning-on/off-, Sham-/Frozen- und Holdout-Designs mit unabhängigen Seeds | Gewichtsänderung muss einen funktionalen Lern-/Stabilitätsbeitrag gegenüber Kontrollen tragen |
| **MSBA / spezialisierte Pfade** | kausale Ressourcen- und Lesionsexperimente unter streng gematchten Budgets | Spezialpfad muss über bloße Implementierbarkeit hinaus messbaren Zusatznutzen zeigen |
| **Embodiment** | `H-EMB-001-B`: identische externe Störung, Closed Loop vs. yoked Replay vs. interrupted feedback | Feedback muss unter matched disturbance einen kausalen Vorteil zeigen |
| **SemanticMemory / Kompression** | neue Human Approval und Präregistrierung für `OBJ-MEM-COMPRESSION-001` | 10%-Budget erreicht die vorab definierte Retentionsgrenze gegenüber Full Raw Replay |
| **Weltmodell** | action-conditioned Mehrschrittvorhersage gegen reactive/no-model/corrupted-model | Modellinformation muss einen kausalen Entscheidungsnutzen liefern |
| **Selbstmodell** | interventionelle Self/Other-Manipulationen | Selbstmodell muss funktional mehr leisten als Profil-/Metadatenidentität |
| **Rekursive Epistemik** | Meta-Metriken zu Fehlklassifikationen, Statussprüngen und Revisionsqualität | Governance muss messbar bessere Forschungsentscheidungen erzeugen oder gegenüber einfacherer Alternative bestehen |
| **Safety / Ethik** | operationalisierte Zielprovenienz-, Interruptibility- und Welfare-Gates | normative Regeln müssen technisch anschlussfähig und unter Gegenfällen revidierbar sein |

### Priorisierungsregel

Die Reihenfolge weiterer Forschung folgt nicht der visuellen Stage-Nummer, sondern dem wissenschaftlichen Informationsgewinn. Vorrang haben Experimente, die einen zentralen offenen Claim entscheiden, einen bekannten Confound beseitigen oder eine Architekturentscheidung irreversibel vereinfachen können.

Daraus folgen gegenwärtig vier priorisierte Linien:

1. **Präregistrierung von `OBJ-MEM-COMPRESSION-001`**, weil sie eine klar falsifizierbare Anschlussfrage an die negative CL-002/003-Linie darstellt.
2. **Scoped Stage-1-Claim und prospektiven EvidenceEngine-kompatiblen Promotion-Pfad definieren, anschließend unabhängig replizieren**, weil die Human Reviews von V2 und V3-R1 bereits abgeschlossen sind, die historische DATA-Linie aber den heutigen Promotionsvertrag nicht erfüllt.
3. **separate `H-5D-005-A`-Präregistrierung**, weil der 64-Neuronen-Topologiebefund keinen 5D-Vorteil beantwortet.
4. **clean-tree Determinismusreplikation**, weil vorhandene positive Same-Seed-Befunde durch Provenienzgrenzen blockiert sind.
5. **`H-EMB-001-B`**, weil erst der matched-disturbance-Vergleich den Closed-Loop-Mechanismus stärker kausal isoliert.

### Abschlusscharakter

Eine spätere kanonische Hauptfassung darf keinen Zweig allein deshalb als „abgeschlossen“ markieren, weil Code, UI oder Dokumentation vollständig sind. Abschluss bedeutet in dieser Arbeit entweder:

- eine Hypothese wurde unter adäquatem Design gestützt oder falsifiziert;
- der Geltungsbereich wurde durch ein negatives Resultat belastbar begrenzt;
- oder die Frage bleibt ausdrücklich offen, weil die notwendige Evidenz noch fehlt.

Gerade diese dritte Möglichkeit gehört zum wissenschaftlichen Charakter der Arbeit. Eine Dissertation oder Monographie wird nicht dadurch stärker, dass jede Frage beantwortet erscheint, sondern dadurch, dass beantwortete, widerlegte und noch offene Fragen methodisch unterscheidbar bleiben.


---

# Anhang — Quellen und Vorarbeiten

[Alle Forschungsfragen und Hypothesen](RESEARCH_REGISTER.md) · [Quellenindex](SOURCE_INDEX.md) · [Semantische Corpus-Integration](CONTENT_INTEGRATION.md) · [Ungekürzter Quellenband 1.7](LEGACY_V17.md) · [Weitere Vorarbeiten](PRIOR_WORK_MAP.md) · [Literatur](REFERENCES.md) · [Prüfmanifest](manifest.json).

Die Quellenbestandsaufnahme belegt referenzierte Datei-Erhaltung am angegebenen Commit, nicht die vollständige semantische Erfassung jeder Idee. Die außerhalb des Repositories rekonstruierte Vorgeschichte ist ausdrücklich unvollständig.
