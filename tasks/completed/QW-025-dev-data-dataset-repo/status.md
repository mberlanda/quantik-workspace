# QW-025 Status

**published-and-restore-verified.** Every acceptance criterion is met.

## The two repos are live

| repo | files | size | private |
| --- | --- | --- | --- |
| [`brpoplpush/quantik-dev-data`](https://huggingface.co/datasets/brpoplpush/quantik-dev-data) | 321 | 837.2 MB | yes |
| [`brpoplpush/quantik-dev-runs`](https://huggingface.co/datasets/brpoplpush/quantik-dev-runs) | 509 | 882.6 MB | yes |

Per-group counts on both match the local `MANIFEST.json`. Both carry
`license:cc-by-nc-4.0`.

## What the audit found before publishing

Diffing `runs/` against the staged manifest found **681 MB unstaged** — nearly
as much as the catalogue covered. The miss that mattered most was `latest.pt` /
`state.json`, the optimizer resume state: without it an interrupted run
restarts at epoch zero, which is the exact failure this initiative exists to
prevent. Also absent: the raw per-ply oracle output (days of CPU, only its
packed `.npz` derivative was staged), `runs/train/*/final`, `lrsweep`, `sweep`
and `autoplay`.

Fixed in models-py #58. **Every file under `runs/` is now covered by exactly one
group**, verified by re-running the diff: `0.000 MB in 0 files`.

## The restore is demonstrated, not assumed

Criterion 5, end to end, and it is the only criterion that proves the rest
worked:

1. `hf download --include "corpora/*"` into an empty directory.
2. `cp -r` into a tree with **no `runs/`** at all.
3. Trained `--preset smoke --epochs 1` against the restored corpus — completed,
   wrote `best/`, exported ONNX.
4. The `provenance.json` that run recorded hashes the corpus it trained on:
   `887e1de514c1d9de2e58e14bc953c01b`, **byte-identical to the `corpora`
   entry in `MANIFEST.json`.**

That closes the loop between the backup, the restore and the provenance system.
A separate spot-check hashed all three `probe` files after download — real
content, not the 130-byte LFS pointers that download looking exactly like
success.

## Open, and deliberately left to a person

`quantik-dev-data` still carries `checkpoints/` (231 MB) and `evaluations/`
(43.6 MB) from the original single-repo upload, before the split. They are now
duplicated in `quantik-dev-runs` and absent from dev-data's `MANIFEST.json` —
unreferenced files that still hash fine, which is precisely the trap `--prune`
exists for.

```bash
hf repos delete-files brpoplpush/quantik-dev-data checkpoints/ evaluations/ --repo-type dataset
```

Deleting remote files is destructive and irreversible, so it is not automated.
Note it reclaims no storage on its own: LFS objects persist in history, and
only `super_squash_history` reclaims them. Squashing `quantik-dev-data` once now
is the cheap moment — one generation of history — and is exactly the operation
the churn split was designed so this repo would never need again.

## Also not automated

`sync_dev_data.sh` stops before `git push`, and `devdata.py` only prints the
upload line. These repos hold what cannot be cheaply recomputed, and an
unattended push is one bad glob away from committing a truncated file over a
good one.
