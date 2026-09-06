# QW-028: Finish the Opening Book Solve

> **Purpose:** Resume the exact opening solve that was written, run twice, and
> abandoned both times — and produce the artifact it was always supposed to
> produce.
> **Load with:** [`QW-021`](../QW-021-opening-coverage-expansion/initiative.md),
> [`QW-027`](../QW-027-corpus-label-structure/initiative.md)

## Problem and motivation

`quantik-models-py/scripts/solve_opening.py` implements a complete and correct
idea: solve every position at one frontier ply with a *root-only* oracle call —
25x cheaper than the full oracle, which solves once per legal move — then
back-induct upward, because a position's value is the best of its children's
negated values and its optimal moves are exactly those leaving the opponent lost.

It was run twice. Both runs were stopped and neither was resumed:

| directory | frontier ply | to solve | solved | |
|---|---|---|---|---|
| `runs/oracle/opening` | 6 | 901,916 | 10,000 | 1.1% |
| `runs/oracle/opening5` | 5 | 105,632 | 64,000 | 60.6% |

Both counts are exact multiples of the oracle's `CHUNK = 2_000` flush size, so
both processes stopped cleanly between flushes rather than crashing mid-write.
`exact_oracle --append-to` reads the existing JSONL and drops those QFENs from
its input, so **both resume from where they stopped**.

Neither reached `opening-exact.npz`. **The opening book has therefore contributed
zero rows to any corpus**, which is the mechanical reason behind the coverage
gap every other initiative here is working around.

The failure was silent in the good way and invisible in the bad way. Nothing
partial ever leaked into training, because `solve_frontier` raises if a single
frontier position is unsolved. But nothing was produced either, and no check
anywhere says "this directory holds an unfinished solve".

## The cost, measured rather than assumed

Root-only solve, 14 threads, on an otherwise idle machine:

| ply | positions in level | s/position | n sampled | full level |
|---|---|---|---|---|
| 3 | 726 | 8.75 | 20 | ~1.8 h |
| 4 | 10,946 | 0.722 | 200 | ~2.2 h |
| 5 | 105,632 | 0.100 | 200 | ~2.9 h |
| 6 | 901,916 | 0.018 | 200 | ~4.5 h |

**Per-position cost falls about 7x per ply while the level grows 9-14x, so the
total per level is nearly flat.** That inverts the intuitive reading: the ply-6
frontier holds 8.5x more positions than the ply-5 one, costs roughly 1.5x more
wall-clock, and yields strictly more — exact policy at ply 5 as well as ply 4.

Remaining work on what is already on disk:

- **`opening5`** — 41,632 positions, about **70 minutes**. Exact values at plies
  0-5, exact policy at plies 0-4.
- **`opening`** — 891,916 positions, about **4.5 hours**. Exact values at plies
  0-6, exact policy at plies 0-5.

The second is the recommendation. Neither is the multi-day campaign the opening
work has been informally scoped against.

## Existing and desired behaviour

**Existing.** Two directories of partial oracle output that no tooling reads and
no check reports on. `runs/oracle/opening/level0{1..6}.npy` are byte-identical to
`runs/canonical/`, so the enumerations are duplicated under two names.

**Desired.** `runs/oracle/opening/opening-exact.npz` — every canonical live
position at plies 0-6 with an exact value, and plies 0-5 with an exact
optimal-move mask — merged into the corpus through the normal path, and a
progress line that makes an unfinished solve visible without counting lines by
hand.

## Contracts and repositories

`quantik-models-py`, plus `quantik-core-rust` only if the oracle's resume path
needs work. No contract changes.

## Constraints and preserved invariants

- **This collides with the held-out probe at plies 4-6.** That is
  [`QW-021`](../QW-021-opening-coverage-expansion/initiative.md)'s blocking
  problem and it does not go away here: the *solve* is safe to run at any time
  and produces a standalone artifact, but **merging it into the training corpus
  must wait for the new partition**. Solve now, merge later. Keeping those two
  steps apart is the whole reason this is separable.
- **Do not delete either partial directory.** `opening5` at 60.6% is 3.5 hours of
  solver time and is the cheaper of the two completions.
- **Verify the resume actually resumes** before committing hours to it, by
  running the oracle against the existing JSONL and confirming it reports
  "resuming: N of M already solved" with the right N.
- **Timings under load are meaningless.** The ladder above was measured idle; do
  not re-measure while training or another solve is running.
- **The estimates above are extrapolations from one ply each.** They have already
  failed once in the other direction: a prediction of ~4 minutes for the 51 ply-2
  positions ran well over an hour. Treat the ply-6 figure as a scale, not a promise.

## Ordering

The solve itself is independent and can run any time — it writes only into
`runs/oracle/`. The **merge** is ordered after QW-021's partition design.
[`QW-027`](../QW-027-corpus-label-structure/initiative.md) is unaffected either
way: plies 0-2 back-induct from data already on disk and need none of this.

## Provenance

Found on 2026-08-30 while auditing `runs/` for
[`QW-025`](../../completed/QW-025-dev-data-dataset-repo/initiative.md), by
noticing that `frontier.qfen` held 901,916 lines and `frontier.jsonl` held
10,000.
