# Parallel branch integration and Stage-6 starting boundary

Date: 2026-09-14.

## Inspected tips

- Main at integration: `f0fad2f0eedfe0c68753c3f806c993d4b3d076e5`.
- Stage-5 safety: `1cb976e7238b1ed4397166278599e7a5ec6a8bda`.
- Parallel Stage-5 research/frontend: `846f6b3ba3e0d020f4d8fc54fe2773dd4f25b488`.
- Reader branch: `83f97514de528263705326d19882169188f33d9d`, already an ancestor of the combined branch.
- Existing Stage-6 branch: `8a8422687c7a879550a9f4fc3a484bcfcbfa0533`, no unique implementation commits at inspection.

## Collision findings

Both Stage-5 branches have complementary changes. The dated branch modifies the
controlled sensor/actuator path and ExperienceEngine and adds bounded contracts.
The other branch adds a read-only Stage-5 projection, research DATA, publication
addendum, runner and frontend. Their new test and workflow filenames are distinct.
The frontend entrypoint was also edited by the reader work: BOTH imports and
initializations must survive. GitHub's merge combined those disjoint edits without
textual conflict; `test_stage5_branch_integration.py` guards against dropping either.

PR #80 integrates current main into the safety branch. PR #81 integrates the other
Stage-5 branch there, preserving both histories. The combined Stage-5 workflow now
runs tests from BOTH branches together with memory, interoception and reader
regressions. Passing a textual merge alone is not runtime verification. Workflow
results must be observed for the actual integrated commit before declaring checks
green; no full-repository result is inferred from this document.

## Boundaries preserved

Do not rewrite the active parallel branch, force-push, or remove its history.
Stage-5 DATA retain their original generating commit; merging new safety logic
does not retroactively re-run or promote those experiments. The Stage-5 timeline
patch script is not itself evidence that the running timeline has been updated.
No scientific maturity score or evidence acceptance is raised by the merge.

Stage 6 begins on the combined basis. Its first increment corrects memory/predictor
contracts, continuation and frontend data access before attempting neural semantic
memory or claiming a learned multistep world model. The six research objects and
remaining causal experiments are retained in `2026-09-14_STAGE5_CHAT_HANDOVER.md`.
