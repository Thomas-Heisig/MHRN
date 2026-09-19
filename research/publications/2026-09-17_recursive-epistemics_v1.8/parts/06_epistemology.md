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

Die außerhalb des Repositories wiedergewonnenen Chat-Zusammenfassungen sind in [`chat_reconstruction.json`](../sources/chat_reconstruction.json) bewusst S4. Wenn später Originaltranskripte eingebunden werden, entstehen neue Provenienzeinträge; die frühere S4-Rekonstruktion wird nicht stillschweigend in eine stärkere Quelle umgeschrieben.

## 27. KI-assistierte Forschung

KI-Unterstützung erzeugt eine zusätzliche Beitrags- und Provenienzdimension. Ein Vorschlag eines Assistenten ist nicht automatisch eine Idee des Autors; eine vom Autor verlangte Richtung ist nicht automatisch eine implementierte Funktion; ein generierter Patch ist nicht automatisch ein wissenschaftlicher Befund.

Seit der Verdichtung von `RQ-ETH-001` reicht deshalb die frühere lineare Kette `user requirement → AI proposal → human decision → commit → run → review → publication synthesis` allein nicht mehr aus. Sie wird als Ereignisfolge beibehalten, aber zusätzlich nach epistemischen Rollen codiert:

- **Konzeptualisierung** — Forschungsfrage, Ziel, Hypothese, Erfolgs- oder Abbruchbedingung;
- **Generierung/Transformation** — Text, Code, Analyse, Kontrollidee oder methodische Variante;
- **Validierung** — Quellen-, Code-, Mess-, Statistik- oder Konsistenzprüfung;
- **Selektion/Kanonisierung** — Übernahme, Revision, Verwerfung, DATA-/EVID-Zuordnung oder Veröffentlichung;
- **Verantwortung** — natürliche Person, die für den veröffentlichten Claim Rechenschaft übernimmt.

Das operative Beitragsmodell liegt in [`RQ_ETH_001_PROVENANCE_STUDY.md`](../../../protocols/RQ_ETH_001_PROVENANCE_STUDY.md). Materieller epistemischer Beitrag, formale Autorenschaft und wissenschaftliche Verantwortung bleiben getrennte Variablen.

Die Arbeit nutzt KI zugleich als Forschungsgegenstand und als Arbeitsinstrument. Das erhöht das Risiko **rekursiver Bestätigungsfehler**: Ein Modell kann frühere eigene Formulierungen wiederfinden, paraphrasieren und dadurch wie eine zweite Quelle wirken. Gegenmaßnahmen sind unter anderem source-bound Originalquellen, getrennte Quellennähe- und Herkunftsklassen, Literaturquarantäne bis zur Prüfung, AI-Provenienzfelder und menschliche Review-Gates. Eine Modellwiederholung zählt nicht als unabhängige Bestätigung.

## 28. Falsifikation von Entstehungs- und Prioritätsaussagen

Auch Schaffensgeschichte muss revidierbar sein. Eine Behauptung wie „Idee X entstand zuerst am Datum Y“ ist nur zulässig, wenn das Artefakt den Inhalt tatsächlich trägt und die untersuchte Quellenmenge keinen älteren widersprechenden Fund enthält. Selbst dann ist zwischen **frühestem dokumentierten Nachweis** und **tatsächlichem Entstehungszeitpunkt** zu unterscheiden.

Edition 1.8 behauptet daher keine absolute Priorität für die rekonstruierten Vor-Repo-Ideen. Sie dokumentiert die **früheste derzeit wiedergewonnene Spur** innerhalb des tatsächlich geprüften Korpus. Neue ältere Primärartefakte revidieren die Chronologie additiv; sie machen die frühere Rekonstruktion nicht zu wissenschaftlichem Fehlverhalten.

## 28.1 Epistemische Regeln aus konkreten Korrekturereignissen

Die Methodik dieser Arbeit ist nicht nur programmatisch gesetzt. Mehrere Regeln wurden durch konkrete Fehlinterpretationen oder stärkere Kontrollen notwendig. Diese Fälle sind **methodische Zeugen**: Sie zeigen, dass eine Regel als Reaktion auf dokumentierte Probleme eingeführt wurde. Sie beweisen noch nicht, dass die Regel die Fehlerquote künftig kausal reduziert.

### Ein negatives Resultat setzt Testadäquanz voraus

Für `H-SNN-003-B` wurde `EXP-GEN-0047` zunächst leicht als Topologie-/Dimensions-Nullbefund lesbar. Die spätere methodische Entscheidung [`2026-09-17_snn003_topology_propagation_v1_adequacy.md`](../../../decisions/2026-09-17_snn003_topology_propagation_v1_adequacy.md) klassifiziert den Lauf dagegen als **`INADEQUATE_TO_TEST_HYPOTHESIS`**: drei Neuronen und zwei Feed-forward-Synapsen ließen die Koordinatenmanipulation den behaupteten Mechanismus nicht hinreichend verändern.

Die zulässige Schlussfolgerung ist daher nicht „5D/Topologie hat keinen Effekt“, sondern „dieses Design war für den intendierten Effekt nicht ausreichend sensitiv“.

**Regel:** Vor Bestätigung, Nullbefund oder Falsifikation muss geprüft werden, ob die manipulierte Variable den behaupteten kausalen Mechanismus tatsächlich verändern konnte.

### DATA und Report sind verschiedene Objekte

Die Human Review [`EXP-GEN-0036/analysis/HUMAN-REVIEW-2026-09-16.md`](../../../experiments/EXP-GEN-0036/analysis/HUMAN-REVIEW-2026-09-16.md) dokumentiert einen Reportingfehler: Gedankenstriche in universellen Summary-Spalten wurden zunächst als fehlende DATA gelesen, obwohl protokollspezifische Runs und Statistiken existierten.

**Regel:** Ein Report ist eine Transformation von DATA und damit ein eigenes fehlerfähiges Objekt. Bei claim-relevanten Unstimmigkeiten müssen source-bound Rohartefakte, protokollspezifische Statistik und Manifest vor der Interpretation geprüft werden.

### Eine positive Baseline-Differenz ist noch keine Mechanismusidentifikation

`EXP-S6-SEM-CL-001` zeigte unter seinem Protokoll Semantic+Replay gegenüber No-Replay. Die stärkere Präregistrierung [`EXP-S6-SEM-CL-002.md`](../../../preregistrations/EXP-S6-SEM-CL-002.md) führte gematchtes Raw-Replay ein. Unter dieser Kontrolle wurde kein konfirmatorischer Zusatznutzen semantischer Prototypen bestätigt. `CL-003` prüfte anschließend eine Dosisalternative; der präregistrierte Interaktionstest bestätigte keinen Dosis-Effekt, obwohl deskriptive Unterschiede verlockend stärker formuliert werden konnten.

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

Präregistrierung trennt prospektive Hypothesenprüfung von nachträglicher Musterdeutung; diese Funktion wird auch in der methodischen Literatur als zentraler Zweck beschrieben ([@NOSEK2018]). Für MHRN lautet die zusätzliche Regel: **Eine spätere bessere Erklärung darf den eingefrorenen ursprünglichen Erfolgsmaßstab nicht umschreiben.**

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

Das operative Design wird in [`RQ_EPIST_002_PROCESS_GOVERNANCE_STUDY.md`](../../../protocols/RQ_EPIST_002_PROCESS_GOVERNANCE_STUDY.md) versioniert. Es ist zunächst **Protokolldesign, nicht präregistriert und nicht zur konfirmatorischen Ausführung autorisiert**.

## 28.8 Gegenwärtiger Ergebnisstand der epistemologischen Achse

Der aktuell belegbare Befund ist enger als „die Governance verbessert Wissenschaft“:

1. Es existieren dokumentierte Korrekturereignisse, bei denen stärkere Kontrollen oder source-bound Prüfung die zulässige Interpretation verändert haben.
2. Aus diesen Ereignissen wurden dauerhafte technische und dokumentarische Regeln abgeleitet.
3. Die Prozessarchitektur ist dadurch **formal restriktiver und auditierbarer** geworden.
4. Noch nicht gezeigt ist, dass diese Architektur über Fälle oder Reviewer hinweg die Fehlklassifikationsrate kausal senkt.

Die bisherigen Fälle stützen damit die **Notwendigkeit einer Prozessstudie**, nicht bereits deren positives Ergebnis.

**Zwischenfazit.** Rekursive Epistemik besitzt einen empirisch anschlussfähigen methodischen Kern, sobald ihre Selbstbeschreibung in prüfbare Ereignisse und Vergleichsdesigns übersetzt wird. Der wissenschaftliche Gegenstand ist dann nicht „wir arbeiten sorgfältiger“, sondern: Welche Status-, Provenienz- und Revisionsdarstellung führt unter kontrollierten Bedingungen zu welchen Entscheidungen?
