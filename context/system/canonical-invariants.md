# Canonical Invariants

Every statement below is evidence-backed; open differences remain explicit.

| Invariant | Authoritative evidence | Implementations/tests | Related contract | Ambiguity |
| --- | --- | --- | --- | --- |
| Board is 4×4; positions 0–15 are row-major | contracts `docs/game-state.md` | Python `commons.py`, QFEN/tests; Rust `constants.rs` | `qfen.v1`, `bitboard.v1` | none found |
| Planes are P0 shapes 0–3 then P1 shapes 0–3 | contracts game-state bitboard order | Python `commons.py`/QFEN; Rust `bitboard.rs` | `bitboard.v1` | none found |
| Shapes 0–3 map A–D; uppercase P0/lowercase P1 | contracts QFEN | Python/Rust QFEN tests | `qfen.v1` | “colour” and “player” terminology varies |
| Each player has two pieces of each shape | engine constants/validators | Python state validator; Rust board inventory | semantic, not fully schema-contracted | parser layers enforce different subsets |
| P0 starts; equal counts means P0, one extra P0 means P1 | contracts side-to-move guidance plus engines | Python state validator; Rust game/board | state/selfplay rows | QFEN alone cannot encode turn |
| Legal placement requires empty target/inventory and no opponent same shape in touched row, column, or 2×2 zone | contracts/domain docs | focused Python move tests; Rust moves/board tests | planned canonical-state contract | low-level constructors differ in strictness |
| Move application sets plane bit and advances turn at board layer | engine APIs | Python move/board; Rust moves/board | planned operation fixture | functional low-level apply may not track inventory |
| Any row, column, or 2×2 zone containing four shapes wins, independent of player colour | contracts/README rules | Python game utils; Rust game masks | planned result fixture | winner attribution on arbitrary invalid states is layered |
| Blocked side loses in high-level board semantics | Python/Rust board result APIs | board/portability tests | not fully contracted | lower-level `is_game_over` may mean winning line only |
| QFEN emits four top-to-bottom ranks with no whitespace | contracts schema/docs | Python/Rust round-trip tests | `qfen.v1` | syntax parsing may accept states later rejected by constructors |
| Durable bitboard order is eight unsigned 16-bit values | contracts game-state/storage docs | both engine adapters | `bitboard.v1` | none found |
| Rust/Python durable state key is version/flags plus eight little-endian u16 planes (18 bytes) | portability evidence and engine serializers | Rust `state.rs`; Python `core.py`/symmetry tests | not a standalone wire ID | overlapping compact formats exist |
| D4 has eight transforms; default canonicalization also considers 24 shape permutations and does not colour-swap | engine symmetry implementations/tests | Python/Rust symmetry tests | canonical behavior not fully contracted | Python API can explicitly colour-swap; docs are misleading |
| Canonical representative is lexicographically least serialized payload | engine code/tests | both engines, portability report | planned canonical-state contract | transform/action mapping needs fixtures |
| Action order/index is shape 0–3 then position 0–15; index = shape×16+position | contracts game-state | both engine tests; models materialization tests | `action-index.v1` | none found |
| Policy vector/mask has 64 slots; mask bit i represents action i | contracts storage/selfplay | engine adapters; models dataset tests | action/selfplay/observation | models sometimes infers mask from positive visits, not all legal actions |
| Self-play/observation value is in [-1,1] from row `side_to_move` perspective | contracts selfplay/observation docs | engine exporters/readers; models materializer/network | `selfplay.v1`, `observation.v1` | decisive self-play uses ±1; observation may be continuous |
| Tensor board is float `[9,4,4]`: planes 0–7 plus all-zero/all-one side-to-move plane | contracts storage docs | Python encoder/tests; models network/tests | `tensor-board.v1` | Rust declares but does not encode tensors directly |
| Durable identity is serialized bytes, not language numeric hash | Rust canonical key and portability report | Python hash is process-dependent | planned canonical-state contract | no portable numeric hash exists |
| Invalid states must fail explicitly at contracted adapter boundary | compatibility policy | engine parsers/constructors currently differ | QW-001 | exact parser-vs-constructor error taxonomy unresolved |

Preserve deterministic JSON field/action order and report all differences. Do not infer a stronger invariant from only one repository.
