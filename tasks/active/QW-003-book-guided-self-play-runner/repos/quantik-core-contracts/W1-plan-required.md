# W1 — quantik-core-contracts

Repository: `quantik-core-contracts`
Branch: `plan/qw-003-quantik-core-contracts` (one PR)

## Objective

# quantik-core-contracts task

Decide and document the compatible provenance surface for self-play runs. Add
or update schema, fixtures, validation, and migration guidance only if the
approved design changes the wire surface. Keep historical fixtures readable.

## Implementation and scope

`allowed_paths` in `manifest.yaml` names the real surface. `decisions` and `invariants` stay empty: decisions.md's five questions (opening policy shape, orientation remapping, engine-pair manifest fields, provenance granularity, seed derivation) are still genuinely open, and none of canonical-invariants.md's entries bear on a self-play runner's scheduling/provenance surface.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
