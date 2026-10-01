"""Real integration status for the MHRN Alpha.5 gate.

This module computes the real integration status of every dashboard
subsystem by probing live backend components. It replaces the previous
frontend-only heuristic that hardcoded ``int-tests`` to ``false``.

Status values (Phase 14):
    passed    — component is connected and active
    disabled  — component is intentionally disabled by config
    pending   — component exists but is not yet initialised
    stale     — component data is outdated (e.g. test baseline)
    failed    — component should be available but is not

A component disabled by config is NEVER reported as "failed".
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from src.dashboard.models import JSONValue
from src.dashboard.verification import (
    compute_source_tree_digest,
    current_git_head,
    evaluate_test_baseline,
)

# ============================================================================
# Scientifically relevant source paths
# ============================================================================

# A test-baseline change (this file, docs, CHANGELOG) must NOT invalidate the
# test status. Only changes to the scientifically relevant source tree should
# mark the baseline as stale. This is why we digest the tree, not the commit.
# The canonical list lives in verification.py; this alias is kept for
# backward compatibility with any code that imported the constant directly.
_SCIENTIFIC_PATHS = [
    "src/",
    "configs/",
    "research/schemas/",
    "pyproject.toml",
    "tests/",
]  # noqa: F841

# ============================================================================
# Status constants
# ============================================================================

PASSED = "passed"
DISABLED = "disabled"
PENDING = "pending"
STALE = "stale"
FAILED = "failed"

_VALID_STATUSES = {PASSED, DISABLED, PENDING, STALE, FAILED}  # noqa: F841


# ============================================================================
# Integration status builder
# ============================================================================


class IntegrationStatusBuilder:
    """Compute real integration status from live backend components.

    The builder is constructed with the live dashboard state snapshot and
    optional handles to the operator bridge, heatmap source, research
    source, and the repository root (for test_baseline.json).
    """

    def __init__(
        self,
        state_snapshot: Any,
        *,
        bridge: Any | None = None,
        heatmap_source: Any | None = None,
        research_source: Any | None = None,
        repo_root: Path | None = None,
    ) -> None:
        self.state = state_snapshot
        self.bridge = bridge
        self.heatmap_source = heatmap_source
        self.research_source = research_source
        self.repo_root = repo_root or Path.cwd()

    # ------------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------------

    def build(self) -> dict[str, JSONValue]:
        """Compute the full integration status dictionary."""
        items: list[dict[str, JSONValue]] = []
        items.append(self._check_bridge())
        items.append(self._check_controller())
        items.append(self._check_runtime())
        items.append(self._check_structural())
        items.append(self._check_snapshot())
        items.append(self._check_delta_storage())
        items.append(self._check_structural_journal())
        items.append(self._check_research())
        items.append(self._check_tests())
        items.append(self._check_error_visibility())

        passed = sum(1 for i in items if i["status"] == PASSED)
        failed = sum(1 for i in items if i["status"] == FAILED)
        disabled = sum(1 for i in items if i["status"] == DISABLED)
        stale = sum(1 for i in items if i["status"] == STALE)

        overall: str
        if failed > 0:
            overall = FAILED
        elif stale > 0:
            overall = STALE
        elif passed > 0 and disabled > 0 and passed + disabled == len(items):
            overall = PASSED
        elif passed == len(items):
            overall = PASSED
        else:
            overall = PENDING

        return {
            "overall": overall,
            "passed": passed,
            "failed": failed,
            "disabled": disabled,
            "stale": stale,
            "total": len(items),
            "items": cast(JSONValue, items),
            "source": "live_backend",
            "acceleration": cast(JSONValue, self._build_acceleration_status()),
        }

    def _build_acceleration_status(self) -> dict[str, JSONValue]:
        """Project canonical CUDA/FE-3 integration state without executing GPU work."""

        manifest_path = (
            self.repo_root
            / "research"
            / "verification"
            / "frozen_environment"
            / "FE3_DETERMINISTIC_TARGET_V1.json"
        )
        manifest_status: dict[str, JSONValue] = {
            "path": str(manifest_path.relative_to(self.repo_root)),
            "status": "missing",
            "valid": False,
        }
        try:
            from src.verification.frozen_environment import load_manifest_artifact

            manifest = load_manifest_artifact(manifest_path)
            manifest_status = {
                "path": str(manifest_path.relative_to(self.repo_root)),
                "status": "verified",
                "valid": True,
                "mode": manifest.mode.value,
                "contract_id": manifest.contract_id,
                "manifest_sha256": manifest.manifest_sha256,
                "environment_id": manifest.environment_id,
                "sensor_ticks": len(manifest.sensor_schedule),
            }
        except (OSError, ValueError) as exc:
            manifest_status["message"] = str(exc)

        backend_status: dict[str, JSONValue]
        try:
            from src.acceleration.cuda import (
                CUDABackend,
                execution_backend_contract_check,
            )

            backend = CUDABackend()
            capabilities = backend.capabilities().to_mapping()
            backend_status = {
                "status": "integrated",
                "contract_ok": execution_backend_contract_check(),
                "backend_name": backend.backend_name,
                "backend_version": backend.backend_version,
                "capabilities": cast(JSONValue, capabilities),
            }
        except Exception as exc:  # fail closed in dashboard projection
            backend_status = {
                "status": "unavailable",
                "contract_ok": False,
                "message": str(exc),
            }

        reports = sorted(
            (self.repo_root / "docs" / "canonical").glob("HARDWARE_ACCEPTANCE_*.json")
        )
        hardware: dict[str, JSONValue]
        if not reports:
            hardware = {
                "status": "pending",
                "accepted": False,
                "artifact": None,
                "message": "No reviewed physical hardware acceptance artifact is present.",
            }
        else:
            latest = reports[-1]
            try:
                raw_object: object = json.loads(latest.read_text(encoding="utf-8"))
                if not isinstance(raw_object, dict):
                    raise ValueError("hardware acceptance artifact must be an object")
                raw = cast(dict[str, object], raw_object)
                accepted = bool(raw.get("passed")) and bool(
                    raw.get("full_fe3_accepted")
                )
                hardware = {
                    "status": "passed" if accepted else "failed",
                    "accepted": accepted,
                    "artifact": str(latest.relative_to(self.repo_root)),
                    "gpu_identity": cast(JSONValue, raw.get("gpu_identity")),
                    "wave4_physical": cast(JSONValue, raw.get("wave4_physical")),
                    "builder_d3c_bridge": cast(
                        JSONValue, raw.get("builder_d3c_bridge")
                    ),
                    "frozen_environment_fe3": cast(
                        JSONValue, raw.get("frozen_environment_fe3")
                    ),
                    "full_fe3_accepted": bool(raw.get("full_fe3_accepted")),
                    "scientific_evidence": False,
                }
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                hardware = {
                    "status": "failed",
                    "accepted": False,
                    "artifact": str(latest.relative_to(self.repo_root)),
                    "message": str(exc),
                }

        capabilities_object = backend_status.get("capabilities")
        backend_live = False
        if isinstance(capabilities_object, dict):
            capabilities_mapping = capabilities_object
            backend_live = (
                capabilities_mapping.get("supports_live_external_input") is True
            )
        fe3_software_ready = bool(manifest_status["valid"]) and backend_live

        try:
            from src.homeostasis.pan_wave5b_preflight import (
                evaluate_pan_wave5b_readiness,
            )

            pan_wave5b = evaluate_pan_wave5b_readiness(self.repo_root).to_mapping()
        except Exception as exc:  # fail closed in dashboard projection
            pan_wave5b = {
                "classification": "PAN_WAVE5B_PREFLIGHT",
                "scientific_evidence": False,
                "integration_claimed": False,
                "preflight_ready": False,
                "ready_for_execution": False,
                "blockers": ["PAN_WAVE5B_PREFLIGHT_UNAVAILABLE"],
                "next_gate": "REPAIR_PAN_WAVE5B_PREFLIGHT",
                "message": str(exc),
            }

        pan_preflight_ready = pan_wave5b.get("preflight_ready") is True

        waves: list[dict[str, JSONValue]] = [
            {"id": "wave1", "label": "Neural I/O Contracts", "status": "integrated"},
            {
                "id": "wave2",
                "label": "Codecs / Adapter / Gateway",
                "status": "integrated",
            },
            {
                "id": "wave3",
                "label": "ExecutionBackend / Parity / Determinism",
                "status": "integrated",
            },
            {"id": "wave4", "label": "Canonical CUDA Backend", "status": "integrated"},
            {
                "id": "fe3",
                "label": "FE-3 Live Backend Bridge",
                "status": "software_verified" if fe3_software_ready else "blocked",
            },
            {
                "id": "hardware",
                "label": "Physical RTX Hardware Acceptance",
                "status": str(hardware["status"]),
            },
            {
                "id": "wave5",
                "label": "PAN Hyperstate / Wave 5B",
                "status": (
                    "preflight_ready" if pan_preflight_ready else "contract_draft"
                ),
            },
            {"id": "wave6", "label": "Structural Plasticity", "status": "blocked"},
            {
                "id": "wave7",
                "label": "Canonical Learning Contract",
                "status": "blocked",
            },
        ]

        return {
            "classification": "MHRN_ACCELERATION_INTEGRATION_STATUS",
            "scientific_evidence": False,
            "software_path_closed": fe3_software_ready,
            "physical_hardware_accepted": bool(hardware["accepted"]),
            "provenance_rule": (
                "CPU/CUDA execution fingerprints differ by design; "
                "semantic equality is manifest + live-input + D3c parity."
            ),
            "backend": cast(JSONValue, backend_status),
            "fe3_manifest": cast(JSONValue, manifest_status),
            "hardware_acceptance": cast(JSONValue, hardware),
            "pan_wave5b_preflight": cast(JSONValue, pan_wave5b),
            "waves": cast(JSONValue, waves),
            "next_gate": str(
                pan_wave5b.get(
                    "next_gate",
                    "REPAIR_PAN_WAVE5B_PREFLIGHT",
                )
            ),
            "limitations": cast(
                JSONValue,
                {
                    "scientific_data": False,
                    "evidence": False,
                    "speedup_claim": False,
                    "pan_hyperstate": False,
                    "structural_plasticity": False,
                    "canonical_learning_contract": False,
                },
            ),
        }

    # ------------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------------

    def _check_bridge(self) -> dict[str, JSONValue]:
        ok = self.bridge is not None
        return {
            "name": "Bridge",
            "status": PASSED if ok else FAILED,
            "source": "live_runtime",
            "message": (
                "OperatorBridge connected" if ok else "OperatorBridge not configured"
            ),
        }

    def _check_controller(self) -> dict[str, JSONValue]:
        controller = getattr(self.bridge, "controller", None) if self.bridge else None
        ok = controller is not None
        return {
            "name": "Controller",
            "status": PASSED if ok else FAILED,
            "source": "live_runtime",
            "message": "RuntimeController connected" if ok else "Controller missing",
        }

    def _check_runtime(self) -> dict[str, JSONValue]:
        controller = getattr(self.bridge, "controller", None) if self.bridge else None
        if controller is None:
            return {
                "name": "Runtime",
                "status": FAILED,
                "source": "live_runtime",
                "message": "No controller",
            }
        try:
            tel = controller.snapshot()
            state = getattr(tel, "controller_state", None)
            state_val = state.value if state is not None else "unknown"
            return {
                "name": "Runtime",
                "status": PASSED,
                "source": "live_runtime",
                "message": f"state={state_val}, tick={getattr(tel, 'tick', 0)}",
            }
        except Exception as e:
            return {
                "name": "Runtime",
                "status": FAILED,
                "source": "live_runtime",
                "message": f"telemetry error: {e}",
            }

    def _check_structural(self) -> dict[str, JSONValue]:
        # Structural plasticity is disabled by config in poc_config.yaml.
        # "disabled by config" is NOT "failed".
        coordinator = getattr(self.bridge, "coordinator", None) if self.bridge else None
        plasticity = getattr(self.bridge, "plasticity", None) if self.bridge else None
        if coordinator is None or plasticity is None:
            return {
                "name": "Structural",
                "status": DISABLED,
                "source": "config",
                "message": "disabled by config (self_organization.enabled=false)",
            }
        return {
            "name": "Structural",
            "status": PASSED,
            "source": "live_runtime",
            "message": "Coordinator + PlasticityEngine connected",
        }

    def _check_snapshot(self) -> dict[str, JSONValue]:
        if self.heatmap_source is None:
            return {
                "name": "Snapshot",
                "status": PENDING,
                "source": "snapshot",
                "message": "No heatmap source configured",
            }
        try:
            path = getattr(self.heatmap_source, "snapshot_path", None)
            if path is None or not Path(path).exists():
                return {
                    "name": "Snapshot",
                    "status": PENDING,
                    "source": "snapshot",
                    "message": "Snapshot file not yet written",
                }
            return {
                "name": "Snapshot",
                "status": PASSED,
                "source": "snapshot",
                "message": f"{Path(path).name} available",
            }
        except Exception as e:
            return {
                "name": "Snapshot",
                "status": FAILED,
                "source": "snapshot",
                "message": f"error: {e}",
            }

    def _check_delta_storage(self) -> dict[str, JSONValue]:
        # Delta storage is disabled by config in poc_config.yaml.
        # Read the live dashboard state to determine availability.
        storage = getattr(self.state, "storage", None) if self.state else None
        available = getattr(storage, "available", False) if storage else False
        if available:
            return {
                "name": "Delta Storage",
                "status": PASSED,
                "source": "live_runtime",
                "message": "AsyncStorageSession active",
            }
        return {
            "name": "Delta Storage",
            "status": DISABLED,
            "source": "config",
            "message": "disabled by config (storage.runtime.enabled=false)",
        }

    def _check_structural_journal(self) -> dict[str, JSONValue]:
        coordinator = getattr(self.bridge, "coordinator", None) if self.bridge else None
        if coordinator is None:
            return {
                "name": "Structural Journal",
                "status": DISABLED,
                "source": "config",
                "message": "disabled by config (self_organization.enabled=false)",
            }
        return {
            "name": "Structural Journal",
            "status": PASSED,
            "source": "journal",
            "message": "StructuralJournal attached",
        }

    def _check_research(self) -> dict[str, JSONValue]:
        if self.research_source is None:
            return {
                "name": "Research",
                "status": DISABLED,
                "source": "research",
                "message": "B5D-SEF registry not found",
            }
        return {
            "name": "Research",
            "status": PASSED,
            "source": "research",
            "message": "B5D-SEF active",
        }

    def _check_tests(self) -> dict[str, JSONValue]:
        """Read tests/test_baseline.json and detect staleness.

        Scientific staleness model
        --------------------------
        A test baseline records the commit at which the test suite was last
        verified AND a digest of the scientifically relevant source tree
        (``src/``, ``configs/``, ``research/schemas/``, ``pyproject.toml``).

        A file inside a commit cannot stably contain its own commit SHA:
        amending the baseline to match the new HEAD produces yet another SHA.
        We therefore do NOT compare ``tested_commit == current_commit``.

        Instead we compare the recorded ``tested_tree_digest`` with the
        current tree digest. The baseline is:

        - ``passed``  — tree digest matches (only docs/baseline metadata changed)
        - ``stale``   — scientifically relevant source code changed since baseline
        - ``pending`` — baseline missing or HEAD/tree digest unavailable
        """
        ev = evaluate_test_baseline(self.repo_root)

        if not ev.available:
            return {
                "name": "Tests",
                "status": PENDING,
                "source": "test_baseline",
                "message": "test_baseline.json not found",
            }

        if ev.current_tree_digest is None:
            return {
                "name": "Tests",
                "status": PENDING,
                "source": "test_baseline",
                "message": "cannot compute current tree digest",
                "tested_commit": ev.tested_commit,
                "current_commit": ev.current_commit,
            }

        # Tree-digest match: only docs/baseline metadata changed since baseline.
        if not ev.stale:
            return {
                "name": "Tests",
                "status": PASSED,
                "source": "test_baseline",
                "message": (
                    f"verified tree digest matches: {ev.passed} passed, "
                    f"{ev.failed} failed, {ev.skipped} skipped"
                ),
                "tested_commit": ev.tested_commit,
                "current_commit": ev.current_commit,
                "tested_tree_digest": ev.tested_tree_digest,
                "current_tree_digest": ev.current_tree_digest,
                "passed": ev.passed,
                "failed": ev.failed,
                "skipped": ev.skipped,
            }

        # Scientifically relevant source code changed since baseline — STALE.
        return {
            "name": "Tests",
            "status": STALE,
            "source": "test_baseline",
            "message": (
                f"source tree changed since baseline "
                f"(tested_commit {(ev.tested_commit or 'unknown')[:8]}, "
                f"HEAD {(ev.current_commit or 'unknown')[:8]})"
            ),
            "tested_commit": ev.tested_commit,
            "current_commit": ev.current_commit,
            "tested_tree_digest": ev.tested_tree_digest,
            "current_tree_digest": ev.current_tree_digest,
        }

    def _check_error_visibility(self) -> dict[str, JSONValue]:
        """Error visibility is passed when the runtime error buffer is
        accessible and no fatal errors have occurred.

        Probes the OperatorBridge error interface. If the bridge is not
        configured, error visibility is pending. If errors exist, the
        status reflects their severity.
        """
        bridge = self.bridge
        if bridge is None:
            return {
                "name": "Error Visibility",
                "status": PENDING,
                "source": "live_backend",
                "message": "No bridge — error infrastructure not available",
            }
        try:
            errors = bridge.runtime_errors()
            error_count = len(errors)
            fatal_count = sum(1 for e in errors if e.get("fatal", False))
            if error_count == 0:
                return {
                    "name": "Error Visibility",
                    "status": PASSED,
                    "source": "live_backend",
                    "message": "No runtime errors observed",
                    "error_count": 0,
                }
            if fatal_count > 0:
                return {
                    "name": "Error Visibility",
                    "status": FAILED,
                    "source": "live_backend",
                    "message": f"{fatal_count} fatal runtime error(s) detected",
                    "error_count": error_count,
                    "fatal_count": fatal_count,
                }
            return {
                "name": "Error Visibility",
                "status": FAILED,
                "source": "live_backend",
                "message": f"{error_count} non-fatal runtime error(s) observed",
                "error_count": error_count,
            }
        except Exception as exc:
            return {
                "name": "Error Visibility",
                "status": FAILED,
                "source": "live_backend",
                "message": f"Error visibility check failed: {exc}",
            }

    # ------------------------------------------------------------------------
    # Helpers (delegated to verification.py for a single source of truth)
    # ------------------------------------------------------------------------

    def _current_git_head(self) -> str | None:
        """Return the current git HEAD SHA, or None if unavailable."""
        return current_git_head(self.repo_root)

    def _current_tree_digest(self) -> str | None:
        """Return a SHA-256 digest of the scientifically relevant source tree.

        Delegates to :func:`verification.compute_source_tree_digest` so that
        ``/api/integration/status`` and ``/api/gate/status`` can never
        disagree about the same source tree.
        """
        return compute_source_tree_digest(self.repo_root)
