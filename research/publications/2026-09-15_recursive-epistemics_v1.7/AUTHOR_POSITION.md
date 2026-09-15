# Worte des Autors — kumulative Wissenschaft, freier Wissenstransfer und Attribution

**Status:** Autorposition, redaktionell aus dem Gespräch in wissenschaftlich belastbarere Form übertragen.  
**Funktion:** epistemologische Position und Forschungsprinzip; keine empirische Evidenz und keine juristische Definition von Plagiat.

## Ausgangspunkt

Der Autor vertritt die Auffassung, dass wissenschaftliche Erkenntnis grundsätzlich **kumulativ** entsteht. Forschung beginnt niemals bei null. Begriffe, Methoden, mathematische Werkzeuge, sprachliche Formen, technische Verfahren und Denkfiguren werden übernommen, verändert, kombiniert und weitergegeben. In diesem weiten epistemischen Sinn ist individuelle Urheberschaft an einer Idee stets begrenzt: Erkenntnis entsteht in einem historischen und sozialen Netz von Vorarbeiten.

Die zugespitzte Formulierung, „sämtliche Forschung ist Plagiat, und das ist gut so“, soll in dieser Arbeit deshalb **nicht** als Billigung akademischen Fehlverhaltens verstanden werden. Sie benennt vielmehr eine Spannung zwischen kollektivem Wissen und institutionellen Regeln der Zuschreibung.

## Zwei Bedeutungen müssen getrennt werden

| Ebene | Gemeint ist | Bewertung in MHRN |
|---|---|---|
| **epistemisch** | Wissen ist kumulativ; Ideen bauen auf vorhandenen Begriffen, Methoden und Beobachtungen auf | grundlegende Voraussetzung wissenschaftlicher Arbeit |
| **institutionell/verfahrensbezogen** | fremde Texte, Daten, Code, Methoden oder zurechenbare Ideen werden ohne hinreichende Kennzeichnung als eigene Leistung dargestellt | wissenschaftlich unzulässig, weil Provenienz und Nachprüfbarkeit zerstört werden |

Der entscheidende Punkt ist damit nicht ein vermeintliches Eigentum an Wahrheit. Entscheidend ist die **Nachvollziehbarkeit der Wissensproduktion**. Quellenangaben, Versionen, Datenprovenienz und Abgrenzungen eigener Beiträge erlauben anderen Forschenden zu prüfen,

- wo eine Behauptung herkommt,
- welche Voraussetzungen übernommen wurden,
- ob eine Quelle später korrigiert oder widerlegt wurde,
- welche Transformation MHRN selbst vorgenommen hat,
- und an welcher Stelle eine Replikation oder Kritik ansetzen muss.

Die praktische Regel lautet daher:

> Wissen soll möglichst frei zirkulieren; seine Herkunft soll dabei möglichst sichtbar bleiben.

Freier Wissenstransfer und strikte Attribution sind keine Gegensätze. Je freier eine Arbeit weiterverwendbar sein soll, desto wichtiger wird ihre Provenienz.

## Konsequenz für MHRN

MHRN darf etablierte oder fremde Mechanismen verwenden, kombinieren und experimentell verändern. Dazu zählen beispielsweise Izhikevich-/LIF-Modelle, STDP, Drei-Faktor-Plastizität, Complementary Learning Systems, Predictive-Coding-Ansätze, Replay/Konsolidierung, World-Model-Methoden, Gateway- und Accelerator-Techniken oder externe Evaluationsverfahren. Für jede solche Übernahme gelten jedoch fünf Pflichten:

1. **Quelle sichtbar machen.** Primärquellen und belastbare Sekundärquellen werden getrennt von bloßen Suchtreffern oder unbestätigten Hinweisen geführt.
2. **Übernahme und Eigenentwicklung trennen.** Eine bekannte Theorie wird nicht dadurch zur Eigenleistung, dass sie in MHRN implementiert wird.
3. **Transformation dokumentieren.** Abweichungen, Erweiterungen, technische Randbedingungen und neue Kombinationen müssen nachvollziehbar sein.
4. **Neuheit nicht behaupten, bevor sie geprüft ist.** Eine ungewöhnliche Kombination ist zunächst eine potenzielle Eigenleistung, keine bewiesene wissenschaftliche Neuheit.
5. **Unsicherheit veröffentlichen.** Ungeklärte Herkunft, widersprüchliche Literatur oder fehlende Prior-Art-Recherche werden sichtbar als offen markiert.

Unbestätigte Begriffe oder Quellen — darunter in früheren Entwürfen etwa `ArithSpec` als vermeintlich normativer Standard — dürfen nicht dadurch wissenschaftliche Autorität erhalten, dass sie häufig wiederholt werden. Sie bleiben in Quellenquarantäne, bis ihre Provenienz geklärt ist.

## Hat MHRN einen eigenen Beitrag?

Der Autor beansprucht in dieser Fassung **keinen Durchbruch**. Die wissenschaftlich sinnvollere Frage lautet: Welche Beiträge sind klar benennbar, prüfbar und von der übernommenen Grundlage unterscheidbar?

Drei Kandidaten verdienen eine gezielte Neuheitsprüfung:

### 1. Trennung von vier Ordnungsbegriffen

MHRN trennt konzeptionell:

- `Logical Identity` — welches logische neuronale/synaptische Objekt gemeint ist,
- `Physical Slot` — wo dieses Objekt in einer konkreten Speicherrepräsentation liegt,
- `Synaptic Reduction` — in welcher wohldefinierten Reihenfolge parallele Beiträge zusammengeführt werden,
- `Execution Scheduling` — wann und auf welchem Backend Operationen tatsächlich ausgeführt werden.

Diese Trennung soll Reproduzierbarkeit von Performance-Optimierung entkoppeln. **Ob die Viererteilung als solche neu ist, ist nicht festgestellt.** Der belastbare Beitrag liegt zunächst in ihrer expliziten, implementierbaren und testbaren Verwendung innerhalb von MHRN.

### 2. Proposal → Approval → Mutation → Journal → Undo

Strukturelle Plastizität wird nicht als unprotokollierter direkter Eingriff behandelt. Änderungen können als Vorschlag entstehen, eine Freigabegrenze durchlaufen, als Mutation ausgeführt, journalisiert und unter definierten Bedingungen rückgängig gemacht werden. Damit werden biologische Inspirationsmechanismen mit einem auditierbaren Engineering-Vertrag verbunden.

Auch hier gilt: **Die wissenschaftliche Neuheit gegenüber allen existierenden Frameworks ist offen.** Geprüft werden muss, welche verwandten transaktionalen, event-sourced oder reversiblen Ansätze bereits existieren.

### 3. Content Gateway und Compute Backend

MHRN behandelt die Frage „welche Information gelangt über eine Grenze?“ getrennt von „auf welcher Hardware oder durch welches Modell wird eine Berechnung ausgeführt?“. Ein Content Gateway kann daher semantische/neurale Inhalte und Provenienz regeln, während ein Compute Backend CPU, GPU, externe Dienste oder andere Ausführungsressourcen betrifft.

Die Trennung ist konzeptionell nützlich für Kausalität, Sicherheit und Experimentkontrolle. **Auch sie wird in 1.7 als potenzieller Beitrag und nicht als bereits bewiesene Prioritätsbehauptung geführt.**

## Was als Beitrag ausreicht

Wissenschaftlicher Fortschritt muss kein spektakulärer Durchbruch sein. Beiträge können bestehen aus:

- einer präziseren Begriffsbildung,
- einer reproduzierbaren Implementierung,
- einer systematischen Synthese bisher getrennter Methoden,
- einem besseren Mess- oder Kontrollverfahren,
- einer negativen oder falsifizierenden Beobachtung,
- einer Infrastruktur, die strengere Experimente ermöglicht,
- oder einer klaren Dokumentation dessen, was **nicht** gezeigt wurde.

MHRN soll daher nicht durch maximale Neuheitsrhetorik legitimiert werden, sondern durch die Qualität der Abgrenzung, der Experimente und der Reproduzierbarkeit.

## Konsequenz des freien Wissenstransfers

Wer Wissen möglichst frei verfügbar machen will, muss akzeptieren, dass andere es übernehmen, verändern und weiterentwickeln. Die wissenschaftliche Gegenleistung ist nicht Kontrolle über die Idee, sondern sichtbare Provenienz und die Möglichkeit, an einer überprüfbaren Entwicklungslinie teilzunehmen.

Die praktische Strategie dieser Arbeit lautet deshalb:

1. **Aufschreiben, was übernommen wurde.**
2. **Aufschreiben, was MHRN selbst entwickelt oder kombiniert hat.**
3. **Aufschreiben, wo Neuheit und Herkunft unklar sind.**
4. **Daten, negative Befunde und Methoden zugänglich halten, soweit rechtlich und ethisch zulässig.**
5. **Andere zur Replikation, Kritik und Weiterentwicklung befähigen.**

Diese Haltung ersetzt keine Zitierregeln. Sie begründet, warum diese Regeln für ein offenes Forschungsprojekt besonders wichtig sind.

## Wissenschaftshistorischer Hinweis

Die häufig mit Robert K. Merton verbundenen Normen wissenschaftlicher Praxis — gemeinschaftliche Wissensorientierung, Universalismus, Uneigennützigkeit/Desinteresse und organisierter Skeptizismus — sind für diese Position ein wichtiger Bezugspunkt. Historische Formulierungen, Prioritätsfragen und die oft Newton zugeschriebene Metapher vom „Stehen auf den Schultern von Riesen“ werden in der endgültigen Einreichungsfassung anhand zitierfähiger Primär- bzw. wissenschaftshistorischer Quellen nachgeprüft. Diese WIP-Fassung macht daraus noch keinen Quellenbeweis.
