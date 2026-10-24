# Prior-art assessment of the methodology claims

2026-10-24. **AI-assisted source review; independent external review PENDING.**
The assistant preparing this review also changed repository methods and
documentation. It is not an independent reviewer. No external person has
been contacted or represented as having approved this assessment.

## Search and inclusion record

Web search on 2026-10-24, queries: “research provenance W3C PROV
recommendation 2013 executable paper computational reproducibility Knuth
1984 literate programming”; “Nosek 2018 preregistration revolution reflexivity
scientific research positionality Finlay 2002”; “eLife executable research
2020”; “Jupyter Notebooks 2016 Kluyver”; “site.cos.io registered reports peer
review before results”. Included original standards, author publications,
institutional author deposits and publisher descriptions directly addressing
one of the four claims. General blog summaries and search aggregators were
excluded. This is a targeted scoping review, not an exhaustive systematic
search or a patent novelty opinion. Ranking, language and database coverage
can omit relevant work; absence from this table is not absence of prior art.

## Claim-to-source comparison

| MHRN claim family | Prior art and verified scope | Consequence for novelty |
| --- | --- | --- |
| Research provenance | [W3C PROV-DM (2013)](https://www.w3.org/TR/prov-dm/) models entities, activities, agents and derivation. | Recording origins and transformations is established. MHRN's hashes, DATA/EVID distinctions and domain-specific gates are implementation choices; they do not invent provenance. No formal PROV interoperability has been demonstrated here. |
| Preregistration | [Nosek et al. (2018)](https://pmc.ncbi.nlm.nih.gov/articles/5856500/) distinguish prospective predictions/analysis plans from postdiction. [COS Registered Reports](https://www.cos.io/initiatives/registered-reports) describes review before data collection. | Frozen plans and separating exploratory from confirmatory work are established. A local Git freeze is not independent registry deposit or a journal's in-principle acceptance. |
| Executable publication | [Knuth's author account of literate programming](https://cs.stanford.edu/~knuth/lp.html) combines program and documentation; [Kluyver et al. (2016)](https://escholarship.org/uc/item/08b3d4s2) presents notebooks as reproducible-workflow publication; [eLife's ERA launch (2020)](https://elifesciences.org/for-the-press/eb096af1/elife-launches-executable-research-articles-for-publishing-computationally-reproducible-results) embeds executable code and outputs. | Linking narrative, code and results is not new. MHRN's source-bound publication pipeline is a project-specific realization; an exportable manuscript or artifact link alone is not an in-browser executable article. |
| Reflexive methodology | [Finlay (2002)](https://doi.org/10.1177/146879410200200205) discusses several forms of researcher reflexivity and their difficulties. Only the publisher's abstract and accessible page were inspected. | Documenting researcher influence, choices and limitations has substantial antecedents. AI participation adds a context needing evaluation, not an automatic claim of a new epistemology. |
| Independent verification | [COS TOP Guidelines](https://www.cos.io/initiatives/top-guidelines) distinguishes verification by an independent party, reproducibility and replication. | Passing local checks or reusing a different software implementation does not by itself establish independent replication. |

All descriptions above are paraphrases. The Knuth original journal DOI
`10.1093/comjnl/27.2.97` was identified, but its full publisher page could not
be retrieved; the author's accessible overview is used for the limited claim.
No inaccessible full text is presented as read.

## Assessment of the actual manuscript claim

Edition 1.8, `parts/10_synthesis.md`, locates the project's contribution in
integration of research software engineering and governance: RQ/H registry,
preregistration, source-bound DATA, human review, EVID status, provenance,
test adequacy and viewer. That modest integration claim is more defensible
than claiming invention of any component. It remains a description of work
performed, not proof that its combination is unprecedented or improves
scientific quality compared with existing workflows.

Recommended wording for subsequent editions:

> MHRN implements a domain-specific integration of established provenance,
> preregistration, reproducible-computation and reflexive-documentation
> practices. Its contribution is the explicit implementation and audit of
> these practices in this evolving SNN programme. Priority of the combination
> and comparative gains in research quality have not been established.

This recommendation does not silently rewrite an already published edition.
To establish a stronger claim, compare MHRN against established workflow and
publication systems on predefined capabilities and failure cases. Include
maintenance cost, usability, audit error rates and negative outcomes; a
feature inventory alone is not a causal evaluation of governance quality.

## External review handoff

An independent reviewer should disclose involvement/conflicts, expand the
search beyond these starting sources, inspect actual implementation and
manuscript passages, distinguish conceptual antecedents from engineering
differences, and return a dated signed assessment with cited counterexamples.
Acceptance requires a review artifact, reviewer identity/role, search scope,
claim-by-claim decisions and explicit unresolved limitations. Until then the
TODO's independence requirement remains open; this preparation is complete.
