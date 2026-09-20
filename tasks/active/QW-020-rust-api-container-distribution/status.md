

## 2026-09-20 — W5 blocked on QW-017; set to plan-required

The W5 packet says it is blocked on QW-017 (ONNX model serving), but the manifest only encoded W2/W3, so the dispatch board advertised it as ready and an agent had to discover the real blocker. QW-017 has no inference code, `docs/model-serving.md` still reads "decision not yet made", and `Cargo.toml` has no runtime dependency. The validator rejects a cross-initiative id in `depends_on` and there is no "blocked" status, so W5 is `plan-required` until QW-017 lands. `docs/deployment.md` (decided) treats the Rust image as a classical-engine self-host artifact and says to reopen decision 1 if Rust gains model serving.
