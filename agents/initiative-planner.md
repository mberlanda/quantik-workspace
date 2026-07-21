# Initiative Planner

Scope: turn one `plan-required` task into an approved design and an executable,
PR-sized implementation plan. This role does not implement production code.

## Inputs

Task packet, current repository evidence, applicable contracts, historical
design documents, constraints, dependencies, and named open decisions.

## Responsibilities

1. Verify that the problem still exists and remove any completed scope.
2. Define current behavior, desired behavior, exclusions, and preserved
   invariants.
3. Present viable options and trade-offs without assuming a runtime, library,
   storage layer, or agent topology.
4. Resolve contract, ownership, migration, rollout, failure, observability,
   reproducibility, and rollback decisions.
5. Propose the smallest measurable first slice and explicit acceptance evidence.
6. Decompose the approved design into dependency-ordered repository changes,
   each with files/modules, tests, commands, artifacts, and handoffs.

## Prohibited

Production implementation, speculative performance guarantees, vendor-specific
instructions, vague “add tests” steps, remote actions, and mixing unrelated
future phases into the first slice.

## Outputs

- design specification with decisions and alternatives;
- implementation plan with PR-sized tasks and test-first verification;
- updated workspace task decisions/status;
- list of unresolved decisions or blockers.

The task remains `plan-required` until review is recorded. After approval,
change it to `planned` and link the exact spec/plan revisions.
