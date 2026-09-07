# W2 — Implement the mapping in the opponent registry

**Repository:** `quantik-models-py` · **Branch:** `feat/skill-levels` · one PR
**Depends on:** W1 merged **and** human-reviewed. **Dispatch:** mechanical.

Implement exactly the mapping `docs/skill-levels.md` specifies. If you would have to choose an
opponent for a level, that is a gap in W1 — send it back.

**Already shipped, do not rebuild:** QW-030 delivered the UI slot for the ladder and the
how-to-play explainer (its V2 `mode-chooser` and V3 `how-to-play` items are `completed`). This item
supplies the data that slot consumes; it does not build UI.

## Steps

1. `src/quantik_models/play/opponents.py` — expose the skill levels from `docs/skill-levels.md`,
   each resolving to its specified opponent spec.
2. Implement the advanced-toggle rule from W1 section 5: the default view is the simplified level
   set, the advanced view is the full roster, sized by what is actually staged.
3. Enforce W1 section 4: no v3-corpus checkpoint (`cpool-v3`, `patience-v2`, `patience-v3`) may be
   reachable through a skill level. Add a test asserting that, so a future staging change cannot
   quietly promote one.
4. `tests/test_play_opponents.py` — each level resolves to the documented spec; the advanced roster
   size follows the rule rather than a hardcoded number; the v3 exclusion holds.

## Completion criteria

```sh
python -m pytest -q
python -m mypy
```

- Both clean.
- Each level's resolved spec matches `docs/skill-levels.md` exactly — assert on the document's
  values, not on reimplemented logic.
- The v3-exclusion test fails if you add one to the mapping. Verify by adding it, watching it fail,
  then removing it.

## Handoff

Record the resolved mapping and the test counts.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
