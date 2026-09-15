import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "src" / "dashboard" / "static"
MODULES = STATIC / "frontend" / "modules"
STYLES = STATIC / "frontend" / "styles"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_publication_uses_one_shared_speech_reader() -> None:
    speech = _read(STATIC / "speech-reader.js")
    scholar = _read(MODULES / "publication-scholar-tools.js")
    bootstrap = _read(MODULES / "publication-scholar-bootstrap.js")
    renderer = _read(STATIC / "file-renderer.js")
    chat = _read(STATIC / "research-chat.js")

    assert 'from "../../speech-reader.js"' in scholar
    assert "createSpeechControls" in scholar
    assert "createSpeechControls" in renderer
    assert "createSpeechControls" in chat
    assert "SpeechSynthesisUtterance" in speech
    assert "SpeechSynthesisUtterance" not in scholar
    assert "canonicalMount.replaceChildren(enhancedControls)" in bootstrap
    assert "enhancedMount.remove()" in bootstrap


def test_shared_speech_reader_is_bilingual_and_prefers_natural_voices() -> None:
    speech = _read(STATIC / "speech-reader.js")

    expected = {
        "de": {"katja", "conrad"},
        "en": {"jenny", "aria", "guy", "ryan", "sonia"},
    }
    for language, required in expected.items():
        match = re.search(rf"\b{language}:\s*(\[[^\]]*\])", speech)
        assert match is not None
        assert required.issubset(json.loads(match.group(1)))
    assert "detectSpeechLanguage" in speech
    assert "chooseSpeechVoice" in speech
    assert "Natural".lower() in speech.lower()
    assert "voiceschanged" in speech


def test_publication_restores_late_windows_and_microsoft_voices() -> None:
    bootstrap = _read(MODULES / "publication-scholar-bootstrap.js")
    refinements = _read(STYLES / "publication-reader-voice-math.css")

    assert "WINDOWS_VOICE_HINTS" in bootstrap
    assert "microsoft" in bootstrap.lower()
    assert "refreshPublicationVoiceSelectors" in bootstrap
    assert "voiceschanged" in bootstrap
    assert "Stimmen neu laden" in bootstrap
    assert "[180, 700, 1800, 3500]" in bootstrap
    assert "width: min(680px" in refinements
    assert ".speech-reader-options-panel select" in refinements
    assert "width: 100%" in refinements


def test_publication_scholar_reader_has_persistent_navigation_and_reading_flow() -> None:
    scholar = _read(MODULES / "publication-scholar-tools.js")
    layout = _read(STYLES / "publication-reader.css")

    assert "pub-scholar-chapters" in scholar
    assert "pub-scholar-chapter-list" in scholar
    assert "pub-reader-bottom-nav" in scholar
    assert 'data-direction="next"' in scholar
    assert "pub-reader-toc" in scholar
    assert "Vollbreite" in scholar
    assert "aside.pub-reader-toc" in layout
    assert "position: sticky" in layout
    assert "max-width: none" in layout


def test_read_aloud_tracks_and_scrolls_current_text() -> None:
    scholar = _read(MODULES / "publication-scholar-tools.js")

    assert "pub-speech-active" in scholar
    assert 'scrollIntoView({ behavior: "smooth", block: "center" })' in scholar
    assert "getSegments" in scholar
    assert "speechSegments(article)" in scholar


def test_publication_formulas_use_shared_mathjax_renderer() -> None:
    formula = _read(STATIC / "formula-renderer.js")
    refinements = _read(STYLES / "publication-reader-voice-math.css")

    assert 'MATH_ROOT_SELECTOR = ".fm-markdown, .pub-reader-article"' in formula
    assert 'processHtmlClass: "fm-markdown|pub-reader-article"' in formula
    assert "mathJax.typesetPromise(roots)" in formula
    assert 'mjx-container[display="true"]' in refinements
    assert ".pub-reader-article mjx-container" in refinements


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


def test_reader_normalizes_explicit_markdown_anchors_without_enabling_raw_html() -> None:
    polish = _read(MODULES / "publication-reader-polish.js")
    frontend = _read(STATIC / "frontend" / "index.js")
    styles = _read(STYLES / "publication-reader-polish.css")

    assert "RAW_MARKUP_PATTERN" in polish
    assert "pub-explicit-anchor" in polish
    assert "dataset.pubExplicitAnchor" in polish
    assert 'createElement("span")' in polish
    assert "innerHTML =" not in polish
    assert "initPublicationReaderPolish();" in frontend
    assert ".pub-explicit-anchor" in styles
    assert "scroll-margin-top" in styles


def test_ask_ai_selection_assistant_is_relocated_outside_contained_reader() -> None:
    polish = _read(MODULES / "publication-reader-polish.js")
    styles = _read(STYLES / "publication-reader-polish.css")
    index_css = _read(STYLES / "index.css")

    assert "panel.append(assistant)" in polish
    assert 'assistant.dataset.floatingSelectionAssistant = "true"' in polish
    assert '> .pub-selection-assistant[data-floating-selection-assistant="true"]' in styles
    assert "position: fixed !important" in styles
    assert "top: calc(var(--pub-app-offset" in styles
    assert "[hidden]" in styles
    assert "display: none !important" in styles
    assert "[data-pub-selection-ai]:hover" in styles
    assert index_css.rstrip().endswith('@import url("./publication-reader-polish.css");')


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

    assert (
        'import { initPublicationScholarTools } from "./modules/publication-scholar-bootstrap.js";'
        in frontend
    )
    assert (
        'import { initPublicationReaderPolish } from "./modules/publication-reader-polish.js";'
        in frontend
    )
    assert frontend.index("initPublicationPanel();") < frontend.index(
        "initPublicationScholarTools();"
    ) < frontend.index("initPublicationReaderPolish();")


def test_reader_layout_is_scoped_and_resets_nested_main_sidebar_offset() -> None:
    layout = _read(STYLES / "publication-reader.css")
    index_css = _read(STYLES / "index.css")

    assert "#tab-publication #publication-panel main.pub-reader-document" in layout
    assert "margin: 0 !important" in layout
    assert "width: 100% !important" in layout
    assert "grid-template-columns: var(--pub-rail-width) minmax(0, 1fr)" in layout
    assert "--pub-reader-gap: 0px" in layout
    assert '@import url("./publication-reader.css");' in index_css
    assert '@import url("./publication-reader-voice-math.css");' in index_css
    assert index_css.index("publication-reader.css") < index_css.index(
        "publication-reader-voice-math.css"
    ) < index_css.index("publication-reader-polish.css")


def test_reader_has_one_sticky_chrome_layer_and_contiguous_document_geometry() -> None:
    layout = _read(STYLES / "publication-reader.css")

    assert ".pub-reader-hero" in layout
    assert "position: relative" in layout
    assert ".pub-reader-toolbar" in layout
    assert "position: sticky" in layout
    assert "column-gap: var(--pub-reader-gap)" in layout
    assert "backdrop-filter: none" in layout


def test_scholar_bootstrap_does_not_watch_entire_reader_subtree() -> None:
    bootstrap = _read(MODULES / "publication-scholar-bootstrap.js")

    assert "observer.observe(container, { childList: true });" in bootstrap
    assert "subtree: true" not in bootstrap
    assert "requestAnimationFrame(() => void enhance())" in bootstrap
    assert 'cache: "no-cache"' in bootstrap
