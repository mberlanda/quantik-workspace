# W2 — quantik-core-rust

Repository: `quantik-core-rust`
Branch: `plan/qw-003-quantik-core-rust` (one PR)

## Objective

# quantik-core-rust task

Design and implement the runner over existing self-play, opening-book, search,
and benchmark APIs. Add focused tests for deterministic seeds, opening
selection, missing/incompatible books, orientation handling, engine pairs,
provenance, and unchanged empty-board compatibility. Run formatting, linting,
and relevant tests and benchmarks.

## Implementation and scope

`allowed_paths` in `manifest.yaml` names the real surface. `decisions` and `invariants` stay empty: decisions.md's five questions (opening policy shape, orientation remapping, engine-pair manifest fields, provenance granularity, seed derivation) are still genuinely open, and none of canonical-invariants.md's entries bear on a self-play runner's scheduling/provenance surface.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
