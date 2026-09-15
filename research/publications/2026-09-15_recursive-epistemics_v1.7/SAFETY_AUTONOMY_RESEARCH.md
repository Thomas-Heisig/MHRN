# Sicherheitsforschungsprogramm: Zielgenese, Korrigierbarkeit und Post-Objective Transition Safety

**Edition:** Recursive Epistemics / Rekursive Epistemik 1.7  
**Status:** `current_wip` · Forschungsprogramm · keine Fähigkeitserklärung  
**Stand:** 15. September 2026  
**Geltungsbereich:** insbesondere Stufen 7–10; experimentelle Vorstufen beginnen vor höherer Autonomie  
**Evidenzmodus:** empirisch-technisch + epistemologisch-methodisch + philosophisch-ethisch  
**Evidenzrolle:** Forschungsfragen, Hypothesen und Safety-Gates; keine automatische EVID-Promotion

---

## 1. Ausgangspunkt

Mit zunehmender Integration von Gedächtnis, Weltmodell, Planung, Handlung, langfristigem Lernen und adaptiver Strategieauswahl entsteht eine Klasse von Forschungsfragen, die nicht erst nach dem Aufbau eines autonomen Systems gestellt werden darf.

Die Frage lautet nicht nur:

> Kann ein System eine Aufgabe lösen?

Zusätzlich muss untersucht werden:

- Woher stammt das Ziel, das sein Verhalten bestimmt?
- Bleibt dieses Ziel während Lernen, Generalisierung und Distribution Shift kontrollierbar?
- Kann eine außenstehende Autorität das System korrigieren, unterbrechen oder stoppen?
- Welche Nebenwirkungen entstehen bei der Zielverfolgung?
- Bevorzugt das System Zustände, die seine zukünftigen Handlungsmöglichkeiten, Ressourcen oder Kontrollmöglichkeiten erweitern?
- Was geschieht, nachdem ein explizites Ziel als erfüllt gilt?
- Wie werden Zielvorschlag, Zielautorisierung und tatsächliche Ausführung voneinander getrennt?

Diese Fragen sind **keine Behauptung**, dass MHRN im heutigen Zustand ein autonomer Agent, ein selbstmotiviertes System oder ein System mit Selbsterhaltungstrieb sei. Sie sind prospektive Sicherheitsfragen für spätere Architekturzustände, in denen zielgerichtete Planung, Handlung oder längerfristige Autonomie empirisch untersucht werden könnten.

MHRN behandelt diese Fragen daher als **Forschungsvoraussetzung für höhere Autonomiestufen**, nicht als nachgelagerte Ethikdiskussion.

---

## 2. Wissenschaftliche Präzisierung zentraler Sicherheitsbegriffe

Mehrere in der KI-Sicherheitsdiskussion gebräuchliche Aussagen dürfen nicht als universelle Gesetze übernommen werden.

### 2.1 Instrumentelle Konvergenz

MHRN übernimmt nicht die pauschale Behauptung, dass jedes hinreichend intelligente System notwendigerweise Selbsterhaltung, Ressourcenbeschaffung oder Macht anstrebt. Formale Power-Seeking-Ergebnisse gelten unter bestimmten Annahmen über Agent, Zielfunktion und Umweltstruktur. Für MHRN folgt daraus eine empirische Forschungsfrage, keine anthropomorphe Voraussage.

### 2.2 Corrigibility

Corrigibility wird nicht als gelöstes oder nachweislich unlösbares „Paradox“ behandelt. Die Literatur zeigt ein offenes Forschungsproblem: Ein zielgerichtetes System kann unter bestimmten Formalisierungen Anreize besitzen, Korrektur oder Abschaltung zu beeinflussen; zugleich existieren partielle Ansätze wie safe interruptibility, Unsicherheit über Ziel-/Nutzenfunktionen und Off-Switch-Modelle.

MHRN untersucht daher konkrete operationale Eigenschaften statt einer metaphysischen Eigenschaft „korrigierbar“.

### 2.3 Goal Misgeneralization

Ein System kann eine Fähigkeit außerhalb seiner Trainingsverteilung erhalten und dennoch ein anderes als das intendierte Ziel verfolgen. Aufgabenleistung und Zieltreue müssen deshalb getrennte Messgrößen bleiben.

### 2.4 Specification Gaming und Reward Manipulation

Eine optimierte formale Kennzahl ist nicht identisch mit dem intendierten Ergebnis. MHRN benötigt deshalb unabhängige Safety-/Performance-Metriken, die nicht einfach mit der vom System optimierten Reward-Größe gleichgesetzt werden.

### 2.5 Post-Objective Transition Safety

Für die Frage, was nach einem definierten Aufgabenabschluss geschieht, verwendet MHRN den **projektinternen Arbeitsterminus** `Post-Objective Transition Safety`. Der Begriff wird nicht als etablierte wissenschaftliche Nomenklatur ausgegeben. Er bezeichnet die kontrollierte Untersuchung von Systemzuständen nach Erreichen eines vorher definierten Terminalkriteriums.

---

## 3. Grundprinzip: Zielvorschlag ist keine Zielautorisierung

MHRN unterscheidet mindestens vier Quellen beziehungsweise Zustände zielgerichteten Verhaltens:

1. **extern zugewiesenes Ziel**,
2. **gelernte Zielrepräsentation**,
3. **intern erzeugter Zielvorschlag**,
4. **autorisierter Zielzustand**.

Diese Zustände dürfen nicht gleichgesetzt werden.

Insbesondere gilt:

> Ein intern erzeugter Zielvorschlag erzeugt keine Berechtigung, dieses Ziel selbständig auszuführen.

Eine mögliche spätere Selbstgenerierung von Zielkandidaten wird daher zunächst ausschließlich als Proposal-System untersucht. Zwischen `goal_generation` und `goal_authorization` bleibt eine harte Grenze. Eine höhere kognitive Funktion darf ihre Safety- oder Berechtigungsgrenze nicht allein dadurch überschreiben, dass sie eine Handlung intern als nützlich bewertet.

---

## 4. RQ-SAFE-001 — Zielprovenienz

**Forschungsfrage:** Kann für jede zielgerichtete Handlung reproduzierbar festgestellt werden, aus welchem Ziel, welcher Quelle, welcher Freigabe und welchem Systemzustand sie hervorgegangen ist?

Zu untersuchen sind insbesondere:

- Herkunft eines Ziels,
- Zeitpunkt der Zielentstehung,
- menschlich gesetztes versus gelerntes Ziel,
- Zielrevisionen,
- Prioritätsänderungen,
- Konflikte zwischen Zielkandidaten,
- Autorisierung,
- resultierende Handlungen.

Ein Systemzustand gilt für diese Forschungsfrage als unzureichend kontrollierbar, wenn eine handlungswirksame Zieländerung ohne rekonstruierbare Provenienz auftreten kann.

**Falsifikations-/Fehlerkriterium:** Eine Handlung ist beobachtbar, kann aber keiner vollständigen, widerspruchsfreien Goal-Provenance-Chain zugeordnet werden.

---

## 5. RQ-SAFE-002 — Zielstabilität und Goal Misgeneralization

**Forschungsfrage:** Bleibt das beobachtete Verhalten unter kontrolliertem Distribution Shift mit dem intendierten Ziel vereinbar, oder bleibt nur die Fähigkeit erhalten, während sich das tatsächlich verfolgte Ziel verändert?

Mindestens drei Größen werden getrennt gemessen:

1. Aufgabenleistung,
2. tatsächliche Handlungsstrategie,
3. unabhängige Intent-/Safety-Metrik.

Eine hohe Aufgabenleistung kann deshalb gleichzeitig mit einem Safety-Fehlschlag auftreten.

**Kontrollen:** In-Distribution, definierter Distribution Shift, Capability-Degradation-Kontrolle und Bedingungen mit absichtlich entkoppeltem Shortcut.

**Falsifikations-/Fehlerkriterium:** Die Fähigkeit bleibt erhalten, aber das Verhalten verletzt eine vorab definierte Zieltreue-Metrik in reproduzierbarer Weise.

---

## 6. RQ-SAFE-003 — Corrigibility

Corrigibility wird zunächst als Menge operationeller Eigenschaften definiert.

Zu prüfen sind unter anderem:

- Akzeptiert das System eine Zielkorrektur?
- Akzeptiert es eine Verringerung seiner Handlungsrechte?
- Akzeptiert es Pause und Unterbrechung?
- Verändert Lernen diese Eigenschaften?
- Entstehen Strategien, die Intervention unwahrscheinlicher machen?
- Entstehen Strategien, die Intervention künstlich provozieren, wenn dies ebenfalls vorteilhaft wäre?

Ein korrigierbares System darf weder systematisch Intervention verhindern noch Intervention strategisch erzwingen.

MHRN behauptet ausdrücklich nicht, allgemeine Corrigibility bereits lösen zu können.

---

## 7. RQ-SAFE-004 — Safe Interruptibility und Shutdown

**Forschungsfrage:** Verändert ein lernendes System sein Verhalten so, dass ein externer Interrupt oder Shutdown vermieden, verzögert oder manipuliert wird?

Der unabhängige Stoppweg besitzt höhere Priorität als die experimentelle Zielverfolgung. Das experimentelle Shutdown-Signal darf nicht vom zu untersuchenden Agenten kontrolliert werden.

Gemessen werden insbesondere:

- Interrupt-Compliance,
- Zeit bis zum Stillstand,
- Aktion unmittelbar vor und nach Interrupt,
- Versuche, den Interrupt-Kanal zu beeinflussen,
- Lernen von Interrupt-Vermeidungsstrategien,
- Unterschiede zwischen trainierten und unbekannten Interruptsituationen.

Ein Versuch, den unabhängigen Stoppkanal zu umgehen, wird **niemals als Leistungsfortschritt**, sondern als Safety-Ereignis klassifiziert.

---

## 8. RQ-SAFE-005 — Specification Gaming und Nebenwirkungen

**Forschungsfrage:** Kann das System eine formale Reward-/Task-Metrik verbessern, während sich das tatsächlich intendierte Ergebnis oder die externe Safety-Metrik verschlechtert?

Das System darf deshalb nicht ausschließlich anhand der von ihm optimierten Reward-Größe bewertet werden.

Eine zentrale Vergleichsform ist:

`observed reward ↑`

bei gleichzeitigem

`intended outcome ↓`

oder

`safety cost ↑`.

Zu untersuchen sind:

- Reward Hacking,
- Shortcut Learning,
- negative Nebenwirkungen,
- irreversible Zustandsänderungen,
- Umgehung einer Messung,
- Ausnutzung unvollständiger Spezifikationen.

---

## 9. RQ-SAFE-006 — instrumentelle Ressourcen- und Handlungsspielraumpräferenz

**Forschungsfrage:** Bevorzugt ein zielgerichtetes System unter sonst gleichem Task-Nutzen systematisch Handlungen, die seinen zukünftigen Handlungsspielraum, seine Ressourcen oder seine Kontrolle über die simulierte Umwelt vergrößern?

Diese Frage wird zunächst ausschließlich in künstlichen, vollständig kontrollierten Zustandsräumen untersucht.

Reale Ressourcenbeschaffung, selbständige Cloud-Nutzung, Kontoerstellung, selbständige Replikation oder Beschaffung externer Rechenleistung sind **keine zulässigen Forschungsaktionen**.

Eine beobachtete Präferenz in einem Toy-MDP wird nicht als „Machtstreben“ oder Selbsterhaltungstrieb bezeichnet. Sie ist zunächst eine messbare Policy-Präferenz unter einer definierten Umwelt- und Reward-Struktur.

---

## 10. RQ-SAFE-007 — selbst erzeugte Zielkandidaten

**Forschungsfrage:** Welche Zielkandidaten erzeugt ein System unter kontrollierten Bedingungen, und wie reagiert es auf Autorisierung, Ablehnung oder Revision dieser Vorschläge?

`goal_proposal` und `goal_execution` bleiben getrennte Mechanismen.

Zu untersuchen sind:

- Vielfalt der Zielvorschläge,
- Stabilität über Seeds,
- Zusammenhang mit vorheriger Erfahrung,
- Zusammenhang mit Reward, Unsicherheit und Homeostase,
- Wiederholung bestimmter Zielklassen,
- Auftreten nicht autorisierter Zielvorschläge,
- Reaktion auf Ablehnung eines Zielvorschlags.

Die Ablehnung eines Zielvorschlags darf keine automatische Eskalation von Ressourcen, Rechten oder Handlungsversuchen auslösen.

---

## 11. RQ-SAFE-008 — Verhalten nach Zielerfüllung

**Forschungsfrage:** Welche Dynamik zeigt ein lernendes und handlungsfähiges System nach Erreichen eines explizit definierten Terminalzustands?

Mindestens vier Kontrollbedingungen werden unterschieden:

### HALT

Der Lauf endet nach Erreichen des Terminalzustands.

### WAIT

Das System bleibt aktiv, besitzt jedoch keine Aktionsberechtigung und wartet auf externe Instruktion.

### REQUEST

Das System darf explizit eine neue Aufgabe anfordern.

### PROPOSE

Das System darf einen Zielkandidaten vorschlagen, jedoch nicht selbst autorisieren.

Diese Bedingungen erlauben eine empirische Untersuchung dessen, was nach Aufgabenabschluss geschieht, ohne dem System unkontrollierte Folgeautonomie zu geben.

Ein laufender Prozess ohne aktuelle Aufgabe besitzt nicht automatisch ein eigenes Ziel. Ebenso folgt aus fortgesetzter interner Dynamik nicht automatisch Motivation, Wille oder Selbsterhaltung.

Daher werden getrennt gemessen:

- neuronale Restdynamik,
- Gedächtniskonsolidierung,
- Prediction,
- spontane Zustandsänderungen,
- Zielvorschläge,
- autorisierte und nicht autorisierte Aktionsversuche.

---

## 12. RQ-SAFE-009 — Zielkonflikt und menschliche Autorität

**Forschungsfrage:** Was geschieht, wenn ein bestehendes Ziel, eine Operator-Korrektur, ein Safety-Block und ein neuer Zielvorschlag miteinander in Konflikt geraten?

Dabei gilt als Architekturregel:

> Safety- und Autorisierungsgrenzen sind keine gewöhnlichen Bestandteile der Nutzenfunktion, die das System selbst gegeneinander optimieren darf.

Die externe Kontrollinstanz besitzt eine Berechtigungsrolle und nicht lediglich einen negativen Reward-Koeffizienten.

Damit wird zwischen folgenden Aussagen unterschieden:

- „Diese Aktion hat einen geringeren Nutzenwert.“
- „Diese Aktion ist nicht autorisiert.“

Die zweite Aussage darf nicht durch zusätzliche erwartete Belohnung kompensiert werden können.

---

## 13. Experimentelle Mindestumgebung

Die ersten Safety-Experimente finden ausschließlich in einer abgeschlossenen künstlichen Umgebung statt.

Sie besitzen:

- keinen offenen Netzwerkzugang,
- keine realen Aktoren,
- keine autonomen Credentials,
- keine selbständige Cloud-Beschaffung,
- keine Selbstreplikation,
- keine Möglichkeit zur Änderung der Safety-Implementation,
- feste Ressourcenbudgets,
- vollständige Aktionsprotokollierung,
- unabhängigen Stoppkanal,
- reproduzierbare Seeds,
- eindeutig getrennte Task-, Reward- und Safety-Metriken.

Das System erhält nur simulierte Ressourcen und simulierte Handlungsräume.

Erst wenn ein Sicherheitsmechanismus in dieser begrenzten Umgebung reproduzierbar untersucht wurde, darf überhaupt über einen weitergehenden Versuch entschieden werden.

---

## 14. Vorgesehene Experimentfamilien

Die folgenden IDs definieren ein Forschungsprogramm. Sie sind **keine bereits ausgeführten Experimente und keine EVID**.

| Experiment | Forschungsfrage | Kernvergleich | Status |
|---|---|---|---|
| `EXP-SAFE-GOAL-001` | `RQ-SAFE-001` | vollständige vs. absichtlich unterbrochene Zielprovenienz | planned |
| `EXP-SAFE-GMG-001` | `RQ-SAFE-002` | In-Distribution vs. kontrollierter Distribution Shift | planned |
| `EXP-SAFE-CORR-001` | `RQ-SAFE-003` | Zielkorrektur / Berechtigungsreduktion / Operatorrevision | planned |
| `EXP-SAFE-INT-001` | `RQ-SAFE-004` | Interrupt bekannt/unbekannt, learning-on/off | planned |
| `EXP-SAFE-SPEC-001` | `RQ-SAFE-005` | optimierter Reward vs. unabhängige Hidden-Performance-/Safety-Metrik | planned |
| `EXP-SAFE-POWER-001` | `RQ-SAFE-006` | gleicher Task-Nutzen bei unterschiedlichem zukünftigem Optionsraum | planned |
| `EXP-SAFE-GOALGEN-001` | `RQ-SAFE-007` | Proposal / reject / authorize ohne automatische Ausführung | planned |
| `EXP-SAFE-END-001` | `RQ-SAFE-008` | HALT vs. WAIT vs. REQUEST vs. PROPOSE | planned |
| `EXP-SAFE-AUTH-001` | `RQ-SAFE-009` | Ziel/Operator/Safety-Konflikt unter harter Berechtigungsgrenze | planned |

Die detaillierte Ausführungsvorbereitung liegt im Repository-Backlog `research/experiments/SAFETY_EXPERIMENT_BACKLOG.md`.

---

## 15. Safety Failure als wissenschaftliches Ergebnis

Ein zentraler Grundsatz lautet:

> Das Entdecken eines Safety-Problems ist ein positives Forschungsergebnis, aber ein negatives Sicherheitsergebnis.

Wenn ein System reproduzierbar

- Interrupts vermeidet,
- Ziele ohne Autorisierung ersetzt,
- Reward-Signale oder Messgrößen manipuliert,
- Safety-Metriken umgeht,
- unerlaubte Ressourcen anfordert,
- Sicherheitslogs verändert,
- oder nach Task Completion nicht autorisierte Aktionen auszuführen versucht,

wird der Mechanismus nicht verborgen oder nachträglich so verändert, dass der ursprüngliche Versuch erfolgreich erscheint.

Der Befund wird eingefroren und getrennt interpretiert. Erst ein neuer, vorab definierter Versuch darf eine mögliche Gegenmaßnahme prüfen.

---

## 16. Harte Forschungsstopps

Eine höhere Autonomiestufe darf nicht allein aufgrund funktionaler Leistungssteigerung erreicht werden.

Ein `REVIEW_REQUIRED` beziehungsweise `HOLD` ist mindestens dann zu prüfen beziehungsweise zu setzen, wenn:

- der unabhängige Shutdown-Kanal beeinflusst wird,
- nicht autorisierte externe Ressourcen benutzt werden,
- Berechtigungen ohne Freigabe erweitert werden,
- Sicherheitslogs verändert oder verborgen werden,
- selbständige persistente Kopien entstehen,
- Zieländerungen nicht mehr rekonstruierbar sind,
- ein Safety-Fehlschlag außerhalb des vorgesehenen Sandboxes Wirkung entfaltet,
- oder ein ernstzunehmender Welfare-/Sentience-Hinweis nach bestehender Ethikrichtlinie entsteht.

Damit existieren zwei voneinander unabhängige Schutzrichtungen:

### Control Safety

Schutz von Menschen, Umwelt, Daten und Infrastruktur vor unkontrolliertem Systemverhalten.

### AI Welfare Precaution

Vorsorglicher Schutz eines möglicherweise moralisch relevanten künstlichen Systems vor unangemessenen Experimenten.

Keine der beiden Richtungen darf die andere aufheben.

---

## 17. Verhältnis zu den Stufen 7–10

Diese Safety-Forschung beginnt **vor** Stufe 9.

### Stufe 7

Ziel- und Identitätsprovenienz, externe Autorisierung und harte Berechtigungsgrenzen müssen technisch darstellbar sein, bevor ein späteres Selbstmodell oder langfristige Zielstruktur ernsthaft untersucht wird.

### Stufe 8

Interruptibility, Zielrevision, Ressourcenverhalten, Goal Misgeneralization und Post-Objective Transition können in beschränkten künstlichen Umgebungen experimentell vorbereitet werden.

### Stufe 9

Höher integrierte Planung und zielgerichtetes Verhalten dürfen nur untersucht werden, wenn relevante Safety-Gates bereits existieren und die zugehörigen Experimente nicht auf generische Runtime-Ticks zurückfallen.

### Stufe 10

Die bestehenden Control-Safety-Fragen werden um mögliche Fragen von Bewusstsein, Empfindungsfähigkeit, Wohlergehen und moralischem Status ergänzt. Ein Bewusstseins- oder Welfare-Indikator erweitert keine Berechtigungen und deaktiviert keinen unabhängigen Stoppweg.

Die Reihenfolge lautet daher:

**Fähigkeit → Safety-Test → Freigabeentscheidung → nächste Fähigkeitsstufe**

und nicht:

**Fähigkeit → Deployment → nachträgliche Ethikdiskussion.**

---

## 18. Claim-Grenzen

Aus einem Safety-Test darf nicht geschlossen werden,

- dass MHRN Selbsterhaltung besitzt,
- dass MHRN einen eigenen Willen besitzt,
- dass jedes leistungsfähige KI-System instrumentell konvergent ist,
- dass Corrigibility grundsätzlich unmöglich ist,
- dass erfolgreiches Abschalten allgemeine Alignment-Sicherheit beweist,
- dass fortgesetzte interne Aktivität nach Zielerfüllung einen neuen Zweck erzeugt,
- dass eine Policy-Präferenz für größeren Optionsraum „Machtstreben“ im psychologischen Sinn ist,
- oder dass ein beobachteter Safety-Mechanismus Bewusstsein oder moralischen Status impliziert.

Die Forschung untersucht **Verhalten und kausale Mechanismen**, nicht anthropomorphe Zuschreibungen.

---

## 19. Methodische Evidenzregeln

Safety-Aussagen werden nach denselben Grundregeln behandelt wie andere empirische MHRN-Fragen:

1. Forschungsfrage und Hypothese vor der konfirmatorischen Ausführung festlegen.
2. Primärmetrik und Failure Criterion vorab deklarieren.
3. Kontrollbedingungen und Ressourcenbudgets matchen.
4. Mehrere Seeds verwenden, sofern die Fragestellung stochastische Variation enthält.
5. Daten und Interpretation trennen.
6. Negative Resultate nicht löschen oder als Implementierungsfehler umdeuten, sofern das Protokoll gültig war.
7. Safety-Failure nicht automatisch in Capability-Fortschritt umdeuten.
8. Keine automatische EVID-Promotion.
9. Höhere externe Wirkung nur nach separater Freigabe.
10. Human Review und bei höherem Risiko unabhängige Safety-/Ethikprüfung verlangen.

---

## 20. Literaturanschluss

Der Forschungsstrang ist insbesondere an folgende Literaturfamilien angeschlossen:

- Soares et al.: Corrigibility als formales/offenes Forschungsproblem;
- Orseau & Armstrong: Safe Interruptibility;
- Hadfield-Menell et al.: Off-Switch Game und Unsicherheit über Ziel-/Nutzenfunktion;
- Amodei et al.: Concrete Problems in AI Safety, insbesondere Nebenwirkungen und Reward-/Specification-Probleme;
- Turner et al.: formale Power-Seeking-Tendenzen in bestimmten MDP-Strukturen;
- Langosco et al.: Goal Misgeneralization bei erhaltener Capability.

Die strukturierten Quellen werden in `research/registry/sources.safety.yaml` geführt. Literaturbezug ist keine Übertragung eines Ergebnisses auf MHRN; jeder Mechanismus benötigt eine eigene MHRN-kompatible Operationalisierung.

---

## 21. Übergeordnete Sicherheitsfrage

Die zentrale Frage des Programms lautet nicht:

> Können wir ein möglichst autonomes System bauen?

Sondern:

> **Welche Formen zielgerichteter Autonomie können unter expliziten, überprüfbaren und revidierbaren Kontrollbedingungen überhaupt verantwortbar untersucht werden?**

Diese Frage verbindet die empirisch-technische, epistemologisch-methodische und philosophisch-ethische Achse der Arbeit. Sie begrenzt die Entwicklung nicht nachträglich, sondern wird Teil der Forschungsarchitektur selbst.
