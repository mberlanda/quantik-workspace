PYTHON ?= python3
export PYTHONPATH := $(CURDIR)/src

.PHONY: format-check lint test validate smoke reports

format-check:
	$(PYTHON) -m compileall -q src tests

lint:
	$(PYTHON) -m compileall -q src tests

test:
	$(PYTHON) -m unittest discover -s tests -v

validate:
	$(PYTHON) -m quantik_workspace.cli validate all

smoke:
	$(PYTHON) -m quantik_workspace.cli repos status --json >/dev/null
	$(PYTHON) -m quantik_workspace.cli context repo quantik-core-contracts --budget 12000 >/dev/null
	$(PYTHON) -m quantik_workspace.cli release drift --json >/dev/null

reports:
	$(PYTHON) -m quantik_workspace.cli reports generate
