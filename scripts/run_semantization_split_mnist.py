"""CLI for EXP-S6-SEM-CL-001."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.research.continual_semantization import (
    SplitMnistConfig,
    load_mnist,
    run_split_mnist_semantization,
    write_result_bundle,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=Path(".cache/mnist"))
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research-output/EXP-S6-SEM-CL-001"),
    )
    parser.add_argument("--train-per-class", type=int, default=1000)
    parser.add_argument("--test-per-class", type=int, default=200)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(101, 111)))
    return parser


def main() -> int:
    args = _parser().parse_args()
    config = SplitMnistConfig(
        train_per_class=args.train_per_class,
        test_per_class=args.test_per_class,
        seeds=tuple(args.seeds),
    )
    data = load_mnist(args.cache_dir)
    result = run_split_mnist_semantization(data, config)
    write_result_bundle(result, args.output_dir)
    print("MHRN_SEMANTIZATION_RESULT=" + json.dumps(result["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
