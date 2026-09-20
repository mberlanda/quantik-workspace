# QW-004 Status

Plan required. `opening-probe.v1` is mentioned in design documents but is not
registered or implemented.

## 2026-08-30 reconciliation

Still `plan-required`. Verified: `opening-probe.v1` has no schema file under
`quantik-core-contracts/schemas/` — it appears only in prose docs, same as when this
initiative was written.

Do not confuse this with two things that sound related but are not it:

- `quantik-models-py/src/quantik_models/arena/probe.py` is the **H2H accuracy harness**
  (agent-vs-exact-truth scoring), not a runtime opening-book lookup surface.
- [`WORKSTREAMS.md`](../../../docs/history/workstreams-archive.md) workstream 10 ("coverage expansion") is about labelling more of
  `runs/canonical/level0N.npy` with the exact oracle so the network trains on shallower
  plies — a corpus-size question, not the compact probe-key/value/bound contract and
  symmetry-safe Rust lookup this initiative specifies. It is a plausible *consumer* of
  QW-004 once QW-004 exists, not a substitute for it.

Left active, unchanged in substance.

## 2026-09-20 — W1 decided and merged

[contracts#28](https://github.com/mberlanda/quantik-core-contracts/pull/28) records the probe design in `docs/opening-probe-v1.md`; D0-D6 accepted as recommended:

- sorted fixed-width binary file (28-byte records, JSON metadata header, binary search);
- the 18-byte `canonical_key.v1` stored verbatim, sorted **bytewise** (numeric `u16` order would miss keys);
- value is `game_value` in {-1, 0, +1}, a `status` byte and a u64 set of all optimal actions in the representative's frame; a `bounded` record with 0 means unknown, never draw;
- transform derived at probe time, and stored actions mapped back with the **inverse** of the caller-to-representative transform (worked example: action 22 maps to 42; applying the transform itself gives 37);
- fail fast on corruption, version or checksum mismatch, unsorted keys, and an illegal mapped-back action; only a missing key or out-of-coverage ply is a miss;
- `opening-book.v1` keeps its version; W2 adds two clarifying sentences.

W3 needs `find_canonical_with_transform` in core plus a Python analogue. Not advisor-reviewed before merge; the worked example was re-verified independently by the agent.
