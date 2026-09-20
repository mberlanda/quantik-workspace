# Handover — task decomposition

Written 2026-09-07, at the end of the session that produced PRs #21, #22, #24 and #25.
Everything derivable from the manifests lives in
[`../docs/generated/dispatch-board.md`](../docs/generated/dispatch-board.md) and
[`../docs/generated/task-dependency-graph.md`](../docs/generated/task-dependency-graph.md);
this file holds only what those cannot express — the calls still to be made, the findings
that changed conclusions, and the follow-ups nobody owns yet.

Refresh the derived view first, and trust it over the numbers below:

```sh
quantik-workspace task status
quantik-workspace reports generate && quantik-workspace validate all
```

## State as of this writing

76 work items across 23 active initiatives. 15 ready now, 61 waiting.
**18 items across 9 initiatives are still `plan-required`** and cannot be dispatched.

An earlier note in the session said "five initiatives"; that was wrong. QW-006, QW-022
and QW-028 also carry placeholders and were missed. The list below is the counted one:

| Initiative | Placeholders | Complexity | Blocked on | What the decision pass has to settle |
|---|---|---|---|---|
| QW-007 | 4 | XL | — (`QW-001` is completed) | Runtime/weights format, capability negotiation, and the parity tolerance. Four repos; the checkpoint surface is the one most likely to break silently. |
| QW-003 | 3 | XL | — | Opening selection, engine pairing, determinism, provenance. The correctness risk is canonical-orientation move reuse in Rust. |
| QW-005 | 3 | XL | QW-002, QW-003, QW-004, QW-006, QW-007 | The whole active-learning loop. **Do not decompose yet** — five unfinished dependencies mean any breakdown is rewritten before it is dispatched. |
| QW-006 | 2 | L | — | Engine-specific policy-mass semantics, the weighting/fallback rule, and the one-hot baseline comparison. Best value-per-effort of the undecomposed set: two items, bounded criteria, no cross-language parity. |
| QW-017 | 2 | XL | QW-019 | `tract-onnx` vs `ort`, settled by loading all four published graphs — the initiative says explicitly "not by argument". LayerNormalization (fused, opset 17+) is the operator that decides it. |
| QW-028 | 1 | M | QW-021 | Nothing, really. Small implementation (progress reporting; resume already exists in `exact_oracle`), hours of wall clock. Decompose whenever QW-021's partition lands. |
| QW-011 | 1 | S | — | **Scope first.** The generator shipped in models-py #51. The remaining work is a picker UI in `quantik-qfen-visualizer`, and that repo is not in `affected_repositories` — so the real work has nowhere to be dispatched. Add the repo and a second work item, the way QW-019's W4 did. |
| QW-022 | 1 | S | — | Whether `e2e-data-pipeline.yml` pins a ref for `quantik-core-py` or installs the published package. Cheap, and it currently tracks that repo's `main` silently. |
| QW-029 | 1 | XL | — | **Scope first.** `problem:` is literally "To be refined." and there are no real acceptance criteria. This needs a scoping pass with the user, not an implementation agent. |

## Suggested order

1. **QW-006** — two items, no open cross-repo risk, unblocks part of QW-005.
2. **QW-022** and **QW-011** — both are one decision plus a small edit; QW-011 needs the
   missing repository added before it means anything.
3. **QW-007**, then **QW-003** — the two XLs that block QW-005. Each wants its own
   decision pass with human review before dependents start.
4. **QW-017** — after QW-019 W1 merges. The bake-off is empirical; budget for actually
   running it.
5. **QW-028** — after QW-021's partition design.
6. **QW-005** — last. It is the join point for everything above.
7. **QW-029** — whenever the user is ready to say what it is.

## How the breakdowns were done

The rule is in [`dispatch-sizing.md`](dispatch-sizing.md) and it is the only thing that
made small items possible:

> An initiative's open decisions become their own `judgment` work item, and everything
> else depends on it.

QW-019 is the worked example — two open questions became `decisions.md#D2` and `#D3`, and
the remaining five items collapsed into a registration and four single-file renames.
Measured bundles run 7.8-13.8 KB, comfortably inside a 64k window.

Grounding packets in the actual repositories, rather than in the manifest's description of
them, changed conclusions four times. Do this before sizing anything:

- **QW-009 is nearly done** — `OnnxEvaluator`, the torch-parity test and the Dockerfile all
  already exist. Rated M, actually S.
- **QW-024's arena script is already written**, determinism trap and control included.
- **QW-020 was never blocked** — its own criteria say the base image ships before QW-017.
- **Three initiatives named repositories missing from `affected_repositories`** (QW-019
  visualizer, QW-021 articles, QW-018 visualizer). QW-011 is the fourth, still open.
  Check this on every initiative you touch; it is the most common defect in the set.

## Loose ends

- **Packet filenames lie in three places.** QW-015 W2/W3 and QW-022 W2 are `completed` but
  still point at `W<N>-plan-required.md`. Harmless to validation, misleading to a reader,
  and they make `grep -rl plan-required` overcount.
- **Coordinator follow-ups** — noted inside packets, owned by nobody, and not work items
  because `quantik-workspace` is not in `workspace.yaml`'s repositories:
  - update ADR 0014 after QW-023 W3 lands;
  - close out QW-012's seed-decision text in `status.md` after QW-026.
- **The compatibility matrix still withholds `supported` at every release.** The blocker is
  mechanical and is queued as QW-015 W8/W9 (both ready now): `workspace.yaml` declares the
  two portability adapters without their required `--contracts-root` and `--output`
  arguments, so both exit 2. It is the cheapest high-value fix open.
- **No `releases/active/` record exists for any planned version**, deliberately — see
  [`../docs/releases/release-plan.md`](../docs/releases/release-plan.md). Open a QREL only
  when the gating initiatives have merged. QREL-2026-001 is why.

## Things a fresh session gets wrong

- `quantik-workspace` is **not** in `workspace.yaml`'s repositories, so ADR and workspace
  edits cannot be work items.
- `schemas/*.json` are orphaned — real validation is hand-rolled in
  `tasks.py::validate_initiative` / `validate_work_items`. Extra manifest keys are safe.
- Tests run as `python -m unittest discover -s tests -v`. Adding `-t .` breaks the helper
  imports.
- Manifests are JSON with alphabetically sorted keys (`config.dump_data()`), which is also
  valid YAML. Do not hand-format them.
- Versioning is lockstep across the core trio: tag contracts first, then **py before rust**.
