# W1 — quantik-core-contracts

Repository: `quantik-core-contracts`
Branch: `plan/qw-019-quantik-core-contracts` (one PR)

## Objective

# quantik-core-contracts

## Objective

Register `engine-request` and `engine-response` with schemas and golden fixtures, and
record the naming decision.

## Inputs

- `contracts.json` — the registry.
- `schemas/` and `fixtures/` — the existing pattern; JSONL for golden fixtures per
  ADR 0003.
- The two hardcoded literals, which are the de facto specification to be captured.

## Approach

Capture the format as it is actually spoken today before changing anything. A schema
that does not accept a real captured request is a rewrite, not a registration.

## Completion criteria

- Both contracts appear in `contracts.json` with a schema path and a fixture glob.
- Fixtures include at least one real captured request from the visualizer and one real
  response from each engine kind.
- `validate contracts` passes.
- The naming decision is written in `decisions.md` with its migration.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: new engine-request-v1/engine-response-v1 doc/schema/fixtures — verified `contracts.json` has no entry for either name today, confirming `problem`'s "phantom contracts" premise. This is the prerequisite W2/W3/W4 (and QW-018) depend on. decisions/invariants stay empty: decisions.md's four points are already resolved as unheaded prose except naming (point 3, explicitly left open).

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
