# QW-026 Decisions

1. **Evaluation-only, no retraining.** The checkpoints QW-012 produced are the
   thing being checked, not the thing in question — a seed only enters at the
   arena/shift step (`scripts/evaluate_lineup.sh`), never at training. Retraining
   would spend more compute to answer a question this task doesn't have.

2. **Reuse the checkpoints, not the first run's output directory.** Write to a
   new `runs/eval/patience-<date>-seed2/` (or similar), not into
   `runs/eval/patience-2026-08-30/`, so the first run stays intact and both are
   comparable side by side rather than one overwriting the other.

3. **Not folded back into QW-012.** QW-012's training and write-up are otherwise
   complete; making this a blocking sub-task of it would hold up closing work
   that is done for a question that is genuinely separate (is the *arena*
   result seed-stable), and split cleanly since QW-026 needs none of QW-012's
   remaining open items to proceed.
