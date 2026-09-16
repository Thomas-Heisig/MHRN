# Stage 6 — Zwischenbilanz CL-001 bis CL-003

**Status:** DATA-only · Human Review ausstehend  
**Edition:** 1.7 (`current_wip`)  
**Datum:** 16. September 2026  
**Evidenzautorität:** keine automatische EVID-Promotion

## Gegenstand

Die Experimente CL-001, CL-002 und CL-003 bilden gemeinsam eine konsistente, aber bewusst begrenzte empirische Linie zur Rolle von Replay und semantischer Verdichtung in Stage 6.

Die Bilanz wird nicht als nachträgliche Rettung einer Hypothese formuliert. Insbesondere werden der deskriptive Dosis-Trend aus CL-003 und sekundäre 40-%-Kontraste nicht zu einem positiven Primärbefund umgedeutet.

## Drei Experimente, ein Muster

- **CL-001:** Semantik + Replay übertrifft die naive No-Replay-Baseline.
- **CL-002:** Semantik zeigt bei gematchtem Budget keinen belegten Vorteil gegenüber Raw-Replay.
- **CL-003:** Auch über die präregistrierten Dosen 5 %, 20 % und 40 % ergibt sich kein bestätigter Vorteil der semantischen Verdichtung gegenüber Raw-Replay; der präregistrierte Interaktionstest C4 bleibt negativ.

Damit ergibt sich auf DATA-Ebene folgende Eingrenzung:

1. Replay trägt zum beobachteten Nutzen gegenüber einer No-Replay-Bedingung bei.
2. Die untersuchte semantische Verdichtung zeigt unter den gematchten Bedingungen von CL-002 und CL-003 keinen bestätigten Zusatznutzen gegenüber Raw-Replay.
3. Die semantische Repräsentation ist dennoch nicht informationsleer: In CL-003 übertrifft Semantic den Random-Prototype-Control deutlich.

## CL-003 — präregistrierte Primärkontraste

CL-003 wurde genau einmal als autorisierte, freeze- und hash-gebundene Kampagne ausgeführt: 84 Runs = 12 Seeds × 7 Bedingungen. Die gespeicherten DATA und Provenienzartefakte bleiben bis zur Human-Review-Entscheidung ausdrücklich **DATA, nicht EVID**.

| Kontrast | Effekt | 95-%-Bootstrap-CI | p | Präregistrierte Entscheidung |
|---|---:|---:|---:|---|
| C1: S20 − R20 Accuracy | +2,175 pp | [0,192; 4,250] pp | 0,07275 | nicht bestanden |
| C2: R20 − S20 Forgetting | +2,745 pp | [0,250; 5,354] pp | 0,07080 | nicht bestanden |
| C3: S20 − X20 Accuracy | +14,896 pp | [14,021; 15,742] pp | 0,000488 | bestanden |
| C4: Dosisinteraktion Accuracy | +0,754 pp | [−0,288; 1,896] pp | 0,23828 | nicht bestanden |

**Klassifikation des Runners:** `H1_negative_H2_negative`.

Der deskriptive Semantic-minus-Raw-Accuracy-Unterschied wächst mit der Dosis von etwa +1,42 pp bei 5 % über +2,18 pp bei 20 % auf +3,00 pp bei 40 %. Dieser Verlauf ist eine Beobachtung, aber kein bestätigter Dosis-Effekt, weil C4 die präregistrierte Erfolgsregel nicht erfüllt.

## Bedeutung von C3

C3 ist der stärkste positive Primärbefund innerhalb von CL-003. Semantic liegt gegenüber dem Random-Prototype-Control um rund +14,9 Prozentpunkte höher.

Die zulässige Interpretation ist eng:

> Die verwendete semantische Repräsentation trägt auf DATA-Ebene relevante, nicht-zufällige Struktur.

Nicht zulässig wäre daraus abzuleiten, dass diese Struktur Raw-Replay überlegen ist. Genau diese stärkere Behauptung wird durch C1/C2/C4 nicht bestätigt.

## Stage-6-Eingrenzung

Die drei Experimente legen gemeinsam eine präzisere Arbeitshypothese nahe als die ursprüngliche Vorstellung eines eigenständigen Vorteils semantischer Verdichtung:

> Unter den bisher untersuchten Bedingungen liegt der nachweisbare Beitrag primär im Replay. Die semantische Verdichtung erhält relevante Struktur, zeigt aber bislang keinen präregistriert bestätigten Zusatznutzen gegenüber gematchtem Raw-Replay.

Diese Aussage ist bis zur Human Review eine **MHRN-Interpretation der vorhandenen DATA**, keine akzeptierte EVID-Entscheidung.

Stage 6 wird damit nicht als „gelöst“ oder als vollständig abgeschlossen bezeichnet. Für den Teilkomplex Semantization/Replay ist jedoch die Formulierung **empirisch eingegrenzt** angemessen: Eine plausible stärkere Hypothese wurde durch zwei kontrollierte Folgeexperimente begrenzt, ohne negative Resultate umzudeuten.

## Verbindlicher Entscheidungs-Gate nach der CL-003-Human-Review

Aus CL-003 wird **kein automatisches CL-004** erzeugt. Die Rollenfrage von `SemanticMemory` darf insbesondere nicht in eine offene Folge von Kompressions-, Generalisierungs-, Skalierungs- und Langzeitgedächtnisexperimenten übergehen, nur um nach einem negativen Resultat jeweils eine neue Rechtfertigung zu suchen.

Nach der Human Review fällt deshalb **zuerst eine Architektur- und Forschungsentscheidung**. Zulässig sind genau drei Pfade:

### Option A — spezialisierte Nebenrolle, keine weitere Semantikprüfung

`Raw-Replay` wird für diesen Teil von Stage 6 zur kanonischen Referenz. `SemanticMemory` bleibt als technisch vorhandener Mechanismuskandidat im Code, wird aber nicht als Kernmechanismus mit nachgewiesenem Zusatznutzen geführt. Für die aktuelle Stage-6-Linie wird keine weitere eigenständige Semantikstudie eröffnet.

### Option B — genau eine alternative Rolle, genau ein konfirmatorisches Experiment

Es wird **eine einzige** theoretisch begründete alternative Rolle ausgewählt, beispielsweise Ressourceneffizienz/Kompression. Vor jeder Implementierung werden eine neue RQ, die konkurrierenden Hypothesen, die Erfolgsgrenze und das Stopkriterium präregistriert. Der Ressourcenrahmen ist auf **eine Rolle, ein Experiment und nur die dafür notwendige minimale Instrumentierung** begrenzt.

Ist dieses Experiment negativ beziehungsweise erfüllt die präregistrierte Rechtfertigungsgrenze nicht, folgt für diese Entscheidungslinie **Option A**. Es wird nicht unmittelbar auf eine zweite `SemanticMemory`-Rolle ausgewichen.

### Option C — Rollenfrage parken

Die Rollenfrage bleibt explizit offen, wird aber nicht weiterverfolgt, bis andere Stage-6-Mechanismen — insbesondere kausaler Prediction Error und World Model — wissenschaftlich weiter geklärt sind. Eine spätere Wiederaufnahme ist nur dann gerechtfertigt, wenn aus diesen Arbeiten eine konkrete funktionale Notwendigkeit für semantische Verdichtung entsteht; bloße Verfügbarkeit eines weiteren testbaren Szenarios reicht nicht.

## Anti-Ausweichregel

Die denkbaren Rollen von `SemanticMemory` sind **kein Forschungsbacklog**. Sie bilden einen Hypothesenraum, aus dem nach der CL-003-Human-Review entweder keine weitere Rolle, genau eine Rolle oder vorerst keine weitere Prüfung gewählt wird.

Damit gilt:

1. Human Review und EVID-Entscheidung zu CL-003 zuerst;
2. danach Wahl A, B oder C;
3. bei B maximal ein neues konfirmatorisches Rollenexperiment;
4. keine serielle Rettung durch Wechsel zur jeweils nächsten Rolle;
5. negative Ergebnisse dürfen zur Reduktion eines Mechanismus führen und müssen nicht durch neue Funktionsannahmen kompensiert werden.

Ein neues Experiment darf erst aus einer danach explizit formulierten Forschungsfrage entstehen. Eine bloße Suche nach einer Bedingung, unter der die bisher nicht bestätigte Überlegenheit oder Notwendigkeit doch noch erscheint, wäre mit dem forschungsgetriebenen Entwicklungsmodus nicht vereinbar.

## Bedeutung für das Projekt

Die unmittelbare Konsequenz ist keine Entfernung von `SemanticMemory`, sondern eine Änderung seiner epistemischen Stellung. Bis zu einer anderslautenden, reviewten Evidenzentscheidung ist Raw-Replay der Referenzmechanismus für den untersuchten Continual-Learning-Teil von Stage 6; `SemanticMemory` ist ein technisch funktionsfähiger, aber hinsichtlich eines zusätzlichen Kernnutzens nicht abschließend gerechtfertigter Mechanismuskandidat.

Damit wird MHRN in diesem Bereich von Feature-Akkumulation zu **empirischer Architekturselektion** gezwungen: Ein zusätzlicher Mechanismus bleibt nicht deshalb zentral, weil er implementiert ist oder theoretisch weitere Rollen haben könnte, sondern nur, wenn eine begrenzte Forschungsentscheidung seine Rolle trägt.

## Provenienz

CL-003-DATA:

- Experiment: `EXP-S6-SEM-CL-003`
- Ausführung: 16. September 2026
- GitHub Actions Run: `35080329458`
- Runs: `84`
- Seeds: `301–312`
- Bedingungen: `R05`, `S05`, `R20`, `S20`, `X20`, `R40`, `S40`
- Ergebnisartefakt: `research/experiments/EXP-S6-SEM-CL-003/results/results.json`
- Maschinenbericht: `research/experiments/EXP-S6-SEM-CL-003/results/runner-summary.json`
- Provenienz: `research/experiments/EXP-S6-SEM-CL-003/results/EXECUTION_PROVENANCE.json`
- Status: `data_persisted_pending_human_review`

Die DATA-Hashes und das Ausführungsartefakt wurden gegen die gespeicherte Provenienz geprüft. Eine menschliche EVID-Entscheidung ist davon ausdrücklich getrennt.
