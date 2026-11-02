# W5 — A release preflight that fails before the tag, not after

**Repository:** `quantik-core-contracts` · **Branch:** `feat/release-preflight` · one PR
**Dispatch:** mechanical.

## Steps

1. Add a preflight (script plus a release-workflow step) asserting, before any tag is created:
   - the tag does **not** already exist — exact tags never move, so an existing tag is a stop;
   - `VERSION` matches the tag being cut, without the `v`;
   - every downstream-referenced action path resolves **at that ref** — i.e.
     `actions/cross-language-smoke/action.yml` and `actions/opening-book-consistency/action.yml`
     exist at the commit being tagged.
2. Each failure names which assertion failed and the offending value. "Preflight failed" without
   the value is a preflight nobody can act on.
3. Test each assertion's failure path.

## Completion criteria

```sh
python -m pytest -q
```

- Three assertions, three tested failure paths, each with the value in the message.
- Running the preflight against the current `VERSION` and an already-published tag fails on the
  first assertion — demonstrate it.

## Handoff

Record the three assertions and their demonstrated failures.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
