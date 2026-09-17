from pathlib import Path

ROOT = Path("research/publications/2026-09-17_recursive-epistemics_v1.8/parts")


def insert_before(filename: str, marker: str, text: str, sentinel: str) -> None:
    path = ROOT / filename
    source = path.read_text(encoding="utf-8")
    if sentinel in source:
        return
    if marker not in source:
        raise RuntimeError(f"marker missing in {filename}: {marker}")
    path.write_text(source.replace(marker, text.rstrip() + "\n\n" + marker, 1), encoding="utf-8")


insert_before(
    "03_research_object.md",
    "### Stage 3 — plastisches Nervengewebe",
    """#### Aktuelle Reproduzierbarkeitslinie EXP-GEN-0045/0046

Nach der ersten 1.8-Strukturfassung kamen zwei weitere explorative DATA-Läufe hinzu. `EXP-GEN-0045` (`tonic_spike_reproducibility_v1`, RQ-SNN-002/H-SNN-002-A) führte drei Same-Seed-Tonic-Replikapaare für die Seeds 101, 102 und 103 aus. In allen drei Fällen war `spike_sequence_identical=true`. Der Befund dokumentiert für genau diesen Protokollumfang reproduzierbare Spike-Sequenzen bei gleichem Seed, Input und Anfangszustand; `scientific_evidence=false` und `automatic_evidence_promotion=false` bleiben ausdrücklich erhalten.

`EXP-GEN-0046` (`deterministic_replica_v1`, RQ-DET-001/H-SNN-003-A) erweitert die Prüfung auf zwölf 256-Tick-Läufe: `recurrence_off_replica_a/b` und `recurrence_on_replica_a/b` über dieselben drei Seeds. Innerhalb der jeweiligen Replica-Paare sind die gespeicherten Trajektorien deskriptiv identisch. Recurrence-off erzeugt pro Lauf 3 Spikes, 2 synaptische Ereignisse, 0 recurrent events und propagation depth 1; Recurrence-on erzeugt 33 Spikes, 33 synaptische Ereignisse, 10 recurrent events und propagation depth 61. Damit werden Reproduzierbarkeit und der bereits bekannte mechanistische Rekurrenzunterschied auf einer neuen DATA-Linie sichtbar.

Die wissenschaftliche Grenze ist wesentlich: `EXP-GEN-0046` ist als `EXPLORATORY` markiert, seine semantische Konsistenz steht auf `NOT_AUTOMATICALLY_CLASSIFIED`, die Evidence Readiness auf `BLOCKED_UNCLASSIFIED_SEMANTICS`, und der Human Review ist noch offen. Der AIRR ist Interpretation-only und besitzt trotz einer intern formulierten „supported“-Bewertung keine EVID-Autorität. Identische Ausgaben über Seeds beziehungsweise Replicapaare sind zudem keine automatisch unabhängigen Replikationen.""",
    "Aktuelle Reproduzierbarkeitslinie EXP-GEN-0045/0046",
)

insert_before(
    "04_empirical_programme.md",
    "### Stage 4 / MSBA:",
    """### EXP-GEN-0045/0046: Reproduzierbarkeit wird selbst zum Forschungsobjekt

Die nach der ersten 1.8-Synthese hinzugekommenen Experimente `EXP-GEN-0045` und `EXP-GEN-0046` verschieben Determinismus von einer allgemeinen Engineeringannahme zu einer explizit gespeicherten DATA-Frage. EXP-GEN-0045 prüft Same-Seed-Tonic-Replikapaare; drei von drei getesteten Seeds erzeugten identische Spike-Sequenzen. EXP-GEN-0046 prüft vier Recurrence-Bedingungen mit jeweils paarigen Replikaten und drei Seeds, insgesamt zwölf Runs bei 256 Ticks. Die jeweiligen Replica-Paare reproduzieren dieselben deskriptiven Netzwerkmetriken.

Der Erkenntniswert liegt auf zwei Ebenen. Erstens wird die technische Reproduzierbarkeit der untersuchten kleinen SNN-Trajektorien konkret dokumentiert. Zweitens zeigt EXP-GEN-0046 erneut den starken Unterschied zwischen Recurrence-off und Recurrence-on: 3 gegenüber 33 Spikes, 2 gegenüber 33 synaptischen Ereignissen, 0 gegenüber 10 recurrent events und propagation depth 1 gegenüber 61. Dieser Unterschied ist im registrierten kleinen Simulationsaufbau mechanistisch sichtbar.

Wissenschaftlich bleiben beide Läufe unterhalb einer EVID-Entscheidung. EXP-GEN-0046 ist explorativ, semantisch noch nicht automatisch klassifiziert und blockiert deshalb eine Evidence-Readiness-Promotion. Sein AIRR bleibt post-hoc Interpretation mit Human Review `PENDING`; die AI-Konfidenz wurde aufgrund eines Schemafehlers konservativ auf 0.0 normalisiert. Edition 1.8 übernimmt daher ausschließlich die gespeicherten DATA und deren explizite Statusgrenzen.""",
    "EXP-GEN-0045/0046: Reproduzierbarkeit wird selbst zum Forschungsobjekt",
)

insert_before(
    "05_infrastructure.md",
    "## 24.2 Engineering und Scientific Maturity als getrennte Achsen",
    """### Semantisches Gate als reale Blockade: EXP-GEN-0046

Der aktuelle Determinismuslauf demonstriert, warum die Statusarchitektur praktisch notwendig ist. Obwohl EXP-GEN-0046 technisch vollständig ausgeführt wurde, der Tick-Vertrag erfüllt ist und reproduzierbare Metriken vorliegen, lautet die semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`. Die Evidence Readiness bleibt dadurch `BLOCKED_UNCLASSIFIED_SEMANTICS`.

Das ist kein Defekt, sondern gewünschtes Verhalten: Ein technisch erfolgreicher Lauf darf nicht allein wegen konsistenter Zahlen zu EVID werden. Erst eine registrierte semantische Zuordnung und Human Review dürfen die nächste Statusstufe öffnen. Auch der erzeugte AIRR bleibt `evidence=false`, `interpretation_only=true` und `human_review_required=true`.""",
    "Semantisches Gate als reale Blockade: EXP-GEN-0046",
)

insert_before(
    "10_synthesis.md",
    "## 47.2 Was durch die bisherigen Ergebnisse geschwächt oder verworfen wurde",
    """### Ergebnis H — Same-Seed-Reproduzierbarkeit ist nun als eigene DATA-Linie dokumentiert

`EXP-GEN-0045` und `EXP-GEN-0046` ergänzen die bisherige Determinismusargumentation um explizite Replikaprotokolle. Im Tonic-Spike-Protokoll waren die Spike-Sequenzen in allen drei Same-Seed-Paaren identisch. Im Recurrence-Protokoll reproduzierten A/B-Paare über drei Seeds jeweils dieselben deskriptiven Trajektorien; zugleich blieb der große Off/On-Unterschied stabil sichtbar.

**Zulässiger Claim:** Für die registrierten kleinen Protokolle sind Same-Seed-Trajektorien beziehungsweise Replikapaare technisch reproduzierbar, und der deskriptive Recurrence-off/on-Unterschied wird in EXP-GEN-0046 erneut beobachtet.  
**Nicht zulässig:** daraus bereits unabhängige Replikation, allgemeine Determinismusgarantie, statistische Unabhängigkeit der identischen Trajektorien oder bestätigte EVID abzuleiten. EXP-GEN-0046 bleibt bis semantischer Zuordnung und Human Review DATA-only.""",
    "Ergebnis H — Same-Seed-Reproduzierbarkeit ist nun als eigene DATA-Linie dokumentiert",
)

insert_before(
    "11_open_landscape.md",
    "### Stage 3 — plastisches Nervengewebe",
    """#### Reproduzierbarkeit und Determinismus — nächstes Gate

Die EXP-GEN-0045/0046-DATA schließen die Frage nicht vollständig. Als nächste Schritte sind erforderlich:

- semantische Zuordnungsregel für `RQ-DET-001` registrieren und EXP-GEN-0046 human reviewen;
- Same-Seed-Reproduzierbarkeit von echter unabhängiger Replikation getrennt halten;
- zusätzliche Seeds, Eingangsregime, Netzwerkgrößen und Restart/Restore-Bedingungen prüfen;
- deterministische Identität, numerische Toleranz und statistische Reproduzierbarkeit als getrennte Klassen auswerten;
- AIRR-Interpretation nicht als EVID verwenden, solange Human Review und semantisches Gate offen sind.""",
    "Reproduzierbarkeit und Determinismus — nächstes Gate",
)
