# Teil VII — Integrität, Autorschaft und kumulative Wissenschaft

## 29. Kumulative Wissenschaft und Plagiat

Wissenschaft ist kumulativ: Begriffe, Modelle, Methoden und Software entstehen in Traditionslinien. Daraus folgt gerade nicht, dass Attribution entbehrlich wäre. Edition 1.8 trennt epistemische Kumulativität von institutionellem Plagiat. Fremde Texte, Daten, Code oder zurechenbare Ideen werden nicht als eigene Primärleistung ausgegeben; zugleich wird nicht behauptet, dass jede technische Kombination allein durch Zitieren neuartig wird.

## 30. Einheitliches Zitationssystem

Die neue Textschicht verwendet Autor-Jahr-Zitation in Anlehnung an APA 7. Literaturquellen erhalten eine stabile Kennung, vollständige bibliografische Angabe, Original-URL beziehungsweise DOI, Prüftag und **tatsächlich geprüften Leseumfang**. Damit wird ein häufiger Fehler vermieden: Metadatenprüfung wird nicht als Volltextprüfung ausgegeben.

Eigene Vorarbeiten werden mit Edition, Pfad und Git-Revision zitiert. Historische Quellenbände bleiben lesbar, aber ihre alte Bibliografie wird nicht automatisch neu zertifiziert. Wörtliche Übernahmen benötigen Seiten- oder Abschnittsbezug. Eigene Übersetzungen werden markiert. Tabellen, Abbildungen, Daten und Code benötigen zusätzlich gegebenenfalls Lizenz-/Nutzungsprüfung.

## 31. Prior Art und Neuheit

MHRN verwendet etablierte neuronale Modelle, STDP, Three-Factor Learning, Homeostase, graphische Nullmodelle, Replay und Gedächtnistheorien. Beispielsweise sind Izhikevich-Neuronen ([@IZHIKEVICH2003]), timingabhängige synaptische Plastizität ([@BI_POO1998]), Drei-Faktor-Regeln ([@FREMAUX2016]), homeostatisches synaptisches Scaling ([@TURRIGIANO1998]; [@TURRIGIANO2008]) und Complementary Learning Systems ([@MCCLELLAND1995]) etablierte Vorarbeiten. Die Neuheit einer MHRN-Kombination folgt daraus weder positiv noch negativ automatisch.

Kandidaten wie die Vierertrennung von Identität/Slot/Reduktion/Scheduling, Proposal→Approval→Mutation→Journal→Undo, Content Gateway versus Compute Backend oder source-bound DATA/EVID-Grenzen bleiben Kandidaten, bis ein belastbarer Prior-Art-Review erfolgt.

### 31.1 Zitierstandard und Quellenklassen

Edition 1.8 verwendet Autor-Jahr-Zitation nach APA 7 ([@APA2020]). Externe Behauptungen sollen **direkt am tragenden Satz** belegt werden. Wo eine ursprüngliche Forschungsarbeit verfügbar und passend ist, wird sie als Primärliteratur bevorzugt; Review-, Survey- und Synthesearbeiten werden als Sekundärliteratur gekennzeichnet. Diese Trennung folgt auch der allgemeinen Empfehlung, Originalforschungsquellen möglichst direkt zu referenzieren und die Tragfähigkeit jeder Referenz für die zugehörige Aussage zu prüfen ([@ICMJE2026]).

Das maschinenlesbare Literaturregister unterscheidet daher vier Klassen: `primary`, `secondary`, `guideline` und `standard`. **Primärliteratur** trägt ursprüngliche empirische, methodische oder theoretische Befunde; **Sekundärliteratur** trägt Review, Survey oder Synthese; **Richtlinien und Standards** regeln Darstellung, Autorenschaft oder Beitragsbeschreibung, erzeugen aber keine Evidenz für MHRN-Mechanismen.

Im Fließtext darf `et al.` nach APA-Konvention zur Verkürzung von Mehrfachautorenschaften verwendet werden; im Literaturverzeichnis werden bei den hier erfassten Arbeiten die vollständigen Autorenlisten ausgegeben. Ein Literaturzitat belegt nur den externen Satz, neben dem es steht. Es kann weder MHRN-DATA erzeugen noch ein internes Experiment ersetzen.

## 32. Similarity und Quellenquarantäne

Interne Similarity-Prüfungen reduzieren Risiken, zertifizieren aber keine Plagiatsfreiheit. Vor einer formalen Einreichung bleiben menschlicher Quellenabgleich und eine institutionell geeignete externe Text-/Code-Similarity-Prüfung offen. Nicht bestätigte Quellen oder vermeintliche Normen bleiben quarantänisiert und dürfen nicht allein aufgrund plausibler Titel in die Argumentation gelangen.

## 33. AI-Assistenz und Verantwortlichkeit

KI-Systeme können Formulierungen, Code, Literaturkandidaten oder Gegenargumente erzeugen. Verantwortung für die veröffentlichte Fassung bleibt beim menschlichen Autor; AI-Systeme werden nicht als Autoren oder Primärquellen geführt ([@ICMJE2026]). Wo ein konkreter AI-Vorschlag für die Genealogie relevant ist, wird er als Prozessartefakt bezeichnet und nicht durch nachträgliche Autorschaftsvereinfachung verdeckt.

## 33.1 Eigene Vorarbeiten sind Quelle, nicht „neuer“ Text

Die Editionslinie 1.0–1.8 enthält erhebliche Eigenwiederverwendung. Das ist wissenschaftlich zulässig, wenn Herkunft und Veränderung sichtbar bleiben. Edition 1.8 behandelt ältere eigene Manuskripte deshalb als **MHRN prior work** und nicht als neue Primärleistung allein durch Umordnung.

Der ungekürzte 1.7-Quellenband in `LEGACY_V17.md` erfüllt genau diese Funktion: Er bewahrt den historischen Text, während 1.8 die Erkenntnisse in eine neue Struktur überführt. Die neue Leistung liegt in der aktualisierten Synthese, den zusätzlichen Befunden, den Korrekturen und der neuen Provenienzstruktur — nicht darin, ältere eigene Sätze als erstmals entstandene Erkenntnis auszugeben.

## 33.2 Kumulative Forschung braucht stärkere Attribution, nicht schwächere

Die in den Vorgängerarbeiten formulierte Position, Forschung sei grundsätzlich kumulativ, wird in 1.8 präzisiert. Je stärker ein Projekt auf bestehende Modelle, Bibliotheken, Theorien und AI-Werkzeuge zurückgreift, desto wichtiger werden vier Ebenen der Zuschreibung:

1. **externe Theorie oder Methode** — etwa Izhikevich, STDP, CLS, Predictive Coding oder Safe Interruptibility;
2. **eigene frühere Arbeit** — ältere MHRN-/Brain-5D-Fassungen und Experimente;
3. **Werkzeugbeitrag** — AI-generierter Code, Recherchehilfe oder Formulierung;
4. **aktuelle Eigenleistung** — konkrete Integration, Hypothese, Experiment, Review oder Synthese dieser Edition.

Damit wird verhindert, dass „kumulativ“ zu einer Ausrede für unklare Herkunft wird.

## 33.3 Der Quellenstatus ist Teil des Claims

Eine Literaturangabe ist nicht nur bibliografische Dekoration. Für MHRN ist relevant, **was tatsächlich geprüft wurde**. Metadaten können Titel, Autor, Jahr und DOI bestätigen; ein Abstract kann den groben Gegenstand bestätigen; erst die Primärlektüre kann stärkere inhaltliche Aussagen tragen.

Diese Differenz wird in 1.8 als Quellenstatus dokumentiert. Nicht bestätigte Literatur bleibt quarantänisiert. Frühere plausible, aber nicht hinreichend verifizierte Hinweise werden nicht aufgrund ihrer Passgenauigkeit übernommen.

## 33.4 KI-generierte Kritik ist wertvoll, aber nicht unabhängig

AI-Reviewer haben im Projekt mehrfach nützliche Fehler identifiziert oder Gegenargumente erzeugt. Gleichzeitig zeigte die AIRR-Pipeline, dass AI-Ausgaben selbst Schema- und Interpretationsfehler enthalten können. Daraus folgt eine doppelte Regel:

- KI-Kritik ist ein legitimes **Prüfwerkzeug** und kann neue Human-Review-Fragen erzeugen.
- Sie ist keine unabhängige Replikation und keine automatische EVID-Instanz.

Ein AI-Review, das einen Lauf korrekt kritisiert, stärkt die Methodik; es verändert aber den Evidenzstatus erst dann, wenn die Kritik auf Primärartefakte zurückgeführt und als menschliche oder formal definierte Reviewentscheidung verarbeitet wurde.

## 33.5 Negative Ergebnisse gehören zur Autorschaft

Autorschaft bedeutet in dieser Arbeit nicht nur, positive Ergebnisse zu vertreten. Die CL-002-Falsifikation, die negative CL-003-Primärkontraste, die nicht testadäquate 5D-v1-Studie und der historische Stage-0-Langzeit-Negativbefund bleiben Teil der Forschungsleistung.

Eine wissenschaftliche Arbeit wird hier nicht dadurch „erfolgreich“, dass jede frühe Idee bestätigt wird. Sie ist dann belastbarer, wenn sie sichtbar macht, welche Annahmen aufgegeben, reduziert oder neu operationalisiert werden mussten.

## 33.6 Neuheitskandidaten und ihre Prüfpflicht

Die folgenden Kombinationen werden als potenzielle Beiträge weiterverfolgt, aber nicht als bewiesene Neuheit ausgegeben:

- Logical Identity / Physical Slot / Synaptic Reduction / Execution Scheduling;
- Proposal → Approval → Mutation → Journal → Undo;
- Content Gateway / Compute Backend;
- source-bound DATA/EVID-Trennung in einem integrierten Forschungs-/Engineeringworkflow;
- getrennte Engineering- und Scientific-Maturity-Achsen;
- rekursive Epistemik als explizite Verbindung von Objekt-Gateways und Forschungsprozess-Gateways.

Für jeden Kandidaten ist ein eigener Prior-Art-Pfad nötig. Eine gute interne Kombination kann wissenschaftlich nützlich sein, auch wenn sich später zeigt, dass ähnliche Strukturen bereits existieren.

## 33.7 Integrität als laufender Prozess

Integrität wird nicht einmalig durch ein Manifest „erledigt“. Vor externer Einreichung bleiben mindestens offen:

- systematischer Prior-Art-Review;
- menschliche Quellenprüfung wichtiger Argumente;
- externe Similarity-Prüfung für Text und gegebenenfalls Code;
- unabhängige fachliche Reviews;
- klare Kennzeichnung eigener Übersetzungen und wiederverwendeter Eigenpassagen;
- Prüfung von Lizenzen und Nutzungsrechten für fremde Abbildungen, Tabellen, Daten und Code.

Edition 1.8 macht diese offenen Punkte sichtbar, statt aus internen Audits ein Zertifikat abzuleiten.
