# quality-template

[![check](https://github.com/muiizz/quality-template/actions/workflows/check.yml/badge.svg)](https://github.com/muiizz/quality-template/actions/workflows/check.yml)

Shared local and CI quality gates for my portfolio repos. One `make check` runs the same gates on a laptop and in CI.

## What it gives you

- Python: ruff, ruff format, mypy strict, pytest with a 90% coverage bar, hypothesis, mutation testing with mutmut.
- TypeScript: eslint, prettier, `tsc --noEmit`, vitest with a 90% coverage bar.
- SQL: sqlfluff. Secrets: gitleaks. File hygiene: end-of-file, trailing whitespace, large files.
- CI (`.github/workflows/check.yml`) installs from lockfiles, then calls `make check`. Nothing else.
- Proofs: each gate is shown to block a fault by a test (`python/proofs/test_gates.py`). See `GATES.md`.

## Run it

```bash
make setup        # installs from lockfiles (needs uv, Node 24, git, curl)
make check        # every gate, then the gate proofs (about 3 minutes)
make demo         # runs both example packages
make eval-smoke   # free, deterministic smoke eval that other repos inherit
```

`make check` runs `check-core` (hooks, tests, mutation) and then `prove-gates`.

## Adopt it in another repo

From the root of the other repo:

```bash
curl -fsSL https://raw.githubusercontent.com/muiizz/quality-template/<sha>/scripts/adopt.sh | bash -s -- <sha>
```

It copies the gate files, refuses to overwrite existing ones without `--force`, and records the source commit in
`.quality-template-version`. Then edit the paths in `Makefile` for your layout. Why a copy script: ADR 0002.

## Results

Run on 23 Nov 2026 (UTC) with `make check`. Machine: AMD Ryzen 5 7535HS, 11 GB RAM, WSL2 (kernel 6.18.58.1), Python 3.12.16, Node 24.22.1.
Commit SHA: `a4e1c8a` (clean tree, exit code 0, 2 min 25 s wall time on this rerun).
No model is called, so model and spend do not apply.

| Measure | Result | Command |
|---|---|---|
| Whole `make check` | 2 min 20 s and 2 min 25 s (two runs) | `make check` |
| Python tests and branch coverage | 11 passed, 100% (bar 90%) | `make test-py` |
| TypeScript tests and coverage | 7 passed, 100% (bar 90%) | `make test-ts` |
| Mutation score, Python core | 40 killed of 40 (bar 0.95) | `make mutate` |
| Gate proofs | 17 passed (14 injected faults, 1 clean control, 2 adoption tests) | `make prove-gates` |

Branch protection proof, 23 Nov 2026: `main` requires the `check` status check, an up-to-date branch, applies to admins, and blocks force pushes and deletion (`docs/branch-protection.json`). A throwaway PR with a type error ([PR 4](https://github.com/muiizz/quality-template/pull/4), closed, not merged) failed `check` at the mypy strict hook, and `gh pr merge` was refused with "the base branch policy prohibits the merge". A direct push to `main` was rejected with "Required status check \"check\" is expected". The setting was applied with `gh api -X PUT repos/muiizz/quality-template/branches/main/protection --input docs/branch-protection.json`.

Fresh clone check, 23 Nov 2026: a new `git clone` of commit `bb3457c` into an empty folder on the same machine passed `make setup && make check` (2 min 58 s, exit 0). It reused the machine's uv and npm caches, so it is not a clean machine. GitHub Actions run for the same tree: `check` passed in 2 min 4 s ([PR 5](https://github.com/muiizz/quality-template/pull/5)).

What failed on the way: the first mutation run killed 35 of 40 mutants. The five survivors were a `<` that could become `<=` on zero amounts and two error messages nobody checked. I added tests for zero amounts and exact messages, and the score went to 40 of 40. Then the "weak tests" proof first passed wrongly: the weakened tests scored exactly 0.90 against a 0.90 bar. I raised the bar to 0.95 so that proof now blocks.

## Docs

`GATES.md` (why each gate exists), `docs/adr/` (decisions), `INTERVIEW.md` (hard questions), `SECURITY.md`.

## What this does not show

- Branch protection is a GitHub setting, not a file in the repo. `docs/branch-protection.json` records what I applied, but nothing in the repo stops someone turning it off. It requires no reviews because this is a solo repo, so it does not show a review process.
- The proofs inject one fault at a time into a copy of this repo. They do not test combinations of faults.
- The example packages are 20 lines each. The speed and the 100% numbers will not hold for a large codebase.
- Mutation testing covers the Python core only. TypeScript has none.
- The gitleaks installer works on Linux x86_64 only. The gates ran on one local machine (above) and on GitHub-hosted Ubuntu runners. I have not tried macOS, Windows or arm64.
- No paid model is called here, so the spend cap rule is stated but not exercised.

## What I would do next

- Turn on branch protection and require the `check` job.
- Add a drift check that compares an adopting repo with the template commit it records.
- Add Stryker mutation testing for the TypeScript core.
- Cache the proof runs so `make check` is faster on a large repo.
- Support macOS and arm64 in the gitleaks installer.
