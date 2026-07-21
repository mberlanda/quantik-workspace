# Domain Glossary

- QFEN: four-rank human-readable piece-only board notation.
- Plane/bitboard: one 16-bit occupancy mask for one player/shape pair.
- Action index: shape-major policy slot, `shape * 16 + position`.
- D4: eight rotations/reflections of the square.
- Canonical state/key: deterministic representative/serialized identity under declared symmetries.
- Contracts release: SemVer of the whole contracts repository, distinct from wire IDs.
- Wire contract: interpretation identifier such as `selfplay.v1`.
- Candidate source mode: validation of the checked-out release candidate.
- Published mode: validation of the immutable external tag/artifact.
- Release lock: audit mapping from readable tag/interface to full SHA.
