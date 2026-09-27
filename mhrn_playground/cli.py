"""Public CLI shim for the isolated MHRN Playground."""

from src.playground.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
