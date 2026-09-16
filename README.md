# Multi-Scale Homeostatic Recurrence Network (MHRN)

## Mehrskaliges homöostatisches Rekurrenznetzwerk

**A Spiking Neural Architecture with Topological Plasticity**  
*Eine spikende neuronale Architektur mit topologischer Plastizität*

[![CI](https://github.com/Thomas-Heisig/MHRN/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Thomas-Heisig/MHRN/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.6.0a4-orange.svg)](pyproject.toml)
[![Publication](https://img.shields.io/badge/publication-1.7_WIP-blue.svg)](research/publications/CURRENT.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

MHRN is an experimental research framework for studying recurrent spiking neural networks, plasticity, self-organization, embodiment, memory and world-model mechanisms under explicit provenance and evidence boundaries.

The sparse **5D SNN remains the primary adaptive system**. Language models, research assistants, peripheral neural networks and digital gateways are bounded components; they do not receive implicit authority over canonical neural state, reward, experiment DATA or accepted EVID.

> **Scientific boundary:** implementation, passing tests, dashboards, generated reports, registered protocols and completed experiment runs are not automatically scientific evidence. MHRN currently makes no claim of AGI, consciousness, sentience, biological equivalence or a demonstrated general advantage of the 5D address space.

---

## Current state — 16 September 2026

| Area | Current state |
| --- | --- |
| Canonical branch | `main` |
| Package | `mhrn-core 0.6.0a4` / `0.6.0-alpha.4` |
| Release status | development; gate open; no active release blocker, final source-freeze/release closure still pending |
| Engineering | Stage 2 recurrent contract closed at its scoped engineering boundary; Stage 3 plastic neural tissue reached; Stage 4/5 engineering contracts integrated; Stage 6 mechanisms and research programme active |
| Scientific focus | Stage 6 — memory, continual learning, semantization, prediction error and world-model validation |
| Current manuscript | **Recursive Epistemics / Rekursive Epistemik 1.7 — WIP** |
| Publication lineage | 1.7 current WIP → 1.6 predecessor → 1.5 frozen empirical baseline |
| Evidence policy | `implementation test != DATA != reviewed EVID != interpretation` |
| Document governance | all `docs/` and `research/` files are classified by role, status, authority, mutability, citation rule and evidence role |

The authoritative machine-readable release record is [`releases/current.json`](releases/current.json). Project identity and naming rules are in [`project_identity.json`](project_identity.json) and [`NAMING.md`](NAMING.md).

### Current Stage-6 research

The present scientific focus is deliberately narrower than the implemented feature set:

- **`EXP-S6-SEM-CL-001`** produced a positive preregistered mechanism result against its own naive online/no-replay baseline.
- **`EXP-S6-SEM-CL-002`** produced a preregistered paired **negative result** for the more specific claim that semantic prototypes outperform matched raw replay under that protocol. The preregistered H1 success criteria were not met.
- **`EXP-S6-SEM-CL-003`** was executed on 16 September 2026 under its frozen authorization. The persisted machine result is `H1_negative_H2_negative`; DATA remain pending Human Review and are not EVID.

The bounded conclusion is therefore not “semantic memory established”, but that the current implementation has memory/replay/semantic-candidate mechanisms while the stronger semantization and world-model claims remain open to controlled testing and replication.

See [`research/CURRENT_SCIENTIFIC_STATE.md`](research/CURRENT_SCIENTIFIC_STATE.md) for the current scientific interpretation and limitations.

---

## Stable entry points

The internal documentation and experiment taxonomy is being refined. The links below are intentionally the stable entry points and should be preferred over hard-coded historical paths:

- **Documentation:** [`docs/README.md`](docs/README.md)
- **Research:** [`research/README.md`](research/README.md)
- **Current scientific state:** [`research/CURRENT_SCIENTIFIC_STATE.md`](research/CURRENT_SCIENTIFIC_STATE.md)
- **Current publication pointer:** [`research/publications/CURRENT.md`](research/publications/CURRENT.md)
- **Publication catalog / viewer source:** [`research/publications/catalog.json`](research/publications/catalog.json)
- **Frozen empirical baseline 1.5:** [`research/publications/FROZEN_V1.5.md`](research/publications/FROZEN_V1.5.md)
- **Current release record:** [`releases/current.json`](releases/current.json)
- **Engineering roadmap:** [`docs/08-roadmap/ROADMAP.md`](docs/08-roadmap/ROADMAP.md)
- **Scientific maturity roadmap:** [`docs/08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md`](docs/08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md)
- **Research roadmap:** [`docs/08-roadmap/RESEARCH_ROADMAP.md`](docs/08-roadmap/RESEARCH_ROADMAP.md)
- **Current TODO:** [`docs/08-roadmap/TODO.md`](docs/08-roadmap/TODO.md)

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

- independent replication of central Stage 2–6 findings;
- CL-003 execution only under its frozen authorization/protocol chain;
- replay/consolidation and semantization studies with matched controls;
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
Citation metadata: [`CITATION.cff`](CITATION.cff).

```bibtex
@software{heisig2026mhrn,
  author  = {Thomas Heisig},
  title   = {Multi-Scale Homeostatic Recurrence Network (MHRN)},
  year    = {2026},
  version = {0.6.0a4},
  url     = {https://github.com/Thomas-Heisig/MHRN},
  license = {MIT}
}
```

Historical names, experiment identifiers, publication checksums and compatible `.b5d` files retain their documented meaning. Renaming the project does not constitute new scientific evidence.

## License

MIT License. See [`LICENSE`](LICENSE).
