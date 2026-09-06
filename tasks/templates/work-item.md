# <ID> — <one independently reviewable outcome>

Repository: `<repository>`
Branch: `<branch>` (one PR)

## Objective

Describe the trigger and resulting behavior. Resolve implementation choices before
local-agent dispatch. Keep unrelated milestones in separate packets.

## Implementation and scope

Name the changes within the manifest `allowed_paths`. Record explicit decision
references (`decisions.md#D1`) and canonical invariant heading references in the
manifest. List prerequisite work-item IDs in `depends_on`.

## Completion criteria and verification

State observable acceptance checks and exact repository commands. Include any
manual verification the automated tests cannot provide.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual
commands/results, and remaining blockers in an item-specific handoff.
