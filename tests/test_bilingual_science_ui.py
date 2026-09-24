from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_frontend_language_controller_defaults_to_english() -> None:
    index = (ROOT / "src/dashboard/static/index.html").read_text(encoding="utf-8")
    frontend = (ROOT / "src/dashboard/static/frontend/index.js").read_text(
        encoding="utf-8"
    )
    i18n = (ROOT / "src/dashboard/static/frontend/core/i18n.js").read_text(
        encoding="utf-8"
    )

    assert '<html lang="en">' in index
    assert 'import { initI18n } from "./core/i18n.js' in frontend
    assert "initI18n();" in frontend
    assert 'const DEFAULT_LANGUAGE = "en";' in i18n
    assert '"mhrn-ui-language-v1"' in i18n
    assert 'data-mhrn-language="en"' in i18n
    assert 'data-mhrn-language="de"' in i18n
    assert '"mhrn:language-change"' in i18n
    assert (
        'const startsWithWord = /^[\\p{L}\\p{N}_]/u.test(from);' in i18n
    )
    assert (
        'const endsWithWord = /[\\p{L}\\p{N}_]$/u.test(from);' in i18n
    )


def test_current_publication_declares_language_provenance() -> None:
    catalog = json.loads(
        (ROOT / "research/publications/catalog.json").read_text(encoding="utf-8")
    )
    current = next(
        item
        for item in catalog["publications"]
        if item["id"] == catalog["current_publication_id"]
    )

    assert current["ui_default_language"] == "en"
    assert current["content_language"] == "de"
    assert current["subtitle"].startswith("Rekursive Epistemik")
    assert current["english_translation"].endswith("/translations/en/MANUSCRIPT.md")
    assert "canonical source language" in current["language_policy"]


def test_publication_reader_never_promotes_translation_to_evidence() -> None:
    reader = (
        ROOT / "src/dashboard/static/frontend/modules/publication-reader.js"
    ).read_text(encoding="utf-8")
    server = (ROOT / "src/dashboard/server.py").read_text(encoding="utf-8")
    i18n = (ROOT / "src/dashboard/static/frontend/core/i18n.js").read_text(
        encoding="utf-8"
    )

    assert "?lang=${encodeURIComponent(getLanguage())}" in reader
    assert "publication.translation.source" in reader
    assert "pending human language review" in i18n
    assert '"translation_fallback"' in server
    assert '"source_entrypoint_path"' in server
    assert '"language_variants"' in server
