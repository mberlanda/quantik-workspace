# W1 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-024-quantik-models-py` (one PR)

## Objective

# quantik-models-py

## Objective

Run the opening arena and write up what it says about ordering at ply 0.

## Inputs

- `scripts/evaluate_opening_arena.sh` — the runner. Read its header first; it
  documents the trap.
- Checkpoints: `runs/train/{swept-cpool,swept-attn,lineup-resnet,lineup-mlp,patience-cpool,patience-cpool-v2}/best`.
- `docs/corpora.md` — why no checkpoint has seen plies 0-2.

## Approach

1. Run at low `GAMES` first and read the distinct-game line. If it is far below
   `GAMES`, raise `TEMP` or `TEMP_PLIES` and repeat. Do not proceed on a bad one.
2. Run the full arena.
3. Report side-balanced rates with Wilson intervals, per start ply, with
   `uniform-mcts` in the same table.

## Completion criteria

- Every reported condition has a distinct-game count close to its game count,
  and that count is stated beside the win rate rather than assumed.
- The write-up answers directly: is there an ordering at ply 0, and does
  `uniform-mcts` sit inside it or below it?
- The single training seed is named as a limitation.
- Handoff records the arena seed, `TEMP`, `TEMP_PLIES`, and the output directory.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `scripts/evaluate_opening_arena.sh` (the runner) and a new write-up doc — no existing doc matches this scope (`docs/benchmarks.md`/`oracle-benchmark.md` are the general figures docs, not this specific measurement), named `docs/opening-arena-ply0.md`. Checkpoints under `runs/train/*/best` are read-only inputs, not touched. decisions/invariants stay empty: decisions.md's six points are already resolved as unheaded prose. Top-level status was already accurate (`ready-to-run`) — untouched.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
