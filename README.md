# quality-template

[![check](https://github.com/muiizz/quality-template/actions/workflows/check.yml/badge.svg)](https://github.com/muiizz/quality-template/actions/workflows/check.yml)

Shared local and CI quality gates for my portfolio repos. One `make check` runs the same gates on a laptop and in CI.

## What it gives you

- Python: ruff, ruff format, mypy strict, pytest with a 90% coverage bar, hypothesis, mutation testing with mutmut.
- TypeScript: type-aware eslint, prettier, `tsc --noEmit`, vitest with a 90% coverage bar.
- SQL: sqlfluff. Secrets: gitleaks. File hygiene: end-of-file, trailing whitespace, large files.
- CI (`.github/workflows/check.yml`) installs from lockfiles, then calls `make check`. Nothing else.
- Mutation: the nightly and manually dispatched workflow enforces the 95% mutation bar and publishes the score and raw counts.
- Proofs: each gate is shown to block a fault by a test (`python/proofs/test_gates.py`). See `GATES.md`.

## Run it

```bash
make setup        # installs from lockfiles (needs uv 0.13.9, Node 24.22.3, git, curl)
make check        # local and required CI gates, then their fault proofs
make mutate       # standalone mutation score
make prove-mutation  # prove that the mutation gate catches weak tests
make demo         # runs both example packages
make eval-smoke   # free, deterministic smoke eval that other repos inherit
```

`make check` runs the full lint, type, secret, and test gates, then `prove-gates`. Setup installs two Git hooks. The pre-commit hook scans staged changes for secrets and checks staged Python, whitespace, and file size. The pre-push hook runs `make check`, the same target used by pull-request CI.

### Gitleaks on macOS and Windows

Linux x86-64 setup downloads and verifies gitleaks automatically. On macOS, download the Darwin archive for your architecture from the [gitleaks 8.30.1 release](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1), compare `shasum -a 256` against the published checksums, and place the unpacked executable at `.tools/gitleaks`. Verify with `.tools/gitleaks version`, then run `make setup`.

On Windows, use WSL2 and follow the Linux instructions. For a native installation, download the Windows ZIP for your architecture from the same release, compare `Get-FileHash -Algorithm SHA256` against the published checksums, and run `gitleaks.exe version` after extracting it. The template's Make and hook commands use Bash.

## Adopt it in another repo

From the root of the other repo:

```bash
curl -fsSL https://raw.githubusercontent.com/muiizz/quality-template/<sha>/scripts/adopt.sh | bash -s -- <sha>
```

It copies the gate files, refuses to overwrite existing ones without `--force`, and records the source commit in
`.quality-template-version`. Then edit the paths in `Makefile` for your layout. Why a copy script: ADR 0002.

## Results

Run on 23 Nov 2026 (UTC) with `make check`. Machine: AMD Ryzen 5 7535HS, 11 GB RAM, WSL2 (kernel 6.18.58.1), Python 3.12.16, Node 24.22.1.
Commit SHA: `8e47e04` (clean tree, exit code 0, 2 min 25 s wall time on this rerun). This repo was rewritten and then deleted and recreated on 23 Nov 2026 to remove a file that should not have been public. The SHAs here are from the rewritten history, which was pushed unchanged to the new repo, and PR numbers start again at 1; the run itself was on the original commit, which differs only by the removed brief file and two edited lines in CLAUDE.md.
No model is called, so model and spend do not apply.

| Measure | Result | Command |
|---|---|---|
| Whole `make check` | 2 min 20 s and 2 min 25 s (two runs) | `make check` |
| Python tests and branch coverage | 11 passed, 100% (bar 90%) | `make test-py` |
| TypeScript tests and coverage | 7 passed, 100% (bar 90%) | `make test-ts` |
| Mutation score, Python core | 40 killed of 40 (bar 0.95) | `make mutate` |
| Gate proofs | 17 passed (14 injected faults, 1 clean control, 2 adoption tests) | `make prove-gates` |

Branch protection proof, 23 Nov 2026 (repeated after the repo was recreated): `main` requires the `check` status check, an up-to-date branch, applies to admins, and blocks force pushes and deletion (`docs/branch-protection.json`). A throwaway PR with a type error ([PR 4](https://github.com/muiizz/quality-template/pull/4), closed, not merged), rebased on the current `main`, failed `check` at the mypy strict hook and GitHub reported `mergeStateStatus: BLOCKED`. I did not attempt the merge itself. A direct push to `main` was rejected with "Required status check \"check\" is expected". The setting was applied with `gh api -X PUT repos/muiizz/quality-template/branches/main/protection --input docs/branch-protection.json`.

Fresh clone check, 23 Nov 2026: a new `git clone` of commit `a16beb4` into an empty folder on the same machine passed `make setup && make check` (2 min 58 s, exit 0). It reused the machine's uv and npm caches, so it is not a clean machine. GitHub Actions on the recreated repo: `check` passed on `7482ff4` in about 2 min 7 s (created 15:59:48 UTC, finished 16:01:55 UTC, [run 45211432823](https://github.com/muiizz/quality-template/actions/runs/45211432823)).

What failed on the way: the first mutation run killed 35 of 40 mutants. The five survivors were a `<` that could become `<=` on zero amounts and two error messages nobody checked. I added tests for zero amounts and exact messages, and the score went to 40 of 40. Then the "weak tests" proof first passed wrongly: the weakened tests scored exactly 0.90 against a 0.90 bar. I raised the bar to 0.95 so that proof now blocks.

## Docs

`GATES.md` (why each gate exists), [local gate evidence](docs/evidence.md), [mutation evidence](docs/mutation.md), `docs/adr/` (decisions), `INTERVIEW.md` (hard questions), `SECURITY.md`.

## What this does not show

- Branch protection is a GitHub setting, not a file in the repo. `docs/branch-protection.json` records what I applied, but nothing in the repo stops someone turning it off. It requires no reviews because this is a solo repo, so it does not show a review process.
- The proofs inject one fault at a time into a copy of this repo. They do not test combinations of faults.
- The example packages are 20 lines each. The speed and the 100% numbers will not hold for a large codebase.
- Mutation testing covers the Python core only. TypeScript has none.
- The automated gitleaks installer targets Linux x86-64. The recorded gate runs cover WSL2 and GitHub-hosted Ubuntu.
- No paid model is called here, so the spend cap rule is stated but not exercised.

## What I would do next

- Add a drift check that compares an adopting repo with the template commit it records.
- Add Stryker mutation testing for the TypeScript core.
- Cache the proof runs so `make check` is faster on a large repo.
- Support macOS and arm64 in the gitleaks installer.
