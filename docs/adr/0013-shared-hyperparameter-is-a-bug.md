# ADR 0013: A Shared Hyperparameter Is a Bug, Not a Control

## Context
A learning rate chosen for the ResNet was inherited unchanged by three later
architectures and used to compare them. A subsequent sweep found the rate suited none
equally and reversed three published, statistically significant conclusions about
architectural behaviour.

## Decision
A hyperparameter that plausibly interacts with architecture (learning rate, epoch
budget) is not held to one shared *value* across a comparison. What is shared is the
*protocol*: same search grid, same compute budget, best result from that grid enters the
comparison. `--patience N` exists for the epoch case but is off by default, so every
currently published lineup number is still a fixed-16-epoch number chosen when the
ResNet was the only architecture — a known, only-partly-fixed instance of this same flaw.

## Alternatives
Keep one shared value per hyperparameter for simplicity — rejected; it already produced
three false conclusions here. Sweep every hyperparameter jointly across every
architecture every time — rejected as disproportionate; the rule targets hyperparameters
with a plausible architecture interaction, not every knob.

## Consequences
An architecture comparison must state whether each such hyperparameter was swept per
architecture or is genuinely architecture-neutral. Re-running the lineup under
`--patience` remains outstanding.
