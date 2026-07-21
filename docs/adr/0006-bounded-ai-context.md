# ADR 0006: Bounded AI Context

## Context
Loading every repository is expensive and increases accidental scope.

## Decision
Assemble stable system context, one repository packet, relevant initiative/task/release files, and execution evidence under a configurable approximate token budget.

## Alternatives
Full-repository prompts or opaque vector/database state.

## Consequences
Inputs are reviewable and reproducible. Context packets must be refreshed and generation fails explicitly when over budget.
