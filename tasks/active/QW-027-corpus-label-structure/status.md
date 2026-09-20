

## 2026-09-20 — W2 merged

[models-py#75](https://github.com/mberlanda/quantik-models-py/pull/75) adds `data/policy_schema.py` (`dense_to_mask` / `mask_to_dense`, refusing rows not exactly uniform over their support or with weight outside {0,1}). Bit-exact on all 250,000 labelled v1 rows (local, one-off) and on a stride-10 slice in the test. **That real-corpus test skips on CI** (`runs/` is gitignored), so green CI does not exercise the claim. `atol` admits and canonicalises a near-uniform row; the round trip is not within `atol`.
