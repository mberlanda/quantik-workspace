# QW-025 Status

**tooling-done-not-published.**

Landed in models-py #57: `export/devdata.py`, `docs/dev-data.md`, and six tests.
Smoke-staged locally for `corpora` (5 files, 52.1 MB) and `probe` (2 files,
2.6 MB); cards, `MANIFEST.json` and `.gitattributes` all written.

**Nothing has been uploaded.** That step needs Hub credentials and is an
outward-facing action, so it is deliberately left to a person:

```bash
python -m quantik_models.export.devdata runs/devdata
huggingface-cli upload-large-folder --repo-type dataset \
  <namespace>/quantik-dev-data runs/devdata
```

Next action: choose the namespace, upload, then do criterion 4 — the restore
demonstration, which is the only criterion that proves the rest worked.
