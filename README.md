# Multi-Scale Homeostatic Recurrence Network (MHRN)

## Mehrskaliges homöostatisches Rekurrenznetzwerk

**A Spiking Neural Architecture with Topological Plasticity**  
*Eine spikende neuronale Architektur mit topologischer Plastizität*

[![Release CI](https://github.com/Thomas-Heisig/MHRN/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Thomas-Heisig/MHRN/actions/workflows/ci.yml)
[![Develop CI](https://github.com/Thomas-Heisig/MHRN/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/Thomas-Heisig/MHRN/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Thomas-Heisig/MHRN?include_prereleases&label=release)](https://github.com/Thomas-Heisig/MHRN/releases/tag/v0.6.0-alpha.7)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Publication](https://img.shields.io/badge/publication-1.8_WIP-blue.svg)](research/publications/CURRENT.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0002--9589--1872-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0002-9589-1872)
[![OSF](https://img.shields.io/badge/OSF-p34uq-2CB9F1?logo=osf&logoColor=white)](https://osf.io/p34uq/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-ThomasHeisig%2FMHRN-FFD21E)](https://huggingface.co/ThomasHeisig/MHRN)
<!-- zenodo-doi-badge:start -->
[![DOI](https://zenodo.org/badge/1335973891.svg)](https://zenodo.org/badge/latestdoi/1335973891)
<!-- zenodo-doi-badge:end -->

MHRN is an experimental research framework for studying recurrent spiking neural networks, plasticity, self-organization, embodiment, memory and world-model mechanisms under explicit provenance and evidence boundaries.

The sparse **5D SNN remains the primary adaptive system**. Language models, research assistants, peripheral neural networks and digital gateways are bounded components; they do not receive implicit authority over canonical neural state, reward, experiment DATA or accepted EVID.

> **Scientific boundary:** implementation, passing tests, dashboards, generated reports, registered protocols, software releases and DOI assignment are not automatically scientific evidence. MHRN currently makes no claim of AGI, consciousness, sentience, biological equivalence or a demonstrated general advantage of the 5D address space.

> **AI transparency:** AI assistants materially support research leads, critique, code, tests and text. Their use is explicitly documented and is itself part of MHRN's methodological research programme. AI output is not treated as authorship, source authority or scientific evidence; Thomas Heisig retains human responsibility for selection, approval and publication.

## Research identity & open-science routes

| Resource | Canonical route | Role |
| --- | --- | --- |
| Source | [GitHub · Thomas-Heisig/MHRN](https://github.com/Thomas-Heisig/MHRN) | canonical code, history and governed research artefacts |
| Current software release | [v0.6.0-alpha.7](https://github.com/Thomas-Heisig/MHRN/releases/tag/v0.6.0-alpha.7) | immutable exact-green source freeze |
| Author identity | [ORCID · 0009-0002-9589-1872](https://orcid.org/0009-0002-9589-1872) | persistent researcher identity |
| Open Science Framework | [OSF · p34uq](https://osf.io/p34uq/) | project / open-science route |
| Hugging Face | [ThomasHeisig/MHRN](https://huggingface.co/ThomasHeisig/MHRN) | rolling source/discovery mirror |
| Hugging Face Space | [ThomasHeisig/MHRN-Space](https://huggingface.co/spaces/ThomasHeisig/MHRN-Space) | public dashboard mirror |
| Research-data mirror | [ThomasHeisig/MHRN-Research-Data](https://huggingface.co/datasets/ThomasHeisig/MHRN-Research-Data) | rolling discovery mirror; not an immutable DOI dataset |
| Zenodo | [Latest DOI / archived release](https://zenodo.org/badge/latestdoi/1335973891) | DOI archive for GitHub releases; badge resolves to the latest archived version once ingestion completes |

The `v0.6.0-alpha.7` release is prepared from the exact green `develop` integration freeze `04f2cd76fa5d18c08a903f3e30aa275afdec31a6`; the immutable GitHub release tag is created only after the release PR has merged to `main` and the resulting `main` CI is green. The repository intentionally records a Zenodo DOI only after a real public Zenodo record exists. Once discovered, the DOI sync replaces the pending badge above with Zenodo's official DOI badge and records the DOI in the citation and publication metadata.

### Citation model

MHRN deliberately separates three citable research objects:

| Object | Type | Current state |
| --- | --- | --- |
| **MHRN v0.6.0-alpha.7** | Software | GitHub release published; Zenodo software DOI route active |
| **Recursive Epistemics / Rekursive Epistemik 1.8** | Publication / preprint | separate Zenodo publication package prepared; DOI pending |
| **MHRN research data** | Dataset(s) | rolling discovery mirror exists; immutable experiment DOI deposits remain separate |

Use the **software DOI** when citing the implementation, the **publication DOI** when citing the scientific manuscript, and a **dataset DOI** when citing a frozen experiment dataset. A DOI on any layer does not promote DATA to accepted EVID.


---

<!-- publication-current-1.8 -->
## Scientific publication: edition 1.8 WIP

The eleven-part structure planned for publication 2.0 is implemented now as **edition 1.8 WIP**, independently of the MHRN software version. It integrates the reconstructed prehistory, architecture, empirical programme, engineering, epistemology, attribution, ethics, recursive epistemics and open research.

- [Current manuscript](research/publications/2026-09-17_recursive-epistemics_v1.8/MANUSCRIPT.md)
- [Research questions and hypotheses](research/publications/2026-09-17_recursive-epistemics_v1.8/RESEARCH_REGISTER.md)
- [Complete baseline source inventory](research/publications/2026-09-17_recursive-epistemics_v1.8/SOURCE_INDEX.md)
- [Unabridged 1.7 source volume](research/publications/2026-09-17_recursive-epistemics_v1.8/LEGACY_V17.md)
- [Prior research map](research/publications/2026-09-17_recursive-epistemics_v1.8/PRIOR_WORK_MAP.md)
- [Extension and citation contract](research/publications/2026-09-17_recursive-epistemics_v1.8/EXTENDING.md)
- [Scientific balance of Edition 1.8](research/publications/2026-09-17_recursive-epistemics_v1.8/SCIENTIFIC_BALANCE.md)
- [Paper offshoots — six bounded publication strands](research/paper_offshoots/README.md)
- [Edition and working-branch genealogy](research/publications/2026-09-17_recursive-epistemics_v1.8/EDITION_GENEALOGY.md)
- [Publication-specific citation metadata](research/publications/2026-09-17_recursive-epistemics_v1.8/CITATION.cff)

Historical publication bytes and empirical artifacts are preserved. Reconstructed chat history remains S4 until original messages are source-bound.

---

## Current state — 21 September 2026

| Area | Current state |
| --- | --- |
| Release branch | `main` — release-only, public frozen line |
| Integration branch | `develop` — active development and research integration |
| Package | `mhrn-core 0.6.0a7` / `0.6.0-alpha.6` |
| Release status | **v0.6.0-alpha.7 release candidate** from green `develop` freeze `04f2cd76fa5d18c08a903f3e30aa275afdec31a6`; publication occurs only after the release PR and post-merge `main` CI are green |
| Engineering | Stage 2 recurrent contract closed at its scoped engineering boundary; Stage 3 plastic neural tissue reached; Stage 4/5 engineering contracts integrated; Stage 6 mechanisms and research programme active |
| Scientific focus | Stage 6 — memory, continual learning, semantization, prediction error and world-model validation; independent external replication remains open |
| Current manuscript | **Recursive Epistemics / Rekursive Epistemik 1.8 — WIP** |
| Publication lineage | 1.8 current WIP → 1.7 predecessor → 1.5 frozen empirical baseline |
| Evidence policy | `implementation/test != DATA != reviewed EVID != independent replication`; release/DOI do not promote evidence |
| AI methodology | AI assistance is explicitly disclosed; the human-AI research process is itself a methodological research object while human authorship and responsibility remain separate |
| Document governance | all `docs/` and `research/` files are classified by role, status, authority, mutability, citation rule and evidence role |

The authoritative machine-readable release record is [`releases/current.json`](releases/current.json). Project identity and naming rules are in [`project_identity.json`](project_identity.json) and [`NAMING.md`](NAMING.md).

### Current Stage-6 research

The present scientific focus is deliberately narrower than the implemented feature set:

- **`EXP-S6-SEM-CL-001`** produced a positive preregistered mechanism result against its own naive online/no-replay baseline.
- **`EXP-S6-SEM-CL-002`** produced a preregistered paired **negative result** for the more specific claim that semantic prototypes outperform matched raw replay under that protocol. The preregistered H1 success criteria were not met.
- **`EXP-S6-SEM-CL-003`** was executed exactly once under its frozen authorization as 84 runs (12 seeds × 7 conditions). The preregistered classification is `H1_negative_H2_negative`: no confirmed Semantic-over-Raw advantage and no confirmed dose interaction. C3 (`S20 − X20`) is positive at about +14.9 percentage points and shows that the semantic representation carries non-random task-relevant structure. The complete result remains **DATA pending human review**, not accepted EVID.

The bounded DATA-level conclusion is therefore: **Replay contributes to the observed benefit; under the matched CL-002/CL-003 conditions semantic compression has not shown a preregistered additional advantage over Raw-Replay, although the semantic representation itself carries relevant structure.** Stage 6 is not declared solved; the Semantization/Replay subquestion is treated as **empirically narrowed** pending Human Review.

See [`research/CURRENT_SCIENTIFIC_STATE.md`](research/CURRENT_SCIENTIFIC_STATE.md) for the current scientific interpretation and limitations. The historical DATA-only Stage-6 balance incorporated into Edition 1.8 remains preserved at [`research/publications/2026-09-15_recursive-epistemics_v1.7/STAGE6_CL001_CL003_BALANCE.md`](research/publications/2026-09-15_recursive-epistemics_v1.7/STAGE6_CL001_CL003_BALANCE.md).

---

## Repository workflow

MHRN uses a release-oriented branch model:

```text
feature / fix / research / chore
            ↓
          develop
            ↓
        release/*
            ↓
           main
```

- **`main`** contains only release-ready public states.
- **`develop`** is the canonical integration branch for ongoing engineering, research tooling, documentation and publication work.
- Normal pull requests target **`develop`**.
- Only explicit **`release/*`** branches may target **`main`**.
- Release merge requires green CI, the release-policy check, applicable integrity gates, and a clean tracked tree.
- Force-pushes and history rewrites of `main` are outside project policy.

See [Branching and release policy](docs/00-governance/BRANCHING_AND_RELEASE_POLICY.md).

---

## Stable entry points

The internal documentation and experiment taxonomy is being refined. The links below are intentionally the stable entry points and should be preferred over hard-coded historical paths:

- **Documentation:** [`docs/README.md`](docs/README.md)
- **Research:** [`research/README.md`](research/README.md)
- **Open science / research networks:** [`OPEN_SCIENCE.md`](OPEN_SCIENCE.md)
- **Machine-readable research-network registry:** [`research-network-registry.json`](research-network-registry.json)
- **Independent replication call:** [`INDEPENDENT_REPLICATION.md`](INDEPENDENT_REPLICATION.md)
- **Current scientific state:** [`research/CURRENT_SCIENTIFIC_STATE.md`](research/CURRENT_SCIENTIFIC_STATE.md)
- **Seed DATA contract:** [`research/specifications/SEED_DATA_CONTRACT.md`](research/specifications/SEED_DATA_CONTRACT.md)
- **Current publication pointer:** [`research/publications/CURRENT.md`](research/publications/CURRENT.md)
- **Research software paper:** [MHRN Research Software Paper](research/publications/papers/2026-09-20_mhrn-research-software_v0.1/PAPER.md)
- **Topology paper:** [Dimensional Embedding and Propagation Dynamics](research/publications/papers/2026-09-20_topology-dynamics_v0.1/PAPER.md)
- **Methods paper:** [Provenance-Separated Reporting for AI-Assisted Research](research/publications/papers/2026-09-20_recursive-epistemics-methods_v0.1/PAPER.md)
- **Publication catalog / viewer source:** [`research/publications/catalog.json`](research/publications/catalog.json)
- **Frozen empirical baseline 1.5:** [`research/publications/FROZEN_V1.5.md`](research/publications/FROZEN_V1.5.md)
- **Current release record:** [`releases/current.json`](releases/current.json)
- **Release checklist:** [`docs/10-releases/RELEASE_CHECKLIST.md`](docs/10-releases/RELEASE_CHECKLIST.md)
- **Engineering roadmap:** [`docs/08-roadmap/ROADMAP.md`](docs/08-roadmap/ROADMAP.md)
- **Scientific maturity roadmap:** [`docs/08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md`](docs/08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md)
- **Research roadmap:** [`docs/08-roadmap/RESEARCH_ROADMAP.md`](docs/08-roadmap/RESEARCH_ROADMAP.md)
- **Current TODO:** [`docs/08-roadmap/TODO.md`](docs/08-roadmap/TODO.md)
- **Privacy / Datenschutz:** [`PRIVACY.md`](PRIVACY.md)
- **Public imprint metadata:** [`public_imprint.json`](public_imprint.json)

The Publication Viewer follows the machine-readable publication catalog and should open the current WIP manuscript rather than a frozen predecessor.

---

## System architecture

```text
External / simulated / virtual environment
        |
        v
Sensors / audio / vision / digital data / devices
        |
        v
Embodiment + authorization + provenance
        |
        +------ optional bounded peripheral neural / virtual areas
        |                 |
        |          Neural Symbiosis / MSBA gateway
        |                 |
        v                 v
+--------------------------------------------------+
|             Sparse 5D Spiking Neural Core        |
| dynamics | recurrence | plasticity | regulation |
+----------------------+---------------------------+
                       |
          +------------+-------------+
          |                          |
          v                          v
 Structural plasticity         Action proposals
 proposal -> approval          explicit decoding /
 -> mutation -> journal        actuator boundary
 -> undo/recovery                    |
                                      v
                               observed outcome
                                      |
                               feedback / reward

Persistence, experiment provenance, DATA/EVID separation
and integrity gates surround the complete loop.
```

### Implemented layers

| Layer | Current capability |
| --- | --- |
| SNN core | sparse 5D coordinates, recurrent connectivity, delayed event propagation, deterministic RNG state, Izhikevich/LIF model paths |
| Plasticity | STDP, eligibility traces, delayed reward / three-factor learning, homeostatic regulation and structural plasticity contracts |
| Structural change | proposal → approval/rejection → bounded mutation → journal → undo/recovery |
| Persistence | `.b5d` snapshots, checkpoints, journals, deterministic restore/continue and compatibility contracts |
| Embodiment | typed sensors/actuators, authorization, audit trails, device discovery and machine-native interoception |
| Neural Symbiosis / MSBA | bounded modality-specific and peripheral neural/virtual gateway contracts with explicit learning controls |
| Memory / prediction | bounded working and episodic memory, replay/consolidation candidates, prediction/world-model infrastructure with explicit claim limits |
| Research system | RQ/H registries, preregistration, experiment runner, DATA/EVID separation, source provenance, review and integrity gates |
| Dashboard | operator/research UI, Research Observatory, Publication/File Viewer, Wesen/Embodiment, experiment and review workflows |
| AI boundary | research AI / Language Organ / Cognitive Advisor remain read-only or proposal-only unless explicitly registered as an experimental treatment |

Detailed architecture: [`docs/02-architecture/ARCHITECTURE.md`](docs/02-architecture/ARCHITECTURE.md).

---

## Scientific and engineering separation

MHRN uses two deliberately separate maturity axes:

1. **Engineering maturity** — whether mechanisms, interfaces, persistence, UI and verification contracts exist and behave as specified.
2. **Scientific maturity** — whether registered questions have suitable frozen protocols, source-bound DATA, reviewed EVID, replications, controls and defensible claim scope.

A technically complete stage can therefore remain scientifically open.

Key safeguards include:

- no automatic DATA → EVID promotion;
- historical DATA and frozen publications are not silently rewritten;
- negative and null results remain part of the record;
- exploratory runs are not relabelled as confirmatory evidence;
- scientific claims remain bounded to the tested population, protocol, implementation and measurement;
- external methods and prior work require attribution and provenance;
- AI-generated or unverified sources are not treated as scientific authority.

Governance: [`docs/00-governance/DOCUMENT_GOVERNANCE.md`](docs/00-governance/DOCUMENT_GOVERNANCE.md)  
Integrity gate: [`docs/05-quality/RESEARCH_INTEGRITY_GATE.md`](docs/05-quality/RESEARCH_INTEGRITY_GATE.md)

---

## Research workflow

```text
Research Question
    -> Hypothesis
    -> frozen / preregistered protocol
    -> Experiment
    -> DATA
    -> analysis + limitations
    -> human / independent review
    -> EVID decision
    -> bounded claim
```

The canonical research registries, schemas, protocols and experiment records live under [`research/`](research/). Their detailed taxonomy is maintained by the research index rather than duplicated here.

---

## Quick start

### Clone and create the environment

```bash
git clone https://github.com/Thomas-Heisig/MHRN.git
cd MHRN
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### Start MHRN

Windows with dashboard and browser:

```powershell
.\start.ps1
```

Direct Python start:

```bash
python -m src.main --config configs/poc_alpha5_live.yaml
```

The direct Python entry point binds the dashboard to loopback by default. The Windows wrappers are intended for trusted-LAN operation and bind to `0.0.0.0:8765` by default; use `-DashboardHost 127.0.0.1` for local-only access.

Preferred launcher implementation: [`scripts/mhrn_launcher.py`](scripts/mhrn_launcher.py).

---

## Verification

Typical local checks:

```bash
python -m pytest -m "not slow"
python -m pytest -m "slow"
python -m mypy src/
python -m pyright
python -m black --check src tests scripts
python -m ruff check src tests scripts
python -m pre_commit run --all-files
```

The repository also uses dedicated workflows for scientific integrity, empirical-data integrity, cognition/research contracts, packaging, security and release verification. A green software gate does not by itself promote a scientific claim.

---

## Repository map

```text
src/                     runtime implementation
  core/                  recurrent sparse SNN
  learning/              STDP, eligibility and reward learning
  homeostasis/           regulatory mechanisms
  self_organization/     structural plasticity and morphology
  embodiment/            sensors, actuators and gateway contracts
  experience/            closed-loop composition
  storage/               snapshots, journals and recovery
  research/              runtime research/evidence machinery
  research_assistant/    bounded AI research tooling
  dashboard/             APIs and operator/research frontend

research/                questions, hypotheses, protocols, experiments,
                         DATA/EVID, literature, reviews and publications

docs/                    governed technical/scientific documentation
configs/                 runtime and experiment configuration
tests/                   regression and contract verification
scripts/                 verification, governance and utility scripts
releases/                machine-readable release records
```

For the live directory taxonomy, use [`docs/README.md`](docs/README.md) and [`research/README.md`](research/README.md); they are the canonical navigation indexes.

---

## Current open scientific work

Major open items include:

- human scientific review of CL-003 and an explicit EVID decision;
- a deliberate post-review Stage-6 research decision before any CL-004 is defined;
- independent replication of central Stage 2–6 findings;
- neuronally defined and ablatable prediction-error mechanisms;
- multi-step action-conditioned world-model dynamics and decision benefit;
- complete coupled-state checkpoint/restore identity for claim-relevant cognition state;
- matched dimensional ablations for the 5D address-space hypothesis;
- systematic prior-art, source and external similarity review before formal manuscript submission.

These items are tracked in the canonical roadmaps rather than as fixed completion percentages in this README.

---

## Security

The dashboard exposes operator, research and file-management capabilities. Do not expose it directly to the public Internet. For trusted-LAN use, restrict TCP port `8765` to the intended private network.

See [`SECURITY.md`](SECURITY.md) and [`docs/03-dashboard/DASHBOARD.md`](docs/03-dashboard/DASHBOARD.md).

---

## Publication, citation and history

Current scientific publication pointer: [`research/publications/CURRENT.md`](research/publications/CURRENT.md).  
Publication archive: [`research/publications/README.md`](research/publications/README.md).  
Change history: [`CHANGELOG.md`](CHANGELOG.md).  
Contribution guide: [`CONTRIBUTING.md`](CONTRIBUTING.md).  
Software citation metadata: [`CITATION.cff`](CITATION.cff).  
Edition 1.8 publication citation metadata: [`research/publications/2026-09-17_recursive-epistemics_v1.8/CITATION.cff`](research/publications/2026-09-17_recursive-epistemics_v1.8/CITATION.cff).
Machine-readable discovery metadata: [`codemeta.json`](codemeta.json).  
Open-science routing and account-side publication checklist: [`OPEN_SCIENCE.md`](OPEN_SCIENCE.md).  
Independent replication invitation: [`INDEPENDENT_REPLICATION.md`](INDEPENDENT_REPLICATION.md).

```bibtex
@software{heisig2026mhrn,
  author  = {Thomas Heisig},
  title   = {Multi-Scale Homeostatic Recurrence Network (MHRN)},
  year    = {2026},
  version = {0.6.0a7},
  url     = {https://github.com/Thomas-Heisig/MHRN},
  license = {MIT}
}
```

Historical names, experiment identifiers, publication checksums and compatible `.b5d` files retain their documented meaning. Renaming the project does not constitute new scientific evidence.

## License

MIT License. See [`LICENSE`](LICENSE).
