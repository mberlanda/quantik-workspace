# QW-023 Decisions

1. **`--epochs 120 --patience 5`, not 40.** The point is to reach early stopping.
   `patience-cpool-v2` hit 40 with its best at the boundary, which tells you the
   budget bound the result rather than the data. Rejected: 60, matching QW-012 —
   `patience-mlp` and `patience-resnet` both hit 60, so it is demonstrably not
   always enough.

2. **v2, not v3.** ADR 0014 finding 2 makes the v2 → v3 increment null at matched
   budget, so training v3 spends compute on the part known to be worthless. v2 is
   the smallest artifact that shows the effect.

3. **Everything else held to `patience-cpool`:** `cpool/medium`, lr 6e-4, seed
   20260828. One variable.

4. **One arena, both arms, plies 3/6/9.** Rejected: reusing an existing arena
   and comparing across runs. Pairwise side-balanced results are only comparable
   within a run — adding competitors is safe, comparing across seeds is not.

5. **A null result closes this initiative successfully.** If the converged v2 run
   matches `patience-cpool`, ADR 0014's first finding is wrong and must be
   amended. That outcome is recorded, not buried.
