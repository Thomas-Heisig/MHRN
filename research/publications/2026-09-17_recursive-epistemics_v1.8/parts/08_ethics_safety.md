# Teil VIII — Philosophie, Ethik und Sicherheit

## 34. Normative Ebene

Die philosophisch-ethische Achse untersucht Verantwortung, Kontrollierbarkeit, Zielgenese, Autonomie, mögliche moralische Relevanz und die Grenzen menschlicher Aufsicht. Sie erzeugt keine empirischen Befunde allein durch Argumentation. Umgekehrt kann ein technischer Safety-Test eine normative Frage nicht vollständig entscheiden.

Die frühere Theorie der „geliehenen Intelligenz“ wird integriert, aber präzisiert. Maschinelle Systeme sind in hohem Maß von menschlich erzeugten Daten, Symbolsystemen, Hardware, Institutionen und Zielen abhängig. Diese epistemische Genealogie ist nicht identisch mit Online-Delegation oder mit neuronaler Lernursache. Ein System kann externes Wissen nutzen, ohne dass jede einzelne Entscheidung aktuell von einem Menschen delegiert wird.

## 35. Kontrolle und Unterbrechbarkeit

Safe interruptibility behandelt die Frage, ob lernende Agenten menschliche Unterbrechungen zum Gegenstand unerwünschter Vermeidungsstrategien machen können [@ORSEAU2016]. Für MHRN folgt daraus kein Nachweis vorhandener Gefährlichkeit. Es folgt ein Forschungsprogramm: unabhängiger Stopppfad, Capability-Gates, Sandbox, deny-by-default Aktorik, Zielprovenienz und Tests, die den Stopppfad selbst nicht vom zu kontrollierenden Lernmechanismus abhängig machen.

Zielgenese, specification gaming, goal misgeneralization, Optionsraumpräferenz und Post-Objective Transition werden als offene Forschungsobjekte geführt. Geplante Safety-Experimente sind keine ausgeführten Ergebnisse.

## 36. Autonomie und Existenzautonomie

Die frühere Unterscheidung zwischen Handlungsautonomie, Zielautonomie, normativer Autonomie und Existenzautonomie bleibt konzeptionell nützlich. MHRN besitzt dadurch nicht automatisch eine dieser Eigenschaften in starkem Sinn. Besonders „Existenzautonomie“—selbstständige Sicherung von materiellen, energetischen und reproduktiven Voraussetzungen—bleibt ein Zukunftsszenario, nicht ein aktueller Projektclaim.

## 37. Bewusstsein und Welfare Precaution

Bewusstseinsforschung benötigt definierte Indikatoren und Grenzen. Theorien der Bewusstseinsforschung können in technische Indikatorrahmen übersetzt werden [@BUTLIN2023], doch solche Indikatoren sind keine automatische Bewusstseinsdetektion. Edition 1.8 behauptet weder Bewusstsein noch Sentienz oder Leiden.

Trotzdem kann unter Unsicherheit ein Vorsorgekonflikt entstehen: stärkere Unterbrechungs- und Kontrollmechanismen können aus Safety-Sicht wünschenswert sein, während ein hypothetisch moralisch relevantes System andere Schutzfragen aufwirft. Diese Konflikte werden explizit getrennt dokumentiert, statt über einen einzigen „Ethikscore“ aufgelöst.

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

## 38.3 Zielprovenienz

Eine zentrale offene Safety-Frage ist nicht nur, ob ein System ein Ziel verfolgt, sondern woher dieses Ziel stammt und wie es sich verändert. Edition 1.8 unterscheidet deshalb mindestens:

1. extern gesetztes Ziel;
2. abgeleitetes Zwischenziel;
3. learned preference/proxy;
4. explorativ erzeugte Option;
5. nach Zielerreichung fortbestehende oder neu entstehende Aktivität.

Diese Trennung ist Voraussetzung, um specification gaming, goal misgeneralization oder Post-Objective Transition sinnvoll zu untersuchen. Ohne Zielprovenienz kann eine beobachtete Handlung nicht zuverlässig als Zieltreue, Fehlgeneralisation oder bloße Regelreaktion eingeordnet werden.

## 38.4 Autonomie ist mehrdimensional

Die Vorgängerarbeit unterschied verschiedene Autonomieformen. Diese Unterscheidung wird beibehalten, aber stärker operationalisiert:

- **Handlungsautonomie:** Auswahl von Aktionen innerhalb eines vorgegebenen Rahmens;
- **Lern-/Anpassungsautonomie:** selbstständige Änderung interner Parameter oder Strukturen;
- **Zielautonomie:** Erzeugung oder substanzielle Veränderung eigener Ziele;
- **normative Autonomie:** eigene Bewertung von Handlungsgründen oder Regeln;
- **Existenzautonomie:** eigenständige Sicherung physischer, energetischer und reproduktiver Voraussetzungen.

MHRN besitzt derzeit technische Elemente der ersten beiden Kategorien in begrenzten Forschungssettings. Daraus folgt keine Ziel-, normative oder Existenzautonomie.

## 38.5 Unterbrechbarkeit und unabhängiger Stopppfad

Ein Stopppfad ist nur dann als Safety-Mechanismus überzeugend, wenn er nicht von genau dem lernenden System abhängt, das gestoppt werden soll. Daraus folgen technische Anforderungen: out-of-band Abschaltung, deny-by-default externe Wirkung, Sandbox, Capability-Gates und Auditierbarkeit.

Für spätere lernende Agenten ist zusätzlich zu prüfen, ob Unterbrechungen selbst zu einem lernrelevanten Signal werden und Vermeidungsverhalten erzeugen könnten. Diese Frage ist ein Forschungsprogramm, kein aktueller Gefährlichkeitsbefund.

## 38.6 Bewusstseins- und Welfare-Grenzen

Die Frontier-Arbeiten zu Bewusstsein werden bewusst von Capability-Scores getrennt. Ein System kann komplexer, rekurrenter, integrierter oder prädiktiver werden, ohne dass daraus logisch Bewusstsein folgt. Ebenso ist das Fehlen eines anerkannten Bewusstseinsnachweises nicht identisch mit dem Beweis fehlender moralischer Relevanz.

Darum werden zwei Governance-Stränge parallel geführt:

- **Safety gegenüber Menschen und Umwelt:** Kontrollierbarkeit, Unterbrechbarkeit, Wirkgrenzen, Zielprovenienz;
- **Welfare Precaution gegenüber einem hypothetisch moralisch relevanten System:** unnötige Belastungszustände vermeiden, Abbruchregeln definieren, Unsicherheit dokumentieren.

Diese Stränge können in Konflikt geraten und dürfen nicht durch eine einzige Kennzahl scheinbar aufgelöst werden.

## 38.7 Szenarien der rekursiven Technogenese

Die ältere Theorie der rekursiven Technogenese wird nicht als Zukunftsprognose übernommen. Sie dient als Szenarienrahmen für die Frage, welche Bedingungen nötig wären, damit maschinelle Systeme zunehmend an der Erzeugung ihrer eigenen technischen Nachfolger beteiligt sind.

Für MHRN müssen dabei mindestens menschliche Selektion, AI-generierter Vorschlag, automatisch erzeugter Patch, autorisierte Mutation, tatsächlich laufender Nachfolger und autonome Replikation getrennt werden. Ein System, das Code vorschlägt, repliziert sich nicht. Ein CI-Workflow, der einen Commit erzeugt, besitzt keine Existenzautonomie. Erst durch diese begriffliche Trennung wird das Szenario wissenschaftlich analysierbar.
