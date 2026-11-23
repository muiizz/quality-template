# ADR 0001: One `make check` for local and CI

Status: accepted, 23 Nov 2026

## Context
Local checks and CI checks drift when they are written twice. A green laptop and a red CI
(or the reverse) wastes time and hides real problems.

## Decision
- The `Makefile` is the only place a gate is defined.
- The CI workflow runs `make setup` (install from lockfiles) and then `make check`. It adds no check of its own.
- pre-commit hooks are thin: each local hook calls a `make` target. Tool versions live in `uv.lock` and
  `package-lock.json`, not in the hook config. Only the generic file hygiene hooks come from a pinned remote repo.
- `make check` is `check-core` (hooks, tests, mutation) plus `prove-gates`.
  `prove-gates` runs `check-core` against copies of the repo with one injected fault each.

## Consequences
- A contributor can run exactly what CI runs.
- CodeQL and Dependabot are separate workflows because they are GitHub services, not local gates.
- `--no-verify` can skip hooks locally. CI still runs `make check`, so the commit cannot merge green.
- TypeScript is pinned to 6.0.3, not the latest 7.0.2, because typescript-eslint 8.73.0 requires
  typescript below 6.1.0. Revisit when typescript-eslint supports 7.
- gitleaks is installed by `scripts/install-gitleaks.sh` for Linux x86_64 only, with a checksum check.
