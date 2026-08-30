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
