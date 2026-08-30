# QW-023 Status

**not-started.**

Verified 2026-08-30 from each run's `metrics.jsonl` against its `config.json`:
`patience-cpool` ran 43 of a 60 cap (early-stopped); `patience-cpool-v2` and
`-v3` each ran all 40 of a 40 cap.

Blocked on [`QW-012`](../../completed/QW-012-lineup-under-patience/initiative.md) — it is
isolating the epoch budget on the published corpus and the corpus must not move
underneath it.

Next action after that: the smoke test, then one training run.

Related: [ADR 0014](../../../docs/adr/0014-corpus-coverage-and-epoch-budget-are-separate-axes.md),
[`QW-021`](../QW-021-opening-coverage-expansion/initiative.md) (which this
initiative's result either motivates or deflates).
