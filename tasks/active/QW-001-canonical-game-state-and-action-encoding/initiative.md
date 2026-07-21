# QW-001: Canonical Game State and Action Encoding Contract

## Motivation

The current repositories agree on the basic 4×4 board, QFEN, eight planes, shape-major 64 actions, and side-to-move value. Compatibility evidence is fragmented. The engines have layered invalid-state behavior, symmetry/canonicalization details are not fully contracted, and models lacks D4 action remapping.

## Desired behaviour

Contracts will define readable JSONL cases and bulk Arrow/Parquet records that carry state, side to move, legal actions, action ordering/indices, transform identity, canonical state/key, legal mask, policy target, value perspective, contract release, and generator metadata. The workspace coordinates repository-owned adapters; it will not implement game logic.

## Constraints

- Preserve the existing wire IDs unless a breaking interpretation requires a new major ID.
- Do not infer colour-swap equivalence, stalemate semantics, or portable numeric hashing without a decision and fixtures.
- Make every transform's action-index mapping explicit.
- Keep JSONL small/readable and use Arrow/Parquet for high-volume records.
- Candidate validation must use checked-out contracts source before any exact tag exists.

## Migration and compatibility

Start with fixtures describing current behavior, classify differences, decide ambiguities in `decisions.md`, then add adapters behind focused tests. Additive metadata must remain readable by current readers or use a new contract. Record cross-produced/cross-consumed files as evidence.

## Release strategy

Contracts first; engines may proceed in parallel after the candidate fixture shape is approved; models follows the stable action/tensor interpretation. A combination is not `supported` until exact commits, fixtures, and commands are recorded.

## Exclusions

No engine implementation, model architecture redesign, opening-book search algorithm, custom agent runtime, or source-code monorepo move belongs here.
