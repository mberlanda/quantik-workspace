# quantik-workspace

`quantik-workspace` is the file-based control plane for the independent Quantik repositories. It coordinates cross-repository intent, repository-scoped tasks, compatibility evidence, bounded AI context, typed dependency/release state, and drift checks.

It is **not** a source monorepo, engine implementation, model implementation, database, server, or custom agent runtime. Implementation repositories own their code; contracts owns interoperable schemas/fixtures/actions; this workspace owns orchestration and evidence.

## Repositories and boundaries

- `quantik-core-py`: Python/reference domain behavior, APIs, tests, benchmarks, and adapters.
- `quantik-core-rust`: optimized Rust behavior, algorithms, APIs, tests, benchmarks, and adapters.
- `quantik-core-contracts`: canonical cross-language schemas, fixtures, validators, wire IDs, policies, and shared actions/workflows.
- `quantik-models-py`: tensors, action/policy/value interpretation, training/inference, datasets, checkpoints, and evaluation.
- `quantik-workspace`: inventory, dependencies, task/release packets, context, reports, locks, and drift detection.

## Start

```bash
git clone https://github.com/mberlanda/quantik-workspace
cd quantik-workspace
./scripts/bootstrap
./scripts/status
./scripts/validate
```

The default layout expects the four repositories as siblings. Override only local paths in ignored `workspace.local.yaml`, for example:

```yaml
repositories:
  quantik-core-rust:
    path: /work/quantik-core-rust
```

Bootstrap creates a workspace-local virtual environment, installs this dependency-free package, validates configuration, and reports missing/dirty repositories. It never overwrites checkouts or requires GitHub authentication. Preview missing clones with `quantik-workspace repos clone`; add `--execute` explicitly to clone.

## Status and task packets

```bash
quantik-workspace repos list
quantik-workspace repos status
quantik-workspace repos status --json
quantik-workspace task validate
```

Status reports paths, branch/commit/upstream, dirty/untracked/ahead/behind state, repository and supported-contract versions, action refs/expectations, active initiatives, and releases. Initiatives under `tasks/` decompose work into one executable repository task per owner and require durable handoffs/evidence.

## Bounded context

```bash
quantik-workspace context repo quantik-core-rust
quantik-workspace context initiative QW-001
quantik-workspace context task QW-001 quantik-core-rust
quantik-workspace context release QREL-2026-001
```

Bundles list included/excluded sources and live revisions. Generation fails explicitly when the approximate budget is exceeded; it does not silently scan or truncate full repositories.

## Compatibility

```bash
quantik-workspace validate contracts
quantik-workspace validate fixtures
quantik-workspace compatibility smoke
quantik-workspace compatibility smoke --execute
```

The workspace validates metadata and invokes repository-owned adapters. It does not implement Quantik behavior. Reports preserve contract, implementation, serialization, ordering, tolerance, intentional, missing-coverage, and infrastructure classifications. `--execute` is required before invoking adapter or benchmark commands.

## Version and release model

Repository/package versions, the whole contracts release, wire IDs (`selfplay.v1`), GitHub Action refs, CI expectations, and supported-contract declarations are distinct axes.

Release states are:

```text
planned → prepared → candidate-green → tagged → published → producer-verified
→ consumer-updates-open → consumer-compatible → completed
```

Candidate actions are tested from checked-out relative paths and cannot rely on the future tag. After publication, exact external `@vX.Y.Z` refs are verified and locked to a full SHA. Exact tags never move; published defects require a patch release.

```bash
quantik-workspace release prepare --repository quantik-core-contracts --version 1.2.0 --id QREL-2026-001 --dry-run
quantik-workspace release validate-candidate QREL-2026-001
quantik-workspace release status QREL-2026-001
quantik-workspace release drift --json
```

Tagging and publication are separate and print dry runs unless `--execute` is supplied. No remote write occurs during inspection, validation, planning, context generation, drift checking, or tests. A release completes only after producer verification, required consumer adoption, compatibility evidence, current documentation, and a valid tag/SHA lock.

## Current baseline

Reconciliation on 2026-07-21 found a contracts 1.2.0 candidate with only
`v1.1.0` published, newer remote release PR heads than the local checkouts, and
an uncommitted Python adoption. It also removed already-shipped search/Parquet
work from the queue and added only outstanding `QW-002` through `QW-007`
initiatives, each with an explicit planning gate where required. See
`docs/discovery/namespace-tracker-reconciliation-2026-07-21.md`.

## Development

```bash
make format-check
make lint
make test
make validate
make smoke
```

Tests use temporary repositories and need no network. Network/publishing operations are opt-in and are never exercised by the default suite.
