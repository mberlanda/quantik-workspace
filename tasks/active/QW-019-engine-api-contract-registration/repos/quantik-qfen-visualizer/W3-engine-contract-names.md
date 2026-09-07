# W3 — `quantik-qfen-visualizer` sends the registered name

**Repository:** `quantik-qfen-visualizer` · **Branch:** `feat/engine-contract-names` · one PR
**Depends on:** W1 merged.

The browser client sends the prefixed string from two files, not one. Both must move together or
the app sends different names down different code paths (`decisions.md#D3`).

## Steps

1. `src/engines.js` (~line 54) — `schema: "engine-request.v1"`.
2. `src/play.js` (~lines 40 and 77) — the same literal appears twice more, once in a comment
   describing what the Rust gateway accepts and once in a request body. Update both; keep the
   comment accurate by noting the gateway also accepts the legacy spelling for one minor cycle.
3. Grep before you finish: `grep -rn "quantik\.engine-" src/` must return nothing.
4. `test/engines.test.js` and `test/play.test.js` — the existing tests assert on the request body.
   Update the expected string, and add one assertion that the sent `schema` is exactly
   `"engine-request.v1"` so a future edit cannot silently reintroduce a prefix.

## Completion criteria

```sh
npm test
grep -rn "quantik\.engine-" src/ || echo "clean"
```

- `npm test` passes with no skipped tests.
- The grep prints `clean`.
- The app still opens from `file://` with no build step — open `index.html` directly and play one
  move against a local engine, or state plainly in the handoff that you could not.

## Handoff

Record the commands, the test counts, and whether the `file://` check was actually performed.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md` and `README.md`. Repository
instructions win over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, the exact commands you
ran and their real output, and anything you could not finish.
