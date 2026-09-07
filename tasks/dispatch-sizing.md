# Dispatch Sizing

How a work item is sized so that it can be handed to a fresh agent session — including a small
model in a 64k context window — and finished without the agent having to guess.

The menu of what is currently pickable is
[`../docs/generated/dispatch-board.md`](../docs/generated/dispatch-board.md), generated from the
manifests. This file is the standard those rows are held to.

## The two fields

Every work item carries `complexity` and `dispatch` in `manifest.yaml`. Together they answer
"which agent gets this?" — which the initiative-level rating alone could not, because a single
initiative routinely contains one item that needs a careful reviewer and five that do not.

| `dispatch` | Meaning | Who runs it |
|---|---|---|
| `mechanical` | Every decision is already made, in the packet or in `decisions.md`. The work is typing, not choosing. | A small model is enough. |
| `execute-and-record` | Run a specified thing, check a specified guard, report the real output. No interpretation. | A small model, if it is disciplined about pasting real output rather than describing it. |
| `judgment` | A real call to make: a design, a partition, a verdict on evidence. | A capable model, with human review before dependents start. |

`complexity` (`S`/`M`/`L`/`XL`) uses the same scale as
[`complexity-assessment.md`](complexity-assessment.md), applied to the item rather than the
initiative.

## The rule that makes the rest work

**An initiative's open decisions become their own `judgment` work item, and everything else
depends on it.**

This is the whole trick. An initiative with an unresolved design question cannot be split into
small mechanical tasks, because every one of them would have to re-derive the same answer and they
would disagree. Resolve the decision once, write it into `decisions.md` under its own heading, and
the remaining items collapse into narrow mechanical changes that reference it.

QW-019 is the worked example: it carried two open questions (schema format, and whether to keep
the `quantik.` prefix). Settled as `decisions.md#D2` and `#D3`, its five items became a schema
registration and four single-file renames.

## Checklist for a dispatchable item

1. **One repository, one branch, one PR.** No item spans repositories.
2. **`allowed_paths` names real files**, and few of them. If it needs a glob to be plausible, it
   is probably two items.
3. **No open decision.** Every choice is either in the packet or referenced through
   `decisions` / `invariants`. If the agent would have to choose, it is a `judgment` item.
4. **Completion criteria are commands, with expected outcomes.** Not "tests pass" — the command,
   and what its output must show.
5. **The packet names what to read first**, with file paths and line numbers where they are known,
   so the agent does not have to search for the specification.
6. **A falsifiable check.** The best packets say "revert this line, watch the test fail, restore
   it". A test nobody has seen fail is not yet evidence.
7. **Say what is out of scope**, especially where the obvious next edit belongs to another item.

## Verify before dispatching

The context bundle is the actual constraint, so measure it rather than assuming:

```sh
quantik-workspace context task QW-019 quantik-core-contracts --work-item W1 \
  --budget 64000 --output /tmp/W1.md
wc -c /tmp/W1.md
```

The bundle carries the operating contract, the repository summary, the packet, the selected
decisions and invariants, the allowed paths, the target branch, and live git state — and nothing
else. Items written to this standard land around 10-15 KB, comfortably inside 64k tokens. If one
does not fit, that is a sign the item is too big, not that the budget is too small.

## What is deliberately not sized this way

Work whose deliverable is a judgement about evidence — "is there a strength ordering at ply 0?",
"does this partition destroy the probe?" — is marked `judgment` and stays that way. Splitting it
finer does not make it safer; it just hides the decision in more places.
