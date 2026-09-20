

## 2026-09-20 — W3 merged

[models-py#76](https://github.com/mberlanda/quantik-models-py/pull/76) adds `scripts/induct_shallow.py`: it checks v3's ply-3 canonical key *set* against `runs/canonical/level03.npy` (never a count) and that every ply-3 row carries an optimal-move set (an advisor-review fix), aborting with exit 2 naming the keys, then back-inducts plies 2, 1, 0. Real v3: 1 + 3 + 51 = 55 positions; ply 0 is lost for the mover (all 64 moves optimal), all 3 ply-1 positions are won (9 optimal moves each), 44 of 51 ply-2 positions are won. Against v2 (664 of 726 at ply 3) it aborts, as intended.

- **W4 (independent oracle confirmation) is still open**; nothing here is confirmed against a direct solve of levels 1-2.
- The artefact is *not* stored (`runs/oracle/shallow-induced.npz` by default): **W6 must regenerate it with the script**, not look for a file.
- `mypy` is configured over `src/` only, so `scripts/induct_shallow.py` and its test are not type-checked. The real-corpus test needs `QUANTIK_RUNS_DIR` and skips on CI; the other 7 tests run there.
