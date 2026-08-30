# QW-027 Status

**not-started.** Findings measured 2026-08-30; no code written yet.

## Verified

- Policy density (8.10% / 7.98% / 7.72%) and the full per-ply label table, read
  directly from the three `.npz` files.
- The two schemas and their byte costs, from the arrays themselves.
- Lossless conversion: 200,000 of 200,000 labelled v1 rows are uniform over
  their support; `policy_weight` takes only {0, 1}; largest optimal set is 31
  moves, so a uint64 suffices.
- v3's ply-3 rows are the complete canonical level — key-set equality against
  `runs/oracle/opening/level03.npy`, 726 of 726.
- Back-induction to plies 0-2 runs end to end and yields exact masks for all 55
  positions.
- The shallow-probe numbers in the initiative, on five checkpoints.
- Per-position solve cost, sampled at 14 threads: ply 6 0.018 s (n=200),
  ply 5 0.100 s (n=200), ply 4 0.722 s (n=200), ply 3 8.75 s (n=20).

## Not yet verified

The plies 0-2 **values** are induced from v3's ply-3 values, so they inherit
whatever the oracle recorded there. A direct root-only oracle solve of levels 2,
1 and 0 is the independent check and has not completed — level 2 alone is about
15 minutes on 14 threads and the empty board is hours, which is itself the
argument for decision 2. Until it lands, the induced values are consistent with
v3, not independently confirmed.

Nothing in findings 1-4 depends on this. Finding 5's *policy* numbers do not
either — the optimal-move masks follow from the same induction, so they carry
the same caveat, but the near-uniformity of the checkpoints at plies 1-2 is a
property of the checkpoints and holds regardless.

## Next action

Run the direct solve of levels 2 and 1 to confirm, then work item 1.

## Related

- [`QW-021`](../QW-021-opening-coverage-expansion/initiative.md) — this removes
  its plies 0-2 criterion and re-costs its solver campaign.
- [`QW-024`](../QW-024-opening-arena-from-ply-zero/initiative.md) — the arena
  that would read these targets.
- [ADR 0014](../../../docs/adr/0014-corpus-coverage-and-epoch-budget-are-separate-axes.md)
  — finding 1 rules out policy density as a confound in it.
