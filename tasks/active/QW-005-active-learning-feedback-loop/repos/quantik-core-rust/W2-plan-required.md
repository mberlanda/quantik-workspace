# W2 — quantik-core-rust

Repository: `quantik-core-rust`
Branch: `plan/qw-005-quantik-core-rust` (one PR)

## Objective

# quantik-core-rust task

After dependencies land, implement only producer/search/book operations assigned
by the approved plan: informative-position export, guided runs, and bounded
write-back with explicit evidence class. Add deterministic, error, and
regression tests and report throughput where it affects pipeline feasibility.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: the existing search-summary and self-play export examples (informative-position export, guided runs) and `opening_book.rs` (bounded write-back), plus a new test file. depends_on W1. Genuinely provisional pending W1's contract and the initiative's five cross-repo dependencies — see W1's note.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
