# QREL-2026-001 Checklist

## Candidate

- [ ] Reconcile local contracts/Rust release branches with their newer public PR heads.
- [x] `VERSION` and `contracts.json` agree on 1.2.0.
- [x] Contracts unit tests and fixture/schema validation pass locally.
- [ ] Candidate composite actions are exercised from relative paths.
- [ ] Stable versus planned documentation is corrected.
- [ ] Candidate-green evidence is recorded.

## Publication

- [ ] Immutable `v1.2.0` tag points to approved commit.
- [ ] GitHub Release, archive, and checksum exist.
- [ ] Both tagged composite actions pass externally.
- [ ] Release lock records tag and full SHA.

## Consumers

- [ ] Open and validate the Python release PR without overwriting its dirty worktree.
- [ ] Python adoption complete without overwriting current user changes.
- [ ] Rust adoption complete; workflow ref/expectation agree.
- [ ] Models adoption complete; explicit supported release exists.
- [ ] Compatibility matrix is evidence-backed.
