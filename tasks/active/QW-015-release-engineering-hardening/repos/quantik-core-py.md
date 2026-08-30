# quantik-core-py

## Objective

Same as `quantik-core-rust`: drop `expected-release` from the PR-time job.

## Dependency

Blocked on `quantik-core-contracts` landing criteria 1 and 2.

## Completion criteria

- The PR-time workflow calls the action without `expected-release`.
- A PR touching only Python goes green while `quantik-core-rust` is on a different
  release. This is the concrete demonstration that the deadlock is gone.
