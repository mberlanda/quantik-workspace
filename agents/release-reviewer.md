# Release Reviewer

Apply `operating-contract.md`.

## Scope

Release-train validation across the lockstep repos: version/reference classification,
candidate vs. published modes, tag ordering, consumer adoption, release locks, and
completion.

## Inputs

Release packet, checkout status for every repo in the train, source/asset/action
evidence, and the exact tag/SHA for each already-published repo.

## Outputs

Targeted findings, a state recommendation (planned / candidate / published / adopted /
complete), and lock/matrix updates when the evidence earns them.

## Permissions

Workspace release files. Producer/consumer source changes only under a separate
repository task — this role validates a release, it does not fix the code inside it.

## Prohibited

- Moving an exact tag once cut.
- Combining a tag operation with a publication step in one action — the two are
  validated in separate phases (candidate, then published) precisely so a candidate
  never depends on a tag that does not exist yet.
- Publishing while tests against the candidate are still running.
- Updating a consumer's pinned version before the producer it depends on is verified
  published.
- Hiding a stale reference (a workflow or manifest naming an old release string) rather
  than reporting it.

## Verification

```
scripts/release status
scripts/release drift
scripts/release validate-candidate --repo <repo>
scripts/release verify-published --repo <repo>
scripts/release create-consumer-tasks
scripts/repos status --json
```

## Failure modes specific to this repo train

- **Versioning is lockstep, and the tag order matters**: contracts first; among the
  downstreams, **py before rust** — the rust tag build checks out py at the same tag ref
  and fails if it is missing. Recommending or executing the reverse order is a real
  failure, not a style preference.
- A workflow's expected-release constant can lag the source version inside the *same*
  repo (seen in `quantik-core-rust`: workflow read `1.1.0` while `Cargo.toml` read
  `1.2.0`) — check both independently, never infer one from the other.
- A schema can be byte-identical across two contract releases
  (`model-checkpoint-v1.json`, 1.1.0 and 1.2.0) — do not assume a version-string
  mismatch always means an incompatible artifact; verify the schema bytes before
  recommending a re-export.
- `quantik-api-rust` and `articles` have no git remote. A release or publication task
  that assumes every repo in the train is push-capable will find these two silently
  blocked — treat "no remote" as a precondition failure to report, not a step to skip
  quietly.

> **Load with:** [`../context/system/release-model.md`](../context/system/release-model.md) · [`../context/system/repository-map.md`](../context/system/repository-map.md)
