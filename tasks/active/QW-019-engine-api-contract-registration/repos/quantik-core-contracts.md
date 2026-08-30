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
