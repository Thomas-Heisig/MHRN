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

## Forschungsentscheidung vor einem CL-004

Aus CL-003 wird **kein automatisches CL-004** erzeugt. Vor einer weiteren Variantenstudie sind zunächst erforderlich:

1. Human Review der CL-003-DATA und der präregistrierten Analyse;
2. gemeinsame Stage-6-Bilanz von CL-001, CL-002 und CL-003;
3. Entscheidung, ob semantische Verdichtung als eigenständiger Mechanismus unter neuen, theoretisch begründeten Ressourcen-/Kompressionsbedingungen weiter geprüft werden soll oder ob der Forschungsfokus auf Replay und andere Mechanismen verschoben wird.

Ein neues Experiment darf erst aus einer danach explizit formulierten Forschungsfrage entstehen. Eine bloße Suche nach einer Bedingung, unter der die bisher nicht bestätigte Überlegenheit doch noch erscheint, wäre mit dem forschungsgetriebenen Entwicklungsmodus nicht vereinbar.

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
