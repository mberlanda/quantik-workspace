# QW-027 Decisions

1. **Split from [`QW-021`](../QW-021-opening-coverage-expansion/initiative.md)
   rather than folded into it.** QW-021 is blocked on a real problem — labelling
   plies 4-6 destroys the held-out probe and the 99.63% figure with it, so it
   cannot start until a new partition is designed. Plies 0-2 are **disjoint from
   the probe**, so they carry none of that risk and need not wait. Rejected:
   adding a criterion to QW-021, which would put a seconds-long numpy step behind
   a partition redesign.

2. **Back-induct plies 0-2 from v3's ply-3 rows; do not solve them.** The
   726 ply-3 positions v3 already holds are the *complete* canonical level, which
   is exactly the precondition `induct()` needs. Rejected: a root-only oracle
   solve of the 55 positions — correct, but the per-position cost rises about 7x
   per ply going up (measured: 0.018 s at ply 6, 0.100 s at ply 5, 0.72 s at
   ply 4, 8.75 s at ply 3 on 14 threads), so the empty board alone is hours of
   work to recover a number that back-induction produces in milliseconds.

3. **Convert v1 forward to `optimal_mask`, not v2/v3 back to dense.** Both
   directions are exact, so this is a storage and tooling choice: the mask is 30
   bytes/row against 282, and it is the schema `merge_corpus` already speaks.
   The dense form's only advantage is holding a non-uniform target, and v1's is
   uniform over its support in every row checked, so nothing is given up.

4. **A new file with a new hash, never an in-place rewrite.** The project has
   already published one wrong conclusion by confusing `exact-sampled.npz` with
   `exact-sampled-v2.npz`; a silently-rewritten v1 would be the same failure with
   no name change at all to catch it.

5. **The deliverable is measurement and documentation, not a strength claim.**
   55 positions cannot move a 3.5M-row run, and saying they did would be the
   sixth version of the mistake this initiative documents. Whether shallow
   labels change play is
   [`QW-024`](../QW-024-opening-arena-from-ply-zero/initiative.md)'s question.

6. **Report the random-legal-play baseline beside every policy number.**
   Mass-on-optimal at ply 0 is 1.000 for *any* distribution, because every legal
   move is optimal there. Without the baseline printed next to it, that number
   reads as a perfect score. It is the exact shape of the "uniform on the empty
   board" misreading this initiative exists to correct.
