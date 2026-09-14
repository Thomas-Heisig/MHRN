"""Read-only Stage-5 contract for the integrated artificial nervous system.

The contract composes existing sensor, interoception, actuation, feedback and
resource-accounting primitives.  It is an engineering/read-only description;
it does not enable productive external actuation and does not promote DATA to
scientific evidence.
"""

from __future__ import annotations

from typing import Any

from .interoception import (
    InteroceptionFrame,
    derive_drives,
    derive_functional_state,
    derive_regulatory_state,
    normalize_vital_signals,
)

STAGE5_REFERENCE_EXPERIMENT = (
    "research/experiments/EXP-STAGE5-20260914-INTEGRATED-NERVOUS-SYSTEM"
)


def reference_interoception_probe() -> dict[str, Any]:
    """Return a deterministic Stage-5 interoception/regulation reference probe."""
    readings = {
        "cpu_percent": 42.0,
        "memory_percent": 55.0,
        "temperature_c": 63.0,
        "network_up": True,
        "battery_percent": 80.0,
        "task_progress": 0.5,
        "novelty": 0.25,
        "actuator_confidence": 1.0,
    }
    frame = InteroceptionFrame(tick=1, signals=normalize_vital_signals(readings))
    drives = derive_drives(frame)
    regulatory = derive_regulatory_state(frame)
    functional = derive_functional_state(frame)
    return {
        "frame": frame.to_json(),
        "drives": drives.to_json(),
        "regulatory": regulatory.to_json(),
        "functional": functional.to_json(),
    }


def integrated_nervous_system_contract() -> dict[str, Any]:
    """Describe Stage 5 without altering the canonical SNN or live devices."""
    return {
        "stage": 5,
        "slug": "integrated_artificial_nervous_system",
        "title": "Integriertes künstliches Nervensystem",
        "scope": "engineering_verification",
        "layers": {
            "sensorik": {
                "implemented": True,
                "paths": [
                    "src/embodiment/sensor.py",
                    "src/embodiment/system_sensor.py",
                    "src/embodiment/sensor_activation.py",
                ],
                "claim": "typed and operator-controlled sensor boundary",
            },
            "interozeption": {
                "implemented": True,
                "paths": ["src/embodiment/interoception.py"],
                "claim": "typed host/resource observations with uncertainty",
            },
            "aktorik": {
                "implemented": True,
                "paths": [
                    "src/embodiment/controlled.py",
                    "src/embodiment/actuator_hub.py",
                    "src/embodiment/audit.py",
                ],
                "claim": "authorized commands with acceptance/effect receipts",
            },
            "feedback": {
                "implemented": True,
                "paths": [
                    "src/experience/engine.py",
                    "src/embodiment/deterministic.py",
                ],
                "claim": "deterministic synthetic sensor-SNN-action-observation loop",
            },
            "ressourcenhaushalt": {
                "implemented": True,
                "paths": [
                    "src/embodiment/interoception.py",
                    "src/embodiment/msba.py",
                ],
                "claim": "bounded resource pressure, uncertainty and energy accounting",
            },
        },
        "runtime_projection": {
            "state": "/api/embodiment/state",
            "pipeline": "/api/embodiment/pipeline",
            "metrics": "/api/embodiment/metrics",
            "history": "/api/embodiment/history",
            "connections": "/api/embodiment/connections",
            "sensors": "/api/embodiment/sensors",
        },
        "experiment": {
            "path": STAGE5_REFERENCE_EXPERIMENT,
            "research_question": "RQ-EMB-001",
            "hypotheses": ["H-EMB-001-A", "H-EMB-001-B"],
            "status": "DATA",
            "automatic_evidence_promotion": False,
        },
        "boundaries": {
            "productive_external_actuation_enabled": False,
            "real_device_verified": False,
            "long_horizon_verified": False,
            "biological_interoception_claim": False,
            "biological_metabolism_claim": False,
            "conscious_experience_claim": False,
            "automatic_evidence_promotion": False,
        },
        "reference_probe": reference_interoception_probe(),
    }
