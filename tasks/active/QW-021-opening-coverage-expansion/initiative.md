# QW-021: Opening Coverage Expansion — Plies 0 to 6

> **Purpose:** Give the network the opening it has never seen, and pay the price
> deliberately: the held-out probe is the thing being trained on.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/repositories/quantik-models-py.md`](../../../context/repositories/quantik-models-py.md)

## Problem and motivation

The flagship network trained on **zero positions below ply 6**. That includes plies 4
and 5, where the contest actually lives.

The scale is the surprising part. Plies 0-6 hold **1,019,275** canonical live positions
in total — *fewer than the 3,087,356 rows already trained on*. Complete coverage of the
entire opening is a **smaller** corpus than the one that already exists.

The enumerations are already computed. Verified 2026-08-30:
`quantik-models-py/runs/canonical/level01.npy` through `level08.npy` are all present,
alongside `counts.json`. Only oracle labelling is missing, and it is known feasible —
the existing probe already contains 1,240 solved positions at ply 4 and 1,240 at ply 5.

## The caveat, which is the whole difficulty

**Plies 4-6 *are* the held-out probe.** Training on them makes the model stronger and
simultaneously destroys the clean generalization test that produced the 99.63% figure —
a figure that appears in published articles.

This is not a reason not to do it. It is a reason to design the new partition first,
and to treat the write-up as part of the work rather than as cleanup.

## Existing and desired behaviour

Existing: a corpus that starts at ply 6, a probe at plies 4-6, and a clean separation
between them that is currently doing real evidential work.

Desired: full opening coverage, a *new* held-out partition that is honestly held out,
and every claim about the old one either restated or scoped.

## Contracts and repositories

`quantik-models-py` only. `observation.v1` is produced, not changed. The exact oracle in
`quantik-core` does the labelling.

## Constraints and preserved invariants

- **Labels come only from the exact oracle.** Game outcomes never become labels. See
  ADR 0011.
- **Held-out accuracy does not predict play strength.** It has failed to, four times.
  The arena is the ranking that matters, and criterion 4 is not negotiable.
- **The seat effect is larger than most model differences** — mover win rates 68-88%,
  responder 15-39%. Any arena comparison must control for it.
- **A smoke test confirms assumptions before anything expensive.** A million-position
  solve is expensive.
- **Prefer the exact opening book over the network for opening play.** The region is
  small enough to solve completely; the network is least informed exactly there. A
  better-in-the-opening network does not change which one should answer.

## Ordering

Sequenced after [`QW-012`](../../completed/QW-012-lineup-under-patience/initiative.md). QW-012 is
already isolating one variable — the epoch budget — on a fixed corpus. Changing the
corpus underneath it would confound the two, which is the failure QW-012's own packet
was written to avoid.

## Provenance

Migrated from WORKSTREAMS §10 ("Coverage expansion — NOT STARTED, HIGH VALUE"). The
`runs/canonical/` inventory was re-verified 2026-08-30; the position counts are quoted
from `runs/coverage.md` and should be re-derived from `counts.json` before being
published again.
