# QW-014 Status

Created 2026-08-30, during reconciliation. Largely complete — recorded so its
conclusions are cited, not re-derived.

Verified directly: `docs/architecture-{resnet,mlp,constraint-pool}.md`,
`docs/architectures.md`, `docs/decisions/0001-architecture-lineup.md`,
`docs/learning-rate-sweep.md`, `docs/corpus-v3.md`, `docs/oracle-benchmark.md`,
`docs/shift-evaluation.md`, and `docs/autoplay.md` all exist and match
[`WORKSTREAMS.md`](../../../docs/history/workstreams-archive.md)'s description. Four architectures trained and evaluated three
ways (IID, shift probe, arena); a 12-run learning-rate sweep found and corrected
a shared-rate bug that reversed three published conclusions; `cpool-v3` beats
`minimax-d2` at 59.7% [57.5, 61.8], the first model to do so; the v3 corpus
chain (solve, merge, retrain, evaluate) completed 2026-08-29 and found held-out
policy accuracy did not predict play strength (v3 wins at ply 3 only, ties at
ply 6).

Two things explicitly left open by the program itself, now tracked as separate
initiatives rather than folded back in here:

- **QW-012** — the epoch-budget question (`--patience` merged, lineup not
  re-run under it) that is the leading explanation for v3's deep-band
  regression.
- Publication to the Hub is blocked on QW-012's outcome, not on anything left
  to do in this initiative.

Nothing left to do here beyond keeping this packet's citations current as
QW-012 and QW-013 land.

## 2026-08-30 — closed

This initiative's criteria are record-keeping: the architecture papers, the learning-rate-sweep reversal and the v3 corpus result are all documented with their measurement protocol stated. They are. The genuinely open work it uncovered — re-running the lineup under `--patience` — is QW-012, and a second training seed follows that. Holding this open would track documentation that already exists.
