# QW-024 run sheet — the opening arena

Everything needed to run this by hand. Commands are from the
`quantik-models-py` checkout root.

## Before the long run

The project's rule is a smoke test that confirms the assumption before anything
expensive. Here the assumption is *the games are independent*, and it is false by
default.

```bash
cd /path/to/quantik-models-py

GAMES=6 START_PLIES=0 MCTS_SIMS=16 SEED=20261001 \
  ./scripts/evaluate_opening_arena.sh runs/eval/opening-smoke \
    cpool=runs/train/swept-cpool/best \
    patience-cpool=runs/train/patience-cpool/best
```

**Read the `distinct games: worst pairing N/6` line in each block.** For the
policy arena it should be at or near 6/6. If it is 1/6, the sampling is not
working and every number below it is one game repeated — stop and raise `TEMP`
or `TEMP_PLIES`.

Expect the MCTS block to be worse than the policy block at small `GAMES`;
measured 9/12 at 128 sims and 1/6 at 16 sims. MCTS concentrates its visit counts,
so it needs more games and more simulations before sampling separates the runs.

## The run

```bash
SEED=20261001 GAMES=300 ./scripts/evaluate_opening_arena.sh \
  runs/eval/opening-2026-08-30 \
    cpool=runs/train/swept-cpool/best \
    attn=runs/train/swept-attn/best \
    resnet=runs/train/lineup-resnet/best \
    mlp=runs/train/lineup-mlp/best \
    patience-cpool=runs/train/patience-cpool/best \
    patience-cpool-v2=runs/train/patience-cpool-v2/best
```

Six agents is 30 ordered pairings; `uniform-mcts` adds a seventh to the MCTS arm.

### What it costs

Measured on this machine, CPU:

| arm | s/game | 9,000 games |
| --- | --- | --- |
| `net-policy` | ~0.22 | ~35 min |
| `net-mcts` @128 | ~0.89 | ~2¼ h |

Both start plies, both arms: **about 5½ hours.** `GAMES=150` halves it, and the
distinct-game count matters more here than the raw game count.

### Knobs

| variable | default | when to change it |
| --- | --- | --- |
| `GAMES` | 300 | lower to shorten; check the distinct count still holds |
| `SEED` | 20261001 | must not be 20260829 or 20260909 (spent), nor a training seed |
| `TEMP` | 1.0 | raise if the distinct count is low |
| `TEMP_PLIES` | 4 | raise to sample deeper — but that measures less of the opening |
| `MCTS_SIMS` | 128 | matches the published lineup; changing it breaks comparability |
| `START_PLIES` | `0 1` | `0` alone is faster and answers slightly less |

## Reading the output

Per condition, `runs/eval/opening-2026-08-30/{policy,mcts}-p{0,1}/` holds
`games.json`. For a two-model claim use

```python
from quantik_models.arena.pack import pairwise
pairwise(["runs/eval/opening-2026-08-30/policy-p0"], "cpool", "patience-cpool")
```

`pairwise` is side-balanced. `head_to_head` is for a fixed oracle and mixes in
the rest of the card — do not use it for a two-model claim.

## Three things to state in the write-up

1. **The distinct-game count beside every win rate.** Not in a footnote. It is
   the number that decides whether the rate means anything.
2. **Where `uniform-mcts` lands.** If the networks cluster *around* it, no
   network knows anything at ply 0 and QW-010 must rank on something else. If
   they sit clearly above it, there is an ordering to use.
3. **One training seed**, 20260828, across every checkpoint compared. No margin
   here has a run-to-run error bar under it.

## If it comes back null

That is a complete result, not a failed run. Record it, and hand QW-010 the
finding that ply-0 strength does not separate these checkpoints — which is
itself the answer to whether `cpool-v3` deserves a skill level.
