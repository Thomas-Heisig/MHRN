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

Die 1.8-Fassung setzt nicht mit einem vermeintlich fertigen MHRN an. Sie behandelt die Entstehung selbst als Forschungsgegenstand. Die **früheste derzeit rekonstruierte Spur** ist `CER-RECON-20250421-01` in der [Chat-Rekonstruktion](../sources/chat_reconstruction.json): ein lernender neuronaler Würfel sollte Zustand über Neustarts hinweg erhalten; nachladbare Funktionen sollten den lernenden Kern nicht unkontrolliert verändern. `CER-RECON-20250421-02` dokumentiert als weitere S4-Rekonstruktion Schichten, dynamische Verbindungen, Mutation sowie historische Traum-/Fantasie-Metaphern. `CER-RECON-20250421-03` trennt davon einen früheren KI-Vorschlag zu Koordinatenkodierung und SQLite-Speicher.

Diese Einträge gehören zur **Quellennäheklasse S4**: rekonstruierte Gesprächszusammenfassungen ohne vollständiges Originaltranskript. Sie belegen weder den tatsächlichen ersten Gedanken noch wissenschaftliche Priorität, Implementierung oder Funktionsnachweis. Die gleiche Grenze ist im Vorgängerwerk `PW-NEUROGENESIS-2025` des [Prior-Work-Registers](../sources/prior_work.json) festgeschrieben.

Der historische Wert liegt deshalb nicht in einer Prioritätsbehauptung, sondern in der Problemkontinuität: Wie kann ein System Zustand behalten, ohne ein Sprachmodell oder eine Datenbank fälschlich als neuronales Gedächtnis zu zählen? Wie lässt sich Wachstum zulassen, ohne die Kausalität zu verlieren? Wie kann ein technisches System zugleich offen erweiterbar und wissenschaftlich prüfbar bleiben? Diese Fragen erscheinen später in strengeren Formen wieder: als Persistenzvertrag, Retrieval-Isolation, strukturelle Plastizität, Capability-Gates, Experimentregister und Evidenzgrenzen.

## 2. Autorposition

Thomas Heisig wird in dieser Arbeit als Autor, Projektleiter und wissenschaftlich verantwortliche natürliche Person geführt. KI-Systeme können Recherche-, Kritik-, Generierungs-, Analyse-, Programmier- und Formulierungsbeiträge leisten. **Ob ein konkreter KI-Beitrag epistemisch materiell ist, ist von formaler Autorenschaft, Entscheidungsmacht und wissenschaftlicher Verantwortung getrennt zu beurteilen.** Genau diese Trennung ist Gegenstand von `RQ-ETH-001` und des [Provenienz- und Beitragsprotokolls](../../../protocols/RQ_ETH_001_PROVENANCE_STUDY.md).

Damit gilt ausdrücklich nicht mehr die vereinfachende Gleichung „KI = bloßes Werkzeug“. Ein Assistenzsystem kann beispielsweise eine Kontrollbedingung, einen methodischen Einwand oder eine Hypothesenvariante erzeugen, die den weiteren Forschungsweg materiell verändert. Daraus folgt jedoch weder automatische Quellenautorität noch formale wissenschaftliche Autorenschaft oder Verantwortung.

Die Selbstauskunft des Autors ist eine Primärquelle für Motivation und Arbeitsweise, jedoch keine empirische Evidenz über neuronale Mechanismen. Persönliche Intuition kann Forschungsfragen erzeugen; sie darf keine Hypothese bestätigen. Die vollständige Selbstauskunft bleibt als versioniertes Provenienzartefakt in [`AUTHOR_AND_CREATION_PRACTICE.md`](../../2026-09-15_recursive-epistemics_v1.7/AUTHOR_AND_CREATION_PRACTICE.md) erhalten und wird im Hauptmanuskript nur soweit zusammengefasst, wie sie die wissenschaftliche Methode betrifft.

### 2.1 Autorenschaft, Beitragsrollen und KI-Offenlegung

**Autor und wissenschaftlich verantwortliche Person dieser Edition ist Thomas Heisig.** Autorenschaft bedeutet hier nicht nur Namensnennung, sondern Verantwortung für Auswahl, Prüfung, Interpretation, Begrenzung und Veröffentlichung wissenschaftlicher Aussagen. Externe Publikationsrichtlinien verbinden Autorenschaft ebenfalls mit Verantwortlichkeit und Rechenschaftspflicht; AI-Systeme werden deshalb nicht als Autoren geführt, weil sie diese Verantwortung nicht übernehmen können ([@ICMJE2026]).

Für die transparente Beschreibung menschlicher Beiträge wird ergänzend die CRediT-Taxonomie verwendet; sie beschreibt Beitragsrollen, entscheidet aber nicht selbst darüber, wer Autor ist ([@CREDIT2022]). Für Thomas Heisig werden in Edition 1.8 derzeit folgende Rollen ausgewiesen: **Conceptualization, Methodology, Software, Investigation, Data curation, Formal analysis, Validation, Visualization, Project administration, Writing – original draft sowie Writing – review & editing**.

Für KI-Systeme wird dagegen zwischen **Beitragsprovenienz** und **Autorschaft** unterschieden. Ein KI-System kann einen materiellen Beitrag zu Konzeptualisierung, Generierung/Transformation, Analyse oder Validierung leisten. Die Annahme, Revision, Verwerfung oder Kanonisierung einer wissenschaftlichen Aussage sowie die formale Verantwortung bleiben davon getrennt. Diese Unterscheidung wird in `RQ-ETH-001` mit Claim-Episoden und einer Contribution-&-Accountability-Matrix operationalisiert.

Literaturangaben, Tatsachenbehauptungen und daraus abgeleitete wissenschaftliche Aussagen bleiben in menschlicher Verantwortung; bei einer externen Einreichung muss die konkrete Nutzung von AI-Werkzeugen zusätzlich nach den Regeln des Zieljournals offengelegt werden ([@ICMJE2026]).

Die wissenschaftliche Textschicht verwendet ein Autor-Jahr-System nach **APA 7** ([@APA2020]). Primärliteratur wird für ursprüngliche empirische, methodische oder theoretische Befunde bevorzugt; Sekundärliteratur wird dort verwendet und als solche ausgewiesen, wo Review, Survey oder Synthese die Einordnung trägt.

## 3. Von Metaphern zu Operationen

Frühe Begriffe wie „DNA“, „Traum“, „Fantasie“, „Emotion“ oder „Gehirn“ werden historisch erhalten, aber nicht rückwirkend biologisch aufgeladen. Die S4-Rekonstruktion `CER-RECON-20250421-02` belegt ihre Verwendung als frühe Designmetaphern, nicht als biologische oder phänomenale Befunde. In der heutigen Terminologie werden solche Begriffe nur dann verwendet, wenn eine messbare technische Entsprechung definiert ist.

Offline-Replay ist nicht Schlaf. Ein Aktivierungs- oder Salienzparameter ist kein Gefühl. Parametervererbung ist keine biologische Genetik. Eine adressierte 5D-Struktur ist kein anatomisches Gehirn.

Diese Entmetaphorisierung ist kein Verlust der ursprünglichen Ideen. Sie macht sie prüfbar. Der Weg von einer anschaulichen Analogie zu einer operationalisierten Variable wird als Teil der Schaffensgeschichte dokumentiert, damit spätere Leser unterscheiden können, was Inspiration, Spezifikation, Implementierung, Messung und Interpretation war.

## 4. Nullpunkt und rekonstruierte Vorgeschichte

Edition 1.8 behauptet keinen exakt datierten „ersten Gedanken“. Für Zeiträume außerhalb des Git-Verlaufs stehen teilweise nur rekonstruierte Gesprächszusammenfassungen oder später wiedergefundene Dokumente zur Verfügung. Die [Chat-Rekonstruktion](../sources/chat_reconstruction.json) führt diese Einträge in der **Quellennäheklasse S4**, solange kein originales, datiertes Primärartefakt geprüft wurde. Wo Originalnachrichten oder Originaldateien fehlen, lautet die wissenschaftlich korrekte Aussage „rekonstruiert“ oder „nicht rekonstruierbar“, nicht eine erfundene Präzision.

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

Das `PW-FRAMEWORK-02` zugeordnete **Brain-5D Scientific Framework v0.2** vom 16. August 2026 verdichtete die frühe Ideenlandschaft zu einem expliziteren wissenschaftlichen Programm. Das [Prior-Work-Register](../sources/prior_work.json) hält zugleich fest, dass der im Repository sichtbare DOCX-Pfad als LFS-Objekt behandelt wird und historische Evidenzklassen nicht automatisch in heutige `EVID`-Entscheidungen überführt werden.

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

Die kanonische Selbstauskunft [`AUTHOR_AND_CREATION_PRACTICE.md`](../../2026-09-15_recursive-epistemics_v1.7/AUTHOR_AND_CREATION_PRACTICE.md) beschreibt einen stark parallelen, werkstattartigen Arbeitsmodus: Problem sichtbar machen, Randbedingungen benennen, Mechanismus isolieren, einen testbaren Eingriff definieren, ausführen, messen, Abweichungen dokumentieren und erst danach verallgemeinern. Sie dokumentiert zugleich einen selbst beschriebenen Abschluss- und Ordnungsdrang. Beides ist **Selbstauskunft**, keine unabhängige psychologische oder wissenschaftliche Evidenz.

Methodisch relevant ist das daraus abgeleitete Risiko: **Struktur lässt sich schneller schließen als Empirie.** Technisch vollständige Module, UI-Zustände oder plausible Architekturen können einen Reifegrad suggerieren, den die experimentelle Prüfung noch nicht trägt.

Die Antwort darauf ist eine methodische Selbstkorrektur: Engineering-Fertigstellung und Scientific Readiness werden getrennt; negative und Nullbefunde dürfen Architektur reduzieren; UI-Prozentwerte sind keine Fähigkeitsscores; eine neue Funktion erhält keinen wissenschaftlichen Status allein durch Integration. Die konkreten Fälle und aktuellen Evidenzstände werden nicht in Teil I fortgeschrieben, sondern in Teil IV, X und XI geführt.

### 4.4 Mensch-KI-Zusammenarbeit als reale Entstehungsbedingung

MHRN ist in einer Arbeitsweise entstanden, in der menschliche Zielsetzung, mehrere KI-Assistenten, Literaturrecherche, Codegenerierung, Review, Tests und Git-Provenienz eng verschränkt sind. Diese Konstellation wird nicht geglättet. Seit der Verdichtung von `RQ-ETH-001` wird sie nicht mehr nur als „Mensch plus Werkzeuge“, sondern als Folge unterscheidbarer epistemischer Ereignisse beschrieben:

- **Konzeptualisierung:** Wer erzeugt oder verändert Forschungsfrage, Ziel, Hypothese oder Erfolgsbedingung?
- **Generierung/Transformation:** Wer erzeugt Text, Code, Analyse, Kontrollidee oder methodische Variante?
- **Validierung:** Wer oder was prüft Quelle, Code, Messung, Statistik oder Konsistenz?
- **Selektion/Kanonisierung:** Wer entscheidet, was übernommen, revidiert, verworfen, als `DATA`/`EVID` behandelt oder veröffentlicht wird?
- **Verantwortung:** Welche natürliche Person kann für die veröffentlichte Aussage wissenschaftlich Rechenschaft übernehmen?

Die operative Einheit dafür ist die **Claim-Episode**. Commits, Runs, Reviews und Freigaben sind dabei Provenienzartefakte innerhalb einer Episode, aber nicht mit epistemischer Rolle oder Autorenschaft gleichzusetzen. Das Design ist in [`RQ_ETH_001_PROVENANCE_STUDY.md`](../../../protocols/RQ_ETH_001_PROVENANCE_STUDY.md) festgelegt; es ist derzeit Protokolldesign und kein bestätigter empirischer Befund.

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

Beide Formulierungen bleiben über die [Vorgängerfassung 1.5](../../2026-09-13_recursive-epistemics_v1.5/section-005.md) provenancegebunden erhalten. Sie sind **historische Forschungsrahmen**, keine aktuelle pauschale `EVID` und keine zusätzlichen heutigen Registryobjekte. Edition 1.8 zerlegt ihren Inhalt in engere, falsifizierbare Forschungszweige zu Dynamik, Topologie, Plastizität, Repräsentation, Gedächtnis, Embodiment, Attribution und Skalierung.

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
