# QW-025 Status

**data-repo-live; runs-repo-not-yet-created.**

`brpoplpush/quantik-dev-data` exists, is **private**, and holds 283 files
uploaded 2026-08-30. Tooling landed in models-py #57 and was reworked in #58.

## What #58 changed, and why

An audit of `runs/` against the staged manifest found **681 MB unstaged** —
nearly as much as the catalogue covered. The miss that mattered most was
`latest.pt` / `state.json`, the optimizer resume state: without it an
interrupted run restarts at epoch zero, which is the exact failure this
initiative exists to prevent. Also missing: the raw per-ply oracle output (days
of CPU, only its packed `.npz` derivative was staged), `runs/train/*/final`,
`lrsweep`, `sweep` and `autoplay`.

Every file under `runs/` is now covered by exactly one group.

The catalogue is split across **two** dataset repos, by churn rather than
subject:

| repo | groups | size | rewritten |
| --- | --- | --- | --- |
| `quantik-dev-data` (live) | solver-output, corpora, enumerations, probe, opening-book | 562 MB | never — appended to only |
| `quantik-dev-runs` (**to create**) | checkpoints, sweeps, autoplay, evaluations | 882 MB | every training generation |

Hub history is permanent — every re-push adds an LFS object and only
`super_squash_history` reclaims it, destructively. Together, the churny half
inflates the history of the irreplaceable half. Split, `quantik-dev-runs` can be
squashed freely and `quantik-dev-data` never has to be.

## Next actions

1. Create `brpoplpush/quantik-dev-runs` (private, dataset) and upload
   `runs/devruns`.
2. Re-upload `quantik-dev-data`: the live copy predates #58 and is missing
   `solver-output`, the earlier probe, and the enumeration log.
3. **Criterion 4 — the restore demonstration.** Still the only criterion that
   proves the rest worked, and still not done. An untested backup is not a
   backup, and this one fails silently: LFS pointers download as small text
   files that look like success.

```bash
scripts/sync_dev_data.sh          # clone-or-pull, re-stage, show diff; never pushes
```

## Deliberately not done

Nothing is pushed by tooling. `sync_dev_data.sh` stops before `git push` and
`devdata.py` only prints the upload line: these repos hold what cannot be
cheaply recomputed, and an unattended push is one bad glob away from committing
a truncated file over a good one.
