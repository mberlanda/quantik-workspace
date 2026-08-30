# WORKSTREAMS archive — imported 2026-08-30

> **Purpose:** the narrative and measured history that accumulated in the root
> `WORKSTREAMS.md` before this workspace became the source of truth.
> **Status:** **archive. Do not add to it, and prefer the initiatives in
> [`../../tasks/`](../../tasks/) wherever the two disagree.**
>
> It is imported because roughly thirty documents across this repo cite it by section,
> and it previously lived in an untracked directory outside every git repo — so those
> citations could not be followed by anyone who cloned this workspace, and the history
> existed on exactly one machine.
>
> It has known errors, kept visible rather than edited out because they are the reason
> this consolidation happened. The clearest: it states in two places that
> `quantik-api-rust` has no git remote. It has one, in sync. That false claim shaped a
> delegation plan for weeks.

---

## Status snapshot — 2026-08-29

The **1.2.0 release is fully shipped**. All three release repos are tagged `v1.2.0`, and
`quantik-core` 1.2.0 is live on both registries.

The **active thread has moved from training to playing.** Workstream 11 (the training
program) is complete for now — its last open question, the epoch budget, was resolved
2026-08-29 and is recorded below. Nothing is running.

**Where to pick up: workstreams 13, 14 and 15**, all requested 2026-08-29 and all
untouched. In priority order as the user framed them:

| | what | state | next action |
|---|---|---|---|
| **13** | Public Docker deployment, no data store | not started | build `OnnxEvaluator` behind a torch-vs-ONNX agreement test, then the Dockerfile |
| **14** | Skill levels + "how to play" for non-expert players | not started | derive the level-to-opponent mapping from the arena tables **before** any UI |
| **15** | Puzzle mode in the browser | generator merged (py#51), UI not started | generate a pack, commit it to the visualizer, build the picker |

**Workstream 13 was recorded as blocked on a user decision. It is not, as of 2026-08-30.**
The torch-vs-ONNX question was framed as "~1 GB image vs build an evaluator first", which
made the two sides look comparable. Measured, they are not: `torch` is **529 MB** installed
against `onnxruntime`'s **80 MB**, `onnxruntime` is already a declared extra already running
graphs in the test suite, and the exported graph signature matches the one-method
`Evaluator` protocol exactly. The evaluator is a small adapter, not a project. See 13.3.
Everything else about the storeless deployment already works — `--no-store` opens no
database and `POST /api/games` answers 503.

**Delegation briefs are now the `plan.md` of their task packet** — [`QW-012`](../../tasks/active/QW-012-lineup-under-patience/plan.md) and [`QW-013`](../../tasks/active/QW-013-play-store-solver-queue-export/plan.md); the
top-level `briefs/` directory this line originally named no longer exists. Two charters are written up in full
for a separate session, both single-repo (`quantik-models-py`) and needing none of the
cross-repo context in this file. **The play-store solver-queue export is done** (py#53,
see §11 "Still to build"). **The `--patience` lineup rerun is still open** — its shape
is different: long compute with a built-in stop-and-decide gate before launching it.

**Independence, for splitting across sessions:** 15 touches only the visualizer and a
static JSON pack, and needs no play service and no models — it is the one that can run
fully parallel to everything else. 14 also lands only in the visualizer, but its *input*
(the level mapping) has to be derived from models-py arena tables first, so it splits into
a research half and a UI half. 13 spans models-py and the visualizer together and should
not be split.

### The play service is built and running

Seven PRs merged 2026-08-29 across two repos. The service serves the visualizer, plays 20
opponents, analyses positions, and records games to
`~/.local/share/quantik/games.db`:

- **models-py** — #45 move handler, #47 replay-and-verify, #48 HTTP server,
  #49 the inert seed, #50 the analysis endpoint, #51 the puzzle generator.
- **visualizer** — #3 play client, #4 solver-verified examples, #5 mobile piece picker,
  #6 evaluation bar and move analysis.

Two findings from that work are recorded in `quantik-models-py/docs/autoplay.md` and are
worth knowing before trusting an arena number again:

1. **The seed decided nothing** for any network agent — `PolicyAgent` defaults to argmax
   and `NetMCTSAgent`'s RNG only ever fed the disabled Dirichlet noise. No published
   margin is invalid (every lineup run used random starts) but at `--start-plies 6` a
   300-game pairing held **263-272 distinct games**, so `arena.pack`'s intervals divide by
   300 and should divide by nearer 265.
2. **The `uniform-mcts` control barely searches.** With uniform priors and a flat zero
   value, FPU reduction locks PUCT onto its first descent — measured, **64 of 64 visits on
   one action**. It still works as a floor, but the gap between a network and that control
   overstates the network's contribution relative to a search that explores. Deliberately
   not changed, because it would change what the published control means.

Earlier training history: twenty-nine PRs merged across 2026-08-28/29 — four architectures
trained and evaluated three ways, a learning-rate sweep that reversed three published
conclusions, autoplay, a shift evaluation, a training preflight, fine-tuning with layer
freezing, committed benchmark figures, convergence-based stopping, and Hugging Face
staging.

**The v3 corpus chain — FINISHED 2026-08-29, kept for the record.** Four stages, each
gated on the previous one's **completion marker in its log** (not on a process being
absent — see the note under workstream 11 on why a `pgrep` gate is broken):

| stage | writes | log |
|---|---|---|
| ~~exact solve, 17,062 positions~~ **DONE 11:32, 50 min** | `runs/eval/oracle-2026-08-29/packed/solved.jsonl` | `scratchpad/solve.log` |
| ~~merge into v3~~ **DONE 11:33** | `runs/oracle/corpus/exact-sampled-v3.npz` | `scratchpad/v3.log` |
| retrain `cpool` from scratch, 6e-4, seed 20260828, 16 epochs | `runs/train/v3-cpool/` | `scratchpad/v3.log` |
| shift eval + oracle arena + v2-vs-v3 head to head | `runs/eval/v3-2026-08-29/` | `scratchpad/v3-eval.log` |

The scripts live in this session's scratchpad
(`/private/tmp/claude-501/-Users-mauroberlanda-Code-quantik-ns/84d6942d-*/scratchpad/`),
which is **temporary**. If the chain has to be restarted from a cold session, the three
commands are: `merge_corpus --corpus …v2.npz --solved …packed/solved.jsonl --out
…v3.npz`; `train.supervised --arch cpool --preset medium --corpus …v3.npz --name
v3-cpool --epochs 16 --lr 6e-4 --seed 20260828`; then `eval.shift` on both checkpoints
and `arena.autoplay --against minimax-d2 --seed 20260907`.

**v3 exists: 3,520,526 rows, 271,676 policy-labelled.** The 17,062 solved
positions became **380,041 rows** — about 22 free child labels each — and
56,473 rows were dropped in the merge to canonical-key duplicates and probe
exclusion. **Verified directly: v3 shares zero canonical keys with the
7,800-position probe**, which is the invariant every evaluation number rests
on.

Where the corpus actually grew, v2 -> v3: ply 6 **86,631 -> 170,766** (nearly
doubled), ply 5 **22,655 -> 29,905**, ply 4 9,664 -> 9,758, ply 3 664 -> 726.
So the growth is concentrated at plies 5-6 — which is where the shift probe's
shallow band sits and where the models are weakest. If v3 does not help there,
it does not help.

### The v3 outcome — the chain is complete

**The whole chain finished 2026-08-29.** Result in one line: **the held-out
policy accuracy this project ranks architectures with did not predict play
strength.**

`v3-cpool` vs `swept-cpool` — same architecture, rate, seed and epoch count,
only the corpus differs. Shift probe: **+0.0002 policy accuracy, p = 1.0**.
In play:

| condition | v2's win rate vs v3 | |
|---|---|---|
| policy, ply 3 | 42.8% [39.8, 45.9] | v3 wins |
| policy, ply 6 | 49.1% [46.0, 52.2] | tie |
| MCTS-128, ply 3 | 45.1% [41.7, 48.6] | v3 wins |
| MCTS-128, ply 6 | 48.9% [45.4, 52.3] | tie |

And `v3-cpool` **beats `minimax-d2` at 59.7% [57.5, 61.8]** — the first model
here to do so. `swept-cpool` scored 48.9% on the same seed, reproducing its
independent 49.4%.

**The confound was tested, not waved away.** v3's added positions came from
network-vs-minimax games, so the oracle result is suspect alone. Net-vs-net
positions are **not** in v3's data; against `attn`/`resnet`/`mlp` v3 wins
66.7% / 64.2% / 66.3%, all significant. The ply-3 gain is real. It vanishes
at ply-6 starts across all four measurements.

**What moved was the value head:** MAE 0.0777 -> 0.0351, sign 0.9646 ->
0.9859. Note the value target is **±1**, not a margin — `rows_from_oracle`
collapses the solver's exact per-action scores to a sign — so this is
calibration on who wins, not an evaluation function.

**A prediction that failed, recorded because it was mine:** the value gain
does *not* amplify under search. Policy gap at ply 3 is 14.4 points; under
128-sim MCTS it is 9.8. Search narrows it.

**The cost, and what to try before touching the architecture.** Deep-band
policy accuracy fell 0.0047 (**p = 0.033**) while ply 4 gained 0.0359
(p = 0.006). Half a point on a band sitting at 0.987 does not justify
structural surgery before the cheap causes are excluded, in this order:

1. **Epochs.** v3's corpus is 10% larger and got the same 16 epochs, so every
   position saw ~10% fewer gradient steps. `--patience` (py#38) exists for
   exactly this and has not been used on it.
2. **Loss balance.** `supervised.py:141-143` normalises policy loss by the
   sum of policy weights but averages value loss over *every* row. The
   value-only fraction is now 92.28% (was 92.02%), so the value gradient's
   share drifted up — the mechanism that produces exactly this signature.
   `--value-loss-weight` is the knob.
3. **Capacity** — `--preset large`.
4. Only then structure: separate policy/value trunks, a deeper policy head,
   or an explicit ply embedding rather than the current scalar plane 8.

**Hardware note, because it was nearly got wrong:** the machine is an Apple
M5 Pro with a **20-core GPU — one Metal device, not 20 devices** — and
`resolve_device("auto")` already returns `mps`. Every run so far was on it.
There is no unused faster path. Measured per-run: `mlp` 6.8 min, `resnet`
29.0, `cpool` 57.6, `attn` 96.9.

### The complete lineup, one evaluation, seed 20260909

`runs/eval/lineup-2026-08-29/` — every number below from one run.

| | policy p3 | policy p6 | MCTS p3 | MCTS p6 |
|---|---|---|---|---|
| `cpool-v3` | **63.1%** | 51.8% | **67.4%** | 55.8% (4th) |
| `cpool` (v2) | 52.7% | 53.0% | 64.4% | **57.7%** |
| `attn` | 48.3% | **53.6%** | 53.9% | 57.0% |
| `resnet` | 46.5% | 46.8% | 58.7% | 56.5% |
| `mlp` | 39.5% | 44.7% | 55.0% | 53.5% |

Shift probe: `cpool-v3` now tops the **shallow** band (0.9358) and has the
best value MAE in the family by a wide margin (**0.0351** against 0.0777).

**v3 is not "the better model". It is a different model with a sharply
depth-dependent advantage** — dominant from ply-3 starts, at or below v2 from
ply 6 in every condition. Six measurements, one seed, all consistent. That
matches where the corpus grew: 13,383 new positions at ply 6 and 3,251 at ply
5, nothing meaningfully shallower. A ply-3 start traverses that whole region;
a ply-6 start begins at its edge.

At ply 6 the four leading intervals overlap heavily (55.8-57.7 under search),
so **the ply-6 ordering is noise-width and no claim should rest on it.**

### Overfitting is not the constraint — measured, not assumed

Train-minus-validation top-1 at the final epoch: `mlp` -0.0005, `resnet`
+0.0021, `swept-cpool` +0.0067, `swept-attn` +0.0082, `v3-cpool` +0.0100.
Under one point everywhere; peak-to-final decay is at most +0.0012. The
models **plateau, they do not degrade**, so spending more epochs is low-risk.

That inverts the diagnosis: v3's deep-band regression is more likely
**underfitting** (10% larger corpus, same 16 epochs, ~10% fewer steps per
position) than capacity or overfitting.

*Do not misread the early epochs:* the gaps start at -0.15 because
`train_top1` accumulates during the epoch while the model is still improving,
and augmentation applies to train and not validation.

### The plan, and why epochs come before seeds

**Running 2026-08-29 14:15 — the epoch test.** Two runs, `cpool` on v2 and on
v3, `--epochs 40 --patience 5`, everything else identical to the published
runs. Sequential, because the GPU is one Metal device and concurrent runs
contend rather than scale. Log: `scratchpad/epoch-test.log`. Checkpoints:
`runs/train/patience-cpool-{v2,v3}/`.

**Seeds come after, not before.** This project already made this call once,
during the learning-rate flaw: *"a second seed was queued and then cancelled:
replicating a possibly-unfair configuration is the wrong thing to spend
compute on."* The fixed 16-epoch budget is the same class of flaw and is now
the leading explanation for the one result blocking publication. Seeding it
three times would buy a precise estimate of a quantity there is reason to
think is biased.

**A consequence to be ready for rather than discover.** If the epoch test
closes the deep-band regression, then **every published number in this file
is a fixed-budget number from a superseded protocol** — the lineup, the
shift evaluation, the arenas and the oracle benchmark were all run at 16
epochs chosen when the ResNet was the only architecture. The comparison
would want re-running under the new stopping rule before anything else is
concluded from it, and that is a ~10 h job, not a patch. If the test does
*not* close it, the published numbers stand and the regression is a real
property of the v3 corpus.

Seed options once the protocol is settled — **A (targeted)**: 3 seeds x
`cpool` on v2 and v3, ~6 h, answers whether the ply-3 gain is seed-robust.
**B (full)**: 3 seeds x 4 architectures, ~10.5 h, answers whether the
architecture ranking is seed-robust. A is what blocks publication.

**Nothing from v3 is published.** Before the Hub weights change: settle the
protocol (running), then seeds, then decide whether the published model
optimises arena strength or held-out accuracy. When it does go up it should
be a new **revision** of `quantik-cpool-c191-b6`, not a new repo.

**Three caveats that must survive into the write-up:**

1. **IID validation top-1 is not comparable between v2 and v3 runs.** The validation
   split is derived from the corpus, so a bigger corpus is a different validation set.
   Only the shift probe (identical, held out of both by `merge_corpus`) and the arena
   against a fixed opponent compare.
2. **The corpus is now partly self-selected.** v3's new positions came from games these
   same networks played, so it is biased toward the distribution `cpool` plays into,
   which should flatter it in the arena. The shift probe is unaffected. This is a
   pre-existing property of the pipeline — v2 has it too — not something v3 introduces.
3. **One variable at a time.** From scratch rather than warm-started, and 16 fixed epochs
   rather than `--patience`, so the only difference from the published run is the corpus.
   The warm start is the better *practice* (`retrain-and-finetune.md` argues for it) and
   the wrong *experiment* here.

The oracle benchmark that produced this queue is **done and merged** (py#40): `cpool` is
even with a two-ply search. See workstream 11.

**Why the whole queue and not a subset.** The user was asked and chose "solve a plies 5-6
subset first", because the solve had been sized at **22 hours** — an estimate carried over
from an earlier batch's 4.7 s/position average. Timing the solver *per ply* showed cost
rising ~7x per ply shallower (ply 6: 0.035 s, ply 5: 0.21 s, ply 4: 1.55 s, ply 3: ~11 s)
against a queue that is 82% ply 6, giving **~40 minutes** — and the solver turned out to
be multi-threaded on top of that. The subset existed only to avoid a cost that was not
real, so the full queue went in. Do not reintroduce the subset.

| Repo | Remote | v1.2.0 tag | Last `main` CI (verified 2026-08-28) |
|---|---|---|---|
| `quantik-core-contracts` | GitHub | yes | `validate-contracts`: success |
| `quantik-core-rust` | GitHub | yes | `Rust CI/CD`: success |
| `quantik-core-py` | GitHub | yes | `Integration Tests`: success |
| `quantik-models-py` | GitHub | — | `Tests`, `E2E Data Pipeline`, `Train Smoke`: success |
| `quantik-qfen-visualizer` | GitHub | — | not checked |
| `quantik-workspace` | GitHub | — | `scheduled-drift-check`: success |
| `quantik-api-rust` | **none** | — | no CI |
| `articles` | **none** | — | no CI |

Published: `quantik-core` **1.2.0** on [PyPI](https://pypi.org/project/quantik-core/1.2.0)
and [crates.io](https://crates.io/crates/quantik-core/1.2.0).

**`quantik-models-py` is now genuinely green**, and the reason it previously was not is
worth keeping: its `main` tick predated the 1.2.0 merges, and the suite that would have
caught the breakage was being skipped rather than run. `e2e-data-pipeline.yml` did call
pytest, but installed `[dev,arrow]` with no torch, so six of fourteen test modules
`importorskip`ed away silently — every model, export, trainer and arena test. Fixed in
[py#13](https://github.com/mberlanda/quantik-models-py/pull/13); see workstream 11.

---

## 1. The 1.2.0 release — DONE

Three repos share one version number, and each one's PR CI proved that version by reading
the *other* repo's `main`. That made the release unlandable by construction: a circular
wait. It was broken by merging one release PR while its own `main` was knowingly red, then
merging the second, then re-running the first.

**Shipped:** contracts#19, rust#37, rust#39, rust#40, py#46 — all merged 2026-08-28.
Annotated `v1.2.0` tags on contracts, rust and py. Tag order matters: **py must be tagged
before rust**, because rust's tag build checks out py at the same tag ref.

**Next action:** none. Carry the lessons into workstream 2.

---

## 2. Release-engineering hardening — NOT STARTED

The deadlock is fixable at its root, and the root is one line in a shared validator.
`normalize_summary()` returns a dict that includes `contract_version`, and `main()` fails
when the Rust and Python dicts differ — so the cross-implementation check ("do the two
engines agree about the game?") silently also enforces "are both stacks on the same
release?". Two claims with different lifetimes fused into one comparison.

**Next action** — in rough priority order:

1. Exclude `contract_version` from the Rust-vs-Python equality in
   `quantik-core-contracts/scripts/validate_opening_book_summary.py`, keeping it for the
   `--expected-release` assertion. This single change removes the deadlock.
2. Drop `expected-release` from both PR-time jobs — **and** remove its `default: "1.2.0"`
   in `quantik-core-contracts/actions/opening-book-consistency/action.yml`, or omitting the
   input silently reintroduces the literal.
3. Auto-tag contracts when `VERSION` changes on `main`.
4. Add a release preflight that checks the tag does not exist, `VERSION` matches, and every
   downstream-referenced action path still exists at that ref.
5. One version literal per repo, everything else derived.
6. Drop the sibling-repo checkout from tag builds.

**Detail:** artifact <https://claude.ai/code/artifact/4c46329e-7678-41f5-bb7a-14912861bc0e>

---

## 3. Substack article — DRAFT COMPLETE, UNPUBLISHED

An article about the deadlock for the Wednesday puzzle/philosophy slot. Title and subtitle
are in the front matter. Deliberately carries **no "Part N"** — the Wednesday slot has
never used one, and Parts VI/VII are already queued.

- Draft: `articles/the-deadlock.md`
- Figures: `articles/images/12-deadlock.png` (hero + cover), `13-two-checks.png`,
  `14-rollout.png`, `15-philosophers.png`
- Generators: `articles/make_release_figures.py`, `articles/make_preview.py`
- Local preview: `articles/preview-the-deadlock.html`
- Conventions and publishing notes: `articles/README.md`

**Next action:** decide on length, then publish. It runs **~2,750 words** against a house
length of 1,750–2,050. All four figures are 2400×1350 and watermarked.

**Preview artifact:** <https://claude.ai/code/artifact/e5ec49e2-c74c-46fe-a74a-28fcbb941054>

---

## 4. Model serving in the Rust API — DECISION PENDING

How to run the policy/value network inside `quantik-api-rust` so the visualizer can play
it. Two candidates: **candle** (Rust-native, reads `weights.safetensors` directly) or
**ONNX** (`tract-onnx` preferred over `ort`, which is still a release candidate).

The deciding number: about 500 lines must move to Rust — encoder (~20), evaluator (78),
`BatchedMCTS` (330), architecture (97). **ONNX saves only the architecture's 97 lines.**
The search port is unavoidable either way. Recommendation is **candle, with a parity test
against PyTorch written first**.

**Correction landed 2026-08-28 (local commit `02bfcd1`, unpushed — that repo has no
remote).** `model-serving.md` specified the **colour-ordered** input encoding from
`quantik_core.ml_data.qfen_to_tensor`. Every checkpoint is trained **mover-relative** —
planes 0–3 belong to the side to move, per `fastboard.encode_tensors`, which is what
`train/supervised.py` and `eval/evaluator.py` both feed the network. A runtime built to
the old text would have swapped the players on every position with player 1 to move: no
error, correct answers on half the positions, confidently wrong on the other half. The
doc now carries the correction inline.

**Next action:** pick a runtime, then build the encoder and parity test. The parity test
should assert the encoding is mover-relative, not merely that shapes match.

**Detail:** `quantik-api-rust/docs/model-serving.md` ·
`quantik-models-py/docs/architectures.md` ·
artifact <https://claude.ai/code/artifact/f07992ce-e29a-496b-b20b-3eeab8af4229>

---

## 5. Publishing checkpoints to Hugging Face — TOOLING DONE, NOTHING PUSHED

Fifteen checkpoints exist under `quantik-models-py/runs/` and none is committed or
retrievable, because `runs/` is gitignored. The publishable payload is roughly 36 MB of
safetensors, plus ~7 MB of ONNX per `lineup-*` model.

~~Recommended layout: **one** Hub repo `mberlanda/quantik-policy-value` with a subfolder
per `model_id`.~~ **Superseded 2026-08-29 — one repo per architecture instead.**
`model-index` is per *repository*, so four models in one repo means one card claiming one
set of metrics, wrong for three of them and wrong in Hub search. Download counts and likes
are per repo too, so a monorepo cannot say which architecture anyone uses. Cost of the
split: four tags to keep in lockstep against this workspace's single-version convention —
stage and tag in one scripted pass, and group them with a Hub **collection** for the
side-by-side reading. The subfolder layout stays right for one model's shards and for a
serving path that fetches `subfolder/weights.safetensors` by route segment.

Still standing from the original research: mirror to a GitHub Release; commit only the
68 KB `smoke-best` as a CI fixture. The CLI is `hf` (huggingface_hub ≥1.29), not
`huggingface-cli`.

**Blocker:** the eleven pre-2026-08-28 manifests are stamped `contract_version: "1.1.0"`,
which `quantik-core-py` 1.2.0 rejects. The root cause is fixed (py#9 merged), so the three
`lineup-*` checkpoints trained on 2026-08-28 stamp **1.2.0** correctly and carry a
`model.onnx` alongside the safetensors — they are publishable as they stand. The older
eleven are not. Because
`quantik-core-contracts/schemas/model-checkpoint-v1.json` is **byte-identical** between the v1.1.0 and v1.2.0
tags, the cleaner fix may be teaching the validator to accept older contract releases for
checkpoints rather than re-running training.

**Update 2026-08-29 (py#39): the publish entry point exists.**
`python -m quantik_models.export.huggingface <checkpoint> <out>` stages a
Hub-ready directory — weights renamed to `model.safetensors`, the ONNX graph,
the manifest, and a generated `README.md` / `config.json` / `.gitattributes`.
The card's `model-index` numbers are read out of `shift.json` and an arena
`games.json` rather than typed. Every digest is verified against the manifest
before the directory is returned. **Nothing uploads** — staging and pushing
stay separate because a push is authenticated, public and awkward to undo.

Two findings that revise the layout recommendation above:

- **One repo per architecture** — runs collapse into one repo as revisions
  (`swept-cpool` and `lineup-cpool` are one architecture at two rates, and the
  superseded run is the evidence for the methodology fix), but architectures
  do not, because `model-index` is per repository.
- **`.gitattributes` must ship in the first commit.** The Hub's default covers
  `*.safetensors` and **not `*.onnx`**, so the ~7 MB graph lands as a plain
  git blob and stays in the history permanently. This is the one mistake here
  a follow-up commit cannot fix.

**Still blocked for the eleven older checkpoints**, whose manifests stamp
`contract_version: "1.1.0"`. The four current ones stamp 1.2.0 and stage
cleanly.

**Update 2026-08-29, second pass — the Hub account is `brpoplpush`.** Repo ids
are derived, not hand-written: `<namespace>/quantik-<architecture>`, giving
`brpoplpush/quantik-{cpool-c191-b6,attn-d192-b6,resnet-c128-b6,mlp-h455-b4}`.
Namespace comes from `--namespace`, then `$QUANTIK_HF_NAMESPACE`, then the
module default. `scripts/stage_hub_repos.sh OUT_DIR CHECKPOINT...` stages all
four in one pass, in two phases so every card can link the rest of the family.

**Branch `feat/hub-namespace` in quantik-models-py, five commits, not yet
pushed or PR'd** (an SSH key for the Hub is still to be set up; nothing about
that blocks the local work). 375 tests pass.

**Verified against the registries, not assumed** — see the
`quantik-published-packages` memory:
- `quantik-core` is live at **1.2.0 on both PyPI and crates.io**, MIT.
- **`quantik-models` is NOT on PyPI.** The card's install line points at the
  GitHub source. `https://pypi.org/project/<name>/` returns 200 with a
  Cloudflare challenge for packages that do not exist — check
  `/pypi/<name>/json` instead.
- The Hub `license:` field takes a lowercase identifier from a fixed table:
  `mit`, not `MIT`. Repo-name rules are undocumented on the Hub; the only
  authoritative constraint is `huggingface_hub`'s `REPO_ID_REGEX`.

**A licence decision that needs confirming.** `quantik-models-py` had no
LICENSE file and no `license` key, and it is the repo that produces the
checkpoints. MIT was added to match `quantik-core-py` and `quantik-core-rust`,
because the cards this repo generates publish a `license:` field and one
asserting a licence the source tree does not carry is worse than none. That is
a judgement call, not an instruction, and it is reversible until something is
published under it. `quantik-core-contracts` still has no LICENSE.

**Commit convention changed 2026-08-29:** no `Co-Authored-By` or
`Claude-Session` trailers, and no generated-with footer in PR bodies. Atomic
commits and detailed bodies stay.

**Next action:** decide whether to teach the validator to accept older
contract releases; confirm the MIT choice; set up the Hub SSH key; then push.
Nothing has been pushed to the Hub.

**Detail:** the publishing walkthrough
<https://claude.ai/code/artifact/7f644a2a-24c3-4163-831b-747b422516a6>, and
the earlier layout research
<https://claude.ai/code/artifact/4d324ac3-2358-40f3-b883-469e44028e28>

---

## 6. API response type — SPECIFIED, NOT BUILT

The response is the bottleneck, not the engines. Everything below is already computed at
the call site and thrown away:

- **Ranked candidates** — the network emits all 64 logits plus a value every forward pass;
  argmax is the caller's choice. MCTS has visit counts; the oracle scores every legal move.
- **Principal variation** — `MinimaxResult.pv` is populated on every search, and
  `search_minimax` in `quantik-api-rust/src/lib.rs` returns `Ok((result.best_move, None))`.
- **`certainty: estimate | proof`** — the cheapest and most valuable field. The network's
  `tanh` value is an estimate and never a proof; the exact oracle is certain. The same
  endpoint should never blur them.

Also: for model engines, `engine_version` should carry the `model_id` rather than the core
revision, so exported games record which network played.

**Next action:** extend the response type; no new algorithms needed.

**Detail:** artifact <https://claude.ai/code/artifact/114ce808-69ed-4394-bcaf-cad3b4523c3a>

---

## 7. Engine API contract — NOT STARTED

`quantik.engine-request.v1` and `quantik.engine-response.v1` are **phantom contracts**.
They use the contract naming convention and the API rejects requests whose schema field
does not match, but they appear nowhere in the contracts registry. They are hardcoded
independently in two repos:

- `quantik-api-rust/src/lib.rs` (Rust `const`)
- `quantik-qfen-visualizer/src/engines.js` (JS string literal)

Nothing keeps them in agreement. Two things to settle while promoting them: **naming**
(every registered contract is `observation.v1`, `qfen.v1` — no `quantik.` prefix) and
**format** (OpenAPI 3.1, which is JSON Schema 2020-12 compatible, enabling client
generation). Prefer a contract-first spec with a CI check that the generated spec matches,
over `utoipa` generating from handlers — the latter inverts the source of truth.

**Next action:** register both schemas in `quantik-core-contracts`.

---

## 8. Dockerize the API — NOT STARTED

Ship `quantik-api-rust` as a container. **GHCR over Docker Hub** as primary: Docker Hub
applies anonymous pull rate limits that bite CI; `ghcr.io` is free for public images and
tied to the repo. Multi-arch via `buildx` (`linux/amd64` + `linux/arm64`, since local dev
is arm64), multi-stage build onto a distroless or scratch base.

Keep the naming honest: the *contract* is authoritative, the container is a distribution
artifact.

**Not blocked.** This section long carried "`quantik-api-rust` has no git remote — nothing
for CI to build from". **That is false and was false when written** (corrected 2026-08-30):
the repo has `origin git@github.com:mberlanda/quantik-api-rust.git`, and local `main` is in
sync with it at `f814093`. Verified three ways — `git remote -v`, `git ls-remote origin HEAD`
matching local `HEAD`, and the public GitHub page. There is something for CI to build from.

---

## 9. NN as an opt-in add-on — NOT STARTED

Do **not** build a dynamic plugin system; two engines do not justify a plugin ABI. Two axes
instead:

- **Compile time** — a Cargo feature. `--features model` pulls in candle and `hf-hub`;
  without it the binary has no ML dependencies. Two images: `quantik-api:X.Y.Z` and
  `quantik-api:X.Y.Z-model`.
- **Runtime** — `QUANTIK_MODELS=sup-sampled-c128b6-best,...` fetches from the Hub on boot
  and registers each under its `model_id`. Verify `weights_hash` at load and refuse a
  checkpoint that fails; serving no models is a valid state.

**Next action:** depends on workstreams 4 and 5.

---

## 10. Coverage expansion — NOT STARTED, HIGH VALUE

The flagship network trained on **zero positions below ply 6** — including plies 4 and 5,
where the contest actually lives. Plies 0–6 hold **1,019,275** canonical live positions in
total, *fewer than the 3,087,356 rows already trained on*. Complete coverage of the entire
opening is a smaller corpus than the one that already exists.

The enumerations are already on disk: `quantik-models-py/runs/canonical/level01.npy`
through `level08.npy`. Only oracle labelling is missing, and solving is known feasible —
the probe already contains 1,240 solved positions at ply 4 and 1,240 at ply 5.

**Caveat, decide deliberately:** plies 4–6 *are* the held-out probe. Training on them makes
the model stronger but the 99.63% figure stops being a clean generalization test, and the
articles quoting it would need rewording. Needs a new train/test partition.

**Related:** for opening play specifically, prefer the exact opening book over the network —
the region is small enough to solve completely, and the network is least informed there.

**Detail:** `quantik-models-py/runs/coverage.md`

---

## 11. Training program — IN PROGRESS

The active thread. Requested: research-grade documentation of `resnet-c128-b6` with
layer-by-layer visibility, alternative architectures documented to the same standard, local
training runs producing **at least three models**, engine-vs-engine autoplay whose games
feed future training, and retrain / fine-tune utilities including partial layer freezing.

### Shipped — twenty-nine PRs, `main` green after each

**2026-08-28:** [py#10](https://github.com/mberlanda/quantik-models-py/pull/10)
architecture registry + ONNX ·
[py#12](https://github.com/mberlanda/quantik-models-py/pull/12) split keyed on
the canonical position · [py#13](https://github.com/mberlanda/quantik-models-py/pull/13)
unit tests actually running in CI · [py#14](https://github.com/mberlanda/quantik-models-py/pull/14)
ADR 0001 · [py#15](https://github.com/mberlanda/quantik-models-py/pull/15) MLP ·
[py#16](https://github.com/mberlanda/quantik-models-py/pull/16) ConstraintPoolNet ·
[py#17](https://github.com/mberlanda/quantik-models-py/pull/17) training preflight.

**2026-08-29:** [py#18](https://github.com/mberlanda/quantik-models-py/pull/18)
load any architecture from a checkpoint ·
[py#19](https://github.com/mberlanda/quantik-models-py/pull/19) shift evaluation ·
[py#20](https://github.com/mberlanda/quantik-models-py/pull/20) autoplay ·
[py#21](https://github.com/mberlanda/quantik-models-py/pull/21) retrain and
fine-tune with layer freezing ·
[py#22](https://github.com/mberlanda/quantik-models-py/pull/22) arena by start
depth · [py#23](https://github.com/mberlanda/quantik-models-py/pull/23) the
ResNet layer by layer · [py#24](https://github.com/mberlanda/quantik-models-py/pull/24)
the attention encoder · [py#25](https://github.com/mberlanda/quantik-models-py/pull/25)
search flattens the differences, plus the `uniform-mcts` control ·
[py#26](https://github.com/mberlanda/quantik-models-py/pull/26) occupancy
analysis and the control result ·
[py#27](https://github.com/mberlanda/quantik-models-py/pull/27) merge solved
positions into a corpus ·
[py#28](https://github.com/mberlanda/quantik-models-py/pull/28) the attention
failure is the learning rate ·
[py#29](https://github.com/mberlanda/quantik-models-py/pull/29) the learning
rate belongs to the architecture ·
[py#30](https://github.com/mberlanda/quantik-models-py/pull/30) mark margins
with their learning rate, and land the results #26 dropped ·
[py#31](https://github.com/mberlanda/quantik-models-py/pull/31) assert every
document this project points at exists ·
[py#32](https://github.com/mberlanda/quantik-models-py/pull/32) the evaluation
section is no longer planned ·
[py#33](https://github.com/mberlanda/quantik-models-py/pull/33) regenerate the
whole comparison in one command ·
[py#34](https://github.com/mberlanda/quantik-models-py/pull/34) set every
learning rate from the sweep ·
[py#35](https://github.com/mberlanda/quantik-models-py/pull/35) the swept
outcome — the constraint prior is a tie on policy ·
[py#36](https://github.com/mberlanda/quantik-models-py/pull/36) numbers
disclaimer everywhere, and a Models section in the README ·
[py#37](https://github.com/mberlanda/quantik-models-py/pull/37) benchmark
figures ·
[py#38](https://github.com/mberlanda/quantik-models-py/pull/38) stop on
convergence instead of on an inherited epoch count ·
[py#39](https://github.com/mberlanda/quantik-models-py/pull/39) stage
checkpoints as Hugging Face model repositories.

**Read first:** `quantik-models-py/docs/decisions/0001-architecture-lineup.md` —
which architectures are trained, which six were declined and why, and the
methodology. It is the umbrella document; the four papers below hang off it.

| doc | what it holds |
|---|---|
| `docs/architectures.md` | the registry, ONNX export invariants, preset tables |
| `docs/architecture-resnet.md` | layer-by-layer, the incumbent |
| `docs/architecture-mlp.md` | layer-by-layer, the control |
| `docs/architecture-constraint-pool.md` | layer-by-layer, the constraint model |
| `docs/policy-value-training-paper.md` | *why* the ResNet is trained as it is; §3.1 now points at the layer-level doc |
| `docs/shift-evaluation.md` | accuracy off the training distribution |
| `docs/autoplay.md` | the arena, and why autoplay generates positions not labels |
| `docs/retrain-and-finetune.md` | `--init-from`, `--freeze`, and two silent failures |

### The lineup, parameter-matched within 0.9%

| arch | `small` | | `medium` | |
|---|---|---|---|---|
| `resnet` | `resnet-c64-b4` | 304,711 | `resnet-c128-b6` | 1,786,823 |
| `mlp` | `mlp-h178-b4` | 305,285 | `mlp-h455-b4` | 1,788,343 |
| `cpool` | `cpool-c96-b4` | 307,333 | `cpool-c191-b6` | 1,780,253 |
| `attn` | `attn-d96-b4` | 308,485 | `attn-d192-b6` | 1,800,709 |

> ### ⚠ Read this before trusting any margin below
>
> **The shared learning rate is the ResNet's.** `2e-3` is the trainer's
> default and was chosen for the ResNet, the only architecture that existed
> when it was set. Every architecture added since has been evaluated at a
> convolutional network's preferred setting.
>
> The attention encoder exposed this by failing completely — flat at 0.5130
> for sixteen epochs at 2e-3, and climbing 0.5380 → 0.6454 → 0.7271 over
> three epochs at 3e-4. It was one commit from being recorded as a failed
> architecture on the strength of an inherited hyperparameter.
>
> ADR 0001's rule is amended to a shared **protocol** rather than a shared
> **value**: the same LR grid at the same budget for every architecture,
> best validation result entering the comparison. The rate is now a property
> of the architecture (`registry.ArchitectureEntry.default_lr`, py#29), so a
> new architecture must state its own rather than inherit the incumbent's by
> silence.
>
> **The sweep is done, and two of four architectures were trained at the wrong
> rate.** Three epochs, `--preset medium`, seed 20260828:
>
> | arch | 2e-3 | 6e-4 | 2e-4 | best |
> |---|---|---|---|---|
> | `mlp` | **0.9261** | 0.9155 | 0.8312 | 2e-3 ✓ |
> | `resnet` | **0.9300** | 0.9282 | 0.9097 | 2e-3 ✓ |
> | `cpool` | 0.9622 | **0.9781** | 0.9666 | **6e-4** ✗ |
> | `attn` | 0.5096 | **0.7938** | 0.5404 | **6e-4** ✗ |
>
> `cpool` gains 1.6 points at 6e-4, so **every published `cpool` number is a
> floor** — the 0.9851 IID top-1, the 1.63-point deep-probe lead, the halved
> value error, the occupancy analysis. The ResNet's top two differ by 0.0018,
> which is "no change", not "2e-3 confirmed".
>
> Caveats that matter: the peak sits at the *middle* of the grid, so 2e-3 is
> established as wrong without 6e-4 being established as right; three epochs
> rank but do not settle; one seed. Detail in `learning-rate-sweep.md`.
>
> **Consequence:** every number in the results table below, in
> `shift-evaluation.md` and in `autoplay.md` was measured at 2e-3. Until the
> sweep finishes, they are comparisons *at the ResNet's preferred setting*
> and the margins may need restating. See `attention-negative-result.md`.

Widths are **solved** against the ResNet, not chosen for roundness;
`tests/test_parameter_matching.py` enforces it.

### Results at swept learning rates — 2026-08-30, current

All trained `--preset medium --epochs 16`, same corpus and split, from
scratch. `cpool` and `attn` at **6e-4**; `resnet` and `mlp` at **2e-3**. Those
rates are swept, not inherited — see the warning box above.

| model | lr | IID top-1 | shift 4-6 | shift 7-12 | arena @p3 | arena @p6 | arena @p9 |
|---|---|---|---|---|---|---|---|
| `cpool-c191-b6` | 6e-4 | **0.9893** | **0.9295** | **0.9919** | **57.2%** | 51.3% | **52.2%** |
| `attn-d192-b6` | 6e-4 | 0.9879 | 0.9102 | 0.9914 | 54.2% | **54.3%** | 50.2% |
| `resnet-c128-b6` | 2e-3 | 0.9701 | 0.9126 | 0.9720 | 47.8% | 48.8% | 49.5% |
| `mlp-h455-b4` | 2e-3 | 0.9516 | 0.8843 | 0.9578 | 40.8% | 45.5% | 48.1% |

Checkpoints: `runs/train/swept-{cpool,attn}/best` and
`runs/train/lineup-{resnet,mlp}/best`. Evaluation output:
`runs/eval/swept-2026-08-30/`.

**The lineup's central question is answered, and it is a tie.** `attn` is
the *weaker form of the constraint hypothesis* — same bet as `cpool`, told
nothing about rows, columns or zones. The policy gap is 0.0014, about 1.4
standard errors, and `attn` had **not converged** while `cpool` had. So the
explicit group wiring buys little or nothing on policy accuracy. It buys
something real on the value head: 0.0315 MAE against 0.0378.

**Search exposes that value-head gap.** Under 128-simulation MCTS at ply-3
starts, `attn` is *last* among the networks (58.6%) despite being second on
raw policy — losing to `cpool` at 42.7% and the ResNet at 42.8%. Good
priors, weaker values.

### Three earlier conclusions that were artifacts of the learning rate

Recorded because the failure mode matters more than the numbers: a
hyperparameter inherited from another architecture produced a plausible,
detailed, statistically significant story about architectural behaviour.

1. **"The ResNet is the better shallow evaluator."** `cpool` went
   0.9092 -> 0.9295 and passed it. Its shallow deficit is gone.
2. **"Each network's advantage lives at a specific depth"**, with the
   ResNet owning the opening. On raw policy the ResNet is now **third at
   every depth** — though under search it is *second* at both, which is a
   separate finding rather than a contradiction.
3. **"128 simulations of search flatten every difference."** Several
   head-to-heads are now significant that previously were not.

The occupancy analysis went the same way: `cpool` losing on high-occupancy
shallow positions by 10.0 points at p=0.0006 became **-0.0260 at p=0.42**.

### A second methodological flaw — mechanism built, lineup not re-run

A shared **epoch budget** is not equal treatment either, for the same reason
a shared learning rate was not. Sixteen epochs was chosen when the ResNet
was the only architecture, and `attn` was still climbing when it ran out —
so **0.9879 is a floor for it**.

**py#38 adds the mechanism**: `--patience N` stops when the combined
validation loss has not improved for N consecutive epochs, and `--epochs`
becomes a cap. It is **off by default**, so every published run still
reproduces exactly and **every number above is still a fixed-budget number**.
Re-running the lineup under the new protocol is separate work and is not
done.

Two things the implementation had to decide, worth not rediscovering:

- **A tie does not buy more epochs.** `best/` is only rewritten on a strict
  decrease, so an epoch that merely equals the best did not produce the
  weights on disk and must not extend the run.
- **`T_max` stays the cap.** The cosine schedule is fixed before the first
  step, so a run that stops at 22 of 60 never reaches `min_lr` and is
  slightly understated against one that spent its whole budget. That argues
  for a generous patience, not for rescaling the schedule — and it means
  `--epochs 60 --patience 5` and `--epochs 22` are *different runs*. The
  recorded `epoch_cap` is what tells them apart.

### Tools built

**`scripts/evaluate_lineup.sh` regenerates every published number in one
command** — shift evaluation, the policy arena at plies 3/6/9, and the MCTS
arena at plies 3/6 with the uniform control. Agent specs are generated from
`NAME=CHECKPOINT` arguments rather than checked in, so a stale spec cannot
silently measure a superseded model, and the arena `SEED` is settable and
deliberately not a training seed.

```bash
SEED=20260830 scripts/evaluate_lineup.sh runs/eval/today \
  resnet=runs/train/lineup-resnet/best cpool=runs/train/swept-cpool/best
```


```bash
# before a long run — ~1 min/arch, projects wall-clock, runs the real code paths
python -m quantik_models.train.preflight --preset medium --epochs 16

# after — accuracy off the training distribution, 7,800 solved held-out positions
python -m quantik_models.eval.shift --checkpoint runs/train/lineup-cpool/best

# engine-vs-engine; generates positions for the solver, not labels
python -m quantik_models.arena.autoplay --agents runs/arena/lineup-agents.json \
  --games 400 --start-plies 3 --out runs/autoplay/lineup-p3

# fine-tune, holding part of the network fixed
python -m quantik_models.train.supervised --init-from <ckpt> --freeze stem,trunk

# train to convergence rather than to a count chosen for another architecture
python -m quantik_models.train.supervised --arch attn --epochs 60 --patience 5

# every network against one fixed classical opponent, three seeds
scripts/oracle_benchmark.sh runs/eval/oracle-today \
  cpool=runs/train/swept-cpool/best attn=runs/train/swept-attn/best

# pool several oracle runs; writes the gzipped, deduplicated solver queue
python -m quantik_models.arena.pack runs/eval/oracle-today/packed \
  runs/eval/oracle-today/s*-p3

# regenerate every committed figure from runs/
python -m quantik_models.report.build_figures --runs runs --out docs/figures

# stage a checkpoint for the Hub (writes files; uploads nothing)
python -m quantik_models.export.huggingface runs/train/swept-cpool/best \
  staging/quantik-cpool --shift runs/eval/swept-2026-08-30/shift.json
```

### Two self-inflicted bugs, both worth remembering

Introduced during this work rather than found in it, and both of the kind
that recurs.

**`--lr` silently became a string.** Making `lr` optional removed the runtime
value the CLI generator infers types from. That inference was a hardcoded name
list — `{"channels", "blocks"}` to `int`, everything else to `str` — so `--lr
2e-3` started arriving as `"2e-3"`. Nothing failed until AdamW compared a float
to a str, **twelve runs into a learning-rate sweep**, which is precisely the run
that cannot tolerate a broken `--lr`. Fixed by reading the annotation, and by
splitting `build_parser` out of `main` so flag types can be asserted without
running a training loop — there had been no way to test the CLI without a full
run, which is how it got past everything.

**A conclusion drawn from one epoch.** The attention encoder was written up as a
failed architecture with "learning rate ruled out", on the strength of a single
epoch where 0.5380 against 0.5031 read as "marginally better". Three epochs read
as learning. The write-up was corrected before merge, but the near-miss is the
point: a 16-epoch question was nearly settled with one epoch of evidence.

### Six defects found, five live on `main` at the time

1. **Unit tests ran but skipped.** `e2e-data-pipeline.yml` installed `[dev,arrow]`
   with no torch, so six of fourteen modules `importorskip`ed away, greenly.
2. **ONNX batch dimension was never dynamic.** `torch.export` specializes size-1
   dimensions, so tracing at batch 1 froze the graph while still advertising a
   symbolic batch. `dynamic_axes` is ignored by the dynamo exporter.
3. **`onnx_opset` was a request, not a result** — `cpool` shipped at opset 18
   stamped 17.
4. **MLP presets off by 2x**, chosen for roundness rather than solved.
5. **`load_evaluator` hardcoded the ResNet**, parsing `resnet-c{c}-b{c}` out of
   the manifest. Could not load `mlp` or `cpool` at all.
6. **Deterministic agents produce no game diversity** — 30 games from the empty
   board gave 45 distinct positions. `--start-plies` fixes it.

### Completed overnight 2026-08-29/30

- **Exact solve of 5,226 autoplay positions** at plies 3-6 — finished in 6h50m,
  all 5,226 solved. Became **118,053 labelled rows** (~22 free child labels
  each) and merged into `runs/oracle/corpus/exact-sampled-v2.npz`:
  3,196,958 rows, 255,058 policy-labelled. Ply 3: 0 -> 664. Ply 4: 0 -> 9,664.
  Ply 5: 0 -> 22,655. Ply 6: 40,000 -> 86,631.

  **The held-out guard dropped 1,554 probe positions** that arrived as
  *children* of solved parents — never sampled, labelled for free. Exactly the
  leak `merge_corpus.py` was written to prevent. Verified: v2 shares zero
  canonical keys with the probe.

  **Nothing has been trained on v2 yet.** Doing so measures a better *corpus*,
  not a better architecture, and the two must not be conflated.
- **12-run learning-rate sweep**, the `uniform-mcts` control arena, `attn` and
  `cpool` retrained at 6e-4, and a full re-evaluation into
  `runs/eval/swept-2026-08-30/`.


### Queued by the user, 2026-08-29 — status

**2 and 3 are done** (py#37, py#39). 1 is running.

1. **Autoplay against a minimax oracle** — IN PROGRESS 2026-08-29.
   **Dispatch subagents** (explicitly requested). Minimax is the *oracle* each
   network is scored against, which closes the "largest open gap" below.
   **Seeds must differ from the training seeds** (`20260827`, `20260828`,
   `20260901`) so seed-linked bias shows rather than hides; vary them across
   runs. **500-1000 games per pairing**, both seats. Record it as a benchmark
   and **store the results compressed** — they are input to the next
   retrain / fine-tune cycle, not just a report.

   **Substituted for subagents: four parallel background runs.** Each is one
   `python -m quantik_models.arena.autoplay` invocation, so a subagent per run
   would have started cold to issue the same shell command. The parallelism
   the request was for is there; the cold starts are not. Flagged rather than
   done silently.

   **Depth is measured, not assumed**: `minimax-d2` costs 0.156 s/move from a
   ply-3 start, `d3` 2.26 s, `d4` 16.4 s. d2 is the affordable oracle at 1000
   games per pairing; d4 is three orders of magnitude off the budget. Also
   found: **the fixed-clock minimax is unusable as an oracle** — iterative
   deepening cannot interrupt a level, so `minimax@10ms` spends 157 ms from a
   ply-3 start and reaches exactly the depth `-d2` does. A budget the engine
   ignores is not a budget.

   Runs: seeds 20260902/03/04 at start ply 3, plus 20260902 at ply 6, 1,000
   games per ordered pairing, into `runs/eval/oracle-2026-08-29/`.
   `scripts/oracle_benchmark.sh` is the reproducer;
   `python -m quantik_models.arena.pack` pools the runs, keeps each seed
   visible beside the pooled interval, and writes the gzipped,
   symmetry-deduplicated solver queue.

   **DONE — py#40. 32,000 games. `cpool` is even with a two-ply search.**

   Start ply 3, 24,000 games, three seeds — win rate vs `minimax-d2`:
   `cpool` **49.4%** [48.2, 50.7] indistinguishable · `attn` 43.1% loses ·
   `resnet` 36.5% loses · `mlp` 31.9% loses. At ply 6 (8,000 games) both
   `cpool` (48.9%) and `attn` (49.7%) are even; the other two lose.

   Two things beyond the headline. **The internal ranking survives contact
   with an outside opponent** — the order against minimax at ply 3 is exactly
   the order of the network-vs-network arena at ply 3, which was not
   guaranteed and is the first evidence here that the ranking is not an
   artifact of the field. And **three fresh seeds found no seed-linked
   bias**: the widest ply-3 gap is 1.5 points against intervals ~1.2 wide.

   **The seat dwarfs every model difference and grows with depth** — `cpool`
   swings 60.6%/38.2% at ply 3 and 77.2%/20.5% at ply 6. Any number that does
   not hold the seat fixed is measuring mostly this.

   Full write-up: `quantik-models-py/docs/oracle-benchmark.md`.

   **Solver queue: 17,062 positions, not 26,157.** The runs filtered against
   `exact-sampled.npz` because that is `autoplay --corpus`'s default, and
   `exact-sampled-v2.npz` had already superseded it — 9,095 of the queue was
   already labelled, about twelve hours of solver time. Fixed structurally:
   **filtering belongs at pack time**, since the arena filters when the games
   are played and the queue is spent much later. `pack --corpus` does it and
   records what it filtered against. Almost all the genuinely novel positions
   are at plies 5-6 (13,383 and 3,251); plies 3-4 are covered.
2. **Hugging Face artefacts** — DONE, py#39.
   `python -m quantik_models.export.huggingface <checkpoint> <out>` stages a
   Hub-ready directory; `docs/publishing-to-hugging-face.md` and the Artifact
   <https://claude.ai/code/artifact/7f644a2a-24c3-4163-831b-747b422516a6>
   ("Silent Failures on the Hub") cover what a repo requires, the
   version-control model and the documentation. **Nothing has been pushed to
   the Hub** — staging and pushing are deliberately separate.
3. **A benchmark across all runs, with graphs** — DONE, py#37. Six committed
   SVGs in `docs/figures/` and `docs/benchmarks.md`.
   `python -m quantik_models.report.build_figures` regenerates them from
   `runs/`; `matplotlib` is in a new `viz` extra.

### Still to build

- ~~**Export the play store to a solver queue.**~~ DONE — py#53.
  `python -m quantik_models.play.export` reads `game_positions` through
  `distinct_positions`, drops what a given corpus already has, and writes
  the same `to-solve.qfen.gz` autoplay does — no new format, no new
  consumer. Run against the live store: 66 positions at ply ≤ 6, 40 already
  in `exact-sampled-v3.npz`, 26 written; fed through `exact_oracle` and
  `merge_corpus.py` unchanged. **Human game outcomes never become labels**
  — the exporter never reads `games.winner`, only positions. See
  `docs/autoplay.md` "Human games feed the same queue". The queue itself is
  small and mostly ply 0-3, which is expensive to solve (see below) — that
  solver run is separate, future work, not part of this brief.
- **Fold the solved autoplay positions into the corpus and retrain.** The tool now
  exists — `python -m quantik_models.data.merge_corpus` (py#27) — and holds the probe
  out of the *merged* result rather than only the new rows, because solving a position
  also labels its children. `retrain-and-finetune.md` argues for warm-starting on the
  *combined* corpus rather than fine-tuning heads on the shallow set alone, which can
  trade away deep accuracy the model already has — and the shift evaluation would show
  it immediately.
- ~~**Finish the learning-rate sweep, then re-run the lineup at the chosen
  rates.**~~ DONE 2026-08-30, and it reversed three published conclusions.
  Twelve runs — four architectures x {2e-3, 6e-4, 2e-4} x 3 epochs — into
  `runs/lrsweep/`. Three epochs because the attention failure was unambiguous by
  epoch 3 and *invisible* at epoch 1, which is the lesson that produced this
  workstream. A second seed was queued and then cancelled: replicating a
  possibly-unfair configuration is the wrong thing to spend compute on.
- **A second seed, after the sweep.** Every number above is one run per
  architecture. The resnet/mlp gaps are wide enough to trust; the shallow
  resnet/cpool gap is 0.34 points on 3,600 positions and is not.
- **Train `attn` to convergence, not to sixteen epochs.** Done at its chosen
  rate (6e-4) but still on the inherited fixed budget, and it was climbing
  when the budget ran out — so 0.9879 is a floor. `--patience` exists now
  (py#38); re-running the lineup under it is the outstanding work, and until
  that happens every number in this file is a fixed-budget number.
- **Plies 0–3 are unevaluated.** The probe starts at ply 4, and the three networks
  disagree flatly about the empty board: ResNet +0.77, MLP +0.59, `cpool` −0.997. At
  most one is right. Ground truth is *not* derivable from what is on disk — only
  10,000 of the 901,916 ply-6 positions in `runs/oracle/opening/frontier.jsonl` are
  solved — so this needs its own solver run and belongs with workstream 10.
- **Attention encoder as an optional fourth.** ADR 0001 declines it with the trigger
  "if the first three land cleanly". All three have. Note the rationale is
  **content-dependent interaction**, not receptive-field range — range is not an
  argument on a 4×4 board.
- **Hypergraph and recurrent-propagation variants.** ADR 0001 promotes these from
  "written down" to "next" if ConstraintPoolNet wins clearly. It did, on the deep
  probes and the ply-6 arena.
- **Deepen `docs/policy-value-training-paper.md`** to the layer-by-layer standard the
  two new architecture papers set. It is now the shallowest of the three.
- **A minimax baseline in the arena — RUNNING 2026-08-29, the largest open
  gap until now.** Every win rate recorded before this is relative to the
  other networks or to `uniform-mcts`, which is a *floor* (its evaluator
  returns zero everywhere). Nothing said whether any of these networks beats
  the project's own engines.

  **The earlier per-move costs were badly inflated by machine contention.**
  `minimax-d2` was recorded at 1.1 s/move while the sweep and the solver were
  saturating the machine. Re-measured on a quiet one, at every start depth:

  | start ply | `minimax-d2` | `minimax-d4` |
  |---|---|---|
  | 0 | 0.025 s | 3.98 s |
  | 1 | 0.152 s | 24.3 s |
  | 2 | 0.279 s | — |
  | 3 | 0.156 s | 16.4 s |
  | 6 | 0.045 s | 0.64 s |

  So d2 never exceeds 0.28 s anywhere — the 1.1 s figure was load, not a
  shallower start. The ordering held; the scale did not, and the difference
  is between "not something to start alongside other work" and "an hour".
  The general point is worth keeping: **a timing taken under load is an upper
  bound and has to be re-taken before anything is planned around it.**

  **`beam` is still unmeasured** and stays on this list.

- **A beam-search baseline — still uncosted, and deliberately so.** `beam-w64`
  was recorded at 73 s/move under the same contention that made `minimax-d2`
  look ten times slower than it is, so that figure means very little. A
  re-timing on 2026-08-29 gave **`beam-w16` at 5.7 s/move from a ply-3 start**
  — 36x `minimax-d2`, implying roughly a day for a matching 1,000-game arena —
  **but that probe was itself taken against a 16-thread exact solver and has
  been discarded rather than recorded as fact.** Re-time it on a quiet
  machine. The harness (`--against`, `arena.pack`) exists; the only missing
  input is an honest cost.

### Reference

**Corpora** under `quantik-models-py/runs/oracle/corpus/`: `exact-sampled.npz`
(3,087,356 rows, 250,000 policy-labelled), `exact-deep.npz` (1,259,355),
`sampled.npz` (3,087,356). Coverage table: `runs/coverage.md`.

**Two incompatible encodings share the name `tensor-board.v1`.** `fastboard.encode_tensors`
is **mover-relative** and is what everything in training uses;
`quantik_core.ml_data.qfen_to_tensor` and `fastboard.to_core_tensor` are colour-ordered and
are used by nothing here. See workstream 4 — this already caused one wrong document.

**Legality masking outside the model is deliberate and standard**, not a defect. The mask
is applied in code around the network, where the rules are already exact, so no engine in
this project can return an illegal move.

---

## 13. Public play deployment — REQUESTED 2026-08-29, NOT STARTED

Ship the visualizer plus the play service as **one container with no data store**, so it
can be deployed publicly and shared. Storage is deliberately deferred: the point is to
find out whether the games are worth collecting before committing to collecting them.

**Storeless already works.** `python -m quantik_models.play --no-store` opens no database
and never creates the file; `POST /api/games` answers **503**. The server needs nothing new
for this. What does need work:

1. **The browser client tries to record anyway** and would show `Not recorded: ... 503` at
   the end of every game. It should learn from `GET /api` that there is no store and stay
   quiet — a public visitor should never see a storage error.
2. **A Dockerfile.** The image needs the weights, which are gitignored locally but
   **published on the Hub** (`brpoplpush`, CC-BY-NC-4.0) — pull them at build time rather
   than baking a copy of `runs/`. Mind the licence split: weights non-commercial, code MIT,
   and a public image has to carry both.
3. **Image size — measured 2026-08-30, and the answer is ONNX.** The earlier framing
   ("there is no ONNX evaluator in Python, only torch") made this sound like an epic. It is
   not. Measured in the local venv: **`torch` 529 MB installed, `onnxruntime` 80 MB** — a
   6.6x difference, before the CUDA-less wheel juggling a torch image needs. And the work
   to get there is bounded:

   - `onnxruntime` is **already a declared extra** (`[project.optional-dependencies].onnx`)
     and is **already executing graphs** in `train/preflight.py`, `export/huggingface.py`
     and their tests. It is not a new dependency, it is an already-trusted one.
   - `selfplay/evaluator.Evaluator` is a **one-method Protocol** —
     `(boards, legal) -> (priors, values)`. `UniformEvaluator` implements it in six lines
     with no torch at all, which is the existing proof that the seam works.
   - The exported graph signature matches that seam exactly. Verified against
     `runs/lrsweep/sweep-cpool-6e-4/best/model.onnx`: input `board ['batch', 9, 4, 4]
     float32`; outputs `policy_logits ['batch', 64]` and `value ['batch']`. So
     `OnnxEvaluator` is `NetEvaluator.__call__` with a numpy softmax substituted for the
     torch one — the masking and batching logic transfer unchanged.

   What must be built first is the **torch-vs-ONNX agreement test on a real checkpoint**,
   not the evaluator: everything the image serves is decided by that test. Workstream 4 is
   the same decision from the Rust side and this measurement carries to it.
4. GHCR over Docker Hub, for the reason in workstream 8.

**Next action:** build `OnnxEvaluator` behind an agreement test, then the Dockerfile.
The runtime question is settled above; what is *not* settled is whether the image ships
all four architectures or one.

---

## 14. Play UX for people who are not us — REQUESTED 2026-08-29, NOT STARTED

The app assumes the player knows what `cpool@128` means. For a public deployment that is
the wrong default audience, without giving up the audience that does care.

- **Skill levels, with the internals behind an "advanced" toggle.** Most visitors want
  easy / medium / hard, not a roster of twenty opponents keyed by architecture and
  simulation count. The mapping from level to opponent must come from the arena numbers
  rather than from intuition — `docs/oracle-benchmark.md` and the lineup tables say which
  opponents actually sit at which strength, and the seat effect (mover 68-88%) is large
  enough that a level assigned by feel would be wrong.
- **A collapsible "how to play".** Quantik's rule — you may not place a shape in a row,
  column or quadrant where your *opponent* already has that shape, and you win by
  completing a line of four different shapes in either colour — is not guessable from the
  board.
- Both land in `quantik-qfen-visualizer`, which mandates a failing test before any
  `src/*.js` change.

**Next action:** derive the level-to-opponent mapping from the existing arena tables and
write it down with the numbers behind it, before wiring any UI.

---

## 15. Puzzle mode in the browser — GENERATOR DONE, UI NOT STARTED

`quantik_models.play.puzzles` mines the exact corpus by theme and writes a JSON pack
(`--per-theme 40` over `exact-sampled-v3` yields 40/40/40/29/40 across `mate-in-1`,
`only-move`, `double-threat`, `endgame`, `already-lost`). Merged as py#51.

`double-threat` is the theme worth naming: after the key move every legal reply loses at
once, and the win does not always land on the same square — block one combination and you
concede the other. Verified against corpus values through a second code path.

**What is left is the browser side:** commit a generated pack into the visualizer, replace
the five hand-picked examples with a themed picker, and check the player's answer against
`solutions`. The pack is static JSON, so puzzle mode needs no play service at all — which
makes it the part of a public deployment that works even with no models loaded.

**Next action:** generate a pack, commit it to `quantik-qfen-visualizer`, build the picker.
Note that `already-lost` has no solution on purpose: it is a study, not a puzzle.

---

## 12. Repo hygiene — OPEN

- ~~**`quantik-api-rust` has no git remote.**~~ **Wrong, corrected 2026-08-30.** It has
  `origin git@github.com:mberlanda/quantik-api-rust.git` and local `main` is in sync at
  `f814093`. Verified by `git remote -v`, `git ls-remote origin HEAD` matching local `HEAD`,
  and the public GitHub page. Workstream 8 is **not** blocked and workstream 4 is not at
  risk for this reason. The claim had propagated into the root `CLAUDE.md` repo table and
  into workstream 8; both are fixed. Kept visible rather than deleted because it was
  repeated as fact for weeks and shaped a delegation plan.
- **`articles` has no git remote.** This half held up — verified 2026-08-30, no remotes
  configured. Three finished Season Two drafts live only on this machine.
- **`quantik-models-py` local `main` is in sync with `origin/main`** as of 2026-08-28,
  after seven merges. Resolved.
- **py#9 merged** — the smoke-checkpoint fixture and the `contract_version` fix. New
  checkpoints stamp 1.2.0; see workstream 5 for the eleven older ones.
- **`e2e-data-pipeline.yml` still checks out `quantik-core-py` with no `ref:`**, so it
  tracks that repo's `main` and inherits breakage silently. Still open. The new `tests.yml`
  deliberately does the opposite — it installs the *published* `quantik-core>=1.2` from
  PyPI, so unit-test green does not depend on another repo's in-flight work. Pin the e2e
  ref, or give it the same treatment.
- `.oracle-worktree/` sits at the workspace root; check whether it is still needed.
