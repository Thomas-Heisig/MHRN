from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_windows_start_wrappers_default_to_trusted_lan_binding() -> None:
    cmd = (ROOT / "start.cmd").read_text(encoding="utf-8")
    powershell = (ROOT / "start.ps1").read_text(encoding="utf-8")

    assert "--host 0.0.0.0" in cmd
    settings = (ROOT / "src" / "dashboard" / "network_settings.py").read_text(
        encoding="utf-8"
    )
    assert "DASHBOARD_LAN_HOST: str = \"0.0.0.0\"" in settings
    assert "DASHBOARD_LAN_HOST; print(DASHBOARD_LAN_HOST)" in powershell


def test_direct_python_entrypoint_remains_loopback_by_default() -> None:
    main = (ROOT / "src" / "main.py").read_text(encoding="utf-8")

    settings = (ROOT / "src" / "dashboard" / "network_settings.py").read_text(
        encoding="utf-8"
    )
    assert "DASHBOARD_HOST: str = \"127.0.0.1\"" in settings
    assert "default=DASHBOARD_HOST" in main
    assert "use 0.0.0.0 for LAN" in main
