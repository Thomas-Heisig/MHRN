"""CLI entry point for the isolated MHRN Playground."""

from __future__ import annotations

import argparse
import json

from .service import catalog, replay, robustness, run
from .visualize.session_dashboard import dashboard_payload
from .visualize.topology_2d import project_2d
from .visualize.topology_3d import project_3d
from .visualize.topology_5d_projection import project_5d


def _projection(result: dict[str, object], mode: str) -> object:
    topology = result.get("topology", {})
    coordinates = topology.get("coordinates", []) if isinstance(topology, dict) else []
    if mode == "2d":
        return project_2d(coordinates)
    if mode == "3d":
        return project_3d(coordinates)
    return project_5d(coordinates, components=2)


def _add_run_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--ticks", type=int, default=256)
    parser.add_argument("--neurons", type=int, default=128)
    parser.add_argument("--edges", type=int, default=512)
    parser.add_argument("--seed", type=int, default=12345)
    parser.add_argument("--dimensions", type=int, default=5)
    parser.add_argument("--model", default="izhikevich_rs")
    parser.add_argument("--topology", default="mhrn_5d")
    parser.add_argument("--synapse", default="static")
    parser.add_argument("--plasticity", default="none")
    parser.add_argument("--stimulus", default="deterministic")
    parser.add_argument("--ensemble", type=int, default=1)
    parser.add_argument("--geometry-mode", default="shortcut_union")
    parser.add_argument("--geometry-lambda-a", type=float, default=0.5)
    parser.add_argument("--geometry-lambda-b", type=float, default=0.5)
    parser.add_argument("--geometry-sigma", type=float, default=0.1)
    parser.add_argument("--geometry-p0", type=float, default=0.3)
    parser.add_argument("--geometry-delay-velocity", type=float, default=0.25)
    parser.add_argument("--neural-io", action="store_true")
    parser.add_argument("--io-input-channels", type=int, default=16)
    parser.add_argument("--io-output-channels", type=int, default=16)
    parser.add_argument("--io-codec", default="population_latency_v1")
    parser.add_argument("--io-decoder", default="population_rate_v1")
    parser.add_argument("--io-payload", default="0.5")
    parser.add_argument("--io-window", type=int, default=16)
    parser.add_argument("--io-current", type=float, default=25.0)
    parser.add_argument("--persist", action="store_true")


def _io_payload(args: argparse.Namespace) -> object:
    raw = args.io_payload
    if args.io_codec == "population_latency_v1":
        return float(raw)
    if args.io_codec == "vector_population_v1":
        value = json.loads(raw)
        if not isinstance(value, list):
            raise ValueError("--io-payload must be a JSON list for vector codec")
        return value
    return raw


def _payload(args: argparse.Namespace) -> dict[str, object]:
    return {
        "ticks": args.ticks,
        "n_neurons": args.neurons,
        "edge_budget": args.edges,
        "seed": args.seed,
        "dimensions": args.dimensions,
        "neuron_model": args.model,
        "topology": args.topology,
        "synapse_model": args.synapse,
        "plasticity_rule": args.plasticity,
        "stimulus": args.stimulus,
        "ensemble_runs": args.ensemble,
        "geometry_mode": args.geometry_mode,
        "geometry_lambda_a": args.geometry_lambda_a,
        "geometry_lambda_b": args.geometry_lambda_b,
        "geometry_sigma": args.geometry_sigma,
        "geometry_p0": args.geometry_p0,
        "geometry_delay_velocity": args.geometry_delay_velocity,
        "neural_io_enabled": args.neural_io,
        "neural_io_input_channels": args.io_input_channels,
        "neural_io_output_channels": args.io_output_channels,
        "neural_io_input_codec": args.io_codec,
        "neural_io_output_decoder": args.io_decoder,
        "neural_io_input_payload": _io_payload(args),
        "neural_io_window_ticks": args.io_window,
        "neural_io_input_current": args.io_current,
        "persist": args.persist,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="MHRN non-canonical Playground")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("catalog")
    sub.add_parser("list-models")
    sub.add_parser("list-topologies")

    runner = sub.add_parser("run")
    _add_run_arguments(runner)

    robust = sub.add_parser("robustness")
    _add_run_arguments(robust)

    replayer = sub.add_parser("replay")
    replayer.add_argument("session_id")

    visualizer = sub.add_parser("visualize")
    visualizer.add_argument("session_id")
    visualizer.add_argument("--projection", choices=("2d", "3d", "5d"), default="5d")

    args = parser.parse_args()
    info = catalog()

    if args.command == "catalog":
        print(json.dumps(info, indent=2, ensure_ascii=False))
        return 0
    if args.command == "list-models":
        print(json.dumps(info["models"], indent=2, ensure_ascii=False))
        return 0
    if args.command == "list-topologies":
        print(json.dumps(info["topologies"], indent=2, ensure_ascii=False))
        return 0
    if args.command == "replay":
        print(json.dumps(replay(args.session_id), indent=2, ensure_ascii=False))
        return 0
    if args.command == "visualize":
        result = replay(args.session_id)
        output = {
            "session_id": args.session_id,
            "projection": args.projection,
            "points": _projection(result, args.projection),
            "dashboard": dashboard_payload(result),
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 0
    if args.command == "robustness":
        print(json.dumps(robustness(_payload(args)), indent=2, ensure_ascii=False))
        return 0

    print(json.dumps(run(_payload(args)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
