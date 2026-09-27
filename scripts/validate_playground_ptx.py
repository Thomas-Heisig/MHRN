"""CI entry point for assembling generated Playground PTX with ptxas."""

from __future__ import annotations

import json
from pathlib import Path

from src.playground.cuda import assemble_bundle, compile_mapping


def main() -> int:
    root = Path("build") / "playground-ptxas"
    results: dict[str, object] = {}
    for preset in ("minimal_closed_loop", "credit_assignment"):
        bundle = compile_mapping({"closed_loop_preset": preset})
        report = assemble_bundle(bundle, output_dir=root / preset)
        if report.registers is None:
            raise RuntimeError(f"ptxas did not report register use for {preset}")
        results[preset] = {
            "gate_count": bundle.manifest["gate_count"],
            "registers": report.registers,
            "shared_bytes": report.shared_bytes,
            "constant_bytes": report.constant_bytes,
            "stack_bytes": report.stack_bytes,
            "spill_store_bytes": report.spill_store_bytes,
            "spill_load_bytes": report.spill_load_bytes,
        }
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
