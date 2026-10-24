# Wissenschaftliche Bilanz â€” Edition 1.8

**Status:** current_wip  
**AutoritÃ¤t:** Publikationssynthese, nicht kanonisches EVID-Register  
**Redaktioneller Abgleich:** 4. Oktober 2026, Ausgangsstand `develop@6c417c2e9e1240f9a649601ca1e9f5e0a249c388`. Dieser PrÃ¼fstand ist kein neuer Experiment-Freeze oder Human Review.

Diese Bilanz macht die offenen und tragfÃ¤higen Aussagen der Edition sichtbar. Sie ersetzt weder Human Review noch EVID-Entscheidungen und erzeugt keine neue Evidenz.

### Stage 0 â€” Human Review und EVID-Promotion abgeschlossen

FÃ¼r `RQ-EVAL-006` wurde der Human Review am 18. September 2026 mit `supports_scoped_claim` abgeschlossen. Der eng prÃ¤registrierte Claim ist inhaltlich positiv geprÃ¼ft: Die deklarierten MHRN-EinzelzellvertrÃ¤ge fÃ¼r Izhikevich-2003, `lif-current-v1` und das separat behandelte Refractory-Semantik-Mapping konformieren im historischen V2-Lauf mit Brian2 2.10.1 innerhalb der vorab fixierten Toleranzen.

Die `1e-8`-Schwelle war vor AusfÃ¼hrung fixiert; die deutlich kleineren beobachteten Fehler Ã¤ndern diese Entscheidungsgrenze nicht post hoc. V1 und V2 bleiben getrennte Aussagen: lokale Transition-KonformitÃ¤t hebt den historischen negativen 1000-Tick-Freilaufbefund nicht auf. `H-EVAL-006-C` ist ein Mapping-/Semantikclaim, kein dritter numerischer KonformitÃ¤tsclaim.

Die Scientific Maturity von Stage 0 betrÃ¤gt **92,5 %**. Das Kriterium `reviewed_evidence` steht auf `met`: Der historische Human Review ist positiv abgeschlossen; zusÃ¤tzlich wurde `EXP-STAGE0-20260918-MODEL-CONFORMANCE-V2-PROMO-R1` auf neuen vorab deklarierten Seeds `22001â€“22003` unter dem aktuellen EvidenceEngine-Provenienzvertrag ausgefÃ¼hrt. A/B/C bestanden, `git.dirty=false`, `validity.valid=true`, die vier Provenienz-Digests und ein `source_freeze_sha` sind vorhanden.

Der Human Review des Promotion-Laufs wurde kanonisch in `human_review.json` gebunden und der scoped Claim anschlieÃŸend getrennt als `EVID-2026-18` registriert. Die automatische Promotion bleibt weiterhin deaktiviert; die Registrierung ist ein expliziter wissenschaftlicher Governance-Schritt. `independent_authorship_replication=false` bleibt unverÃ¤ndert. Damit verbleiben **7,5 Prozentpunkte** bis 100 %, die ausschlieÃŸlich durch die separat definierte unabhÃ¤ngige Replikation geschlossen werden kÃ¶nnen.

## 1. Claim-Ledger als wissenschaftliche Bilanz

Der Claim-Ledger enthÃ¤lt sieben zentrale Syntheseclaims. Ihre Status sind nicht redaktionelle Hinweise, sondern die wissenschaftliche Grenze der Edition 1.8.

| Claim | Thema | Status | Wissenschaftliche Bedeutung |
| --- | --- | --- | --- |
| `SYN-18-001` | Forschungsgenealogie | `methodological_claim` | Rekonstruierte FrÃ¼hgeschichte bleibt S4, solange keine Originaltranskripte gebunden sind. |
| `SYN-18-002` | Semantization vs. Replay | `DATA_interpretation_pending_review` | CL-001â€“003 begrÃ¼nden keinen preregistrierten Semantic-over-matched-Raw-Vorteil; die Interpretation bleibt reviewgebunden. |
| `SYN-18-003` | Kausale Zuordnung des Lernens | `open` | Read-only-/Proposal-only-Sprachgrenzen machen Attribution prÃ¼fbar, beweisen aber noch nicht, dass der neuronale Kern eine Aufgabe kausal lernt. |
| `SYN-18-004` | Rekursive Epistemik | `argumentative_claim` | Struktureller Vergleich von Objekt- und Forschungsprozess-Gateways; keine Gleichsetzung neuronalen Lernens mit menschlicher Rechtfertigung. |
| `SYN-18-005` | Kontrolle und Welfare | `argumentative_claim` | Normative/ethische Synthese; keine empirische Bewusstseins- oder Wohlfahrtsaussage. |
| `SYN-18-006` | Verlustarme Publikationsinfrastruktur | `implemented_pending_verification` | Byte-/Quelleninventar macht Auslassungen auditierbarer, zertifiziert aber keine semantische VollstÃ¤ndigkeit. |
| `SYN-18-007` | 5D-Geometrie | `open` | FÃ¼nf Koordinatenachsen bleiben eine testbare ReprÃ¤sentationshypothese, kein bestÃ¤tigter Funktionsvorteil und keine biologische Dimensionsbehauptung. |

### Warum `SYN-18-007` offen bleiben muss

Der bisherige Lauf `EXP-GEN-0047` / `topology_propagation_v1` wird in Edition 1.8 nicht als positiver oder negativer 5D-Befund gefÃ¼hrt. Der Human-Review ordnet den genuinen Geometrieeffekt als **NOT TESTED** ein, weil die Zielhypothese nicht angemessen operationalisiert wurde und die AktivitÃ¤ts-/Kontrollbedingungen fÃ¼r eine belastbare Dimensionsaussage nicht ausreichen. Die korrekte Schlussfolgerung ist daher nicht â€ž5D funktioniertâ€œ oder â€ž5D funktioniert nichtâ€œ, sondern: **der Claim bleibt offen, bis gematchte Dimensions-, Graph-, Metrik- und Ressourcenkontrollen eine spezifische, replizierbare Aussage erlauben.**

Diese Offenheit ist eine zentrale QualitÃ¤tsgrenze der 1.8: Ein inadÃ¤quates oder zu schwaches Design wird nicht in einen werblichen Null- oder Positivbefund umgedeutet.

### Stage-1-Topologiebefund: `H-SNN-003-B` und 5D strikt trennen

Seit `EXP-S1-TOPO-V2-20260918` liegt fÃ¼r `RQ-SNN-003 / H-SNN-003-B` ein neuer prÃ¤registrierter DATA-Befund vor. In einem 64-Neuronen-/246-Kanten-Regime mit getrennten Kalibrier- und Evaluations-Seeds, Activity-Adequacy-Gate und vorab definierten PrimÃ¤rkontrasten unterscheiden sich mehrere Topologiebedingungen in aktiver Reichweite und/oder First-Output-Latenz. Der Laufstatus `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL` bedeutet hier: **Topologie beeinflusst die Propagationsdynamik innerhalb des untersuchten Small-SNN-Operating-Envelope.**

Diese Aussage darf nicht in â€ž5D ist Ã¼berlegenâ€œ umformuliert werden. Im Gegenteil erreichten `5d_shuffled` und `random_graph` den Output in diesem Aufbau frÃ¼her als die regulÃ¤re 5D-Anordnung. Alle sechs Bedingungen besitzen dasselbe 246-Kanten-Budget; die Unterschiede sind daher nicht als bloÃŸer Dichte-/Sparsity-Effekt zu beschreiben. Zugleich sÃ¤ttigt `active_fraction` fÃ¼r 1d/2d/3d bei 1,0, sodass dieser Endpunkt die drei Bedingungen im gewÃ¤hlten Regime nicht diskriminiert. Der Latenzendpunkt diskriminiert breiter; trotz seines Namens trat in der Evaluation keine tatsÃ¤chliche Zensierung auf (Sentinel wÃ¤re 129 bei 128 Ticks). Das neue Resultat stÃ¤rkt deshalb den allgemeinen Topologieclaim, wÃ¤hrend der dimensionsspezifische 5D-Claim offen bleibt. Der historische Human Review akzeptiert die begrenzte Interpretation; die historischen V2-DATA bleiben unverÃ¤ndert. Der heutige Evidenzvertrag wurde anschlieÃŸend prospektiv Ã¼ber `EXP-S1-TOPO-PROMO-R1-20260927` geschlossen; der kanonische Human Review `supports` fÃ¼hrte Ã¼ber die separate EvidenceEngine-Promotion zu `EVID-2026-19`.

### Interne Replikation: V3-R1 lÃ¶st die V2-Ceiling-Grenze auf

`EXP-S1-TOPO-V3-R1-20260918` Ã¼bernimmt den V2-Operating-Envelope unverÃ¤ndert (64 Neuronen, 246 Kanten, Gewicht 55.0, 128 Ticks), verwendet aber neue Seeds und prospektiv definierte zeitaufgelÃ¶ste Endpunkte. Ein davor ausgefÃ¼hrter V3-Lauf wird wegen einer falsch implementierten Holm-Familie **nicht** als konfirmatorische Analyse verwendet; seine DATA bleiben unverÃ¤ndert als Auditspur.

Im korrigierten R1-Lauf steigt die mediane `activation_auc_0_32` von 22,15625 (1d) Ã¼ber 26,5703125 (2d) auf 28,0078125 (3d), wÃ¤hrend die Halbaktivierungslatenz von 10 Ã¼ber 6 auf 4 Ticks fÃ¤llt. Die low-dimensionalen Kontraste sind nach einer gemeinsamen Holm-Korrektur Ã¼ber alle zehn PrimÃ¤rtests signifikant. Alle fÃ¼nf V2-Kontraste der First-Output-Latenz replizieren auf den neuen Seeds in derselben Richtung.

Damit ist die frÃ¼here `active_fraction=1.0`-SÃ¤ttigung prÃ¤ziser einzuordnen: Sie begrenzt einen terminalen Endpunkt, verdeckt aber nicht die zeitliche Topologiedynamik. V3-R1 bleibt eine human-reviewed **interne DATA-Replikation**, nicht unabhÃ¤ngige Replikation; die spÃ¤tere kanonische EVID stammt separat aus dem prospektiven Promotion-Lauf `EXP-S1-TOPO-PROMO-R1-20260927`.

### Stage-1-Maturity, zweite EVID-Linie und offene Replikation

Die Scientific Maturity von Stage 1 betrÃ¤gt jetzt **85 %**. RQ/H, prÃ¤registrierte Protokolle, source-bound DATA, Attribution und das 20-%-Kriterium `reviewed_evidence` sind erfÃ¼llt. Der Replikationsblock bleibt mit 0/15 offen. Zwei getrennte EVID-Linien werden nicht doppelt als Maturity-Punkte gezÃ¤hlt.

Die Topologielinie besitzt nach dem prospektiven Promotion-Lauf `EVID-2026-19`. Als zweite Funktionslinie besitzt `RQ-TEMP-002 / H-TEMP-002-A` nach `EXP-S1-TEMP-PROMO-R1-20260927` und einem Human Review `supports` mit dokumentierter Task-SÃ¤ttigung `EVID-2026-20`. Der Decoder unterscheidet `forward`, `reverse` und `simultaneous`; die perfekte simultane Klassenaccuracy ist nicht als Forward/Reverse-Order-Accuracy zu lesen.

Eine explorativ beobachtete Effizienzsystematik wurde bewusst nicht in `EVID-2026-19` integriert. `H-SNN-003-C / CLAIM-S1-EFFICIENCY-001` bleiben `untested`; die dafÃ¼r entworfene R1 ist nach einem gÃ¼ltigen negativen Recruitment-Kalibrationsgate freeze-blockiert und erzeugte keine konfirmatorische Evaluation.

Der nÃ¤chste mÃ¶gliche Maturity-Zuwachs liegt ausschlieÃŸlich im Replikationsblock. Die projektseitige Brian2-Cross-Implementation kann bei bestandenem Pre-Freeze-Vertrag, Reference-DATA, Human Review und kanonischer Statusentscheidung maximal 7,5/15 als partielle Replikation beitragen. Failed oder Inconclusive bleiben wissenschaftlich gleichwertig sichtbar und erhÃ¶hen den Score nicht. Volle 15/15 bleiben externer unabhÃ¤ngiger Replikation vorbehalten.

### Konsequenz: `H-5D-005-A` bleibt open/untested

Kanonisch bleibt `RQ-5D-005` **open** und `H-5D-005-A` **untested**. Weder `EXP-GEN-0047` noch das neue 64-Neuronen-Stage-1-Experiment sind fÃ¼r diese stÃ¤rkere dimensionsspezifische Hypothese ein hinreichender Evidenzbeitrag. Die nÃ¤chste **5D-spezifische** PrÃ¼fung muss mindestens folgende TestadÃ¤quanz einfrieren:

- **â‰¥ 1.000 Neuronen pro Bedingung**;
- im Mittel **â‰¥ 10 eingehende Synapsen pro Neuron**;
- **distanzabhÃ¤ngige KonnektivitÃ¤tswahrscheinlichkeit**, sodass Geometrie kausal auf den realisierten Graphen wirken kann; geometrieabhÃ¤ngige Delays kÃ¶nnen zusÃ¤tzlich geprÃ¼ft werden;
- degree-/density-matched 1D/2D/3D/5D-, `5d_shuffled`- und `random_graph`-Kontrollen;
- Multi-Neuron-Stimulus, Activity-Adequacy-Gate, unabhÃ¤ngige Seeds, vorab fixierte Endpunkte/Inferenz und clean-tree Graph-/Source-Provenienz.

Scheitert bereits das Activity-Adequacy-Gate, lautet das Ergebnis erneut `NOT_TESTED`; daraus darf kein 5D-Nullbefund entstehen.

## 2. NÃ¤chster empirischer Schritt: `OBJ-MEM-COMPRESSION-001`

Der nÃ¤chste vorbereitete empirische Schritt ist `LP-20260917194217 / OBJ-MEM-COMPRESSION-001`. Er entsteht aus der negativen bzw. nicht bestÃ¤tigenden CL-002/CL-003-Linie, stellt aber **eine andere Frage**: nicht â€žlernt SemanticMemory besser?â€œ, sondern â€žkann semantische Prototypkonsolidierung Speicher um Faktor 10 reduzieren, ohne die Retention unter die vorab definierte Grenze fallen zu lassen?â€œ.

Die prospektive Kernhypothese lautet: **`semantic_prototype_replay_10pct_budget` erreicht bei 10 % des Raw-Replay-Speicherbudgets mindestens 95 % der Retention von `raw_replay_full_budget`.** Externe Arbeiten liefern hierfÃ¼r den Vergleichsraum, nicht die konkrete Erfolgsgrenze: [McClelland et al., 1995](REFERENCES.md#ref-MCCLELLAND1995), [D'Alba et al., 2025](REFERENCES.md#ref-DALBA2025) und [Shi et al., 2025](REFERENCES.md#ref-SHI2025).

Die Rollenentscheidung wird **vor DATA** festgelegt: Ein positives Ergebnis stÃ¼tzt eine begrenzte Kompressionsrolle von SemanticMemory unter genau diesem Protokoll; ein negatives Ergebnis stÃ¼tzt diese Kompressionsrolle fÃ¼r den getesteten Mechanismus nicht. Generalisierung, LangzeitgedÃ¤chtnis oder Weltmodell-BrÃ¼cke dÃ¼rfen nur als neue, eigenstÃ¤ndig begrÃ¼ndete und prÃ¤registrierte Rollen geprÃ¼ft werden.

`LP-20260917194217-R1` ist weiterhin `proposal_only` und nicht durch die historische Approval des Originalplans gedeckt. Der unmittelbar nÃ¤chste Arbeitsschritt ist daher **PrÃ¤registrierungsvorbereitung**, nicht AusfÃ¼hrung: kanonische RQ/H-Bindung, exakte Speicherbudget-Messung, Seed-/Taskplan, Retentionsaggregation, Ã„quivalenz-/Inferenzregel, AusschlÃ¼sse/Failure-Regeln, Analysevertrag und Source-/Config-Freeze mÃ¼ssen vor einem ausfÃ¼hrungsfÃ¤higen Status feststehen.

## 3. Wissenschaftliche NebenstrÃ¤nge

Der kanonische Index [`research/paper_offshoots/README.md`](../../paper_offshoots/README.md) ist in `main` vorhanden und in Edition 1.8 semantisch integriert. Er enthÃ¤lt sechs begrenzte Paper-Ideen:

1. `PO-001` â€” empirische Grenzen semantischer Verdichtung im Continual Learning (`in_preparation`);
2. `PO-002` â€” Content/Compute-Trennung und kontrollierte periphere Werkzeuge (`concept`);
3. `PO-003` â€” Scientific Integrity und rekursive Epistemik in KI-assistierter Einzelforschung (`concept`);
4. `PO-004` â€” Post-Objective Transition und Corrigibility (`planned`);
5. `PO-005` â€” Geometrie-zu-Dynamik-Kopplung multidimensionaler SNN-Topologien (`design_required`);
6. `PO-006` â€” kontrolliertes synthetisches Embodiment (`data_available_review_open`).

Die NebenstrÃ¤nge sind **Forschungsplanung, keine Publikation und keine DATA/EVID**. Sie dÃ¼rfen die Edition 1.8 nicht rÃ¼ckwirkend als empirische Evidenzquelle verwenden.

## 4. Was â€žvollstÃ¤ndigâ€œ hier bedeutet

Nach dem **aktuellen Manifest der Edition 1.8** sind dokumentiert:

- 9.412 Quelldateien im gepinnten Baseline-Inventar,
- 18.022 indexierte Markdown-Abschnitte,
- 411 erhaltene historische Publikationsdateien,
- 1.965 Repository-/Rekonstruktionsereignisse,
- 107 projizierte Forschungsobjekte,
- 7 Vorarbeiten,
- 31 EintrÃ¤ge im semantischen Content-Integration-Ledger.

Das stÃ¼tzt die Aussage, dass die dokumentierte Materialabdeckung hoch ist. Es ist **keine absolute VollstÃ¤ndigkeitszertifizierung**. Das Manifest setzt ausdrÃ¼cklich:

- `complete_chat_archive_available = false`,
- `semantic_completeness_certified = false`,
- `material_prior_work_coverage_declared = true`.

Daher lautet die belastbare Formulierung: **Nach dem aktuellen Manifest ist keine wesentliche dokumentierte Forschungslinie als verloren ausgewiesen; tatsÃ¤chliche semantische VollstÃ¤ndigkeit ist jedoch nicht zertifiziert und muss durch Stichproben, externe Audits oder zusÃ¤tzliche PrimÃ¤rquellen weiter geprÃ¼ft werden.**

## 5. Reader- und Versionsgrenze

Der aktive Publication Viewer folgt `research/publications/catalog.json` und Ã¶ffnet Edition 1.8. Der Ordner `research/publications/reader/` gehÃ¶rt zur historischen Lesefassung vom 7. September 2026 und wird aus ProvenienzgrÃ¼nden nicht als aktueller Reader umgeschrieben. Siehe [historischen Reader-Hinweis](../HISTORICAL_READER.md).

## 6. Branch- und Zitierprovenienz

Die Arbeitsbranches, aus denen Edition 1.8 und ihre Viewer-/Corpus-Erweiterungen hervorgegangen sind, werden vor einer Branch-Bereinigung in [`EDITION_GENEALOGY.md`](EDITION_GENEALOGY.md) mit Namen und Tip-SHA dokumentiert. Wissenschaftliche Zitation soll trotzdem Commit-SHAs und Editionspfade verwenden, nicht mutable Branch-Namen.

FÃ¼r die Arbeit steht eine eigene [`CITATION.cff`](CITATION.cff) bereit. Sie verwendet denselben Autor (**Thomas Heisig**) und dieselbe Lizenz (**MIT**) wie die Software-`CITATION.cff` im Repository-Root, hÃ¤lt Software und Publikation aber als getrennte zitierbare Objekte auseinander.

## Nachtrag: AusfÃ¼hrung und Erkenntnis seit Ende September

Die [ergÃ¤nzende Synthese](parts/10_synthesis.md) bindet EXP-GEN-0048 und die 23 konzeptuellen Audit-LÃ¤ufe vom 1. Oktober. Der Tick-Vertragsfehler liefert keinen gÃ¼ltigen Determinismustest. Die 276 AuditdatensÃ¤tze sind erzeugte Vorlagen mit `audit_complete=false`; die REVIEW-Serie wartet auf menschliche Beurteilung. Technische Fertigstellung ist hier keine inhaltliche Bewertung. Diese Integration verÃ¤ndert keine DATA, Human Reviews, EVID oder Stage-Scores.
