# QW-030 Decisions

## Recorded, not open

### D1

**The app is vendored into `quantik-models` as package data.** Chosen over the
   two alternatives below because it produces one PyPI package, one release
   cadence, one port, and leaves `quantik-qfen-visualizer` exactly as it is —
   dependency-free, `file://`-openable, with its own CI. The cost is a one-way
   sync step and a vendored tree in the Python repo, mitigated by
   `app/SOURCE.json` and an asset-integrity test.

   - **Rejected: a second PyPI package in the visualizer repo** (`quantik-play`,
     depending on `quantik-models[serve,hub]`). It matches the phrase "visualizer
     with quantik-models as a dependency" most literally, and it is the cleaner
     layering on paper. Rejected because it puts Python packaging, a release
     cadence and a version-compatibility matrix into a repository whose entire
     value proposition is having no build system, to buy a boundary that the sync
     script already enforces one-way.
   - **Rejected: merging the two repositories.** Truly monolithic, no sync at all.
     Rejected because the visualizer's independent identity — it speaks the engine
     contract to *any* HTTP endpoint, including `quantik-api-rust` — is a real
     property, and `workspace.yaml` already records that edge. Merging it into the
     Python package would make the Rust gateway a second-class consumer of a repo
     it does not depend on.

### D2

**The vendored copy is a byte copy, not a build product.** If the app ever
   needs a build step, that is a new decision requiring its own record — not
   something to introduce inside the sync script.

### D3

**The sync is release-time, not per-PR.** The vendored app lags the visualizer's
   `main` between M1 and M5 by design. Syncing on every visualizer PR would make
   every UI change a two-repository change and would put the Python repo's CI on
   the critical path of a CSS tweak.

### D4

**No skill-level ladder ships here.** Carried forward from QW-010 decision 4
   unchanged: a published ladder is hard to change once players have opinions
   about it, no arena on disk starts before ply 3, and at ply 0 every checkpoint is
   uniform to three decimal places (max legal prior 0.016–0.023) — so the phase a
   human game actually begins in is unmeasured for every model in the family.
   QW-024 is `ready-to-run` and is one arena run, not a research programme.

   This is the constraint most likely to be violated by a well-meaning
   implementer, because "easy / medium / hard" is the obvious thing to build and
   the numbers to fake it with are sitting in `docs/oracle-benchmark.md`. The UI
   prepares the slot. The data lands after QW-024.

### D5

**`--static` is preserved as an override.** It stops being the mechanism the
   default depends on, and becomes the mechanism for developing the visualizer
   against a live checkout.

### D6

**An absent `recording` field means recording is on.** A server that predates
   M2 does have a store. Failing closed here would silently stop recording games
   against every already-deployed service.

## Open

### O1

**Does the mode chooser persist across visits, or reset to the prompt?**
   Persisting is friendlier for a returning player and hides the mode concept from
   someone who used the app once and came back to something different. Not
   load-bearing; pick one and write down which.

### O2

**What does the app show when the roster is classical-only** — a service with
   `[serve]` and no staged models? "Play a model" is a mode with nothing behind
   it. Options: hide the mode, show it disabled with a reason, or offer the
   classical engines under it. Needs a decision before V2 ships.

### O3

**Does the public deployment ship `best` or `full`?** Carried from QW-009
   criterion 4 — still a product call, not a technical one, and unchanged by this
   initiative. The M4 size measurement is an input to it, not the answer.
