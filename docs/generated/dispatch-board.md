# Dispatch Board

Generated from `tasks/active/*/manifest.yaml`. One row per work item — the unit an agent is actually assigned. `ready` means nothing blocks it today.

Generate a work item's execution bundle with:

```sh
quantik-workspace context task <INITIATIVE> <REPOSITORY> --work-item <ID> \
  --budget 64000 --output /tmp/<ID>.md
```

**15 ready now · 61 waiting.** `dispatch` says what kind of agent an item wants: `mechanical` (every decision already made — a small model is enough), `execute-and-record` (run the specified thing, report real output), `judgment` (a real call to make — capable model, human review).

## Ready now

| Initiative | Item | Repository | Complexity | Dispatch | Branch |
| --- | --- | --- | --- | --- | --- |
| `QW-002` | `W1` | `quantik-models-py` | M | judgment | `docs/pipeline-profile-design` |
| `QW-004` | `W1` | `quantik-core-contracts` | L | judgment | `docs/opening-probe-design` |
| `QW-009` | `W1` | `quantik-models-py` | S | mechanical | `feat/publish-image-workflow` |
| `QW-015` | `W1` | `quantik-core-contracts` | S | mechanical | `fix/unfuse-contract-version` |
| `QW-015` | `W5` | `quantik-core-contracts` | M | mechanical | `feat/release-preflight` |
| `QW-015` | `W6` | `quantik-core-contracts` | S | mechanical | `chore/single-version-literal` |
| `QW-015` | `W8` | `quantik-core-py` | S | mechanical | `fix/portability-report-defaults` |
| `QW-015` | `W9` | `quantik-core-rust` | S | mechanical | `fix/portability-report-defaults` |
| `QW-019` | `W1` | `quantik-core-contracts` | M | mechanical | `feat/register-engine-contracts` |
| `QW-020` | `W1` | `quantik-api-rust` | M | mechanical | `feat/dockerfile` |
| `QW-021` | `W1` | `quantik-models-py` | L | judgment | `docs/opening-coverage-partition` |
| `QW-023` | `W1` | `quantik-models-py` | M | execute-and-record | `feat/corpus-axis-converged-run` |
| `QW-024` | `W1` | `quantik-models-py` | M | execute-and-record | `feat/opening-arena-results` |
| `QW-026` | `W1` | `quantik-models-py` | S | execute-and-record | `feat/patience-arena-second-seed` |
| `QW-027` | `W1` | `quantik-models-py` | M | execute-and-record | `docs/corpus-structure` |

## Waiting

| Initiative | Item | Repository | Complexity | Dispatch | Waiting on |
| --- | --- | --- | --- | --- | --- |
| `QW-002` | `W2` | `quantik-models-py` | M | mechanical | QW-002.W1 |
| `QW-002` | `W3` | `quantik-models-py` | M | mechanical | QW-002.W2 |
| `QW-002` | `W4` | `quantik-models-py` | S | mechanical | QW-002.W3 |
| `QW-003` | `W1` | `quantik-core-contracts` | - | - | plan-required |
| `QW-003` | `W2` | `quantik-core-rust` | - | - | QW-003.W1 |
| `QW-003` | `W3` | `quantik-models-py` | - | - | QW-003.W2 |
| `QW-004` | `W2` | `quantik-core-contracts` | M | mechanical | QW-004.W1 |
| `QW-004` | `W3` | `quantik-core-rust` | L | mechanical | QW-004.W2 |
| `QW-004` | `W4` | `quantik-core-rust` | M | execute-and-record | QW-004.W3 |
| `QW-005` | `W1` | `quantik-core-contracts` | - | - | QW-002, QW-003, QW-004, QW-006, QW-007 |
| `QW-005` | `W2` | `quantik-core-rust` | - | - | QW-005.W1, QW-002, QW-003, QW-004, QW-006, QW-007 |
| `QW-005` | `W3` | `quantik-models-py` | - | - | QW-005.W2, QW-002, QW-003, QW-004, QW-006, QW-007 |
| `QW-006` | `W1` | `quantik-core-rust` | - | - | plan-required |
| `QW-006` | `W2` | `quantik-models-py` | - | - | QW-006.W1 |
| `QW-007` | `W1` | `quantik-core-contracts` | - | - | plan-required |
| `QW-007` | `W2` | `quantik-core-py` | - | - | QW-007.W1 |
| `QW-007` | `W3` | `quantik-core-rust` | - | - | QW-007.W1 |
| `QW-007` | `W4` | `quantik-models-py` | - | - | QW-007.W1 |
| `QW-009` | `W2` | `quantik-models-py` | S | execute-and-record | QW-009.W1 |
| `QW-010` | `W1` | `quantik-models-py` | M | judgment | QW-024 |
| `QW-010` | `W2` | `quantik-models-py` | S | mechanical | QW-010.W1, QW-024 |
| `QW-011` | `W1` | `quantik-models-py` | - | - | plan-required |
| `QW-015` | `W2` | `quantik-core-rust` | - | - | completed |
| `QW-015` | `W3` | `quantik-core-py` | - | - | completed |
| `QW-015` | `W4` | `quantik-core-contracts` | S | mechanical | QW-015.W1 |
| `QW-015` | `W7` | `quantik-core-contracts` | S | execute-and-record | QW-015.W1, QW-015.W4 |
| `QW-016` | `W1` | `articles` | M | judgment | QW-015 |
| `QW-016` | `W2` | `articles` | S | judgment | QW-015 |
| `QW-017` | `W1` | `quantik-api-rust` | - | - | QW-017.W2, QW-019 |
| `QW-017` | `W2` | `quantik-models-py` | - | - | QW-019 |
| `QW-018` | `W1` | `quantik-core-contracts` | M | judgment | QW-019 |
| `QW-018` | `W2` | `quantik-core-contracts` | M | mechanical | QW-018.W1, QW-019 |
| `QW-018` | `W3` | `quantik-api-rust` | M | mechanical | QW-018.W2, QW-019 |
| `QW-018` | `W4` | `quantik-qfen-visualizer` | S | mechanical | QW-018.W2, QW-019 |
| `QW-019` | `W2` | `quantik-api-rust` | S | mechanical | QW-019.W1 |
| `QW-019` | `W3` | `quantik-qfen-visualizer` | S | mechanical | QW-019.W1 |
| `QW-019` | `W4` | `quantik-models-py` | S | mechanical | QW-019.W1 |
| `QW-019` | `W5` | `quantik-models-py` | S | mechanical | QW-019.W3, QW-019.W4 |
| `QW-020` | `W2` | `quantik-api-rust` | M | mechanical | QW-020.W1 |
| `QW-020` | `W3` | `quantik-api-rust` | S | execute-and-record | QW-020.W1 |
| `QW-020` | `W4` | `quantik-api-rust` | S | judgment | QW-020.W1 |
| `QW-020` | `W5` | `quantik-api-rust` | M | mechanical | QW-020.W2, QW-020.W3 |
| `QW-021` | `W2` | `quantik-models-py` | S | execute-and-record | QW-021.W1 |
| `QW-021` | `W3` | `quantik-models-py` | M | execute-and-record | QW-021.W2 |
| `QW-021` | `W4` | `quantik-models-py` | S | mechanical | QW-021.W3 |
| `QW-021` | `W5` | `quantik-models-py` | L | execute-and-record | QW-021.W4 |
| `QW-021` | `W6` | `quantik-models-py` | M | mechanical | QW-021.W5 |
| `QW-021` | `W7` | `articles` | M | mechanical | QW-021.W5 |
| `QW-022` | `W1` | `quantik-models-py` | - | - | plan-required |
| `QW-022` | `W2` | `articles` | - | - | completed |
| `QW-023` | `W2` | `quantik-models-py` | M | execute-and-record | QW-023.W1 |
| `QW-023` | `W3` | `quantik-models-py` | M | judgment | QW-023.W2 |
| `QW-024` | `W2` | `quantik-models-py` | M | judgment | QW-024.W1 |
| `QW-026` | `W2` | `quantik-models-py` | S | mechanical | QW-026.W1 |
| `QW-027` | `W2` | `quantik-models-py` | M | mechanical | QW-027.W1 |
| `QW-027` | `W3` | `quantik-models-py` | M | mechanical | QW-027.W2 |
| `QW-027` | `W4` | `quantik-models-py` | S | execute-and-record | QW-027.W3 |
| `QW-027` | `W5` | `quantik-models-py` | S | mechanical | QW-027.W1 |
| `QW-027` | `W6` | `quantik-models-py` | S | mechanical | QW-027.W4, QW-027.W5 |
| `QW-028` | `W1` | `quantik-models-py` | - | - | QW-021 |
| `QW-029` | `W1` | `quantik-models-py` | - | - | plan-required |
