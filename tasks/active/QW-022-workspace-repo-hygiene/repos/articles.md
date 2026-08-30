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
  [`QW-016`](../../QW-016-season-two-article-publication/initiative.md), which carries
  the same criterion.
