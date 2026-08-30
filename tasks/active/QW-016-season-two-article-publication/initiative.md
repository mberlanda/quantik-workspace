# QW-016: Season Two Article Publication

> **Purpose:** Publish the finished deadlock article, and stop three completed drafts
> from living on exactly one disk.
> **Load with:** [`context/repositories/articles.md`](../../../context/repositories/articles.md)

## Problem and motivation

Two separate problems share one repository.

**The article is done and unpublished.** `articles/the-deadlock.md` is a complete draft
for the Wednesday puzzle/philosophy slot, with title and subtitle in the front matter,
four figures at 2400x1350 (`images/12-deadlock.png` as hero and cover,
`13-two-checks.png`, `14-rollout.png`, `15-philosophers.png`), generators
(`make_release_figures.py`, `make_preview.py`) and a local preview
(`preview-the-deadlock.html`). What blocks it is a length call: ~2,750 words against a
house length of 1,750-2,050.

**The repository has no remote.** Verified 2026-08-30: `git remote -v` is empty; there
is one commit, `7d8b75b`, "Quantik Season Two: three Substack drafts with generated
figures". This is the half of the old repo-hygiene note that held up — the
`quantik-api-rust` half did not, and is corrected in
[`QW-022`](../QW-022-workspace-repo-hygiene/initiative.md).

## Existing and desired behaviour

Existing: drafts, figures and generators all present and finished; nothing published;
nothing backed up.

Desired: the deadlock article published, and the drafts somewhere other than this laptop.

## Contracts and repositories

`articles` only. No contracts. The article *describes* `quantik-core-contracts`
machinery, so its technical claims are coupled to that repo even though no code is.

## Constraints and preserved invariants

- **No Markdown tables** — Substack does not render them. See `articles/README.md`.
- **Every figure carries the `THE FULL-STACK MIND` wordmark.**
- **No "Part N" on the Wednesday slot.**

## The coupling worth stating

This article is *about* the deadlock that [`QW-015`](../QW-015-release-engineering-hardening/initiative.md)
fixes. Publishing after the fix lands turns a complaint into a post-mortem, which is
the better piece — but it also means every line number and code quotation in the draft
must be re-checked, because QW-015 changes exactly the file the article quotes.

## Provenance

Migrated from WORKSTREAMS §3 ("Substack article — DRAFT COMPLETE, UNPUBLISHED") and
the surviving half of §12.
