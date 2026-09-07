# V4 — Make it feel like a playground

**Branch:** `chore/playground-styling`

`src/styles.css` only. **No logic, no `src/*.js` changes**, so this is the one
task with no failing test in front of it — and therefore the one where rendering
it is the entire verification. Screenshots in the PR.

What is being fixed: the page reads as an instrument panel. Every control has
equal visual weight, the board is one panel among several, and the first thing the
eye lands on is a monospace text field.

- The board is the largest thing on the page and is what loads first.
- The mode chooser and the primary action (New game) are the only prominent
  controls above the board.
- Assessment, evaluation bar and top-moves stay, quieter — they are genuinely
  interesting to a curious non-expert, and hiding them would be a loss.
- The drawer is visually recessive: no border-heavy panel, no accent colour.
- Keep the existing colour variables and the theme customization. Contrast has to
  survive both piece themes.

Do not add a dependency, a font CDN, or a build step. The app opens from
`file://` and that is a property worth more than any of those.

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

Decision references: `decisions.md#D4`.

No skill ladder, puzzle mode, or engine request-shape changes. Preserve file:// support and dependency-free classic scripts.
