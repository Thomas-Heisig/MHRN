from __future__ import annotations

import random

import pytest

from src.core.network import Brain5DConfig, NeuralNetwork
from src.core.neural_tissue import (
    ConnectionRole,
    NeuralTissueConfig,
    NeuralTissueController,
    NeuronTissueState,
    SynapseTissueState,
    TimescaleConfig,
)


def _network() -> tuple[NeuralNetwork, int, int]:
    network = NeuralNetwork(
        Brain5DConfig(dimensions=(3, 3, 3, 3, 3)),
        random.Random(7),
    )
    pre = network.add_neuron((1, 1, 1, 1, 1))
    post = network.add_neuron((1, 1, 1, 1, 2))
    network.connect(pre, post, weight=0.25, delay=1)
    return network, pre, post


def test_timescales_are_ordered_and_positive() -> None:
    with pytest.raises(ValueError):
        TimescaleConfig(plasticity_interval_ticks=0)
    with pytest.raises(ValueError):
        TimescaleConfig(
            plasticity_interval_ticks=10,
            consolidation_interval_ticks=5,
        )
    with pytest.raises(ValueError):
        TimescaleConfig(
            plasticity_interval_ticks=10,
            consolidation_interval_ticks=100,
            development_interval_ticks=50,
        )


def test_neuron_context_and_calcium_bridge_tick_to_slow_state() -> None:
    state = NeuronTissueState()
    config = NeuralTissueConfig()

    gain = state.integrate_context(basal=2.0, apical=3.0)
    state.on_tick(spiked=True, config=config)
    state.plasticity_step(1.0)

    assert gain > 1.0
    assert state.calcium > 0.0
    assert state.second_messenger > 0.0
    assert state.prediction_error > 0.0
    assert 0.0 <= state.metabolic_reserve <= 1.0


def test_synapse_stp_depresses_then_recovers() -> None:
    state = SynapseTissueState()
    config = NeuralTissueConfig()

    first = state.effective_release(config)
    after_release = state.depression_resource
    state.recover(config)

    assert first > 0.0
    assert after_release < 1.0
    assert state.depression_resource > after_release
    assert state.use_count == 1


def test_controller_keeps_weight_mutation_opt_in() -> None:
    network, pre, post = _network()
    controller = NeuralTissueController(
        network,
        NeuralTissueConfig(
            timescales=TimescaleConfig(
                plasticity_interval_ticks=1,
                consolidation_interval_ticks=10,
                development_interval_ticks=100,
            ),
            enable_weight_updates=False,
        ),
    )
    before = network.synapses[pre][0].weight
    network.inject_current(pre, 100.0)
    report = controller.step()

    assert report.plasticity_ran is True
    assert network.synapses[pre][0].weight == before
    assert (pre, post) in controller.synapses


def test_weight_update_uses_energy_budget_when_explicitly_enabled() -> None:
    network, pre, post = _network()
    controller = NeuralTissueController(
        network,
        NeuralTissueConfig(
            timescales=TimescaleConfig(
                plasticity_interval_ticks=1,
                consolidation_interval_ticks=10,
                development_interval_ticks=100,
            ),
            plasticity_energy_cost=0.01,
            enable_weight_updates=True,
        ),
    )
    controller.neurons[pre].activity_memory = 1.0
    controller.neurons[post].activity_memory = 1.0
    controller.neurons[post].calcium = 2.0
    controller.synapses[(pre, post)].bcm_threshold = 0.1
    before_reserve = controller.neurons[post].metabolic_reserve
    before_weight = network.synapses[pre][0].weight

    report = controller.step()

    assert report.plasticity_energy_spent >= 0.0
    assert controller.neurons[post].metabolic_reserve <= before_reserve
    assert network.synapses[pre][0].weight >= before_weight


def test_roles_attention_and_compartment_context_are_explicit() -> None:
    network, pre, post = _network()
    controller = NeuralTissueController(network)

    controller.set_connection_role(pre, post, ConnectionRole.FEEDBACK)
    controller.set_attention_gain(pre, post, 1.5)
    controller.set_neuromodulator(post, 1.25)
    gain = controller.compartment_gain(post, basal=1.0, apical=1.0)

    state = controller.synapses[(pre, post)]
    assert state.connection_role is ConnectionRole.FEEDBACK
    assert state.modulation_gain == pytest.approx(1.5)
    assert controller.neurons[post].neuromodulator_gain == pytest.approx(1.25)
    assert gain > 1.0


def test_consolidation_can_freeze_high_confidence_synapse() -> None:
    network, pre, post = _network()
    controller = NeuralTissueController(
        network,
        NeuralTissueConfig(
            timescales=TimescaleConfig(
                plasticity_interval_ticks=1,
                consolidation_interval_ticks=1,
                development_interval_ticks=10,
            ),
            consolidation_rate=1.0,
        ),
    )
    state = controller.synapses[(pre, post)]
    state.synaptic_tag = 1.0
    state.confidence = 1.0

    controller.step()

    assert state.consolidation == pytest.approx(1.0)
    assert state.frozen is True


def test_development_emits_auditable_prune_proposal_without_mutation() -> None:
    network, pre, post = _network()
    controller = NeuralTissueController(
        network,
        NeuralTissueConfig(
            timescales=TimescaleConfig(
                plasticity_interval_ticks=1,
                consolidation_interval_ticks=1,
                development_interval_ticks=1,
            ),
            structural_prune_confidence=0.2,
            enable_structural_mutation=False,
        ),
    )
    controller.synapses[(pre, post)].confidence = 0.01

    report = controller.step()

    assert report.development_ran is True
    assert any(
        proposal.action == "prune"
        and proposal.pre_id == pre
        and proposal.post_id == post
        for proposal in report.structural_proposals
    )
    assert network.synapse_count == 1


def test_controller_sidecar_serialization_is_separate_from_network() -> None:
    network, pre, post = _network()
    controller = NeuralTissueController(network)
    controller.set_connection_role(pre, post, "feedforward")
    payload = controller.to_dict()

    assert payload["schema_version"] == 1
    assert str(pre) in payload["neurons"]
    assert f"{pre}:{post}" in payload["synapses"]
    assert payload["synapses"][f"{pre}:{post}"]["connection_role"] == "feedforward"
    assert "neurons" in network.to_dict()
