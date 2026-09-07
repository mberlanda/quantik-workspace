# W1 — Unfuse `contract_version` from the engine-agreement comparison

**Repository:** `quantik-core-contracts` · **Branch:** `fix/unfuse-contract-version` · one PR
**Dispatch:** mechanical. Exact locations given.

`scripts/validate_opening_book_summary.py` asks two questions with one comparison. Line 118 puts
`contract_version` into the dict `normalize_summary` returns, and `main()` fails at line 142 on
`rust_summary != python_summary`. So *"do the two engines agree about the game?"* silently also
asks *"are both stacks on the same release?"* — two claims with different lifetimes fused into one
equality. **That fusion produced the 1.2.0 release deadlock.** Verified still present 2026-08-30.

## Steps

1. `scripts/validate_opening_book_summary.py:118` — remove `contract_version` from the dict
   `normalize_summary` returns, so the equality at line 142 compares only game facts.
2. Keep `contract_version` available for the `--expected-release` assertion. That check stays; it
   is the other, legitimate question — it just must not ride on the equality.
3. Add a test: two otherwise identical summaries with **different** `contract_version` values
   **pass** the equality and **fail** `--expected-release`. Both halves matter. A test that only
   checks the equality passes would go green if you deleted the release check entirely.

## Completion criteria

```sh
python -m pytest -q
```

- The new test asserts both halves.
- Reverting step 1 makes the new test fail — verify by reverting, watching it fail, then restoring.

## Handoff

Record the test name and the revert check.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
