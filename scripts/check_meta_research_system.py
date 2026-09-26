#!/usr/bin/env python3
from __future__ import annotations
from src.research.meta_system import MetaSystem

def main() -> int:
    system=MetaSystem()
    drift=system.write(check=True)
    if drift:
        print("ERROR: stale meta-system projections: "+", ".join(drift))
        return 1
    print("Meta research system checks passed.")
    return 0
if __name__=="__main__":
    raise SystemExit(main())
