# Release Workflow

Use `release plan/prepare --dry-run`, review classified occurrences, then write workspace metadata. Run `validate-candidate`; it intentionally rejects future-tag references and missing relative-action checks. Remote-impact commands show their proposed command unless `--execute` is given. After publication, run exact verification, create/adopt consumer tasks, record the lock and matrix, and complete.
