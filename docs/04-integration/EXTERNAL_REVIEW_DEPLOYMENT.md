# External Review Deployment

**Status:** deployment design for the isolated review portal  
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

The existing workflow `.github/workflows/review-portal.yml` verifies the portal and publishes only `src/dashboard/static/review` when Pages is enabled. Start it manually with `publish_pages: true`, or set the repository variable `MHRN_REVIEW_PAGES_ENABLED=true`.

This mode has no central response storage. Participants export their JSON/CSV locally. The export is not automatically sent anywhere.

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
