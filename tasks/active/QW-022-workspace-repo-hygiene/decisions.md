# QW-022 Decisions

1. **The e2e workflow and `tests.yml` should stay different.** Rejected: making the e2e
   pipeline install the published package too. That would delete the only check that
   two in-flight repositories still integrate, which is the entire reason the e2e
   pipeline exists. The defect is that the choice is implicit, not that it is wrong.

2. **A pinned `ref` is preferred over tracking `main`.** Tracking `main` means an
   unrelated repository's merge can turn this repository's CI red with no local change,
   and the failure presents as a local bug. A pinned ref makes the update an explicit,
   reviewable commit. Rejected: leaving it floating and treating breakage as a signal —
   it is a signal delivered to the wrong repository.

3. **The `quantik-api-rust` correction is not deleted.** Rejected: removing the
   struck-through claim now that it is fixed. It was repeated as fact for weeks, shaped
   a delegation plan, and blocked a workstream. Kept as an exhibit, with the
   verification method named, so the next unverified inherited claim is easier to
   recognise.

4. **`.oracle-worktree/` is documented or removed, not left.** An unexplained directory
   at the workspace root is exactly the kind of thing that becomes load-bearing by
   accident. Check whether the oracle tooling still references it before deleting.
