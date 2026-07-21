# ADR 0002: Contracts as Interoperability Authority

## Context
Python, Rust, and models exchange states and datasets.

## Decision
`quantik-core-contracts` owns wire schemas, fixtures, validators, and compatibility policy; uncontracted semantics require an initiative.

## Alternatives
Treat Python or Rust as universal authority, or infer compatibility from APIs.

## Consequences
Compatibility is reviewable and executable. Contract work can lag implementation discovery, and ambiguity must be recorded rather than guessed.
