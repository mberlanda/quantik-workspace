# QW-021 Status

**not-started.**

Verified 2026-08-30 — `quantik-models-py/runs/canonical/` contains `level01.npy`
through `level08.npy`, `counts.json` and `count.log`. The enumerations exist; the
labelling does not.

Blocked on [`QW-012`](../../completed/QW-012-lineup-under-patience/initiative.md) by decision 5.

Next action, and it costs no compute: design the replacement train/test partition and
write it down. Everything expensive is downstream of that document.

## 2026-08-30: two abandoned solves already exist, and the campaign is smaller than assumed

Found while auditing `runs/` for [`QW-025`](../../completed/QW-025-dev-data-dataset-repo/initiative.md).
`scripts/solve_opening.py` is written, correct, and was run twice — and both runs
were stopped and never resumed:

| directory | frontier ply | to solve | solved | |
|---|---|---|---|---|
| `runs/oracle/opening` | 6 | 901,916 | 10,000 | 1.1% |
| `runs/oracle/opening5` | 5 | 105,632 | 64,000 | 60.6% |

Both counts are exact multiples of the oracle's `CHUNK = 2_000` flush size, so
both processes stopped cleanly between flushes rather than crashing mid-write.
The output is intact and **resumable**: `exact_oracle`'s `--append-to` reads the
existing JSONL and drops those QFENs from its input.

Neither run reached `opening-exact.npz`, which is why the opening book has
contributed **zero rows** to any corpus. `solve_frontier` raises if any frontier
position is unsolved, so nothing partial ever leaked into training — the
abandoned work is missing, not wrong.

The enumerations in `runs/oracle/opening/level0{1..6}.npy` are byte-identical to
`runs/canonical/`, so the two directories are the same data under two names.

## The per-level cost measurement decision 6 asks for

Root-only solve, 14 threads, sampled from each canonical level:

| ply | positions in level | s/position | n sampled | full level |
|---|---|---|---|---|
| 3 | 726 | 8.75 | 20 | ~1.8 h |
| 4 | 10,946 | 0.722 | 200 | ~2.2 h |
| 5 | 105,632 | 0.100 | 200 | ~2.9 h |
| 6 | 901,916 | 0.018 | 200 | ~4.5 h |

**The per-position cost falls about 7x per ply while the level grows about 9-14x,
so the total cost per level is nearly flat.** That inverts the natural reading of
decision 6: the ply-6 frontier has 8.5x more positions than the ply-5 one and
costs only about 1.5x more wall-clock, while yielding strictly more (exact policy
at ply 5 as well as ply 4). It also means an estimate taken at one ply is wrong
by roughly an order of magnitude at the next — the failure decision 6 was written
to prevent, now measured rather than feared.

Resuming from what is already on disk:

- `opening5` — 41,632 positions remaining, **about 70 minutes**. Yields exact
  values at plies 0-5 and exact policy at plies 0-4.
- `opening` — 891,916 remaining, **about 4.5 hours**. Yields exact values at
  plies 0-6 and exact policy at plies 0-5.

The second is the better target and the recommendation, on the strength of the
flat cost above. Neither is the multi-day campaign this initiative was scoped
against.

## Plies 0-2 no longer need a solver at all

[`QW-027`](../QW-027-corpus-label-structure/initiative.md) establishes that v3
already holds the **complete** canonical ply-3 level, so plies 0, 1 and 2 —
55 positions in total — back-induct from it exactly, in seconds of numpy, with no
oracle time. They are also disjoint from the held-out probe, so they carry none
of the partition risk that blocks this initiative.

Acceptance criterion 2 names plies 0-2 as the coverage that matters. That part is
now separable and should land in QW-027 first; what stays here is plies 4-6,
which is where the probe problem actually lives.

Full history: [`workstreams-archive.md`](../../../docs/history/workstreams-archive.md) §10.
