.PHONY: help clean clean-docs clean-test setup test format docs servedocs
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python3 -c "$$BROWSER_PYSCRIPT"

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-docs clean-test ## remove test cache and built docs

clean-docs: ## remove build artifacts
	rm -fr _build

clean-test: ## remove test and coverage artifacts
	rm -fr .pytest_cache

setup: ## setup poetry env and install dependencies
	poetry install --with devs

test: ## run tests
	poetry run pytest

format: ## format python files with black
	poetry run black .

docs: ## generate Sphinx HTML documentation, including API docs
	poetry run sphinx-build -b html docs _build -EW --keep-going

servedocs: docs ## compile the docs and open them in a browser
	python3 -m http.server --directory _build --bind 127.0.0.1
