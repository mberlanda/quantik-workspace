# QW-024 Decisions

1. **`temperature 1.0` over the first 4 plies**, not zero. Measured: it takes a
   policy pairing from 1/8 distinct games to 40/40, and changes the answer from
   100% to 52.5%. Rejected: raising `--start-plies` instead, which is what the
   tool's own warning suggests — it would abandon the question, since ply 0 is
   the thing being measured.

2. **`dirichlet_weight` is not a substitute.** Measured at 0.25 with no
   temperature: still 1/12 distinct. Both are set for the MCTS arm; only the
   temperature does the work.

3. **`temperature` and `temperature_plies` are top-level spec keys.** Under
   `params` they raise `TypeError` for `net-policy` and are silently swallowed
   as an `MCTSParams` field for `net-mcts` — a failure that produces plausible
   numbers. Recorded because it cost a run to find.

4. **Plies 0 and 1, not 0 alone.** Ply 0 has one position and ply 1 has three,
   so they answer slightly different questions about how early differences
   appear, and ply 1 gives the sampling something to work with.

5. **`patience-cpool` and `patience-cpool-v2` are included** alongside the
   published four. They are the converged run on the published corpus and the
   shallow-corpus arm, so if shallow coverage helps in the opening this is where
   it shows. Rejected: the published four alone — it would answer a narrower
   question than the one blocking QW-010.

6. **A null result is a complete result.** If every pairing is indistinguishable
   at ply 0 including `uniform-mcts`, that closes this initiative and tells
   QW-010 to rank on a different criterion. Record it as an outcome.
