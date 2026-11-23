# Gates: why each one exists

Local pre-push and required CI both call `make check`. The nightly mutation workflow calls `make mutate` and `make prove-mutation`. Each gate has a fault proof in `python/proofs/test_gates.py`.

| Gate | Tool (pinned) | The mistake it stops | Proof case |
|---|---|---|---|
| Secret scan | gitleaks 8.30.1 | A key or token in the index, working tree, or Git history. | `fake-secret` |
| Python lint | ruff 0.17.6 | Unused imports, likely bugs, unsafe calls. | `python-lint-error` |
| Python format | ruff format | Style arguments in review. | `python-format-error` |
| Python types | mypy 2.4.1, strict | Wrong types that tests do not reach. | `python-type-error` |
| TypeScript lint | eslint 10.15.0 | `var`, loose equality, unused code, and unsafe assignments from `any`. | `typescript-lint-error`, `typescript-type-aware-lint-error` |
| TypeScript format | prettier 3.10.1 | Style arguments in review. | `typescript-format-error` |
| TypeScript types | tsc 6.0.3, strict, `--noEmit` | Type errors in code that is never run by a test. | `typescript-type-error` |
| SQL lint | sqlfluff 4.5.0 | Inconsistent or unsafe SQL style. | `sql-lint-error` |
| File hygiene | pre-commit-hooks 6.0.0 | Missing final newline, trailing spaces, large files. | `trailing-whitespace` |
| Tests | pytest 9.2.0, vitest 5.1.1 | Behaviour changes nobody meant. | `python-failing-test`, `typescript-failing-test` |
| Coverage 90% | pytest-cov, vitest v8 | New code that no test runs. | `python-coverage-below-threshold`, `typescript-coverage-below-threshold` |
| Mutation score 0.95 | mutmut 3.8.1 (Python core only) | Tests that run code but check nothing. | `weak-tests-low-mutation-score` |
| Gate proofs | pytest | A gate that silently stopped working. | the proofs are the proof |
| Dependency updates | Dependabot | Old, vulnerable dependencies. | not tested here |
| Static analysis | CodeQL | Security bugs a linter does not see. | not tested here |

## Rules for changing a gate

- Never lower a threshold or skip a check to make a run pass. Fix the code or the test.
- A change to a gate needs its proof case changed in the same commit.
- Coverage shows which code ran. The mutation score shows whether the tests would notice a change.
  You need both.

## `make eval-smoke`

A free, deterministic check that other repos keep and fill with their own cases. It spends no money.
Any repo that adds a paid model call must read `MAX_USD_PER_RUN` and a monthly cap, and stop before the cap.
