# W4 — Remove `expected-release` from PR-time jobs *and* its default

**Repository:** `quantik-core-contracts` · **Branch:** `ci/drop-expected-release` · one PR
**Depends on:** W1 merged. **Dispatch:** mechanical.

Dropping the input from the workflows is only half the fix. `actions/opening-book-consistency/action.yml:23`
carries a **default of `"1.2.0"`**, so omitting the input silently reintroduces the literal — the
failure mode looks identical to the bug being fixed.

## Steps

1. `.github/workflows/validate-contracts.yml` — remove `expected-release` from the PR-time job(s).
   A pull request must not require a coordinated release to go green.
2. `actions/opening-book-consistency/action.yml:23` — remove the `"1.2.0"` default. If the input
   remains supported it must have **no** default; an omitted input then means "do not check",
   not "check against a stale literal".
3. Keep the release-time check wherever the release workflow performs it. This item removes the
   PR-time coupling, not the check itself.
4. `grep -rn "1\.2\.0" .github/ actions/` and confirm no live default remains.

## Completion criteria

- Both workflow and action files are valid YAML.
- The grep shows no remaining hardcoded release default.
- Omitting the input does not fall back to a literal — read the action file back and confirm.

## Handoff

Record the grep output and the files changed.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
