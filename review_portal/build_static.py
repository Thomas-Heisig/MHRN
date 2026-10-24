"""Package only public questionnaire assets, with online collection disabled."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/dashboard/static/review"
FILES = ("index.html", "app.js", "model.js", "instrument.js", "review.css")


def build(output: Path) -> dict[str, object]:
    """Create a new directory; never publish admin pages, secrets or response data."""
    contents = {name: (SOURCE / name).read_bytes() for name in FILES}
    html = contents["index.html"].decode("utf-8")
    html = html.replace('<html lang="de">', '<html lang="de" data-review-mode="export-only">')
    html = html.replace('="/review/', '="./')
    html = html.replace("connect-src 'self'", "connect-src 'none'")
    html = html.replace(
        '<a href="./admin.html">Erhebungsverwaltung</a>',
        '<a href="./privacy.html">Datenschutz und Exportmodus</a>',
    )
    if 'data-review-mode="export-only"' not in html or "admin.html" in html:
        raise ValueError("Static export contract changed; inspect the source HTML")
    contents["index.html"] = html.encode("utf-8")
    contents["review.css"] += (
        b'\nhtml[data-review-mode="export-only"] .withdrawal { display: none; }\n'
    )
    contents["privacy.html"] = (ROOT / "review_portal/privacy-export.html").read_bytes()
    contents[".nojekyll"] = b""
    manifest = {
        "mode": "export-only",
        "collection_enabled": False,
        "files_sha256": {
            name: hashlib.sha256(data).hexdigest() for name, data in contents.items()
        },
        "independent_review": "not_asserted",
    }
    output.mkdir(parents=True, exist_ok=False)
    for name, data in contents.items():
        (output / name).write_bytes(data)
    (output / "deployment-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.output), indent=2))


if __name__ == "__main__":
    main()
