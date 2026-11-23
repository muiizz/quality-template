# Python mutation evidence

Run started at 2026-11-23T16:34:38Z in a clean clone of commit
`6bb10b50aa765e5dbbe1832b8b2fb06fc964de62`. The host ran Linux x86-64 with
CPython 3.12.14, uv 0.13.9, and mutmut 3.8.1. The mutation target was
`python/qtemplate/core.py`.

| Command | Exit code | Result |
|---|---:|---|
| `uv sync --project python --frozen` | 0 | Installed the locked Python tools |
| `make mutate` | 0 | Killed all 40 mutants, above the 95% threshold |
| `make prove-mutation` | 0 | The proof confirmed that weakening the tests makes the mutation gate fail |

Mutmut reported zero survivors, timeouts, skipped mutants, and mutants without
tests. The nightly and manually dispatched GitHub workflow uploads the score log
and raw counters.
