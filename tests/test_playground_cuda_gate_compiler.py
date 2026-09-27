"""Contracts for the Playground-only PAN gate compiler."""

from __future__ import annotations

import pytest

from src.playground.cuda import (
    GateLaunchInputs,
    GateType,
    compile_config,
    compile_mapping,
    compile_yaml,
    compiler_catalog,
    cooperative_capacity,
    cpu_gate_reference,
    cuda_runtime_status,
    gate_execution_parity_summary,
    gate_parity_summary,
    nontrivial_gate_launch_inputs,
    parse_ptxas_verbose,
    smoke_gate_launch_inputs,
    validate_gate_launch_inputs,
)
from src.playground.models import PlaygroundConfig


def test_minimal_closed_loop_lowers_to_45_gates() -> None:
    config = PlaygroundConfig.from_mapping(
        {"closed_loop_preset": "minimal_closed_loop"}
    )
    bundle = compile_config(config)

    assert bundle.manifest["classification"] == "PLAYGROUND_CUDA_GATE_COMPILER"
    assert bundle.manifest["scientific_evidence"] is False
    assert bundle.manifest["gate_count"] == 45
    assert bundle.manifest["stage_inventory"] == {
        "A1": 16,
        "A2": 8,
        "A3": 3,
        "A4": 3,
        "B1": 8,
        "C1": 3,
        "C2": 2,
        "D1": 2,
    }
    assert bundle.manifest["execution_status"] == "SOURCE_GENERATED_NOT_EXECUTED"
    assert bundle.manifest["canonical_cuda_backend"] is False


def test_minimal_closed_loop_emits_sm86_ptx_with_real_gate_instructions() -> None:
    bundle = compile_mapping({"closed_loop_preset": "minimal_closed_loop"})

    assert ".version 7.1" in bundle.ptx
    assert ".target sm_86" in bundle.ptx
    assert ".entry pan_gate_kernel" in bundle.ptx
    assert "and.b64" in bundle.ptx
    assert "tanh.approx.f32" in bundle.ptx
    assert "fma.rn.f32" in bundle.ptx
    assert "setp.gt.f32" in bundle.ptx
    assert "selp.u32" in bundle.ptx
    assert "%globaltimer" not in bundle.ptx


def test_cuda_scaffold_requires_cooperative_grid_sync_without_cdp() -> None:
    bundle = compile_mapping({"closed_loop_preset": "minimal_closed_loop"})
    source = bundle.cuda_source
    resources = bundle.manifest["resource_contract"]

    assert "cooperative_groups.h" in source
    assert "cg::this_grid()" in source
    assert "grid.sync()" in source
    assert "const bool active = gid < cfg.n_neurons" in source
    assert "cudaLaunchDevice" not in source
    assert resources["grid_sync"] == "COOPERATIVE_LAUNCH_REQUIRED"
    assert resources["dynamic_parallelism_inside_cooperative_kernel"] is False
    assert resources["structural_mutation"] == (
        "HOST_OR_EXPLICIT_STRUCTURAL_BARRIER_PHASE"
    )


def test_compiler_uses_64_bit_channel_masks_for_64_channel_contract() -> None:
    bundle = compile_mapping({"input_channels": 64})

    assert bundle.manifest["resource_contract"]["channel_mask_bits"] == 64
    assert "and.b64" in bundle.ptx
    assert "0x8000000000000000" in bundle.ptx


def test_yaml_preset_alias_is_supported_with_safe_validation() -> None:
    bundle = compile_yaml("preset: minimal_closed_loop\n")
    assert bundle.manifest["preset"] == "minimal_closed_loop"
    assert bundle.manifest["gate_count"] == 45

    with pytest.raises(ValueError, match="YAML root"):
        compile_yaml("- not\n- a\n- mapping\n")


def test_sm86_rejects_ptx_70() -> None:
    config = PlaygroundConfig.from_mapping(
        {"closed_loop_preset": "minimal_closed_loop"}
    )
    with pytest.raises(ValueError, match="sm_86 requires PTX ISA >= 7.1"):
        compile_config(config, target_sm="sm_86", ptx_version="7.0")


def test_tanh_codegen_rejects_targets_below_sm75() -> None:
    config = PlaygroundConfig.from_mapping(
        {"closed_loop_preset": "minimal_closed_loop"}
    )
    with pytest.raises(ValueError, match="tanh.approx.f32"):
        compile_config(config, target_sm="sm_70")


def test_credit_assignment_adds_explicit_c4_gates() -> None:
    bundle = compile_mapping({"closed_loop_preset": "credit_assignment"})
    stages = bundle.manifest["stage_inventory"]
    inventory = bundle.manifest["gate_inventory"]

    assert stages["C4"] == 4
    assert inventory["G_FMA"] >= 1
    assert inventory["G_ADD"] >= 3


def test_compiler_catalog_exposes_all_declared_gate_types_and_boundaries() -> None:
    payload = compiler_catalog()
    assert payload["classification"] == "PLAYGROUND_CUDA_GATE_COMPILER"
    assert payload["scientific_evidence"] is False
    assert set(payload["gate_types"]) == {item.value for item in GateType}
    assert payload["synchronization"]["memory_fence"] == (
        "membar.gl is not a grid barrier"
    )
    assert payload["structural_growth"] == "separate structural barrier/host phase"


def test_ptxas_verbose_parser_reports_measured_resources(tmp_path) -> None:
    report = parse_ptxas_verbose(
        (
            "ptxas info    : Compiling entry function 'pan_gate_kernel' for 'sm_86'\n"
            "ptxas info    : Function properties for pan_gate_kernel\n"
            "    16 bytes stack frame, 8 bytes spill stores, 4 bytes spill loads\n"
            "ptxas info    : Used 37 registers, 512 bytes smem, 384 bytes cmem[0]\n"
        ),
        target_sm="sm_86",
        cubin_path=tmp_path / "kernel.cubin",
    )
    assert report.registers == 37
    assert report.shared_bytes == 512
    assert report.constant_bytes == 384
    assert report.stack_bytes == 16
    assert report.spill_store_bytes == 8
    assert report.spill_load_bytes == 4


def test_cooperative_capacity_depends_on_occupancy_not_sm_count_alone() -> None:
    fits = cooperative_capacity(
        n_neurons=7168,
        block_size=128,
        multiprocessor_count=28,
        active_blocks_per_sm=2,
    )
    assert fits.required_blocks == 56
    assert fits.resident_block_capacity == 56
    assert fits.launch_fits is True

    too_large = cooperative_capacity(
        n_neurons=7169,
        block_size=128,
        multiprocessor_count=28,
        active_blocks_per_sm=2,
    )
    assert too_large.required_blocks == 57
    assert too_large.launch_fits is False


def test_cooperative_capacity_fails_when_device_lacks_support() -> None:
    report = cooperative_capacity(
        n_neurons=128,
        block_size=128,
        multiprocessor_count=28,
        active_blocks_per_sm=4,
        cooperative_launch=False,
    )
    assert report.resident_block_capacity == 112
    assert report.launch_fits is False


def test_gate_parity_summary_is_explicitly_not_full_snn_equivalence() -> None:
    summary = gate_parity_summary(
        [1.0, 2.0, 3.0],
        [1.0, 2.000001, 3.0],
        tolerance=1.0e-5,
    )
    assert summary["passed"] is True
    assert summary["comparison_scope"] == "GATE_OUTPUT_ONLY_NOT_FULL_SNN"
    assert summary["scientific_evidence"] is False


def test_compiler_declares_executable_kernel_abi() -> None:
    bundle = compile_mapping({"closed_loop_preset": "minimal_closed_loop"})
    abi = bundle.manifest["kernel_abi"]

    assert abi["entry"] == "pan_gate_kernel"
    assert abi["parameter_count"] == 17
    assert abi["input_channels"] == 8
    assert abi["action_space_size"] == 4
    assert abi["pan_dimensions"] >= 1
    assert abi["parameters"][-1] == "epsilon:f32"


def test_smoke_launch_inputs_match_compiler_abi() -> None:
    bundle = compile_mapping({"closed_loop_preset": "minimal_closed_loop"})
    inputs = smoke_gate_launch_inputs(bundle, n_neurons=12, seed=12345)
    shape = validate_gate_launch_inputs(bundle, inputs)

    assert shape["n_neurons"] == 12
    assert len(inputs.channel_masks) == 12
    assert len(inputs.amplitudes) == shape["input_channels"]
    assert len(inputs.action_map) == (shape["action_count"] * shape["input_channels"])
    assert len(inputs.feedback_matrix) == (shape["n_neurons"] * shape["pan_dimensions"])
    assert len(inputs.logits) == shape["n_neurons"] * shape["action_count"]
    assert all(mask == 0xFF for mask in inputs.channel_masks)


def test_gate_launch_input_validation_fails_closed_on_bad_shape() -> None:
    bundle = compile_mapping({"closed_loop_preset": "minimal_closed_loop"})
    good = smoke_gate_launch_inputs(bundle, n_neurons=4)
    broken = GateLaunchInputs(
        input_current=good.input_current,
        channel_masks=good.channel_masks,
        amplitudes=good.amplitudes[:-1],
        reward_ring=good.reward_ring,
        action_map=good.action_map,
        feedback_matrix=good.feedback_matrix,
        population=good.population,
        logits=good.logits,
        tick=good.tick,
        target_index=good.target_index,
        previous_action=good.previous_action,
        seed=good.seed,
        epsilon=good.epsilon,
    )

    with pytest.raises(ValueError, match="amplitudes length"):
        validate_gate_launch_inputs(bundle, broken)


def test_cpu_gate_reference_matches_nontrivial_minimal_loop_math() -> None:
    bundle = compile_mapping(
        {
            "closed_loop_preset": "minimal_closed_loop",
            "pan_feedback_gain": 0.0,
        }
    )
    inputs = GateLaunchInputs.from_sequences(
        input_current=[1.0, 2.0],
        channel_masks=[0xFF, 0xFF],
        amplitudes=[1.0] * 8,
        reward_ring=[0.5],
        action_map=[
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            3.0,
            4.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        feedback_matrix=[0.0]
        * (2 * int(bundle.manifest["kernel_abi"]["pan_dimensions"])),
        population=[0.0] * int(bundle.manifest["kernel_abi"]["pan_dimensions"]),
        logits=[
            0.1,
            0.2,
            0.3,
            0.9,
            0.1,
            0.8,
            0.2,
            0.3,
        ],
        tick=0,
        target_index=2,
        previous_action=1,
        seed=123,
        epsilon=0.0,
    )

    result = cpu_gate_reference(bundle, inputs)
    outputs = result["outputs"]

    assert outputs["current"] == pytest.approx([46.5, 56.5], abs=1.0e-6)
    assert outputs["action"] == [3, 1]
    assert result["comparison_scope"] == "GATE_OUTPUT_ONLY_NOT_FULL_SNN"
    assert result["scientific_evidence"] is False


def test_gate_execution_parity_compares_current_and_action() -> None:
    reference = {
        "outputs": {
            "current": [1.0, 2.0],
            "action": [2, 1],
        }
    }
    candidate = {
        "outputs": {
            "current": [1.00001, 1.99999],
            "action": [2, 1],
        }
    }
    summary = gate_execution_parity_summary(reference, candidate)

    assert summary["parity_class"] == "D2"
    assert summary["actions_exact"] is True
    assert summary["current_max_abs_error"] < 1.0e-4
    assert summary["passed"] is True

    candidate["outputs"]["action"] = [2, 0]
    failed = gate_execution_parity_summary(reference, candidate)
    assert failed["actions_exact"] is False
    assert failed["passed"] is False


def test_cuda_runtime_status_fails_closed_without_optional_cuda_dependencies() -> None:
    status = cuda_runtime_status(
        ptxas="definitely-not-a-real-ptxas",
        driver_library="definitely-not-a-real-cuda-driver",
    )

    assert status["classification"] == "PLAYGROUND_CUDA_RUNTIME_STATUS"
    assert status["scientific_evidence"] is False
    assert status["ptxas_available"] is False
    assert status["driver_available"] is False
    assert status["stages"]["CUDA-1.3"] == (
        "IMPLEMENTED_REQUIRES_LOCAL_GPU_VERIFICATION"
    )
    assert status["stages"]["CUDA-1.4"].startswith("NOT_IMPLEMENTED")


def test_nontrivial_gate_inputs_exercise_current_action_feedback_and_rng() -> None:
    bundle = compile_mapping(
        {
            "closed_loop_preset": "minimal_closed_loop",
            "pan_feedback_gain": 0.0,
        }
    )
    inputs = nontrivial_gate_launch_inputs(
        bundle,
        n_neurons=32,
        seed=12345,
        epsilon=0.5,
    )
    reference = cpu_gate_reference(bundle, inputs)
    outputs = reference["outputs"]

    assert len(inputs.input_current) == 32
    assert any(value != 0.0 for value in inputs.input_current)
    assert any(value != 0.0 for value in inputs.action_map)
    assert any(value != 0.0 for value in inputs.reward_ring)
    assert any(value != 0.0 for value in inputs.logits)
    assert inputs.tick >= 3
    assert inputs.epsilon == pytest.approx(0.5)
    assert len(outputs["current"]) == 32
    assert len(outputs["action"]) == 32
    assert len(set(outputs["current"])) > 1
    assert all(
        0 <= int(action) < int(bundle.manifest["kernel_abi"]["action_space_size"])
        for action in outputs["action"]
    )
