# W2 — quantik-core-contracts

Repository: `quantik-core-contracts`
Branch: `plan/qw-018-quantik-core-contracts` (one PR)

## Objective

# quantik-core-contracts

## Objective

Carry the extended response in the registered `engine-response` schema created by
QW-019, with the new fields optional.

## Approach

Add `candidates`, `principal_variation` and `certainty` to the schema, with
`certainty` constrained to the two-value enum. Fixtures cover one response per engine
kind, including a network response, so a fixture asserts that `estimate` and `proof`
both round-trip and that the enum rejects a third value.

## Completion criteria

- Schema and fixtures land together; the validator accepts the fixtures.
- The enum is closed — a fixture with `certainty: "likely"` is rejected.
- Handoff records the contract version and whether it was a minor addition.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: new `engine-response-v1` doc/schema/fixtures — verified nothing under that name exists in this repo today, confirming `problem`'s premise (hardcoded, unregistered response). This item is itself the prerequisite QW-019 (this initiative's own `dependencies`) needs to land the base contract for — genuinely sequenced, not just cross-referenced. decisions/invariants stay empty.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
