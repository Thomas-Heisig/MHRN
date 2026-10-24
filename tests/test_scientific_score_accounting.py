from copy import deepcopy

from scripts import check_scientific_maturity_integrity as checker


def test_maturity_checker_rejects_unexplained_score(monkeypatch, capsys):
    original = checker.load_json

    def changed(path):
        value = deepcopy(original(path))
        if path.endswith("scientific-progress.json"):
            value["stages"][2]["score"] = 0.123
        return value

    monkeypatch.setattr(checker, "load_json", changed)
    assert checker.main() == 1
    assert "score does not match weighted criteria" in capsys.readouterr().out


def test_maturity_checker_rejects_duplicate_criterion(monkeypatch, capsys):
    original = checker.load_json

    def changed(path):
        value = deepcopy(original(path))
        if path.endswith("scientific-progress.json"):
            value["stages"][0]["criteria"].append(value["stages"][0]["criteria"][0])
        return value

    monkeypatch.setattr(checker, "load_json", changed)
    assert checker.main() == 1
    assert "each weighted criterion once" in capsys.readouterr().out
