# W8 — Make the portability adapter runnable as the workspace declares it

**Repository:** `quantik-core-py` · **Branch:** `fix/portability-report-defaults` · one PR
**Dispatch:** mechanical.

`quantik-workspace compatibility smoke --execute` cannot run. Measured 2026-09-07:

```
command failed (2): .venv/bin/python -m quantik_core.api_portability_report
usage: api_portability_report.py [-h] --contracts-root CONTRACTS_ROOT --output OUTPUT
api_portability_report.py: error: the following arguments are required:
  --contracts-root, --output
```

The workspace declares the adapter command without arguments and passes it through verbatim, so
**no cross-stack compatibility evidence has ever been produced.** That is why the compatibility
matrix withholds `supported` at every release, including the current one.

Fix it on this side rather than by hardcoding paths into the workspace manifest: the adapter knows
its own sensible defaults, the manifest does not.

## Steps

1. `--contracts-root` defaults to the sibling checkout (`../quantik-core-contracts` relative to
   the repository root) when omitted. If that path does not exist, fail with a message naming the
   path it tried and the flag to override it.
2. `--output` defaults to **stdout** when omitted. The workspace runner captures stdout and parses
   it as JSON, so writing the report there makes the declared command work as-is.
3. Both flags keep working exactly as they do now when passed explicitly. This is an additive
   change; no existing caller may break.
4. Test both defaults and both explicit forms.

## Completion criteria

```sh
python -m pytest -q
.venv/bin/python -m quantik_core.api_portability_report      # must now succeed
```

- The bare invocation exits 0 and prints valid JSON to stdout.
- Explicit `--contracts-root`/`--output` behave unchanged.
- The missing-sibling error names the attempted path.

## Handoff

Paste the bare invocation's real output, and confirm it parses as JSON.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
