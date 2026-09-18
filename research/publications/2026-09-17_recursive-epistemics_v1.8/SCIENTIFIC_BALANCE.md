# Wissenschaftliche Bilanz — Edition 1.8

**Status:** current_wip  
**Autorität:** Publikationssynthese, nicht kanonisches EVID-Register  
**Stand der Prüfung:** `main@774671bcff753489f833b50bbdd3bea7ab3e3169`, 18. September 2026

Diese Bilanz macht die offenen und tragfähigen Aussagen der Edition sichtbar. Sie ersetzt weder Human Review noch EVID-Entscheidungen und erzeugt keine neue Evidenz.

### Stage 0 — Human Review positiv, EVID-Promotion noch offen

Für `RQ-EVAL-006` wurde der Human Review am 18. September 2026 mit `supports_scoped_claim` abgeschlossen. Der eng präregistrierte Claim ist inhaltlich positiv geprüft: Die deklarierten MHRN-Einzelzellverträge für Izhikevich-2003, `lif-current-v1` und das separat behandelte Refractory-Semantik-Mapping konformieren im historischen V2-Lauf mit Brian2 2.10.1 innerhalb der vorab fixierten Toleranzen.

Die `1e-8`-Schwelle war vor Ausführung fixiert; die deutlich kleineren beobachteten Fehler ändern diese Entscheidungsgrenze nicht post hoc. V1 und V2 bleiben getrennte Aussagen: lokale Transition-Konformität hebt den historischen negativen 1000-Tick-Freilaufbefund nicht auf. `H-EVAL-006-C` ist ein Mapping-/Semantikclaim, kein dritter numerischer Konformitätsclaim.

Die Scientific Maturity von Stage 0 beträgt **82,5 %**. Das Kriterium `reviewed_evidence` bleibt `partial`: Der historische Human Review ist positiv abgeschlossen, und inzwischen liegt mit `EXP-STAGE0-20260918-MODEL-CONFORMANCE-V2-PROMO-R1` auch ein **EvidenceEngine-konformer interner Promotion-Replikationslauf als DATA** vor. Er wurde auf neuen vorab deklarierten Seeds `22001–22003` mit unveränderter `1e-8`-Grenze ausgeführt; A/B/C bestanden, `git.dirty=false`, `validity.valid=true`, die vier Provenienz-Digests und ein `source_freeze_sha` sind vorhanden.

Der Lauf erzeugt dennoch nicht selbst EVID. Sein eigener Review-Request steht auf `PENDING`, `automatic_evidence_promotion=false`, `scientific_evidence=false` und `independent_authorship_replication=false`. Erst ein separater positiver Human Review dieses Promotion-Laufs und eine danach getrennte kanonische EVID-Registrierung können die verbleibenden 10 Prozentpunkte des Human-EVID-Kriteriums schließen. Die separate 7,5-%-Lücke für echte unabhängige Replikation bleibt davon unberührt.

## 1. Claim-Ledger als wissenschaftliche Bilanz

Der Claim-Ledger enthält sieben zentrale Syntheseclaims. Ihre Status sind nicht redaktionelle Hinweise, sondern die wissenschaftliche Grenze der Edition 1.8.

| Claim | Thema | Status | Wissenschaftliche Bedeutung |
| --- | --- | --- | --- |
| `SYN-18-001` | Forschungsgenealogie | `methodological_claim` | Rekonstruierte Frühgeschichte bleibt S4, solange keine Originaltranskripte gebunden sind. |
| `SYN-18-002` | Semantization vs. Replay | `DATA_interpretation_pending_review` | CL-001–003 begründen keinen preregistrierten Semantic-over-matched-Raw-Vorteil; die Interpretation bleibt reviewgebunden. |
| `SYN-18-003` | Kausale Zuordnung des Lernens | `open` | Read-only-/Proposal-only-Sprachgrenzen machen Attribution prüfbar, beweisen aber noch nicht, dass der neuronale Kern eine Aufgabe kausal lernt. |
| `SYN-18-004` | Rekursive Epistemik | `argumentative_claim` | Struktureller Vergleich von Objekt- und Forschungsprozess-Gateways; keine Gleichsetzung neuronalen Lernens mit menschlicher Rechtfertigung. |
| `SYN-18-005` | Kontrolle und Welfare | `argumentative_claim` | Normative/ethische Synthese; keine empirische Bewusstseins- oder Wohlfahrtsaussage. |
| `SYN-18-006` | Verlustarme Publikationsinfrastruktur | `implemented_pending_verification` | Byte-/Quelleninventar macht Auslassungen auditierbarer, zertifiziert aber keine semantische Vollständigkeit. |
| `SYN-18-007` | 5D-Geometrie | `open` | Fünf Koordinatenachsen bleiben eine testbare Repräsentationshypothese, kein bestätigter Funktionsvorteil und keine biologische Dimensionsbehauptung. |

### Warum `SYN-18-007` offen bleiben muss

Der bisherige Lauf `EXP-GEN-0047` / `topology_propagation_v1` wird in Edition 1.8 nicht als positiver oder negativer 5D-Befund geführt. Der Human-Review ordnet den genuinen Geometrieeffekt als **NOT TESTED** ein, weil die Zielhypothese nicht angemessen operationalisiert wurde und die Aktivitäts-/Kontrollbedingungen für eine belastbare Dimensionsaussage nicht ausreichen. Die korrekte Schlussfolgerung ist daher nicht „5D funktioniert“ oder „5D funktioniert nicht“, sondern: **der Claim bleibt offen, bis gematchte Dimensions-, Graph-, Metrik- und Ressourcenkontrollen eine spezifische, replizierbare Aussage erlauben.**

Diese Offenheit ist eine zentrale Qualitätsgrenze der 1.8: Ein inadäquates oder zu schwaches Design wird nicht in einen werblichen Null- oder Positivbefund umgedeutet.

### Stage-1-Topologiebefund: `H-SNN-003-B` und 5D strikt trennen

Seit `EXP-S1-TOPO-V2-20260918` liegt für `RQ-SNN-003 / H-SNN-003-B` ein neuer präregistrierter DATA-Befund vor. In einem 64-Neuronen-/246-Kanten-Regime mit getrennten Kalibrier- und Evaluations-Seeds, Activity-Adequacy-Gate und vorab definierten Primärkontrasten unterscheiden sich mehrere Topologiebedingungen in aktiver Reichweite und/oder First-Output-Latenz. Der Laufstatus `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL` bedeutet hier: **Topologie beeinflusst die Propagationsdynamik innerhalb des untersuchten Small-SNN-Operating-Envelope.**

Diese Aussage darf nicht in „5D ist überlegen“ umformuliert werden. Im Gegenteil erreichten `5d_shuffled` und `random_graph` den Output in diesem Aufbau früher als die reguläre 5D-Anordnung. Alle sechs Bedingungen besitzen dasselbe 246-Kanten-Budget; die Unterschiede sind daher nicht als bloßer Dichte-/Sparsity-Effekt zu beschreiben. Zugleich sättigt `active_fraction` für 1d/2d/3d bei 1,0, sodass dieser Endpunkt die drei Bedingungen im gewählten Regime nicht diskriminiert. Der Latenzendpunkt diskriminiert breiter; trotz seines Namens trat in der Evaluation keine tatsächliche Zensierung auf (Sentinel wäre 129 bei 128 Ticks). Das neue Resultat stärkt deshalb den allgemeinen Topologieclaim, während der dimensionsspezifische 5D-Claim offen bleibt. Bis Human Review abgeschlossen ist, bleibt der Befund DATA-only.

### Interne Replikation: V3-R1 löst die V2-Ceiling-Grenze auf

`EXP-S1-TOPO-V3-R1-20260918` übernimmt den V2-Operating-Envelope unverändert (64 Neuronen, 246 Kanten, Gewicht 55.0, 128 Ticks), verwendet aber neue Seeds und prospektiv definierte zeitaufgelöste Endpunkte. Ein davor ausgeführter V3-Lauf wird wegen einer falsch implementierten Holm-Familie **nicht** als konfirmatorische Analyse verwendet; seine DATA bleiben unverändert als Auditspur.

Im korrigierten R1-Lauf steigt die mediane `activation_auc_0_32` von 22,15625 (1d) über 26,5703125 (2d) auf 28,0078125 (3d), während die Halbaktivierungslatenz von 10 über 6 auf 4 Ticks fällt. Die low-dimensionalen Kontraste sind nach einer gemeinsamen Holm-Korrektur über alle zehn Primärtests signifikant. Alle fünf V2-Kontraste der First-Output-Latenz replizieren auf den neuen Seeds in derselben Richtung.

Damit ist die frühere `active_fraction=1.0`-Sättigung präziser einzuordnen: Sie begrenzt einen terminalen Endpunkt, verdeckt aber nicht die zeitliche Topologiedynamik. Der Status bleibt **interne DATA-Replikation pending Human Review**, nicht unabhängige EVID.

### Konsequenz: `H-5D-005-A` bleibt open/untested

Kanonisch bleibt `RQ-5D-005` **open** und `H-5D-005-A` **untested**. Weder `EXP-GEN-0047` noch das neue 64-Neuronen-Stage-1-Experiment sind für diese stärkere dimensionsspezifische Hypothese ein hinreichender Evidenzbeitrag. Die nächste **5D-spezifische** Prüfung muss mindestens folgende Testadäquanz einfrieren:

- **≥ 1.000 Neuronen pro Bedingung**;
- im Mittel **≥ 10 eingehende Synapsen pro Neuron**;
- **distanzabhängige Konnektivitätswahrscheinlichkeit**, sodass Geometrie kausal auf den realisierten Graphen wirken kann; geometrieabhängige Delays können zusätzlich geprüft werden;
- degree-/density-matched 1D/2D/3D/5D-, `5d_shuffled`- und `random_graph`-Kontrollen;
- Multi-Neuron-Stimulus, Activity-Adequacy-Gate, unabhängige Seeds, vorab fixierte Endpunkte/Inferenz und clean-tree Graph-/Source-Provenienz.

Scheitert bereits das Activity-Adequacy-Gate, lautet das Ergebnis erneut `NOT_TESTED`; daraus darf kein 5D-Nullbefund entstehen.

## 2. Nächster empirischer Schritt: `OBJ-MEM-COMPRESSION-001`

Der nächste vorbereitete empirische Schritt ist `LP-20260917194217 / OBJ-MEM-COMPRESSION-001`. Er entsteht aus der negativen bzw. nicht bestätigenden CL-002/CL-003-Linie, stellt aber **eine andere Frage**: nicht „lernt SemanticMemory besser?“, sondern „kann semantische Prototypkonsolidierung Speicher um Faktor 10 reduzieren, ohne die Retention unter die vorab definierte Grenze fallen zu lassen?“.

Die prospektive Kernhypothese lautet: **`semantic_prototype_replay_10pct_budget` erreicht bei 10 % des Raw-Replay-Speicherbudgets mindestens 95 % der Retention von `raw_replay_full_budget`.** Externe Arbeiten liefern hierfür den Vergleichsraum, nicht die konkrete Erfolgsgrenze: [McClelland et al., 1995](REFERENCES.md#ref-MCCLELLAND1995), [D'Alba et al., 2025](REFERENCES.md#ref-DALBA2025) und [Shi et al., 2025](REFERENCES.md#ref-SHI2025).

Die Rollenentscheidung wird **vor DATA** festgelegt: Ein positives Ergebnis stützt eine begrenzte Kompressionsrolle von SemanticMemory unter genau diesem Protokoll; ein negatives Ergebnis stützt diese Kompressionsrolle für den getesteten Mechanismus nicht. Generalisierung, Langzeitgedächtnis oder Weltmodell-Brücke dürfen nur als neue, eigenständig begründete und präregistrierte Rollen geprüft werden.

`LP-20260917194217-R1` ist weiterhin `proposal_only` und nicht durch die historische Approval des Originalplans gedeckt. Der unmittelbar nächste Arbeitsschritt ist daher **Präregistrierungsvorbereitung**, nicht Ausführung: kanonische RQ/H-Bindung, exakte Speicherbudget-Messung, Seed-/Taskplan, Retentionsaggregation, Äquivalenz-/Inferenzregel, Ausschlüsse/Failure-Regeln, Analysevertrag und Source-/Config-Freeze müssen vor einem ausführungsfähigen Status feststehen.

## 3. Wissenschaftliche Nebenstränge

Der kanonische Index [`research/paper_offshoots/README.md`](../../paper_offshoots/README.md) ist in `main` vorhanden und in Edition 1.8 semantisch integriert. Er enthält sechs begrenzte Paper-Ideen:

1. `PO-001` — empirische Grenzen semantischer Verdichtung im Continual Learning (`in_preparation`);
2. `PO-002` — Content/Compute-Trennung und kontrollierte periphere Werkzeuge (`concept`);
3. `PO-003` — Scientific Integrity und rekursive Epistemik in KI-assistierter Einzelforschung (`concept`);
4. `PO-004` — Post-Objective Transition und Corrigibility (`planned`);
5. `PO-005` — Geometrie-zu-Dynamik-Kopplung multidimensionaler SNN-Topologien (`design_required`);
6. `PO-006` — kontrolliertes synthetisches Embodiment (`data_available_review_open`).

Die Nebenstränge sind **Forschungsplanung, keine Publikation und keine DATA/EVID**. Sie dürfen die Edition 1.8 nicht rückwirkend als empirische Evidenzquelle verwenden.

## 4. Was „vollständig“ hier bedeutet

Nach dem **aktuellen Manifest der Edition 1.8** sind dokumentiert:

- 9.412 Quelldateien im gepinnten Baseline-Inventar,
- 18.022 indexierte Markdown-Abschnitte,
- 411 erhaltene historische Publikationsdateien,
- 1.965 Repository-/Rekonstruktionsereignisse,
- 96 projizierte Forschungsobjekte,
- 7 Vorarbeiten,
- 24 Einträge im semantischen Content-Integration-Ledger.

Das stützt die Aussage, dass die dokumentierte Materialabdeckung hoch ist. Es ist **keine absolute Vollständigkeitszertifizierung**. Das Manifest setzt ausdrücklich:

- `complete_chat_archive_available = false`,
- `semantic_completeness_certified = false`,
- `material_prior_work_coverage_declared = true`.

Daher lautet die belastbare Formulierung: **Nach dem aktuellen Manifest ist keine wesentliche dokumentierte Forschungslinie als verloren ausgewiesen; tatsächliche semantische Vollständigkeit ist jedoch nicht zertifiziert und muss durch Stichproben, externe Audits oder zusätzliche Primärquellen weiter geprüft werden.**

## 5. Reader- und Versionsgrenze

Der aktive Publication Viewer folgt `research/publications/catalog.json` und öffnet Edition 1.8. Der Ordner `research/publications/reader/` gehört zur historischen Lesefassung vom 7. September 2026 und wird aus Provenienzgründen nicht als aktueller Reader umgeschrieben. Siehe [historischen Reader-Hinweis](../HISTORICAL_READER.md).

## 6. Branch- und Zitierprovenienz

Die Arbeitsbranches, aus denen Edition 1.8 und ihre Viewer-/Corpus-Erweiterungen hervorgegangen sind, werden vor einer Branch-Bereinigung in [`EDITION_GENEALOGY.md`](EDITION_GENEALOGY.md) mit Namen und Tip-SHA dokumentiert. Wissenschaftliche Zitation soll trotzdem Commit-SHAs und Editionspfade verwenden, nicht mutable Branch-Namen.

Für die Arbeit steht eine eigene [`CITATION.cff`](CITATION.cff) bereit. Sie verwendet denselben Autor (**Thomas Heisig**) und dieselbe Lizenz (**MIT**) wie die Software-`CITATION.cff` im Repository-Root, hält Software und Publikation aber als getrennte zitierbare Objekte auseinander.
