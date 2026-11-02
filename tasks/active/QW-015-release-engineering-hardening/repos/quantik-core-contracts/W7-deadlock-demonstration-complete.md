# W7 — Demonstrate the deadlock is gone

**Repository:** `quantik-core-contracts` · **Branch:** `test/deadlock-demonstration` · one PR
**Depends on:** W1 **and** W4 merged. **Dispatch:** execute and record.

The initiative's last acceptance criterion is a demonstration, not an assertion: a PR that changes
only Python, with contracts still on the previous release, goes green without a coordinated tag.

## Steps

1. Construct the scenario: a change touching only the Python side, with contracts left on its
   current release and no new tag.
2. Run the PR-time checks against it and capture the real output.
3. If it goes green, record the transcript in `docs/consistency-checks.md` under a heading naming
   the deadlock this proves is gone, with the date.
4. If it does **not** go green, that is the finding. Report exactly which check still couples the
   two, and stop — do not weaken the check to force green.

## Completion criteria

- A real transcript, not a description.
- `docs/consistency-checks.md` records the scenario and the date.
- If red: the coupling check is named precisely in the handoff.

## Handoff

Record the scenario, the transcript, and the verdict.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
