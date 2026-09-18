# Wissenschaftliche Bilanz — Edition 1.8

**Status:** current_wip  
**Autorität:** Publikationssynthese, nicht kanonisches EVID-Register  
**Stand der Prüfung:** `main@774671bcff753489f833b50bbdd3bea7ab3e3169`, 18. September 2026

Diese Bilanz macht die offenen und tragfähigen Aussagen der Edition sichtbar. Sie ersetzt weder Human Review noch EVID-Entscheidungen und erzeugt keine neue Evidenz.

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

## 2. Wissenschaftliche Nebenstränge

Der kanonische Index [`research/paper_offshoots/README.md`](../../paper_offshoots/README.md) ist in `main` vorhanden und in Edition 1.8 semantisch integriert. Er enthält sechs begrenzte Paper-Ideen:

1. `PO-001` — empirische Grenzen semantischer Verdichtung im Continual Learning (`in_preparation`);
2. `PO-002` — Content/Compute-Trennung und kontrollierte periphere Werkzeuge (`concept`);
3. `PO-003` — Scientific Integrity und rekursive Epistemik in KI-assistierter Einzelforschung (`concept`);
4. `PO-004` — Post-Objective Transition und Corrigibility (`planned`);
5. `PO-005` — Geometrie-zu-Dynamik-Kopplung multidimensionaler SNN-Topologien (`design_required`);
6. `PO-006` — kontrolliertes synthetisches Embodiment (`data_available_review_open`).

Die Nebenstränge sind **Forschungsplanung, keine Publikation und keine DATA/EVID**. Sie dürfen die Edition 1.8 nicht rückwirkend als empirische Evidenzquelle verwenden.

## 3. Was „vollständig“ hier bedeutet

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

## 4. Reader- und Versionsgrenze

Der aktive Publication Viewer folgt `research/publications/catalog.json` und öffnet Edition 1.8. Der Ordner `research/publications/reader/` gehört zur historischen Lesefassung vom 7. September 2026 und wird aus Provenienzgründen nicht als aktueller Reader umgeschrieben. Siehe [historischen Reader-Hinweis](../HISTORICAL_READER.md).

## 5. Branch- und Zitierprovenienz

Die Arbeitsbranches, aus denen Edition 1.8 und ihre Viewer-/Corpus-Erweiterungen hervorgegangen sind, werden vor einer Branch-Bereinigung in [`EDITION_GENEALOGY.md`](EDITION_GENEALOGY.md) mit Namen und Tip-SHA dokumentiert. Wissenschaftliche Zitation soll trotzdem Commit-SHAs und Editionspfade verwenden, nicht mutable Branch-Namen.

Für die Arbeit steht eine eigene [`CITATION.cff`](CITATION.cff) bereit. Sie verwendet denselben Autor (**Thomas Heisig**) und dieselbe Lizenz (**MIT**) wie die Software-`CITATION.cff` im Repository-Root, hält Software und Publikation aber als getrennte zitierbare Objekte auseinander.
