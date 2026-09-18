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
