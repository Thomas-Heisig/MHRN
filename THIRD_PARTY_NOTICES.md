# Third-Party Software Notices

MHRN itself is licensed under the MIT License. Third-party dependencies retain
their own licenses. This file records research-relevant dependencies whose
license and attribution should remain visible in releases and publications.

## Brian 2

- **Project:** Brian 2
- **Upstream:** Brian team
- **Use in MHRN:** external reference simulator for neuron-model conformance and
  the Stage-1 cross-implementation reference-replication programme
- **Pinned reference version:** 2.10.1 where explicitly declared by the
  preregistered workflow
- **License:** CeCILL 2.1
- **Upstream repository:** https://github.com/brian-team/brian2
- **License information:** https://github.com/brian-team/brian2/blob/master/LICENSE

Brian 2 is installed as an external Python dependency for the relevant
reference workflows; its source code is not relicensed under the MHRN MIT
License.

If a future MHRN distribution bundles or redistributes Brian 2 itself rather
than installing it as a separate dependency, that distribution must preserve
the applicable Brian 2 copyright/license notices and include the CeCILL 2.1
license material required by the upstream license.

### Scientific citation

The Brian project explicitly asks users of Brian in published research to cite:

> Stimberg, M., Brette, R., & Goodman, D. F. M. (2019). Brian 2, an intuitive
> and efficient neural simulator. *eLife*, 8, e47314.
> https://doi.org/10.7554/eLife.47314

This publication citation is recorded as scientific attribution for research
that uses Brian 2. It is kept distinct from the software-license obligations:
the project citation request does not replace compliance with CeCILL 2.1, and
the CeCILL license does not replace normal scholarly citation.

## Release rule

Before a public release that changes third-party dependencies:

1. confirm the exact dependency version;
2. confirm the upstream license from the authoritative project;
3. preserve required notices for any bundled/redistributed code;
4. update this file if the dependency's role or license changes;
5. ensure research publications cite software used materially in the reported
   experiments where requested or academically appropriate.
