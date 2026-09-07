# V3 — How to play

**Branch:** `feat/how-to-play`

A collapsible explainer near the board, closed by default, open on a first visit
(reuse V1's storage helper if it landed; otherwise a local equivalent). Quantik's
rule is not guessable from the board:

- You place a shape on any empty square.
- You may **not** place a shape in a row, column, or 2×2 zone where your
  **opponent** already has that shape. Your own is fine.
- You win by completing a row, column, or zone with **four different shapes**, in
  either colour — whoever places the fourth wins, regardless of who owns the
  others.

**Check that wording against `quantik-core-contracts`' own rule statement before
writing it into the app**, and say in the PR which file you checked it against.
Two divergent statements of one rule is the failure to avoid; the contracts repo
is the source of truth.

**Testable part — `src/rules.js` (new):** export the rule text as structured data
(a title plus an ordered list of points) so `app.js` renders it rather than
holding a string. `test/rules.test.js` asserts the three group kinds and the
four-different-shapes win condition are all present — a cheap guard against
someone trimming the explainer down to something wrong.

## Execution contract


1. **A failing test comes first**, for any change to `src/*.js` logic. Not after,
   not "covered by an existing test". Write it, watch it fail, then implement.
2. **`node --test` does not verify a UI change.** The runner loads modules against
   a minimal DOM stub via `test/helpers/loadClassicScript.js`; it checks logic, not
   rendering. Serve `index.html` and look at it before calling anything done, and
   say in the PR what you looked at.

The consequence for design: **push logic into modules that never touch
`document`**, and keep `app.js` thin wiring. This packet names the module to
put the testable part in. That split is not a style preference — it is the only
way the logic is testable at all here.


**One logical change per commit. One PR for this work item.** Branches `feat/…`,
`chore/…`, `fix/…`. Commit messages explain *why*; the diff shows what. No commit
trailers. `npm test` green before every PR.

## Scope and handoff

Edit only the manifest allowed paths. Record exact starting and final revisions, branch, PR, commands and results, and dependency evidence in a work-item-specific handoff. Path expansion requires coordinator review.

Decision references: none.

No skill ladder, puzzle mode, or engine request-shape changes. Preserve file:// support and dependency-free classic scripts.
