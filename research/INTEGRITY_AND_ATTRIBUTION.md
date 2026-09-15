# MHRN Research Integrity and Attribution Policy

**Status:** project policy / pre-submission control

**Applies to:** source code, documentation, research reports, dissertation/manuscript editions, figures, experiment protocols, AI-assisted drafts, benchmark notes and release notes.

## 1. Purpose

MHRN separates scientific progress from engineering progress. The same separation applies to research integrity: a technically reproducible artifact is not automatically an original scientific contribution, and a correctly cited source is not automatically evidence for an MHRN claim.

This policy reduces plagiarism, text-recycling, citation, licensing and provenance risks. It does **not** certify that a manuscript is plagiarism-free. External similarity checking and human source review remain mandatory before submission.

## 2. Mandatory provenance classes

Every substantial scientific statement should be traceable to at least one of the following provenance classes:

1. **MHRN observation** — produced by a source-bound experiment or verification artifact.
2. **MHRN interpretation** — inference from MHRN observations; must state limits and cannot be promoted automatically to EVID.
3. **External theory or method** — idea, algorithm, model, benchmark or empirical finding from another source; cite the original source where possible.
4. **MHRN prior work** — material from an earlier MHRN edition, report or public artifact; cite or disclose the earlier version when reused substantially.
5. **AI-assisted wording or synthesis** — assistance is not an authority. Every factual or literature claim must be checked against a citable primary or authoritative source before publication.

## 3. Code attribution

For copied or adapted external code, record:

- upstream project and exact source URL or release/tag,
- license and license-compatible use,
- original file/function or algorithmic source,
- extent of modification,
- date imported,
- responsible reviewer.

A dependency listed in a package manager is not sufficient attribution when project code is copied or adapted from it.

Algorithmic implementations should cite the paper/specification that motivates the mechanism even when the implementation is independently written.

## 4. Text recycling and self-citation

MHRN contains multiple public manuscript editions and addenda. Reuse across those versions is expected during development, but publication-facing reuse must be transparent.

Before external submission:

- disclose the relationship to earlier public editions,
- cite earlier MHRN work when it constitutes prior dissemination,
- avoid presenting reused text, figures, tables or results as newly produced,
- identify duplicated datasets/analyses and distinguish reanalysis from new experiments,
- keep a change note when a paragraph is substantially inherited from an earlier edition.

"Self-plagiarism" rules vary by venue; the project therefore treats undisclosed substantial reuse as an integrity risk rather than relying on a single universal threshold.

## 5. Literature and idea attribution

Related work must distinguish:

- **background**: general context,
- **mechanistic precedent**: a source that directly motivates an implemented mechanism,
- **comparison baseline**: a system or method compared empirically,
- **interpretive precedent**: a theory used to interpret results,
- **unverified lead**: a possibly relevant source that has not yet been verified and must not be cited as settled fact.

Whenever MHRN adopts a mechanism analogous to a published method, the manuscript must state both the precedent and the meaningful implementation differences.

## 6. AI-assisted research safeguards

AI-generated references, titles, DOIs, journal details and performance claims are treated as unverified until checked against a primary/authoritative source. AI-generated prose must not be used to disguise copied source text.

Required checks before publication:

1. resolve each citation to a real source;
2. confirm author, title, year and venue;
3. verify the claimed finding in the source;
4. check that paraphrasing is genuinely independent;
5. ensure direct quotations are explicitly marked and minimal;
6. ensure the cited source actually supports the nearby claim.

## 7. Similarity and plagiarism screening

Repository checks can catch missing attribution files, duplicated local passages and obvious copied code patterns, but they cannot prove originality against the global literature.

Before manuscript submission, perform:

- a reputable text-similarity check accepted by the target institution or venue,
- manual review of every high-similarity passage,
- citation audit for paraphrases and conceptual borrowing,
- code-origin review for imported/adapted code,
- figure/table provenance review.

Commercial tools such as iThenticate/Turnitin may be used if institutionally available; the project does not treat a similarity percentage alone as a plagiarism verdict.

## 8. Scientific claim boundary

No literature citation can substitute for an MHRN experiment. Conversely, an MHRN experiment cannot establish priority over an idea already present in prior literature.

Claims must distinguish:

- implemented,
- technically verified,
- DATA-supported,
- human-reviewed EVID,
- independently replicated.

Only the latter states may justify progressively stronger scientific language, and none of them justify consciousness or biological-equivalence claims automatically.

## 9. Required release artifacts

For any release that changes scientific claims or mechanisms, maintain:

- `research/RELATED_WORK.md`,
- this policy,
- the scientific stage manifest in `src/dashboard/static/scientific-progress.json`,
- source-bound experiment/protocol references,
- a publication/change note if manuscript claims changed.

## 10. Pre-submission checklist

- [ ] Every non-trivial external mechanism has a primary-source citation.
- [ ] Every quantitative external claim has been verified in the cited source.
- [ ] No unverified AI-generated citation remains.
- [ ] Reused MHRN text/results are disclosed and cross-referenced.
- [ ] Copied/adapted code has source and license provenance.
- [ ] Figures and tables have explicit provenance.
- [ ] Similarity screening completed and manually reviewed.
- [ ] DATA and EVID are not conflated.
- [ ] Negative/null results remain visible.
- [ ] Release wording matches the actual scientific maturity stage.

## 11. Non-guarantee statement

Passing these controls means that documented integrity checks were completed. It does **not** mean that criticism is impossible or that plagiarism has been mathematically excluded. Scientific criticism remains part of the process; the project goal is to make claims traceable, bounded, falsifiable and properly attributed.
