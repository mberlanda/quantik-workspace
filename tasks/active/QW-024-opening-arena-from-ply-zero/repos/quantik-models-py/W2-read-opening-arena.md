# W2 — Answer the question that blocks QW-010

**Repository:** `quantik-models-py` · **Branch:** `docs/opening-arena-reading` · one PR
**Depends on:** W1 merged. **Dispatch:** judgment — this item wants a capable model and a human
reviewer, not a cheap one.

W1 produced numbers. This item decides what they mean, because QW-010's skill-level ladder is
blocked on exactly one question and a wrong answer ships a ladder that ranks opponents on a phase
the player never starts in.

## The question

**Is there a strength ordering between these checkpoints at ply 0 at all, or are they
indistinguishable there?**

The `uniform-mcts` control is what separates the two readings, and it is why the script includes
it. Every checkpoint is uniform to three decimal places on the empty board (max legal prior
0.016-0.023). So:

- If the networks beat `uniform-mcts` but not each other, the honest finding is *"search does the
  work at ply 0; the networks are indistinguishable there"* — and QW-010 cannot derive a ladder
  from this phase at all. That is a real, useful, publishable answer.
- If the networks separate from each other **and** from the control, report the ordering with
  its uncertainty.
- If nothing separates from the control, say that plainly.

## Steps

1. Read `docs/opening-arena-ply0.md` and the raw outputs in the directory W1 named.
2. Extend the document with a **Reading** section that answers the question above in its first
   sentence, and states the evidence for it immediately after.
3. Add a **What this unblocks in QW-010** section: state whether a ply-0-derived ladder is
   supportable, and if it is not, say what QW-010 should use instead.
4. Quantify uncertainty. With `GAMES` per ordered pairing, a difference of a few points is not a
   ranking. If two agents are within noise, write "indistinguishable", not an ordering.
5. Do not run new arenas here. If the data cannot answer the question, say so and name what run
   would — that is a legitimate outcome of this item.

## Completion criteria

- The first sentence of **Reading** answers the ordering question directly.
- Every claim traces to a number in W1's tables, and no claim rests on a pooled (seat-unbalanced)
  win rate.
- **What this unblocks in QW-010** gives QW-010 something actionable either way.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record which sections you added and any question the data could not settle.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions
win over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, the exact commands you
ran and their real output, and anything you could not finish.
