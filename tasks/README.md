# Task Packets

Cross-repository initiatives live in `active/`, `completed/`, or `archived/`. Each initiative decomposes intent into atomic work items: one packet, one branch, and one PR per item. Create packets only for outstanding implementation work; completed behavior belongs in discovery, evidence, and implementation reports rather than illustrative tasks.

Each initiative's manifest carries an optional `complexity` (`S`/`M`/`L`/`XL`) and
`complexity_notes` field — an engineering-complexity rating used as a proxy for agent
assignment; see [`complexity-assessment.md`](complexity-assessment.md) for the scale.
[`docs/generated/task-dependency-graph.md`](../docs/generated/task-dependency-graph.md) is
a Mermaid graph plus adjacency table of every initiative's `dependencies`, complexity, and
done/blocked/ready state, generated from the manifests by `quantik-workspace reports
generate` and checked for staleness by `quantik-workspace validate generated` — read it (or
`task-dependency-graph.json`) rather than re-deriving the graph by hand.

Use `status: plan-required` when the verified problem exists but a design or
implementation plan is missing. Such a packet is pickable only for plan
generation and review. Change it to `planned` after the approved plan revision
is recorded; implementation may then begin.

Validate with `quantik-workspace task validate`.

## Atomic format and dispatch

`manifest.yaml` owns `work_items`. Each entry declares a unique `id`, affected
`repository`, `packet` under `repos/<repository>/`, a branch unique within that
repository, and non-empty repository-relative `allowed_paths` (glob patterns).
`depends_on` lists work-item IDs within the initiative; the coordinator verifies
merged handoffs before dispatch. Allowed paths are instructions, not an OS sandbox.

`decisions` contains explicit `decisions.md#Heading` references; `invariants`
contains `context/system/canonical-invariants.md#Heading` references. Headings
must match exactly and uniquely. Only those sections enter execution context.
Empty lists include no decisions/invariants; the coordinator must select what
is relevant. Scope, acceptance checks, and required commands belong in the packet.

```sh
quantik-workspace context task QW-030 quantik-models-py --work-item M1 --budget 6000 --output /tmp/M1.md
```

Pass that bundle to the local agent. It includes the operating contract,
repository summary, selected packet/references, allowed paths, target branch,
dependency IDs, and current branch/revision/dirty state. It excludes planning
documents and sibling work items. It does not launch an agent or create a PR.
Do not append initiative-wide files or extra role bundles to this execution input.
Repository-owned instructions still apply when working in the checkout.

`task create` scaffolds one `plan-required` work item per repository. Replace
placeholder allowed paths, refine the objective and checks, select references,
and split further wherever another branch/PR is needed. Set the initiative and
item to `planned` only after planning review. Execution generation rejects
`plan-required` items. Existing legacy initiatives remain valid until migrated.

`quantik-workspace task migrate QW-NNN` converts a legacy `repos/<repo>.md`
initiative in place: one `plan-required` work item per affected repository,
its packet's Objective carrying that repository's existing text verbatim,
`allowed_paths` left as the same `REPLACE_WITH_EXPLICIT_PATHS` placeholder
`task create` writes. It invents nothing — no paths, decisions, or invariants
— so a migrated item still needs the same planning pass described above
before dispatch. The initiative-level `status` is left untouched; only the
work items it generates carry `plan-required`.

Track each item's status in its manifest entry; record handoffs with the item ID,
branch, PR URL, exact revisions, checks and results. QW-030 is the migrated example.

`task status` reports active initiatives with each item’s tracked status, repository,
branch, packet, and dependencies. It does not infer merged state from Git.
