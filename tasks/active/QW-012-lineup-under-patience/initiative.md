# QW-012: Re-run the Architecture Lineup Under --patience

> **Purpose:** Re-run the four-architecture lineup to convergence instead of a
> fixed sixteen-epoch budget, and settle whether the cpool/attn tie survives.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/repositories/quantik-models-py.md`](../../../context/repositories/quantik-models-py.md)

## Problem and motivation

This is the same class of flaw as the learning-rate issue the training program
(QW-014) already paid for once: a hyperparameter inherited from the first
architecture (the ResNet) produced a plausible, detailed, statistically
significant story that was not true once corrected. `attn` had not converged at
sixteen epochs; its `0.9879` IID top-1 is a floor, not a measurement, and it is
currently ranked second on policy accuracy with a number known to be
understated.

## Existing and desired behaviour

Existing: `--patience N` (py#38) stops on a stale combined validation loss;
`--epochs` becomes a cap; off by default, so every published run still
reproduces exactly. `patience-cpool-{v2,v3}` already exist on disk as two
40-epoch `--patience 5` runs — `patience-cpool-v2` may already be the `cpool`
arm of this initiative's target run; check its `config.json` before spending
compute on it. Desired: all four architectures trained the same way, evaluated
with `scripts/evaluate_lineup.sh` under a fresh arena seed, and the write-up
updated everywhere it currently states a fixed-budget number without that
qualifier.

## Contracts and repositories

`quantik-models-py` only. No contracts are touched — this changes a training
protocol and its evaluation, not any wire format.

## Constraints and preserved invariants

- A tie does not buy more epochs — `best/` is rewritten only on strict decrease.
- `T_max` stays the cap; a generous `--patience` is the fix, not schedule
  rescaling, and `--epochs 60 --patience 5` is a different run from `--epochs
  22`, distinguished by the recorded `epoch_cap`.
- Do not change `--patience`'s off-by-default behavior.
- Do not delete or overwrite the fixed-budget checkpoints or
  `runs/eval/swept-2026-08-30/` — published articles quote those numbers.
- Timing must be measured idle, per the standing "verify before long runs"
  practice — a `minimax-d2` figure recorded under load was 4x its idle value.

## Migration and compatibility strategy

Additive: new checkpoints under distinctly-named `runs/train/patience-*`
directories; nothing existing is replaced.

## Release strategy and ordering

The full charter is written up as
[`briefs/lineup-under-patience.md`](../../../../briefs/lineup-under-patience.md)
— that document is the plan; this packet links to it rather than duplicating it.
One PR, atomic commits, merged when CI is green.

## Risks and exclusions

Excludes a second training seed — explicitly the *next* piece of work once this
protocol question is settled, not part of this initiative. Excludes any
architecture change (separate policy/value trunks, ply embedding, etc.) — those
are only in scope if this initiative's own result motivates them.

## Acceptance criteria

See `manifest.yaml`.
