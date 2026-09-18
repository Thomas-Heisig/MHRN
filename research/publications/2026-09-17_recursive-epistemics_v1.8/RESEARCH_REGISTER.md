# Forschungsfragen, Hypothesen und Claims — Registry-Projektion

Die Originalobjekte werden vollständig und ohne Statusänderung wiedergegeben. RQ-, Hypothesen- und Claim-Status bleiben getrennt. Fehlende Zuordnungen werden nicht erfunden.

## CLAIM-5D-001

Typ: `claim`; Quellstatus: `untested`; Quelle: [research/registry/claims.yaml](../../registry/claims.yaml), JSON-Pointer `/2`.

```json
{
  "id": "CLAIM-5D-001",
  "claim": "Die fünfdimensionale Organisation verbessert die Robustheit gegenüber lokalen Strukturverlusten.",
  "research_question": "RQ-5D-001",
  "hypothesis": "H-5D-001-A",
  "evidence": [],
  "experiments": [],
  "sources": [],
  "status": "untested",
  "confidence": "none",
  "required_evidence": [
    "dimensional_ablation",
    "damage_experiment",
    "statistical_replication"
  ],
  "minimum_runs": 30,
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## CLAIM-5D-002

Typ: `claim`; Quellstatus: `untested`; Quelle: [research/registry/claims.yaml](../../registry/claims.yaml), JSON-Pointer `/3`.

```json
{
  "id": "CLAIM-5D-002",
  "claim": "5D-Netzwerke zeigen eine höhere Informationskapazität als niedrigdimensionale Netzwerke gleicher Neuronenzahl.",
  "research_question": "RQ-5D-004",
  "hypothesis": "H-5D-004-A",
  "evidence": [],
  "experiments": [],
  "sources": [],
  "status": "untested",
  "confidence": "none",
  "required_evidence": [
    "information_capacity_measurement",
    "dimensional_ablation",
    "statistical_replication"
  ],
  "minimum_runs": 20,
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## CLAIM-AIR-001

Typ: `claim`; Quellstatus: `untested`; Quelle: [research/registry/claims.yaml](../../registry/claims.yaml), JSON-Pointer `/7`.

```json
{
  "id": "CLAIM-AIR-001",
  "claim": "Ein standardisiertes ResearchPacket verbessert die Identifikation vorab definierter methodischer Fehler gegenüber einem unstrukturierten Experimentbericht.",
  "research_question": "RQ-AIR-001",
  "hypothesis": "H-AIR-001-A",
  "evidence": [],
  "experiments": [],
  "sources": [],
  "status": "untested",
  "confidence": "none",
  "required_evidence": [
    "structured_vs_unstructured_comparison",
    "held_out_goldstandard",
    "per_defect_class_metrics"
  ],
  "minimum_runs": 30,
  "created": "2026-09-02",
  "updated": "2026-09-02"
}
```

## CLAIM-DET-001

Typ: `claim`; Quellstatus: `inconclusive`; Quelle: [research/registry/claims.yaml](../../registry/claims.yaml), JSON-Pointer `/5`.

```json
{
  "id": "CLAIM-DET-001",
  "claim": "Brain-5D erzeugt bei identischem Seed, Input und Anfangszustand deterministisch identische Spike-Abfolgen und Netzwerkzustände.",
  "research_question": "RQ-DET-001",
  "hypothesis": "H-SNN-003-A",
  "evidence": [
    "EVID-2026-03",
    "EVID-2026-05",
    "EVID-2026-07",
    "EVID-2026-09",
    "EVID-2026-11",
    "EVID-2026-13",
    "EVID-2026-15"
  ],
  "experiments": [
    "EXP-DET-0001",
    "EXP-DET-0001",
    "EXP-DET-0001",
    "EXP-DET-0001",
    "EXP-DET-0001",
    "EXP-DET-0001",
    "EXP-DET-0001",
    "EXP-DET-0001",
    "EXP-DET-0001",
    "EXP-DET-0001"
  ],
  "sources": [],
  "status": "inconclusive",
  "confidence": "low",
  "required_evidence": [
    "ab_restore_identity",
    "fresh_process_restore_identity",
    "rng_state_persistence"
  ],
  "minimum_runs": 10,
  "created": "2026-08-23",
  "updated": "2026-08-31"
}
```

## CLAIM-SELF-001

Typ: `claim`; Quellstatus: `untested`; Quelle: [research/registry/claims.yaml](../../registry/claims.yaml), JSON-Pointer `/6`.

```json
{
  "id": "CLAIM-SELF-001",
  "claim": "In Brain-5D entstehen spontan funktionale Module ohne explizite Programmierung.",
  "research_question": "RQ-SELF-001",
  "hypothesis": "H-SELF-001-A",
  "evidence": [],
  "experiments": [],
  "sources": [],
  "status": "untested",
  "confidence": "none",
  "required_evidence": [
    "module_detection",
    "control_comparison",
    "statistical_replication"
  ],
  "minimum_runs": 30,
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## CLAIM-SNN-001

Typ: `claim`; Quellstatus: `untested`; Quelle: [research/registry/claims.yaml](../../registry/claims.yaml), JSON-Pointer `/0`.

```json
{
  "id": "CLAIM-SNN-001",
  "claim": "Pair-based STDP erzeugt unter definierten Pre/Post-Zeitabständen eine asymmetrische Gewichtsanpassung.",
  "research_question": "RQ-SNN-004",
  "hypothesis": "H-SNN-004-A",
  "evidence": [],
  "experiments": [],
  "sources": [
    "SRC-SONG-ABBOTT-2000",
    "SRC-BI-POO-1998"
  ],
  "status": "untested",
  "confidence": "none",
  "required_evidence": [],
  "minimum_runs": 10,
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## CLAIM-STDP-001

Typ: `claim`; Quellstatus: `untested`; Quelle: [research/registry/claims.yaml](../../registry/claims.yaml), JSON-Pointer `/1`.

```json
{
  "id": "CLAIM-STDP-001",
  "claim": "Pair-based STDP erzeugt unter definierten Pre/Post-Zeitabständen eine asymmetrische Gewichtsanpassung.",
  "research_question": "RQ-STDP-001",
  "hypothesis": "H-STDP-001-A",
  "evidence": [],
  "experiments": [],
  "sources": [
    "SRC-SONG-ABBOTT-2000",
    "SRC-BI-POO-1998"
  ],
  "status": "untested",
  "confidence": "none",
  "required_evidence": [
    "pair_timing_curve",
    "statistical_replication"
  ],
  "minimum_runs": 10,
  "created": "2026-09-02",
  "updated": "2026-09-02"
}
```

## CLAIM-STOR-001

Typ: `claim`; Quellstatus: `inconclusive`; Quelle: [research/registry/claims.yaml](../../registry/claims.yaml), JSON-Pointer `/4`.

```json
{
  "id": "CLAIM-STOR-001",
  "claim": "Das .b5d-Format ermöglicht verlustfreie Serialisierung und Deserialisierung des vollständigen Netzwerkzustands.",
  "research_question": "RQ-STORAGE-001",
  "hypothesis": "H-STOR-001-A",
  "evidence": [
    "EVID-2026-04",
    "EVID-2026-06",
    "EVID-2026-08",
    "EVID-2026-10",
    "EVID-2026-12",
    "EVID-2026-14",
    "EVID-2026-16"
  ],
  "experiments": [
    "EXP-STOR-0001",
    "EXP-STOR-0001",
    "EXP-STOR-0001",
    "EXP-STOR-0001",
    "EXP-STOR-0001",
    "EXP-STOR-0001",
    "EXP-STOR-0001",
    "EXP-STOR-0001",
    "EXP-STOR-0001",
    "EXP-STOR-0001"
  ],
  "sources": [],
  "status": "inconclusive",
  "confidence": "low",
  "required_evidence": [
    "serialize_deserialize_roundtrip",
    "state_equality_check"
  ],
  "minimum_runs": 10,
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-5D-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/14`.

```json
{
  "id": "H-5D-001-A",
  "research_question": "RQ-5D-001",
  "hypothesis": "Ein 5D-angeordnetes Netzwerk zeigt signifikant andere Dynamik als ein 2D/3D-Netzwerk gleicher Neuronenzahl.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-5D-002-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/15`.

```json
{
  "id": "H-5D-002-A",
  "research_question": "RQ-5D-002",
  "hypothesis": "Die Signalpropagationszeit und -reichweite skaliert mit der Dimensionalität des Netzwerks.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-5D-003-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/16`.

```json
{
  "id": "H-5D-003-A",
  "research_question": "RQ-5D-003",
  "hypothesis": "5D-Netzwerke entwickeln eine höhere Modularität als niedrigdimensionale Netzwerke.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-5D-004-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/17`.

```json
{
  "id": "H-5D-004-A",
  "research_question": "RQ-5D-004",
  "hypothesis": "Die zusätzlichen Dimensionen in 5D sind informationstragend und nicht redundant.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-5D-005-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/37`.

```json
{
  "id": "H-5D-005-A",
  "research_question": "RQ-5D-005",
  "hypothesis": "Mindestens eine registrierte Propagationsmetrik unterscheidet sich in 5D von topology-matched niedrigdimensionalen Einbettungen.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## H-AIR-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/32`.

```json
{
  "id": "H-AIR-001-A",
  "research_question": "RQ-AIR-001",
  "hypothesis": "Ein Scientific Research Assistant mit strukturiertem ResearchPacket erkennt vorab definierte methodische Defekte mit höherem F1-Score als dasselbe Modell mit einem unstrukturierten Experimentbericht.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-02",
  "updated": "2026-09-02"
}
```

## H-EMB-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/27`.

```json
{
  "id": "H-EMB-001-A",
  "research_question": "RQ-EMB-001",
  "hypothesis": "Brain-5D kann in einer geschlossenen Sensor-Aktor-Schleife zielgerichtet agieren.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-EPIST-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/31`.

```json
{
  "id": "H-EPIST-001-A",
  "research_question": "RQ-EPIST-001",
  "hypothesis": "Systemerkenntnis und Forschererkenntnis sind in Brain-5D kategorial unterscheidbar.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-ETH-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/29`.

```json
{
  "id": "H-ETH-001-A",
  "research_question": "RQ-ETH-001",
  "hypothesis": "Die Autorenschaft von Brain-5D-Erkenntnissen ist ein verteiltes Phänomen zwischen Mensch, Modell und System.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-ETH-002-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/30`.

```json
{
  "id": "H-ETH-002-A",
  "research_question": "RQ-ETH-002",
  "hypothesis": "Die Kontrolle über Brain-5D-Experimente liegt primär beim Entwickler, nicht beim automatisierten System.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-GEN-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/35`.

```json
{
  "id": "H-GEN-001-A",
  "research_question": "RQ-GEN-001",
  "hypothesis": "Learning-on verbessert die Erfolgsrate auf vorab registrierten Perturbationsproben gegenüber Learning-off und Sham-Replay.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## H-HOM-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/12`.

```json
{
  "id": "H-HOM-001-A",
  "research_question": "RQ-HOM-001",
  "hypothesis": "Synaptische Homeostase hält die mittlere Feuerrate eines SNN innerhalb eines definierten Sollbereichs.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-HOM-002-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/13`.

```json
{
  "id": "H-HOM-002-A",
  "research_question": "RQ-HOM-002",
  "hypothesis": "Homeostase und STDP wirken synergistisch: Homeostase verhindert STDP-induzierte Drift.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-LIFE-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/42`.

```json
{
  "id": "H-LIFE-001-A",
  "research_question": "RQ-LIFE-001",
  "hypothesis": "Sequenzielle Lernaufgaben zeigen eine messbare Veränderung der Retentions- oder Gewichtssignatur gegenüber einer Single-Task-Baseline.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## H-LLM-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/28`.

```json
{
  "id": "H-LLM-001-A",
  "research_question": "RQ-LLM-001",
  "hypothesis": "Ein Language Organ kann SNN-Zustände in sinnvolle natürliche Sprache übersetzen.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-MEM-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/26`.

```json
{
  "id": "H-MEM-001-A",
  "research_question": "RQ-MEM-001",
  "hypothesis": "Brain-5D kann Informationen über synaptische Gewichte speichern und auf Input-Muster abrufen.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-PERF-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/40`.

```json
{
  "id": "H-PERF-001-A",
  "research_question": "RQ-PERF-001",
  "hypothesis": "Der Core-Tick-Loop ist nicht der einzige dominante Kostenblock vollständiger Science-Läufe; mindestens ein zusätzlicher gemessener Subsystemanteil ist relevant.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## H-PING-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/6`.

```json
{
  "id": "H-PING-001-A",
  "research_question": "RQ-PING-001",
  "hypothesis": "Identische Impulse erzeugen bei identischem Anfangszustand dieselbe beobachtete Response-Signatur.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-03",
  "updated": "2026-09-03"
}
```

## H-REC-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/34`.

```json
{
  "id": "H-REC-001-A",
  "research_question": "RQ-REC-001",
  "hypothesis": "Rekurrenzgewicht und Delay erzeugen reproduzierbare Übergänge zwischen sofortigem Erlöschen, transienter Aktivität und Aktivität bis zum Ende des registrierten Beobachtungsfensters.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## H-REC-002-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/41`.

```json
{
  "id": "H-REC-002-A",
  "research_question": "RQ-REC-002",
  "hypothesis": "Größere rekurrente Delays verändern Persistenzdauer oder Propagation Depth gegenüber dem Delay-1-Kontrollarm.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## H-REG-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/9`.

```json
{
  "id": "H-REG-001-A",
  "research_question": "RQ-REG-001",
  "hypothesis": "Chronischer Druck erhöht deterministisch Resource Pressure und Thermal Threat, während unbekannte Telemetrie Unsicherheit erhält.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-03",
  "updated": "2026-09-03"
}
```

## H-REG-002-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/38`.

```json
{
  "id": "H-REG-002-A",
  "research_question": "RQ-REG-002",
  "hypothesis": "Der registrierte Regulationsfeedbackpfad verbessert die Recovery-Metrik nach einer identischen Druckphase gegenüber Regulation-off.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## H-REPL-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/36`.

```json
{
  "id": "H-REPL-001-A",
  "research_question": "RQ-REPL-001",
  "hypothesis": "Der Rekurrenzbehandlungseffekt bleibt über mindestens 20 vorab registrierte Initialisierungsseeds in Richtung und Größenordnung konsistent.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## H-SCALE-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/22`.

```json
{
  "id": "H-SCALE-001-A",
  "research_question": "RQ-SCALE-001",
  "hypothesis": "Brain-5D skaliert von 5.000 auf 1.000.000 Neuronen ohne qualitative Änderung der Spikedynamik.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-SELF-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/23`.

```json
{
  "id": "H-SELF-001-A",
  "research_question": "RQ-SELF-001",
  "hypothesis": "In Brain-5D entstehen spontan funktionale Cluster durch lokale STDP-Regeln.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-SELF-002-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/24`.

```json
{
  "id": "H-SELF-002-A",
  "research_question": "RQ-SELF-002",
  "hypothesis": "Die beobachtete Selbstorganisation ist emergent und nicht durch die Architektur vorgegeben.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-SNN-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/0`.

```json
{
  "id": "H-SNN-001-A",
  "research_question": "RQ-SNN-001",
  "hypothesis": "Brain-5D erzeugt über mindestens 100.000 Simulations-Ticks stabile Spike-Dynamiken ohne numerische Drift.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-SNN-002-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/1`.

```json
{
  "id": "H-SNN-002-A",
  "research_question": "RQ-SNN-002",
  "hypothesis": "Das Izhikevich-Neuronenmodell erzeugt bei identischem Input reproduzierbare Spikefolgen.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-SNN-003-A

Typ: `hypothesis`; Quellstatus: `supported`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/2`.

```json
{
  "id": "H-SNN-003-A",
  "research_question": "RQ-DET-001",
  "hypothesis": "Bei gleichem Seed, Input und Anfangszustand sind Spike-Abfolgen deterministisch identisch.",
  "status": "supported",
  "evidence": [
    "EVID-2026-03",
    "EVID-2026-05",
    "EVID-2026-07",
    "EVID-2026-09",
    "EVID-2026-11",
    "EVID-2026-13",
    "EVID-2026-15"
  ],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-SNN-003-B

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/3`.

```json
{
  "id": "H-SNN-003-B",
  "research_question": "RQ-SNN-003",
  "hypothesis": "Unter gleicher Neuronenzahl, Dichte und Stimulusbedingung unterscheiden sich Propagationslatenz oder -reichweite zwischen mindestens zwei vorab definierten Topologien; ein Vorteil einer 5D-Anordnung wird nicht vorausgesetzt.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-11",
  "updated": "2026-09-11"
}
```

## H-SNN-004-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/4`.

```json
{
  "id": "H-SNN-004-A",
  "research_question": "RQ-SNN-004",
  "hypothesis": "STDP führt zu einer meßbaren asymmetrischen Verschiebung der synaptischen Gewichtsverteilung.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-SNN-005-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/5`.

```json
{
  "id": "H-SNN-005-A",
  "research_question": "RQ-SNN-005",
  "hypothesis": "Ein Netzwerk mit STDP zeigt signifikant bessere Lernleistung als ein Netzwerk ohne STDP.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-SNN-006-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/43`.

```json
{
  "id": "H-SNN-006-A",
  "research_question": "RQ-SNN-006",
  "hypothesis": "Alle zehn vorab registrierten, unterschiedlichen seed-gebundenen Parameterrealisierungen bleiben ueber 100.000 Ticks numerisch und topologisch stabil; unter gepaartem Tonic-Drive bleibt die post-burn-in Aktivitaet positiv mit CV und relativer Drift jeweils <= 0.25.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-16",
  "updated": "2026-09-16"
}
```

## H-STDP-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/10`.

```json
{
  "id": "H-STDP-001-A",
  "research_question": "RQ-STDP-001",
  "hypothesis": "Pair-based STDP erzeugt unter definierten Pre/Post-Zeitabständen eine asymmetrische Gewichtsanpassung (LTP bei Δt > 0, LTD bei Δt < 0).",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-STDP-002-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/11`.

```json
{
  "id": "H-STDP-002-A",
  "research_question": "RQ-STDP-002",
  "hypothesis": "STDP-getriebene Gewichte konvergieren unter Dauerstimulation zu einer stabilen Verteilung.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-STOR-001-A

Typ: `hypothesis`; Quellstatus: `supported`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/18`.

```json
{
  "id": "H-STOR-001-A",
  "research_question": "RQ-STORAGE-001",
  "hypothesis": "Ein vollständiger neuronaler Zustand kann verlustfrei im .b5d-Format gespeichert und zurückgeladen werden.",
  "status": "supported",
  "evidence": [
    "EVID-2026-04",
    "EVID-2026-06",
    "EVID-2026-08",
    "EVID-2026-10",
    "EVID-2026-12",
    "EVID-2026-14",
    "EVID-2026-16"
  ],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-STOR-002-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/19`.

```json
{
  "id": "H-STOR-002-A",
  "research_question": "RQ-STORAGE-002",
  "hypothesis": "Für kausale Fortsetzung eines Laufs müssen Neuron-State, Synapsen-State, Eligibility-Traces, RNG-State und Event-Queue gespeichert werden.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-STOR-003-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/20`.

```json
{
  "id": "H-STOR-003-A",
  "research_question": "RQ-STORAGE-003",
  "hypothesis": "Die Speicherdichte des .b5d-Formats skaliert sublinear mit der Neuronenzahl.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-STOR-004-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/21`.

```json
{
  "id": "H-STOR-004-A",
  "research_question": "RQ-STORAGE-004",
  "hypothesis": "Das .b5d-Format skaliert auf mindestens 50 Millionen Neuronen ohne Leistungseinbruch.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-STRUCT-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/25`.

```json
{
  "id": "H-STRUCT-001-A",
  "research_question": "RQ-STRUCT-001",
  "hypothesis": "Strukturelle Plastizität (Pruning/Sprouting) führt zu messbar verbesserter Netzwerkeffizienz.",
  "status": "untested",
  "evidence": [],
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## H-SUITE-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/33`.

```json
{
  "id": "H-SUITE-001-A",
  "research_question": "RQ-SUITE-001",
  "hypothesis": "Alle Science-Suite-Teilprotokolle erfuellen in einem gemeinsamen Lauf ihre registrierten Ausfuehrungsvertraege und erzeugen auswertbare DATA-, Statistik- und Provenienzartefakte.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## H-TEMP-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/7`.

```json
{
  "id": "H-TEMP-001-A",
  "research_question": "RQ-TEMP-001",
  "hypothesis": "Die Temporal-State-Vergleiche unterscheiden sich deterministisch nach FAST-, MEDIUM- und SLOW-Horizont.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-03",
  "updated": "2026-09-03"
}
```

## H-TEMP-002-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/39`.

```json
{
  "id": "H-TEMP-002-A",
  "research_question": "RQ-TEMP-002",
  "hypothesis": "Forward-, Reverse- und Simultanfolgen erzeugen bei gleicher Ereignisanzahl unterscheidbare spike-basierte Antwortsignaturen.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## H-TIME-001-A

Typ: `hypothesis`; Quellstatus: `untested`; Quelle: [research/registry/hypotheses.yaml](../../registry/hypotheses.yaml), JSON-Pointer `/8`.

```json
{
  "id": "H-TIME-001-A",
  "research_question": "RQ-TIME-001",
  "hypothesis": "Die Tick-Leiter liefert reproduzierbare Durchsatz- und Zustandsmessungen bis 1.000.000 Ticks.",
  "status": "untested",
  "evidence": [],
  "created": "2026-09-03",
  "updated": "2026-09-03"
}
```

## RQ-5D-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/14`.

```json
{
  "id": "RQ-5D-001",
  "domain": "5D Topology",
  "question": "Hat die fünfdimensionale Anordnung einen messbaren Effekt auf die Netzwerkdynamik?",
  "relevance": "Kernfrage des gesamten Brain-5D-Projekts.",
  "literature": [
    "SRC-IZHIKEVICH-2003"
  ],
  "hypotheses": [
    "H-5D-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-5D-002

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/15`.

```json
{
  "id": "RQ-5D-002",
  "domain": "5D Topology",
  "question": "Wie verändert Dimensionalität die Signalpropagation im Netzwerk?",
  "relevance": "Verständnis der Informationsausbreitung in höherdimensionalen SNNs.",
  "literature": [],
  "hypotheses": [
    "H-5D-002-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-5D-003

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/16`.

```json
{
  "id": "RQ-5D-003",
  "domain": "5D Topology",
  "question": "Entsteht in 5D eine andere Modularität als in niedrigeren Dimensionen?",
  "relevance": "Modularität ist ein Schlüsselkonzept für funktionale Spezialisierung.",
  "literature": [],
  "hypotheses": [
    "H-5D-003-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-5D-004

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/17`.

```json
{
  "id": "RQ-5D-004",
  "domain": "5D Topology",
  "question": "Sind zusätzliche Dimensionen informationstragend oder lediglich zusätzliche Koordinaten?",
  "relevance": "Eine der wichtigsten Fragen des gesamten Projekts — betrifft fundamentale Natur der 5D-Repräsentation.",
  "literature": [],
  "hypotheses": [
    "H-5D-004-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-5D-005

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/37`.

```json
{
  "id": "RQ-5D-005",
  "domain": "5D Topology",
  "question": "Verändert 5D-Geometrie Propagation, Robustheit oder Dynamik, wenn Neuronenzahl, Synapsenzahl, Grad- und Gewichtsmuster sowie Stimulusplan kontrolliert gleich bleiben?",
  "relevance": "Der kleine 5D-Test in EXP-GEN-0021 isolierte keinen dimensionsspezifischen Effekt.",
  "literature": [],
  "hypotheses": [
    "H-5D-005-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": "Der erste operationalisierte Test hält die Graphstruktur bewusst klein und identisch."
  },
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## RQ-AIR-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/32`.

```json
{
  "id": "RQ-AIR-001",
  "domain": "AI-Assisted Research",
  "question": "Kann ein LLM-basierter Scientific Research Assistant methodische Fehler in Brain-5D-Experimenten anhand eines standardisierten ResearchPacket zuverlässig identifizieren?",
  "relevance": "Prüft den wissenschaftlichen Nutzen der Research-Assistant-Architektur, ohne ihr wissenschaftliche Entscheidungsgewalt zu geben.",
  "literature": [],
  "hypotheses": [
    "H-AIR-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-09-02",
  "updated": "2026-09-02"
}
```

## RQ-DET-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/2`.

```json
{
  "id": "RQ-DET-001",
  "domain": "Determinism",
  "question": "Bleibt die Spikefolge bei gleichem Seed, Input und Zustand deterministisch?",
  "relevance": "Determinismus ist Voraussetzung für kausale Analyse und reproduzierbare Forschung.",
  "literature": [
    "SRC-IZHIKEVICH-2003"
  ],
  "hypotheses": [
    "H-SNN-003-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-EMB-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/27`.

```json
{
  "id": "RQ-EMB-001",
  "domain": "Embodiment",
  "question": "Kann Brain-5D in einer Sensor-Aktor-Schleife (Embodiment) sinnvoll agieren?",
  "relevance": "Embodiment erweitert Brain-5D von einer reinen Simulation zu einem interaktiven System.",
  "literature": [],
  "hypotheses": [
    "H-EMB-001-B",
    "H-EMB-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-EPIST-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/31`.

```json
{
  "id": "RQ-EPIST-001",
  "domain": "Epistemology",
  "question": "Was gilt als Erkenntnis des Systems Brain-5D im Unterschied zur Erkenntnis des Forschers?",
  "relevance": "Epistemologische Grundlagen für maschinelle Wissensproduktion.",
  "literature": [],
  "hypotheses": [
    "H-EPIST-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-ETH-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/29`.

```json
{
  "id": "RQ-ETH-001",
  "domain": "Ethics",
  "question": "Wer ist der Autor von Brain-5D-Erkenntnissen — Mensch, Modell oder System?",
  "relevance": "Grundsatzfrage zur Autorenschaft und Verantwortung in KI-gestützter Forschung.",
  "literature": [],
  "hypotheses": [
    "H-ETH-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-ETH-002

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/30`.

```json
{
  "id": "RQ-ETH-002",
  "domain": "Ethics",
  "question": "Wo liegt die Kontrolle und Verantwortung bei Brain-5D-Experimenten?",
  "relevance": "Verantwortungsverteilung zwischen Entwickler, Modell und automatisiertem System.",
  "literature": [],
  "hypotheses": [
    "H-ETH-002-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-GEN-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/35`.

```json
{
  "id": "RQ-GEN-001",
  "domain": "Learning Generalization",
  "question": "Verbessert reward-moduliertes lokales Lernen die Leistung auf Holdout- und Perturbationsbedingungen, die nicht zur Anpassung verwendet wurden?",
  "relevance": "EXP-GEN-0021 zeigte funktionelle Änderung unter Learning-on, aber keine Generalisierung.",
  "literature": [],
  "hypotheses": [
    "H-GEN-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": "Generalisierung muss gegenüber Learning-off und Sham-Replay getrennt werden."
  },
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## RQ-HOM-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/12`.

```json
{
  "id": "RQ-HOM-001",
  "domain": "Homeostasis",
  "question": "Kann synaptische Homeostase die Feuerrate in einem SNN stabilisieren?",
  "relevance": "Homeostase ist ein zentraler biologischer Regulationsmechanismus.",
  "literature": [
    "SRC-TURRIGIANO-2008"
  ],
  "hypotheses": [
    "H-HOM-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-HOM-002

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/13`.

```json
{
  "id": "RQ-HOM-002",
  "domain": "Homeostasis",
  "question": "Wie interagiert Homeostase mit STDP? Wirken sie synergistisch oder antagonistisch?",
  "relevance": "Das Zusammenspiel beider Mechanismen ist entscheidend für stabile Plastizität.",
  "literature": [
    "SRC-TURRIGIANO-2008"
  ],
  "hypotheses": [
    "H-HOM-002-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-LIFE-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/42`.

```json
{
  "id": "RQ-LIFE-001",
  "domain": "Lifelong Learning",
  "question": "Bleibt zuvor erworbene Lernleistung bei sequenziellen Aufgaben erhalten oder entstehen messbare Interferenzeffekte?",
  "relevance": "Das positive Single-Task-Learningsignal aus EXP-GEN-0021 motiviert Retentionstests.",
  "literature": [],
  "hypotheses": [
    "H-LIFE-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": "Der erste Runner ist ein Vorläufer-Screen; echte Catastrophic-Forgetting-Evidenz erfordert ein gemeinsames fortlaufend trainiertes Netzwerk."
  },
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## RQ-LLM-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/28`.

```json
{
  "id": "RQ-LLM-001",
  "domain": "Language Organ",
  "question": "Kann ein Language Organ (SNM ↔ LLM) sinnvolle Kommunikation ermöglichen?",
  "relevance": "Schnittstelle zwischen neuronaler Simulation und natürlicher Sprache.",
  "literature": [],
  "hypotheses": [
    "H-LLM-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-MEM-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/26`.

```json
{
  "id": "RQ-MEM-001",
  "domain": "Memory",
  "question": "Kann Brain-5D Informationen über synaptische Gewichte speichern und zuverlässig abrufen?",
  "relevance": "Gedächtnis ist eine Kernfunktion neuronaler Systeme.",
  "literature": [],
  "hypotheses": [
    "H-MEM-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-PERF-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/40`.

```json
{
  "id": "RQ-PERF-001",
  "domain": "Runtime Performance",
  "question": "Welche Subsysteme dominieren die Wall-Time wissenschaftlicher Läufe und welche Optimierungen erhöhen den Durchsatz bei erhaltener deterministischer Äquivalenz?",
  "relevance": "EXP-GEN-0021 zeigte eine große Differenz zwischen isoliertem Tick-Durchsatz und Suite-Laufzeit.",
  "literature": [],
  "hypotheses": [
    "H-PERF-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": "Performanceänderungen mit veränderter numerischer oder zeitlicher Semantik gelten als Protokolländerung."
  },
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## RQ-PING-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/6`.

```json
{
  "id": "RQ-PING-001",
  "domain": "Network Dynamics",
  "question": "Ist die beobachtete Network-Impulse-Response bei identischem Zustand und Seed reproduzierbar?",
  "relevance": "Reproduzierbarkeit der kontrollierten Impulsantwort.",
  "hypotheses": [
    "H-PING-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-09-03",
  "updated": "2026-09-03"
}
```

## RQ-REC-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/34`.

```json
{
  "id": "RQ-REC-001",
  "domain": "Recurrent Dynamics",
  "question": "Unter welchen Rekurrenzgewichten und Delays wechselt Brain-5D zwischen sofortigem Erlöschen, transienter rekurrenter Aktivität und bis zum Beobachtungsende persistierender Aktivität?",
  "relevance": "EXP-GEN-0021 zeigte einen klaren rekurrenzabhängigen Dynamikunterschied, aber noch keine Parametergrenze.",
  "literature": [],
  "hypotheses": [
    "H-REC-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": "Abgeleitet aus EXP-GEN-0021; persistente Aktivität ist nicht gleichbedeutend mit Gedächtnis oder Kognition."
  },
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## RQ-REC-002

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/41`.

```json
{
  "id": "RQ-REC-002",
  "domain": "Recurrent Dynamics",
  "question": "Wie verändern Loop-Delay und skalierte Rekurrenzstruktur Persistenzdauer, Inter-Spike-Dynamik und Extinktionsverhalten?",
  "relevance": "Der Drei-Neuronen-Loop aus EXP-GEN-0021 reicht nicht für Skalierungsaussagen.",
  "literature": [],
  "hypotheses": [
    "H-REC-002-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": "Version 1 operationalisiert zunächst Loop-Delay als kontrollierten Skalierungsparameter."
  },
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## RQ-REG-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/9`.

```json
{
  "id": "RQ-REG-001",
  "domain": "Regulation",
  "question": "Wie reagieren Drives und funktionale Zustandsgrößen auf nominale, chronische und unbekannte Telemetrie?",
  "relevance": "Deterministische Prüfung der Selbstregulation unter Ressourcen- und Sensorbedingungen.",
  "hypotheses": [
    "H-REG-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-09-03",
  "updated": "2026-09-03"
}
```

## RQ-REG-002

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/38`.

```json
{
  "id": "RQ-REG-002",
  "domain": "Closed-loop Regulation",
  "question": "Verbessert aktive Regulation Stabilität und Recovery eines laufenden SNN unter identischen Ressourcen- oder Sensorperturbationen gegenüber deaktivierter Regulation?",
  "relevance": "EXP-GEN-0021 validierte Regulationszustände, aber noch keinen funktionalen Closed-loop-Nutzen.",
  "literature": [],
  "hypotheses": [
    "H-REG-002-B",
    "H-REG-002-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": "Der Feedbackpfad muss als technische Intervention und nicht als Emotion interpretiert werden."
  },
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## RQ-REPL-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/36`.

```json
{
  "id": "RQ-REPL-001",
  "domain": "Replication",
  "question": "Bleiben die in EXP-GEN-0021 beobachteten Rekurrenz- und Learning-Effekte unter unabhängigen Initialisierungen und sauberem Prozess erhalten?",
  "relevance": "Identische Seedsignaturen zeigen Determinismus, aber keine statistisch unabhängige Replikation.",
  "literature": [],
  "hypotheses": [
    "H-REPL-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": "Replikation erfordert echte Variation der Initialisierung und einen Clean Freeze."
  },
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## RQ-SCALE-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/22`.

```json
{
  "id": "RQ-SCALE-001",
  "domain": "Scaling",
  "question": "Skaliert Brain-5D von 5.000 auf Millionen Neuronen ohne qualitative Dynamikveränderung?",
  "relevance": "Nachweis der Architekturskalierbarkeit.",
  "literature": [],
  "hypotheses": [
    "H-SCALE-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-SELF-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/23`.

```json
{
  "id": "RQ-SELF-001",
  "domain": "Self-Organization",
  "question": "Entstehen in Brain-5D spontan funktionale Cluster oder Module?",
  "relevance": "Selbstorganisation ist ein Schlüsselmerkmal biologischer neuronaler Systeme.",
  "literature": [
    "SRC-IZHIKEVICH-2003"
  ],
  "hypotheses": [
    "H-SELF-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-SELF-002

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/24`.

```json
{
  "id": "RQ-SELF-002",
  "domain": "Self-Organization",
  "question": "Ist die beobachtete Selbstorganistion emergenter Natur oder durch die Architektur programmiert?",
  "relevance": "Unterscheidung zwischen echter Emergenz und deterministischer Architekturfolge.",
  "literature": [],
  "hypotheses": [
    "H-SELF-002-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-SNN-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/0`.

```json
{
  "id": "RQ-SNN-001",
  "domain": "Spiking Neural Networks",
  "question": "Kann Brain-5D stabile Spike-Dynamiken über lange Simulationszeiträume erzeugen?",
  "relevance": "Grundvoraussetzung für alle weiteren Lern- und Selbstorganisationsexperimente.",
  "literature": [
    "SRC-IZHIKEVICH-2003",
    "SRC-GERSTNER-2014"
  ],
  "hypotheses": [
    "H-SNN-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-SNN-002

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/1`.

```json
{
  "id": "RQ-SNN-002",
  "domain": "Spiking Neural Networks",
  "question": "Kann das eingesetzte Neuronenmodell bei konstantem Input reproduzierbare Spikefolgen erzeugen?",
  "relevance": "Basis für deterministische Reproduzierbarkeit aller Experimente.",
  "literature": [
    "SRC-IZHIKEVICH-2003",
    "SRC-GERSTNER-2014"
  ],
  "hypotheses": [
    "H-SNN-002-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-SNN-003

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/3`.

```json
{
  "id": "RQ-SNN-003",
  "domain": "Spiking Neural Networks",
  "question": "Wie variiert die Propagation mit der Topologie?",
  "relevance": "Grundlegendes Verständnis der Signalausbreitung in multidimensionalen SNNs.",
  "literature": [
    "SRC-WATTS-STROGATZ-1998",
    "SRC-BARABASI-1999"
  ],
  "hypotheses": [
    "H-SNN-003-B"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": "EXP-S1-TOPO-V2-20260918 und die korrigierte interne Replikation EXP-S1-TOPO-V3-R1-20260918 liefern DATA-seitige Unterstützung dafür, dass die konkrete Topologie im präregistrierten 64-Neuronen-/246-Kanten-Stage-1-Regime die Propagationsdynamik beeinflusst. R1 löst die terminale active_fraction-Sättigung von 1d/2d/3d durch prospektiv definierte zeitaufgelöste Endpunkte auf und repliziert alle fünf V2-First-Output-Latenzrichtungen auf neuen Seeds. Human Review und EVID-Entscheidung stehen aus.",
    "confidence": "replicated_internal_data_review_pending",
    "limitations": "Interne Replikation ist keine unabhängige externe Replikation. Kein 5D-Vorteilsclaim; H-5D-005-A bleibt separat open/untested und erfordert das größere dimensionsspezifische Prüfprogramm."
  },
  "created": "2026-08-23",
  "updated": "2026-09-18"
}
```

## RQ-SNN-004

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/4`.

```json
{
  "id": "RQ-SNN-004",
  "domain": "Spiking Neural Networks",
  "question": "Wie verändert STDP die synaptische Gewichtsmatrix?",
  "relevance": "Zentrale Fragestellung für plastische Netzwerke.",
  "literature": [
    "SRC-SONG-ABBOTT-2000",
    "SRC-BI-POO-1998"
  ],
  "hypotheses": [
    "H-SNN-004-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-SNN-005

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/5`.

```json
{
  "id": "RQ-SNN-005",
  "domain": "Spiking Neural Networks",
  "question": "Verbessert STDP tatsächlich eine definierte Lernleistung?",
  "relevance": "Wissenschaftlich wesentlich stärker als reine Gewichtsänderung — benötigt Kontrollgruppe ohne STDP.",
  "literature": [
    "SRC-SONG-ABBOTT-2000",
    "SRC-BI-POO-1998"
  ],
  "hypotheses": [
    "H-SNN-005-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-SNN-006

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/43`.

```json
{
  "id": "RQ-SNN-006",
  "domain": "Spiking Neural Networks",
  "question": "Bleibt die unter RQ-SNN-001 beobachtete Langzeitstabilitaet unter vorab definierten lokalen Variationen von synaptischem Gewicht und Tonic-Drive erhalten?",
  "relevance": "Trennt die deterministische Stabilitaet einer festen Parameterisierung von lokaler Robustheit ueber tatsaechlich unterschiedliche, seed-gebundene Modellparameterisierungen.",
  "literature": [
    "SRC-IZHIKEVICH-2003",
    "SRC-GERSTNER-2014"
  ],
  "hypotheses": [
    "H-SNN-006-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-09-16",
  "updated": "2026-09-16"
}
```

## RQ-STDP-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/10`.

```json
{
  "id": "RQ-STDP-001",
  "domain": "STDP",
  "question": "Erzeugt pair-based STDP unter definierten Pre/Post-Zeitabständen eine asymmetrische Gewichtsanpassung?",
  "relevance": "Fundamentale STDP-Eigenschaft, die in Brain-5D verifiziert werden muss.",
  "literature": [
    "SRC-SONG-ABBOTT-2000",
    "SRC-BI-POO-1998"
  ],
  "hypotheses": [
    "H-STDP-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-STDP-002

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/11`.

```json
{
  "id": "RQ-STDP-002",
  "domain": "STDP",
  "question": "Bleiben STDP-getriebene Gewichte unter Dauerstimulation stabil oder oszillieren/explodieren sie?",
  "relevance": "Stabilität ist Voraussetzung für längerfristiges Lernen.",
  "literature": [
    "SRC-SONG-ABBOTT-2000"
  ],
  "hypotheses": [
    "H-STDP-002-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-STORAGE-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/18`.

```json
{
  "id": "RQ-STORAGE-001",
  "domain": "Storage",
  "question": "Kann ein vollständiger neuronaler Zustand verlustfrei im .b5d-Modell gespeichert werden?",
  "relevance": "Grundlage für Persistenz und Checkpointing.",
  "literature": [],
  "hypotheses": [
    "H-STOR-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-STORAGE-002

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/19`.

```json
{
  "id": "RQ-STORAGE-002",
  "domain": "Storage",
  "question": "Welche Informationen müssen gespeichert werden, damit ein Lauf kausal fortgesetzt werden kann?",
  "relevance": "Vollständige Zustandsspeicherung für deterministische Reproduktion.",
  "literature": [],
  "hypotheses": [
    "H-STOR-002-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-STORAGE-003

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/20`.

```json
{
  "id": "RQ-STORAGE-003",
  "domain": "Storage",
  "question": "Welche Speicherdichte erreicht das multidimensionale Modell?",
  "relevance": "Skalierbarkeit des Speicherformats.",
  "literature": [],
  "hypotheses": [
    "H-STOR-003-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-STORAGE-004

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/21`.

```json
{
  "id": "RQ-STORAGE-004",
  "domain": "Storage",
  "question": "Wie verhält sich das .b5d-Format bei 5.000, 50.000, 500.000, 5 Mio., 50 Mio. und 312,5 Mio. Neuronen?",
  "relevance": "Extrapolation der theoretischen Skalierbarkeit.",
  "literature": [],
  "hypotheses": [
    "H-STOR-004-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-STRUCT-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/25`.

```json
{
  "id": "RQ-STRUCT-001",
  "domain": "Structural Plasticity",
  "question": "Führt strukturelle Plastizität (Pruning/Sprouting) zu funktional verbesserten Netzwerken?",
  "relevance": "Strukturelle Anpassung ist ein mächtiger Mechanismus biologischer Gehirne.",
  "literature": [],
  "hypotheses": [
    "H-STRUCT-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-08-23",
  "updated": "2026-08-23"
}
```

## RQ-SUITE-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/33`.

```json
{
  "id": "RQ-SUITE-001",
  "domain": "Research Infrastructure",
  "question": "Erzeugt der vollstaendige Science-Suite-Lauf unter gemeinsamer Provenienz vollstaendige und intern konsistente Diagnoseartefakte fuer alle registrierten Teilprotokolle?",
  "relevance": "Trennt technische Omnibus-Validierung von hypothesenspezifischer wissenschaftlicher Evidenz.",
  "literature": [],
  "hypotheses": [
    "H-SUITE-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": "Omnibus-Diagnostik ist keine Primaerevidenz fuer die enthaltenen Fach-RQs."
  },
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## RQ-TEMP-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/7`.

```json
{
  "id": "RQ-TEMP-001",
  "domain": "Temporal State",
  "question": "Wie unterscheiden sich FAST-, MEDIUM- und SLOW-Referenzzustände unter identischer Ausführung?",
  "relevance": "Messung von Persistenz und Zustandsdrift ohne Runtime-Zurückspulen.",
  "hypotheses": [
    "H-TEMP-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-09-03",
  "updated": "2026-09-03"
}
```

## RQ-TEMP-002

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/39`.

```json
{
  "id": "RQ-TEMP-002",
  "domain": "Temporal Learning",
  "question": "Reagiert Brain-5D auf spike-tragende zeitliche Reihenfolge anders als auf umgekehrte oder simultane Kontrollfolgen?",
  "relevance": "EXP-GEN-0021 zeigte Temporal-State-Diskrepanzen ohne Spike-Aktivität.",
  "literature": [],
  "hypotheses": [
    "H-TEMP-002-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": "Eine Reihenfolgenabhängigkeit ist zunächst nur eine dynamische Differenz, kein Gedächtnisnachweis."
  },
  "created": "2026-09-05",
  "updated": "2026-09-05"
}
```

## RQ-TIME-001

Typ: `research_question`; Quellstatus: `open`; Quelle: [research/registry/questions.yaml](../../registry/questions.yaml), JSON-Pointer `/8`.

```json
{
  "id": "RQ-TIME-001",
  "domain": "Learning Timescale",
  "question": "Wie verändert sich die messbare Laufzeit und Lernaktivität über die registrierte Tick-Leiter?",
  "relevance": "Kalibrierung der zeitlichen Ausführung vor Langzeitexperimenten.",
  "hypotheses": [
    "H-TIME-001-A"
  ],
  "evidence": [],
  "status": "open",
  "answer": {
    "current": null,
    "confidence": "none",
    "limitations": null
  },
  "created": "2026-09-03",
  "updated": "2026-09-03"
}
```
