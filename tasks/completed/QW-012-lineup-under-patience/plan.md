# Brief — re-run the architecture lineup under `--patience`

**Repo:** `quantik-models-py` (single repo; nothing else is touched)
**State:** mechanism merged (py#38), lineup not re-run
**Shape:** low ambiguity, low code, **long compute** — the risk is in the protocol, not the diff
**Suggested model:** Sonnet. Escalate to Opus only for the "what counts as convergence" call in step 2 if the runs disagree.

---

## Why this exists

Every published lineup number was measured at a **fixed sixteen-epoch budget**, and
sixteen was chosen when the ResNet was the only architecture in the project. That makes
it the ResNet's budget, inherited by three architectures that never agreed to it.

This is the *same class of flaw* as the learning-rate one, which this project already
paid for once: `cpool` and `attn` had been trained at `2e-3` — the ResNet's default —
and when the rate was swept, **three published conclusions reversed**. An inherited
hyperparameter had produced a plausible, detailed, statistically significant story about
architectural behaviour that was not true. Read
`docs/learning-rate-sweep.md` and the warning box in [`WORKSTREAMS.md`](../../../docs/history/workstreams-archive.md) §11 before
starting, so you know what the failure looks like from the inside.

The specific evidence that the epoch budget is the same flaw:

- **`attn` had not converged at sixteen epochs.** It was still climbing when the budget
  ran out, so its recorded `0.9879` IID top-1 is a **floor**, not a measurement. It is
  currently ranked second on policy accuracy *with a number known to be understated*.
- **`cpool` peaked at epoch 25 and 31** in the two 40-epoch `--patience 5` runs that do
  exist (`patience-cpool-v2`, `patience-cpool-v3`). Both beat their own sixteen-epoch
  versions. `docs/corpus-v3.md` states the conclusion outright: **"Sixteen epochs is not
  a defensible budget for `cpool`."**
- **Overfitting is not the constraint.** Train-minus-validation top-1 at the final epoch
  is under one point for every model in the family, and peak-to-final decay is at most
  0.0012. The models plateau, they do not degrade — so more epochs is low-risk and
  *underfitting* is the live hypothesis.

So: two of four architectures are known to be measured short, and the lineup's headline
finding — that `cpool` and `attn` are tied on policy accuracy — rests on one of them
being cut off mid-climb.

## What is already done, so you do not rebuild it

| | |
|---|---|
| `--patience N` | merged as py#38. Stops when combined validation loss has not improved for N consecutive epochs; `--epochs` becomes a cap. **Off by default**, so every published run still reproduces exactly. |
| `scripts/evaluate_lineup.sh` | regenerates *every* number the comparison rests on in one command — shift evaluation, policy arena at plies 3/6/9, MCTS arena at plies 3/6 with the uniform control. Agent specs are generated from `NAME=CHECKPOINT` arguments, so a stale spec cannot silently measure a superseded checkpoint. |
| `patience-cpool-{v2,v3}` | two 40-epoch `--patience 5` runs on disk under `runs/train/`. **They are NOT reusable as the `cpool` arm** — see the correction below. |
| `registry.ArchitectureEntry.default_lr` | each architecture states its own rate (py#29). Do **not** pass a shared `--lr`. |

## Two implementation decisions already taken — do not relitigate

Both are recorded in [`WORKSTREAMS.md`](../../../docs/history/workstreams-archive.md) §11 and in `docs/retrain-and-finetune.md`:

1. **A tie does not buy more epochs.** `best/` is only rewritten on a *strict* decrease,
   so an epoch that merely equals the best did not produce the weights on disk and must
   not extend the run.
2. **`T_max` stays the cap.** The cosine schedule is fixed before the first step, so a
   run that stops at 22 of 60 never reaches `min_lr` and is slightly understated against
   one that spends its whole budget. **This argues for a generous patience, not for
   rescaling the schedule.** It also means `--epochs 60 --patience 5` and `--epochs 22`
   are *different runs*; the recorded `epoch_cap` is what tells them apart.

## The work

### 1. Smoke test before any long run — mandatory

The user's standing instruction, and it has caught real problems here before. Before
launching four training runs, confirm on a tiny budget that the protocol does what you
think:

- Train one architecture with `--epochs 4 --patience 2` and verify the manifest records
  `patience`, `epoch_cap` and `stopped_early`, and that `stopped_early` is *true* when it
  stops early and *false* when it hits the cap. Both directions.
- Verify `best/` corresponds to the recorded best epoch and not the final one.
- Time one epoch per architecture on a quiet machine, then multiply. **Do not reuse any
  timing recorded in this repo taken under load** — `minimax-d2` was recorded at 1.1 s/move
  under contention and is actually 0.28 s, a 4x error, and `beam-w16`'s 5.7 s/move figure
  was discarded for the same reason. Measure it yourself, idle.

Write the projected wall-clock to the run log before starting. If it exceeds a night,
say so and stop for a decision rather than launching it.

### 2. Train all four to convergence

`--preset medium`, same corpus and split as the published lineup, from scratch, each at
**its own swept rate**: `cpool` and `attn` at `6e-4`, `resnet` and `mlp` at `2e-3`.
Suggested budget `--epochs 60 --patience 5` — generous, per the `T_max` note above.
Seed 20260828, matching the existing family, so this is a budget change and *nothing
else*.

Name them distinctly (e.g. `runs/train/patience-{resnet,mlp,cpool,attn}`) so they never
collide with the fixed-budget checkpoints, which must remain on disk — the published
numbers have to stay reproducible.

**Correction, 2026-08-30 — do not reuse `patience-cpool-v2`.** An earlier draft of this
brief said to check it for reuse as the `cpool` arm. That was wrong, and acting on it
would have produced an invalid lineup. Verified from the `config.json` files on disk:

| run | corpus | epochs |
|---|---|---|
| `patience-cpool-v2` | `exact-sampled-v2.npz` | 40, patience 5 |
| `swept-cpool` (published lineup) | `exact-sampled.npz` | 16 |
| `lineup-resnet` (published lineup) | `exact-sampled.npz` | 16 |

**Different corpora.** Dropping `patience-cpool-v2` into the lineup would compare a
40-epoch run on one corpus against 40-epoch runs on another, confounding corpus with
budget in the single arm the whole exercise is trying to isolate — the same class of
error as the inherited learning rate. Train all four arms fresh on `exact-sampled.npz`.

### 3. Re-run the whole evaluation

```
scripts/evaluate_lineup.sh runs/eval/patience-<date> \
  resnet=runs/train/patience-resnet/best \
  cpool=runs/train/patience-cpool/best \
  mlp=runs/train/patience-mlp/best \
  attn=runs/train/patience-attn/best
```

Use a **fresh arena seed**, not `20260829`. The script's own comment explains why: reusing
a seed makes seed-linked bias invisible rather than absent.

### 4. Report — this is the actual deliverable

The training is mechanical. The write-up is the work. It must state, per architecture:
**the epoch it stopped at, whether it stopped early or hit the cap, and how the new
numbers move against the fixed-budget ones.** Then answer the one question this whole
exercise exists to answer:

> **Does the `cpool`/`attn` tie survive giving `attn` the epochs it wanted?**

Update `docs/decisions/0001-architecture-lineup.md`, the results table in
[`WORKSTREAMS.md`](../../../docs/history/workstreams-archive.md) §11, `docs/shift-evaluation.md` and `docs/autoplay.md`. Every one of
those currently carries a fixed-budget number presented without that qualifier.

## Guard rails — how this goes wrong quietly

- **Do not delete or overwrite the fixed-budget checkpoints or `runs/eval/swept-2026-08-30/`.**
  The published articles quote those numbers; they must stay reproducible.
- **`--patience` is off by default and must stay off by default.** Changing the default
  silently re-defines every future run.
- **Read the multiple-comparisons caveat in `docs/corpus-v3.md` before calling anything
  significant.** Twenty intervals were computed there and six excluded 50% — roughly one
  is expected by chance. The pattern across rows carries the argument, never a single cell.
- **The seat dwarfs the model.** Mover win rates run 68–88%, responder 15–39%. Two
  networks a point apart are being compared inside an effect forty times larger. Keep the
  side-balancing, and do not quote an unbalanced win rate.
- **Held-out accuracy has now failed to predict play strength four times in this project.**
  If validation top-1 and the arena disagree, **the arena is the ranking that matters.**
  Say so in the write-up rather than splitting the difference.
- **One seed, still.** Every checkpoint in this family is seed 20260828. This run does not
  fix that and must not claim to. A second seed is the *next* piece of work and is
  explicitly unblocked by this one finishing (`docs/corpus-v3.md`: "Seeds come after the
  protocol, not before").

## Working agreement

- One PR, atomic commits, merged when CI is green. Do not stack open work.
- Commit as the user only — **no `Co-Authored-By:` or `Claude-Session:` trailers**.
- Documentation lands in the same PR as the numbers it describes.
- If a recommendation is made, the rejected alternatives get written down with it.

## Where to read first

- [`WORKSTREAMS.md`](../../../docs/history/workstreams-archive.md) §11 — "A second methodological flaw", and the learning-rate warning box
- `docs/corpus-v3.md` — the resolution section; this is the precedent for the whole task
- `docs/retrain-and-finetune.md` — `--patience`, `--init-from`, `--freeze`, and two silent failures
- `docs/decisions/0001-architecture-lineup.md` — the ADR this updates
- `scripts/evaluate_lineup.sh` — read it before running it
