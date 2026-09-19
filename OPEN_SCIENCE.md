# Open Science & Research Network Integration

This file is the public routing map for MHRN research visibility. GitHub `main` is the canonical software and research source. External services are mirrors, registries, archives or discovery indexes; they must not silently change canonical DATA/EVID status.

## Identity and canonical records

| Service | Role | MHRN status / route |
| --- | --- | --- |
| GitHub | canonical code, protocols, experiment artefacts and version history | https://github.com/Thomas-Heisig/MHRN |
| ORCID | author identity and cross-service identity anchor | https://orcid.org/0009-0002-9589-1872 |
| OSF | preregistration / registration layer and project landing page | https://osf.io/p34uq/ |
| Zenodo | immutable software/data/preprint deposits and DOI minting | GitHub release integration should archive eligible releases; `.zenodo.json` and `CITATION.cff` provide repository metadata |
| OpenAIRE Research Graph | downstream discovery graph | expected primarily through DOI/metadata harvesting from Zenodo/DataCite and other scholarly sources; verify records after each DOI becomes public |
| OpenAlex | scholarly discovery/index graph | DOI/ORCID-based discovery; verify after DOI publication |
| Semantic Scholar | paper/author discovery | claim the author profile and paper records after public preprints/DOIs exist |
| Google Scholar | citation discovery | add public papers/preprints/DOIs to the author profile when indexed |
| arXiv | preprints for mature scientific manuscripts | submit publication-ready papers, not raw experiment folders |
| NeuroLibre | executable, reproducible neuroscience papers | use for central experiments with a complete reproducible computational environment |
| DataCite ecosystem | DOI metadata propagation | reached through DOI-granting repositories such as Zenodo |

## Repository metadata surfaces

- `CITATION.cff`: GitHub citation and software-author metadata.
- `.zenodo.json`: Zenodo release-deposit metadata.
- `codemeta.json`: machine-readable software discovery metadata.
- `pyproject.toml`: package identity and project URLs.
- `INDEPENDENT_REPLICATION.md`: public replication invitation.
- `.github/ISSUE_TEMPLATE/independent_replication.md`: structured intake for replication reports.

## Publication model

Do not make one GitHub software release masquerade as multiple scientific object types.

### Software releases

A normal MHRN software release represents a software version. When the Zenodo-GitHub connection is enabled for this repository, eligible GitHub releases can be archived as immutable software records with DOI/version metadata.

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

## Current replication targets

See [INDEPENDENT_REPLICATION.md](INDEPENDENT_REPLICATION.md) for the current open call covering:
- `EXP-S1-TEMP-ORDER-V2-20260919`
- `EXP-REC-002-CLEAN-R2-20260919`
- `EXP-SNN004-STDP-ASYM-R2-20260919`

## Account-side actions that cannot be encoded in Git

Repository metadata prepares the records, but the following require the account owner in the respective service:

- enable/verify the Zenodo-GitHub repository connection;
- finalize and publish deposits/DOIs;
- create/finalize OSF registrations;
- authorize ORCID update permissions where desired;
- submit manuscripts to arXiv;
- claim/merge Semantic Scholar and Google Scholar author records;
- submit a NeuroLibre article and address its review/build requirements.

No repository file should claim these account-side actions are complete until the public record can be verified.

## Verification after publication

For every new DOI/preprint:
1. confirm title, author and ORCID;
2. confirm software/data/preprint resource type;
3. confirm GitHub/source-freeze links;
4. add DOI back to the appropriate canonical metadata file;
5. confirm discovery in ORCID, OpenAIRE and OpenAlex once indexed;
6. claim/merge duplicate author-paper records in discovery services;
7. never infer Human Review, EVID or independent replication from indexing alone.
