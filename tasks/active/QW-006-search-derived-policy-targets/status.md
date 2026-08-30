# QW-006 Status

Plan required. Self-play already exports MCTS root visits; observation export
still synthesizes a one-hot policy target.

## 2026-08-30 reconciliation

Still `plan-required`, confirmed by reading the exporter directly, not inferring
from docs. `quantik-core-rust/crates/quantik-core/src/bench/contracts.rs`,
function `observation_v1_row`:

```rust
let mut policy_visits = vec![0u32; 64];
policy_visits[selected_action] = 1;
```

This is the exact defect the initiative describes, unchanged. Two things worth
recording so the eventual plan does not re-derive them:

- The `observation.v1` schema already supports a real distribution —
  `policy_visits` is `fixed_size_list<uint32,64>`, and the contract's own test
  fixtures use dense multi-valued arrays (e.g. counts of 2 and 6 at different
  indices), so this is an exporter gap, not a schema gap.
- `selfplay.v1`'s exporter (`selfplay_export.rs`) already carries real MCTS visit
  counts per action (`root_move_visits`, via `selfplay_v1_row`) — a working
  reference for what `observation_v1_row` should do, from an engine that already
  produces the statistic. `MoveObservation`/`cross_engine_benchmark.rs`, the actual
  caller of `observation_v1_row`, does not currently carry that distribution
  through from MCTS, so plumbing it is real work, not just a formula change.

Left active, unchanged in substance.
