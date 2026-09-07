# W3 — quantik-core-py

Repository: `quantik-core-py`
Branch: `plan/qw-015-quantik-core-py` (one PR)

## Objective

# quantik-core-py

## Objective

Same as `quantik-core-rust`: drop `expected-release` from the PR-time job.

## Dependency

Blocked on `quantik-core-contracts` landing criteria 1 and 2.

## Completion criteria

- The PR-time workflow calls the action without `expected-release`.
- A PR touching only Python goes green while `quantik-core-rust` is on a different
  release. This is the concrete demonstration that the deadlock is gone.

## Implementation and scope

**Completed.** `.github/workflows/contracts.yml:68` carries the same "deliberately not set here" comment at the PR-time job; the one remaining `--expected-release 1.3.0` in this file (line 35) is a different, release-time job, which criterion 1 explicitly keeps. Verified in the checked-out repository, not assumed.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
