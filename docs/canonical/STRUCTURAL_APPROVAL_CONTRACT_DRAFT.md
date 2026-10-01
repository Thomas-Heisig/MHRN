# Structural Approval Contract — Draft v0.1

**Contract ID:** `mhrn-structural-approval-v0.1`  
**Status:** `DESCRIPTOR_IMPLEMENTED_BARRIER_ALIGNMENT_PENDING`  
**Research questions:** `RQ-STRUCT-APPROVAL-001`, `RQ-CUDA-STRUCT-001`  
**Scientific evidence:** none created by this contract

## Purpose

Wave 6 binds the already existing MHRN self-organization pieces into one
fail-closed authorization contract. This is a governance/semantics draft, not a
new structural-plasticity algorithm.

Existing implementation pieces already include proposal generation,
`ProposalApprovalPolicy`, `SelfOrganizationCoordinator`,
`StructuralPlasticityEngine`, durable `StructuralJournal`, and inverse-record
undo. The missing step is a single versioned rule for when those pieces may be
allowed to mutate topology, especially across CPU/CUDA execution segments.

## Approval modes

The executable descriptor supports four modes:

- `DISABLED`: no structural mutation authority.
- `MANUAL_ONLY`: requires an explicit manual authorization in addition to all
  safety/barrier/journal/freeze gates.
- `POLICY_AUTO`: requires enabled, non-dry-run auto-approval policy plus the
  same hard gates.
- `PREREGISTERED_AUTO`: additionally requires the exact policy artifact to be
  frozen by the governed protocol.

Human authorization never bypasses safety limits, a missing structural barrier,
an unhealthy journal, or a scientific freeze.

## Stable policy provenance

`structural_policy_artifact_hash()` hashes the complete structural config,
contract ID and approval mode through canonical JSON with sorted keys. Changing
mode or policy parameters changes the hash.

## Required structural barrier

The target Wave-6 execution sequence is:

```text
complete execution segment
 -> synchronize backend
 -> export structural metrics
 -> SelfOrganizationPolicy -> StructuralProposal
 -> mode-specific authorization
 -> safety/cooldown/kind/resource checks
 -> StructuralPlasticityEngine / Manipulator
 -> StructuralJournal append + commit
 -> increment topology generation
 -> rebuild canonical topology / CSR / schedules
 -> checkpoint + invariant verification
 -> next execution segment
```

No direct mutation inside a running cooperative CUDA kernel is authorized by
this draft.

## Journal and undo semantics

The current journal already stores monotonic sequence IDs, tick, proposal ID,
approval provenance, automatic/manual flag, mutation payload and optional
neuron snapshots. Records are CRC checked and become authoritative only after a
commit marker. Undo creates and commits an inverse structural record; it does
not erase history.

Wave 6 requires the host barrier to treat journal health as a hard prerequisite
and to preserve stable logical neuron/edge identities across repacking.

## Scientific freeze rule

A confirmatory run must preregister one of:

1. structural mutation disabled;
2. a frozen deterministic approval policy artifact;
3. a predetermined intervention schedule.

Ad-hoc operator changes during a confirmatory run are protocol deviations and
must not be hidden as normal learning.

## Current blockers

- structural host/GPU barrier is not yet wired as one canonical execution path;
- topology-generation update/rebuild verification is not yet bound to this
  descriptor;
- journal health is not yet projected into every mutation call;
- no Human Review has frozen this draft.

Therefore descriptor self-check success does **not** imply
`ready_for_mutation=true`.

## Evidence boundary

This draft creates no DATA, EVID or structural-plasticity validity claim. It
defines authorization semantics and fail-closed preconditions only.
