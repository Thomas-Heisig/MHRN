# MHRN Development Roadmap

**Canonical roadmap for active `develop`; `main` is release-only**  
**Baseline:** `mhrn-core 0.6.0a7`
**Updated:** 2026-10-04

## 2026-10-04 Gateway Plastic preregistration and execution boundary

- The seven registered `RQ-GW-*` operational protocols are `boundary_audit`
  contracts with `direct_test_of_hypothesis=false`; their seed lists describe
  audit reexecution, not independent Gateway Plastic runs.
- The Gateway activation route accepts caller-provided preregistration JSON and
  starts one runtime seed. There is no registered functional Plastic runner,
  frozen input-frame sequence, or executable stop rule to define a reproducible
  trial across independent runtime instances.
- Keep registry-backed Plastic activation and multi-seed execution open until
  a suitable frozen functional protocol and runner contract exist. No Gateway
  DATA/EVID is inferred from the current audit protocols or activation status.

## 2026-10-04 Stage-3 plastic-network scale benchmark

- Added `scripts/benchmark_plastic_network.py`, separate from the small
	mechanism reference. It uses a deterministic bipartite graph, a real
	`LearningEngine` hook, preflight memory bounds, `asymmetric`, `symmetric`, and
	`off` controls, and uniform or heterogeneous-cohort stimuli. Numeric
	boundedness is reported separately from ongoing spikes, active-weight
	fraction, and workload-required weight diversity. Candidate visits/s is an
	operation-count estimate, not a hardware counter. Receipts include workload,
	software and CPU metadata; all remain engineering-only.
- Matched 10,000-neuron / 100,000-synapse runs (seed 42, 100 epochs): the
	heterogeneous asymmetric profile ended with 56.25% of weights at the lower
	bound, 43.75% active and positive variance; the symmetric profile ended with
	43.75% at the lower bound and 18.75% at the upper bound; the learning-off
	profile retained all weights at 0.05. The earlier uniform-input profile drove
	all weights to zero. Its identical weights are expected under that symmetric
	input/topology; it is not evidence by itself of an update implementation bug.
- At 100,000 neurons / 1M synapses for 20 heterogeneous asymmetric epochs, the
	measured Python peak was about 1.03 GB, the estimated candidate-visit rate
	about 210k/s, and 50% of weights remained active. These workload-specific
	profiles do not establish general or long-horizon stability.
- The declared 100,000-neuron / 10M-synapse upper point remains unmeasured:
	its preflight estimate is 19.45 GiB, exceeding this machine's available RAM.
	Full Stage-3 scale benchmarking remains open pending suitable hardware.
- Related work now includes verified STDP/homeostasis/continual-learning and
	neural-simulator sources. No Brian 2/NEST/Norse head-to-head is claimed until
	model semantics, workload, hardware, precision and timing policy are matched.

## 2026-10-02 CUDA-/Parity-UI-Provenienz

- Playground-Diagnosen zeigen je Request `PENDING`, `RUNNING`, `PASSED`,
	`FAILED` oder `COMPLETED`, dazu Start/Endzeit und Laufzeit.
- Ergebnisflächen trennen CUDA-1.3, CUDA-1.4 und CUDA-1.5; die bereits
	vorhandene Integrationsübersicht verknüpft Wave 4, FE-3, Hardware-Acceptance,
	PAN Wave 5B und das nächste Gate.
- Der CUDA-Status meldet den Repository-HEAD, kennzeichnet aber den
	Source-Working-Tree-Digest, dessen Scope sowie geänderte relevante Pfade.
- Abgeschlossene und fehlgeschlagene Diagnose-Requests werden als atomare,
	SHA-256-geprüfte JSON-Receipts unter dem lokalen gitignorierten
	`artifacts/cuda_diagnostics/` aufbewahrt und über einen validierten API-Link
	abrufbar gemacht.
- Hardware-Receipts enthalten bei erfolgreicher Auflösung GPU-Modell,
	PCI-Bus-ID, Treiberversion und einen gehashten Geräte-UUID; wenn die Identität
	nicht auflösbar ist, bleibt sie ausdrücklich `unavailable`.
- Sichere Cancel-/Resume-Semantik fehlt weiterhin: CUDA-Rekurrenz läuft als
	ein Kernel bis zur Synchronisierung; Builder-, Cue- und Transferläufe sind
	blockierende Aufrufe ohne Cancel-Token/Resume-Checkpoint. Die UI darf daraus
	keinen künstlichen Fortschritt oder unsicheren Abbruch ableiten.
- Playground-Diagnostik bleibt Engineering-/Exploratory-Output, niemals DATA,
	EVID oder Hardware-Acceptance. Echter Fortschritt/Abbruch bleibt offen.

## 2026-10-02 R0 Research-Catalog-Abschluss

- Der generierte Katalogaudit ist `CLEAN`; nichtkanonische Referenzen sind
	begründet als historisch, Testfixture oder Vorschlag klassifiziert.
- Es gibt keine disallowed missing RQ/H IDs, Registry-Linkfehler oder stale
	Allow-List-Einträge.
- 95 operationale Protokolle besitzen gültige Preregistrierungen und
	registrierte Freeze-Status. Das ist ein Governance-/Engineeringbefund,
	keine wissenschaftliche Evidenz.

## 2026-10-01 Konzeptaudit-Ausführung und Review-Routing

- Die 22 zuvor ausstehenden kognitiven, epistemischen und Welfare-
	Konzeptaudit-Protokolle wurden mit ihren registrierten Seeds sequenziell
	ausgeführt.
- Ihre Ergebnisse bleiben ausdrücklich methodische `EXPLORATORY` DATA ohne
	direkten Hypothesentest, SNN-Lauf oder EVID-Promotion.
- Neue Audits gehen mit einem strukturierten Review Request direkt in die
	Human Review Inbox; AI-Interpretation wird für diesen Audittyp übersprungen.
- Gateway-Plastic benötigt weiterhin eine eigene eingefrorene Registrierung,
	passende unabhängige Seeds und separate Ausführungsautorisierung.

## 2026-09-29 Ausführbarkeitsgrenzen im Playground

- Sichtbare Bausteine werden nicht mehr implizit als ausführbar behandelt.
- Katalog-, Analyse- und Referenzbausteine sind im Popup als nicht direkt
	ausführbar gekennzeichnet.
- Experimentelle Topologien zeigen ihre Mindestdimension und sind bei
	inkompatibler Dimension in der Builder-Auswahl deaktiviert.

## 2026-10-01 Experimentdetail und Artefaktübersicht

- Die Experimentdetailfläche bündelt verfügbare Laufartefakte und öffnet sie
	über den zentralen File Viewer.
- Human Review, Git-Commit und Provenienz-Digests werden separat angezeigt;
	fehlende Angaben bleiben unbekannt und erzeugen keinen Evidenzstatus.

## 2026-09-27 Alpha.7 release line

- `develop` remains the canonical integration branch; `main` remains release-only.
- The former standalone `playground` branch is no longer part of the intended
  long-lived branch topology once its content is verified as contained in
  `develop`.
- Stage 0 scientific maturity is 92.5%; Stage 1 is 85%. Scoped project EVID is
  registered as `EVID-2026-18`, `EVID-2026-19` and `EVID-2026-20`.
- The next Stage-1 maturity increment depends on the bounded Brian2 R2
  cross-implementation replication path; full replication credit remains
  reserved for genuinely external independent replication.
- Playground CUDA work remains on the engineering ladder: generated/assembled/
  loaded preflight and parity contracts precede any claim of an executed,
  equivalent GPU SNN backend.
- Release/DOI mechanics remain separate from Human Review, EVID and replication.

## 2026-10-04 Alpha.7 release integration

- Integration PR #269 merged to `main` at `4a6eb988`; it adds the publication
	synthesis and Stage-3 benchmark diagnostics without promoting scientific
	status.
- Release PR #270 merged at source freeze `8a0bb095`; post-merge CI run
	`37210840569` passed completely. Tag and GitHub pre-release
	`v0.6.0-alpha.7` point to that exact commit.
- Zenodo record `23138847` is publicly verified at DOI
	`10.5281/zenodo.23138847`; concept DOI `10.5281/zenodo.22860682` is stable.
	Hugging Face sync also succeeded on the release commit.
- OSF/ORCID are linked routes without a configured automatic release-update
	workflow. No institution-specific update endpoint is registered.
- Release and DOI publication leave Human Review, EVID, maturity and independent
	replication state unchanged.

## 2026-09-29 Post-hoc Experimentauswertung

- Experimentkarten im Wissenschaftsbereich erlauben die nachträgliche
	Beantwortung und Auswertung registrierter Hypothesen.
- Die Erfassung dokumentiert Begründung, Beobachtungen, Limitationen und
	nächste Schritte statt nur einen technischen Ausführungsstatus.
- Markdown- und JSON-Artefakte werden pro Experiment abgelegt, im Manifest
	verknüpft und über den zentralen File Viewer geöffnet.
- Interpretation, Human Review und EVID bleiben als getrennte nachgelagerte
	Schritte erhalten; Speichern erzeugt keine automatische Evidenz.

## 2026-09-27 Bausteine-Katalog und Sprachumschaltung

- Der Playground-Bausteine-Tab erklärt jeden Katalogeintrag per Hover und
	ausführlichem Info-Popup.
- Repo- und Playground-Bausteine werden gemeinsam mit den ausführbaren
	Modellen, Topologien, Stimuli, Analysen und Robustheitskontrollen gezeigt.
- Der globale Sprachselector schaltet Kategorietitel, Beschreibungen,
	Quellenlabel und Explorationsgrenze zwischen Deutsch und Englisch um.
- Neue Backend-Einträge fallen auf eine fachliche, sprachabhängige Beschreibung
	zurück, statt ohne Erklärung im Katalog zu erscheinen.

## 2026-09-27 Live-Detailansichten

- Vergrößerte Live-Grafiken werden hochauflösend und ohne einmaliges Bitmap-
	Hochskalieren gerendert.
- Die aktive Detailansicht folgt jedem Live-Step und zeigt ihren Laufstatus.
- Session-Aktionen sind auch im Zoomfenster direkt erreichbar.
- Aktualisierungsfaktoren `1x`, `5x`, `10x`, `25x`, `50x` und `100x` bündeln
	Simulationstakte ohne parallele Requests.
- Wiederholte Topologie-Payloads werden bei Live-Batches reduziert; die
	Darstellung bleibt aus dem letzten gültigen Graphen lesbar.

## 2026-09-27 Release-Statusmarker

- Die Release-Ansichten für Entwicklung und Wissenschaft zeigen neben den
	Statusbezeichnungen die etablierten Häkchenmarker für erledigt, teilweise
	erledigt und offen.
- Die kanonischen Statusbezeichnungen `met`, `partial` und `open` bleiben
	unverändert und werden nicht als wissenschaftliche Evidenz umgedeutet.
- Wissenschaftliche Kriterienkarten verwenden ein einheitliches Raster;
	Research-/Docs-Dateiverweise öffnen den zentralen File Viewer als Popup.
- Claims, EVID, Experimente und Hypothesen sind je Timeline-Stufe über einen
	eigenen Registerbereich direkt erreichbar.
- Lange Stufennamen wie `Bewusstseinsforschung` umbrechen innerhalb der
	Timeline-Karten ohne horizontales Überlaufen.
- Playground-Defaults für Topologie, Erregbarkeit und Verhalten sind auf den
	aktualisierten Referenzstand gesetzt: `weight=4`, Lernrate/Epsilon `0.2`.
- Die Playground-Oberfläche verwendet ein ruhigeres Laborraster mit klarer
	Kartenhierarchie, kompakten Feldern und responsiver Darstellung.
- Der Builder bietet integrierte Izhikevich- und PAN-Presets sowie lokal
	speicherbare eigene Konfigurationen.
- Der Presetkatalog A–G ist in `docs/playground/PRESETS.md` dokumentiert und
	über den Closed-Loop-Selector im Builder verfügbar.
- Live-PAN-Sessions besitzen ein interaktives Monitor-Popup mit Start/Pause,
	Metriken, Spike-Verlauf, Parameteransicht und Stick-Figure-Canvas.
- Der Sandbox-Loop besitzt optionalen Posture-Score, gestaffelte Reward-Events,
	separate Score-/Event-Kanäle, Reibung, Weltgrenzen und Episoden-Reset.
- Temporäre PAN-Live-Sessions können über den Builder gesammelt gelöscht
	werden, wenn das Session-Limit erreicht ist.
- Der Release-Workspace besitzt einen eigenen Tab für die wissenschaftliche
	Gesamtarbeit mit allen elf Manuskriptteilen.
- Jeder Teil zeigt den redaktionellen Arbeitsstand als Prozentwert mit
	`met`, `partial` oder `open`; diese Werte sind keine EVID-Metrik.
- Der Gesamtarbeits-Tab folgt strukturell der Scientific-Maturity-Ansicht mit
	Kicker, Gesamtprozentzahl, Einleitung, Statuslegende und Kontextboxen.
- `INDEPENDENT_REPLICATION.md` ist aus der wissenschaftlichen Timeline wieder
	als geschützte Root-Datei im File-Viewer öffnbar.

## 2026-09-26 External Review Deployment

- Review-Fragebogen kann statisch über GitHub Pages oder als isolierter
	Hugging-Face-Docker-Space bereitgestellt werden.
- Online-Antworten bleiben außerhalb des Git-Repositories verschlüsselt.
- Nur geprüfte, nicht-identifizierende Aggregate dürfen später veröffentlicht
	werden.
- GitHub Pages export-only was provisioned at
	<https://thomas-heisig.github.io/MHRN/>; GitHub reports HTTPS enforced.
- Live smoke on 2026-10-04 found the page HTML but 404s for its CSS/JS because
	canonical `main` still uses absolute `/review/...` paths. A relative-path fix
	is present on `develop` (`6c417c2`), but that branch is nine commits ahead
	with unrelated changes and has no open PR. Keep the fix behind the normal
	release review before republishing.
- Online collection remains disabled. No private study configuration,
	persistent response store, backup/restore evidence or study-specific
	privacy/ethics disposition is configured; GitHub Pages is not a collector.

## 2026-09-20 Publikationsnavigation

- „Einfach erklärt“ steht als Einstieg vorne, bevor der eigentliche
	Publikationsreader geöffnet wird.
- Manuskript, Open Science und rechtliche Informationen bleiben als getrennte
	Publikationstabs erhalten.

## 2026-09-20 Publikation und Open Science

- Open Science ist jetzt ein eigener gleichrangiger Tab innerhalb der
	Publikationsansicht.
- Die Hauptpublikation bleibt als fokussierter Reader von Portal- und
	Netzwerkmetadaten getrennt.

## 2026-09-20 Hugging Face identity

- Current Hugging Face publication namespace: `ThomasHeisig`.
- GitHub Actions uses the repository secrets `HF_USERNAME` and `HF_TOKEN`;
	the token value is never stored in the repository.
- The 2026-10-04 rolling mirror sync completed successfully in [GitHub Actions run 37201795384](https://github.com/Thomas-Heisig/MHRN/actions/runs/37201795384) for canonical `main` SHA `963d68d523b38096619e41743c8c4b5b2ac1d42c`. The research-data mirror manifest reports this SHA; the workflow publication step succeeded for all three targets.

## 2026-09-20 Experimentstatus in der Übersicht

- Die Forschungsfragenübersicht zeigt technische Laufzähler und kompakte
	Häkchenstatus aus dem Registry-/Manifest-Katalog.
- Einzel-Experimente zeigen abgeschlossen, fehlgeschlagen, laufend oder noch
	nicht ausgeführt direkt in der Liste.
- Statusmarker bleiben von DATA, Human Review und EVID getrennt.
- Karten öffnen eine Detailansicht mit strukturierten Metadaten, vollständigem
	Manifest und „In Ausführung übernehmen“.

## 2026-09-19 Public Alpha.5 release candidate

- Alpha.5 is a **technical pre-release candidate**, not scientific completion.
- Publication to `main` is allowed only through an explicit `release/*` branch after full CI, Repository Health/Clean Tree, and applicable scientific/publication/DATA-integrity gates are green.
- The Release preview separates **Entwicklung**, **Wissenschaft** and **Veröffentlichung**.
- Public provider identity/contact data are documented; a self-hosted public dashboard remains deployment-privacy-pending until the actual hosting/proxy/logging stack is known.
- Edition 1.8 states explicitly that AI-assisted research is both disclosed tooling and a **methodological research object**; AI remains neither author nor evidence authority.
- Independent external replication is an explicit post-publication objective. The original author does not self-certify novelty or scientific value.
- Zenodo/DOI status remains external and version-specific. The published
	Alpha.6 software archive is verified at
	[Zenodo record 22860683](https://zenodo.org/records/22860683), version DOI
	`10.5281/zenodo.22860683`, concept DOI `10.5281/zenodo.22860682`.
- Alpha.7 has not yet been archived; the Recursive Epistemics 1.8 publication
	package is separate and its DOI remains pending.


## 2026-09-19 Public ORCID authorship linking

- Canonical project, citation and author metadata now link Thomas Heisig to
	ORCID `0009-0002-9589-1872`.
- Runtime profile identity remains separate from public authorship identity.
- Private ORCID contact data is not stored in the repository.
- Zenodo release metadata links the GitHub source and the same ORCID. The
	Alpha.6 record is now externally verified; later versions require their own
	published record and DOI reconciliation.
- The public OSF project resource is linked as a research/provenance location.

## 2026-09-20 Seed DATA provenance

- Added the canonical [Seed DATA contract](../../research/specifications/SEED_DATA_CONTRACT.md)
	for construction, usage, stored fields, paired comparisons and replication
	limits.
- Scientific Integrity and document-governance gates now require this contract.

## 2026-09-18 Human-review queue and inbox integrity

- The review inbox now distinguishes real human decisions from AI-authored
	review artifacts and detects DATA-only result artifacts such as CL-003.
- The current open queue contains `EXP-GEN-0041`,
	`EXP-S1-TOPO-V3-R1-20260918` and `EXP-S6-SEM-CL-003`.
- CL-003 has a bounded human-review candidate; no human decision or automatic
	DATA-to-EVID promotion is created by the repository.

## 2026-09-19 Experiment- und Reihenarchiv

- Einzelne Experimente lassen sich idempotent archivieren; bereits verborgene
	Einträge erzeugen keinen Fehlalarm mehr.
- Experimentreihen können inklusive ihrer Kindexperimente metadata-only
	archiviert und gemeinsam wiederhergestellt werden.
- Die kanonischen Experiment- und Workflow-Artefakte werden dabei nicht
	verschoben oder verändert.
- Reihen mit bereits archivierten Kindern werden als `partial` im Archiv
	geführt und nicht mehr fälschlich in der aktiven Reihenliste angezeigt.
- Das Archiv ist im Frontend standardmäßig geschlossen und durchsucht Reihen
	und Einzelexperimente über eine gemeinsame Suchfunktion.

## 2026-09-16 Release navigation separation

- Registered Wissenschaft as a first-class Release route next to Entwicklung.
- The scientific maturity timeline now opens through the central workspace
	router instead of relying only on a late-injected special button.
- Entwicklung and Wissenschaft render as separate Release views.

## 2026-09-16 Gateway experiment report boundary

- Documented Frozen, Random, Shuffle and Plastic directly in the dashboard's
	Gateway Experiment surface, including the fail-closed Plastic prerequisites.
- Gateway activations can now write a JSON state artifact and a Markdown
	report under the experiment directory; the generated manifest remains
	explicitly non-evidentiary and requires Human Review.
- Productive Gateway activation and scientific EVID promotion remain locked.


## 2026-09-16 Experiment archive results viewer

- Extended the "Experimentreihen & Archiv" panel so every past experiment —
  active or archived — shows result-viewing buttons (Report, Summary,
  Statistics, Raw Data) built from its `manifest.artifacts` paths.
- Previously only just-finished runs exposed result buttons; past experiments
  could only be archived/restored. Now any experiment with a manifest can be
  inspected directly from the library.
- The file viewer header gains Report/Summary/Statistics/Raw Index switch
  buttons for past experiments, matching the popup already available for
  completed runs.

## 2026-09-13 Stage 2 closure and Stage 3 plastic neural tissue

- Closed Stage 2 at the scoped engineering boundary after the merged recurrent
  reference contract proved sustained bounded activity, deterministic replay,
  long-run execution and restart/restore continuity. The declared 1,000-10,000
  neuron scale remains a separate performance benchmark, not a completion
  blocker for recurrence mechanics.
- Added the Stage-3 plastic-neural-tissue contract and deterministic reference
  runner covering STDP, signed eligibility, delayed reward/three-factor
  plasticity, homeostasis, structural plasticity and checkpointed adaptive
  state.
- Added matched `learning_on`, `learning_off` and `sham_replay` controls plus a
  deterministic replay identity check. The reference is engineering
  verification only and cannot create or promote scientific EVID.
- Advanced the development version to `mhrn-core 0.6.0a2`.
- R2 productive-learning evidence closure, held-out independent runs and
  target-scale plastic-network benchmarks remain open research work.

## 2026-09-13 Stage 6/7 reconciliation and Stages 8-10 frontier foundation

- Stage 6 now reflects bounded working/episodic memory, the observation-only `TransitionWorldModel`, ExperienceEngine composition and the registered exploratory 2026-09-10 cognition campaign. Delayed-information and one-step prediction controls were executed; semantic memory, canonical coupled-state checkpointing and SNN-level confirmatory evidence remain open.
- Stage 7 now reflects versioned technical Wesen identity, digest/revision/lineage, snapshot binding and the persistent operational Behavior Profile. These are foundations only: causal self/other attribution and a genuine operational self-model remain unimplemented.
- Stages 8-10 now reference their merged research foundation, experiment backlog, literature provenance and frontend placeholder contract. Their maturity intentionally remains `planned`/0 %; planning material is not implementation or EVID.
- The development version remains `mhrn-core 0.6.0a2`; historical experiment manifests retain the version recorded when they actually ran.

## 2026-09-12 Scientific metrics workbench

- Added a live `/api/science/metrics` contract derived from the retained
	telemetry window and real network topology; unavailable analyses remain
	null/`UNKNOWN` rather than being inferred from operational zeros.
- Added a Research scientific instrument covering spike trains, topology and
	5D geometry, criticality, learning, homeostasis/energy, replication
	statistics, provenance, falsification notes and comparison capture.
- Reorganized the instrument into twelve navigable analysis layers while
	preserving the existing Experiment Runner, Files and Registry surfaces.
- Wired the Research Observatory directly from `app.js` and added an asset
	version marker to make the new frontend deterministic after reload.
- Added bounded operator links to network drill-down and runtime input/output
	controls. Local annotations are explicitly not scientific evidence until
	exported with an experiment record.

## 2026-09-12 Parameter sidebar route

- Linked sidebar menu 07 to the runtime Parameter Inspector and retained its
	active state after opening the Settings workspace.

## 2026-09-12 Research workspace tabs

- Grouped the Research workspace into Experiments, Files and Registry tabs.
- Kept the experiment runner and quick-access lanes together, isolated the file
	manager, and mounted the dynamic research registry in its own panel.
- Added browser coverage for switching between all three Research sub-tabs.

## 2026-09-11 Full backend API integration into frontend

- Completed a repo-wide API audit identifying 25 backend endpoints not yet
	consumed by the frontend.
- Created 7 new ES-module panels (cognition, gateway-monitor, docs-browser,
	research-docs, ai-report-tools, learning-prep, structural-inspector,
	system-info) that integrate all 25 endpoints with auto-refresh and
	resilient parallel fetching via `Promise.allSettled`.
- Added shared CSS layout rules in `shell.css` and wired all modules into
	`index.js` `init()`.

## 2026-09-11 Frontend shell accessibility

- Corrected the fixed visual shell's content clearance: the active workspace
	now starts below the measured topbar and primary navigation, while dynamic
	footer height is reserved for scrolling on desktop and mobile.
- Added a Playwright regression covering both top chrome clearance and footer
	clearance at the end of the document.

## 2026-09-10 Bounded memory, prediction and behavior profile foundation

- Updated the Release workspace's canonical current-release projection to the
	2026-09-10 state: engineering foundation complete, zero active
	release-blocking implementation items, and explicit snapshot/control and
	final source-freeze follow-ups.
- Implemented an optional `ExperienceEngine` data path for bounded
	working/episodic memory and later prediction comparisons.
- Added independent read/write controls, capacity and retention limits,
	duplicate suppression, atomic persistence, schema ownership and integrity
	checks. Memory eviction does not delete research artifacts.
- Added a one-step observation-only transition predictor with an explicit
	persistence reference, target-state leakage boundary and error/uncertainty
	records. It is not yet used for action selection.
- Added an operational behavior profile with separate initial, situational and
	slow disposition state. It affects behavior only through an explicit tuple of
	decoder candidates and logs bounded simulation-tick updates.
- Wired configured Behavior Profiles into `build_experience_subsystem()` and
	the existing `ExperienceEngine`; no LLM personality or psychological claim
	is introduced.
- Focused engineering screen: 18 tests passed for memory, profile, experience
	and existing profile lifecycle paths. No scientific promotion was performed.
- Added granular cognition telemetry and explicit read/write controls at
	`/api/cognition/*`; the Wesen page now shows memory, prediction and
	operational Behavior Profile state.
- Added individual sensor lifecycle controls with fail-closed adapter,
	authorization and safety checks; discovery never activates hardware.
- Added experiment-only Gateway lifecycle controls in Wesen while productive
	Gateway activation remains locked.
- Added explicit profile snapshot binding and central File Viewer access, plus
	the machine-readable backend/frontend coverage contract.
- Executed exploratory component controls include delayed-cue memory read/write/time-shuffle conditions and adaptive/frozen/persistence/no-model one-step prediction conditions. These are DATA-level screens, not SNN-level cognition evidence.
- Open: coupled runtime snapshot/checkpoint boundary, full-state pause/resume identity, explicit File Viewer raw-run drill-down, semantic memory, SNN-level held-out confirmatory studies, human review and independent replication.

## 2026-09-08 Versioned embedding and cluster analysis

- t-SNE, UMAP and K-Means cluster export now run through a bounded, provenance-bound backend job.
- The Research Workspace exposes method, seed, point and cluster controls plus persisted job history.
- Outputs remain technical analyses and require human review; they are not automatic scientific evidence.

## 2026-09-08 Research experiment organizer

- Research now exposes experiment-series launch, active experiment inventory, immutable archive and restore controls in the existing dashboard workflow.
- Archive operations now use a non-destructive metadata-only work-view index; canonical experiment paths and scientific artifacts remain unchanged.

## 2026-09-08 v0.6.0a1 development line opened

- Opened the v0.6 Scaling & Deterministic Performance line after the reviewed v0.5.0-alpha.7 gate closure.
- Kept the v0.6 milestone explicitly open: version movement is release engineering, not evidence of completed scaling or scientific validation.
- The active v0.6 criteria remain the source of truth for future compatibility, benchmark, storage, resume and migration work.

## 2026-09-09 v0.6 engineering foundation review

- Verified the v0.6 compatibility contract for runtime state, restart-capable snapshots, resumable runs and frozen B5D/journal formats.
- Verified reproducible scaling measurements with explicit memory, tick-cost, runtime-phase and pacing budgets.
- Verified bounded telemetry/storage compaction, immutable raw-run indexes and deterministic detail extraction.
- Verified deterministic pause/resume/restart identity and byte-identical migration/rollback behavior.
- The focused acceptance suite passes: 10 tests passed across persistence, benchmarks, runtime identity, pacing, research-data compaction and workspace contracts.
- The only v0.6 release item still open is publication of the immutable release record after the exact source-freeze CI and release-readiness snapshot are green. This is a gate/publication step, not missing implementation.
- Open research operationalization remains tracked in R0-R12 and the linked specialist TODOs; the engineering foundation does not constitute scientific evidence.

## 2026-09-09 Repository-derived development timeline

- Added the Release **Entwicklungs-Timeline** as a new routed tab and added its development bar to the chronological release timeline.
- Added `GET /api/release/development-timeline` with eleven explicit stages, structured criteria, continuous technical/scientific markers, score separation and confidence.
- Classified stages from module/test paths, registry objects, verification artifacts, test-baseline state and real runtime or snapshot sizes; roadmap prose remains context-only.
- Kept the consciousness frontier operational and non-assertive: stage 10 can display research criteria only and never produces a consciousness claim.
- Added detail panels, responsive browser coverage and backend/API tests for planned-feature handling, runtime fallback and engineering/evidence separation.

## 2026-09-09 Trusted-LAN dashboard access

- Windows `start.cmd` and `start.ps1` now bind the integrated dashboard to `0.0.0.0:8767` by default so it is reachable through the host machine's LAN IP.
- Direct Python startup remains loopback-only by default; explicit host overrides remain available for local-only or explicitly selected bindings.
- Documented the Windows Firewall and trusted-network boundary; public exposure remains unsupported without an authentication layer.
- Improved startup diagnostics with the canonical version, configuration, runtime mode, bind/local/LAN URLs, process ID and UTF-8 console handling.

## 2026-09-09 Profile & Identitaet

- [x] Add schema-v1 holistic technical Wesen profiles and bounded registry metadata.
- [x] Add canonical digest, revision history, parent lineage and atomic writes.
- [x] Bind profiles to existing snapshots by digest without copying neural state into `profile.json`.
- [x] Add profile-only/state-bound load modes, clone, archive/delete guards and secure ZIP import/export.
- [x] Integrate senses, learning, morphology, actuators, gateway, memory, self-model, resources and safety declarations.
- [x] Add the Wesen Profile & Identitaet dashboard view and lifecycle actions.
- [x] Apply supported runtime pacing settings during profile-only load and bind optional profile identity into experiment manifests.
- [ ] Connect the canonical snapshot restore hook for Profile + State loading; it remains fail-closed with `runtime_applied: false`.
- [ ] Keep autonomous profile mutation locked until bounded domains, journal, rollback and experiment gates exist.

## 2026-09-08 Cross-platform source-freeze digest mismatch on Windows

- Scientific source-freeze digests now use canonical Git text content across LF/CRLF checkouts while preserving byte-exact binary files.
- Gate diagnostics expose real dirty and untracked relevant paths, source commits, digest values and the reproducible stale reason.
- Baseline and verification artifact generation use the same canonical per-file representation.

## 2026-09-08 Cross-platform gate and browser contract repair

- Publication manifests now remain byte-exact when a Windows checkout uses `core.autocrlf=true`; citation, TeX and checksum text is pinned to LF.
- File-rendering contracts use byte-exact fixtures, and unsafe POSIX absolute manifest paths are rejected consistently.
- The shared Markdown renderer normalizes CRLF input before building safe heading, prose and link nodes.
- Browser inventory fixtures override canonical sensor/actuator IDs, so the Wesen pipeline reports host-independent endpoint transitions.
- The focused browser regressions pass; the full 15-test Chromium suite is the release check for this surface.

## 2026-09-07 DOCX viewer surface alignment

- Flattened the DOCX preview into the existing file viewer surface instead of rendering a bright paper card inside the modal.
- Reused dashboard text, line and accent variables for DOCX headings, links and tables; images and lists now follow the same responsive width rules.

## 2026-09-07 BibTeX links and prose rendering

- Added safe DOI and publication URL links to both the shared BibTeX preview and the legacy structured BibTeX table.
- Aligned BibTeX link and table styling with the dashboard base CSS variables.
- Markdown and documentation line wrapping now forms flowing paragraphs instead of one paragraph per source line, while preserving structural blocks.

## 2026-09-07 Functional viewer restoration

- Restored viewer back navigation and exposed `window.openBrain5DFile(source, path)` plus the `brain5d:open-file` event for cross-module file opening.
- Added central read-only LLM analysis from the viewer through the existing Research Chat backend.
- Reconnected Mammoth DOCX rendering with sanitized HTML fallback and added bounded multicolor syntax rendering for Python, C++, JavaScript and related source files.
- Existing text edit mode remains optimistic-lock protected and is available wherever the preview contract marks a file editable.

## 2026-09-07 Viewer regression restoration

- Restored full-width Markdown layout in the shared file viewer.
- Kept workflow artifact actions, including Human Review, report, summary, statistics and raw-data access, bound to the research source regardless of the last selected file-manager source.

## 2026-09-07 Viewer path compatibility

- Normalized Windows backslashes at the browser and API preview boundaries so workflow artifacts such as `experiments\\EXP-SNN-001-R5\\summary.md` resolve to the canonical repository path.
- Added an HTTP regression test covering the encoded Windows-style path.

## 2026-09-07 Structured archive and JSON previews

- ZIP-compatible containers (`.zip`, `.epub`, `.whl`, `.jar`, `.cbz`) now expose a bounded member manifest without extracting or executing entries.
- Archive previews mark suspicious `..` or absolute member paths and reject archives above the member-count or uncompressed-size budget.
- JSON previews now provide an expandable, bounded tree while retaining the original content for copy/edit operations.
- Remaining viewer gaps are media metadata, PDF text extraction, older binary Office formats, and local Graphviz/PlantUML conversion.

## 2026-09-07 File Viewer format and rendering pass

- Unified Markdown rendering now preserves fenced-language classes, renders Mermaid diagrams lazily in strict mode, and routes relative document links through the canonical viewer.
- Markdown and notebook cells expose a formula-aware surface for MathJax, including bounded notebook PNG/JPEG outputs.
- `.tex`/`.latex` files are classified as formula sources; `.mmd`/`.mermaid` as Mermaid diagrams; `.dot`/`.gv` and `.puml`/`.plantuml` as safe source previews.
- BibTeX previews now show the structured table without appending a duplicate raw source block.
- Graphviz and PlantUML source-to-SVG conversion remains intentionally open because the viewer has no local converter and remote rendering would disclose research content.

## 2026-09-07 GitHub/Hugging Face mirror synchronization

- Refreshed the current baseline in the project, documentation and Hugging Face READMEs.
- Kept GitHub `main` as the canonical source and documented the Hugging Face mirror as a derived publication target.
- Updated the optional mirror workflow to publish a fresh one-commit source snapshot with Git LFS objects, avoiding rejected binary blobs from inherited history.

## 2026-09-07 Hugging Face Space

- Prepared the Docker entrypoint for the integrated dashboard on `0.0.0.0:8767`.
- Added Docker Space metadata and published the live dashboard as `superdigger/MHRN-Space`.
- Added the Space repository to the automatic GitHub-to-Hugging-Face synchronization workflow.

## 2026-09-07 Space API rate-limit handling

- Added a shared JSON response parser that reports HTML/429 proxy responses as API errors.
- Reduced dashboard polling frequency automatically on `*.hf.space` deployments.

## 2026-09-07 Full-stack dashboard E2E verification

- Added an executable Chromium Playwright suite for batch selection, per-protocol Seeds/Ticks editing, aggregate workflow output and Footer progress.
- Covered workspace routing, responsive shell overflow and box-state minimize/maximize behavior at 1440, 1024 and 390 pixel viewports.
- Made the registered per-protocol batch Seeds/Ticks inputs editable so the tested workflow contract is available to operators.
- Verified `npm run test:e2e`: 5 passed and `python -m pytest tests -q`: 825 passed, 5 skipped.

## 2026-09-07 Release timeline restoration

- Restored a documentation-backed Product Timeline in the Release workspace.
- The dashboard merges dated milestones from TODO, ROADMAP and CHANGELOG and keeps source provenance visible.
- Checklist completion remains derived from the source Markdown rather than copied into frontend code.
- The Release workspace now separates completed history, current Alpha.7 work and planned backlog into three timeline lanes.
- Release navigation now separates Gate, version history, current preview, chronological Timeline, and the three canonical project documents.
- Historical Git tags extend the visible release range from 0.1.0 through the current development node.
- Release document actions delegate to the existing File Viewer so Markdown, text, JSON and other supported formats keep one rendering path.

## 2026-09-07 Full-stack runtime phase profiling

- Added canonical RuntimeTelemetry phase slots for learning, homeostasis, structural, embodiment, Neural Symbiosis/MSBA, dashboard telemetry and storage.
- Added an external phase-recording API for runtime hooks and exposed active/total phase coverage in the Runtime dashboard panel.
- Inactive subsystem phases remain explicit `0.0` DATA rather than inferred measurements.

## 2026-09-07 Neuron/synapse scaling profile

- Extended `scripts/benchmark_ladder.py` with explicit connections-per-neuron, actual synapse counts and synapse throughput.
- Generated a bounded 100/500/1000-neuron profile with two connections per neuron; the artifact remains a performance measurement, not scientific evidence.

## 2026-09-07 RQ-SNN-001 clean-freeze rerun and AIRR retry

- Executed the exact frozen `sustained_activity_stability_v1` protocol as `EXP-SNN-001-R5` from a clean worktree: 20 runs, 10 seeds, 100,000 ticks per run, zero runtime errors and `dirty=false` provenance.
- Corrected semantic classification so the dedicated RQ-SNN-001 protocol is `DIRECT_MATCH`; Human Review and EVID promotion remain open.
- Attempted append-only AIRR retries for `EXP-GEN-0033`; local Ollama runs produced fallback/timeout or schema-invalid role outputs, so AIRR-2026-0003 remains review-pending and non-evidence.

## 2026-09-07 Pacing-only determinism proof

- Added a deterministic controller batch comparison proving target-Hz configuration does not alter ticks, spikes or state digest when simulated inputs and `dt` are identical.
- The proof uses synchronous bounded batches, isolating pacing configuration from simulation semantics.

## 2026-09-07 Runtime pacing benchmark

- Added `scripts/runtime_pacing_benchmark.py` for bounded low-rate, targeted and unlimited RuntimeController measurements.
- Benchmark artifacts record target/achieved Hz, realtime ratio, `dt`, tick cost, phase profile and simulation tick without making a scientific performance claim.

## 2026-09-07 Hard protection and ordering gates

- Added fail-closed thermal-safety, fan-failure and persistence-failure trips that force `SURVIVAL` and block learned gateway allocation regardless of utility.
- Locked the protection order to reduce plasticity first, freeze it at criticality, and preserve thermal sensing, persistence and storage integrity.

## 2026-09-07 Separate energy contribution accounting

- Added component-level normalized energy accounting for sensor, encoder, spikes, synaptic events, plasticity, structural events, memory, I/O and adapter contributions.
- Preserved the aggregate estimate while exposing the component breakdown as DATA.

## 2026-09-07 Energy provenance classes

- Added explicit provenance classes for normalized model units, calibrated joule conversions, direct telemetry measurements and unavailable values.
- Preserved measured and estimated joules as separate fields with an explicit non-equivalence flag.

## 2026-09-07 Preregistered increased-dimensional projection controls

- Added `PROTO-MSBA-PROJECTION-001` with structured 5D baseline and external 8D/16D projection controls.
- Required explicit projection mapping and prohibited productive-core dimension migration in the protocol contract.

## 2026-09-07 Dimension-shuffled 5D control

- Added a deterministic `5d_shuffled` control arm that preserves dimensions, graph topology, seed and tick contract while permuting the three-node coordinate embedding.
- Exposed control classification in run metrics without treating the shuffled embedding as productive N-D core support.

## 2026-09-07 Epistemic layer separation in workflows

- Added a shared machine-readable `epistemic_layers` contract to workflow JSON, manifests and API results.
- Reports now separate UI state, DATA, EVID and post-hoc interpretation; EVID remains explicitly uncreated until its gates pass.

## 2026-09-07 Embodiment treatment provenance

- Added deterministic `DATA_ONLY` provenance records binding adapter identity, projection mode/dimensions, gateway configuration and normalized energy coefficients.
- Provenance records require preregistration and human review and cannot promote themselves to EVID.

## 2026-09-07 Digital payload checksum persistence

- Added JSON provenance persistence for digital `SymbolFrame` payloads with SHA-256 checksum, payload size, codec, sequence and source provenance.
- Declared checksum persistence in the MSBA scientific boundary without copying the raw payload into the provenance record.

## 2026-09-07 Dynamic embodiment connection coverage

- Added API transition coverage for a sensor changing from available/active to unavailable/inactive.
- Added frontend contract coverage that clears stale organ details when a selected connection disappears; real browser E2E remains open because Chromium is unavailable in this environment.

## 2026-09-07 Experiment-only host telemetry observations

- Added an opt-in provider to the regulation runner so host telemetry is recorded only as an explicit `host_telemetry` experiment condition, with raw readings, typed signals and missing-value semantics preserved.

## 2026-09-07 Missing and uncertain sensor conditions

- Classified malformed numeric/boolean sensor values as `unknown` and propagated uncertainty through thermal and continuity drives without treating raw presence as valid telemetry.

## 2026-09-07 Peripheral adapter mutation boundary coverage

- Added a negative catalog test proving a peripheral adapter is not executed during registration or publication and cannot silently change canonical core or research state through that boundary.

## 2026-09-07 Real-body platform failure-path coverage

- Added Windows-compatible regression coverage for absent optional `psutil` sensors and unavailable `os.getloadavg`, preserving explicit unknown values without fabricated readings.

## 2026-09-07 Live telemetry propagation coverage

- Added HTTP integration coverage for unavailable telemetry (`503`) and stale frame metadata flowing from `TelemetryFrameStore` through `OperatorBridge` and the live projection API.

## 2026-09-07 Operator bridge control-boundary coverage

- Added regression coverage proving unknown structural proposals do not create decisions or history records and unknown runtime commands return explicit errors.

## 2026-09-07 Dashboard batch error-path coverage

- Added an HTTP regression test proving invalid batch protocols return a structured `400` JSON response.

## 2026-09-07 Evidence-engine edge coverage

- Added regression coverage proving dirty source trees and mismatched source-freeze digests cannot produce validated EVID promotion, even with a human review artifact.

## 2026-09-07 Regulation recovery experiment executed

- Executed frozen `closed_loop_regulation_v1` / `PREREG-REG-002` as `EXP-REG-0002-R1`.
- Completed 40 runs across 20 seeds and regulation-off/on arms at 128 ticks with zero runtime errors.
- Regulation-on reduced pressure-phase spikes from 15 to 5 and increased recovery-phase spikes from 21 to 25; recovery-ratio means were 5.0 versus 1.4.
- Results remain review-pending because source provenance is dirty and human review is required.

## 2026-09-07 Recurrence/propagation validation executed

- Executed frozen `recurrence_map_v1` / `PREREG-REC-001` as `EXP-REC-0001-R1`.
- Completed 300 runs across 20 seeds, five recurrent weights including the zero control, and three delays at 256 ticks.
- Observed immediate decay, transient recurrence and persistent-to-window classes without runtime errors; human review and EVID promotion remain open.
- Added regression coverage for the registered grid and its persistence classifications.

## 2026-09-07 Dashboard batch HTTP contract coverage

- Added HTTP coverage for the experiment workflow catalog route and batch POST route.
- The route contract now verifies structured workflow responses independently of browser automation.
- Batch service tests cover sequential order, per-protocol parameters and partial failure isolation.

## 2026-09-07 Batch service contract coverage

- Added automated coverage for sequential protocol order, per-protocol Seeds/Ticks and child failure isolation.
- Aggregate JSON/Markdown workflow reports are covered independently of browser availability.
- Browser-level interaction coverage remains a separate environment-dependent gate.

## 2026-09-07 Current-head verification and protocol contracts

- Fixed the stale frontend ExperimentMode lifecycle contract.
- Updated the operational protocol contract test for the new frozen `RQ-SNN-001` stability protocol.
- Current head verification: 796 passed, 5 skipped, 0 failed.

## 2026-09-07 Batch route verification

- Added an HTTP contract test for the workflow catalog and batch POST routes.
- Current head verifies structured batch responses independently of browser availability.

## 2026-09-07 Dissertation results synchronization

- Added the verified MHRN experiment results to `KI_Die_geliehene_Intelligenz_Kontrollverlust_Embodiment_Dissertationsbasis.docx`.
- The DOCX now distinguishes technical completion, exploratory/replication status, dirty-tree provenance and pending human review.
- A repeatable updater is retained at `scripts/update_dissertation_results.py`.

## 2026-09-07 Failed experiment retries repaired

- `independent_replication_v1` failed because the valid preregistration mode `REPLICATION` was missing from the manifest governance enum; this is now supported.
- `learning_interference_screen_v1` failed because neuronal transient state was not reset between declared independent task episodes; the reset is now protocol-scoped and preserves learned weights.
- Retries completed successfully as `EXP-REPL-0001-R1` and `EXP-LIFE-0001-R1` with zero runtime errors.

## 2026-09-06 Registry-driven sequential workflow

- The Experiment-Workflow now plans all catalog entries by default and executes selected experiments sequentially.
- Operational protocols use their registered seed expressions and tick budgets automatically.
- Exploratory entries use bounded Runtime-Ticks diagnostic defaults; per-entry plan values are visible and read-only.

## 2026-09-06 Batch result visibility

- Batch start now shows immediate running state, persistent result text and explicit errors in the workflow dialog/output area.
- Successful batch dialogs close only after the aggregate workflow report has been rendered.
- Footer status now shows the batch as a live test run and preserves the completed workflow result.

## 2026-09-06 Exploratory experiment artifacts

- Exploratory Runtime-Ticks runs now write the same visible experiment artifacts as normal runs: manifest, report, `DATA/runs.json` and `summary.md`.
- Batch results include the child summary path and explicit `EXPLORATORY` / `test_run` markers.

## 2026-09-06 Batch execution options and exploratory start

- Batch execution now accepts per-protocol seed and tick settings from the dialog.
- Operational-only batches no longer require a runtime bridge; exploratory selections require it and use bounded runtime ticks.
- The dialog shows all 48 catalog questions, provides all/none selection, and no longer disables exploratory entries.

## 2026-09-06 Exploratory workflow execution

- Exploratory research questions can now be selected and executed through the batch workflow as explicit `runtime_ticks_v1` diagnostic runs.
- Questions without a registered hypothesis use the explicit `EXPLORATORY-UNSPECIFIED` marker; no evidence or confirmatory claim is implied.
- The batch endpoint now attaches exploratory selections to the runtime controller instead of rejecting them as unknown operational protocols.

## 2026-09-06 Experiment workflow selection repair

- The batch dialog now renders all Research Catalog questions, not only questions with an operational protocol.
- Questions without a frozen operational protocol remain visible as disabled `EXPLORATORY` entries rather than disappearing.
- Batch start errors and completion results are shown in the dialog/workflow output.

## 2026-09-06 Experiment workflow UI activation

- Activated the existing Experiment-Workflow button and dialog in the Research workspace.
- The `batch_workflow_v1` protocol selection now opens the same start/cancel options dialog.
- Selected registered protocols are submitted to `/api/experiment/workflow/batch`; the aggregate JSON/Markdown report is shown in the workflow result area.

## 2026-09-06 EXP-GEN-0033 replication

- Re-ran the complete science suite as `EXP-GEN-0033-R1` without modifying the original experiment.
- The replication completed 57 runs, 100,000 requested ticks, `SATISFIED` tick validation and zero runtime errors.
- Deterministic data, statistics and a transparent fallback AIRR report are archived for the replication.

## 2026-09-06 AIRR missing-artifact recovery

- Added a safe AIRR fallback for schema-invalid or unavailable AI role responses.
- Existing valid role analyses are reused; missing reviewer/writer roles become explicit `analysis_unavailable` records instead of deleting the deterministic data analysis.
- Repaired `EXP-GEN-0033` with a reviewable AIRR JSON/Markdown report while keeping scientific evidence disabled.

## 2026-09-06 RQ-SNN-001 operationalization and long-run result

- Added frozen operational protocol `sustained_activity_stability_v1` with 100,000 ticks, ten independent seeds, no-input control, tonic-drive treatment, burn-in, windowed traces, finite-state/topology gates and explicit thresholds.
- Final replication `EXP-SNN-001-R2` completed 20 runs with 0 runtime errors and 20/20 preregistered stability passes.
- The result is operational and reviewable, but not promoted to scientific EVID: the recorded source tree is dirty and mandatory human review remains pending.

## 2026-09-06 Live experiment footer status

- The Footer now receives the running workflow's real experiment ID, progress percentage and status label from `brain5d:experiment-progress`.
- Periodic dashboard refreshes no longer overwrite an active workflow with `inactive / no session`.

## 2026-09-06 Runtime & Wesen grid readability

- Runtime & Wesen now uses explicit grid areas for left state controls, the central body map, right inspection controls and the full-width Neural Symbiosis row.
- The Embodied Multi-Network Interface is no longer squeezed into a single leftover column.
- Symbiosis cards reflow from three to two to one column across desktop, tablet and mobile widths.

## 2026-09-06 Full-page tabs and responsive box states

- Active workspaces now use the full available page area beneath the fixed application chrome.
- Dashboard panels receive shared `minimized`, `standard` and `maximized` states with responsive controls and Escape-to-standard behavior.
- Dynamically created panels and containers without a native header receive the same presentation controls without changing runtime data contracts.

## 2026-09-06 Wissenschaft Network route restored

- The `Wissenschaft → Neuronales Netzwerk` context route now reveals the active Network workbench instead of being hidden by the retired-workspace CSS rule.
- Network view tabs are available again and continue to respect JavaScript-controlled `hidden` panels.

## 2026-09-06 Fixed application header and primary areas

- Header and the three primary areas `Dashboard`, `Wissenschaft` and `Runtime & Wesen` remain fixed together at the top of the viewport.
- The frontend architecture measures their actual wrapped heights and reserves the matching workspace offset for tablet and mobile layouts.
- Only the active workspace content scrolls; the fixed Footer remains independently reserved at the bottom.

## 2026-09-06 Fixed bottom Footer

- Footer is fixed to the bottom edge of the viewport across desktop, tablet and mobile layouts.
- Body and main reserve the responsive Footer height so the last workspace content remains reachable instead of being covered.
- Safe-area padding is applied for mobile browser insets.

## 2026-09-06 Footer status-bar consolidation

- Footer Runtime controls, tick, command feedback, I/O, experiment, mode and health now share one responsive semantic grid.
- Settings and Release actions are nested in the existing Health area instead of being injected as an extra grid row.
- Footer controls retain accessible click targets at desktop, tablet and mobile widths.

## 2026-09-06 Dashboard CSS consolidation pass II

- Removed the unscoped legacy white Topbar rule that overrode the coordinated shell theme.
- Reduced the Overview chrome to one workspace header, one status rail and the actual data surfaces.
- Replaced remaining fixed research/runtime workbench heights with viewport-aware guardrails and preserved local scrolling only where content requires it.
- Fixed the Embodiment renderer initialization order so unavailable connection lists no longer raise a runtime error.

## 2026-09-06 Canonical dashboard CSS and accessible views

- `src/dashboard/static/styles.css` is now the single CSS entry point and imports the component layers once; runtime stylesheet injection no longer duplicates the cascade.
- Shared tokens, fixed typography roles, surface types and green/orange/red status semantics now cover 4K, 1080p, tablet and mobile layouts.
- Tabs and `hidden` state are authoritative for dense workspaces; tables/logs retain local scrolling and dialogs use the available viewport as a full-size overlay.
- Contrast, reduced motion, larger controls and a persisted Reader view are available from the header; the Wesen morphology timeline is initialized before telemetry arrives.

## 2026-09-06 Footer 6/3 grid alignment

- Footer top row uses six equal columns for product, Runtime, I/O, experiment, mode and health.
- Footer bottom row uses three equal telemetry columns for activity, spikes and resource pressure.
- Symbols and Footer text share fixed compact sizing for consistent alignment.

## 2026-09-06 Compact Footer controls

- Footer symbols use compact 20px controls and reduced spacing.
- Footer labels, vital values and I/O text use a denser 1080p/100% scale while remaining readable.

## 2026-09-06 Fixed 1080p application shell

- Header and the primary menu band are fixed shell regions at the top of the viewport.
- `main` is the only vertically scrollable display area between the chrome regions.
- Footer remains visible at the bottom and does not shrink away at 1080p/100%.

## 2026-09-06 Responsive viewport and footer flow

- Removed the fixed active-tab viewport canvas that only fit a narrow 1080p/67% combination.
- Active workspaces now grow naturally and keep the complete Footer reachable at other resolutions and zoom levels.
- The Experience shell prevents horizontal overflow while preserving the full content area between Header and Footer.

## 2026-09-06 Frontend shell consolidation

- The visible frontend shell now has one navigation owner; legacy tab buttons remain internal routing targets only.
- Footer Runtime controls are static DOM elements with one controller and no dynamically appended duplicate panel.
- Legacy footer CSS and the MAX batch-yield note were removed; current shell styling lives in the Experience stylesheet.

## 2026-09-06 Header and footer shell stabilization

- Header sizing and responsive wrapping are centralized in the final Experience shell rules.
- Footer markup includes global Runtime controls and live I/O while remaining compatible with the flat legacy DOM.
- Footer and header no longer rely on fixed viewport positioning that can clip the document.

This roadmap separates **implemented engineering capability** from **scientific evidence still required**. A feature can be technically complete without its scientific hypothesis being confirmed.

## Current baseline

At the 2026-09-06 research-catalog integration point:

- **791 tests** are collected on current `main`;
- Research Catalog / variable-projection-dimension PR #21 is merged; merge commit `85e7209509b348bf7912dde01d3d9ebb078a2e61`;
- the latest fully completed pre-merge `main` CI baseline was #598 and successful;
- post-merge/current-head CI is the authoritative verification and must complete before the current head is described as fully green;
- Python 3.11/3.12/3.13, Black, Ruff, Pylint, Pre-Commit, Mypy, Pyright, security, Scientific Integrity, wheel and Docker remain mandatory gates;
- historical experiment DATA remains immutable evidence history.

Instrumentation repairs, registry repairs and new architecture produce new observations/experiments rather than rewriting prior DATA/EVID.

## Completed engineering foundation

Current development contains:

- sparse persisted 5D spiking core with delayed event propagation and deterministic RNG/state;
- STDP, signed eligibility and reward-modulated learning;
- homeostatic regulation;
- structural proposal/approval/mutation/journal/undo/recovery;
- `.b5d` storage, delta journaling and checkpoints;
- research registries, manifests, DATA/EVID separation and scientific integrity gates;
- bounded Language Organ / Research Assistant / Cognitive Advisor contracts;
- typed embodiment, actuator authorization, audit chain and deterministic environment loop;
- source-freeze binding across protocol code, configuration and DATA digests;
- productive-learning controls and train/validation/holdout partition enforcement;
- real host interoception and dynamic device discovery without fabricated fallback values;
- adaptive read-only `Wesen` workspace;
- protocol-driven Research Experiment Runner and Science Suite;
- network impulse response instrumentation for ticks, spikes, activated neurons, synaptic events, latency, recurrence and state digests;
- compressed immutable raw-run preservation plus bounded `runs.json` / `analysis/ai_packet.json` projections;
- Neural Symbiosis open-set peripheral network/virtual-area contracts at the embodiment boundary;
- MSBA modality-specific pathways, energy/resource accounting and fail-closed candidate allocation/plasticity;
- fragmentable canonical RQ/H registry with duplicate-ID rejection;
- canonical MSBA RQ/H integration into the normal Experiment Workflow;
- searchable Research Catalog UI that distinguishes operational from exploratory questions;
- repository-wide read-only RQ/H reference audit support;
- configurable MSBA/external projection dimensionality from 1 through 32 while preserving the productive 5D persistence contract.

## Roadmap principle

Development now prioritizes **evidence closure**, research-catalog completeness and controlled experiments over feature accumulation. Reachability in the UI is not evidence and an exploratory runtime run is not a substitute for a hypothesis-specific protocol.

---

## R0 — Research catalog closure and experiment operationalization

**Goal:** every canonical research question and hypothesis is discoverable, link-valid and explicitly classified by experiment readiness.

Implemented foundation:

1. load `questions.yaml` / `hypotheses.yaml` plus deterministic `questions.*.yaml` / `hypotheses.*.yaml` fragments;
2. fail closed on duplicate identifiers;
3. expose MSBA RQ/H entries through the existing Experiment Workflow;
4. provide searchable RQ/H selection instead of relying on a long pulldown;
5. allow exploratory runtime experiments for unmapped questions while preventing accidental EVID promotion;
6. provide a repository-wide reference audit so documentation/code references can be compared with the canonical registry.

Still required:

1. assign every still-unmapped canonical RQ/H a dedicated runner or an explicit `design_pending` state;
2. freeze controls, stopping rules, primary outcomes and preregistrations before confirmatory execution;
3. expose domain/status/evidence/progress facets through the workflow catalog API; ✅
4. publish the registry audit as a CI Markdown/JSON artifact and maintain an explicit, reasoned historical/test-fixture allow-list where appropriate;
5. regenerate only current generated catalog/matrix documents after registry changes, never experiment-owned historical reports. ✅

**Priority:** immediate.

---

## R1 — Post-repair propagation and recurrence validation

**Goal:** establish a clean multi-seed baseline for propagation and recurrent return using the repaired instrumentation.

Tasks:

- execute the registered recurrence/propagation protocol over independent seeds;
- persist complete spike, synapse, latency and digest metrics;
- compare recurrence-on/off using preregistered metrics;
- review before any EVID promotion;
- never rewrite `EXP-GEN-0009` to `EXP-GEN-0012`.

---

## R2 — Productive-learning evidence closure

**Goal:** demonstrate whether learning changes later behavior rather than merely internal weights.

Maintain frozen protocol/configuration, train/validation/holdout separation, pre/post behavior probes, learning-off and sham/replay controls, independent seeds and human-review-gated EVID promotion.

Audit 2026-10-04: the frozen `PREREG-GEN-001` requires at least 20 independent
seeds and disjoint partitions. Its current `run_generalization` runner reports
`validation_episodes_executed=0` and `holdout_episodes_executed=0`, so declared
partition counts and drive-perturbation probes do not yet satisfy executed
held-out evaluation. Existing `EXP-STDP-0002` is dirty/exploratory, uses three
seeds under `RQ-STDP-001`, and has no human review/request; it cannot close R2.
Do not execute the confirmatory campaign until the holdout stimulus/partition
semantics are operationalized without changing the frozen acceptance criteria.
Human evidence review remains a post-run gate.

---

## R3 — Closed-loop embodiment evidence

**Goal:** test Sensor → SNN → Actuator → Outcome → Reward as a controlled causal loop.

Required comparisons include replay/open-loop, sensor-loss, degraded-quality and actuator-no-effect conditions. Action acceptance and measured effect must remain separate receipts.

---

## R4 — Neural Symbiosis / MSBA experimental gateway program

**Goal:** test whether the SNN can learn to select, weight or compensate across peripheral neural/virtual areas without compromising the canonical core.

The first implementation stage is **experiment-only**. Production peripheral activation remains out of scope until controls are validated.

### Current implementation status — 2026-09-09

- [x] First-class bounded gateway runtime with `disabled` through `active_plastic`, `paused` and `error` lifecycle states;
- [x] Frozen, deterministic Random and deterministic Shuffle controls;
- [x] Experiment-only plasticity guard with frozen preregistration and explicit AI authority boundaries;
- [x] Persistable topology, RNG/checkpoint state, bounded structural journal and resource/throttling telemetry;
- [x] Read-only Neural Symbiosis/gateway status APIs and Wesen topology/status view;
- [x] Productive gateway capability remains `available: false` pending validation;
- [ ] Execute the new gateway RQ programme with independent seeds, statistical comparisons and human scientific review.

Required work:

1. add an experiment-runner adapter that constructs explicitly declared peripheral areas;
2. persist exact adapter/model/version/artifact hashes;
3. persist gateway state independently from core synapse state;
4. keep gateway plasticity disabled outside registered experiments;
5. support matched frozen-gateway, random-gateway, timing-shuffle and information/activity controls;
6. support reduced-, native- and increased-dimensional projection treatments with explicit mappings;
7. execute `RQ-MSBA-E01` through `RQ-MSBA-E05` only after their hypothesis-specific runners and preregistrations exist;
8. evaluate noisy-area suppression and sensor-lesion compensation;
9. compare alternative homeostatic reward/error formulations rather than assuming a signed population mean is valid;
10. require independent seeds and evidence review before claims of learned tool/area use.

---

## R5 — Variable dimensionality and versioned N-D core research

**Goal:** allow dimensionality to become an explicit experimental variable without breaking existing 5D evidence or persistence.

### Implemented safe layer

- MSBA/external projection spaces accept 1–32 dimensions;
- schemas can record projection dimension count separately from productive core dimensions;
- UI exposes the projection-dimension request and states the productive 5D limitation;
- historical 5D neuron IDs and `.b5d` snapshots remain unchanged.

### Required before productive core >5D

1. design and freeze a versioned N-D neuron-ID/storage representation;
2. define backward-compatible `.b5d` readers/migration and canonical state hashing;
3. generalize spatial indexing, coordinate packing, neighbor generation, distances, topology diagnostics and structural locality;
4. add combinatorial-growth/memory guards for high dimensions;
5. prove bit-for-bit equivalence for unchanged 5D configurations;
6. create a preregistered N-D projection sweep first, then a separate productive-core N-D experiment after storage migration;
7. never reinterpret earlier 5D experiments as N-D evidence.

---

## R6 — Time-scale and runtime calibration

Benchmark target Hz, achieved Hz, realtime ratio, `dt` and per-subsystem tick cost. Prove pacing-only changes do not alter deterministic simulated outcomes when `dt` and inputs remain unchanged.

---

## R7 — Scientific test of the 5D organization

Compare full 5D organization against dimension-shuffled, reduced-dimensional, increased-dimensional projection and topology-matched non-spatial controls. Measure propagation, locality, learning efficiency, structural motifs, robustness and computational cost. Increased-dimensional *projection* results must not be mislabeled as productive-core N-D results.

---

## R8 — Self-regulation, continuity and sensor-loss studies

Test homeostasis/interoception as functional control mechanisms without anthropomorphic interpretation. Persist body-boundary/sensor availability changes when they are experimental variables.

---

## R9 — Memory and world-model layer

Only after stable behavioral baselines exist: define explicit memory-state contracts, compare memory-on/off, add prediction/recall metrics, distinguish observation history from learned internal state and external knowledge, and require predictive/behavioral utility before using the term world model.

---

## R10 — Multimodal grounding and knowledge intake

Introduce camera/audio/document/network/knowledge observations through typed provenance-rich SignalFrames and Neural Symbiosis/MSBA adapters. Scientific runs require frozen/replayable source snapshots and explicit treatment identity.

---

## R11 — AI-as-treatment research

Compare no-AI, frozen replay, sham/random proposer and model-family conditions under identical research packets. AI involvement remains provenance-bound and cannot be silently mixed into controls.

---

## R12 — Scaling and performance engineering

Scale only when evidence needs justify it. Profile network/tick cost, memory footprint, storage/journal backpressure and bounded telemetry before adding accelerator/native kernels. Any optimization requires semantic-equivalence tests.

## Release direction

Before a new major research milestone is declared:

1. `main` CI is green;
2. deterministic/recovery contracts remain intact;
3. Scientific Integrity Gate is green;
4. new causal capabilities have matched controls;
5. experiment artifacts are reproducible from recorded manifests;
6. documentation source-of-truth is current;
7. AI/peripheral-network involvement is registered as provenance/treatment where applicable;
8. dashboard/catalog visualization remains separated from scientific evidence;
9. historical DATA has not been rewritten to fit newer instrumentation;
10. any open research operationalization or N-D migration work remains explicitly listed in both TODO and this roadmap.

## Historical roadmaps

Files such as `ROADMAP_ALPHA4.md`, `ROADMAP_ALPHA5*.md`, `ROADMAP_V*.md` and sprint-specific plans are historical records and do not override this roadmap.

### 2026-09-08 — File Viewer backlog completion

- Completed the remaining executable File Viewer backlog through the shared Dashboard/Research Chat renderer.
- Added bounded media/PDF metadata and optional local-only Graphviz/PlantUML rendering.
- Added DOCX structural markers, RIS/APA/IEEE citation output and a responsive split editor with live preview/conflict diff.
- Human-review/EVID promotions remain deliberately gated and are never auto-approved by CI or AI tooling.

## Version roadmap — v0.6 to v1.2

### v0.6 — Scaling & deterministic performance
- Larger sparse networks and bounded storage/telemetry.
- Reproducible performance benchmarks across supported Python versions.
- Runtime frequency controls, compact run summaries and deterministic resume.

### v0.7 — Knowledge & learning experiments
- Operational learning protocols with registered controls and independent seeds.
- Interference, retention, transfer and retrieval experiments.
- Evidence-ready statistics artifacts without model-generated quantitative claims.

### v0.8 — Embodiment & Neural Symbiosis
- MSBA peripheral adapters remain experiment-only until controls validate them.
- Sensor/actuator contracts, lesion/noise studies and resource-allocation experiments.
- No production peripheral activation without explicit governance gates.

### v0.9 — Memory, world model & self-model
- Bounded episodic/semantic memory experiments.
- World-model prediction, calibration and counterfactual evaluation.
- Self-model observables treated as operational variables, not consciousness claims.

### v1.0 — Reproducible research platform
- Stable public APIs and artifact schemas.
- Research Review Inbox, evidence workflow and publication-integrity checks integrated end to end.
- Reproducible release bundles, migration notes and compatibility guarantees.

### v1.1 — Replication & multi-system validation
- Independent replication packages and cross-hardware reproducibility studies.
- Comparative baselines against reduced-dimensional, shuffled and non-neural controls.
- External adapter/provider compatibility matrix with provenance hashes.

### v1.2 — Governed adaptive system
- Preregistered adaptive allocation, structural growth and peripheral plasticity behind explicit review gates.
- Human-auditable policy/decision ledger for adaptive system changes.
- Long-horizon stability, rollback, safety isolation and failure-recovery experiments.
- Production enablement remains opt-in and requires validated controls plus human approval.

## Connectome-informed embodiment integration (2026-09-09)

- [x] Add canonical questions/hypotheses/source provenance without duplicate RQ-EMB-001, RQ-REG-002 or RQ-MSBA-E05.
- [x] Register six native exploratory joint/SNN screens and six explicitly blocked advanced designs.
- [x] Add bounded reference import, topology controls, body-state sidecars and design/evidence gates.
- [x] Add source-bytecode consistency, uncertainty-aware Wesen telemetry and a scientific supplement.
- [ ] Obtain and independently validate a pinned licensed biological subset; implement exact source-model replication.
- [ ] Validate three-factor sensorimotor learning, frozen/random gateway controls and disjoint holdout.
- [ ] Execute sensor-compensation, homeostasis, efference-copy and morphology-transfer studies after adapter review.
- [ ] Extend Wesen with separately labelled live/replay/reference modes, causal intervention links and File Viewer inspection.
- [ ] Run prospectively reviewed multi-seed confirmatory experiments and independent replication; no automatic EVID promotion.

[Architecture and execution](../02-architecture/CONNECTOME_EMBODIMENT.md) and
[scientific supplement](../../research/publications/2026-09-09_connectome-embodiment_supplement/README.md).


## PAN / CUDA integration programme

The non-canonical Playground PAN work and its explicit canonical-integration requirements are tracked in the [PAN/GPU work programme](../playground/PAN_GPU_ROADMAP.md). It covers neuron/synapse/network persistence, hybrid and full CUDA execution, body/Neural-I/O coupling, research controls, canonical storage/self-organization, RuntimeController and scaling. Completion of a Playground stage does not promote scientific evidence or establish a canonical backend.


## CUDA/PAN canonicalization and simulator capability gaps (2026-09-28)

The CUDA/PAN/Gate work has reached the point where it creates both a canonicalization programme and a separate simulator-capability backlog. The authoritative gap matrix and architecture decision are documented in [MHRN simulator capability gaps](MHRN_SIMULATOR_CAPABILITY_GAPS.md).

The Playground is **not** promoted wholesale into the core. Reusable execution mechanisms are to be extracted behind canonical MHRN contracts while the Playground remains a composition/reference workspace.

New canonical research families are registered for deterministic accelerated execution, CPU/CUDA parity, computational scaling, executable Gate-IR semantics, PAN state semantics, PAN GPU parity, structural host/GPU barriers, causal closed-loop parity and restricted external simulator interoperability. Registration creates no EVID and does not promote historical Playground verification.

Simulator capability gaps tracked independently from scientific claims include equation-defined model descriptions, physical-unit validation, generalized synapse-rule contracts, multicompartment neurons, electrical/gap-junction synapses, stochastic model specification, standardized benchmark workloads and optional neuromorphic/backend adapters.

Priority order:

1. canonical ExecutionBackend + state identity;
2. canonical Learning/Synapse contract;
3. D1/D2/D3 parity + execution provenance;
4. storage/checkpoint + BoundaryFrame/Neural I/O integration;
5. CUDA-1.6 frozen then live closed-loop bridge;
6. PAN semantic freeze and only then full PAN GPU work;
7. structural mutation through canonical host barriers;
8. standardized benchmarks and Brian 2 reference interoperability;
9. optional broader model DSL, multicompartment, gap junction, neuromorphic and multi-GPU work.


### Contract refinements required before CUDA-1.6

The following contracts are now explicit prerequisites rather than implicit TODOs:

- [Canonical Learning and Synapse Contract](../02-architecture/MHRN_LEARNING_SYNAPSE_CONTRACT.md): CPU and CUDA must implement one update-order/STDP/eligibility/reward/delay semantic contract before plastic D3 work.
- [Frozen Environment Contract](../02-architecture/MHRN_FROZEN_ENVIRONMENT_CONTRACT.md): separates Boundary replay, frozen deterministic world with live actions and full deterministic live-loop parity.
- [Canonical Runtime Checkpoint Contract](../02-architecture/MHRN_RUNTIME_CHECKPOINT_CONTRACT.md): enumerates continuation-critical network, learning, delay, PAN/tissue, Neural-I/O, environment and execution-provenance state.
- [Structural Mutation Approval Contract](../02-architecture/MHRN_STRUCTURAL_APPROVAL_CONTRACT.md): clarifies proposal eligibility, deterministic policy approval, optional human authorization and mandatory host/GPU structural barriers.

The benchmark/reference suite moves **before** live CUDA-1.6 and full PAN-GPU work. A restricted Brian 2 reference subset may be used as an external validation anchor, but never as a hidden MHRN implementation backend or as proof of scientific validity.


## 2026-09-29 Playground -> MHRN integration wave 1

- Promoted the neural-I/O type contract from Playground ownership into the
  canonical Embodiment layer.
- Retained `src/playground/neural_io/contracts.py` as a compatibility
  re-export so existing Playground code remains connected.
- Added a Playground-visible integration catalog and transfer-verification
  surface. Runtime source mutation is explicitly prohibited.
- Next promotion candidate: deterministic neural-I/O codecs, after codec/frame
  semantics are frozen.
- CUDA infrastructure remains queued behind the canonical ExecutionBackend
  boundary; learning, closed-loop and PAN promotion remain blocked by their
  declared semantic contracts.
- OLD frontend views remain retained surfaces and are not implicitly promoted
  into MHRN core.


## 2026-09-29 Playground -> MHRN integration wave 2

- Canonicalized deterministic neural-I/O codecs/decoders under Embodiment.
- Canonicalized a framework-neutral `NeuralIOAreaAdapter` satisfying
  `NetworkAreaAdapter`.
- Kept Playground codec imports as exact compatibility re-exports and the
  Playground adapter as an identity wrapper.
- Neutralized new spike-frame IDs to `mhrn-spike-*`.
- The next technical promotion is the ExecutionBackend abstraction before
  moving CUDA Driver/NVRTC/ABI/parity infrastructure.
- Learning, closed-loop environment and PAN remain blocked by their semantic
  contract gates.


## 2026-09-29 Playground -> MHRN integration wave 3

- Canonical ExecutionBackend protocol added under src/runtime/backend.py.
- BackendState is explicitly data-only and rejects opaque non-serializable runtime handles.
- Canonical D1/D2/D3 parity framework added under src/verification/parity.
- Stable execution fingerprints now bind seed, canonical config hash, backend identity/version, tick count and parity-contract version.
- Counter-RNG, same-tick update ordering and delay-ring semantics are canonical under src/runtime/determinism.
- Playground Builder parity and CUDA plasticity now consume the canonical verifier/determinism primitives through compatibility paths.
- The visible Playground integration catalog marks ExecutionBackend and Parity/Determinism as integrated.
- CUDA Driver/NVRTC/ABI/recurrent/plasticity extraction is the next Wave-4 task.
- No scientific DATA or EVID is created by Wave 3.


## 2026-10-01 — Playground integration Wave 5A

**Goal:** freeze PAN semantics before further GPU promotion.

- [x] Extract the PAN continuation-state surface into
  `src/homeostasis/pan_contract.py`.
- [x] Extract current reference coefficients into `PANFormulaParameters`.
- [x] Declare deterministic update ordering for engineering comparison.
- [x] Make the Playground PAN runtime consume the draft contract without
  changing its algorithm.
- [x] Expose Wave 5 as `contract_draft` in the acceleration status UI.
- [x] Preserve the scientific boundary: RQ-PAN-SEM-001 remains open and PAN
  remains non-evidentiary.
- [ ] Human/method review of the state/update contract.
- [ ] Freeze a versioned PAN v1 contract.
- [ ] Extend RuntimeCheckpoint with all frozen PAN continuation state.
- [ ] Implement the same frozen contract on canonical CUDA PAN execution.
- [ ] Run PAN D1/D2/checkpoint parity only after physical FE-3 acceptance and
  semantic freeze.


## 2026-10-01 — Wave 6/7 contract design

Wave 6 and Wave 7 proceed in parallel with physical RTX-3060 acceptance because
they are semantics/governance work, not hardware acceptance.

### Wave 6 — governed structural plasticity

- [x] Add deterministic approval-policy artifact hashing.
- [x] Define fail-closed modes: DISABLED, MANUAL_ONLY, POLICY_AUTO and PREREGISTERED_AUTO.
- [x] Require mode-specific authorization in addition to topology permission,
  Structural Barrier availability, journal health and scientific freeze.
- [ ] Align the existing StructuralPlasticityEngine mutation path with one canonical host barrier.
- [ ] Bind topology-generation increment, CSR/schedule rebuild and checkpoint
  verification to that barrier.
- [ ] Human Review/freeze of the structural approval contract.
- [ ] CUDA structural mutation remains gated until those steps are complete.

### Wave 7 — learning/synapse semantics

- [x] Inventory current CPU STDP/eligibility/reward order and checkpoint state.
- [x] Inventory current CUDA STP/reward/weight-decay candidate semantics.
- [x] Expose known mismatches fail-closed in an executable contract descriptor.
- [ ] Decide stable edge identity for parallel synapses.
- [ ] Freeze or explicitly exclude STP semantics for the contract version.
- [ ] Align reward-credit and weight-decay semantics across CPU/CUDA.
- [ ] Implement the same frozen contract on both paths and run canonical learning parity.
- [ ] Human Review/freeze before scientific learning studies.

These drafts create no DATA/EVID and do not authorize Wave-5B PAN execution.
