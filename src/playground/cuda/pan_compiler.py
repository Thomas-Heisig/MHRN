"""Playground-only PAN gate compiler for CUDA/PTX reference kernels.

This module lowers validated :class:`PlaygroundConfig` values into a small gate
IR and emits two artifacts:

* PTX for a single-step reference gate kernel.
* CUDA C++ for a cooperative persistent-kernel scaffold.

The compiler is an engineering Playground component. It does not promote a run
to DATA/EVID, does not replace the canonical CUDA contracts, and does not claim
measured GPU performance. Structural mutation remains outside the cooperative
persistent kernel because cooperative grid synchronization and CUDA Dynamic
Parallelism are not combined by this reference path.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import struct
from collections import Counter
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import cast

import yaml

from ..models import PlaygroundConfig

CLASSIFICATION = "PLAYGROUND_CUDA_GATE_COMPILER"
DEFAULT_TARGET_SM = "sm_86"
DEFAULT_PTX_VERSION = "7.0"


class GateType(str, Enum):
    """Gate operations supported by the bounded reference compiler."""

    G_AND = "G_AND"
    G_OR = "G_OR"
    G_XOR = "G_XOR"
    G_NOT = "G_NOT"
    G_ADD = "G_ADD"
    G_MUL = "G_MUL"
    G_FMA = "G_FMA"
    G_CMP = "G_CMP"
    G_SEL = "G_SEL"
    G_EXP = "G_EXP"
    G_TANH = "G_TANH"
    G_ARGMAX = "G_ARGMAX"
    G_SHUFFLE = "G_SHUFFLE"
    G_ATOM = "G_ATOM"
    G_TIMER = "G_TIMER"
    G_BAR = "G_BAR"
    G_SYNC = "G_SYNC"
    G_DELAY = "G_DELAY"
    G_INDEX = "G_INDEX"
    G_GATHER = "G_GATHER"
    G_HASH = "G_HASH"
    G_DOT = "G_DOT"
    G_OUT = "G_OUT"


@dataclass(frozen=True, slots=True)
class Gate:
    """One typed gate in the compiler IR."""

    index: int
    stage: str
    gate_type: GateType
    label: str
    params: dict[str, object]


@dataclass(frozen=True, slots=True)
class GateProgram:
    """Validated gate program derived from a Playground configuration."""

    config: PlaygroundConfig
    gates: tuple[Gate, ...]
    target_sm: str
    ptx_version: str

    def inventory(self) -> dict[str, int]:
        counts = Counter(gate.gate_type.value for gate in self.gates)
        return dict(sorted(counts.items()))

    def stage_inventory(self) -> dict[str, int]:
        counts = Counter(gate.stage for gate in self.gates)
        return dict(sorted(counts.items()))


@dataclass(frozen=True, slots=True)
class CompileBundle:
    """Serializable result of one gate-compilation request."""

    manifest: dict[str, object]
    gate_ir: list[dict[str, object]]
    ptx: str
    cuda_source: str

    def to_mapping(self) -> dict[str, object]:
        return {
            "manifest": self.manifest,
            "gate_ir": self.gate_ir,
            "ptx": self.ptx,
            "cuda_source": self.cuda_source,
        }


def _target_number(target_sm: str) -> int:
    match = re.fullmatch(r"sm_(\d{2,3})", target_sm.strip())
    if match is None:
        raise ValueError("target_sm must use NVIDIA form sm_XX, for example sm_86")
    return int(match.group(1))


def _validate_target(config: PlaygroundConfig, target_sm: str) -> None:
    number = _target_number(target_sm)
    if number < 50:
        raise ValueError("reference compiler requires target_sm >= sm_50")
    if config.pan_feedback_nonlinearity == "tanh" and number < 75:
        raise ValueError("tanh.approx.f32 requires target_sm >= sm_75")


def _gate(
    gates: list[Gate],
    stage: str,
    gate_type: GateType,
    label: str,
    **params: object,
) -> None:
    gates.append(
        Gate(
            index=len(gates),
            stage=stage,
            gate_type=gate_type,
            label=label,
            params=dict(params),
        )
    )


def build_gate_program(
    config: PlaygroundConfig,
    *,
    target_sm: str = DEFAULT_TARGET_SM,
    ptx_version: str = DEFAULT_PTX_VERSION,
) -> GateProgram:
    """Translate a validated Playground configuration into a deterministic IR."""

    _validate_target(config, target_sm)
    gates: list[Gate] = []

    # A1 - input differentiation. A 64-bit mask is used because the builder
    # allows up to 64 channels; a u32 mask would lose channels 32..63.
    for channel in range(config.input_channels):
        _gate(gates, "A1", GateType.G_AND, f"input_mask_ch_{channel}", channel=channel)
        _gate(
            gates,
            "A1",
            GateType.G_MUL,
            f"input_amplitude_ch_{channel}",
            channel=channel,
        )

    if config.target_encoding != "none":
        slots = config.action_space_size if config.target_encoding == "one_hot" else 1
        for action in range(slots):
            _gate(
                gates,
                "A2",
                GateType.G_CMP,
                f"target_match_{action}",
                action=action,
            )
            _gate(
                gates,
                "A2",
                GateType.G_MUL,
                f"target_cue_{action}",
                action=action,
            )

    if config.reward_signal_enabled:
        _gate(
            gates,
            "A3",
            GateType.G_DELAY,
            "reward_delay",
            delay_ticks=config.reward_delay_ticks,
        )
        _gate(
            gates,
            "A3",
            GateType.G_MUL,
            "reward_magnitude",
            magnitude=config.reward_magnitude,
        )
        _gate(
            gates,
            "A3",
            GateType.G_CMP,
            "reward_channel_select",
            channel=config.reward_channel,
        )

    if config.action_loop_enabled:
        _gate(gates, "A4", GateType.G_INDEX, "action_map_index")
        _gate(gates, "A4", GateType.G_GATHER, "action_map_gather")
        _gate(
            gates,
            "A4",
            GateType.G_MUL,
            "action_coupling",
            strength=config.action_coupling_strength,
        )

    if config.neuron_threshold_variance > 0.0:
        _gate(gates, "B1", GateType.G_HASH, "threshold_hash")
        _gate(
            gates,
            "B1",
            GateType.G_MUL,
            "threshold_variance_scale",
            sigma=config.neuron_threshold_variance,
        )
        _gate(gates, "B1", GateType.G_ADD, "threshold_bias")
    if config.neuron_tau_m_variance > 0.0:
        _gate(gates, "B1", GateType.G_HASH, "tau_hash")
        _gate(
            gates,
            "B1",
            GateType.G_MUL,
            "tau_variance_scale",
            sigma=config.neuron_tau_m_variance,
        )
        _gate(gates, "B1", GateType.G_ADD, "tau_bias")
    if config.inhibitory_fraction > 0.0:
        _gate(gates, "B1", GateType.G_HASH, "inhibitory_hash")
        _gate(
            gates,
            "B1",
            GateType.G_CMP,
            "inhibitory_fraction_compare",
            fraction=config.inhibitory_fraction,
        )

    if config.refractory_variance > 0.0:
        _gate(gates, "B2", GateType.G_CMP, "refractory_compare")
        _gate(gates, "B2", GateType.G_SEL, "refractory_select")
    if config.adaptation_strength > 0.0:
        _gate(gates, "B2", GateType.G_FMA, "adaptation_update")
    if config.oscillation_enabled:
        _gate(gates, "B2", GateType.G_MUL, "oscillation_omega")
        _gate(gates, "B2", GateType.G_ADD, "oscillation_phase")

    if config.pan_enabled and config.pan_closed_loop and config.pan_feedback_gain > 0.0:
        _gate(
            gates,
            "C1",
            GateType.G_DOT,
            "pan_feedback_dot",
            dimensions=config.pan_dimensions,
        )
        nonlinearity = {
            "tanh": GateType.G_TANH,
            "linear": GateType.G_SEL,
            "sign": GateType.G_SEL,
            "clip": GateType.G_SEL,
        }[config.pan_feedback_nonlinearity]
        _gate(
            gates,
            "C1",
            nonlinearity,
            f"pan_feedback_{config.pan_feedback_nonlinearity}",
        )
        _gate(
            gates,
            "C1",
            GateType.G_MUL,
            "pan_feedback_gain",
            gain=config.pan_feedback_gain,
        )
        _gate(
            gates,
            "C2",
            GateType.G_CMP,
            "pan_feedback_threshold",
            threshold=config.pan_feedback_threshold,
        )
        _gate(
            gates,
            "C2",
            GateType.G_SEL,
            "pan_feedback_saturation",
            saturation=config.pan_feedback_saturation,
        )

    if config.credit_assignment != "none":
        _gate(
            gates,
            "C4",
            GateType.G_FMA,
            "eligibility_decay_and_spike",
            td_lambda=config.td_lambda,
        )
        _gate(
            gates,
            "C4",
            GateType.G_MUL,
            "eligibility_reward",
            gamma=config.gamma_discount,
        )
        _gate(gates, "C4", GateType.G_ADD, "weight_update")
        _gate(
            gates,
            "C4",
            GateType.G_CMP,
            "credit_window",
            window=config.credit_window,
        )

    _gate(
        gates,
        "D1",
        GateType.G_ARGMAX,
        "action_argmax",
        action_count=config.action_space_size,
    )
    _gate(
        gates,
        "D1",
        GateType.G_SEL,
        "epsilon_greedy_select",
        epsilon=config.behavior_epsilon,
    )

    return GateProgram(
        config=config,
        gates=tuple(gates),
        target_sm=target_sm,
        ptx_version=ptx_version,
    )


def _f32_hex(value: float) -> str:
    bits = struct.unpack("<I", struct.pack("<f", float(value)))[0]
    return f"0f{bits:08x}"


def _u64_mask(channel: int) -> str:
    return f"0x{(1 << channel):016x}"


def _gate_comment(gate: Gate) -> str:
    params = ", ".join(f"{key}={value}" for key, value in sorted(gate.params.items()))
    suffix = f" [{params}]" if params else ""
    return (
        f"    // gate {gate.index:03d} {gate.stage} "
        f"{gate.gate_type.value} {gate.label}{suffix}"
    )


def _emit_gate_ptx(gate: Gate, program: GateProgram) -> list[str]:
    """Lower one IR gate into PTX instructions using the reference scratch ABI."""

    config = program.config
    lines = [_gate_comment(gate)]
    kind = gate.gate_type
    label = gate.label

    if kind == GateType.G_AND:
        channel = cast(int, gate.params.get("channel", 0))
        lines += [
            f"    and.b64 %rd20, %rd19, {_u64_mask(channel)};",
            "    setp.ne.u64 %p0, %rd20, 0;",
        ]
    elif kind == GateType.G_OR:
        lines.append("    or.b32 %r20, %r20, %r21;")
    elif kind == GateType.G_XOR:
        lines.append("    xor.b32 %r20, %r20, %r21;")
    elif kind == GateType.G_NOT:
        lines.append("    not.b32 %r20, %r20;")
    elif kind == GateType.G_ADD:
        if label == "threshold_bias":
            lines.append("    add.f32 %f20, %f20, %f6;")
        elif label == "tau_bias":
            lines.append("    add.f32 %f21, %f21, %f6;")
        elif label == "weight_update":
            lines.append("    add.f32 %f24, %f24, %f25;")
        elif label == "oscillation_phase":
            lines.append("    add.f32 %f23, %f23, %f22;")
        else:
            lines.append("    add.f32 %f1, %f1, %f2;")
    elif kind == GateType.G_MUL:
        if label.startswith("input_amplitude_ch_"):
            channel = cast(int, gate.params.get("channel", 0))
            offset = channel * 4
            lines += [
                f"    add.u64 %rd21, %rd2, {offset};",
                "    ld.global.f32 %f2, [%rd21];",
                "    selp.f32 %f3, %f0, 0f00000000, %p0;",
                "    mul.f32 %f3, %f3, %f2;",
                "    add.f32 %f1, %f1, %f3;",
            ]
        elif label.startswith("target_cue_"):
            cue = _f32_hex(config.target_cue_current)
            lines += [
                f"    selp.f32 %f2, {cue}, 0f00000000, %p0;",
                "    add.f32 %f1, %f1, %f2;",
            ]
        elif label == "reward_magnitude":
            lines.append(f"    mul.f32 %f4, %f4, {_f32_hex(config.reward_magnitude)};")
        elif label == "action_coupling":
            lines += [
                f"    mul.f32 %f2, %f2, {_f32_hex(config.action_coupling_strength)};",
                "    add.f32 %f1, %f1, %f2;",
            ]
        elif label == "threshold_variance_scale":
            lines.append(
                f"    mul.f32 %f6, %f6, {_f32_hex(config.neuron_threshold_variance)};"
            )
        elif label == "tau_variance_scale":
            lines.append(
                f"    mul.f32 %f6, %f6, {_f32_hex(config.neuron_tau_m_variance)};"
            )
        elif label == "pan_feedback_gain":
            lines.append(f"    mul.f32 %f8, %f8, {_f32_hex(config.pan_feedback_gain)};")
        elif label == "eligibility_reward":
            lines += [
                f"    mul.f32 %f25, %f24, {_f32_hex(config.gamma_discount)};",
                "    mul.f32 %f25, %f25, %f4;",
                f"    mul.f32 %f25, %f25, {_f32_hex(config.behavior_learning_rate)};",
            ]
        elif label == "oscillation_omega":
            omega = 2.0 * math.pi * config.oscillation_frequency * config.dt_ms / 1000.0
            lines.append(f"    mul.f32 %f22, %f30, {_f32_hex(omega)};")
        else:
            lines.append("    mul.f32 %f2, %f0, %f2;")
    elif kind == GateType.G_FMA:
        if label == "eligibility_decay_and_spike":
            lines.append(
                f"    fma.rn.f32 %f24, %f24, {_f32_hex(config.td_lambda)}, %f10;"
            )
        elif label == "adaptation_update":
            decay = math.exp(-config.dt_ms / max(config.adaptation_tau, 1e-9))
            lines.append(f"    fma.rn.f32 %f26, %f26, {_f32_hex(decay)}, %f10;")
        else:
            lines.append("    fma.rn.f32 %f2, %f0, %f1, %f2;")
    elif kind == GateType.G_CMP:
        if label.startswith("target_match_"):
            action = cast(int, gate.params.get("action", 0))
            channel = (config.target_cue_channel + action) % config.input_channels
            lines += [
                f"    setp.eq.u32 %p1, %r6, {action};",
                f"    and.b64 %rd20, %rd19, {_u64_mask(channel)};",
                "    setp.ne.u64 %p2, %rd20, 0;",
                "    and.pred %p0, %p1, %p2;",
            ]
        elif label == "reward_channel_select":
            lines += [
                f"    and.b64 %rd20, %rd19, {_u64_mask(config.reward_channel)};",
                "    setp.ne.u64 %p0, %rd20, 0;",
                "    selp.f32 %f2, %f4, 0f00000000, %p0;",
                "    add.f32 %f1, %f1, %f2;",
            ]
        elif label == "inhibitory_fraction_compare":
            lines.append(
                f"    setp.lt.f32 %p3, %f6, {_f32_hex(config.inhibitory_fraction)};"
            )
        elif label == "pan_feedback_threshold":
            lines += [
                "    abs.f32 %f9, %f8;",
                f"    setp.ge.f32 %p4, %f9, {_f32_hex(config.pan_feedback_threshold)};",
            ]
        elif label == "credit_window":
            lines.append(f"    setp.le.u32 %p5, %r18, {config.credit_window};")
        elif label == "refractory_compare":
            lines.append("    setp.ge.u32 %p5, %r8, %r17;")
        else:
            lines.append("    setp.gt.f32 %p0, %f1, 0f00000000;")
    elif kind == GateType.G_SEL:
        if label == "pan_feedback_saturation":
            saturation = _f32_hex(config.pan_feedback_saturation)
            negative = _f32_hex(-config.pan_feedback_saturation)
            lines += [
                f"    setp.gt.f32 %p5, %f8, {saturation};",
                f"    selp.f32 %f8, {saturation}, %f8, %p5;",
                f"    setp.lt.f32 %p5, %f8, {negative};",
                f"    selp.f32 %f8, {negative}, %f8, %p5;",
                "    selp.f32 %f8, %f8, 0f00000000, %p4;",
                "    add.f32 %f1, %f1, %f8;",
            ]
        elif label == "pan_feedback_linear":
            lines.append("    mov.f32 %f8, %f8;")
        elif label == "pan_feedback_sign":
            lines += [
                "    setp.gt.f32 %p5, %f8, 0f00000000;",
                "    selp.f32 %f8, 0f3f800000, 0fbf800000, %p5;",
            ]
        elif label == "pan_feedback_clip":
            lines += [
                "    setp.gt.f32 %p5, %f8, 0f3f800000;",
                "    selp.f32 %f8, 0f3f800000, %f8, %p5;",
                "    setp.lt.f32 %p5, %f8, 0fbf800000;",
                "    selp.f32 %f8, 0fbf800000, %f8, %p5;",
            ]
        elif label == "epsilon_greedy_select":
            lines += [
                "    xor.b32 %r20, %r3, %r14;",
                "    xor.b32 %r20, %r20, %r8;",
                "    mul.lo.u32 %r20, %r20, 2654435761;",
                "    cvt.rn.f32.u32 %f7, %r20;",
                "    mul.f32 %f7, %f7, 0f2f800000;",
                "    setp.lt.f32 %p6, %f7, %f5;",
                f"    rem.u32 %r21, %r20, {config.action_space_size};",
                "    selp.u32 %r13, %r21, %r13, %p6;",
            ]
        elif label == "refractory_select":
            lines.append("    selp.f32 %f1, %f1, 0f00000000, %p5;")
        else:
            lines.append("    selp.f32 %f1, %f1, %f0, %p0;")
    elif kind == GateType.G_EXP:
        lines += [
            "    mul.f32 %f2, %f0, 0f3fb8aa3b;",
            "    ex2.approx.ftz.f32 %f2, %f2;",
        ]
    elif kind == GateType.G_TANH:
        lines.append("    tanh.approx.f32 %f8, %f8;")
    elif kind == GateType.G_ARGMAX:
        count = cast(int, gate.params.get("action_count", config.action_space_size))
        lines += [
            "    mul.wide.u32 %rd22, %r3, %r15;",
            "    add.u64 %rd23, %rd7, %rd22;",
            "    ld.global.f32 %f11, [%rd23];",
            "    mov.u32 %r13, 0;",
        ]
        for action in range(1, count):
            offset = action * 4
            lines += [
                f"    ld.global.f32 %f12, [%rd23+{offset}];",
                "    setp.gt.f32 %p0, %f12, %f11;",
                "    selp.f32 %f11, %f12, %f11, %p0;",
                f"    selp.u32 %r13, {action}, %r13, %p0;",
            ]
    elif kind == GateType.G_SHUFFLE:
        lines.append("    shfl.sync.idx.b32 %r20|%p0, %r21, 0, 0x1f, 0xffffffff;")
    elif kind == GateType.G_ATOM:
        lines.append("    atom.global.add.f32 %f2, [%rd10], %f1;")
    elif kind == GateType.G_TIMER:
        lines.append("    mov.u64 %rd24, %globaltimer;")
    elif kind == GateType.G_BAR:
        lines.append("    bar.sync 0;")
    elif kind == GateType.G_SYNC:
        lines.append("    membar.gl; // memory fence only; NOT a grid barrier")
    elif kind == GateType.G_DELAY:
        delay = cast(int, gate.params.get("delay_ticks", 0))
        lines += [
            f"    setp.ge.u32 %p0, %r8, {delay};",
            f"    sub.u32 %r20, %r8, {delay};",
            "    rem.u32 %r20, %r20, %r9;",
            "    mul.wide.u32 %rd20, %r20, 4;",
            "    add.u64 %rd20, %rd3, %rd20;",
            "    ld.global.f32 %f4, [%rd20];",
            "    selp.f32 %f4, %f4, 0f00000000, %p0;",
        ]
    elif kind == GateType.G_INDEX:
        lines += [
            f"    mul.lo.u32 %r12, %r7, {config.input_channels};",
            f"    rem.u32 %r10, %r3, {config.input_channels};",
            "    add.u32 %r12, %r12, %r10;",
        ]
    elif kind == GateType.G_GATHER:
        lines += [
            "    mul.wide.u32 %rd20, %r12, 4;",
            "    add.u64 %rd20, %rd4, %rd20;",
            "    ld.global.f32 %f2, [%rd20];",
        ]
    elif kind == GateType.G_HASH:
        salt = {
            "threshold_hash": 0x9E3779B9,
            "tau_hash": 0x85EBCA6B,
            "inhibitory_hash": 0xC2B2AE35,
        }.get(label, 0x27D4EB2D)
        lines += [
            f"    xor.b32 %r20, %r3, {salt};",
            "    mul.lo.u32 %r20, %r20, 2654435761;",
            "    cvt.rn.f32.u32 %f6, %r20;",
            "    mul.f32 %f6, %f6, 0f2f800000;",
            "    add.f32 %f6, %f6, 0fbf000000;",
        ]
    elif kind == GateType.G_DOT:
        dimensions = cast(int, gate.params.get("dimensions", config.pan_dimensions))
        lines.append("    mov.f32 %f8, 0f00000000;")
        lines.append(f"    mul.lo.u32 %r20, %r3, {dimensions};")
        for dim in range(dimensions):
            offset = dim * 4
            lines += [
                f"    add.u32 %r21, %r20, {dim};",
                "    mul.wide.u32 %rd20, %r21, 4;",
                "    add.u64 %rd21, %rd5, %rd20;",
                "    ld.global.f32 %f2, [%rd21];",
                f"    ld.global.f32 %f3, [%rd6+{offset}];",
                "    fma.rn.f32 %f8, %f2, %f3, %f8;",
            ]
    elif kind == GateType.G_OUT:
        lines.append("    st.global.f32 [%rd10], %f1;")
    else:
        raise AssertionError(f"unsupported gate: {kind}")

    return lines


def emit_ptx(program: GateProgram) -> str:
    """Emit a self-contained single-step PTX reference kernel."""

    config = program.config
    lines = [
        f".version {program.ptx_version}",
        f".target {program.target_sm}",
        ".address_size 64",
        "",
        "// Playground reference kernel. Not a canonical scientific CUDA backend.",
        "// Channel masks are u64 because input_channels may be 64.",
        "// Physical register use must be measured with ptxas; "
        "PTX registers are virtual.",
        "",
        ".visible .entry pan_gate_kernel(",
        "    .param .u64 p_input,",
        "    .param .u64 p_channel_masks,",
        "    .param .u64 p_amplitudes,",
        "    .param .u64 p_reward_ring,",
        "    .param .u64 p_action_map,",
        "    .param .u64 p_feedback_matrix,",
        "    .param .u64 p_population,",
        "    .param .u64 p_logits,",
        "    .param .u64 p_out_current,",
        "    .param .u64 p_out_action,",
        "    .param .u32 p_n_neurons,",
        "    .param .u32 p_tick,",
        "    .param .u32 p_reward_ring_size,",
        "    .param .u32 p_target_index,",
        "    .param .u32 p_previous_action,",
        "    .param .u32 p_seed,",
        "    .param .f32 p_epsilon",
        ")",
        "{",
        "    .reg .pred %p<8>;",
        "    .reg .b32 %r<32>;",
        "    .reg .b64 %rd<32>;",
        "    .reg .f32 %f<32>;",
        "",
        "    ld.param.u64 %rd0, [p_input];",
        "    ld.param.u64 %rd1, [p_channel_masks];",
        "    ld.param.u64 %rd2, [p_amplitudes];",
        "    ld.param.u64 %rd3, [p_reward_ring];",
        "    ld.param.u64 %rd4, [p_action_map];",
        "    ld.param.u64 %rd5, [p_feedback_matrix];",
        "    ld.param.u64 %rd6, [p_population];",
        "    ld.param.u64 %rd7, [p_logits];",
        "    ld.param.u64 %rd8, [p_out_current];",
        "    ld.param.u64 %rd9, [p_out_action];",
        "    ld.param.u32 %r4, [p_n_neurons];",
        "    ld.param.u32 %r8, [p_tick];",
        "    ld.param.u32 %r9, [p_reward_ring_size];",
        "    ld.param.u32 %r6, [p_target_index];",
        "    ld.param.u32 %r7, [p_previous_action];",
        "    ld.param.u32 %r14, [p_seed];",
        "    ld.param.f32 %f5, [p_epsilon];",
        "",
        "    mov.u32 %r0, %tid.x;",
        "    mov.u32 %r1, %ctaid.x;",
        "    mov.u32 %r2, %ntid.x;",
        "    mad.lo.u32 %r3, %r1, %r2, %r0;",
        "    setp.ge.u32 %p7, %r3, %r4;",
        "    @%p7 bra DONE;",
        "",
        "    mul.wide.u32 %rd10, %r3, 4;",
        "    add.u64 %rd11, %rd0, %rd10;",
        "    ld.global.f32 %f0, [%rd11];",
        "    mov.f32 %f1, 0f00000000;",
        "    mov.f32 %f10, 0f00000000;",
        "    mov.f32 %f20, 0f00000000;",
        "    mov.f32 %f21, 0f00000000;",
        "    mov.f32 %f23, 0f00000000;",
        "    mov.f32 %f24, 0f00000000;",
        "    mov.f32 %f26, 0f00000000;",
        "    cvt.rn.f32.u32 %f30, %r8;",
        "",
        "    mul.wide.u32 %rd18, %r3, 8;",
        "    add.u64 %rd18, %rd1, %rd18;",
        "    ld.global.u64 %rd19, [%rd18];",
        f"    mov.u32 %r15, {config.action_space_size * 4};",
        "    mov.u32 %r17, 0;",
        "    mov.u32 %r18, 0;",
        "",
    ]

    for gate in program.gates:
        lines.extend(_emit_gate_ptx(gate, program))
        lines.append("")

    lines += [
        "    mul.wide.u32 %rd20, %r3, 4;",
        "    add.u64 %rd21, %rd8, %rd20;",
        "    st.global.f32 [%rd21], %f1;",
        "    add.u64 %rd22, %rd9, %rd20;",
        "    st.global.u32 [%rd22], %r13;",
        "",
        "DONE:",
        "    ret;",
        "}",
        "",
    ]
    return "\n".join(lines)


def emit_cuda_source(program: GateProgram) -> str:
    """Emit a cooperative persistent-kernel scaffold for the compiled program."""

    c = program.config
    adaptation_decay = math.exp(-c.dt_ms / max(c.adaptation_tau, 1e-9))
    return f"""// Generated by MHRN Playground PAN gate compiler.
// Classification: {CLASSIFICATION}; scientific_evidence=false.
// Target: {program.target_sm}; PTX baseline: {program.ptx_version}.
//
// IMPORTANT:
// - Launch this kernel cooperatively when grid.sync() is used.
// - Do not use CUDA Dynamic Parallelism from this cooperative kernel.
// - Structural growth/rebuild is a separate host/barrier phase in this reference.
// - Register count is determined by ptxas, not by symbolic R0..R45 labels.

#include <cooperative_groups.h>
#include <cuda_runtime.h>

namespace cg = cooperative_groups;

struct PanGateConfig {{
    unsigned n_neurons;
    unsigned input_channels;
    unsigned action_count;
    unsigned pan_dimensions;
    unsigned reward_delay_ticks;
    float target_cue_current;
    float reward_magnitude;
    float action_coupling_strength;
    float feedback_gain;
    float feedback_threshold;
    float feedback_saturation;
    float epsilon;
    unsigned seed;
}};

__device__ __forceinline__ unsigned pan_hash(unsigned x) {{
    x ^= x >> 16;
    x *= 0x7feb352dU;
    x ^= x >> 15;
    x *= 0x846ca68bU;
    x ^= x >> 16;
    return x;
}}

extern "C" __global__ void pan_persistent_kernel(
    const float* input,
    const unsigned long long* channel_masks,
    const float* amplitudes,
    const float* reward_ring,
    unsigned reward_ring_size,
    const float* action_map,
    const float* feedback_matrix,
    const float* population,
    const float* logits,
    const unsigned* targets,
    float* out_current,
    unsigned* out_action,
    unsigned ticks,
    PanGateConfig cfg
) {{
    cg::grid_group grid = cg::this_grid();
    const unsigned gid = blockIdx.x * blockDim.x + threadIdx.x;
    const bool active = gid < cfg.n_neurons;

    float eligibility = 0.0f;
    float adaptation = 0.0f;
    unsigned previous_action = 0U;

    for (unsigned tick = 0; tick < ticks; ++tick) {{
        if (active) {{
        float current = input[gid];
        const unsigned long long mask = channel_masks[gid];

        #pragma unroll
        for (unsigned ch = 0; ch < {c.input_channels}; ++ch) {{
            if ((mask & (1ULL << ch)) != 0ULL) {{
                current += input[gid] * amplitudes[ch];
            }}
        }}

        const unsigned target = targets[tick];
        if (
            {1 if c.target_encoding != 'none' else 0}
            && tick % {max(c.behavior_episode_ticks, 1)} < {c.target_persistence}
        ) {{
            const unsigned cue_ch =
                ({c.target_cue_channel}U + target) % cfg.input_channels;
            if ((mask & (1ULL << cue_ch)) != 0ULL) {{
                current += {c.target_cue_current:.9g}f;
            }}
        }}

        if ({1 if c.reward_signal_enabled else 0} && tick >= {c.reward_delay_ticks}U) {{
            const unsigned reward_index =
                (tick - {c.reward_delay_ticks}U) % reward_ring_size;
            if ((mask & (1ULL << {c.reward_channel}U)) != 0ULL) {{
                current += reward_ring[reward_index] * {c.reward_magnitude:.9g}f;
            }}
        }}

        if ({1 if c.action_loop_enabled else 0}) {{
            const unsigned channel = gid % cfg.input_channels;
            current += action_map[previous_action * cfg.input_channels + channel]
                * {c.action_coupling_strength:.9g}f;
        }}

        float feedback = 0.0f;
        if ({1 if c.pan_enabled and c.pan_closed_loop and c.pan_feedback_gain > 0.0 else 0}) {{
            #pragma unroll
            for (unsigned dim = 0; dim < {c.pan_dimensions}; ++dim) {{
                feedback = fmaf(
                    feedback_matrix[gid * cfg.pan_dimensions + dim],
                    population[dim],
                    feedback
                );
            }}
            {'feedback = tanhf(feedback);' if c.pan_feedback_nonlinearity == 'tanh' else ''}
            feedback *= {c.pan_feedback_gain:.9g}f;
            if (fabsf(feedback) < {c.pan_feedback_threshold:.9g}f) {{
                feedback = 0.0f;
            }}
            feedback = fminf(
                {c.pan_feedback_saturation:.9g}f,
                fmaxf(-{c.pan_feedback_saturation:.9g}f, feedback)
            );
            current += feedback;
        }}

        unsigned action = 0U;
        float best = logits[gid * cfg.action_count];
        for (unsigned candidate = 1; candidate < cfg.action_count; ++candidate) {{
            const float value = logits[gid * cfg.action_count + candidate];
            if (value > best) {{
                best = value;
                action = candidate;
            }}
        }}
        const unsigned random_bits = pan_hash(cfg.seed ^ gid ^ tick);
        const float uniform =
            static_cast<float>(random_bits) * 2.3283064365386963e-10f;
        if (uniform < cfg.epsilon) action = random_bits % cfg.action_count;

        if ({1 if c.credit_assignment != 'none' else 0}) {{
            eligibility = fmaf(eligibility, {c.td_lambda:.9g}f, 0.0f);
        }}
        if ({1 if c.adaptation_strength > 0.0 else 0}) {{
            adaptation *= {adaptation_decay:.9g}f;
            current -= adaptation * {c.adaptation_strength:.9g}f;
        }}

        out_current[gid] = current;
        out_action[gid] = action;
        previous_action = action;
        }}

        grid.sync();
    }}
}}
"""


def _resource_contract(program: GateProgram) -> dict[str, object]:
    target = _target_number(program.target_sm)
    ampere_86 = target == 86
    return {
        "target_sm": program.target_sm,
        "ptx_version": program.ptx_version,
        "max_physical_registers_per_thread": 255 if target >= 20 else None,
        "physical_register_count": "MEASURE_WITH_PTXAS",
        "conceptual_gate_state_registers": "NOT_A_PHYSICAL_REGISTER_CLAIM",
        "channel_mask_bits": 64,
        "shared_memory_plan": "NOT_FIXED_BY_COMPILER_V1",
        "sm86_shared_memory_per_block_max_kb": 99 if ampere_86 else None,
        "sm86_dynamic_shared_memory_opt_in_above_kb": 48 if ampere_86 else None,
        "grid_sync": "COOPERATIVE_LAUNCH_REQUIRED",
        "dynamic_parallelism_inside_cooperative_kernel": False,
        "structural_mutation": "HOST_OR_EXPLICIT_STRUCTURAL_BARRIER_PHASE",
        "rng": "DETERMINISTIC_HASH_SEED_GID_TICK",
        "globaltimer_used_for_rng": False,
    }


def compiler_catalog() -> dict[str, object]:
    """Return bounded compiler capabilities for the Playground catalog."""

    return {
        "classification": CLASSIFICATION,
        "scientific_evidence": False,
        "status": "REFERENCE_CODEGEN_IMPLEMENTED_GPU_EXECUTION_NOT_CLAIMED",
        "default_target_sm": DEFAULT_TARGET_SM,
        "default_ptx_version": DEFAULT_PTX_VERSION,
        "gate_types": [item.value for item in GateType],
        "outputs": ["gate_ir", "ptx", "cuda_source"],
        "synchronization": {
            "block_barrier": "bar.sync / __syncthreads",
            "memory_fence": "membar.gl is not a grid barrier",
            "grid_barrier": "cooperative_groups grid.sync + cooperative launch",
        },
        "structural_growth": "separate structural barrier/host phase",
        "note": (
            "Playground engineering compiler only. Generated source and PTX do not "
            "constitute measured acceleration, scientific DATA, or EVID."
        ),
    }


def compile_config(
    config: PlaygroundConfig,
    *,
    target_sm: str = DEFAULT_TARGET_SM,
    ptx_version: str = DEFAULT_PTX_VERSION,
) -> CompileBundle:
    """Compile one validated PlaygroundConfig into IR + PTX + CUDA source."""

    program = build_gate_program(
        config,
        target_sm=target_sm,
        ptx_version=ptx_version,
    )
    gate_ir = [
        {
            **asdict(gate),
            "gate_type": gate.gate_type.value,
        }
        for gate in program.gates
    ]
    ptx = emit_ptx(program)
    cuda_source = emit_cuda_source(program)
    manifest: dict[str, object] = {
        "classification": CLASSIFICATION,
        "scientific_evidence": False,
        "preset": config.closed_loop_preset,
        "gate_count": len(program.gates),
        "gate_inventory": program.inventory(),
        "stage_inventory": program.stage_inventory(),
        "target_sm": target_sm,
        "ptx_version": ptx_version,
        "resource_contract": _resource_contract(program),
        "ptx_line_count": len(ptx.splitlines()),
        "cuda_line_count": len(cuda_source.splitlines()),
        "execution_status": "SOURCE_GENERATED_NOT_EXECUTED",
        "canonical_cuda_backend": False,
        "structural_mutation_in_kernel": False,
    }
    return CompileBundle(
        manifest=manifest,
        gate_ir=gate_ir,
        ptx=ptx,
        cuda_source=cuda_source,
    )


def compile_mapping(
    payload: Mapping[str, object],
    *,
    target_sm: str = DEFAULT_TARGET_SM,
    ptx_version: str = DEFAULT_PTX_VERSION,
) -> CompileBundle:
    """Validate an untrusted mapping through PlaygroundConfig and compile it."""

    config = PlaygroundConfig.from_mapping(payload)
    return compile_config(config, target_sm=target_sm, ptx_version=ptx_version)


def compile_yaml(
    source: str,
    *,
    target_sm: str = DEFAULT_TARGET_SM,
    ptx_version: str = DEFAULT_PTX_VERSION,
) -> CompileBundle:
    """Compile one YAML document using safe parsing and config validation."""

    loaded = yaml.safe_load(source)
    if not isinstance(loaded, Mapping):
        raise ValueError("YAML root must be a mapping")
    payload: dict[str, object] = {str(key): value for key, value in loaded.items()}
    if "preset" in payload and "closed_loop_preset" not in payload:
        payload["closed_loop_preset"] = payload.pop("preset")
    return compile_mapping(payload, target_sm=target_sm, ptx_version=ptx_version)


def write_bundle(bundle: CompileBundle, output_dir: Path) -> dict[str, Path]:
    """Write compiler artifacts to an explicit local directory."""

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "manifest": output_dir / "pan_gate_manifest.json",
        "gate_ir": output_dir / "pan_gate_ir.json",
        "ptx": output_dir / "pan_gate_kernel.ptx",
        "cuda_source": output_dir / "pan_gate_kernel.cu",
    }
    paths["manifest"].write_text(
        json.dumps(bundle.manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    paths["gate_ir"].write_text(
        json.dumps(bundle.gate_ir, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    paths["ptx"].write_text(bundle.ptx, encoding="utf-8")
    paths["cuda_source"].write_text(bundle.cuda_source, encoding="utf-8")
    return paths


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compile PAN Playground YAML to gate IR/PTX"
    )
    parser.add_argument("config", type=Path, help="Playground YAML file")
    parser.add_argument("--out", type=Path, required=True, help="Output directory")
    parser.add_argument("--target-sm", default=DEFAULT_TARGET_SM)
    parser.add_argument("--ptx-version", default=DEFAULT_PTX_VERSION)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    bundle = compile_yaml(
        args.config.read_text(encoding="utf-8"),
        target_sm=args.target_sm,
        ptx_version=args.ptx_version,
    )
    paths = write_bundle(bundle, args.out)
    print(json.dumps({key: str(value) for key, value in paths.items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
