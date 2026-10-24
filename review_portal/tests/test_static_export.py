"""Static deployment must remain portable and unable to collect responses."""

import hashlib
import json

import pytest

from review_portal.build_static import FILES, build


def test_only_export_assets_are_packaged(tmp_path):
    output = tmp_path / "MHRN"
    result = build(output)
    assert set(p.name for p in output.iterdir()) == set(FILES) | {
        "privacy.html", ".nojekyll", "deployment-manifest.json"
    }
    html = (output / "index.html").read_text(encoding="utf-8")
    assert 'data-review-mode="export-only"' in html
    assert "connect-src 'none'" in html
    assert '="/review/' not in html
    assert "admin.html" not in html
    assert result["collection_enabled"] is False
    stored = json.loads((output / "deployment-manifest.json").read_text())
    for name, digest in stored["files_sha256"].items():
        assert hashlib.sha256((output / name).read_bytes()).hexdigest() == digest


def test_existing_directory_is_never_published_or_overwritten(tmp_path):
    (tmp_path / "private-response.json").write_text("private")
    with pytest.raises(FileExistsError):
        build(tmp_path)
    assert list(tmp_path.iterdir()) == [tmp_path / "private-response.json"]
