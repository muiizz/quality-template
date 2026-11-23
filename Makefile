# One set of gates. CI calls `make check` and nothing else.
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

UV   := uv run --frozen
PYD  := cd python &&
NPMD := npm --prefix ts
GITLEAKS := $(CURDIR)/.tools/gitleaks

.PHONY: setup check check-core precommit lint-py format-py mypy eslint prettier tsc sqlfluff \
        secrets test test-py test-ts mutate prove-gates demo eval-smoke update-gates

setup:  ## Install everything from the lockfiles. Safe to run again.
	$(PYD) uv sync --frozen
	$(NPMD) ci
	scripts/install-gitleaks.sh
	@if [ -d .git ]; then $(PYD) $(UV) pre-commit install --config ../.pre-commit-config.yaml; fi

check: check-core prove-gates  ## Every gate, then the proof that each gate blocks a fault.

check-core: precommit test mutate

precommit:
	@echo "==> gate: pre-commit hooks"
	$(PYD) $(UV) pre-commit run --all-files --config ../.pre-commit-config.yaml

# Targets below are the hook bodies. Hooks call these, so the versions live in the lockfiles.
lint-py:
	$(PYD) $(UV) ruff check .
format-py:
	$(PYD) $(UV) ruff format --check .
mypy:
	$(PYD) $(UV) mypy
eslint:
	$(NPMD) run --silent lint
prettier:
	$(NPMD) run --silent format:check
tsc:
	$(NPMD) run --silent typecheck
sqlfluff:
	$(PYD) $(UV) sqlfluff lint ../sql --config ../.sqlfluff
secrets:
	scripts/install-gitleaks.sh
	$(GITLEAKS) dir . --config .gitleaks.toml --no-banner --redact
	@if git rev-parse --verify HEAD >/dev/null 2>&1; then \
	  $(GITLEAKS) git . --config .gitleaks.toml --no-banner --redact; \
	fi

test: test-py test-ts
test-py:
	@echo "==> gate: python tests and coverage"
	$(PYD) $(UV) pytest --cov
test-ts:
	@echo "==> gate: typescript tests and coverage"
	$(NPMD) test

mutate:
	@echo "==> gate: mutation score on python core"
	$(PYD) $(UV) python -m tools.mutation_gate

prove-gates:
	@echo "==> gate: proofs that each gate blocks a fault"
	$(PYD) $(UV) pytest proofs -p no:cacheprovider --no-cov

demo:  ## Run both example packages.
	$(PYD) $(UV) python -m qtemplate
	cd ts && npx --no-install tsc -p tsconfig.demo.json
	node ts/dist/main.js

eval-smoke:  ## Deterministic, free smoke eval. Other repos inherit this target.
	$(PYD) $(UV) python -m evals.smoke

update-gates:  ## Pull the newest gate files from the template into this repo.
	scripts/adopt.sh --update
