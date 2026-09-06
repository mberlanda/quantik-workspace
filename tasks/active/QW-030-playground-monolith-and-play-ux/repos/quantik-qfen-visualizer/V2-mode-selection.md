# V2 — Modes of play

**Branch:** `feat/mode-chooser`

The first thing on the page. Four modes, prompted lightly — buttons or a segmented
control, not a form:

| mode | player 0 | player 1 |
|---|---|---|
| Play a model | human | engine |
| Watch two engines | engine | engine |
| Two players | human | human |
| Just the board | neither — the QFEN/analysis view the app is today |

Picking a mode sets the two controller selects that now live in the drawer. The
drawer stays the place to override them; the mode is the shortcut, not a
replacement.

**Testable part — `src/modes.js` (new):** `MODES` (id, label, one line of
description) and a pure `applyMode(profile, modeId)` returning the controller
assignment, with an unknown id falling back to a named default rather than
throwing. `test/modes.test.js` covers every mode's assignment, the fallback, and
that the mode round-trips through `settings.js`'s profile.

`settings.js` gains a `mode` field on the profile, normalized like the others.

**"Just the board" must stay reachable** — it is what the app is today and it is
the mode this repository's own name describes.

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

Decision references: `decisions.md#D4`, `decisions.md#O1`, `decisions.md#O2`.

No skill ladder, puzzle mode, or engine request-shape changes. Preserve file:// support and dependency-free classic scripts.
