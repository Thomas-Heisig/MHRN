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

Die 1.8-Fassung setzt nicht mit einem vermeintlich fertigen MHRN an. Sie behandelt die Entstehung selbst als Forschungsgegenstand. Die frühesten in dieser Revision wiedergewonnenen Spuren stammen aus Gesprächen über einen persistenten neuronalen Würfel, dynamische Verbindungen, entwicklungsähnliche Schichten, Mutation, Speicherung über Neustarts hinweg und die Trennung zwischen einem lernenden Kern und nachladbaren Funktionen. Diese Spuren werden als **rekonstruierte Vorphase** geführt. Sie belegen weder, dass dies die erste Idee überhaupt war, noch dass die beschriebenen Mechanismen damals schon implementiert waren.

Der historische Wert liegt in der Problemkontinuität: Wie kann ein System Wissen behalten, ohne dass ein externes Sprachmodell oder eine Datenbank fälschlich als neuronales Gedächtnis gezählt wird? Wie lässt sich Wachstum zulassen, ohne die Kausalität zu verlieren? Wie kann ein technisches System zugleich offen erweiterbar und wissenschaftlich prüfbar bleiben? Diese Fragen erscheinen später in deutlich strengeren Formen wieder: als Persistenzvertrag, Retrieval-Isolation, strukturelle Plastizität, Capability-Gates, Experimentregister und Evidenzgrenzen.

## 2. Autorposition

Thomas Heisig wird in dieser Arbeit als Autor und Projektleiter geführt. KI-Systeme sind als Recherche-, Synthese-, Kritik-, Programmier- und Formulierungswerkzeuge dokumentiert, erhalten aber keine automatische Quellen- oder Autoritätsrolle. Entscheidend ist nicht, ob ein Satz mit menschlicher oder maschineller Hilfe formuliert wurde, sondern ob seine Herkunft, seine Prüfgrundlage und seine Entscheidungskette nachvollziehbar sind.

Die Selbstauskunft des Autors ist eine Primärquelle für Motivation und Arbeitsweise, jedoch keine empirische Evidenz über neuronale Mechanismen. Persönliche Intuition kann Forschungsfragen erzeugen; sie darf keine Hypothese bestätigen. Umgekehrt wird die ungewöhnlich enge Mensch-KI-Arbeit nicht versteckt. Sie ist selbst Teil der epistemologischen Fragestellung dieser Arbeit: Was bedeutet Autorschaft, wenn externe kognitive Werkzeuge permanent an Suche, Gegenargument, Implementierung und Text beteiligt sind?

### 2.1 Autorenschaft, Beitragsrollen und KI-Offenlegung

**Autor und wissenschaftlich verantwortliche Person dieser Edition ist Thomas Heisig.** Autorenschaft bedeutet hier nicht nur Namensnennung, sondern Verantwortung für Auswahl, Prüfung, Interpretation und Begrenzung der veröffentlichten Aussagen. Externe Publikationsrichtlinien verbinden Autorenschaft ebenfalls mit Verantwortlichkeit und Rechenschaftspflicht; AI-Systeme werden deshalb nicht als Autoren geführt, weil sie diese Verantwortung nicht übernehmen können ([@ICMJE2026]).

Für die transparente Beschreibung menschlicher Beiträge wird ergänzend die CRediT-Taxonomie verwendet; sie beschreibt Beitragsrollen, entscheidet aber nicht selbst darüber, wer Autor ist ([@CREDIT2022]). Für Thomas Heisig werden in Edition 1.8 derzeit folgende Rollen ausgewiesen: **Conceptualization, Methodology, Software, Investigation, Data curation, Formal analysis, Validation, Visualization, Project administration, Writing – original draft sowie Writing – review & editing**.

KI-Systeme werden als Recherche-, Synthese-, Kritik-, Programmier- und Formulierungswerkzeuge offengelegt, nicht als Primärquelle, Autor oder Evidenzinstanz. Literaturangaben, Tatsachenbehauptungen und daraus abgeleitete wissenschaftliche Aussagen bleiben in menschlicher Verantwortung; bei einer externen Einreichung muss die konkrete Nutzung von AI-Werkzeugen zusätzlich nach den Regeln des Zieljournals offengelegt werden ([@ICMJE2026]).

Die wissenschaftliche Textschicht verwendet ein Autor-Jahr-System nach **APA 7** ([@APA2020]). Primärliteratur wird für ursprüngliche empirische, methodische oder theoretische Befunde bevorzugt; Sekundärliteratur wird dort verwendet und als solche ausgewiesen, wo Review, Survey oder Synthese die Einordnung trägt.

## 3. Von Metaphern zu Operationen

Frühe Begriffe wie „DNA“, „Traum“, „Fantasie“, „Emotion“ oder „Gehirn“ werden historisch erhalten, aber nicht rückwirkend biologisch aufgeladen. In der heutigen Terminologie werden sie nur dann verwendet, wenn eine messbare technische Entsprechung definiert ist. Offline-Replay ist nicht Schlaf. Ein Aktivierungs- oder Salienzparameter ist kein Gefühl. Parametervererbung ist keine biologische Genetik. Eine adressierte 5D-Struktur ist kein anatomisches Gehirn.

Diese Entmetaphorisierung ist kein Verlust der ursprünglichen Ideen. Sie macht sie testbar. Der Weg von einer anschaulichen Analogie zu einer operationalisierten Variable wird als Teil der Schaffensgeschichte dokumentiert, damit spätere Leser unterscheiden können, was Inspiration, was Spezifikation, was Implementierung und was tatsächlich gemessener Befund war.

## 4. Nullpunkt als offene Grenze

Edition 1.8 behauptet keinen exakt datierten „ersten Gedanken“. Für Zeiträume außerhalb des Git-Verlaufs stehen teilweise nur Zusammenfassungen früherer Chats oder später wiedergefundene Dokumente zur Verfügung. Diese werden mit Provenienzklasse S4 gekennzeichnet. Wo Originalnachrichten oder Originaldateien fehlen, lautet die wissenschaftlich korrekte Aussage „rekonstruiert“ oder „nicht rekonstruierbar“, nicht eine erfundene Präzision.

Damit ist Teil I bewusst erweiterbar. Neue Primärartefakte können die Chronologie verdichten oder korrigieren. Sie dürfen aber nicht stillschweigend bestehende Versionen überschreiben. Jede neue historische Zuordnung braucht Quelle, Datum beziehungsweise Datumsunsicherheit und eine Aussage darüber, ob sie Autoranforderung, KI-Vorschlag, Implementierung, Messung oder spätere Interpretation dokumentiert.

## 4.1 Die ursprüngliche Problemfamilie

Die rekonstruierten Vorarbeiten zeigen keine einzelne „Ur-Idee“, sondern eine wiederkehrende Problemfamilie. Schon vor dem heutigen MHRN standen sechs Fragen nebeneinander:

1. Wie kann ein neuronales System **über Neustarts hinweg** einen wissenschaftlich definierten Zustand behalten?
2. Wie kann ein Netzwerk **wachsen, sich verbinden und verändern**, ohne dass der Veränderungspfad unprüfbar wird?
3. Wie lassen sich **räumliche oder funktionale Nachbarschaften** so repräsentieren, dass daraus später experimentierbare Geometrie entsteht?
4. Wie kann externe Software — Datenbank, Sprache, Plugin, Werkzeug — genutzt werden, ohne sie fälschlich als **intern gelerntes neuronales Wissen** auszugeben?
5. Wie können Offline-Phasen, Replay und Rekombination genutzt werden, ohne Metaphern wie „Traum“ oder „Fantasie“ als empirische Tatsachen zu behandeln?
6. Wie kann ein System modular erweiterbar bleiben, ohne dass jedes neue Modul automatisch Schreibrechte auf den kausalen Lernkern erhält?

Diese Kontinuität erklärt einen großen Teil der späteren Architektur. Die heutige Trennung von Content Gateway, Compute Backend, neuronaler Persistenz, Retrieval-Isolation, Capability-Gates und struktureller Mutation ist keine nachträgliche ästhetische Ordnung. Sie ist eine Antwort auf Mehrdeutigkeiten, die bereits in der Vorphase sichtbar waren.

## 4.2 Aus Brain-5D übernommene Forschungsräume

Das Brain-5D Scientific Framework v0.2 verdichtete die frühe Ideenlandschaft zu einem expliziteren wissenschaftlichen Programm. Darin tauchten bereits mehrere Forschungsräume auf, die bis heute fortwirken:

- mehrdimensionale Adress- und Geometriehypothesen;
- unterschiedliche Neuronmodelle und Zeitskalen;
- STDP, Eligibility, Drei-Faktor-Lernen, Homeostase und strukturelle Plastizität;
- Graphnullmodelle, Motive, Stabilität, Metastabilität und kritische Dynamik;
- Information, Decoding, Representational Similarity und temporale Generalisierung;
- Gedächtnis, Continual Learning, Replay, Vorhersage und Language Organ;
- Storage, digitaler Zustand, Embodiment, Safety und Ressourcenskalierung.

Edition 1.8 übernimmt diese Räume nicht als bereits bestätigte Theorie. Sie übernimmt sie als **Genealogie der Forschungsfragen**. Mehrere Begriffe wurden inzwischen eingeengt: „5D“ ist keine Naturbehauptung; „Digital Twin“ ist ohne physisches Gegenstück primär ein reproduzierbarer digitaler Zustand; „Language Organ“ ist kein autoritativer Lernkern; „Homeostase“ ist eine technische Regelklasse, solange biologische Homologie nicht gezeigt wurde.

## 4.3 Die Schaffensart als methodischer Risikofaktor

Die kanonische Selbstauskunft des Autors beschreibt einen stark parallelen, werkstattartigen Arbeitsmodus: Problem sichtbar machen, Randbedingungen benennen, Mechanismus isolieren, Eingriff definieren, ausführen, messen, Fehler dokumentieren, erst danach verallgemeinern. Dieser Modus hat die hohe Entwicklungsgeschwindigkeit ermöglicht, erzeugt aber ein spezifisches Risiko: **Struktur lässt sich schneller schließen als Empirie.**

Genau dieses Risiko ist in den Vorgängerarbeiten mehrfach sichtbar geworden. Ein technisch sauber gebautes Modul konnte im Frontend bereits vollständig erscheinen, obwohl seine wissenschaftliche Rolle erst teilweise geprüft war. Ein plausibles Semantikmodul konnte zentral wirken, bevor Raw-Replay als stärkere Kontrolle eingeführt wurde. Eine 5D-Bedingung konnte formal existieren, obwohl die Dynamik nicht ausreichend an die Geometrie gekoppelt war.

Aus diesen Erfahrungen entstand eine methodische Selbstkorrektur: Engineering-Fertigstellung und Scientific Readiness werden getrennt; negative Ergebnisse dürfen Architektur reduzieren; UI-Prozentwerte sind keine Fähigkeitsscores; und eine neue Funktion erhält keinen wissenschaftlichen Status allein durch Integration.

## 4.4 Mensch-KI-Zusammenarbeit als reale Entstehungsbedingung

MHRN ist in einer Arbeitsweise entstanden, in der menschliche Zielsetzung, mehrere KI-Assistenten, Literaturrecherche, Codegenerierung, Review, Tests und Git-Provenienz eng verschränkt sind. Diese Konstellation wird nicht geglättet. Für die Entstehungsgeschichte ist gerade wichtig, zwischen unterschiedlichen Beitragsarten zu unterscheiden:

- **Autoranforderung:** welche Richtung, Grenze oder Funktion der Mensch verlangt;
- **KI-Vorschlag:** welche Lösung, Formulierung oder Hypothese ein Assistenzsystem anbietet;
- **menschliche Entscheidung:** welche Variante angenommen, verändert oder verworfen wird;
- **Commit:** was tatsächlich implementiert und versioniert wurde;
- **Run/DATA:** was tatsächlich ausgeführt und gemessen wurde;
- **Review:** welche Interpretation anschließend akzeptiert, eingeschränkt oder verworfen wurde.

Diese Kette ist ein Teil der späteren Theorie rekursiver Epistemik. Die Arbeit untersucht nicht nur ein lernendes System; sie entsteht selbst in einem System aus Quellen, Werkzeugen, Reviews, Entscheidungen und Statusänderungen.

## 4.5 Persönliche Motivation und ihre wissenschaftliche Grenze

Die Vorgängerfassung dokumentiert die persönliche Motivation des Autors als Mischung aus technischer Praxis, starkem Ordnungs- und Abschlussdrang sowie langfristigem Interesse an kognitiven Systemen und deren Veränderungen. Diese Motivation ist epistemisch relevant, weil sie erklärt, warum bestimmte Fragen verfolgt werden. Sie besitzt jedoch keine Beweiskraft für deren Antwort.

Die verbindliche Regel lautet deshalb: **Nähe erzeugt Fragen, nicht Antworten.** Persönliche Erfahrung, handwerkliche Systemintuition oder interdisziplinäre Analogien dürfen einen Suchraum öffnen; sie ersetzen weder neurowissenschaftliche Fachliteratur noch Statistik, Replikation, Ethikprüfung oder Peer Review.

Gerade weil MHRN außerhalb institutioneller Forschungsstrukturen entstanden ist, muss die Arbeit ihre Grenzen expliziter machen: Was ist Selbstbeschreibung? Was ist externe Theorie? Was ist implementierter Mechanismus? Was ist DATA? Was wurde menschlich reviewt? Was ist noch offen? Diese Trennung ist nicht nur Dokumentationsstil, sondern ein Kompensationsmechanismus für fehlende institutionelle Selbstverständlichkeit.

## 4.6 Forschungsproblem, Leitfrage und dissertationsähnliche Gesamtarchitektur

Edition 1.8 versteht sich als wissenschaftliche Monographie im Work-in-Progress-Status. Sie ist **keine eingereichte Dissertation und kein akademischer Gradanspruch**, übernimmt aber bewusst eine dissertationsähnliche Forschungslogik: Problemstellung, Forschungsstand, Forschungslücke, Leitfrage, Teilfragen, Methodik, Ergebnisse, Diskussion, Limitationen und revidierbare Schlussfolgerungen werden sichtbar getrennt.

### Übergeordnetes Forschungsproblem

Das Grundproblem dieser Arbeit ist nicht allein der Bau eines größeren spikenden Systems. Es lautet: **Wie kann eine modular wachsende, verkörperbare spikende Architektur so untersucht werden, dass technische Existenz, kausaler Mechanismus, empirischer Nutzen, Provenienz und normative Reichweite nicht miteinander verwechselt werden?**

Aus der bisherigen Schaffensgeschichte folgt eine zweite Ebene des Problems: Das Forschungsobjekt verändert sich während seiner Untersuchung. Neue Module können Hypothesen erzeugen, negative Resultate können Architektur reduzieren, KI-Werkzeuge können Recherche und Implementierung beschleunigen, und die Dokumentation selbst beeinflusst spätere Entscheidungen. Deshalb muss nicht nur das System, sondern auch der Forschungsprozess kontrollierbar und revidierbar sein.

### Zentrale Leitfrage

> **Wie lässt sich eine evolvierende spikende Forschungsarchitektur so entwickeln, operationalisieren und prüfen, dass behauptete Funktionalität und Lernkausalität durch explizite Kontrollen, Provenienz und revidierbare Evidenzverträge getragen werden, während stärkere kognitive, biologische oder normative Aussagen nur dort zugelassen werden, wo ihre eigenen Prüfbedingungen erfüllt sind?**

Diese Leitfrage ist breiter als eine einzelne Hypothese. Sie wird durch mehrere Teilstudien beantwortet, die unterschiedliche Evidenzformen besitzen und deshalb nicht in einen gemeinsamen Erfolgswert gepresst werden.

### Arbeitsleitthese

Die leitende, revidierbare Arbeitsthese lautet:

> **Wissenschaftliche Reife entsteht in MHRN nicht durch die Addition möglichst vieler Mechanismen, sondern durch deren empirische Selektion unter expliziten Kontroll-, Provenienz- und Evidenzbedingungen.**

Diese These ist kein vorweggenommenes Ergebnis. Sie wird daran gemessen, ob die Forschungszweige tatsächlich zeigen, dass schwächere Erklärungen ausgeschlossen, negative Resultate architektonisch verarbeitet, offene Hypothesen offen gelassen und neue Funktionen erst nach geeigneten Vergleichsbedingungen wissenschaftlich aufgewertet werden.

### Teilstudien und Forschungszweige

| Forschungszweig | Wissenschaftliche Kernfrage | Primärer methodischer Zugriff | Gegenwärtige Grenze |
| --- | --- | --- | --- |
| **Basale neuronale Dynamik und Determinismus** | Sind definierte Einzelzell- und Netzwerktrajektorien unter kontrollierten Bedingungen reproduzierbar und referenzkonform? | Referenzvergleich, Same-Seed-Replikate, Zustands-/Hash-Provenienz | keine allgemeine Determinismus- oder biologische Äquivalenzbehauptung |
| **Rekurrenz, Topologie und 5D** | Welche Netzwerkunterschiede sind kausal auf Rekurrenz beziehungsweise Geometrie zurückzuführen? | matched controls, Ablation, Topologie-/Delay-Kopplung, Activity-Adequacy-Gates | 5D-v1 war für den zentralen Geometrieclaim nicht testadäquat |
| **Plastizität und adaptive Dynamik** | Verändern STDP, Drei-Faktor-Regeln, Homeostase und Strukturplastizität Lernen oder Stabilität gegenüber geeigneten Kontrollen? | learning-on/off, Sham, Frozen, Perturbation und gehaltene Testdaten | Implementierung ist nicht gleich funktionaler Lernnachweis |
| **Spezialisierte Pfade und MSBA** | Liefern modalitätsspezifische und adaptive Pfade unter kontrollierten Ressourcenbedingungen messbaren technischen Nutzen? | E01–E05, synthetische Kosten-/Recovery-/Integritätsvergleiche | kein Nachweis emergenter Arealbildung oder allgemeiner Überlegenheit |
| **Embodiment** | Kann eine Sensor–SNN–Aktor–Feedback-Kette zielgerichtete Wirkung unter kontrollierten Störungen erzeugen und kausal vom Open Loop getrennt werden? | Closed Loop, Fehlerarme, Yoked-/Interrupted-Controls | Realweltübertragbarkeit und `H-EMB-001-B` bleiben offen |
| **Gedächtnis, Replay und Weltmodell** | Welche Retention stammt von Replay, semantischer Verdichtung oder einem tatsächlich kausal wirksamen Vorhersagemodell? | matched Replay, Random-Prototypes, Holdout, Kompressions- und Modellkontrollen | SemanticMemory-Zusatznutzen nicht bestätigt; Kompressionsfrage noch präregistrierungspflichtig |
| **Epistemologie und Forschungsprozess** | Verbessern Provenienz-, Freeze-, Review- und EVID-Gates die Qualität der wissenschaftlichen Entscheidungen? | Prozessrekonstruktion, Status-Audit, Kontrafaktik, Revisionstracing | interne Verbesserung ist keine unabhängige externe Validierung |
| **Ethik, Safety und Autonomie** | Welche Kontroll-, Ziel- und Welfare-Fragen entstehen bei zunehmender Wirk- und Lernfähigkeit? | normative Analyse, Szenarien, technische Safety-Verträge | keine Prognose, kein Bewusstseins- oder Sentienznachweis |

Damit besitzt jeder Forschungszweig einen eigenen wissenschaftlichen Gegenstand. Teil IV behandelt die empirischen Zweige als Teilstudien; Teil VI die epistemologische Methodik; Teil VIII die normative Analyse; Teil IX die Theorieentwicklung; Teil X übernimmt die General Discussion; Teil XI formuliert Limitationen, offene Hypothesen und die priorisierte Forschungsagenda.
