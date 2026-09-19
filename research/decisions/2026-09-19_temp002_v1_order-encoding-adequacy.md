# TEMP-002 V1 order-encoding adequacy decision

**Date:** 2026-09-19  
**Scope:** RQ-TEMP-002 / H-TEMP-002-A

## Finding

The historical `temporal_order_spiking_v1` runner stores `forward=(0,4)` and `reverse=(4,0)`, but execution checks only whether the current tick is a member of the tuple. Both conditions therefore reduce to the identical stimulation-tick set `{0,4}`.

This means the historical forward and reverse arms cannot constitute a confirmatory test of temporal order. Their existing DATA remain valid records of what was executed, but they must not be promoted as evidence that the network distinguishes A->B from B->A.

## Corrective action

Historical preregistrations, reports and DATA are left unchanged. A new prospective protocol, `PREREG-S1-TEMP-ORDER-V2`, uses two distinguishable input channels, a fixed output decoder and an information-destroyed control while matching event count, timing and total injected charge.

The V2 run remains DATA until human review. It is not an independent replication because it is executed in the same repository and tool chain.
