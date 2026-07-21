# Task Packets

Cross-repository initiatives live in `active/`, `completed/`, or `archived/`. Each initiative decomposes intent into repository-scoped tasks, so an implementer needs only stable system context, one repository packet, the initiative decision record, and its repository task. Create packets only for outstanding implementation work; completed behavior belongs in discovery, evidence, and implementation reports rather than illustrative tasks.

Use `status: plan-required` when the verified problem exists but a design or
implementation plan is missing. Such a packet is pickable only for plan
generation and review. Change it to `planned` after the approved plan revision
is recorded; implementation may then begin.

Validate with `quantik-workspace task validate`.
