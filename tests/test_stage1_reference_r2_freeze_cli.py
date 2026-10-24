"""A freeze must have an explicit valid date and a clean source tree."""

import sys

import pytest

from scripts import freeze_stage1_topology_reference_r2 as freeze


@pytest.mark.parametrize("args", [[], ["--freeze-date", "invalid"]])
def test_freeze_rejects_missing_or_invalid_date(monkeypatch, tmp_path, args):
    target = tmp_path / "freeze.json"
    monkeypatch.setattr(freeze, "F", target)
    monkeypatch.setattr(sys, "argv", ["freeze", *args])
    with pytest.raises(SystemExit) as error:
        freeze.main()
    assert error.value.code == 2
    assert not target.exists()


def test_valid_date_does_not_bypass_clean_tree(monkeypatch, tmp_path):
    target = tmp_path / "freeze.json"
    monkeypatch.setattr(freeze, "F", target)
    monkeypatch.setattr(freeze, "git", lambda *args: " M source.py")
    monkeypatch.setattr(sys, "argv", ["freeze", "--freeze-date", "2026-10-24"])
    with pytest.raises(RuntimeError, match="clean tree"):
        freeze.main()
    assert not target.exists()
