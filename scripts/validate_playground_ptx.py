"""CI entry point for assembling generated Playground PTX with ptxas."""

from __future__ import annotations

import json
from pathlib import Path

from src.playground.cuda import assemble_bundle, compile_mapping
from src.playground.cuda.nvrtc import compile_cuda_source
from src.playground.cuda.runtime import assemble_ptx


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
    source = Path("src/playground/cuda/recurrent.cu").read_text()
    recurrent_dir = root / "recurrent"
    recurrent_dir.mkdir(parents=True, exist_ok=True)
    ptx_path = recurrent_dir / "recurrent.ptx"
    ptx_path.write_text(compile_cuda_source(source), encoding="utf-8")
    recurrent_report = assemble_ptx(
        ptx_path.read_text(), output_dir=recurrent_dir, target_sm="sm_86"
    )
    results["recurrent"] = recurrent_report.to_mapping()
    plastic_report = assemble_ptx(
        compile_cuda_source("#define PAN_PLASTIC\n" + source),
        output_dir=root / "plasticity",
        target_sm="sm_86",
    )
    results["plasticity"] = plastic_report.to_mapping()
    results["builder_membrane"] = assemble_ptx(
        compile_cuda_source(Path("src/playground/cuda/membrane.cu").read_text()),
        output_dir=root / "builder-membrane",
        target_sm="sm_86",
    ).to_mapping()
    results["builder_pan_state"] = assemble_ptx(
        compile_cuda_source(Path("src/playground/cuda/pan_state.cu").read_text()),
        output_dir=root / "builder-pan-state",
        target_sm="sm_86",
    ).to_mapping()
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
