# QW-001 Decisions

All six decisions below are resolved as of 2026-09-06, grounded in what
`quantik-core-py` and `quantik-core-rust` actually do today (verified by
reading both codebases, not assumed), not invented from scratch. Normative
text lives in `quantik-core-contracts`:

- [`docs/symmetry-transposition.md`](https://github.com/mberlanda/quantik-core-contracts/blob/main/docs/symmetry-transposition.md)
  (decisions 1, 2, 5)
- [`docs/game-state.md`](https://github.com/mberlanda/quantik-core-contracts/blob/main/docs/game-state.md)
  (decisions 3, 4)
- `fixtures/symmetry/symmetry-v1.json` and
  `fixtures/invalid-states/invalid-state-v1.json` (golden cases for all of
  the above)

PRs: [quantik-core-contracts#21](https://github.com/mberlanda/quantik-core-contracts/pull/21) (merged),
[quantik-core-rust#41](https://github.com/mberlanda/quantik-core-rust/pull/41) (merged),
[quantik-core-py#47](https://github.com/mberlanda/quantik-core-py/pull/47) (merged), and
[quantik-models-py#63](https://github.com/mberlanda/quantik-models-py/pull/63) (open, pending CI/merge)
— see status.md.

## 1. Is canonical equivalence D4 × shape permutation only, or does any interface include colour swap?

**Decided: D4 × 24 shape-permutations (192 elements), colour swap excluded.**

Both implementations' canonical key, canonical QFEN, and orbit size already
compute over the full 192-element group in every production call site (TT
keys, opening-book keys, `State.canonical_key()`/`state.rs::canonical_key`,
the portability report). Rust has no colour-swap code at all. Python has a
dormant, opt-in `color_swap` parameter that no production caller ever sets
(only its own unit tests exercise it).

**Rejected alternative:** treat colour swap as part of the portable
canonical form. Rejected because it would collapse a position with its
"mirror-colour" twin into the same canonical key, which breaks every
consumer that currently relies on the canonical key preserving whose pieces
are whose (side-to-move value perspective, opening-book side-specific
statistics) — and neither implementation does this anywhere today, so
adopting it would be a new behavior invented for this task, which the
initiative's constraints explicitly forbid.

**Correction, not just a decision:** `quantik-core-contracts`'
`docs/symmetry-transposition.md` previously documented only the 8-element
D4 group. That was wrong relative to both implementations' real, already
cross-language-identical behavior (Rust's `book_export.rs` even asserts the
18-byte key is "byte-identical to the Python implementation's"), so the
fix is to the doc, not the code.

## 2. How is a move/action mapped to and from every canonical transform?

**Decided:** a portable `transform_index = d4_index * 24 + shape_perm_index`
(0..191, where `shape_perm_index` indexes the 24 permutations of `(0,1,2,3)`
in lexicographic order — provably the same order in both languages, since
Rust's nested-loop generator and Python's `itertools.permutations` both
enumerate permutations of a sorted input in lexicographic order). Each
implementation exposes:

- `remap_action_index(action_index, transform_index) -> action_index`
- `inverse_transform_index(transform_index) -> transform_index`

**This was a real gap, not just an undocumented decision.** Before this
task: Rust had no action-index-level (or even Move-level) transform mapping
at all — `D4_MAPS`/`SHAPE_PERMS` existed only as private tables inside
`find_canonical`. Python had a `Move`-level `apply_symmetry_to_move`, but no
production code called it (only its own tests) and it operated on `Move`
objects, not the `action-index.v1` integer.

**Rejected alternative:** scope the remap contract to the 8 pure geometric
D4 transforms only (matching the pre-existing, now-corrected doc), leaving
the 24-element shape-permutation half of the group without any contracted
action-index mapping. Rejected because `orbit_size` and `canonical_key`
already depend on the full 192-element group being well-defined and
portable; leaving action-index remapping at 8 elements would make canonical
identity and action remapping travel over different-sized groups, which is
exactly the kind of half-covered contract this initiative exists to close.

## 3. Does terminal include blocked-side loss in every contracted operation, or only board/game APIs?

**Decided: every state/game/adapter-facing terminal check must include it.**
Both implementations already do this everywhere except one low-level,
win-only function per language (`game_utils.is_game_over` in Python,
`game.rs::is_game_over` in Rust) — which must not be named or documented as
a terminal check; it is a win check.

**Rejected alternative:** carve out an exception for the low-level win-only
functions by contracting two different "terminal" concepts (win-only vs.
full-terminal). Rejected as unnecessary complexity: the low-level functions
are implementation details used internally by a couple of call sites, not
part of any registered contract's surface, so simply not calling them
"terminal" resolves the ambiguity without adding a second vocabulary.

## 4. Which invalid-state checks are required at parser, state constructor, and adapter boundaries?

**Decided**, per boundary:

- **Parser** (QFEN string → bitboards): structural only — 4 ranks of 4
  valid characters. Always enforced, in both languages, independent of any
  "strict" flag.
- **Constructor** (bitboards → validated state): full — no overlap, no
  inventory (per-shape max 2) exceeded, turn balance in `{0, 1}`, no
  cross-player same-shape line conflict.
- **Adapter / portability-report**: the same full set as the constructor,
  unconditionally.

**This surfaced two real, not hypothetical, cross-stack gaps**, both fixed
in the `quantik-core-rust` PR:

1. `QuantikBoard::from_bitboard` only checked turn balance and per-shape
   piece counts — not overlap or line conflicts — while Python's
   constructor (`board.py.__init__` → `validate_game_state`) already ran
   all four checks.
2. Rust's portability-report adapter (`bench/portability.rs::project_case`)
   checked only turn-balance parity, skipping the one function
   (`bench/contracts.rs`'s local `validate_bitboard_state`) that did full
   validation. A state with balanced turn count but an illegal
   same-shape/same-line placement (e.g. `"Aa../..../..../...."`) passed
   through the Rust report while Python's already rejected it — an actual,
   reproduced divergence, not a theoretical one.

Both are closed by extracting the full check into
`quantik-core-rust`'s new `validation.rs` module (`InvalidStateReason`,
matching Python's `ValidationResult` names), used by the constructor, the
portability report, and `bench/contracts.rs`. Check order (overlap/
inventory, then turn balance, then placement legality) now matches
`quantik_core.state_validator.validate_game_state` exactly in both
languages.

**Rejected alternative:** require full validation at the parser boundary
too (reject malformed game states directly from the QFEN string). Rejected
because both implementations already treat the parser as intentionally
lenient (Python's `bb_from_qfen(qfen, validate=False)` by default; Rust's
`qfen::bb_from_qfen` never validates game rules), and overlap specifically
cannot even be expressed in QFEN's one-character-per-cell format — the
check has to happen once a `Bitboard` exists, which is the constructor.

## 5. Is the canonical 18-byte key the portable identity, with numeric language hashes explicitly excluded?

**Decided: yes, ratified as-is.** Both implementations already produce the
identical 18-byte layout (`[version:u8][flags:u8][8 × u16 LE canonical
bitboards]`) and never expose a numeric hash (Rust's `#[derive(Hash)]`,
Python's `__hash__` overrides) as a cross-language or persisted identity —
those exist solely for in-process `dict`/`HashMap` keys. No code change was
needed; `docs/symmetry-transposition.md`'s "Transposition Keys" section now
states this explicitly instead of recommending `canonical_qfen` (a string)
as the external key, which undersold what's actually shipped.

**Rejected alternative:** none seriously considered — a numeric hash is
strictly worse (not stable across languages, runs, or Rust/Python hash-seed
policy) for a purpose the byte-level key already serves correctly in both
stacks today.

## 6. Does a self-play legal mask mean all legal actions or only actions with positive visits?

**Decided: no field collision exists, both conventions are ratified as-is.**

- `observation.v1` / `search-summary.v1`'s `legal_action_mask`: the full
  legal-action enumeration, strictly validated as complete in both
  languages (a partial mask is rejected).
- `selfplay.v1`'s `policy`: a genuinely different, separately-named field —
  the visited-action subset from search, validated only as a subset of
  legal moves, never required to be complete. `selfplay.v1` has no
  `legal_action_mask` field at all.

**Rejected alternative:** none — the premise that these two conventions
collide under one name turned out not to hold once both schemas were read;
there was nothing to decide beyond writing this down so the question stops
recurring.

## Explicitly out of scope, found during discovery, not fixed here

- `quantik-core-rust`'s `bench/contracts.rs::observation_v1_row` writes a
  **synthetic one-hot** `policy_visits` (a `1` at the single recorded
  benchmark move, `0` elsewhere) rather than real search-visit counts. This
  is the same defect QW-006 (search-derived policy targets) exists to fix
  from the training-target side; QW-001 did not touch it.
- The near-terminal "blocked side, board not full" fixture case that
  `api-portability-testing.md`'s fixture plan lists as recommended was not
  added to the shared `fixtures/api-portability/game-state-v1.json` in this
  pass (a working QFEN for this case already exists, hand-copied into
  `quantik-core-rust`'s own hermetic integration test —
  `"A..C/bbd./CD.A/.adB"` — but porting it into the actual shared contracts
  fixture, and adding the `move` field both report generators require, is
  a small follow-up, not a blocker for any of the six decisions above).
