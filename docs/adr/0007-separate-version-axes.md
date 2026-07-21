# ADR 0007: Separate Version Axes

## Context
Package versions, contracts releases, wire majors, action refs, and CI expectations have been conflated.

## Decision
Model and validate each axis independently; classify every occurrence before proposing a change.

## Alternatives
Shared version numbers or global replacement.

## Consequences
Drift becomes diagnosable and historical fixtures remain intact. Manifests are more detailed and release tooling must understand source roles.
