#!/usr/bin/env python3
"""Freeze corrected Stage-1 topology reference R2; freezing never authorizes execution."""
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research"/"preregistrations"/"PREREG-S1-TOPO-REFERENCE-R2.json"; F=ROOT/"research"/"preregistrations"/"PREREG-S1-TOPO-REFERENCE-R2.freeze.json"
A=ROOT/"research"/"audits"/"STAGE1_TOPOLOGY_REFERENCE_MECHANISM_AUDIT_20260927.json"; I=ROOT/"research"/"calibrations"/"CAL-S1-TOPO-REFERENCE-INTEGRATOR-R1"/"result.json"; R=ROOT/"research"/"calibrations"/"CAL-S1-TOPO-REFERENCE-RESET-R1"/"result.json"; S=ROOT/"research"/"calibrations"/"CAL-S1-TOPO-REFERENCE-SYNAPSE-R1"/"result.json"; T=ROOT/"research"/"calibrations"/"CAL-S1-TOPO-REFERENCE-TOPOLOGY-MAP-R2"/"result.json"
PROTO=ROOT/"reference"/"stage1_topology_brian2"/"reference_protocol_r2.json"; RUN=ROOT/"reference"/"stage1_topology_brian2"/"runner_r2.py"; VER=ROOT/"scripts"/"verify_stage1_topology_reference_r2.py"; TR=ROOT/"reference"/"stage1_topology_brian2"/"TRANSLATION_R2.md"; IND=ROOT/"scripts"/"check_stage1_reference_independence.py"; SEED=ROOT/"scripts"/"check_stage1_reference_seed_freshness_r2.py"; CT=ROOT/"tests"/"test_stage1_reference_r2_contract.py"; PT=ROOT/"tests"/"test_stage1_reference_r2_preflight.py"
def read(path): return json.loads(path.read_text(encoding="utf-8"))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args): return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def main()->int:
    if F.exists(): raise FileExistsError(F)
    if git("status","--porcelain"): raise RuntimeError("R2 freeze requires clean tree")
    p=read(P)
    if p.get("status")!="DRAFT_PRE_FREEZE_GATES_PENDING" or p.get("execution_authorized") is not False: raise RuntimeError("R2 not freeze-eligible")
    for x in (A,I,R,S,T,PROTO,RUN,VER,TR,CT,PT):
        if not x.is_file(): raise RuntimeError(f"missing {x.relative_to(ROOT)}")
    a,i,r,s,t=map(read,(A,I,R,S,T))
    if not (a.get("pass") and i.get("pass") and i.get("multi_tick",{}).get("pass") and i.get("multi_tick",{}).get("contains_spike") and r.get("pass") and s.get("pass") and t.get("pass")): raise RuntimeError("one or more R2 gates failed")
    proto=read(PROTO)
    if proto.get("seeds")!=p["evaluation"]["seeds"] or proto.get("framework_version")!="2.10.1": raise RuntimeError("R2 protocol mismatch")
    subprocess.run(["python",str(IND.relative_to(ROOT))],cwd=ROOT,check=True); subprocess.run(["python",str(SEED.relative_to(ROOT))],cwd=ROOT,check=True); subprocess.run(["python","-m","pytest",str(CT.relative_to(ROOT)),str(PT.relative_to(ROOT)),"-q"],cwd=ROOT,check=True)
    source=a.get("source_sha256",{})
    if not source: raise RuntimeError("mechanism audit not source-hash-bound")
    for rel,expected in source.items():
        if sha(ROOT/rel)!=expected: raise RuntimeError(f"source drift {rel}")
    freeze={"schema_version":1,"preregistration_id":p["preregistration_id"],"supersedes":"PREREG-S1-TOPO-REFERENCE-R1","freeze_date":"2026-09-27","freeze_commit":git("rev-parse","HEAD"),"preregistration_sha256_before_status_update":sha(P),"reference_data_created":False,"execution_authorized":False,"scientific_evidence":False,"replication_credit_awarded":False,"mechanism_audit":{"path":str(A.relative_to(ROOT)),"sha256":sha(A),"pass":True},"integrator_parity":{"path":str(I.relative_to(ROOT)),"sha256":sha(I),"pass":True,"reused_from_r1_with_source_hash_revalidation":True},"reset_parity":{"path":str(R.relative_to(ROOT)),"sha256":sha(R),"pass":True,"reused_from_r1_with_source_hash_revalidation":True},"synapse_delay_parity":{"path":str(S.relative_to(ROOT)),"sha256":sha(S),"pass":True,"reused_from_r1_with_source_hash_revalidation":True},"topology_mapping_parity":{"path":str(T.relative_to(ROOT)),"sha256":sha(T),"pass":True},"translation_specification":{"path":str(TR.relative_to(ROOT)),"sha256":sha(TR)},"sanitized_runner_protocol":{"path":str(PROTO.relative_to(ROOT)),"sha256":sha(PROTO)},"reference_runner":{"path":str(RUN.relative_to(ROOT)),"sha256":sha(RUN),"execution_authorized":False},"reference_verifier":{"path":str(VER.relative_to(ROOT)),"sha256":sha(VER)},"contract_tests":{str(CT.relative_to(ROOT)):sha(CT),str(PT.relative_to(ROOT)):sha(PT)},"evaluation_seeds":p["evaluation"]["seeds"],"canonical_target_digest":hashlib.sha256(json.dumps(p["canonical_targets"],sort_keys=True,separators=(",",":")).encode()).hexdigest(),"decision_rule_digest":hashlib.sha256(json.dumps(p["decision_rule"],sort_keys=True,separators=(",",":")).encode()).hexdigest(),"authorization_rule":p["execution_authorization_requirements"],"note":"R2 corrects the pre-DATA R1 mapping ambiguity. Freeze fixes the scientific contract only; separate explicit human execution authorization remains mandatory."}
    F.write_text(json.dumps(freeze,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    p["status"]="FROZEN_BEFORE_REFERENCE_EXECUTION_AUTHORIZATION"; p["execution_authorized"]=False; p["freeze_authorization"]={"allowed":True,"rule":"All R2 pre-freeze gates passed and are hash-bound. This does not authorize reference evaluation.","reference_runner_implementation_allowed":True,"reference_runner_execution_allowed":False}; p["freeze_record"]=str(F.relative_to(ROOT)); p["freeze_semantics"]="R2 scientific contract is frozen. Reference DATA remain forbidden until a separate explicit human execution-authorization record binds this freeze commit and runner hash."; P.write_text(json.dumps(p,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":p["status"],"execution_authorized":False})); return 0
if __name__=="__main__": raise SystemExit(main())
