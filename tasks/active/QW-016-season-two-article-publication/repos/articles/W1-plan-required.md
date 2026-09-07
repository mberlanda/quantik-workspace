# W1 — articles

Repository: `articles`
Branch: `plan/qw-016-articles` (one PR)

## Objective

# articles

## Objective

Publish `the-deadlock.md` to the Wednesday slot, and get the Season Two drafts off a
single machine.

## Inputs

- `the-deadlock.md` — the draft; title and subtitle are in its front matter.
- `images/12-deadlock.png` (hero and cover), `13-two-checks.png`, `14-rollout.png`,
  `15-philosophers.png` — all 2400x1350, all watermarked.
- `make_release_figures.py`, `make_preview.py`, `preview-the-deadlock.html`.
- `README.md` — house conventions.

## Approach

1. Take the length decision and record it in `decisions.md`.
2. Re-read the draft against `quantik-core-contracts/scripts/validate_opening_book_summary.py`
   as it stands at publication time. The article quotes it; QW-015 changes it.
3. Regenerate the preview, check every figure carries the wordmark, confirm no
   Markdown tables survived editing.
4. Publish. No "Part N".
5. Settle the remote.

## Completion criteria

- The article is live.
- `git remote -v` is non-empty and the drafts are pushed, or `decisions.md` records the
  deliberate alternative and names where the backup lives.
- Handoff records the published URL and the commit the drafts were pushed at.

## Implementation and scope

**Criterion 4 is now met, and QW-015 is largely-complete, unblocking
this.** Verified in the checked-out repository: `articles` has origin
`git@github.com:mberlanda/quantik-articles.git` (matches the `quantik-ns/
CLAUDE.md` repo table) and `main` is up to date with `origin/main` — the
three drafts are pushed. `problem`'s "no git remote... at commit 7d8b75b"
is stale; a remote was added since.

**Criteria 1-3 remain genuinely open** — `the-deadlock.md` is still 2,831
words against the 1,750-2,050 house length (the length decision in
`decisions.md` point 2 is still framed as open, not taken), publication to
the Wednesday Substack slot isn't something this repo's git history can
confirm either way, and the validator line numbers need re-checking against
`quantik-core-contracts` now that QW-015 has landed most of its fix
(v1.3.1). `allowed_paths` names the draft, `decisions.md`, and its four
figures. `decisions`/`invariants` stay empty: this is an editorial call,
not a design one — the length and publish-timing decisions are for
whoever owns the piece, not a mechanical planning-pass fill.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
