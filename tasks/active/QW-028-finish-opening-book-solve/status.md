# QW-028 Status

**not-started.** Discovered and costed 2026-08-30. **Every claim in "Verified"
below was re-checked against the working tree on 2026-09-06 and still holds** —
both solves are untouched at 10,000/901,916 and 64,000/105,632, neither directory
has an `.npz`, and all six `level0N.npy` are still byte-identical to `runs/canonical/`.

## Verified

- Both partial solves exist and their counts are exact multiples of the oracle's
  `CHUNK = 2_000`, so both stopped cleanly between flushes.
- `exact_oracle` implements the resume in `already_solved()` — it parses the
  output JSONL and removes those QFENs from its input.
- `opening-exact.npz` does not exist in either directory, and no corpus contains
  a row from the opening book.
- `runs/oracle/opening/level0{1..6}.npy` are byte-identical to
  `runs/canonical/level0{1..6}.npy`.
- The per-ply cost ladder, sampled idle at 14 threads.

## Not yet verified

The resume has not been exercised end to end. The estimates are single-ply
extrapolations and one has already failed by more than an order of magnitude in
the other direction.

## Next action

Run `exact_oracle --roots-only --append-to runs/oracle/opening5/frontier.jsonl`
against `frontier.qfen` for a few seconds and confirm it prints
`resuming: 64000 of 105632 already solved`. That is the whole precondition.

## Related

- [`QW-021`](../QW-021-opening-coverage-expansion/initiative.md) — owns the
  partition problem that gates the merge.
- [`QW-027`](../QW-027-corpus-label-structure/initiative.md) — plies 0-2, which
  need none of this.
