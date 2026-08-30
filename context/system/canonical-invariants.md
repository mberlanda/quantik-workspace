# Canonical Invariants

> **Purpose:** Facts true across every Quantik repo whose violation is silent — check these before trusting a number or shipping an encoder.
> **Load with:** [`repository-map.md`](repository-map.md) (repo ownership) · [`current-architecture.md`](current-architecture.md) (how these fit together) · [`domain-glossary.md`](domain-glossary.md) (terms used below) · [`release-model.md`](release-model.md) (the versioning invariant)

This file is loaded into every repository and every initiative bundle — keep additions
short and evidence-backed rather than exhaustive. Repository-specific detail belongs in
`../repositories/<repo>.md`, not here.

## Silent-failure invariants

These do not raise an error when violated. The system keeps running.

1. **`tensor-board.v1` is ambiguous — two incompatible encodings share the name.**
   Everything in training uses `fastboard.encode_tensors`: float32 `(9,4,4)`, channels
   0–3 the side-to-move's shapes, 4–7 the opponent's, channel 8 the side-to-move flag
   broadcast over the board — **mover-relative**. `quantik_core.ml_data.qfen_to_tensor`
   and `fastboard.to_core_tensor` are **colour-ordered** (channel 0 is always player 0's
   shape A) and are used by nothing in training. Building to the wrong one produces a
   model that plays legally and confidently wrong on half of all positions, with nothing
   indicating a fault. **Discriminating fixture:** QFEN `"A.../..../..../...."` — one
   piece, so `side_to_move == 1` (parity of pieces on the board) — puts that piece's bit
   at channel 4 under mover-relative, channel 0 under colour-ordered. This already
   produced one wrong document in three places (`quantik-api-rust/docs/model-serving.md`,
   corrected 2026-08-28). *Verified 2026-08-30 against
   `quantik-models-py/src/quantik_models/env/fastboard.py`.*

2. **Quantik has no draws.** Both terminal conditions — a completed line
   (`win_condition`) and no legal reply (`no_legal_moves`) — are losses **for the side to
   move**, so the winner is always the last mover. `win_probability = (value + 1) / 2` is
   therefore exact. *Verified against `fastboard.terminal_status` and
   `quantik_models/play/service.py`'s `win_probability` field, 2026-08-30.*

3. **Legality masking lives outside the model, by design.** The rules are exact in
   `quantik-core`; the network never has to approximate them, and no engine in this
   project can return an illegal move.

4. **Game outcomes never become labels.** Only positions travel to the corpus — from
   autoplay and from human games alike. Labels come only from the exact oracle. See
   `domain-glossary.md` for corpus vs. probe.

5. **Contracts are the source of truth.** Schemas live in `quantik-core-contracts`; code
   is validated against them, never the reverse.

6. **Action index is `shape * 16 + position`; `ACTION_COUNT = 64`; shapes are `"ABCD"`.**
   Board positions are 0–15, row-major. Policy vectors and legality masks are 64 slots,
   bit/slot `i` is action `i`.

## Engine-level invariants (evidence table)

| Invariant | Evidence | Open ambiguity |
| --- | --- | --- |
| Bitboard planes are P0 shapes 0–3 then P1 shapes 0–3 | contracts `bitboard.v1`; both engines | none found |
| Shapes 0–3 map A–D; uppercase = P0, lowercase = P1 | contracts QFEN; both engines' QFEN tests | "colour" vs "player" terminology varies |
| Each player has two pieces of each shape | engine constants/validators | parser layers enforce different subsets |
| P0 moves first; side to move is the parity of pieces on the board | contracts + both engines | QFEN alone cannot encode whose turn it is |
| A placement is legal only on an empty square, with a piece left in hand, where the opponent holds no piece of that shape in the touched row, column, or 2×2 zone | contracts/domain docs; focused move tests, both engines | low-level constructors differ in strictness |
| A row, column, or 2×2 zone holding all four shapes wins, independent of colour | contracts/README rules; both engines | winner attribution on arbitrary invalid states is layered |
| QFEN is four top-to-bottom ranks, no whitespace | contracts schema/docs; round-trip tests | syntax parsing may accept states constructors later reject |
| Durable bitboard order is eight u16 values; durable state key is version/flags + 8 little-endian u16 planes (18 bytes) | portability evidence; `state.rs`, `core.py` | overlapping compact formats also exist |
| Canonical key: D4 (8 transforms) × 24 shape permutations = 192 symmetries, no colour-swap by default; representative is the lexicographically least serialized payload | both engines' symmetry tests, portability report | Python API can explicitly colour-swap; some docs are misleading about it |
| Durable identity is the serialized bytes, not a language-native hash | Rust canonical key; Python hash is process-dependent | no portable numeric hash exists |
| Invalid states fail explicitly at the contracted adapter boundary | compatibility policy | engine parsers/constructors differ; QW-001 tracks the exact error taxonomy |

Preserve deterministic JSON field/action order and report all differences. Do not infer a
stronger invariant from only one repository.
