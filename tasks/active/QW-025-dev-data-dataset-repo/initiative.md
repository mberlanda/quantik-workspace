# QW-025: Publish `quantik-dev-data`

> **Purpose:** Get the expensive, irreplaceable half of this project off one
> machine.
> **Load with:** [`context/system/repository-map.md`](../../../context/system/repository-map.md)

## Problem and motivation

`runs/` is gitignored, is about 1.3 GB, and exists in one place. It holds days
of exact-solver time, hours of training, and every number this project has
published.

**The model repositories do not cover this.** A model repo carries weights and a
card — not the corpus the weights were fitted to, nor the probe they were scored
against. Someone who downloads all four published models still cannot reproduce
a single number in the lineup, because the corpus and the probe are not there.

Six groups, by why they are expensive:

| group | why |
|---|---|
| `corpora` | days of exact-solver time |
| `enumerations` | hours of search; `level08.npy` alone is 273 MB |
| `probe` | small, but it is the reference every evaluation is measured against |
| `opening-book` | the expensive shallow solve |
| `checkpoints` | hours per run, and `--init-from` means they are reusable |
| `evaluations` | hours of CPU per arena |

## Existing and desired behaviour

Existing: `python -m quantik_models.export.devdata <out>` stages all six with
per-group cards, a `MANIFEST.json` carrying a sha256 per file, and
`.gitattributes` for LFS. It **copies and never uploads**. Nothing is published.

Desired: the dataset repo exists, and a restore has been demonstrated rather
than assumed.

## Contracts and repositories

`quantik-models-py` owns the tooling. The artefact is a Hugging Face dataset
repository, tracked here because it is a publishing decision rather than a code
change.

## Constraints and preserved invariants

- **LFS from the first commit.** A `.npz` or `.safetensors` committed as a plain
  blob cannot be fixed later. This is the same trap `stage_hub_repos.sh`
  documents for model repos, and it is why `.gitattributes` is staged.
- **The probe is held out.** Publishing it does not change that. Its card leads
  with the fact, and `merge_corpus` excludes probe keys from the *merged result*
  because solving a position also labels its children — which is how sixteen
  probe positions reached the first corpus.
- **CC BY-NC 4.0 for data, MIT for code**, matching the model repositories.
- **Identify a file by its hash.** Two corpora here differ by one character in
  the filename and are different files; confusing them produced a wrong
  published conclusion.

## Provenance

Requested 2026-08-30: "create another hf hub repo with quantik-dev-data so we
can use it outside the gitignored runs folder … so as not to have to restart
from scratch with weeks of CPU compute thrown away."
