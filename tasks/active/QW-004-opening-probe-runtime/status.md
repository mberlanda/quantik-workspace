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
- `WORKSTREAMS.md` workstream 10 ("coverage expansion") is about labelling more of
  `runs/canonical/level0N.npy` with the exact oracle so the network trains on shallower
  plies — a corpus-size question, not the compact probe-key/value/bound contract and
  symmetry-safe Rust lookup this initiative specifies. It is a plausible *consumer* of
  QW-004 once QW-004 exists, not a substitute for it.

Left active, unchanged in substance.
