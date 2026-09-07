# W5 — Re-sync the vendored app and add the OpenAPI document

**Repository:** `quantik-models-py` · **Branch:** `chore/resync-visualizer-engine-names` · one PR
**Depends on:** W3 **and** W4 merged.

Two loose ends that both need everything else to have landed first.

## Part 1 — re-sync the vendored app (required)

`src/quantik_models/play/app/` is a vendored copy of `quantik-qfen-visualizer`, produced by
`scripts/sync_visualizer.py` and stamped with the source commit in `app/SOURCE.json`. It still
contains the prefixed string in `app/src/engines.js` and `app/src/play.js` because those bytes
predate W3.

1. Confirm W3 is merged and note its merge commit.
2. Run the existing sync against a clean visualizer checkout at that commit:
   `python scripts/sync_visualizer.py ../quantik-qfen-visualizer`. It refuses a dirty source
   tree — that refusal is deliberate, do not work around it.
3. Confirm `app/SOURCE.json` records W3's merge commit, not an older one.
4. Do not hand-edit anything under `app/`. If the synced result is wrong, the fix belongs in the
   visualizer or in the sync script, never in the copy.

```sh
python -m pytest -q tests/test_play_app_assets.py
grep -rn "quantik\.engine-" src/quantik_models/play/app/ || echo "clean"
python -m pytest -q && python -m mypy
```

`test_play_app_assets.py` already asserts every script and stylesheet `index.html` references
exists in the vendored tree; it is the check that catches a partial sync. The grep must print
`clean`, and `SOURCE.json` must carry a 40-character commit.

## Part 2 — the OpenAPI 3.1 document (optional; drop it if Part 1 is enough for one PR)

Per `decisions.md#D2` the registered schemas are the source of truth and an OpenAPI document is
additive. If you take this on, it belongs in `quantik-core-contracts`, not here — open it as a
**separate** work item rather than widening this branch across repositories. Leave a note in the
handoff either way so the decision is not silently dropped.

## Handoff

Record W3's merge commit, the `SOURCE.json` before and after, the grep output, and whether Part 2
was taken on or deferred.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md` and `README.md`. Repository
instructions win over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, the exact commands you
ran and their real output, and anything you could not finish.
