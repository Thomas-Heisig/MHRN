# Open Science & Research Network Integration

This file is the public routing map for MHRN research visibility. GitHub is the canonical software and research source: `develop` is the active integration line and `main` is the release-only public freeze line. External services are mirrors, registries, archives, review layers or discovery indexes; they must not silently change canonical DATA/EVID status.

## Status vocabulary

- **ACTIVE** — public MHRN identity or canonical route already exists and is represented in the repository.
- **CONFIGURED** — repository metadata is ready, but an external account action or public verification is still required.
- **HARVEST TARGET** — no manual duplicate deposit is normally required; discovery should follow DOI/ORCID metadata.
- **SUBMISSION TARGET** — use when a manuscript/reproducibility package is mature enough and platform scope is appropriate.
- **OPTIONAL DISCOVERY** — useful for reach, but not a source of scientific authority.

## Identity, archive, discovery and publication routes

| Service | Role | MHRN status | Required next action |
| --- | --- | --- | --- |
| GitHub | canonical code, protocols, experiment artefacts and version history | **ACTIVE** | integrate on `develop`; publish only green release freezes to `main` |
| Hugging Face MHRN | rolling public source/model-card mirror | **CONFIGURED** | add `HF_USERNAME` and `HF_TOKEN`; workflow creates and synchronizes `MHRN` automatically |
| Hugging Face MHRN-Space | rolling Docker dashboard/research UI mirror | **CONFIGURED** | same credentials; workflow creates and synchronizes `MHRN-Space` automatically |
| Hugging Face MHRN-Research-Data | rolling research-tree discovery mirror | **CONFIGURED** | same credentials; workflow creates and synchronizes `MHRN-Research-Data`; immutable experiment DOIs remain separate |
| ORCID | author identity and cross-service identity anchor | **ACTIVE in repository** — `0009-0002-9589-1872` | verify public ORCID record and authorize trusted auto-updates where desired |
| OSF | project landing page; registrations/preregistrations | **ACTIVE in repository** — `https://osf.io/p34uq/` | use registrations for protocol freezes; do not rely on OSF Projects as the only long-term file store |
| Zenodo | immutable software/data/preprint deposits and DOI minting | **CONFIGURED** — `.zenodo.json` + `CITATION.cff` present | enable/verify MHRN in Zenodo GitHub integration and publish DOI-bearing records |
| DataCite | DOI metadata network | **HARVEST TARGET** | reached through Zenodo and other DOI repositories; ensure ORCID and relations are present in DOI metadata |
| OpenAIRE Research Graph | research-object aggregation and linking | **HARVEST TARGET** | verify records after DOI publication; link funding/project metadata only when factual |
| OpenAlex | scholarly graph / DOI and author discovery | **HARVEST TARGET** | verify DOI/ORCID records after indexing |
| Semantic Scholar | paper and author discovery | **OPTIONAL DISCOVERY** | claim/merge the author profile and paper records after preprints/DOIs exist |
| Google Scholar | scholarly search and citation discovery | **OPTIONAL DISCOVERY** | maintain an author profile and verify indexing; do not treat indexing as review |
| Software Heritage | source-code preservation | **ARCHIVAL TARGET** | verify Zenodo-triggered software archival and/or request Save Code Now for the GitHub origin |
| arXiv | disciplinary preprints | **SUBMISSION TARGET** | submit mature papers when category/scope and endorsement requirements are satisfied |
| bioRxiv | life-science preprints | **SUBMISSION TARGET if scope fits** | use only for manuscripts genuinely within bioRxiv scope; not as a generic software mirror |
| NeuroLibre | executable reproducible neuroscience preprints | **HIGH-PRIORITY SUBMISSION TARGET** | prepare a dedicated NRP-compatible repository/package, public data archive and reproducible runtime |
| PCI / Peer Community In | open recommendation/peer-review layer for preprints | **SUBMISSION TARGET where a matching PCI exists** | submit an appropriate preprint to the relevant PCI and keep recommendation status separate from MHRN EVID |
| HAL | open scholarly repository / long-term dissemination | **OPTIONAL DEPOSIT TARGET** | deposit suitable preprints/software records where permitted and cross-link DOI/ORCID |
| ResearchGate | researcher-facing discovery/social dissemination | **OPTIONAL DISCOVERY** | claim profile and link legally shareable versions/DOIs; do not upload publisher-restricted files |
| institutional/conference proceedings | formal scientific dissemination | **SUBMISSION TARGET** | submit papers/posters where scope fits; list affiliation truthfully as independent researcher when applicable |
| specialist workshops/posters | direct community discovery | **OUTREACH TARGET** | prioritize SNN, neuromorphic, computational-neuroscience and reproducibility venues |
| direct researcher contact | targeted scientific communication | **OUTREACH TARGET** | contact authors whose work is directly used, linking one concrete result/protocol rather than a generic project pitch |

## Repository metadata surfaces

- `CITATION.cff`: GitHub citation and software-author metadata.
- `.zenodo.json`: Zenodo release-deposit metadata. Because both files exist, Zenodo's GitHub integration uses `.zenodo.json` for release metadata.
- `codemeta.json`: machine-readable software discovery metadata.
- `research-network-registry.json`: machine-readable visibility/status registry.
- `pyproject.toml`: package identity and project URLs.
- `INDEPENDENT_REPLICATION.md`: public replication invitation.
- `HF_MODEL_README.md`: generated Hugging Face source/model-card landing page.
- `HF_DATASET_README.md`: generated rolling research-data mirror landing page.
- `.github/workflows/sync-huggingface.yml`: self-provisioning Hugging Face publication fan-out from release-only `main`.
- `.github/ISSUE_TEMPLATE/independent_replication.md`: structured intake for replication reports.

## Publication object model

Do not make one GitHub software release masquerade as multiple scientific object types.

### Software releases

A normal MHRN software release represents a software version. When the Zenodo-GitHub connection is enabled for this repository, eligible GitHub releases can be archived as immutable software records with DOI/version metadata and downstream source preservation.

### Experiment datasets

An experiment dataset should be deposited as a **separate dataset/research object** when a DOI is required for that experiment. Its metadata should identify:

- experiment ID;
- RQ and hypothesis;
- preregistration;
- source-freeze commit;
- canonical DATA commit;
- software release/commit used;
- raw/processed data included;
- analysis code;
- claim boundary;
- Human Review / EVID / independent-replication status.

Do not tag every experiment as a new software version solely to obtain a DOI. That conflates software versioning with dataset identity.

### Preprints

Mature papers may be deposited as preprints and linked bidirectionally to their code/data DOI records. Working manuscripts must remain labelled as working manuscripts until intentionally released.

### Reproducible executable papers

For NeuroLibre, prepare a separate publication-ready reproducibility package with notebooks/MyST content, public data, a reproducible Binder-compatible runtime, bibliography and author metadata. NeuroLibre technical screening verifies the reproducibility package; it must not be recorded internally as scientific peer review unless a separate scientific review process actually occurred.

### External recommendation / review

PCI-style recommendations, journal peer review, conference review and independent replication are distinct events. Record each separately. None should be collapsed into a generic `reviewed=true` flag.

## Current replication targets

See [INDEPENDENT_REPLICATION.md](INDEPENDENT_REPLICATION.md) for the current open call covering:

- `EXP-S1-TEMP-ORDER-V2-20260919`
- `EXP-REC-002-CLEAN-R2-20260919`
- `EXP-SNN004-STDP-ASYM-R2-20260919`

## External visibility workflow

For each release-quality scientific object:

1. freeze code/protocol/data and verify green CI;
2. publish the correct object type (software, dataset, preprint, reproducibility package);
3. mint or record DOI;
4. include ORCID and bidirectional related identifiers;
5. verify propagation to DataCite/OpenAIRE/OpenAlex;
6. claim/merge Semantic Scholar and Google Scholar records after indexing;
7. preserve code in Software Heritage;
8. submit mature manuscript to arXiv/bioRxiv/HAL as scope allows;
9. submit central reproducibility paper to NeuroLibre when package requirements are met;
10. submit to a matching PCI or formal venue for external review/recommendation;
11. distribute the independent-replication call directly to relevant researchers and specialist communities;
12. record external responses, replications, reviews and contradictions without changing historical DATA.

## Account-side actions that cannot be encoded in Git

Repository metadata prepares the records, but these require the account owner or an external submission system:

- enable/verify the Zenodo-GitHub repository connection;
- publish Zenodo deposits/DOIs;
- create/finalize OSF registrations;
- authorize ORCID update permissions;
- verify/claim OpenAIRE, OpenAlex, Semantic Scholar, Google Scholar, HAL or ResearchGate records where user action is offered;
- satisfy arXiv account/category/endorsement requirements and submit a manuscript;
- submit to bioRxiv where within scope;
- submit a NeuroLibre reproducibility package and complete technical screening;
- submit to a relevant PCI or conference/journal;
- send direct researcher outreach.

No repository file should claim these actions are complete until the public record can be verified.

## Verification after publication

For every new DOI/preprint/external review:

1. confirm title, authors and ORCID;
2. confirm resource type;
3. confirm GitHub/source-freeze/data links;
4. add DOI/external identifier back to canonical metadata;
5. verify discovery in relevant scholarly graphs;
6. merge duplicate author-paper records when possible;
7. record review/recommendation/replication status as its own provenance object;
8. never infer Human Review, EVID or independent replication from indexing, downloads or citations alone.
