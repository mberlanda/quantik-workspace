# W1 — Take the length decision and re-check the claims

**Repository:** `articles` · **Branch:** `docs/deadlock-publication-ready` · one PR
**Blocked on:** QW-015 W1 merged (it changes the line numbers this article cites).
**Dispatch:** judgment.

`the-deadlock.md` is a finished draft with four watermarked 2400x1350 figures and a local preview,
and it has never been published. It runs **~2,750 words against a house length of 1,750-2,050**, so
publishing requires a length decision nobody has taken.

**This item does not publish anything.** Publishing to Substack is an outward-facing action for the
author, not an agent. This item makes the piece publication-ready and records the decision.

## Steps

1. **Take the length decision and record it in `decisions.md`:** cut to house length, or publish
   long and state why this slot tolerates it. Either is acceptable; not deciding is what has
   blocked the piece.
2. If cutting: cut to 1,750-2,050 words, preserving the argument. Report the before and after word
   counts.
3. **Re-check every technical claim against the repository**, especially the
   `validate_opening_book_summary.py` line numbers. QW-015 W1 moves `contract_version` out of the
   dict `normalize_summary` returns — the article's cited lines 118 and 142 may no longer say what
   it claims. Verify each against the current file and correct or rescope as needed. An article
   describing a bug that has since been fixed must say so, in the past tense.
4. Remove any "Part N" label. The Wednesday slot has never used one, and Parts VI/VII are already
   queued.
5. Repository conventions: **no Markdown tables** (Substack does not render them), and the
   `THE FULL-STACK MIND` wordmark on every figure — confirm all four still carry it.

## Completion criteria

- `decisions.md` records the length decision and its reasoning.
- Word count is either inside 1,750-2,050 or explicitly justified in that decision.
- Every cited line number was checked against the current repository; list them with verdicts.
- No "Part N" appears.
- No Markdown tables; four figures, all watermarked.

## Handoff

Record the word counts, the line-number verdicts, and that publication remains for the author.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
