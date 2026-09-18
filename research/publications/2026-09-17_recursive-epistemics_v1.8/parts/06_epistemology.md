# Teil VI — Epistemologie und Methodik der Schaffensgeschichte

## 25. Drei Forschungsachsen

Edition 1.8 führt drei gleichrangige, aber methodisch unterschiedliche Achsen: **empirisch-technisch**, **epistemologisch-methodisch** und **philosophisch-ethisch**. Gleichrangig bedeutet nicht, dass dieselben Evidenzregeln gelten. Ein Lauf kann einen empirischen Effekt prüfen. Eine Provenienzanalyse kann zeigen, wie eine Entscheidung entstand. Eine normative These muss durch begründete Prämissen, Gegenargumente und Folgerungen getragen werden. Keine Achse darf die andere imitieren.

Die Aussagekoordinate lautet: `Achse × Thema × Entwicklungsphase × Provenienz × Evidenzstatus`. Sie ersetzt eindimensionale Kapitelnummern nicht, erweitert sie aber um die Frage, **was für eine Art Aussage** an welcher Stelle gemacht wird.

## 26. Provenienzklassen

S1 umfasst harte Primärartefakte: Commits, Tags, frozen Preregistrierungen, DATA, Manifeste und Hashes. S2 umfasst zeitgenössische Prozessartefakte wie Issues, Reviews, Chats oder AI-Interaktionen. S3 umfasst zeitgenössische Selbstauskunft. S4 ist retrospektive Rekonstruktion. Bei Widerspruch hat das zeitgenössische Artefakt Vorrang; fehlende Dokumentation bleibt als Lücke sichtbar.

Die außerhalb des Repositories wiedergewonnenen Chat-Zusammenfassungen sind in dieser Edition bewusst S4. Sie dürfen nicht zu scheinbar wörtlichen Zitaten oder Prioritätsbeweisen hochgestuft werden. Wenn später Originaltranskripte eingebunden werden, entstehen neue Provenienzeinträge, nicht heimliche Umschreibungen der alten Rekonstruktion.

## 27. KI-assistierte Forschung

KI-Unterstützung erzeugt eine zusätzliche Provenienzdimension. Ein Vorschlag eines Assistenten ist nicht automatisch eine Idee des Autors; eine vom Autor verlangte Richtung ist nicht automatisch eine implementierte Funktion; ein generierter Patch ist nicht automatisch ein wissenschaftlicher Befund. Edition 1.8 trennt deshalb `user requirement`, `AI proposal`, `human decision`, `commit`, `run`, `review` und `publication synthesis`, soweit die Quellen dies erlauben.

Die Arbeit nutzt KI zugleich als Gegenstand und Werkzeug. Das erhöht das Risiko rekursiver Bestätigungsfehler: Ein System könnte seine eigenen früheren Formulierungen wiederfinden und als externe Unterstützung missverstehen. Dagegen helfen Quellenklassen, Originalquellen, quarantänisierte Literatur und getrennte Human-Review-Gates.

## 28. Falsifikation von Entstehungs- und Prioritätsaussagen

Auch Schaffensgeschichte muss revidierbar sein. Eine Behauptung wie „Idee X entstand zuerst am Datum Y“ ist nur zulässig, wenn das Artefakt den Inhalt tatsächlich trägt und ältere Quellen nicht widersprechen. Ein späteres Dokument kann die frühere Existenz einer Idee bezeugen, aber selten ihren exakten Entstehungszeitpunkt.

Edition 1.8 behauptet daher keine absolute Priorität für die rekonstruierten Vor-Repo-Ideen. Sie dokumentiert die **früheste derzeit wiedergewonnene Spur** und öffnet ein Register für Korrekturen.

## 28.1 Epistemische Regeln, die aus konkreten Forschungsfehlern entstanden

Die Methodik dieser Arbeit ist nicht nur theoretisch gesetzt. Mehrere Regeln wurden durch konkrete Fehlinterpretationen notwendig.

### Ein negatives Resultat setzt Testadäquanz voraus

Die 5D-v1-Teilstudie ist das klarste Beispiel. Identische Resultate über verschiedene Dimensionsbedingungen wären oberflächlich ein Nullbefund. Die Human Review zeigte jedoch, dass die Dimension die relevante Netzwerkdynamik kaum beeinflussen konnte. Die korrekte epistemische Klassifikation ist daher nicht „Hypothese widerlegt“, sondern „für den intendierten Geometrieeffekt nicht getestet“.

Daraus folgt die Regel: Vor jeder Bestätigung oder Falsifikation muss geprüft werden, ob das Design **sensitiv für den behaupteten Mechanismus** war.

### DATA und Report sind verschiedene Objekte

In `EXP-GEN-0036` existierten Runs und protokollspezifische Statistik, obwohl die Summary in mehreren universellen SNN-Spalten `—` zeigte. Eine erste Interpretation hielt dies für fehlende DATA. Die Review korrigierte diese Schlussfolgerung.

Daraus folgt: Reporting ist eine Transformation von DATA und kann selbst fehlerhaft sein. Wissenschaftliche Interpretation darf sich bei kritischen Punkten nicht allein auf eine Sekundärprojektion stützen, wenn Rohartefakte und Statistik verfügbar sind.

### Eine positive Baseline-Differenz ist noch keine Mechanismusidentifikation

CL-001 zeigte einen Vorteil von Semantic+Replay gegenüber No-Replay. Erst CL-002 mit gematchtem Raw-Replay machte sichtbar, dass dieser Befund die Rolle von Replay und semantischer Verdichtung nicht getrennt hatte. Der stärkere Kontrollarm veränderte die zulässige Theorie.

Daraus folgt: Die Qualität einer Hypothesenprüfung hängt nicht nur von Signifikanz oder Effektgröße ab, sondern davon, ob die **plausibelste alternative Erklärung** experimentell adressiert wird.

### Externe Softwarekonformität ist nicht identisch mit unabhängiger Replikation

Die Stage-0-V2-Prüfung gegen Brian2 ist ein starker Referenzvergleich. Sie bleibt jedoch durch MHRN formuliert, ausgeführt und interpretiert. Deshalb erfüllt sie nicht automatisch das Kriterium einer unabhängig autorisierten Replikation.

Daraus folgt eine Trennung von Referenzkonformität, Human Review und unabhängiger Replikation.

## 28.2 Methodik der epistemologischen Achse

Die epistemologisch-methodische Achse benötigt eigene Prüfverfahren. Sie darf nicht nur kommentieren, wie Forschung „eigentlich“ funktionieren sollte. Für MHRN werden deshalb folgende Verfahren verwendet:

1. **Provenienzanalyse:** Welche Quelle existierte wann und in welchem Status?
2. **Entscheidungsrekonstruktion:** Welche Alternative wurde vor einer Implementierung oder Ausführung erwogen?
3. **Status-Transition-Audit:** An welcher Stelle wechselte ein Objekt von Idee zu Spezifikation, DATA, Review oder EVID?
4. **Kontrafaktische Prozessprüfung:** Welche andere Schlussfolgerung wäre entstanden, wenn eine stärkere Baseline oder ein anderes Reporting vorgelegen hätte?
5. **Revisionstracing:** Welche konkrete Architektur- oder Methodikänderung folgte aus einem negativen oder korrigierten Befund?
6. **AI-Provenienzprüfung:** Stammt ein Argument aus externer Literatur, einem Modellvorschlag, dem Autor, einer Messung oder einer späteren Synthese?

Damit kann die Schaffensgeschichte selbst falsifizierbare Aussagen enthalten. Ein behaupteter Entscheidungsursprung kann durch einen älteren Commit widerlegt werden; eine vermeintlich menschliche Idee kann sich als zuvor dokumentierter AI-Vorschlag herausstellen; eine angeblich datengetriebene Architekturentscheidung kann sich als bereits vor den DATA festgelegt zeigen.

## 28.3 Explorativ, konfirmatorisch und rekonstruktiv

MHRN unterscheidet drei Modi, die häufig vermischt werden:

- **explorativ:** Hypothesen- und Mechanismussuche; flexibel, aber nachträgliche Muster dürfen nicht als präregistriert ausgegeben werden;
- **konfirmatorisch:** Endpunkte, Kontraste, Seeds, Ausschlüsse und Erfolgsregeln sind vor der Ausführung eingefroren;
- **rekonstruktiv:** historische oder epistemische Rekonstruktion aus vorhandenen Artefakten; Aussagen hängen von Provenienzqualität und Vollständigkeit der Quellen ab.

Die frühe NeuroGenesis-/Brain-5D-Geschichte ist überwiegend rekonstruktiv. CL-003 ist in seiner Ausführung konfirmatorisch angelegt. Viele Stage-8–10-Arbeiten sind derzeit explorativ beziehungsweise programmatisch. Diese Modi dürfen in der Synthese verbunden, aber nicht epistemisch gleichgestellt werden.

## 28.4 Präregistrierung schützt auch vor dem eigenen Entwicklungsdrang

Die Forschungsarbeit entsteht in einem schnell iterierenden Engineeringkontext. Gerade dort verhindert ein Freeze, dass neue Einsichten nach Sichtung der DATA unbemerkt Teil des ursprünglichen Erfolgsmaßstabs werden. CL-003 zeigte den Wert dieser Grenze: Der deskriptiv mit der Dosis wachsende Semantic-minus-Raw-Unterschied wäre verführerisch als positiver Dosisbefund formulierbar gewesen; der präregistrierte Interaktionstest C4 blieb jedoch negativ. Deshalb ist die stärkere Behauptung nicht zulässig.

Präregistrierung trennt prospektive Hypothesenprüfung von nachträglicher Musterdeutung; genau diese Funktion wird in der methodischen Literatur als zentraler Zweck beschrieben ([@NOSEK2018]). In diesem Projekt wirkt sie damit nicht nur gegen klassische p-Hacking-Risiken, sondern gegen **architektonisches Nachrationalisieren**.

## 28.5 Revidierbarkeit als Qualitätskriterium

Eine starke Aussage in MHRN nennt nicht nur, warum sie aktuell plausibel ist, sondern auch, wodurch sie sich ändern würde. Für 5D ist dies ein geometriesensitives matched-control Experiment. Für SemanticMemory ist es ein begrenzter, vorab begründeter Zusatznutzen gegenüber Raw-Replay. Für ein Weltmodell ist es Mehrschritt- und Entscheidungsnutzen unter geeigneten Kontrollen. Für ein Selbstmodell ist es kausale Self/Other-Differenzierung.

Die Arbeit versteht Revidierbarkeit daher nicht als Schwäche, sondern als explizite Schnittstelle zwischen heutiger Synthese und zukünftiger Evidenz.
