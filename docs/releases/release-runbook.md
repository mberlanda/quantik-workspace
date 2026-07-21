# Release Runbook

1. Inspect all checkouts and preserve dirty work.
2. Create/validate the release train and consumer tasks.
3. Prepare producer sources; classify every version occurrence.
4. Run source validators and relative composite actions.
5. Record the approved full commit and move to candidate-green.
6. Create one annotated exact tag; never move it.
7. Publish Release/packages separately with explicit authorization.
8. Verify tag, assets/checksums, archive contents, and external actions.
9. Write the audit lock; open consumer tasks.
10. Adopt in consumers, run compatibility, update the matrix/docs, then complete.

Commands default to dry-run/read-only. `tag`, `publish`, clone/update, adapters, and benchmarks require explicit `--execute`; this repository's CI never publishes.
