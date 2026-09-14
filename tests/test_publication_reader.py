from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "src" / "dashboard" / "static"


def _read(relative: str) -> str:
    return (STATIC / relative).read_text(encoding="utf-8")


def test_frontend_uses_new_publication_reader() -> None:
    frontend = _read("frontend/index.js")
    assert 'import { initPublicationPanel } from "./modules/publication-reader.js";' in frontend
    assert "publication-panel.js" not in frontend


def test_publication_reader_keeps_markdown_inside_reader() -> None:
    reader = _read("frontend/modules/publication-reader.js")
    assert 'const READER_EXTENSIONS = /\\.(?:md|markdown|txt)$/i;' in reader
    assert 'data-pub-reader-link' in reader
    assert 'openReaderDocument' in reader
    assert '/api/files/preview/' in reader


def test_publication_reader_resolves_cross_root_links_and_files() -> None:
    reader = _read("frontend/modules/publication-reader.js")
    assert 'repoPath.startsWith("research/")' in reader
    assert 'repoPath.startsWith("docs/")' in reader
    assert 'REPOSITORY_BLOB_ROOT' in reader
    assert 'data-pub-file' in reader
    assert 'window.openBrain5DFile' in reader


def test_publication_reader_has_navigation_search_toc_and_accessible_states() -> None:
    reader = _read("frontend/modules/publication-reader.js")
    for token in (
        'data-pub-action="back"',
        'data-pub-action="forward"',
        'id="pub-reader-search"',
        'class="pub-reader-toc"',
        'role="status"',
        'aria-live="polite"',
        'data-pub-heading',
    ):
        assert token in reader
