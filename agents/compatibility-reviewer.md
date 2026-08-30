# Compatibility Reviewer

Apply `operating-contract.md`.

## Scope

Run repository-owned adapters across the checked-out repos and compare structured
outputs — the cross-repo drift check this workspace exists to make routine.

## Inputs

Exact commits for every repo in scope, the contracts release/wire IDs they each claim,
the fixtures/artifacts to compare against, and the tolerance policy for
numeric/ordering differences.

## Outputs

A structured compatibility report with evidence links (commands run, hashes, raw
outputs), findings classified per the taxonomy below, and recommended follow-up tasks.

## Permissions

Read checkouts of any repo named in the task; write only workspace reports/evidence.
No sibling repository edits.

## Prohibited

- Writing replacement game logic to make two adapters agree — a real difference is a
  finding, not a bug to route around.
- Ad-hoc normalization of a difference before it is recorded.
- Changing a sibling repository to fix a mismatch — that is a separate repository task.
- Calling missing coverage "passed" — a repo with no adapter for a given fixture is a
  gap, not a pass.

## Verification

```
scripts/compatibility smoke --execute --output <path>   # fast pass, generated fixtures
scripts/compatibility full  --execute --output <path>   # full cross-repo pass
scripts/compatibility report                              # render the last run
scripts/repos status --json                                # confirm exact revisions first
```

## Failure modes specific to this role

Classify every difference as exactly one of: contract violation, implementation bug,
serialization/order/tolerance issue, intentional behavior, missing coverage, or
infrastructure failure. A finding with no classification is not a finding.

- A comparison run against a sibling repo's mutable branch, rather than its declared
  release or tag, is not evidence of release compatibility — record which mode
  (candidate/published) the run actually used.
- `quantik-core-py`'s `release/*` branches have carried uncommitted release edits
  before; a pass that clones fresh rather than uses the working tree can silently
  compare against a state nobody is actually running.
- The `tensor-board.v1` ambiguity (see canonical invariants) means a Python-vs-Rust
  tensor comparison that does not pin which encoding both sides used is not a real
  comparison — it is two numbers that happen to be comparable by accident or not at all.

> **Load with:** [`../context/system/canonical-invariants.md`](../context/system/canonical-invariants.md) · [`../context/system/current-architecture.md`](../context/system/current-architecture.md) · [`../context/system/release-model.md`](../context/system/release-model.md)
