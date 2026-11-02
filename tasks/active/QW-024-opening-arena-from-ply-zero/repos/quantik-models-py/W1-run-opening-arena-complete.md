# W1 — Run the ply-0 and ply-1 arena and record the numbers

**Repository:** `quantik-models-py` · **Branch:** `feat/opening-arena-results` · one PR
**Dispatch:** execute and record. You are not being asked to interpret the result — W2 does that.

`scripts/evaluate_opening_arena.sh` is **already written and already correct**. Read its header
before running anything: it documents the trap this measurement exists to avoid (deterministic
agents replay one game at ply 0; `temperature 1.0` over the first 4 plies took a pairing from
1/8 distinct games to 40/40), and it already builds the `uniform-mcts` control and defaults
`START_PLIES` to `0 1`. Do not modify the script. If you believe it needs a change, stop and say
so in the handoff.

## Steps

1. Confirm the six checkpoints exist before launching — the script exits on a missing one, but
   finding out four hours in is worse:
   `runs/train/swept-cpool/best`, `runs/train/swept-attn/best`, `runs/train/lineup-resnet/best`,
   `runs/train/lineup-mlp/best`, `runs/train/patience-cpool/best`,
   `runs/train/patience-cpool-v2/best`.
2. Confirm the seed. The script defaults `SEED=20261001`. It must not be `20260829` or
   `20260909` (both spent) and must not be a training seed. `grep -rn "2026" scripts/*.sh docs/`
   and confirm before launching; name the seed you used in the write-up.
3. Run it, sending output to a directory that does not already exist:
   ```sh
   scripts/evaluate_opening_arena.sh runs/eval/opening-ply0 \
     cpool=runs/train/swept-cpool/best attn=runs/train/swept-attn/best \
     resnet=runs/train/lineup-resnet/best mlp=runs/train/lineup-mlp/best \
     patience-cpool=runs/train/patience-cpool/best \
     patience-cpool-v2=runs/train/patience-cpool-v2/best
   ```
4. **Read the `distinct games: worst pairing N/GAMES` line before any win rate.** If `N` is far
   below `GAMES`, the run is not reportable: the win rates rest on fewer independent games than
   were played and every interval is too narrow. Record `N/GAMES` for every start ply. If it is
   low, say so in the write-up and stop — do not report win rates, and do not tune the script to
   make the number look better.
5. Write `docs/opening-arena-ply0.md` containing **only what was measured**:
   - the exact command, seed, `GAMES`, `MCTS_SIMS`, `TEMP`, `TEMP_PLIES`;
   - the distinct-games audit from step 4, per start ply, before any other table;
   - the leaderboards for start ply 0 and start ply 1, policy and MCTS;
   - win rates reported **side-balanced** (as mover and as responder separately, not pooled).
     The seat effect is 68-88% mover / 15-39% responder, larger than any difference expected
     between these checkpoints, so a pooled number is meaningless.
   - `runs/` is gitignored, so the PR contains the document, not the raw outputs. Record the
     output directory path so W2 can read it.

Leave interpretation to W2. No "cpool is strongest" sentences here.

## Completion criteria

- `docs/opening-arena-ply0.md` exists and contains a distinct-games line for every start ply.
- Every win rate in it is split by seat.
- `python -m pytest -q` and `python -m mypy` still clean (you changed no code, so they must be).
- The output directory is named in the document and still on disk.

## Handoff

Record the seed, the full command, wall-clock time, the distinct-games numbers, and the output
directory.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions
win over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, the exact commands you
ran and their real output, and anything you could not finish.
