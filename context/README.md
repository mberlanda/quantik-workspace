# Bounded Context

> **Purpose:** How a session loads the minimum it needs to act correctly, and where each
> fact lives so it is stated once.
> **Start with:** [`system/repository-map.md`](system/repository-map.md) · then the one
> repository packet you need · then one task.

## Bundles are composed by code, not by links

This is the part worth understanding before adding anything here. `quantik-workspace
context …` does not follow links — `src/quantik_workspace/context.py` names the exact
files each bundle contains:

| command | composes |
|---|---|
| `context repo <name>` | `system/repository-map.md` + `system/canonical-invariants.md` + `repositories/<name>.md` |
| `context initiative <QW-ID>` | `system/canonical-invariants.md` + the initiative's `initiative.md`, `manifest.yaml`, `decisions.md`, `status.md` |
| `context task <QW-ID> <repo>` | the above **plus** `repositories/<repo>.md` and the initiative's `repos/<repo>.md` |
| `context release <ID>` | `system/release-model.md` + the release's `release.yaml`, `checklist.md`, `status.md` |

Two consequences that govern how these files are written:

1. **`canonical-invariants.md` and `repository-map.md` are paid for on every request.**
   Keep them short and high-signal. Detail belongs in the repository packet.
2. **A file no command composes is unreachable through the CLI.**
   `current-architecture.md` and `domain-glossary.md` are currently in that position —
   they are linked from the two hot files so a session at least learns they exist, and
   are read on demand. Adding a document here does not make it load; changing what loads
   means changing `context.py`, which is a deliberate control-plane change.

The budget is `len(text) / 4` against `workspace.context_budget_tokens` (12,000, so about
48,000 characters). **Generation fails rather than truncating** — an over-budget bundle is
a signal to narrow the request or shorten a document, never to raise the ceiling by
reflex. See [ADR 0006](../docs/adr/0006-bounded-ai-context.md).

## The layers

| layer | holds | lives in |
|---|---|---|
| system | what is true across every repo | [`system/`](system/) |
| repository | what one repo owns, its toolchain, its CI, its current state | [`repositories/`](repositories/) |
| initiative / task | one unit of work and its per-repo packet | [`../tasks/`](../tasks/) |
| release | one release train and its evidence | [`../releases/`](../releases/) |
| decisions | why the shape is what it is | [`../docs/adr/`](../docs/adr/) · [`decisions/`](decisions/) |

## The rule that keeps this accurate

**Every fact is stated in exactly one file; everywhere else links to it.** The drift this
structure exists to prevent came from the opposite habit — the same claim restated in a
root `CLAUDE.md`, a [`WORKSTREAMS.md`](../docs/history/workstreams-archive.md) and a repo doc, then corrected in one of them. On
2026-08-30 that produced a false blocker (`quantik-api-rust` "has no git remote"; it has
one, in sync) that had shaped a delegation plan for weeks.

So: date every measured number and name where it was measured; prefer omitting a number
to copying an unverifiable one; and when a reading is superseded, keep it beside the
correction rather than deleting it — the superseded run is usually the evidence for the
fix.
