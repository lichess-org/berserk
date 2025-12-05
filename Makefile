.PHONY: help clean clean-docs clean-test setup test format format-check docs servedocs build publish
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

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-docs clean-test ## remove test cache and built docs

clean-docs: ## remove build artifacts
	rm -fr _build

clean-test: ## remove test and coverage artifacts
	rm -fr .pytest_cache

setup: ## setup uv env and install dependencies
	uv sync --locked

setup-ci: ## for Docker, install the deps only. need to run `setup` after
	uv sync --locked --no-install-project

test: ## run tests with pytest
	uv run pytest tests

test_record: ## run tests with pytest and record http requests
	uv run pytest --record-mode=once tests

test_live_api: ## run tests with live API (no cassettes)
	uv run pytest --disable-recording --throttle-time=1.0 tests

typecheck: ## run type checking with pyright
	uv run pyright berserk integration/local.py $(ARGS)

format: ## format python files with ruff
	uv run ruff format $(ARGS)

format-check: ## check formatting with ruff (for CI)
	uv run ruff format . --diff

docs: ## generate Sphinx HTML documentation, including API docs
	uv run sphinx-build -b html docs _build -EW --keep-going

servedocs: docs ## compile the docs and serve them locally
	python3 -m http.server --directory _build --bind 127.0.0.1

build: ## build the package
	uv build

publish: build ## publish to pypi
	@echo
	@echo "Release checklist:"
	@echo " - Did you update the documentation? (including adding new endpoints to the README?)"
	@echo " - Did you update the changelog? (remember to thank contributors)"
	@echo " - Did you check that tests, docs, and type checking pass?"
	@echo " - Did you bump the version?"
	@echo " - Did you tag the commit? (can also be done afterwards)"
	@echo
	@read -p "Are you sure you want to create a release? [y/N] " ans && [ $${ans:-N} = y ]
	sleep 5
	uv publish
