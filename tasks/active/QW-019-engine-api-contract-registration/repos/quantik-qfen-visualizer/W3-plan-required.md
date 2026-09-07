# W3 — quantik-qfen-visualizer

Repository: `quantik-qfen-visualizer`
Branch: `plan/qw-019-quantik-qfen-visualizer` (one PR)

## Objective

# quantik-qfen-visualizer

## Objective

Validate the requests it sends and the responses it accepts against the registered
schema.

## Inputs

- `src/engines.js:54` — the literal.
- `AGENTS.md` — **mandates a failing test before implementation** for any `src/*.js`
  change.
- `test/index.test.js:13-20` — pins the exact `<script src>` list; a new module must be
  added there or the page test fails.

## Constraints

Dependency-free classic scripts. Do not introduce a bundler or an npm schema validator
for this; a checked-in generated validator or a narrow hand-written check is preferable
to changing the repo's build posture, and that choice must be recorded.

## Completion criteria

- A failing test exists before the implementation, per `AGENTS.md`.
- `npm test` passes with the new module registered in `test/index.test.js`.
- Handoff records how validation was done without adding a runtime dependency.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `src/engines.js` — confirmed the literal `schema: "quantik.engine-request.v1"` around line 54. depends_on W1. decisions/invariants stay empty.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
