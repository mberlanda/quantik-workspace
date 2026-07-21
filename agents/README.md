# Agent Operating Prompts

These prompts are independent of model vendor, agent host, command runner, and
collaboration transport. A role may be performed by one process or delegated to
a collaborator with the required capability.

Apply prompts in this order:

1. `operating-contract.md` for shared authority, safety, evidence, and handoff
   rules;
2. `initiative-planner.md` when a task is marked `plan-required`;
3. exactly one repository/review role for implementation or verification;
4. the task packet and bounded context generated for that role.

The historical `quantik-ai` prompts were reviewed as source material. Their
explicit role/input/output/quality-gate structure is retained. Their fixed
six-agent graph, Python-only architecture, provider libraries, Redis/SQLAlchemy
runtime, speculative scale targets, and generated demo workflow are not current
requirements and are not copied here.
