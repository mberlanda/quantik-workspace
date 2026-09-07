# W1 — quantik-core-rust

Repository: `quantik-core-rust`
Branch: `plan/qw-006-quantik-core-rust` (one PR)

## Objective

# quantik-core-rust task

Map each supported search engine's root statistics to the approved observation
policy semantics. Add focused tests for legality, ordering, determinism,
overflow, zero/terminal cases, and engine fallbacks. Keep `search-summary.v1`
diagnostics distinct from per-position training rows.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `bench/contracts.rs` is the exporter named in `problem` (confirmed: `policy_visits` is its field), plus a new test file. `decisions`/`invariants` stay empty: decisions.md's five questions (which engines expose what, cross-engine comparability, zero/tie/terminal representation, fallback marking, adoption metrics) are open.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
