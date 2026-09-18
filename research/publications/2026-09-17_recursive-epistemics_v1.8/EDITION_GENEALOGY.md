# Edition- und Working-Branch-Genealogie — Edition 1.8

**Zweck:** Historischer Kontext vor der Repository-Bereinigung.  
**Audit-Basis:** `main@774671bcff753489f833b50bbdd3bea7ab3e3169` am 18. September 2026.  
**Maschinenlesbare Editionslinie:** [`registers/edition_genealogy.json`](registers/edition_genealogy.json).

Branch-Namen sind mutable Arbeitsreferenzen und keine wissenschaftlichen Identifikatoren. Für Zitation und Reproduktion sind Commit-SHAs, Editionspfade, Manifeste und frozen Artefakte maßgeblich.

## Dokumentierte Arbeitsbranches

| Branch | Historischer Tip-SHA | Verhältnis zur Audit-Basis `main` | Einordnung |
| --- | --- | --- | --- |
| `docs/edition-1-8-corpus-integration` | `633a16e15db9c2a4f4754a440a947bad8f1ebee8` | Branch-only: 0; main-only seit Tip: 74 | Tip ist Vorfahr von main; Corpus-Integration in main enthalten. |
| `docs/edition-1-8-current-reviews-20260918` | `7d5ca56a5deb19b16e1eccc91f0746b783160750` | Branch-only: 0; main-only seit Tip: 59 | Tip ist Vorfahr von main; Review-Fortschreibung in main enthalten. |
| `docs/edition-1-8-current-state-20260918` | `9f167c5b301191209228f18484a4ad7630b3e2a5` | Branch-only: 0; main-only seit Tip: 53 | Tip ist Vorfahr von main; Current-State-Arbeit in main enthalten. |
| `feat/publication-reader-complete-v18-20260918` | `87f1364c558bdf8eb7824a319c22ed53a103479d` | Branch-only: 0; main-only seit Tip: 38 | Tip ist Vorfahr von main; Reader-/Viewer-Arbeit in main enthalten. |
| `fix/learning-prep-provenance-ui-20260917` | `426cc5a6642281d6221d70555d4043c9701735b5` | Branch-only: 0; main-only seit Tip: 100 | Tip ist Vorfahr von main; Provenienz-/UI-Arbeit in main enthalten. |
| `research/edition18-reader-paths-offshoots-20260918` | `29aadee2b796117a88ee8cfaf7d9ee2b509fe7f7` | Branch-only: 0; main-only seit Tip: 2 | Tip ist Vorfahr von main; Reader-Pfade und Paper-Offshoots in main enthalten. |
| `fix/publication-18-consistency-20260918` | `87d0260e56dd9306590a4b8d929b881f8dd6f0c8` | Graphhistorie nach Squash-Merge divergiert | PR #136 wurde in `774671bcff753489f833b50bbdd3bea7ab3e3169` gemergt. Der Branch-Tip ist wegen Squash-/Rematerialisierungs-Historie kein direkter Vorfahr; sein Kontext bleibt über PR #136, Tip-SHA und Merge-Commit erhalten. |

## Löschregel

Ein Branch darf nach dieser Dokumentation entfernt werden, wenn:

1. sein relevanter Inhalt in `main` enthalten oder durch einen gemergten PR nachvollziehbar repräsentiert ist;
2. Tip-SHA und fachlicher Zweck hier dokumentiert sind;
3. keine frozen Publikation oder DATA/EVID-Provenienz den Branch-Namen als alleinigen Identifikator verwendet.

Die Branch-Löschung entfernt nur die mutable Referenz. Die referenzierten Commits/PRs und die in `main` materialisierten Inhalte bleiben die maßgebliche Provenienz, solange sie durch die Repository-Historie erreichbar sind.
