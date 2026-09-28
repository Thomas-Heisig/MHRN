# MHRN Structural Mutation Approval Contract v0.1

**Status:** canonical design contract refining the existing SelfOrganizationCoordinator path  
**Scientific evidence:** none created by this document

## Existing invariant

MHRN already uses:

```text
HomeostasisSignal
 -> SelfOrganizationPolicy
 -> StructuralProposal
 -> SelfOrganizationCoordinator
 -> Reject / Manual Approval / Auto-Approval Policy
 -> StructuralPlasticityEngine
 -> Manipulator
 -> StructuralJournal
 -> Undo / Recovery
```

This contract clarifies what "approval" means for future CPU/CUDA structural plasticity.

## Separation of concerns

### Proposal eligibility

`SelfOrganizationPolicy` may decide that a candidate mutation satisfies an algorithmic trigger.

That creates a proposal only.

It is not permission to mutate.

### Safety/policy approval

A deterministic approval policy may authorize a proposal only if all configured hard constraints pass, including:

- proposal kind enabled;
- neuron/edge limits;
- protected population constraints;
- topology/identity invariants;
- resource budget;
- cooldown/hysteresis;
- no active forbidden scientific freeze;
- structural barrier available;
- journal/undo path healthy.

The policy version and config hash are execution provenance.

### Human authorization

Human authorization is required when the experiment or governance mode declares it, especially for:

- confirmatory protocols whose preregistration requires a fixed topology or human-reviewed adaptation rule;
- enabling a new auto-approval policy;
- changing approval thresholds during a governed campaign;
- production/peripheral modes explicitly requiring operator control.

Human authorization does not choose scientific results and does not substitute for algorithmic validity; it authorizes a declared policy or proposal under governance.

## Approval modes

```text
MANUAL_ONLY
POLICY_AUTO
PREREGISTERED_AUTO
DISABLED
```

Default for new structural mechanisms remains fail-closed.

A scientific manifest records the mode, policy artifact hash and whether topology changes are permitted by the protocol.

## CUDA structural barrier

No structural mutation commits inside a neural tick or inside an executing cooperative kernel.

Normative sequence:

```text
complete execution segment
 -> synchronize backend
 -> export structural metrics
 -> create StructuralProposal
 -> coordinator approval/rejection
 -> StructuralPlasticityEngine
 -> Manipulator
 -> StructuralJournal commit
 -> rebuild canonical topology/CSR
 -> increment topology_generation
 -> rebuild schedule/packed state
 -> verify hashes/invariants
 -> start new execution segment
```

## Identity rules

Approved mutation must preserve stable logical neuron IDs and stable edge IDs for surviving entities.

New entities receive new IDs. Deleted IDs are not silently reused within the same lineage.

CSR positions, physical GPU slots and schedule bucket positions are derived runtime state.

## Scientific freeze rules

A confirmatory run must preregister one of:

- structural mutation disabled;
- a fixed deterministic proposal/approval policy;
- a predetermined structural intervention schedule.

Unregistered operator decisions during the run invalidate confirmatory status and are recorded as protocol deviation.

## Negative controls

The canonical test suite must include rejection for:

- proposal without coordinator approval;
- mutation during an active tick/kernel;
- mutation with unhealthy journal/undo path;
- topology-generation change without a structural journal record;
- surviving identity changed by repacking;
- auto-approval enabled without an explicit policy artifact.
