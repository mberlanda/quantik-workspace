# W2 — articles

Repository: `articles`
Branch: `plan/qw-022-articles` (one PR)

## Objective

# articles

## Objective

Get the Season Two drafts off a single machine.

## Inputs

- One commit, `7d8b75b`; `git remote -v` empty.

## Approach

Add a remote and push, or record the deliberate alternative and name where the backup
lives. Note that the drafts are unpublished work, so a private remote is a legitimate
choice; "no remote at all" is not.

## Completion criteria

- `git remote -v` is non-empty and `main` is pushed, or `decisions.md` records the
  alternative and the backup location.
- Cross-checked against
  [`QW-016`](../../../QW-016-season-two-article-publication/initiative.md), which carries
  the same criterion.

## Implementation and scope

Not yet planned. Replace this item's placeholder `allowed_paths` in `manifest.yaml` with explicit repository-relative paths, select the `decisions`/`invariants` references it actually needs, and split into further work items wherever another branch/PR is needed.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
