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

ARGS ?=

ARTIFACT := {{ cookiecutter.artifact }}
{%- if cookiecutter.__packaging == 'debian' %}
MODULE := {{ cookiecutter.__module }}

ARCH ?= {{ cookiecutter.__arch }}
CODENAME := {{ cookiecutter.__codename }}
IMAGE = $(ARTIFACT)-deb:$(CODENAME)-$(ARCH)
CONTAINER_HOME = $(HOME)/.cache/$(ARTIFACT)-deb/$(CODENAME)-$(ARCH)

DEBFULLNAME ?= $(shell git config user.name)
DEBEMAIL ?= $(shell git config user.email)

DOCKER_RUN = docker run --rm --interactive \
	$$(test -t 0 && echo --tty) \
	--platform linux/$(ARCH) \
	--env UV_PROJECT_ENVIRONMENT=/home/ubuntu/venv \
	--env DEBFULLNAME="$(DEBFULLNAME)" \
	--env DEBEMAIL="$(DEBEMAIL)" \
	--volume "$(CONTAINER_HOME):/home/ubuntu" \
	--volume "$$PWD:/home/ubuntu/app" \
	$(IMAGE)
{%- endif %}

# ---------------------------------------- HELP ----------------------------------------

.PHONY: help
help: ## Display this help
	@sed -rn 's/^([a-zA-Z0-9_%-]+):.*?## (.*)$$/"\1" "\2"/p' \
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
	uv run pytest -s -v --cov --cov-report=term-missing --cov-fail-under=60 \
		--junit-xml=junit.xml --cov-report=xml:coverage.xml

.PHONY: run
run: install-deps  ## Run the application
	uv run $(ARTIFACT) ${ARGS}

.PHONY: git-clean
git-clean: ## Clean the project using git clean
	git clean -Xdf

# --------------------------------------- BUILD ----------------------------------------

{%- if cookiecutter.__packaging == 'python' %}

.PHONY: build
build: install-deps lint test  ## Build source distribution and wheel
	uv build
{%- elif cookiecutter.__packaging == 'debian' %}

.PHONY: image
image: ## Build the image
	docker build . \
		--platform linux/$(ARCH) \
		--build-arg CODENAME=$(CODENAME) \
		--build-arg USER_UID=$$(id -u) \
		--build-arg USER_GID=$$(id -g) \
		--file packaging/deb.Dockerfile \
		--tag $(IMAGE)

.PHONY: shell
shell: image  ## Open a shell in the image
	mkdir -p "$(CONTAINER_HOME)"
	$(DOCKER_RUN) bash

.PHONY: pyinstaller
pyinstaller: install-deps lint test  ## Create a binary executable using pyinstaller
	uv run pyinstaller \
		--onefile \
		--clean \
		--noconfirm \
		--name $(ARTIFACT) \
		--copy-metadata $(ARTIFACT) \
		--distpath pkg \
		src/$(MODULE)/cli.py

.PHONY: pkg
pkg: pyinstaller  ## Build the Debian package
	debuild --no-lintian -us -uc -b
	debuild -- clean
	mkdir -p dist
	mv ../$(ARTIFACT)_*.deb dist/
	rm -f ../$(ARTIFACT)_*.{build,buildinfo,changes}
	cd dist && for deb in *.deb; do sha256sum "$$deb" > "$$deb.sha256"; done

.PHONY: build
build: image  ## Build the Debian package in the image
	mkdir -p "$(CONTAINER_HOME)"
	$(DOCKER_RUN) make pkg
{%- endif %}
