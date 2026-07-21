# ADR 0001: Workspace as Control Plane

## Context
Quantik implementation repositories need cross-repository intent without source consolidation.

## Decision
Keep independent repositories and store only inventory, tasks, evidence, context, and release state here.

## Alternatives
A monorepo or Git submodules would couple source histories and checkout policy.

## Consequences
Ownership stays clear and repository agents remain scoped. Cross-repository automation must handle missing/dirty sibling checkouts. The drawback is more explicit coordination metadata.
