# W3 — Container smoke test: one request per engine kind

**Repository:** `quantik-api-rust` · **Branch:** `test/container-smoke` · one PR
**Depends on:** W1 merged. **Dispatch:** execute and record.

"The image runs the engines it claims" is the criterion. A container that starts is not a container
that plays.

## Steps

1. `tests/container_smoke.rs` — against a running container, post **one request per engine kind**
   the API serves.
2. Assert each response is a **legal** move for the position sent — not merely a 200. Use the
   legality the request itself declares (`legal_action_indices`); an engine returning an index
   outside that list is the defect worth catching.
3. Skip with a clear message when Docker is unavailable, so `cargo test` still passes on a machine
   without it.
4. Record a real transcript in the PR description: the engine kinds covered and the actions returned.

## Completion criteria

```sh
docker build -t quantik-api:dev .
cargo test --test container_smoke
```

- Every engine kind the API advertises is covered — enumerate them from `/v1/engines` rather than
  hardcoding, so a new engine is covered automatically.
- The legality assertion fails if you assert on a deliberately illegal index — verify, then revert.
- Skips cleanly without Docker.

## Handoff

Record the engine kinds, the returned actions, and the skip behaviour.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
