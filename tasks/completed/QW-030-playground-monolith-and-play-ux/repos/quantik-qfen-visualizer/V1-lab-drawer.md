# V1 — The lab drawer

**Branch:** `feat/lab-drawer`

Move into one `<details>` at the **bottom** of the page, collapsed by default:
the QFEN input and its Copy/Reset buttons, the seed input, the speed select, both
per-player controller selects, both remote endpoint URL fields, the service-base
override, and Export/Import trace.

**Keep every element id.** This is a relocation. The existing tests address these
ids and must keep passing untouched; if one breaks, you moved more than the DOM.

**Testable part — `src/layout.js` (new):** export the ordered list of advanced
control ids, a predicate over it, and read/write helpers for the drawer's
open/closed state in `localStorage` (same defensive `try`/`catch` shape
`settings.js` already uses for the theme — storage can throw, not just return
null). `test/layout.test.js` covers the default-closed state, that a persisted
open state survives a reload, and that a corrupt stored value falls back to
closed rather than throwing.

Label it for what it is — "Advanced", "Lab", "Under the hood" — not "Settings".
The existing Settings panel is theme colours and stays where it is.

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
