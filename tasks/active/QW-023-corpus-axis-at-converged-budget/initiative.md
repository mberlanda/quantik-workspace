# QW-023: Settle the Corpus Axis at Converged Budget

> **Purpose:** Run the one experiment that separates corpus coverage from epoch
> budget with both arms converged.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`docs/adr/0014-corpus-coverage-and-epoch-budget-are-separate-axes.md`](../../../docs/adr/0014-corpus-coverage-and-epoch-budget-are-separate-axes.md)

## Problem and motivation

[ADR 0014](../../../docs/adr/0014-corpus-coverage-and-epoch-budget-are-separate-axes.md)
concludes that shallow-ply coverage is real and corpus-caused. The evidence is
good enough to overturn the previous conclusion and **not** good enough to be the
final word, because of an asymmetry in the runs it compares:

| run | corpus | cap | ran | converged? |
|---|---|---|---|---|
| `patience-cpool` | v1 | 60 | 43 | **yes** |
| `patience-cpool-v2` | v2 | 40 | 40 | **no — hit cap** |
| `patience-cpool-v3` | v3 | 40 | 40 | **no — hit cap** |

So the finding is "a converged v1 run loses to non-converged v2/v3 runs on
shallow accuracy". That is *stronger* evidence for the conclusion than a
symmetric comparison would be — the v2 arm was handicapped and still won — but it
is not the clean experiment, and the project has now been wrong twice about this
corpus by reasoning from comparisons that moved more than one thing.

## Existing and desired behaviour

Existing: no converged run exists on `exact-sampled-v2.npz`.

Desired: one, at a cap high enough that early stopping is the expected outcome,
compared against `patience-cpool` in a single arena.

## Why v2 and not v3

ADR 0014's second finding is that the v2 → v3 increment is null at matched
budget. Training v3 here would spend the compute on the increment already known
to buy nothing. **v2 is the smallest artifact that demonstrates the effect**, and
that is what makes it the right arm.

## Contracts and repositories

`quantik-models-py` only. No contracts. This is a training protocol and its
evaluation.

## Constraints and preserved invariants

- **The arena is the ranking that matters.** Held-out accuracy has failed to
  predict play strength five times. Report both; conclude from the arena.
- **The seat dwarfs the model** — mover 68-88%, responder 15-39%. Side-balanced
  or the result is unreadable.
- **A run that hits its cap is not converged** and must not be reported as one.
  This initiative exists because that distinction was lost once already.
- **One seed throughout is a known limitation**, not a finding. Say so.
- **Smoke-test before the long run.** A 120-epoch cap is a long run.

## Ordering

After [`QW-012`](../../completed/QW-012-lineup-under-patience/initiative.md), which is
isolating the epoch budget on a fixed corpus and must not have the corpus moved
underneath it.

## Provenance

Raised by the 2026-08-30 v3 investigation as the experiment its own
recommendation rests on being run.
