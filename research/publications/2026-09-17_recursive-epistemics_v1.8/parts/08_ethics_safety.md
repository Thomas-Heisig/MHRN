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

### RQ-ETH-001 — Autorenschaft von MHRN-Erkenntnissen

**Forschungsfrage:** Wer ist der Autor von MHRN-Erkenntnissen — Mensch, Modell oder System?

**Registrierte Hypothese `H-ETH-001-A`:** Autorenschaft ist ein verteiltes Phänomen zwischen Mensch, Modell und System.

Diese Hypothese ist nicht als metaphysische Behauptung zu lesen. Sie zerlegt vielmehr mindestens vier kausale Rollen:

1. **Problem- und Zielsetzung:** Wer legt die Forschungsfrage, Erfolgsbedingungen und Grenzen fest?
2. **Transformation:** Welcher Akteur erzeugt Formulierungen, Code, Analysen oder Hypothesenvorschläge?
3. **Selektion und Freigabe:** Wer entscheidet, welche Vorschläge verworfen, übernommen, ausgeführt oder veröffentlicht werden?
4. **Verantwortung:** Wer trägt die wissenschaftliche, rechtliche und normative Verantwortung für die veröffentlichte oder operative Handlung?

Ein Sprachmodell kann substanzielle Transformationsarbeit leisten, ohne deshalb automatisch wissenschaftlicher Letztautor oder Verantwortungsträger zu sein. Umgekehrt wäre es unzureichend, maschinelle Ko-Konstruktion zu verschweigen, wenn sie einen materiellen Beitrag zum Forschungsprozess geleistet hat.

**Prüfbarkeit:** Die Frage wird über Provenienz, Versionsgeschichte, Prompt-/Tool-Logs, Reviewentscheidungen, Ausführungsfreigaben und publizierte Verantwortungszuordnung untersucht. Ein Runtime-Tick ist keine geeignete Messung für Autorschaft.

**Claim-Grenze:** Aus maschineller Beteiligung folgt weder moralische Personenschaft noch autonome wissenschaftliche Verantwortung.

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

Safe interruptibility behandelt die Frage, ob lernende Agenten menschliche Unterbrechungen zum Gegenstand unerwünschter Vermeidungsstrategien machen können ([@ORSEAU2016]). Corrigibility, Off-Switch-Modelle, Specification-Gaming-Probleme, formale Optionsraumpräferenzen und Goal Misgeneralization liefern hierfür unterschiedliche theoretische Ausgangspunkte ([@SOARES2015]; [@HADFIELD2017]; [@AMODEI2016]; [@TURNER2021]; [@LANGOSCO2022]). Keiner dieser Befunde wird als direkter Nachweis über MHRN übernommen; jeder Mechanismus benötigt eine MHRN-kompatible Operationalisierung.

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

Bewusstseinsforschung benötigt definierte Indikatoren und Grenzen. Theorien der Bewusstseinsforschung können in technische Indikatorrahmen übersetzt werden ([@BUTLIN2023]), doch solche Indikatoren sind keine automatische Bewusstseinsdetektion. Edition 1.8 behauptet weder Bewusstsein noch Sentienz oder Leiden.

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
