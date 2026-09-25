# Stage 4 — Spezialisierte neuronale Areale

**Entwicklungsziel:** vollständige technische Integration modalitätsspezifischer Audio-, Vision- und Digitalpfade in MHRN, einschließlich Adaptervertrag, unterschiedlicher Plastizitätskandidaten, experimenteller Kontrollpfade, API-/Frontend-Projektion und reproduzierbarer Engineering-Verifikation.

## Technischer Vertrag

Stage 4 wird als klar begrenzter Engineering-Vertrag geschlossen:

| Modalität | Referenzareal | Pfad | Adapter | Plastizitätskandidat |
|---|---|---|---|---|
| Audio | `stage4.audio.temporal` | temporal coherence | `threshold_features` | phase-weighted temporal STDP |
| Vision | `stage4.vision.spatial` | spatial multiplex | `threshold_features` | spatial STDP + structural growth |
| Digital | `stage4.digital.symbolic` | quantized high fidelity | `identity` | population/meta-gating |

Der Digitalpfad hält den exakten Payload außerhalb der verlustbehafteten SNN-Repräsentation und prüft Ein-/Ausgabe mit SHA-256. Learnable Komponenten dürfen Routing, Gain und Admission betreffen, nicht den ursprünglichen Payload.

## Skalierungsvertrag

Die Stage-4-Untergrenze wird als **aggregierter Topologievertrag** beschrieben:

- 100.000 Neuronen Budget;
- 10.000.000 gerichtete Synapsen/Kanten Budget;
- Audio: 25.000 × mittlerer Fanout 96 = 2,4 Mio.;
- Vision: 50.000 × mittlerer Fanout 128 = 6,4 Mio.;
- Digital: 25.000 × mittlerer Fanout 48 = 1,2 Mio.

Diese Zahlen materialisieren nicht zehn Millionen Python-Edge-Objekte. `dynamic_scale_execution_verified=false` bleibt deshalb Bestandteil des maschinenlesbaren Vertrags. Ein vollständiger dynamischer Lauf dieser Größenordnung ist eine separate Scaling-/Performance-Frage und darf nicht aus dem Stage-4-Vertrag abgeleitet werden.

## Forschungsfragen- und Experiment-Traceability

Die Stage-4-Implementierung wird nicht aus einer einzelnen Kennzahl abgeleitet. Die spezifischen MSBA-Forschungsfragen bilden unterschiedliche kausale bzw. technische Teilfragen ab:

| Forschungsfrage | Stage-4-Bezug | Aktueller Datensatz |
|---|---|---|
| `RQ-MSBA-E01` | Vergleich von Audio, Vision und Digital unter matched tasks und Ressourcenmetriken | `EXP-BATCH-20260914074039-90` |
| `RQ-MSBA-E02` | adaptive gegenüber fixer/zufälliger Ressourcenallokation | `EXP-BATCH-20260914074039-91` |
| `RQ-MSBA-E03` | visueller ROI/Foveation-Pfad und Ressourcensteuerung | `EXP-BATCH-20260914074039-92` |
| `RQ-MSBA-E04` | exakte digitale Payload-/Checksum-Integrität | `EXP-BATCH-20260914074039-93` |
| `RQ-MSBA-E05` | kontrollierter Modalitätsverlust und Kompensation | `EXP-BATCH-20260914074039-94` |

Die übergeordneten Fragen `RQ9` (multimodale Grounding-/Signalintegration ohne versteckten LLM-Primärlerner) und `RQ11` (emergente funktionale Organisation) sind mit Stage 4 verbunden, werden durch Stage 4 aber **nicht geschlossen**. Insbesondere beweist ein technisch vorhandenes spezialisiertes Areal weder emergente Organisation noch einen generellen Vorteil gegenüber einer unspezialisierten Vergleichsarchitektur.

Damit ist die Forschungslogik zweistufig: `RQ-MSBA-E01` bis `E05` prüfen die unmittelbar implementierten Modalitäts-/Gateway-Eigenschaften; `RQ9` und `RQ11` bleiben breitere wissenschaftliche Programme für spätere kausale und unabhängige Tests.

## Bereits vorhandene Versuchsdaten

Die Implementierung bindet die jüngste MSBA-Serie als DATA-Grundlage ein:

- `EXP-BATCH-20260914074039-90` — RQ-MSBA-E01 / Energieeffizienz;
- `EXP-BATCH-20260914074039-91` — RQ-MSBA-E02 / Ressourcenallokation;
- `EXP-BATCH-20260914074039-92` — RQ-MSBA-E03 / visueller ROI;
- `EXP-BATCH-20260914074039-93` — RQ-MSBA-E04 / digitale Integrität;
- `EXP-BATCH-20260914074039-94` — RQ-MSBA-E05 / Modalitätsverlust und Kompensation.

Die Serie verwendet die Seeds 101, 102 und 103. Die aufgezeichneten Daten zeigen unter anderem:

- E01: gleiche mittlere Aufgabenaccuracy der drei Referenzmodalitäten, aber unterschiedliche modellierte Kosten pro korrekter Entscheidung; im vorliegenden Datensatz liegt Digital unter Audio und Audio unter Vision;
- E03: der Referenz-ROI-Pfad erreicht in diesem synthetischen Versuchsdesign die gleiche Trefferquote wie Full-Image bei deutlich geringerem modelliertem visuellen Energieverbrauch;
- E04: in den gespeicherten Bedingungen wurden keine Checksum- oder Exact-Payload-Mismatches registriert;
- E05: die adaptive Referenzkompensation zeigt im gespeicherten Datensatz eine höhere Task-Recovery als die feste Allokation.

Diese Aussagen beschreiben die vorhandenen **DATA-Artefakte**. Sie sind weder allgemeine Leistungsbehauptungen noch automatische EVID-Promotion. `RQ-MSBA-E02` und die vollständige inferentielle Interpretation aller fünf Fragen bleiben ebenfalls dem menschlichen Review-/EVID-Prozess unterworfen.

## Full-Stack-Integration

Die Stage-4-Integration umfasst:

1. `src/embodiment/specialized_areas.py` — kanonischer Areal-, Topologie- und Referenzprobe-Vertrag;
2. bestehendes `src/embodiment/msba.py` — Modalitätsprofile, Ressourcen-/Energievertrag und Plastizitätskandidaten;
3. bestehendes `src/embodiment/neural_symbiosis.py` — offene periphere Areale und Pipeline-Verträge;
4. bestehendes `src/experiments/msba_lab.py` — E01–E05, Frozen/Random/Shuffle-, Information-Destroyed-, ROI- und Läsionskontrollen;
5. `/api/embodiment/neural-symbiosis` — gemeinsame read-only Projektion von Katalog, Gateway und Stage-4-Vertrag;
6. Wesen/MSBA-Frontend — Darstellung der drei spezialisierten Areale, Skalierungsgrenze, Plastizitätsregel und Forschungsstatus;
7. `scripts/run_stage4_reference.py` — deterministische Engineering-Verifikation;
8. `tests/test_stage4_specialized_neural_areas.py` — Stage-4-spezifische End-to-End-Vertragstests.

## Wissenschaftliche Grenze

Stage 4 darf technisch als abgeschlossen gelten, wenn der Referenzrunner und die zugehörigen Tests grün sind. Das bedeutet **nicht**:

- dass ein 100k-Neuronen-/10M-Synapsen-Netz vollständig dynamisch ausgeführt wurde;
- dass produktive externe neuronale Areale freigeschaltet wurden;
- dass Gateway-Plastizität außerhalb preregistrierter Experimente erlaubt ist;
- dass E01–E05 automatisch wissenschaftliche EVID geworden sind;
- dass biologische Modalitätsareale nachgebildet oder biologisch validiert wären;
- dass `RQ9` oder `RQ11` durch die Engineering-Verifikation beantwortet wären;
- dass ein kausaler Vorteil modalitätsspezifischer Areale gegenüber einer matched unspezialisierten Kontrollarchitektur bereits gezeigt wäre.

Produktive Aktivierung bleibt `LOCKED`. Wissenschaftliche Promotion benötigt weiterhin den bestehenden Review-/EVID-Prozess.


## Digital sensory interface profile

The existing Digital pathway is now explicitly interpreted as a **digital sensory modality**. The canonical interface profile is documented in `docs/02-architecture/MHRN_GATAWAY_NEURAL_INTERFACE.md` and the integration decision `research/decisions/2026-09-25_digital_sensory_interface_integration.md`.

The candidate `DIGITAL-SENSORY-BUS-100X100-v0` specifies a 100 × 100 / 10,000-channel logical population layout shared by query and response contracts. This is an architecture candidate only; it does not claim that arbitrary formulas, code or relational structures have already been bound successfully in spikes.

Stage 4 owns the **transduction and modality pathway** part of this interface. Learned query selection belongs to Stage 5 closed-loop action, while delayed credit/prediction belongs to Stage 6. No new stage is introduced.

The new cross-stage questions are `RQ-GW-008` (source transfer), `RQ-GW-009` (query as learned action) and `RQ-GW-010` (adaptive modality routing). They are prospective and untested.
