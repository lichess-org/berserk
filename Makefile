.PHONY: help clean clean-docs clean-test setup test format docs servedocs publish
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

setup: ## setup poetry env and install dependencies
	poetry install --with dev

test: ## run tests
	poetry run pytest

format: ## format python files with black and docformatter
	poetry run black berserk tests
	poetry run docformatter --in-place --black berserk/*.py

docs: ## generate Sphinx HTML documentation, including API docs
	poetry run sphinx-build -b html docs _build -EW --keep-going

servedocs: docs ## compile the docs and serve them locally
	python3 -m http.server --directory _build --bind 127.0.0.1

publish: ## publish to pypi
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
	poetry publish --build
