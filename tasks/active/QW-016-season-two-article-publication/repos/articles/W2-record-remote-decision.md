# W2 — Settle where the Season Two drafts live

**Repository:** `articles` · **Branch:** `chore/record-remote-decision` · one PR
**Dispatch:** judgment — it is a decision, but a small one.

`git remote -v` is **empty** — verified 2026-08-30 at commit 7d8b75b. Three finished Season Two
drafts exist on exactly one machine, with no second copy anywhere.

## Steps

1. Take the decision and record it in `decisions.md`. Two acceptable outcomes:
   - **Add a remote** and push all three drafts. The workspace expects
     `mberlanda/quantik-articles`. Record the remote and the pushed commit.
   - **Keep the repository local deliberately** — and then **name the backup arrangement** in the
     same entry. "It is local" without a named backup is not a decision, it is the current
     accident.
2. Do not create a remote repository or push without the author's go-ahead: publishing drafts to a
   hosted service is outward-facing and theirs to authorise. If you cannot get it, write the
   decision entry with the recommendation and stop.
3. Whatever is decided, the entry states what happens to the other two Season Two drafts.

## Completion criteria

- `decisions.md` names the outcome, and — if local — the backup arrangement.
- If a remote was added with authorisation: `git remote -v` is non-empty and the drafts are pushed.
- If not: the handoff says explicitly that it awaits the author.

## Handoff

Record the decision and whether authorisation was obtained.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
