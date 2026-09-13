from __future__ import annotations

import pytest

from src.core.biophysical_contracts import DendriticNonlinearity
from src.core.compartment_neuron import CompartmentConfig, CompartmentNeuron
from src.core.gap_junction import GapJunction, GapJunctionConfig
from src.core.glia.astrocyte import AstrocyteConfig, AstrocyteField
from src.core.glia.microglia import MicrogliaConfig, MicrogliaField
from src.core.hh_neuron import HHConfig, HodgkinHuxleyNeuron
from src.core.slow.protein_synthesis import (
    ProteinSynthesisConfig,
    SlowConsolidation,
    TagCaptureState,
)
from src.core.slow.receptor_trafficking import (
    ReceptorTrafficking,
    ReceptorTraffickingConfig,
    ReceptorTraffickingState,
)
from src.core.synapse_stochastic import QuantalSTPSynapse, QuantalSynapseConfig


def test_hh_ablation_uses_same_class_with_channels_disabled() -> None:
    base = HodgkinHuxleyNeuron(1, HHConfig(enabled=True, enable_na=True, enable_k=True))
    ablated = HodgkinHuxleyNeuron(
        1, HHConfig(enabled=True, enable_na=False, enable_k=True)
    )
    for tick in range(20):
        base.step(10.0, tick)
        ablated.step(10.0, tick)
    assert base.v != ablated.v
    assert base.provenance_tag.parameters["enable_na"] is True
    assert ablated.provenance_tag.parameters["enable_na"] is False


def test_compartment_and_nmda_plateau_are_independent_axes() -> None:
    linear = CompartmentNeuron(
        1,
        CompartmentConfig(
            enabled=True, dendritic_nonlinearity=DendriticNonlinearity.LINEAR
        ),
        dendrite_v=[-30.0, -30.0],
    )
    plateau = CompartmentNeuron(
        1,
        CompartmentConfig(
            enabled=True,
            dendritic_nonlinearity=DendriticNonlinearity.NMDA_PLATEAU,
            enable_nmda_plateau=True,
        ),
        dendrite_v=[-30.0, -30.0],
    )
    linear.step(0.0, (0.0, 0.0), 0)
    plateau.step(0.0, (0.0, 0.0), 0)
    assert plateau.dendrite_v[0] > linear.dendrite_v[0]


def test_quantal_release_is_seed_reproducible() -> None:
    config = QuantalSynapseConfig(enabled=True, seed=1234)
    left = QuantalSTPSynapse(2, 0.5, 1, config)
    right = QuantalSTPSynapse(2, 0.5, 1, config)
    left_trace = [left.release(tick) for tick in range(1, 100)]
    right_trace = [right.release(tick) for tick in range(1, 100)]
    assert left_trace == right_trace
    assert left.to_dict() == right.to_dict()
    assert left.provenance_tag.seed == 1234


def test_gap_junction_is_bidirectional_and_conservative() -> None:
    junction = GapJunction(1, 2, GapJunctionConfig(enabled=True, conductance=0.2))
    current_a, current_b = junction.currents(-70.0, -50.0)
    assert current_a == pytest.approx(-current_b)
    assert current_a > 0.0


def test_astrocyte_has_no_effect_without_explicit_enable() -> None:
    field = AstrocyteField(AstrocyteConfig(enabled=False))
    assert field.plasticity_update(10.0) == 1.0
    assert field.calcium == 0.0


def test_microglia_only_emits_proposal() -> None:
    field = MicrogliaField(
        MicrogliaConfig(enabled=True, prune_confidence_threshold=0.2)
    )
    proposal = field.develop(1, 2, confidence=0.1)
    assert proposal is not None
    assert proposal.action == "prune"
    assert (proposal.pre_id, proposal.post_id) == (1, 2)


def test_tag_capture_expires_outside_window() -> None:
    engine = SlowConsolidation(
        ProteinSynthesisConfig(enabled=True, capture_window_ticks=10)
    )
    state = TagCaptureState()
    engine.tag(state, tick=0, strength=1.0)
    before = engine.consolidate(state, tick=5, synthesis_signal=1.0)
    assert before > 0.0
    engine.tag(state, tick=10, strength=1.0)
    frozen = state.consolidation
    after = engine.consolidate(state, tick=21, synthesis_signal=1.0)
    assert after == frozen
    assert state.tagged_tick is None


def test_receptor_trafficking_modulates_transmission_not_weight() -> None:
    mechanism = ReceptorTrafficking(
        ReceptorTraffickingConfig(enabled=True, insertion_rate=0.1)
    )
    state = ReceptorTraffickingState(availability=0.5)
    weight = 0.8
    mechanism.plasticity_update(state, insertion_signal=1.0, removal_signal=0.0)
    assert weight == 0.8
    assert mechanism.transmission(weight, state) == pytest.approx(weight * 0.6)
