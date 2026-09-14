# Nachtrag zu Fassung 1.5 — Stage 4: spezialisierte neuronale Areale

**Thomas Heisig | 14. September 2026**

Dieser Nachtrag aktualisiert die wissenschaftliche Forschungsarbeit **Fassung 1.5** um den nach deren Redaktionsstand verifizierten Stage-4-Engineeringstand. Die ursprüngliche Ausgabe vom 13. September 2026, ihre Kampagnenprovenienz und ihre Binärexporte bleiben unverändert. Der Nachtrag ist daher eine quellengebundene Ergänzung und keine rückwirkende Umschreibung historischer Messdaten.

## 1. Gegenstand

Stage 4 untersucht und implementiert drei technisch getrennte modalitätsspezifische Pfade:

| Modalität | Referenzareal | Adapter | Plastizitätskandidat | technische Rolle |
|---|---|---|---|---|
| Audio | `stage4.audio.temporal` | `threshold_features` | phase-weighted temporal STDP | zeitliche/phasengebundene Signalrepräsentation |
| Vision | `stage4.vision.spatial` | `threshold_features` | spatial STDP + structural-growth candidate | räumlich strukturierte visuelle Repräsentation |
| Digital | `stage4.digital.symbolic` | `identity` | population/meta-gating candidate | verlustfreie Payload-Bindung außerhalb des SNN plus neuronale Routing-Repräsentation |

Der technische Vertrag liegt in `src/embodiment/specialized_areas.py`. Die read-only Full-Stack-Projektion erfolgt über `/api/embodiment/neural-symbiosis` sowie die Wesen- und MSBA-Ansichten im Frontend.

## 2. Skalierungsbehauptung

Der Stage-4-Vertrag spezifiziert eine **aggregierte Topologie-Untergrenze** von 100.000 Neuronen und 10.000.000 gerichteten Synapsen/Kanten:

- Audio: 25.000 Neuronen, 2,4 Mio. Kantenbudget;
- Vision: 50.000 Neuronen, 6,4 Mio. Kantenbudget;
- Digital: 25.000 Neuronen, 1,2 Mio. Kantenbudget.

Diese Größenordnung wurde **nicht** als vollständig materialisiertes, dynamisch laufendes 100k/10M-Netz verifiziert. `dynamic_scale_execution_verified=false` ist Bestandteil des maschinenlesbaren Verifikationsartefakts. Aus dem aggregierten Budget darf deshalb keine Performance-, Echtzeit- oder biologische Skalierungsbehauptung abgeleitet werden.

## 3. Forschungsfragen und aktuelle DATA-Artefakte

Die Stage-4-Experimente sind den spezifischen MSBA-Forschungsfragen zugeordnet:

| RQ | Prüfgegenstand | aktuelles DATA-Artefakt | beobachteter Stand |
|---|---|---|---|
| `RQ-MSBA-E01` | modalitätsspezifische Kosten bei matched tasks | `EXP-BATCH-20260914074039-90` | gleiche mittlere Task-Accuracy der Referenzmodalitäten; modellierte Kosten im gespeicherten Datensatz Digital < Audio < Vision |
| `RQ-MSBA-E02` | adaptive Ressourcenallokation | `EXP-BATCH-20260914074039-91` | adaptive Referenzbedingung liegt im gespeicherten Datensatz über fixer und zufälliger Allokation |
| `RQ-MSBA-E03` | visueller ROI/Foveation-Pfad | `EXP-BATCH-20260914074039-92` | adaptive ROI-Referenz erreicht im synthetischen Design dieselbe Task-Accuracy wie Full-Image bei niedrigerem modelliertem Energieverbrauch |
| `RQ-MSBA-E04` | digitale Integrität | `EXP-BATCH-20260914074039-93` | keine gespeicherten Checksum- oder Exact-Payload-Mismatches |
| `RQ-MSBA-E05` | Modalitätsverlust und Kompensation | `EXP-BATCH-20260914074039-94` | adaptive Referenzkompensation zeigt höhere Task-Recovery als fixe Allokation |

Alle fünf Serien sind **DATA**, keine automatisch akzeptierte `EVID`. Die Engineering-Verifikation darf die wissenschaftliche Review-Entscheidung nicht ersetzen.

## 4. Übergeordnete Forschungsfragen

Stage 4 trägt zu `RQ9` (multimodale Signalintegration/Grounding ohne versteckten LLM-Primärlerner) und `RQ11` (emergente funktionale Organisation) bei, beantwortet beide aber nicht vollständig.

Insbesondere bleiben offen:

1. ein kausaler Vergleich spezialisierter gegenüber matched unspezialisierten Arealen;
2. unabhängige Replikation der E01–E05-Ergebnisse;
3. dynamische Skalierungsversuche über steigende reale Neuronen-/Kantenbudgets;
4. Langzeitstabilität bei gleichzeitig aktiver modalitätsspezifischer Plastizität;
5. Nachweis emergenter funktionaler Organisation statt lediglich vorgegebener Spezialisierung;
6. physikalische Energiemessung anstelle modellierter bzw. normalisierter Energiegrößen.

Damit wird Stage 4 **technisch erreicht**, während die weitergehenden wissenschaftlichen Hypothesen offen bzw. reviewpflichtig bleiben.

## 5. Verifikationsstand

Das reproduzierbare Engineering-Artefakt ist:

`research/generated/verification/specialized_neural_areas_reference_alpha3.json`

Der verifizierte Umfang umfasst:

- deterministische Audio-, Vision- und Digital-Referenzproben;
- exakte digitale SHA-256-Eingabe-/Ausgabeintegrität;
- Stage-4-spezifische Tests und bestehende MSBA-/Gateway-Verträge;
- Frontend- und Timeline-Vertragstests;
- explizite Sperre produktiver Gateway-Aktivierung;
- explizite Sperre automatischer Evidence-Promotion.

Die letzte erfolgreich ausgeführte Stage-4-Verifikation auf dem Feature-Branch berichtete 56 bestandene zielgerichtete Tests; die Full-Stack-/Timeline-Prüfungen waren ebenfalls grün.

## 6. Wissenschaftliche Schlussfolgerung für Fassung 1.5

Der neue Stand rechtfertigt folgende begrenzte Aktualisierung der Fassung 1.5:

> MHRN besitzt nun einen reproduzierbar verifizierten Engineering-Vertrag für drei modalitätsspezifische neuronale Pfade mit unterschiedlichen Adapter-, Routing- und Plastizitätsregeln sowie einer read-only Full-Stack-Projektion. Die zugeordneten E01–E05-Datensätze stützen mehrere technische Teilfunktionen innerhalb ihrer synthetischen Versuchsdesigns. Sie zeigen noch keinen allgemeinen Vorteil spezialisierter Areale, keine biologische Äquivalenz und keine dynamisch verifizierte 100k/10M-Skalierung.

Diese Formulierung ersetzt keine historische Passage der Fassung 1.5, sondern ergänzt deren aktuellen Geltungsbereich ab dem 14. September 2026.

## 7. Referenzen im Repository

- `research/stage4_specialized_neural_areas.md`
- `research/registry/msba_experiments.yaml`
- `research/generated/verification/specialized_neural_areas_reference_alpha3.json`
- `src/embodiment/specialized_areas.py`
- `src/experiments/msba_lab.py`
- `tests/test_stage4_specialized_neural_areas.py`
- `tests/test_stage4_frontend_contract.py`

**Evidenzstatus:** menschliches wissenschaftliches Review ausstehend; keine automatische EVID-Freigabe.