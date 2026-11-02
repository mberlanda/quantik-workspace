# W1 — Re-run the patience lineup on an unspent seed

**Repository:** `quantik-models-py` · **Branch:** `feat/patience-arena-second-seed` · one PR
**Dispatch:** execute and record.

QW-012's evaluation ran `scripts/evaluate_lineup.sh` without overriding `SEED`, so it took the
script default `20260829` — the exact value QW-012's own plan said not to reuse, already spent on
`runs/eval/epoch-test/`. The cpool-vs-attn ply-6 MCTS-128 margin it reported is **0.8 points**,
small enough that a seed-linked artifact is a live explanation rather than a remote one.

**Retrain nothing.** The four `runs/train/patience-{resnet,mlp,cpool,attn}/best` checkpoints and
`runs/eval/patience-2026-08-30/` are inputs; leave every one of them on disk and unmodified.

## Steps

1. Choose a seed never used in this project. Forbidden: `20260827`, `20260828`, `20260829`,
   `20260901`, `20260909`. `20261001` is taken by the opening arena (QW-024). **Confirm before
   launching**, do not assume:
   ```sh
   grep -rn "20261015" scripts/ docs/ src/ runs/ 2>/dev/null || echo "unused"
   ```
   `20261015` is the suggested value if that prints `unused`. Name the seed in the write-up.
2. Run against the same four checkpoints with the seed overridden:
   `SEED=20261015 scripts/evaluate_lineup.sh <new output dir> …` — read the script's usage line
   first and match it exactly. Write to a new directory; do not write into
   `runs/eval/patience-2026-08-30/`.
3. Check the distinct-games / independence line the script prints before reading any win rate,
   the same way QW-024's arena requires. A degenerate run is not reportable.
4. Write `docs/patience-arena-second-seed.md` reporting **both runs side by side** — the original
   seed `20260829` numbers and the new seed's — not just the new one. A single new table cannot
   answer whether the ranking held.
5. State directly, in one sentence near the top, whether the cpool-vs-attn ranking holds and
   specifically whether the 0.8-point ply-6 MCTS-128 margin survives, reverses, or lands inside
   noise. All three are acceptable answers; only silence is not.

## Completion criteria

- The seed is named, and shown to be unspent by the grep in step 1.
- The document reports both seeds' numbers in the same table.
- The cpool-vs-attn question is answered in one explicit sentence.
- `runs/eval/patience-2026-08-30/` is byte-identical to before (`git status` will not show it —
  `runs/` is gitignored — so verify by listing it, and say so).
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record the seed, the grep output proving it unspent, both runs' key numbers, and the verdict.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions
win over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, the exact commands you
ran and their real output, and anything you could not finish.
