# QW-027: Corpus Label Structure and the Shallow-Ply Floor

> **Purpose:** Write down what the training corpora actually contain, and close
> the two gaps that audit exposed — a policy signal an order of magnitude
> thinner than the row count suggests, and a shallow-ply floor no corpus reaches
> below.
> **Load with:** [`docs/adr/0014-corpus-coverage-and-epoch-budget-are-separate-axes.md`](../../../docs/adr/0014-corpus-coverage-and-epoch-budget-are-separate-axes.md),
> [`QW-021`](../QW-021-opening-coverage-expansion/initiative.md)

## Problem and motivation

Every published number about these models is quoted against a row count —
3.09M, 3.20M, 3.52M. An audit on 2026-08-30 established that the row count
describes the **value** corpus and badly misdescribes the **policy** corpus, and
that the corpora have a floor nobody had written down.

None of this is a defect in the data. It is a set of properties the data has had
all along, which no document states, and which change how three existing results
should be read.

### Finding 1 — about 8% of rows carry a policy label

Measured directly from each `.npz`:

| corpus | rows | policy-labelled | share |
|---|---|---|---|
| `exact-sampled` (v1) | 3,087,356 | 250,000 | 8.10% |
| `exact-sampled-v2` | 3,196,958 | 255,058 | 7.98% |
| `exact-sampled-v3` | 3,520,526 | 271,676 | 7.72% |

The remaining ~92% are value-only. **The density is flat across all three**,
which matters because it rules out a hidden second variable behind ADR 0014: the
v1→v2→v3 comparison does not silently also move the policy/value ratio.

### Finding 2 — the deep-ply label counts are a sampling cap, not coverage

Policy labels per ply are *identical round numbers* in all three corpora from
ply 7 down: 60,000 / 60,000 / 30,000 / 20,000 / 20,000 / 20,000 at plies
7-12, and **zero at ply 13 in every corpus**. Every corpus revision added policy
labels only at plies 3-6.

So "the corpus grew by 323,568 rows" (the v2→v3 step) is not the same claim as
"the policy signal grew", and the two must stop being quoted interchangeably.

### Finding 3 — two incompatible policy schemas

| | v1 | v2 / v3 |
|---|---|---|
| arrays | `policy_target` float32 (N,64) + `policy_weight` float32 (N,) | `optimal_mask` uint64 (N,) |
| bytes/row | 282 | 30 |

They do not concatenate, which is why no tool merges v1 with v2. The conversion
is nonetheless **exact in both directions**, and this was verified rather than
assumed: across 200,000 labelled v1 rows, `policy_target` is uniform over its
support in 200,000 of 200,000 cases and `policy_weight` takes only the values
{0, 1}. The dense array is a 256-byte encoding of a 64-bit set, and the largest
optimal set observed is 31 moves, so a uint64 holds every one of them.

### Finding 4 — no corpus reaches below ply 3

v1 starts at **ply 6**. v2 and v3 start at **ply 3**. Plies 0, 1 and 2 are
**55 canonical positions in total** — 1, 3 and 51 — and no model has been
trained on one of them.

Coverage of the shallow region, against the canonical level sizes:

| ply | canonical live | in v3 | |
|---|---|---|---|
| 0 | 1 | 0 | — |
| 1 | 3 | 0 | — |
| 2 | 51 | 0 | — |
| 3 | 726 | 726 | complete |
| 4 | 10,946 | 9,758 | 89% |
| 5 | 105,632 | 29,905 | 28% |
| 6 | 901,916 | 170,766 | 19% |

### Finding 5 — "uniform on the empty board" is the correct answer, and the real evidence is one ply deeper

The empty board is a **loss for the mover** under perfect play, so every legal
move is equally optimal and the exact policy target *is* uniform over all 64.
A checkpoint that outputs a uniform distribution there is right. The observation
that every checkpoint does so is therefore not evidence of anything.

The evidence is at plies 1 and 2, where the exact target is sharp. Measured
against back-inducted exact targets, with the random-legal-play baseline stated:

| | ply 1 mass-on-optimal | ply 2 mass-on-optimal | ply 2 value sign |
|---|---|---|---|
| *random legal play* | **0.170** | **0.331** | — |
| `lineup-cpool` | 0.160 | 0.336 | 37/51 |
| `v3-cpool` | 0.381 | 0.357 | 8/51 |
| `lineup-attn` | 0.189 | 0.356 | 24/51 |
| `lineup-mlp` | 0.023 | 0.520 | 43/51 |
| `lineup-resnet` | 0.204 | 0.440 | 44/51 |

The flagship `cpool` checkpoints are **indistinguishable from random legal play**
on shallow policy, `mlp` is seven times *below* chance at ply 1, and the value
head disagrees across architectures by 8/51 versus 44/51 on the same 51
positions. These are the same checkpoints that score 99.6% on the held-out
probe. This is the sixth time held-out accuracy has failed to describe
behaviour, and the first time it has been measured on positions no corpus
contains.

### Finding 6 — the floor closes with zero solver time

Back-induction needs only the values one ply deeper, and v3 already holds the
**complete** canonical ply-3 level (726 of 726, verified by key-set equality
against `level03.npy`). Inducting down from it yields exact values and exact
optimal-move masks for all 55 positions at plies 0-2 in seconds of numpy, using
the `induct()` function that already exists in `scripts/solve_opening.py`.

This has been run end to end. It is the cheapest gap in the project.

## Existing and desired behaviour

**Existing.** `docs/` describes the corpora by row count and ply range and says
nothing about policy density, the per-ply label caps, the two schemas, or the
floor. `data/merge_corpus.py` cannot combine v1 with v2/v3 and no document says
why.

**Desired.** One document that states all four properties with the numbers
above; a converter that makes v1 mergeable; and the 55 shallow positions
labelled and folded in through the normal corpus path.

## Contracts and repositories

`quantik-models-py` only. No contract changes: `observation.v1` pins the tensor,
not the corpus layout, and both policy schemas are internal to the `.npz`.

## Constraints and preserved invariants

- **The probe stays held out.** Plies 0-2 are disjoint from it, so this
  expansion does not have QW-021's partition problem — that is precisely why it
  is separable from QW-021 and can land first.
- **The arena is the ranking that matters.** Any claim that shallow labels help
  is settled in [`QW-024`](../QW-024-opening-arena-from-ply-zero/initiative.md),
  not on held-out accuracy.
- **55 positions will not move a 3.5M-row training run on their own.** The
  deliverable is the *measurement* and the *documentation*; a strength claim is
  out of scope here and belongs to QW-021.
- **Identify a corpus by its hash.** Any converted v1 artifact is a new file
  with a new hash, never an in-place rewrite.

## Ordering

Independent of QW-012 and QW-023 — it touches no training run. It should land
**before** [`QW-021`](../QW-021-opening-coverage-expansion/initiative.md), whose
plies 0-2 criterion this reduces from a solver campaign to a numpy step, and
before [`QW-024`](../QW-024-opening-arena-from-ply-zero/initiative.md), which is
the arena that would read these targets.

## Provenance

Raised by the 2026-08-30 dev-data audit
([`QW-025`](../../completed/QW-025-dev-data-dataset-repo/initiative.md)) while
cataloguing what `runs/` holds.
