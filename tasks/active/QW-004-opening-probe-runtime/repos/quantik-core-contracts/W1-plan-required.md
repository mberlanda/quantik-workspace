# W1 — quantik-core-contracts

Repository: `quantik-core-contracts`
Branch: `plan/qw-004-quantik-core-contracts` (one PR)

## Objective

# quantik-core-contracts task

Own the opening-probe design, identifier, schema/format metadata, fixtures,
validators, compatibility policy, and source-book conversion rules. Resolve
action orientation with QW-001 and obtain contract review before Rust work.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: new opening-probe-v1 doc/schema/fixtures (nothing exists yet — verified, no opening-probe.* anywhere in this repo), plus the existing opening-book-v1/opening-book-summary-v1 doc and schema this must define source-book conversion rules against. `decisions`/`invariants` stay empty: decisions.md's five questions (storage format, value shape, transform storage, mandatory metadata, miss/corruption behavior) are still open.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
