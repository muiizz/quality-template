# Local quality gate evidence

On 23 Nov 2026 UTC, a clean clone of commit
`722a5604d29521b567b36e006a2166729af9f3fb` on Linux x86-64 ran
CPython 3.12.14, Node 24.22.3, uv 0.13.9, and gitleaks 8.30.1. The clone
used the machine's dependency caches. The acceptance run used synthetic
fixtures and a disposable local bare Git repository.

| Check | Exit code | Result |
|---|---:|---|
| `make setup` | 0 | Installed locked dependencies and both hooks |
| `make check` | 0 | 12 Python tests and 7 TypeScript tests, both at 100% coverage. All 17 required fault, clean-control, and adoption proofs passed. |
| Commit containing a staged synthetic token | 1 | The staged gitleaks hook reported one leak |
| Commit introducing an incompatible TypeScript assignment | 0 | The staged checks passed |
| Push containing the incompatible assignment | 1 | Pre-push ran `make check` and failed at `tsc --noEmit` |
| Commit restoring the TypeScript source | 0 | The staged checks passed |

A second disposable clone at
`7d80898ea9e5e4ce9851dfbc4b30bd7e9cec57c4` repeated the TypeScript fault and
repaired the source. The repaired commit and push both returned 0. The
pre-push hook reported that the full quality gate passed.
