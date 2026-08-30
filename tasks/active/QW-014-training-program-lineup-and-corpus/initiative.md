# QW-014: Training Program — Architecture Lineup, Learning-Rate Correction, and the v3 Corpus Result

> **Purpose:** Record the training program's conclusions as workspace state, so
> they are cited rather than re-derived, and so the two things still genuinely
> open (patience, a second seed) are visible as follow-on work, not folded back
> into "training hasn't started."
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/repositories/quantik-models-py.md`](../../../context/repositories/quantik-models-py.md)

## Problem and motivation

Requested: research-grade documentation of the ResNet with layer-by-layer
visibility, alternative architectures documented to the same standard, at least
three locally-trained models, engine-vs-engine autoplay feeding future
training, and retrain/fine-tune utilities including partial layer freezing.
Twenty-nine PRs delivered all of it across 2026-08-28/29, entered nowhere in
this workspace.

## Existing and desired behaviour

Existing, verified: four architectures (`resnet`, `mlp`, `cpool`, `attn`),
parameter-matched within 0.9% and enforced by
`tests/test_parameter_matching.py`; `ArchitectureEntry.default_lr` making rate a
per-architecture property after the shared-rate bug was found; `--patience`
merged but not yet applied to the lineup (QW-012); `arena.autoplay`,
`arena.pack`, `data.merge_corpus`, and the exact oracle running a full
solve-and-retrain cycle twice (v2, v3); `export.huggingface` staging four
architecture-scoped Hub repos. Desired: this is recorded as the current,
citable state of the program, not re-discovered.

## Contracts and repositories

`quantik-models-py` only. Touches `model-checkpoint.v1` (every checkpoint's
manifest, ONNX graph and hash) and `observation.v1` (indirectly — the exact
oracle's labels are what the corpus and shift-probe evaluation are built from;
the observation exporter's own one-hot defect is QW-006's scope, not this
initiative's).

## Constraints and preserved invariants

- **Held-out accuracy has failed to predict play strength four times in this
  project.** Where validation top-1 and the arena disagree, the arena is the
  ranking that matters — this is a standing methodological result, not a single
  finding, and should not be re-litigated per architecture.
- **The seat effect dwarfs every model difference and grows with depth** —
  `cpool` swings 60.6%/38.2% at ply 3 to 77.2%/20.5% at ply 6. Any cited number
  that does not hold the seat fixed is measuring mostly this.
- Nothing from v3 is published to the Hub yet — that decision is explicitly
  gated on QW-012's outcome, not on anything in this initiative.
- `quantik-models` is **not** on PyPI — its Hub cards must not imply otherwise.

## Migration and compatibility strategy

N/A — this initiative is a recording task over completed work, not new
implementation.

## Release strategy and ordering

N/A — already executed. Forward work is split out: QW-012 (patience re-run),
QW-013 (a second position source into the same corpus pipeline).

## Risks and exclusions

Excludes re-running anything — that is QW-012's scope entirely. Excludes the
attention-encoder-as-optional-fourth and hypergraph/recurrent-propagation
follow-ons ADR 0001 gestures at; those are future architecture work, not part
of recording what already ran.

## Acceptance criteria

See `manifest.yaml`.
