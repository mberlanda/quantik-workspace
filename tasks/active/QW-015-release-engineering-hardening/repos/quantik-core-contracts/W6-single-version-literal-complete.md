# W6 — One version literal per repository

**Repository:** `quantik-core-contracts` · **Branch:** `chore/single-version-literal` · one PR
**Dispatch:** mechanical.

## Steps

1. `VERSION` is the source; `contracts.json`'s `release_version` is its declared mirror. Every
   other occurrence of the release string must derive rather than repeat.
2. `grep -rn "1\.3\.\|1\.2\." --include="*.yml" --include="*.yaml" --include="*.py" --include="*.json" .`
   and, for each hit, classify it as: the source, the declared mirror, a historical record (keep),
   or a hardcoded repeat (remove and derive).
3. Fix the repeats. Leave historical records alone — a research note recording what 1.1.0 did is
   not drift.
4. Record the classification in the PR description so a reviewer can check the judgement calls.

## Completion criteria

- After the change, the grep returns only: `VERSION`, the declared mirror, and entries explicitly
  classified as historical in the PR description.
- `python -m pytest -q` clean.
- `quantik-workspace release drift` reports no `version-mirror` issue for this repository.

## Handoff

Record the full classification table.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
