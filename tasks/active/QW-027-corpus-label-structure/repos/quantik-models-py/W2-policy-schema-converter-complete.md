# W2 — v1 dense-to-mask converter that refuses to lose information

**Repository:** `quantik-models-py` · **Branch:** `feat/policy-schema-converter` · one PR
**Depends on:** W1 merged. **Dispatch:** mechanical.

v1 and v2/v3 use incompatible policy schemas, which is why nothing merges them, though the
conversion is exact **when the dense target is uniform over its support**. When it is not, the
mask cannot represent the weighting, and converting anyway silently discards it.

## Steps

1. `src/quantik_models/data/policy_schema.py` — a converter both ways between v1's dense
   float32 `(N,64)` + weight and v2/v3's `uint64 optimal_mask`.
2. **Refuse, loudly, a row whose `policy_target` is not uniform over its support.** Raise with the
   row identifier and what made it non-uniform. Do not warn-and-continue: a silently dropped
   weighting is exactly the class of error this initiative exists to remove.
3. Round-trip test on a **real v1 slice**, not synthetic data: dense → mask → dense must be
   bit-exact for uniform rows.
4. Test that a deliberately non-uniform row raises, and that the message names the row.
5. `action = shape * 16 + position`, 64 slots, bit `i` is action `i`
   (`context/system/canonical-invariants.md#I6`) — assert the bit order explicitly in a test, so a
   future endianness or ordering change fails here rather than in a trained model.

## Completion criteria

```sh
python -m pytest -q
python -m mypy
```

- The round-trip test uses a real v1 slice and asserts bit-exactness.
- The non-uniform refusal test asserts on the message content.
- The bit-order test fails if you reverse the ordering — verify by reversing it, then restoring.

## Handoff

Record which v1 slice you used and the test counts.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
