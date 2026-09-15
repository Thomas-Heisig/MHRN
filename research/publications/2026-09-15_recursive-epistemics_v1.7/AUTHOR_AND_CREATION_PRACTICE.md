# Autor und Schaffensart

**Dokumenttyp:** Kanonische Selbstauskunft des Autors  
**Status:** `current`  
**Autorität:** primär als Selbstauskunft  
**Gültigkeit:** ab Edition 1.7  
**Stand:** 15. September 2026  
**Zitierregel:** zitierbar als Autorposition bzw. Selbstauskunft  
**Evidenzrolle:** keine empirische Evidenz; biografische, epistemologische und methodische Kontextualisierung  
**Abgrenzung:** ergänzt [`AUTHOR_POSITION.md`](AUTHOR_POSITION.md) und [`INTEGRITY_AND_ATTRIBUTION.md`](INTEGRITY_AND_ATTRIBUTION.md), ersetzt beide Dokumente nicht  
**Quellenbasis:** konsolidierte Selbstauskunft aus dem für diese Edition verfügbaren Projekt-, Gesprächs- und Profilkontext; keine unabhängige biografische Verifikation

---

## 0. Geltungsbereich und Leseregel

Dieses Dokument beschreibt, **wer ich als Autor von MHRN bin, aus welchem Hintergrund heraus ich arbeite, wie diese Arbeit tatsächlich entsteht und welche methodischen Folgen daraus entstehen**.

Es ist bewusst persönlicher als das übrige Forschungsmanuskript. Gerade deshalb gilt eine strenge Leseregel:

1. Biografische Angaben in diesem Dokument sind **Selbstauskünfte**.
2. Meine persönliche Erfahrung darf **Fragen und Hypothesen motivieren**, aber keine Hypothese bestätigen.
3. Berufliche Qualifikationen außerhalb der akademischen Neurowissenschaft oder Informatik können meine Arbeitsweise erklären, ersetzen aber **keine fachwissenschaftliche Qualifikation, Literaturprüfung, Replikation oder externe Begutachtung**.
4. Die hier beschriebene Nutzung künstlicher Intelligenz ist ein Teil der Entstehungsprovenienz. Ein KI-System wird dadurch **weder wissenschaftlicher Autor noch Evidenzquelle**.
5. Aussagen zu meinem kognitiven Profil sind freiwillige Selbstbeschreibung. Sie sind weder Gegenstand eines MHRN-Experiments noch diagnostischer Nachweis innerhalb dieser Arbeit.
6. Operative Daten über Kunden, Mitarbeitende, Minderjährige, Vereinsmitglieder, Patientenkontexte oder andere Dritte gehören nicht in eine kanonische Autorenselbstauskunft und werden hier bewusst nicht übernommen.

Die Selbstauskunft macht die Person hinter dem Projekt sichtbar, ohne die Person zum Beweis für das Projekt zu machen.

---

## 1. Position

Ich bin Thomas Heisig und der Autor sowie verantwortliche menschliche Entscheidungsträger hinter MHRN.

Ich bin **kein Neurowissenschaftler, kein promovierter Informatiker und kein Mitglied einer Forschungsinstitution**. Ich verfüge nicht über ein universitäres Labor, institutionelle Rechenzentren, eine Forschungsgruppe oder ein formales akademisches Betreuungsverhältnis, das die wissenschaftliche Qualität dieser Arbeit automatisch absichern könnte.

Ich arbeite als **unabhängiger Einzelforscher und Systementwickler mit begrenzter Zeit, begrenzter Rechenleistung und begrenzter fachlicher Reichweite**. Gleichzeitig verfüge ich über technische Werkzeuge, lokale und externe Sprachmodelle, Audioverarbeitung, Internetzugang, Softwarewerkzeuge und KI-gestützte Coding-Systeme, durch die Aufgaben parallelisiert werden können, die früher häufig auf mehrere Personen verteilt gewesen wären.

Diese technische Situation darf nicht romantisiert werden. Sprachmodelle ersetzen weder Laborinfrastruktur noch Domänenexpertise, unabhängige Replikation, Statistik, Ethikprüfung oder Peer Review. Sie verändern aber, **welche Breite an Recherche-, Entwicklungs-, Dokumentations- und Prüfaufgaben ein einzelner Mensch praktisch bearbeiten kann**.

Mein wissenschaftlicher Anspruch ist deshalb nicht institutioneller Status, sondern **Nachvollziehbarkeit**:

- Was wurde behauptet?
- Woher stammt die Behauptung?
- Was wurde implementiert?
- Was wurde tatsächlich gemessen?
- Was ist Interpretation?
- Was ist noch offen?
- Was wurde verworfen oder widerlegt?

Ich beanspruche **keinen wissenschaftlichen Durchbruch aufgrund meiner Person**. Ich beanspruche das Recht und die Pflicht, eine eigenständige Forschungsarbeit zu strukturieren, zu dokumentieren, zu falsifizieren und zur Prüfung offenzulegen.

### 1.1 Beruflicher und technischer Hintergrund

Mein Ausgangspunkt ist nicht das akademische Labor, sondern eine ungewöhnlich breite **handwerkliche, technische, kaufmännische und informationstechnische Praxis**.

Zu meinem selbst angegebenen beruflichen und qualifikatorischen Hintergrund gehören insbesondere:

- Steinmetz- und Steinbildhauermeister,
- Natursteintechniker,
- Elektroniker-Geselle,
- kaufmännische Ausbildung mit Einzelhandels-/EDV-Bezug,
- betriebswirtschaftliche Qualifikation,
- laufende bzw. weiterführende Qualifikation im Restaurierungsbereich,
- praktische Computer-, Netzwerk- und Softwareentwicklungserfahrung.

Zusätzlich habe ich Verantwortung in praktischen Kontexten übernommen, die mit dieser Forschung nicht fachlich gleichgesetzt werden dürfen, meine Arbeitsweise aber mitgeprägt haben: handwerklicher Betrieb, technische Unterstützung in einer medizinischen Praxisumgebung, Vereins- und Jugendarbeit im Fußball sowie weitere organisatorische und sicherheitsbezogene Aufgaben.

Diese Herkunft beeinflusst meine Denkweise. Ich bin gewohnt, Systeme nicht nur abstrakt zu beschreiben, sondern sie **zu bauen, zu messen, Fehler einzugrenzen, Randbedingungen zu beachten, Verantwortung zuzuordnen und nach einem Eingriff erneut zu prüfen**. Im Handwerk ist eine Konstruktion nicht richtig, weil sie elegant beschrieben wurde. Sie muss passen, tragen und reproduzierbar ausgeführt werden können. In Elektrotechnik und IT gilt Ähnliches: Ein Fehler kann aus einer Schnittstelle, einem Zustand, einer falschen Annahme oder einer Wechselwirkung entstehen.

Diese praktische Systemperspektive ist für MHRN relevant. Sie ist aber **keine Ersatzqualifikation für Neurowissenschaft, Statistik, theoretische Informatik oder Medizin**. Wo mir formale Fachausbildung fehlt, muss die Arbeit das durch transparentere Grenzen, Primärliteratur, Tests, Gegenprüfung und externe Kritik kompensieren — nicht durch Selbstvertrauen.

### 1.2 Technische Arbeitsumgebung

Die Forschung entsteht überwiegend auf lokaler, allgemein verfügbarer Computerhardware und mit einer modularen Softwareumgebung. Zum dokumentierten Arbeitsstil gehören unter anderem:

- Python-basierte wissenschaftliche und technische Komponenten,
- Git und GitHub als Versions- und Provenienzinfrastruktur,
- automatisierte Tests, CI/Gates und reproduzierbare Artefakte,
- Web- und Backend-Technologien wie FastAPI, React/Vite und relationale bzw. lokale Persistenz,
- lokale Sprachmodelle und Ollama-basierte Ausführung,
- externe Sprachmodelle und Recherchewerkzeuge,
- Audio-, Text-, Code- und UI-Arbeit in parallelen Arbeitsströmen.

Exakte Modell-, Hardware- und Versionsstände gehören in technische Manifeste und Ausführungsprotokolle. Diese Selbstauskunft soll die Arbeitsweise erklären und deshalb nicht durch schnell veraltende Versionsnummern zur technischen Inventarliste werden.

Die Begrenztheit der Infrastruktur ist wissenschaftlich relevant: Was auf lokaler Consumer-Hardware reproduzierbar ist, ist etwas anderes als ein Ergebnis aus einem großen institutionellen Compute-Cluster. Umgekehrt ist die lokale Ausführbarkeit ein bewusstes Engineering-Ziel, aber **kein wissenschaftlicher Qualitätsbeweis**.

---

## 2. Antrieb

Der Antrieb ist nicht Neugier allein. Er ist auch nicht bloßer Ehrgeiz. Er ist eine **Kombination aus persönlicher Betroffenheit, starkem Abschluss- und Ordnungsdrang und dem Bedürfnis, kognitive Systeme so weit zu verstehen, dass aus abstrakten Ideen überprüfbare Mechanismen werden**.

Ich beschreibe mein eigenes kognitives Profil als **ADHS mit autistischer Varianz**. Diese Formulierung ist hier eine freiwillige Selbstauskunft. Sie wird nicht als wissenschaftlicher Befund über mich verwendet und sie legitimiert keine Aussage über andere Menschen.

Ich möchte kognitive Systeme verstehen, weil ich in einem System lebe, das ich selbst als anders arbeitend erlebe als den statistischen Normalfall. Langfristig interessieren mich auch Parkinson, Demenz und andere Veränderungen kognitiver Systeme. Diese Themen haben persönliche Nähe und Bedeutung. MHRN ist deshalb nicht aus einem vollständig distanzierten Interesse entstanden.

Gerade daraus folgt eine methodische Pflicht: **Nähe erzeugt Fragen, nicht Antworten**.

Der Antrieb hat zwei Seiten, die zusammengehören und dennoch getrennt werden müssen:

- Die **persönliche Seite**: Betroffenheit, Nähe, Neugier auf die eigene und fremde Kognition, das Bedürfnis nach Verstehen.
- Die **systematische Seite**: der Wunsch, ein Werkzeug und eine Forschungsumgebung zu bauen, die über meine Person hinaus überprüfbare Aussagen ermöglichen könnte.

Die persönliche Seite liefert mögliche Forschungsfragen. Die systematische Seite muss Methoden, Kontrollbedingungen, Präregistrierung, Messungen und Falsifikationsmöglichkeiten liefern.

Meine Erfahrung bleibt **n = 1**. Sie kann eine Hypothese inspirieren. Sie kann weder deren Allgemeingültigkeit noch deren biologische oder medizinische Richtigkeit begründen.

Parkinson und Demenz sind in diesem Zusammenhang **langfristige Forschungs- und Verständnisziele**, keine Behauptung, dass MHRN derzeit Krankheiten modelliert, erklärt, diagnostiziert oder behandelt. Jede spätere medizinische Relevanz müsste durch eigene, fachlich geeignete Forschung getragen werden.

---

## 3. Wer ich bin und wie ich arbeite

Ich bin jemand, der nur schwer aufhört, solange ein System für mich strukturell offen ist. Ich erlebe einen starken inneren Drang, Zusammenhänge zu schließen, Widersprüche aufzulösen und Arbeit bis zu einem erkennbaren Zustand von Vollständigkeit weiterzutreiben.

Dieser Modus hat MHRN weit getragen. Er ist zugleich eine der wichtigsten Gefahren des Projekts.

**Struktur lässt sich schneller schließen als Empirie.**

Man kann eine Architektur ergänzen, eine Dokumenthierarchie vervollständigen, eine API definieren oder ein Modell sauber beschreiben. Ein wissenschaftlicher Befund dagegen braucht Daten, Kontrollbedingungen, Wiederholung, statistische Auswertung, Gegenhypothesen und im Idealfall unabhängige Replikation. Mein persönlicher Abschlussdrang darf diese langsamere Evidenzlogik nicht überspringen.

Ich arbeite häufig **parallel und hochfrequent**. In einer Arbeitssitzung können Text, Audio, Code, Frontend, Git, Literatur, Experimente und mehrere KI-Systeme gleichzeitig beteiligt sein. Ich erlebe diese Parallelität nicht als bloße Ablenkung, sondern als meinen produktiven Arbeitsmodus. Für die wissenschaftliche Bewertung ist diese Selbsteinschätzung jedoch zweitrangig: Entscheidend ist, ob die entstehenden Artefakte reproduzierbar, versioniert und überprüfbar sind.

Mein bevorzugter Entwicklungsmodus ähnelt einer Werkstatt:

1. Problem sichtbar machen.
2. Randbedingungen benennen.
3. Mechanismus isolieren.
4. Einen testbaren Eingriff definieren.
5. Ausführen.
6. Messen.
7. Fehler oder Abweichung dokumentieren.
8. Erst danach verallgemeinern.

In der Softwareentwicklung zeigt sich derselbe Anspruch in sauberen Modulen, formalen Schnittstellen, Tests, konsistenter Dokumentation, klaren Statusangaben und einer möglichst eindeutigen `Single Source of Truth`.

### 3.1 Interdisziplinarität ohne Kompetenzillusion

Meine Biografie führt dazu, dass ich zwischen sehr unterschiedlichen Denkweisen wechseln kann: Material und Toleranz aus dem Handwerk, Fehlersuche aus der Elektrotechnik, Kosten und Prozesse aus kaufmännischer Arbeit, Zustände und Schnittstellen aus der Softwareentwicklung, Verantwortung und Kommunikation aus Vereins- und Organisationsarbeit.

Das ist nützlich für Systemarchitektur. Es erzeugt aber ein Risiko: Wer viele Domänen berührt, kann leichter glauben, eine Domäne bereits verstanden zu haben, obwohl nur eine Analogie verstanden wurde.

Darum gilt für MHRN:

> Interdisziplinarität erweitert den Suchraum; sie hebt Kompetenzgrenzen nicht auf.

Eine handwerkliche oder technische Analogie kann einen Mechanismus verständlich machen. Sie ist noch kein neurowissenschaftlicher Beleg.

---

## 4. Was ich möchte

Ich möchte nicht, dass MHRN durch meine Person interessant sein muss. Ich möchte, dass es **prüfbar** wird.

Meine Ziele sind:

- ein **funktionierendes System**, dessen Verhalten mehr ist als eine lose Sammlung unverbundener Module;
- ein **ehrlicher wissenschaftlicher Beitrag**, der überprüft, kritisiert und zitiert werden kann, selbst wenn der Beitrag klein oder negativ ist;
- eine **Forschungsinfrastruktur**, die zwischen Architektur, Hypothese, Daten, Interpretation und Evidenz unterscheidet;
- ein **Werkzeug**, das langfristig beim Verständnis kognitiver Mechanismen helfen könnte;
- eine Entwicklungslinie, in der sichtbar bleibt, was übernommen, verändert, selbst entwickelt, falsifiziert oder noch nicht geprüft wurde.

Ich möchte nicht behaupten, dass MHRN diese Ziele bereits erreicht hat. Ich möchte die Struktur schaffen, in der sie testbar werden — und anschließend die Empirie liefern, die zeigt, welche Teile tragen und welche nicht.

Ein negativer Ausgang ist zulässig. Wenn eine zentrale Annahme nicht trägt, ist eine sauber dokumentierte Widerlegung wissenschaftlich wertvoller als eine Architektur, die durch nachträgliche Anpassungen immer recht behält.

---

## 5. Wohin das führt

Das Ziel ist nicht die eine große Entdeckung. Das Ziel ist ein **lernendes, anpassungsfähiges und auditierbares System**, das unterschiedliche verfügbare Ressourcen nutzen kann — lokal oder extern, klein oder groß — ohne dabei die kausale, methodische und provenancebezogene Kontrolle zu verlieren.

Wohin das führt, ist offen. Es kann

- in eine akademisch anschlussfähige Forschungsarbeit,
- in ein praktisch nutzbares technisches System,
- in eine Reihe kleiner reproduzierbarer Beiträge,
- oder in eine ehrliche negative Bilanz

münden.

Alle diese Ausgänge können wissenschaftlich wertvoll sein, wenn der Weg dokumentiert und die Aussagegrenzen eingehalten werden.

MHRN steht dabei in Kontinuität mit meinen früheren Arbeiten an Brain-5D und biologisch inspirierten SNN-Architekturen. Diese Kontinuität ist eine **Entwicklungsgeschichte**, keine Behauptung, dass frühere Projektnamen oder frühere Hypothesen bereits validierte wissenschaftliche Ergebnisse darstellen.

Was ich als methodischen Kern beibehalten will, ist die **Kette von vorab definierter Frage, ausführbarer Methode, erzeugtem Artefakt, Auswertung und veröffentlichter Schlussfolgerung**. Wo ein Experiment konfirmatorisch sein soll, müssen relevante Erfolgs- und Abbruchregeln vor der Datenauswertung feststehen. Wo dies nicht möglich oder nicht geschehen ist, muss die Analyse als explorativ gekennzeichnet werden.

Ich weiß außerdem, dass meine Arbeitszeit und persönliche Kapazität endlich sind. Diese Endlichkeit ist kein Argument für wissenschaftliche Abkürzungen. Sie ist ein Argument für Priorisierung: **nicht alles gleichzeitig behaupten, nicht alles gleichzeitig bauen und kritische Fragen vor zusätzlichen Funktionen bearbeiten**.

---

## 6. Schaffensart

Mit **Schaffensart** meine ich die dokumentierte Art, wie diese Arbeit entsteht: Wer entscheidet? Welche Systeme wirken mit? Welche Rolle haben sie? Wo liegt Verantwortung? Wie wird aus einem Vorschlag eine wissenschaftlich verantwortete Aussage?

MHRN entsteht in einer Form **assistierter Einzelautorschaft mit verteilter kognitiver Assistenz**.

Diese Bezeichnung ist absichtlich genauer als „verteilte Autorschaft“. Die beteiligten KI-Systeme sind keine Autoren im wissenschaftlichen Verantwortlichkeitssinn. Sie erzeugen Vorschläge, Gegenargumente, Code, Formulierungen, Suchrichtungen und Prüfimpulse. **Die Autorschaft und Verantwortung werden nicht verteilt.**

### 6.1 Autorenkern

Der Autorenkern ist ein Mensch mit begrenzter Kapazität, spezifischem kognitivem Profil und ungewöhnlich vielen parallelen Arbeitsströmen.

Ich entscheide,

- welche Frage verfolgt wird,
- welche Architektur akzeptiert oder verworfen wird,
- welche Hypothese präregistriert wird,
- welche Änderung in das Repository gelangt,
- welche Aussage als belastbar gelten darf,
- und welche Unsicherheit veröffentlicht werden muss.

Ich trage die Verantwortung für jede veröffentlichte Aussage, unabhängig davon, ob eine Formulierung, ein Codefragment oder ein Einwand durch mich allein, durch ein Sprachmodell oder in einem iterativen Dialog entstanden ist.

KI-Unterstützung kann Verantwortung nicht annehmen und entlastet mich daher nicht von ihr.

### 6.2 Externe Assistenz — dialogisch

Mehrere Sprachmodelle werden **parallel und dialogisch** genutzt, um Ideen zu prüfen, Gegenargumente zu erzeugen, Formulierungen zu schärfen, Literaturfragen zu strukturieren, Wissenslücken zu identifizieren und Inkonsistenzen aufzudecken.

Zum Stand dieser Edition gehören dazu insbesondere:

- **DeepSeek** — unter anderem für kritische Analyse, Strukturierung, Vertragsarbeit, Gegenargumentation und Code-Review,
- **ChatGPT** — unter anderem für externe Perspektiven, wissenschaftliche Einordnung, Gegenprüfung, Rechercheunterstützung, sprachliche Präzisierung und Repository-Arbeit,
- **weitere Systeme**, soweit sie für einzelne Aufgaben eingesetzt und in der jeweiligen Provenienz erfasst werden.

Diese Systeme verstehe ich als **dialogische Resonanz- und Prüfwerkzeuge**, nicht als Autoritäten. Sie können überzeugend falsch sein. Sie können dieselbe populäre Fehlannahme voneinander übernehmen. Mehrere Modelle, die dasselbe behaupten, sind deshalb **keine unabhängige Replikation**.

Ein von einem Sprachmodell vorgeschlagener Literaturhinweis wird erst dann wissenschaftliche Quelle, wenn die tatsächliche Quelle gefunden, geprüft und korrekt zitiert wurde. Dies entspricht dem Vertrag in [`INTEGRITY_AND_ATTRIBUTION.md`](INTEGRITY_AND_ATTRIBUTION.md).

### 6.3 Interne Assistenz — im MHRN-System

Einige Modelle werden nicht nur als externe Dialogwerkzeuge verwendet, sondern lokal bzw. innerhalb der MHRN-Infrastruktur für definierte Assistenzaufgaben eingesetzt.

Zum in dieser Selbstauskunft dokumentierten Arbeitsstand gehören unter anderem:

- **Qwen 3 7B** — als interner Revisor für Konsistenz-, Struktur- und Prüfaufgaben,
- **Gemma 8B** — für Zusammenfassungs- und Klassifikationsunterstützung,
- **Ollama-basierte Modelle** — abhängig von Aufgabe, lokaler Verfügbarkeit und dokumentierter Konfiguration.

Die konkrete Modell-ID, Quantisierung, Prompt-Konfiguration und Laufzeitumgebung muss dort festgehalten werden, wo ein Modell tatsächlich Teil eines reproduzierbaren Experiments oder einer technischen Pipeline ist.

Ein interner KI-Revisor ist **kein unabhängiger Peer Reviewer**. Er ist Teil derselben Forschungsinfrastruktur und kann systematische Fehler des Projekts teilen.

### 6.4 Coding-Assistenz

Für die Codeentwicklung werden spezialisierte Werkzeuge genutzt, die selbst auf Sprachmodellen beruhen. Zum dokumentierten Arbeitsstand zählen unter anderem:

- **GitHub Copilot mit DeepSeek**,
- **zai-org GLM**,
- **KIMI**,
- **GLM-basierte Werkzeuge bzw. Modelle**.

Diese Systeme können Codevorschläge, Refactorings, Testideen und Fehlerdiagnosen erzeugen. Sie beschleunigen die Implementierung, sind aber nicht automatisch Quelle der Architektur und nicht Garant für Korrektheit.

Für generierten oder stark assistierten Code gelten dieselben Engineering-Anforderungen wie für von Hand geschriebenen Code:

- Review,
- Tests,
- deterministische bzw. spezifizierte Randbedingungen,
- nachvollziehbare Änderungen,
- Commit-/Versionsprovenienz,
- und bei wissenschaftlich relevanten Komponenten die Verbindung zwischen Codezustand und Experiment.

### 6.5 Nicht-KI-Infrastruktur als Teil der Schaffensart

Die Schaffensart besteht nicht nur aus Sprachmodellen. Ebenso wichtig sind die Werkzeuge, die Gedanken in überprüfbare Zustände zwingen:

- Git-Historie,
- Branches und Reviews,
- automatisierte Tests,
- CI/Gates,
- ausführbare Experimente,
- strukturierte Reports,
- Manifestdateien,
- Editionen und Frozen-Stände,
- sowie die Trennung von aktueller WIP-Fassung und unveränderlichen historischen Artefakten.

Diese Werkzeuge haben eine epistemische Funktion: Sie reduzieren die Möglichkeit, eine frühere Aussage unbemerkt an ein späteres Ergebnis anzupassen.

### 6.6 Rollen- und Verantwortungsmatrix

| Ebene | Darf beitragen | Darf nicht allein begründen |
|---|---|---|
| **Menschlicher Autorenkern** | Fragestellung, Architektur, Auswahl, Interpretation, Veröffentlichung, Verantwortung | wissenschaftliche Wahrheit allein durch persönliche Überzeugung |
| **Dialogische KI** | Alternativen, Kritik, Entwürfe, Struktur, Suchrichtungen | Quellenautorität, empirische Evidenz, unabhängige Replikation |
| **Interne KI-Modelle** | definierte Review-, Klassifikations- oder Assistenzaufgaben | unabhängiges Peer Review oder externe Bestätigung |
| **Coding-Assistenz** | Codeentwürfe, Refactoring, Tests, Diagnose | Korrektheit ohne Review/Test oder wissenschaftliche Neuheit |
| **Literatur** | theoretische und empirische Fremdevidenz nach Prüfung | Beweis für MHRN-spezifische Implementationsbehauptungen ohne eigene Messung |
| **Experimente** | Daten über definierte MHRN-Zustände und Kontraste | Verallgemeinerung über das jeweilige Design hinaus |
| **Externe Menschen/Reviewer** | unabhängige Kritik, Replikation, Facheinschätzung | automatische Richtigkeit; auch externe Kritik muss nachvollziehbar sein |

### 6.7 Zentrale Formulierung

Die Schaffensart lässt sich präzise so formulieren:

> Wir dokumentieren, wie ein Mensch mit begrenzter Kapazität ein wissenschaftlich-technisches System baut, indem er verteilte kognitive Assistenz orchestriert, ohne Autorschaft, Auswahlentscheidung und Verantwortung an diese Assistenz zu delegieren.

Das ist keine Metapher für Teamarbeit. Es ist eine Beschreibung des tatsächlichen Arbeitsprozesses.

---

## 7. Verhältnis zwischen Autor und MHRN-Architektur

Es existiert eine auffällige strukturelle Ähnlichkeit zwischen meiner Arbeitsweise und Teilen der MHRN-Idee: Ein begrenzter Kern nutzt spezialisierte externe Ressourcen, führt Informationen über definierte Grenzen zusammen und soll dennoch die Kontrolle über Zustand, Provenienz und Entscheidung behalten.

Diese Ähnlichkeit ist **heuristisch interessant, aber wissenschaftlich gefährlich**, wenn sie nicht begrenzt wird.

Die frühere Formulierung „Der Autor ist Prototyp des Systems, das er baut“ darf deshalb nur in einem eingeschränkten Sinn verwendet werden. Präziser ist:

> Die Arbeitsweise des Autors kann eine Heuristik für Architekturfragen liefern. Sie ist keine Evidenz dafür, dass die daraus abgeleitete Architektur biologisch richtig, allgemein kognitiv wirksam oder technisch überlegen ist.

MHRN darf nicht recht bekommen, nur weil seine Architektur zu meiner eigenen Selbstbeschreibung passt. Eine solche Selbstähnlichkeit wäre sonst ein geschlossener Bestätigungskreis.

Der Autor ist damit **Entstehungskontext**, nicht Validierungsdatensatz.

---

## 8. Bekannte Bias- und Fehlerrisiken

Die Selbstauskunft ist nur wissenschaftlich nützlich, wenn sie nicht ausschließlich Stärken beschreibt. Aus meinem Arbeitsmodus ergeben sich konkrete Risiken.

### 8.1 Abschluss- und Closure-Bias

Mein starker Drang, Systeme zu vervollständigen, kann dazu führen, dass eine strukturell geschlossene Erklärung subjektiv befriedigender wirkt als ein offener empirischer Befund.

**Gegenmaßnahme:** Offene Fragen, `current_wip`, Stage-Matrizen und negative Ergebnisse bleiben sichtbar. Ein fehlender Befund darf nicht durch zusätzliche Architektur „weggebaut“ werden.

### 8.2 Confirmation Bias durch persönliche Nähe

Die persönliche Motivation kann bestimmte Erklärungen attraktiver machen — insbesondere dort, wo sie an mein eigenes Erleben anschließen.

**Gegenmaßnahme:** Persönliche Erfahrung erzeugt nur Fragen. Behauptungen müssen über Literatur, Code, Experimente oder externe Prüfung getragen werden. Gegenhypothesen und Falsifikationsbedingungen sind explizit zu dokumentieren.

### 8.3 Automation Bias

Ein sprachlich souveräner KI-Vorschlag kann plausibler wirken, als seine Evidenz rechtfertigt.

**Gegenmaßnahme:** KI-Ausgabe bleibt Vorschlag. Quellen werden verifiziert; experimentelle Behauptungen benötigen Artefakte; Code benötigt Tests; Literaturhinweise ohne Prüfung bleiben unverifiziert.

### 8.4 Korrelation mehrerer Modelle statt Unabhängigkeit

Mehrere KI-Systeme können aufgrund verwandter Trainingsdaten, verbreiteter Sekundärquellen oder ähnlicher Optimierungsziele denselben Fehler reproduzieren.

**Gegenmaßnahme:** Modellkonsens wird nicht als unabhängige Evidenz gezählt. Unabhängigkeit muss aus Datenherkunft, Methode oder menschlich/externer Replikation entstehen, nicht aus der Anzahl gleichlautender Chatantworten.

### 8.5 Breite-vor-Tiefe-Risiko

Parallele Arbeit ermöglicht große thematische Breite, kann aber dazu verleiten, zu viele Teilgebiete gleichzeitig nur oberflächlich abzudecken.

**Gegenmaßnahme:** Stages, Priorisierung, explizite `planned`-/`active`-/`reached`-Zustände und abgegrenzte Experimente. Ein implementierter Mechanismus ist nicht automatisch ein wissenschaftlich verstandener Mechanismus.

### 8.6 Analogie-Bias

Meine handwerkliche, elektrotechnische und softwaretechnische Erfahrung fördert mechanistische Analogien. Diese können produktiv sein, aber biologische Systeme sind nicht verpflichtet, sich wie Softwarearchitekturen oder technische Maschinen zu verhalten.

**Gegenmaßnahme:** Analogie und Evidenz werden sprachlich getrennt. Biologische Behauptungen benötigen biologische Literatur oder geeignete empirische Daten.

### 8.7 Kompetenzgrenzen

Die Kombination vieler Qualifikationen kann den Eindruck breiter fachlicher Autorität erzeugen.

**Gegenmaßnahme:** Qualifikationen werden als Herkunft der Arbeitsweise dokumentiert, nicht als Ersatz für fehlende Fachausbildung. Wo externe Fachkompetenz nötig ist, wird diese Lücke benannt.

### 8.8 Ressourcen- und Einzelforscher-Bias

Ein einzelner Autor kann nicht gleichzeitig vollständige Domänenexpertise, unabhängige Replikation und echte organisatorische Trennung der Rollen herstellen.

**Gegenmaßnahme:** Rollen werden zumindest artefaktseitig getrennt; frozen Stände werden nicht überschrieben; unabhängige Reviewer und Replikationen bleiben ausdrücklich erforderlich.

---

## 9. Konsequenzen für die wissenschaftliche Arbeit

Aus meiner Position und Schaffensart ergeben sich verbindliche Arbeitsregeln für Edition 1.7 und folgende Editionen.

### 9.1 Provenienz vor Rhetorik

Jede wissenschaftlich relevante Aussage soll soweit praktikabel erkennen lassen, ob sie stammt aus

- Literatur,
- eigener technischer Implementierung,
- eigenem Experiment,
- externer Prüfung,
- KI-unterstützter Synthese,
- persönlicher Selbstauskunft,
- oder einer Kombination davon.

Die Herkunft einer Formulierung ist nicht identisch mit der Evidenzquelle der Aussage.

### 9.2 Quelle der Frage und Quelle der Antwort trennen

Eine Forschungsfrage kann aus persönlichem Erleben, einer Analogie, einer KI-Diskussion oder einem technischen Problem entstehen. Die Antwort muss durch die Methode getragen werden, die zur jeweiligen Behauptung passt.

Das ist besonders für die persönlich motivierten Themen von MHRN entscheidend.

### 9.3 KI ist Assistenz, nicht Evidenz

Keine Behauptung wird dadurch wissenschaftlich belastbar, dass ChatGPT, DeepSeek, Qwen, Gemma, KIMI, GLM oder ein anderes Modell sie formuliert oder bestätigt hat.

KI kann

- Hypothesen erzeugen,
- Kritik formulieren,
- Literaturkandidaten finden,
- Code vorschlagen,
- Tests entwerfen,
- Texte strukturieren.

Evidenz entsteht erst durch die jeweils geeignete überprüfbare Quelle oder Messung.

### 9.4 Präregistrierung und Trennung von konfirmatorisch/explorativ

Wo ein Experiment als konfirmatorisch gelten soll, werden Hypothese, Primärmetriken, Kontraste, Erfolgsregeln und relevante Ausschluss-/Abbruchkriterien **vor** der Ergebniskenntnis fixiert.

Änderungen nach Datenkenntnis sind zulässig, müssen dann aber als explorativ oder als neue Folgestudie kenntlich gemacht werden.

### 9.5 Negative Befunde gehören zur Publikationskette

Ein Experiment, das eine erwartete Wirkung nicht zeigt, bleibt Teil der Forschung. Ein Fehlschlag wird nicht aus der Historie entfernt, nur weil er die Erzählung stört.

Das Ziel ist keine Serie positiver Resultate, sondern eine rekonstruierbare Kette von Entscheidungen und Befunden.

### 9.6 Versionierung ist Teil der Methode

Editionen, Frozen-Stände, aktuelle WIP-Fassungen und Git-Historie sind nicht bloß Softwareorganisation. Sie bilden die zeitliche Provenienz der Aussagen ab.

Die aktuelle Edition darf frühere Ergebnisse interpretieren oder korrigieren, aber einen eingefrorenen historischen Befund nicht stillschweigend umschreiben.

### 9.7 Externe Prüfung bleibt notwendig

Interne Gegenargumente, mehrere KI-Systeme und automatisierte Tests erhöhen die Prüfbreite. Sie ersetzen keine unabhängige fachliche Kritik.

MHRN muss deshalb offen bleiben für

- externe Replikation,
- Fachreview,
- statistische Kritik,
- neurowissenschaftliche Kritik,
- ethische und rechtliche Prüfung,
- sowie technische Red-Team- und Reproduzierbarkeitsprüfungen.

### 9.8 Edition-1.7-Artefakte als Kontrollstruktur

Die persönlichen Risiken dieser Selbstauskunft werden in der Edition nicht nur rhetorisch beantwortet. Die vorhandenen Artefakte übernehmen unterschiedliche Kontrollfunktionen:

- [`AUTHOR_POSITION.md`](AUTHOR_POSITION.md) — epistemologische Autorposition zu kumulativer Wissenschaft und Attribution,
- [`INTEGRITY_AND_ATTRIBUTION.md`](INTEGRITY_AND_ATTRIBUTION.md) — Regeln für Quellen, AI-Unterstützung, Selbstwiederverwendung und unverifizierte Literatur,
- [`CONTRIBUTION_MAP.md`](CONTRIBUTION_MAP.md) — Abgrenzung potenzieller Eigenbeiträge von übernommenen Grundlagen,
- [`SCIENTIFIC_STAGE_MATRIX.md`](SCIENTIFIC_STAGE_MATRIX.md) — Trennung von Entwicklungs- und Evidenzständen,
- [`REFERENCES.md`](REFERENCES.md) — Literatur- und Quellenstatus,
- [`WORK_IN_PROGRESS.md`](WORK_IN_PROGRESS.md) — sichtbar offene Arbeiten und Grenzen,
- [`MANUSCRIPT.md`](MANUSCRIPT.md) — aktuelle integrierte wissenschaftliche Darstellung.

Diese Dokumente reduzieren Bias nicht automatisch. Sie machen jedoch sichtbar, **wo ein Bias eine Aussage verändert haben könnte**.

---

## 10. Was „geliehene Intelligenz“ in dieser Arbeit bedeutet

Der Begriff **geliehene Intelligenz** beschreibt den Zugriff des Autorenkerns auf kognitive Leistungen, die nicht vollständig aus dem eigenen biologischen Gedächtnis und der eigenen unmittelbaren Verarbeitung stammen: Literatur, Suchmaschinen, Sprachmodelle, lokale Modelle, Coding-Assistenten, Softwarebibliotheken, frühere Arbeiten anderer Menschen und technische Werkzeuge.

In diesem weiten Sinn ist wissenschaftliche Arbeit grundsätzlich auf fremde Vorleistungen angewiesen. Die gegenwärtige KI-Infrastruktur macht diese Abhängigkeit nur unmittelbarer, dialogischer und schneller sichtbar.

Der Begriff darf aber nicht drei Dinge verwischen:

1. **Urheberschaft:** Ein Assistenzsystem wird nicht dadurch Mitautor, dass es Text oder Code erzeugt.
2. **Attribution:** Übernommene Gedanken, Daten, Methoden oder Texte verlieren ihre Herkunft nicht dadurch, dass sie durch ein Modell vermittelt wurden.
3. **Evidenz:** Ein Modelloutput wird nicht zur wissenschaftlichen Quelle, nur weil er nützlich oder korrekt formuliert ist.

Die wissenschaftlich präzisere Beschreibung der Schaffensart ist daher:

> **assistierte Einzelautorschaft mit verteilter kognitiver Assistenz**.

Damit bleibt die produktive Idee des „geliehenen“ Denkens erhalten, ohne Verantwortung und wissenschaftliche Autorschaft zu verwischen.

---

## 11. Verantwortung

Die Verantwortung endet nicht dort, wo ein Werkzeug beginnt.

Wenn ein KI-System eine falsche Quelle nennt und ich sie übernehme, ist die veröffentlichte Fehlangabe meine Verantwortung. Wenn ein Coding-Assistent einen Fehler erzeugt und ich ihn merge, ist der Fehler Teil meiner verantworteten Software. Wenn ein Experiment schlecht entworfen ist, wird es nicht dadurch besser, dass mehrere Modelle den Entwurf plausibel fanden.

Umgekehrt wäre es ebenfalls falsch, Assistenz zu verstecken und dadurch den Eindruck zu erzeugen, jede Formulierung, jeder Codepfad und jede Rechercheleistung sei ohne maschinelle Unterstützung entstanden.

Die richtige Position liegt zwischen diesen Extremen:

- **Assistenz offenlegen, wo sie wissenschaftlich relevant ist.**
- **Verantwortung nicht delegieren.**
- **Quellen unabhängig von der Assistenz verifizieren.**
- **Beitrag und Herkunft trennen.**
- **Unsicherheit sichtbar lassen.**

Die Selbstauskunft selbst ist deshalb Teil der Provenienz der Forschungsarbeit.

---

## 12. Was aus meiner Biografie nicht folgt

Aus meiner Biografie folgt **nicht**,

- dass MHRN biologisch plausibel ist,
- dass meine Selbstbeschreibung von ADHS/autistischer Varianz ein wissenschaftliches Modell dieser Phänomene liefert,
- dass MHRN Parkinson oder Demenz erklärt,
- dass breite technische Erfahrung fehlende neurowissenschaftliche Ausbildung ersetzt,
- dass eine funktionierende Softwarearchitektur eine Theorie des Gehirns bestätigt,
- dass viele KI-Assistenten viele unabhängige Experten ersetzen,
- dass persönliche Ausdauer wissenschaftliche Evidenz kompensiert,
- oder dass ein ungewöhnlicher Entwicklungsprozess automatisch einen ungewöhnlichen wissenschaftlichen Beitrag erzeugt.

Diese Negativabgrenzung ist zentral. Das Projekt soll nur das beanspruchen, was seine Daten und seine überprüfbaren Artefakte tragen.

---

## 13. Kernaussage

Ich bin kein Genie und beanspruche keinen institutionellen Forschungsstatus. Ich bin ein handwerklich, technisch, kaufmännisch und informationstechnisch geprägter Einzelforscher mit einem selbst beschriebenen spezifischen kognitiven Profil, persönlicher Motivation und Zugang zu einer neuen Dichte digitaler Assistenz.

Ich baue MHRN in **assistierter Einzelautorschaft mit verteilter kognitiver Assistenz**. Sprachmodelle, lokale Modelle und Coding-Assistenten erweitern meinen Such-, Prüf- und Umsetzungsraum. Sie tragen jedoch weder wissenschaftliche Verantwortung noch erzeugen sie durch ihre Zustimmung Evidenz.

Die Verantwortung für Auswahl, Behauptung, Integration und Veröffentlichung liegt bei mir.

Meine persönliche Nähe zu kognitiven Fragen ist Quelle der Motivation und zugleich mögliche Fehlerquelle. Deshalb muss MHRN stärker auf Provenienz, Präregistrierung, negative Befunde, Versionsketten, Falsifizierbarkeit und externe Kritik setzen, nicht schwächer.

Was aus MHRN wird, ist offen. Es wird sich an der Empirie entscheiden, nicht an meiner Biografie und nicht an der Vision.

Was jetzt existiert, ist eine dokumentierte Absicht, eine dokumentierte Schaffensart, eine wachsende technische Forschungsinfrastruktur und eine Verpflichtung, zwischen dem zu unterscheiden, **was gedacht, was gebaut, was gemessen und was tatsächlich gezeigt wurde**.

---

## 14. Zitierfähige Kurzform dieser Selbstauskunft

> Thomas Heisig entwickelt MHRN als unabhängiger Einzelforscher mit handwerklichem, elektrotechnischem, kaufmännischem und informationstechnischem Hintergrund sowie einem selbst beschriebenen kognitiven Profil aus ADHS mit autistischer Varianz. Die persönliche Nähe zu kognitiven Fragestellungen motiviert die Forschung, gilt aber ausdrücklich nicht als Evidenz. Die Arbeit entsteht als assistierte Einzelautorschaft mit verteilter kognitiver Assistenz: Externe Sprachmodelle, lokal betriebene Modelle und Coding-Assistenten dienen der Kritik, Strukturierung, Rechercheunterstützung und Implementierung, ohne wissenschaftliche Autorschaft oder Evidenzautorität zu übernehmen. Die Verantwortung für Auswahl, Behauptung, Integration und Veröffentlichung liegt beim menschlichen Autorenkern. MHRN behandelt diese Schaffensart selbst als provenancebezogenen Kontext und begegnet ihren Risiken durch Versionierung, Quellenprüfung, explizite Evidenzgrenzen, Präregistrierung, Veröffentlichung negativer Befunde und die Forderung nach externer Replikation und Kritik.

---

## 15. Datenschutz- und Aktualisierungshinweis

Diese Selbstauskunft konsolidiert nur Informationen, die für Rolle, Motivation und wissenschaftliche Arbeitsweise des Autors relevant sind. Sie ist **keine vollständige Biografie**.

Bewusst nicht übernommen werden personenbezogene operative Details aus anderen Lebensbereichen, insbesondere Daten über Kunden, Mitarbeitende, Minderjährige, Vereinsmitglieder, medizinische Kontakte oder sonstige Dritte.

Werkzeug- und Modelllisten beschreiben den Stand dieser Edition. Da Assistenzsysteme wechseln können, ist für konkrete wissenschaftliche oder technische Reproduzierbarkeit stets die Provenienz des jeweiligen Experiments, Commits oder Artefakts maßgeblich.

Änderungen an dieser Selbstauskunft müssen wie andere kanonische Dokumente versioniert werden. Eine spätere Änderung der persönlichen Position darf die historische Fassung dieser Edition nicht unsichtbar überschreiben.
