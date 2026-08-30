# quantik-core-rust

## Objective

Drop `expected-release` from the PR-time job that calls the composite action, once
the action's default is removed.

## Dependency

Blocked on `quantik-core-contracts` landing criteria 1 and 2. Removing the input
before the default is gone changes nothing — the literal still applies.

## Completion criteria

- The PR-time workflow calls the action without `expected-release`.
- A PR touching only Rust goes green while `quantik-core-py` is on a different release.
- The tag build still checks out `quantik-core-py` at the same ref; that ordering is
  unchanged by this initiative and must be shown still working.
