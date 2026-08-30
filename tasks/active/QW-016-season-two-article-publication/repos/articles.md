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
