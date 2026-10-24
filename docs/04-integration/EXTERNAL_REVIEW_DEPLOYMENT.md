# External Review Deployment

**Status:** export-only GitHub Pages preparation selected on 24 October 2026; no new deployment or independent approval asserted.
**Scope:** public questionnaire, optional online collection and sanitized descriptive export

## Security boundary

The MHRN dashboard (`:8765`) is never published. The external review portal is a separate static site or isolated collector. It has no runtime, file-manager, experiment-runner, EVID-write or research-AI permissions.

```text
GitHub Pages or Hugging Face Space
        |
        v
questionnaire UI
        |
        v (only for configured online collection)
separate review collector
        |
        v
encrypted storage outside Git
```

## Option 1: GitHub Pages, export-only

The workflow `.github/workflows/review-portal.yml` verifies the portal and builds an allowlisted package with `python -m review_portal.build_static --output <new-directory>`. Only this package is uploaded when Pages is enabled. Start publication manually with `publish_pages: true` on `main`; preparation alone does not run this workflow. Avoid enabling the automatic publication variable until the published configuration has been reviewed.

This mode has no central response storage. Participants export their JSON/CSV locally. The export is not automatically sent anywhere.

The prepared package uses relative assets for the project subpath, explicitly disables API discovery and blocks network connections through `connect-src 'none'`. Admin pages and collector files are excluded. A browser test opens `/MHRN/index.html`, exports a synthetic answer and verifies that no API requests occur. The package includes an export-specific privacy page and SHA-256 manifest. Instrument questions, version and reviewed-materials revision remain unchanged.

Local verification on 24 October 2026: 57 Python tests, six JavaScript model tests,
catalogue byte check, workflow YAML check and the static browser scenario passed.
The browser scenario verified the project subpath, a synthetic JSON download,
disabled online controls, privacy page, mobile layout and zero API requests.
These results verify the prepared package, not the deployed site or independent review.

### Selected deployment and acceptance boundaries

| Area | Export-only preparation | Remaining production check |
| --- | --- | --- |
| Address | `https://thomas-heisig.github.io/MHRN/`; no custom domain purchase | Confirm actual Pages URL and whether an existing site would be replaced |
| TLS | GitHub Pages-managed HTTPS | Verify actual certificate and HTTPS enforcement after publication |
| Response storage | Browser memory; optional local draft/export | No central database; users manage their own local files |
| Backups | Rebuild public assets from reviewed Git commit and package hashes | Keep the release commit/package available; no server response-backup claim |
| Study settings | Local review context; central collection disabled | Any future collection requires a separate concrete study configuration |
| Legal/privacy | Export-specific notice with public project contact and GitHub hosting disclosure | Human review of actual deployment and intended use remains open |
| Independent review | Not asserted by technical tests | Record actual reviewer, scope, findings and conflicts before claiming completion |

GitHub reports Pages enabled for this repository, but that is not proof that the prepared package is live. The local GitHub CLI credentials could not be verified; no settings or public site were changed during preparation.

GitHub Pages documents both its project URL structure and security-related visitor IP logging in [About Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages). HTTPS behavior is described in [Securing Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https). Hosting logs are distinct from questionnaire responses. Before central collection, information duties must be assessed against the actual processing; see the [official Article 13 text](https://www.ms.niedersachsen.de/startseite/uber_uns/datenschutzerklaerung-nach-dsgvo-181391.html).

## Option 2: Hugging Face Docker Space

Create a public Docker Space and use `review_portal/Dockerfile.huggingface` as the Space Dockerfile. Configure the Space port as `7860`.

For local/export-only mode, do not configure `MHRN_REVIEW_STUDY`; the portal remains collection-disabled.

For online collection, configure Space Secrets/Variables, never repository files:

```text
MHRN_REVIEW_STUDY=/run/secrets/study.json
MHRN_REVIEW_DATA_DIR=/data
MHRN_REVIEW_KEY_FILE=/run/secrets/encryption.key
MHRN_REVIEW_ADMIN_TOKEN_FILE=/run/secrets/admin.token
```

The study file and key files must be provided through the deployment secret mechanism. Persistent encrypted storage must be explicitly configured and verified; a normal ephemeral Space restart must never be treated as durable data storage.

## Option 3: Separate VPS collector

Use `review_portal/compose.example.yaml` with Caddy from `review_portal/Caddyfile.example`. Bind the collector to `127.0.0.1:8766` and publish only Caddy HTTPS on port 443.

Do not expose:

- MHRN dashboard port `8765`;
- GitHub tokens or repository write credentials to the browser;
- admin tokens in URLs;
- the collector data directory inside the repository.

## Data flow and repository publication

Raw responses never enter the public Git repository. Use the authenticated admin export on the collector and keep that export outside the repository:

```powershell
python scripts/export_external_review_aggregate.py `
  C:\private\mhrn-review\admin-export.json `
  research\generated\external-review-aggregate.json
```

The generated file contains descriptive aggregates only. It excludes answers, notes, names, e-mail addresses, participant codes, signatures, invitation codes and withdrawal tokens. Human privacy/data review is required before committing or publishing the aggregate. The aggregate is not EVID and does not automatically update scientific claims.

A GitHub Action may later validate and publish this sanitized aggregate, but it must not receive raw response exports or write them to a public repository. Prefer a private data repository or external controlled storage for raw exports.

## Required preflight

1. Confirm controller, purpose, contact, retention, backups and legal basis in `study.json`.
2. Bind the study to a reviewed commit and immutable instrument digest.
3. Use HTTPS and verify DNS/TLS.
4. Confirm encryption-key backup and recovery procedure separately.
5. Test invitation, withdrawal and expiry behavior with synthetic records.
6. Confirm admin access is restricted independently of public questionnaire access.
7. Perform a human privacy/security review before enabling `enabled: true`.
