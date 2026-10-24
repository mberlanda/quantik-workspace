# W4 — The visualizer tolerates an older server

**Repository:** `quantik-qfen-visualizer` · **Branch:** `feat/tolerate-response-fields` · one PR
**Depends on:** W2 merged. **Dispatch:** mechanical.

Acceptance criterion 5 requires the client to tolerate the new fields being **absent** — a browser
served from one deployment routinely talks to an older API.

## Steps

1. `src/engines.js` — read candidates, PV and `certainty` when present; behave exactly as today
   when they are absent. Absent must never throw and never render an empty control.
2. Where `certainty` is shown, an absent value must not be displayed as `estimate`. Unknown and
   estimated are different claims, and conflating them is the failure this field exists to prevent.
3. `test/engines.test.js` — a response with all new fields; a response with none of them (the
   older-server case); and a response with `certainty` absent, asserting it is not shown as
   `estimate`.

## Completion criteria

```sh
npm test
```

- Passes with no skipped tests.
- The older-server test fails if you make any new field required — verify, then revert.
- The app still opens from `file://` with no build step, or say plainly in the handoff that this
  was not checked.

## Handoff

Record the test counts and the older-server check.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
