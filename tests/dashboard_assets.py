"""Read the actual static stylesheet graph used by the canonical dashboard."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

STATIC = Path(__file__).resolve().parents[1] / "src" / "dashboard" / "static"


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "link" and attributes.get("rel") == "stylesheet":
            href = attributes.get("href")
            if href:
                self.hrefs.append(href)


def stylesheet_paths() -> tuple[Path, ...]:
    parser = _Links()
    parser.feed((STATIC / "index.html").read_text(encoding="utf-8"))
    seen: set[Path] = set()
    ordered: list[Path] = []

    def visit(href: str, parent: Path) -> None:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            raise AssertionError("The dashboard stylesheet must be local: " + href)
        path = (
            STATIC / url.path.lstrip("/")
            if url.path.startswith("/")
            else parent / url.path
        ).resolve()
        path.relative_to(STATIC)
        if path in seen:
            return
        assert path.is_file(), f"Loaded stylesheet is missing: {path}"
        seen.add(path)
        ordered.append(path)
        text = path.read_text(encoding="utf-8")
        for imported in re.findall(r'@import\s+(?:url\(\s*)?["\']([^"\']+)["\']', text):
            visit(imported, path.parent)

    for href in parser.hrefs:
        visit(href, STATIC)
    return tuple(ordered)


def dashboard_css() -> str:
    text = "\n".join(path.read_text(encoding="utf-8") for path in stylesheet_paths())
    return re.sub(r"([;{(]\s*[-\w]+):\s*", r"\1: ", text)


def compact_css(text: str | None = None) -> str:
    return re.sub(r"\s+", "", dashboard_css() if text is None else text)
