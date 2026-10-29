#
# vim:ft=make
# Makefile
#

.DEFAULT_GOAL := help
.ONESHELL:
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# ---------------------------------------- HELP ----------------------------------------

.PHONY: help
help: ## Display this help
	@sed -rn 's/^([a-zA-Z_%-]+):.*?## (.*)$$/"\1" "\2"/p' \
		< $(firstword $(MAKEFILE_LIST)) | \
		xargs printf "make %-27s# %s\n"

# ------------------------------------ DEVELOPMENT -------------------------------------

.PHONY: install-deps
install-deps: ## Install dependencies
	uv sync

.PHONY: show-deps
show-deps: install-deps  ## Show dependencies
	uv pip list

.PHONY: lint
lint: install-deps  ## Run all code linters and formatters
	uv run pre-commit run --all-files

.PHONY: lint-fast
lint-fast: install-deps  ## Run all code linters and formatters on staged files
	uv run pre-commit run

.PHONY: lint-%
lint-%: install-deps  ## Run linter xyz using the lint-xyz target
	uv run pre-commit run --all-files --hook-stage manual $(subst lint-,,$@)

.PHONY: install-pre-commit-hook
install-pre-commit-hook: ## Install hook for pre-commit
	uv run pre-commit install

.PHONY: uninstall-pre-commit-hook
uninstall-pre-commit-hook: ## Uninstall pre-commit hook
	uv run pre-commit uninstall

.PHONY: test
test: install-deps  ## Run pytest with coverage
	uv run pytest -s -v --cov --cov-report=term-missing \
		--junit-xml=junit.xml --cov-report=xml:coverage.xml

.PHONY: git-clean
git-clean: ## Clean the project using git clean
	git clean -Xdf