# W3 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-003-quantik-models-py` (one PR)

## Objective

# quantik-models-py task

After the Rust runner is stable, invoke it through the canonical pipeline,
validate its artifacts, and publish one coherent self-play workflow document.
Do not implement engine behavior in the orchestration repository.

## Implementation and scope

`allowed_paths` in `manifest.yaml` names the real surface. `decisions` and `invariants` stay empty: decisions.md's five questions (opening policy shape, orientation remapping, engine-pair manifest fields, provenance granularity, seed derivation) are still genuinely open, and none of canonical-invariants.md's entries bear on a self-play runner's scheduling/provenance surface.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
