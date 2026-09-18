from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "src" / "dashboard" / "static"


def _read(relative: str) -> str:
    return (STATIC / relative).read_text(encoding="utf-8")


def test_frontend_uses_new_publication_reader() -> None:
    frontend = _read("frontend/index.js")
    assert (
        'import { initPublicationPanel } from "./modules/publication-reader.js";'
        in frontend
    )
    assert "publication-panel.js" not in frontend


def test_publication_reader_keeps_markdown_inside_reader() -> None:
    reader = _read("frontend/modules/publication-reader.js")
    assert "const READER_EXTENSIONS = /\\.(?:md|markdown|txt)$/i;" in reader
    assert "data-pub-reader-link" in reader
    assert "openReaderDocument" in reader
    assert "/api/files/preview/" in reader


def test_publication_reader_resolves_cross_root_links_and_files() -> None:
    reader = _read("frontend/modules/publication-reader.js")
    assert 'repoPath.startsWith("research/")' in reader
    assert 'repoPath.startsWith("docs/")' in reader
    assert "REPOSITORY_BLOB_ROOT" in reader
    assert "data-pub-file" in reader
    assert "window.openBrain5DFile" in reader


def test_publication_reader_has_navigation_search_toc_and_accessible_states() -> None:
    reader = _read("frontend/modules/publication-reader.js")
    for token in (
        'data-pub-action="back"',
        'data-pub-action="forward"',
        'id="pub-reader-search"',
        'class="pub-reader-toc"',
        'role="status"',
        'aria-live="polite"',
        "data-pub-heading",
    ):
        assert token in reader


def test_publication_reader_uses_canonical_entrypoint_and_complete_document_map() -> None:
    reader = _read("frontend/modules/publication-reader.js")
    server = (ROOT / "src" / "dashboard" / "server.py").read_text(encoding="utf-8")

    assert "data.entrypoint_path || data.readme_path" in reader
    assert "renderPublicationLibrary(data, view)" in reader
    assert '"Kapitel"' in reader
    assert '"Anhänge & Register"' in reader
    assert '"Editionen"' in reader
    assert '"chapters": cast(JSONValue, chapters)' in server
    assert '"attachments": cast(JSONValue, attachments)' in server
    assert '"history": cast(JSONValue, history)' in server
    assert '"documents": cast(JSONValue, documents)' in server
    assert "current_publication_id" in server
    assert "entrypoint_rel" in server


def test_publication_reader_shows_title_author_date_and_edition_metadata() -> None:
    reader = _read("frontend/modules/publication-reader.js")

    for token in (
        "data.document_title",
        "data.title",
        "data.author",
        "data.date",
        "data.edition",
        "pub-reader-catalog-title",
    ):
        assert token in reader
