# Local Setup

Default layout places this repository beside the four implementation repositories. Copy path-only overrides into ignored `workspace.local.yaml` if needed. Run `./scripts/bootstrap`, then `./scripts/status` and `./scripts/validate`.

Bootstrap installs an offline workspace-local path hook and console entry point; the runtime has no third-party dependencies. It does not overwrite repository paths or require GitHub authentication. Cloning missing public repositories and fetching updates require explicit `--execute` through the CLI.
