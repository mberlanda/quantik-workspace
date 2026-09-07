# W1 — quantik-core-contracts

Repository: `quantik-core-contracts`
Branch: `plan/qw-005-quantik-core-contracts` (one PR)

## Objective

# quantik-core-contracts task

During design, classify every proposed feedback artifact as an existing
contract use, additive metadata, derived run manifest, or new wire contract.
Implement contract changes first with fixtures, validators, precedence rules,
and migration notes. Do not encode orchestration policy in schemas.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `search-summary-v1` (the disagreement-evidence candidate) and `opening-book-v1` (the write-back target) doc/schema/fixtures. Provisional — this initiative depends on QW-002, QW-003, QW-004, QW-006 and QW-007 (per `dependencies`, all themselves plan-required), so the real artifact classification decisions.md#1-3 ask for can't be made for real until those land; these paths name where that classification will surface, not a chosen design. `decisions`/`invariants` stay empty.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
