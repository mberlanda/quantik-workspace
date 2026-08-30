# quantik-models-py

## Objective

Publish the staged artefacts and prove a restore works.

## Inputs

- `src/quantik_models/export/devdata.py` — the catalogue and the stager.
- `docs/dev-data.md` — the reader-facing description; update `<namespace>`.
- `runs/` — about 1.3 GB, the source.

## Approach

1. Stage all six groups. Read the generated cards before uploading anything.
2. Create the dataset repo and upload. Confirm LFS took effect on the first
   commit — check a `.npz`'s reported size on the Hub, not just that it exists.
3. Restore into a directory with no `runs/`, verify one file's sha256 against
   `MANIFEST.json`, and run a training smoke test against the restored corpus.
4. Replace `<namespace>` in `docs/dev-data.md` with the real one.

## Completion criteria

- The repo exists, is LFS-tracked, and carries all six groups with their cards.
- A restore is demonstrated end to end, including the sha256 spot-check — an
  untested backup is not a backup, and LFS pointers download as small text files
  that look like success.
- Handoff records the namespace, the total uploaded size, and the smoke test that
  ran against the restored corpus.
