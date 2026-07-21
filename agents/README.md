# Agent Operating Prompts

Each role consumes bounded workspace context and one scoped task. Shared rules: inspect dirty state first; change only explicitly authorized repositories; never push/tag/publish/open PRs without separate authority; do not hide semantic differences; use repository-owned commands; report full commits, diffs, tests, artifacts, assumptions, and unperformed actions using `tasks/templates/completion-report.md`.
