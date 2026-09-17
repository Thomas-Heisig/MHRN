# Teil I — Nullpunkt, Autor und Entstehungsbedingungen

## 1. Forschungsgegenstand vor dem Repository

Die 1.8-Fassung setzt nicht mit einem vermeintlich fertigen MHRN an. Sie behandelt die Entstehung selbst als Forschungsgegenstand. Die frühesten in dieser Revision wiedergewonnenen Spuren stammen aus Gesprächen über einen persistenten neuronalen Würfel, dynamische Verbindungen, entwicklungsähnliche Schichten, Mutation, Speicherung über Neustarts hinweg und die Trennung zwischen einem lernenden Kern und nachladbaren Funktionen. Diese Spuren werden als **rekonstruierte Vorphase** geführt. Sie belegen weder, dass dies die erste Idee überhaupt war, noch dass die beschriebenen Mechanismen damals schon implementiert waren.

Der historische Wert liegt in der Problemkontinuität: Wie kann ein System Wissen behalten, ohne dass ein externes Sprachmodell oder eine Datenbank fälschlich als neuronales Gedächtnis gezählt wird? Wie lässt sich Wachstum zulassen, ohne die Kausalität zu verlieren? Wie kann ein technisches System zugleich offen erweiterbar und wissenschaftlich prüfbar bleiben? Diese Fragen erscheinen später in deutlich strengeren Formen wieder: als Persistenzvertrag, Retrieval-Isolation, strukturelle Plastizität, Capability-Gates, Experimentregister und Evidenzgrenzen.

## 2. Autorposition

Thomas Heisig wird in dieser Arbeit als Autor und Projektleiter geführt. KI-Systeme sind als Recherche-, Synthese-, Kritik-, Programmier- und Formulierungswerkzeuge dokumentiert, erhalten aber keine automatische Quellen- oder Autoritätsrolle. Entscheidend ist nicht, ob ein Satz mit menschlicher oder maschineller Hilfe formuliert wurde, sondern ob seine Herkunft, seine Prüfgrundlage und seine Entscheidungskette nachvollziehbar sind.

Die Selbstauskunft des Autors ist eine Primärquelle für Motivation und Arbeitsweise, jedoch keine empirische Evidenz über neuronale Mechanismen. Persönliche Intuition kann Forschungsfragen erzeugen; sie darf keine Hypothese bestätigen. Umgekehrt wird die ungewöhnlich enge Mensch-KI-Arbeit nicht versteckt. Sie ist selbst Teil der epistemologischen Fragestellung dieser Arbeit: Was bedeutet Autorschaft, wenn externe kognitive Werkzeuge permanent an Suche, Gegenargument, Implementierung und Text beteiligt sind?

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
