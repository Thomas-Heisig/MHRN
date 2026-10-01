"""Central network settings for the MHRN dashboard.

All components (launcher, server, start scripts, Hugging Face config)
read their default host, port and LAN policy from this single module.
Change values here to reconfigure the entire stack.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Dashboard HTTP server
# ---------------------------------------------------------------------------

DASHBOARD_HOST: str = "127.0.0.1"
"""Default bind address for the dashboard HTTP server.

- ``127.0.0.1`` — loopback only, safe for single-user local access.
- ``0.0.0.0`` — all interfaces; required for LAN/Intranet access.
  Only use on trusted networks; the dashboard has no built-in
  authentication layer.
"""

DASHBOARD_PORT: int = 8767
"""Default TCP port for the dashboard HTTP server."""

# ---------------------------------------------------------------------------
# Public / Internet policy
# ---------------------------------------------------------------------------

ALLOW_PUBLIC_DEPLOYMENT: bool = False
"""Whether the dashboard is allowed to bind to a public interface.

Set this to ``True`` only when a proper reverse proxy, TLS, authentication,
logging and privacy notice are in place. The dashboard exposes operator,
research and file-management endpoints without built-in access control.
"""

PUBLIC_DEPLOYMENT_NOTE: str = (
    "The dashboard exposes operator, research and file-management capabilities. "
    "Do not expose it directly to the public Internet. For trusted-LAN use, "
    f"restrict TCP port {DASHBOARD_PORT} to the intended private network."
)
"""Safety note displayed in the README and referenced in deployment docs."""

# ---------------------------------------------------------------------------
# Hugging Face Space
# ---------------------------------------------------------------------------

HF_SPACE_PORT: int = DASHBOARD_PORT
"""Port used inside the Hugging Face Docker Space (must match EXPOSE)."""

HF_SPACE_HOST: str = "0.0.0.0"  # nosec B104 - required container bind for HF Spaces
"""Host used inside the Hugging Face Space container."""

# ---------------------------------------------------------------------------
# Convenience accessors
# ---------------------------------------------------------------------------


def dashboard_local_url() -> str:
    """Return the loopback URL of the dashboard."""
    return f"http://127.0.0.1:{DASHBOARD_PORT}"


def dashboard_bind_spec() -> str:
    """Return the ``host:port`` string used for bind / firewall docs."""
    return f"{DASHBOARD_HOST}:{DASHBOARD_PORT}"
