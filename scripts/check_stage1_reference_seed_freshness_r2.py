#!/usr/bin/env python3
"""Freeze-gate seed freshness check for Stage-1 reference replication R2."""
from __future__ import annotations
import json, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREREG=ROOT/"research"/"preregistrations"/"PREREG-S1-TOPO-REFERENCE-R2.json"
ALLOWED_PATHS={PREREG.relative_to(ROOT).as_posix(),"reference/stage1_topology_brian2/reference_protocol_r2.json","research/preregistrations/PREREG-S1-TOPO-REFERENCE-R2.freeze.json"}
def main()->int:
    prereg=json.loads(PREREG.read_text(encoding="utf-8"))
    seeds=[str(int(v)) for v in prereg["evaluation"]["seeds"]]
    files=subprocess.check_output(["git","ls-files","-z"],cwd=ROOT).decode().split("\0")
    collisions={seed:[] for seed in seeds}
    pattern=re.compile(r"(?<!\\d)("+ "|".join(re.escape(s) for s in seeds) +r")(?!\\d)")
    for name in files:
        if not name or name in ALLOWED_PATHS: continue
        path=ROOT/name
        if not path.is_file(): continue
        try: content=path.read_text(encoding="utf-8")
        except (UnicodeDecodeError,OSError): continue
        for m in pattern.finditer(content): collisions[m.group(1)].append(name)
    collisions={s:sorted(set(v)) for s,v in collisions.items() if v}
    payload={"preregistration_id":prereg["preregistration_id"],"checked_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),"seeds":prereg["evaluation"]["seeds"],"allowed_paths":sorted(ALLOWED_PATHS),"collisions":collisions,"collision_free":not collisions}
    print(json.dumps(payload,indent=2,sort_keys=True)); return 0 if payload["collision_free"] else 1
if __name__=="__main__": raise SystemExit(main())
