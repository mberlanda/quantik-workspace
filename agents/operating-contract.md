# Shared Operating Contract

## Mission

Complete one scoped Quantik task with verifiable repository evidence. The
workspace coordinates work; implementation remains in the owning repository.

## Required inputs

- assigned task manifest, initiative, decisions, status, and repository task;
- bounded repository/system context;
- closest repository instructions;
- exact starting revisions and dirty state;
- approved contract candidate or published release when required.

If an input is missing, classify it as discoverable evidence, an open decision,
a missing plan, or a blocker. Do not silently invent it.

## Authority

- Read within the assigned namespace and run non-destructive verification.
- Edit only repositories explicitly assigned by the task.
- Preserve pre-existing changes and avoid unrelated cleanup.
- Treat remote writes, review requests, merges, tags, releases, and publication
  as separate actions requiring explicit authority.

## Method

1. Verify the starting revision and task assumptions.
2. Map acceptance criteria to files, behavior, and tests.
3. Resolve required decisions or planning gates before implementation.
4. Make the smallest coherent change, in dependency order.
5. Run focused tests and the repository-owned quality gates proportional to
   risk.
6. Review the final diff for scope, compatibility, security, determinism, and
   documentation.
7. Produce the standard completion report.

## Quality gates

- No claim of completion without exact commands and results.
- No cross-language semantic change without contract fixtures and migration
  analysis.
- No compatibility pass when coverage is missing; classify it as missing.
- No performance claim without a reproducible measurement and baseline.
- No plan-derived implementation unless the plan is approved and current.
- No task created for work already verified as complete.

## Output contract

Return the completed report from `tasks/templates/completion-report.md`, plus
structured handoff evidence when another repository depends on the result.
State assumptions, classified differences, remaining risks, and all remote
actions not performed.
