# Model Routing

## The heuristic

Route by **how much judgment remains after the spec is written**, not by how big the
task looks. A task's size is independent of whether it needs a strong model; the
variable that decides is whether the spec already resolved the ambiguity, or left it for
whoever implements to resolve while working.

- **Strong-model task**: the spec cannot be written without judgment calls that change
  the answer — weighing confounds, naming rejected alternatives, deciding what counts as
  evidence. Route this to the coordinating tier (here: `opus`/`fable`) as consultant and
  coordinator.
- **Weak-model task**: the spec already resolved every judgment call; what remains is
  mechanical — follow the steps, make the test pass, report the diff. Route this to the
  delegate tier (`sonnet`/`haiku`).
- **Review stays with the coordinating tier regardless of who implemented**, because
  reviewing is itself a judgment task: did the diff actually resolve what the spec
  required, and did it introduce a new judgment call nobody noticed.

Task size is a poor proxy for this and reliably misleads in both directions — a small
task can hide a live confound; a large task can be large only in lines touched, with
every decision already made.

## Examples from this project

**Small task, strong model required — the skill-level mapping (workstream 14).**
Mapping arena opponents to "easy / medium / hard" for a public UI looks like a one-line
lookup table, small enough to hand to a delegate model with "assign levels by feel." But
the arena numbers carry a confound a delegate has no way to know to check for: the seat
effect alone swings win rate 68–88%, dwarfing the differences between opponents. A
mapping built without holding the seat fixed would rank opponents by an artifact of who
moved first, not by strength. Deriving the mapping is small in output and large in
judgment — it requires knowing the seat-effect finding exists and applying it, which is
exactly the context a spec cannot pre-resolve, because writing that context down *is*
the task.

**Larger task, weak model sufficient — a mandated-failing-test UI change
(`quantik-qfen-visualizer`).** "Add a collapsible how-to-play panel; TDD is mandatory,
write the failing test first" fully specifies the judgment: what test passes, what
changes, what the acceptance criterion is. Implementing it is mechanical regardless of
how many lines of `src/*.js` it touches. This is `sonnet`/`haiku` work, with
`opus`/`fable` review on the resulting diff.

**A negative example, recorded because it was caught rather than avoided — the shared
learning rate.** A learning-rate value chosen for one architecture (the ResNet) was
inherited by three later architectures without re-deriving it per architecture. That is
a routing failure of the same shape even with no agent involved: a value carrying an
implicit judgment call ("this rate suits this architecture") was propagated as if it
were a fixed input, and it produced three plausible, detailed, statistically significant,
**false** conclusions about architectural behaviour before a sweep caught it. The fix
generalizes the routing rule: make the *protocol* shared (same grid, same budget, best
result enters the comparison) and re-derive the *value* every time judgment is actually
required. A shared epoch budget has the identical shape and is still only partly fixed.

## What this is not

Not a claim that the delegate tier cannot be trusted with judgment, or that the
coordinating tier must touch every line. It is a claim that the spec is the boundary:
resolve every judgment call before delegating, or keep the task at the tier that can
supply the missing judgment while doing the work.
