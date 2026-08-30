# Domain Glossary

> **Purpose:** Terms a new session actually trips on, across the board-rules layer and the ML layer.
> **Load with:** [`canonical-invariants.md`](canonical-invariants.md) (the facts these terms describe) · [`current-architecture.md`](current-architecture.md) (where each piece lives)

This file is not loaded automatically by `quantik-workspace context ...` — it is reachable
only through the links in `canonical-invariants.md` and `repository-map.md`.

## Board and rules

- **QFEN** — four-rank, human-readable, piece-only board notation: uppercase letters are
  player 0's shapes, lowercase player 1's, `.` empty. No whitespace.
- **Plane / bitboard** — one 16-bit occupancy mask for one player/shape pair; eight planes
  per position.
- **Ply** — one half-move (one placement). Distinct from "turn", which is ambiguous about
  which player's turn.
- **Action index** — the shared 64-slot policy/mask convention: `shape * 16 + position`,
  shapes ordered `A, B, C, D`. `ACTION_COUNT = 64`.
- **D4** — the eight rotations/reflections of the square.
- **Canonical key / the 192 symmetries** — the deterministic representative of a position
  under D4 (8) × shape permutations (24, i.e. 4!) = 192 total transforms, by default
  without colour-swap. The representative is the lexicographically least serialized
  payload; used to deduplicate positions and to canonicalize actions across symmetric
  boards.
- **The exact oracle** — the classical solver (minimax, at a stated depth, or the true
  game-theoretic solve where feasible) that produces ground-truth values and best moves.
  The only source of labels; see `canonical-invariants.md` invariant 4.

## Model / training

- **Mover-relative vs. colour-ordered** — the two incompatible tensor encodings that both
  claim `tensor-board.v1`. Mover-relative orders channels by whose turn it is (what
  training actually uses); colour-ordered orders channels by player identity regardless of
  turn (used by nothing in training). See `canonical-invariants.md` invariant 1 — getting
  this wrong is silent.
- **Policy head** — the network output over the 64 actions (pre-mask logits); combined
  with the legality mask to produce a move distribution.
- **Value head** — the network's scalar estimate of the position, in `[-1, 1]` from the
  side-to-move's perspective. An *estimate*, never a proof — contrast with the exact
  oracle.
- **Corpus vs. probe** — the corpus is the training/validation data: positions merged from
  solved autoplay and oracle labelling. The probe is a disjoint, held-out set of
  oracle-solved positions, deliberately kept out of the corpus, used only to measure
  accuracy off the training distribution (a "shift probe").
- **Shift probe / shift evaluation** — accuracy measured on the probe rather than a
  held-out split of the corpus, i.e. generalization beyond what the corpus's own sampling
  could have leaked into validation.
- **Arena** — engine-vs-engine (or engine-vs-oracle) play used to *rank* agents and to
  *generate positions* for later oracle labelling. Arena results, not held-out accuracy,
  are treated as the measurement that predicts play strength.
- **Seat effect** — the win-rate asymmetry between moving first and second (observed
  roughly 68–88% mover / 15–39% responder), large enough that any win rate not
  seat-balanced is measuring mostly this rather than the models being compared.
- **Opponent id (`model@simulations`)** — the stable name an opponent is addressed by in
  the arena and the play service, e.g. `cpool@128` = the `cpool` architecture checkpoint
  under 128 MCTS simulations. Classical (non-network) opponents use a plain name, e.g.
  `minimax-d2`.

## Release / contracts

- **Contracts release** — the SemVer of the whole `quantik-core-contracts` repository,
  distinct from any single wire ID.
- **Wire contract** — an interpretation identifier such as `selfplay.v1` or
  `quantik.engine-request.v1`.
- **Candidate / source mode** — validation of the checked-out release candidate, before
  tagging. **Published mode** — validation of the immutable external tag/artifact, after
  tagging. See `release-model.md`.
- **Release lock** — the audit mapping from a readable tag/interface to a full commit SHA.
