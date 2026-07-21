# ADR 0005: Repository-Scoped Task Packets

## Context
Cross-repository initiatives otherwise require unbounded context and unclear completion.

## Decision
Decompose each initiative into one task per repository with inputs, outputs, contracts, commands, tests, dependencies, and handoff evidence.

## Alternatives
One global issue or ad-hoc chat history.

## Consequences
Work can proceed independently and survive sessions. Packet maintenance is overhead, and initiative completion requires more than one merged PR.
