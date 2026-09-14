from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "src" / "dashboard" / "static"
MODULES = STATIC / "frontend" / "modules"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_publication_uses_one_shared_speech_reader() -> None:
    speech = _read(STATIC / "speech-reader.js")
    scholar = _read(MODULES / "publication-scholar-tools.js")
    renderer = _read(STATIC / "file-renderer.js")
    chat = _read(STATIC / "research-chat.js")

    assert 'from "../../speech-reader.js"' in scholar
    assert "createSpeechControls" in scholar
    assert "createSpeechControls" in renderer
    assert "createSpeechControls" in chat
    assert "SpeechSynthesisUtterance" in speech
    assert "SpeechSynthesisUtterance" not in scholar


def test_shared_speech_reader_is_bilingual_and_prefers_natural_voices() -> None:
    speech = _read(STATIC / "speech-reader.js")

    assert 'de: ["katja", "conrad"]' in speech
    assert 'en: ["jenny", "aria", "guy", "ryan", "sonia"]' in speech
    assert "detectSpeechLanguage" in speech
    assert "chooseSpeechVoice" in speech
    assert "Natural".lower() in speech.lower()
    assert "voiceschanged" in speech


def test_publication_scholar_reader_has_persistent_navigation_and_reading_flow() -> None:
    scholar = _read(MODULES / "publication-scholar-tools.js")

    assert "pub-scholar-chapters" in scholar
    assert "pub-scholar-chapter-list" in scholar
    assert "pub-reader-bottom-nav" in scholar
    assert 'data-direction="next"' in scholar
    assert "pub-reader-toc" in scholar
    assert "position: sticky" in scholar
    assert "max-width: none" in scholar
    assert "Vollbreite" in scholar


def test_read_aloud_tracks_and_scrolls_current_text() -> None:
    scholar = _read(MODULES / "publication-scholar-tools.js")

    assert "pub-speech-active" in scholar
    assert 'scrollIntoView({ behavior: "smooth", block: "center" })' in scholar
    assert "getSegments" in scholar
    assert "speechSegments(article)" in scholar


def test_selected_dissertation_text_can_be_sent_to_existing_research_ai() -> None:
    scholar = _read(MODULES / "publication-scholar-tools.js")
    bootstrap = _read(MODULES / "publication-scholar-bootstrap.js")

    assert "brain5d:ask-ai" in scholar
    assert "Markierter Text" in scholar
    assert "DATA/EVIDENCE" in scholar
    assert "brain5d:ask-ai" in bootstrap
    assert "research-chat-input" in bootstrap
    assert "research-chat-form" in bootstrap
    assert "requestSubmit" in bootstrap


def test_file_viewer_bridge_uses_public_workspace_router_contract() -> None:
    bootstrap = _read(MODULES / "publication-scholar-bootstrap.js")

    assert "MHRNWorkspaceArchitecture" in bootstrap
    assert 'selectRoute?.("files", "browse")' in bootstrap
    assert "openBrain5DFile" in bootstrap
    assert "window.selectRoute" not in bootstrap


def test_easy_language_is_reserved_as_separate_future_mode() -> None:
    scholar = _read(MODULES / "publication-scholar-tools.js")

    assert "Leichte Sprache" in scholar
    assert "noch nicht veröffentlicht" in scholar
    assert "disabled" in scholar


def test_frontend_initializes_scholar_tools_after_publication_reader() -> None:
    frontend = _read(STATIC / "frontend" / "index.js")

    assert 'import { initPublicationScholarTools } from "./modules/publication-scholar-bootstrap.js";' in frontend
    assert frontend.index("initPublicationPanel();") < frontend.index("initPublicationScholarTools();")
