"""Proof that each gate blocks the fault it exists for.

Each test copies this repo to a temp folder, injects exactly one fault, and runs the same
command CI runs for the gates (`make check-core`). It then asserts the run failed and that the
expected gate is the one that reported it. A clean copy must pass, so a broken harness cannot
make the proofs pass by accident.

The fake secret is built from pieces at run time, so this file never holds a secret-shaped string.
"""

import hashlib
import os
import re
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SKIP_COPY = {
    ".git",
    ".venv",
    "node_modules",
    ".tools",
    "mutants",
    "coverage",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    ".hypothesis",
}


def fake_secret() -> str:
    """A GitHub-token-shaped string that is not a real credential."""
    digest = hashlib.sha256(b"quality-template-fake").digest()
    body = "".join(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"[b % 62] for b in digest
    )
    return "ghp" + "_" + body[:36]


def append(rel: str, text: str) -> Callable[[Path], None]:
    def fault(root: Path) -> None:
        path = root / rel
        path.write_text(path.read_text() + text)

    return fault


def replace(rel: str, old: str, new: str, *, regex: bool = False) -> Callable[[Path], None]:
    def fault(root: Path) -> None:
        path = root / rel
        before = path.read_text()
        after = re.sub(old, new, before, flags=re.S) if regex else before.replace(old, new)
        assert after != before, f"fault did not change {rel}"
        path.write_text(after)

    return fault


def several(*faults: Callable[[Path], None]) -> Callable[[Path], None]:
    def fault(root: Path) -> None:
        for one in faults:
            one(root)

    return fault


def write_new(rel: str, text: str) -> Callable[[Path], None]:
    def fault(root: Path) -> None:
        (root / rel).write_text(text)

    return fault


UNTESTED_PY = """

def untested(x: int) -> int:
    if x > 10:
        return x * 2
    if x > 5:
        return x * 3
    if x > 2:
        return x * 4
    total = 0
    for i in range(x):
        total += i
    return total + 1
"""

UNTESTED_TS = """
export function untested(x: number): number {
  if (x > 10) {
    return x * 2;
  }
  if (x > 5) {
    return x * 3;
  }
  let total = 0;
  for (let i = 0; i < x; i += 1) {
    total += i;
  }
  return total + 1;
}
"""


@dataclass(frozen=True)
class Case:
    name: str
    fault: Callable[[Path], None]
    # Regexes that must all match the combined output (multi-line mode).
    expect: tuple[str, ...]


CASES = [
    Case(
        "fake-secret",
        write_new("notes.txt", f"token = {fake_secret()}\n"),
        (r"^gitleaks\.+Failed",),
    ),
    Case(
        "python-type-error",
        append("python/qtemplate/core.py", '\nBAD: int = "text"\n'),
        (r"^mypy strict\.+Failed",),
    ),
    Case(
        "python-lint-error",
        append("python/qtemplate/core.py", "\nimport os\n"),
        (r"^ruff lint\.+Failed",),
    ),
    Case(
        "python-format-error",
        append("python/qtemplate/core.py", "\nX = [1,2,3]\n"),
        (r"^ruff format\.+Failed",),
    ),
    Case(
        "typescript-type-error",
        append("ts/src/core.ts", '\nexport const bad: number = "text";\n'),
        (r"^tsc no emit\.+Failed",),
    ),
    Case(
        "typescript-lint-error",
        append("ts/src/core.ts", "\nexport var legacy = 1;\n"),
        (r"^eslint\.+Failed",),
    ),
    Case(
        "typescript-format-error",
        append("ts/src/core.ts", "\nexport const  x  =  1;\n"),
        (r"^prettier\.+Failed",),
    ),
    Case(
        "sql-lint-error",
        append("sql/example.sql", "select * from run_records\n"),
        (r"^sqlfluff\.+Failed",),
    ),
    Case(
        "trailing-whitespace",
        append("README.md", "text with trailing space \n"),
        (r"^trim trailing whitespace\.+Failed",),
    ),
    Case(
        "python-failing-test",
        replace("python/tests/test_core.py", '== "hello world"', '== "wrong"'),
        (r"gate: python tests and coverage", r"1 failed"),
    ),
    Case(
        "python-coverage-below-threshold",
        append("python/qtemplate/core.py", UNTESTED_PY),
        (r"gate: python tests and coverage", r"Required test coverage of 90\.0% not reached"),
    ),
    Case(
        "typescript-failing-test",
        replace("ts/tests/core.test.ts", 'toBe("hello world")', 'toBe("wrong")'),
        (r"gate: typescript tests and coverage", r"1 failed"),
    ),
    Case(
        "typescript-coverage-below-threshold",
        append("ts/src/core.ts", UNTESTED_TS),
        (r"gate: typescript tests and coverage", r"does not meet global threshold"),
    ),
    Case(
        "weak-tests-low-mutation-score",
        several(
            replace(
                "python/tests/test_core.py", r'match=r"\^spend[^"]*"', 'match="spend"', regex=True
            ),
            replace(
                "python/tests/test_core.py",
                r'match=r"\^amounts[^"]*"',
                'match="negative"',
                regex=True,
            ),
            replace(
                "python/tests/test_core.py",
                r"def test_zero_amounts_are_allowed.*?\n\n\n",
                "",
                regex=True,
            ),
        ),
        (r"gate: mutation score", r"mutation gate: killed \d+ of \d+"),
    ),
]


@pytest.fixture(scope="module")
def tool_env() -> dict[str, str]:
    env = dict(os.environ)
    env.pop("VIRTUAL_ENV", None)
    env["UV_PROJECT_ENVIRONMENT"] = str(REPO / "python" / ".venv")
    return env


def make_copy(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(REPO, root, ignore=lambda _dir, names: [n for n in names if n in SKIP_COPY])
    (root / "ts" / "node_modules").symlink_to(REPO / "ts" / "node_modules")
    (root / ".tools").symlink_to(REPO / ".tools")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    return root


def run_gates(root: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    return subprocess.run(
        ["make", "check-core"],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_clean_copy_passes(tmp_path: Path, tool_env: dict[str, str]) -> None:
    root = make_copy(tmp_path)
    result = run_gates(root, tool_env)
    assert result.returncode == 0, result.stdout[-3000:] + result.stderr[-3000:]


@pytest.mark.parametrize("case", CASES, ids=[c.name for c in CASES])
def test_fault_is_blocked(case: Case, tmp_path: Path, tool_env: dict[str, str]) -> None:
    root = make_copy(tmp_path)
    case.fault(root)
    result = run_gates(root, tool_env)
    output = result.stdout + result.stderr
    assert result.returncode != 0, f"{case.name} was NOT blocked"
    for pattern in case.expect:
        assert re.search(pattern, output, flags=re.M), (
            f"{case.name}: expected /{pattern}/ in output:\n{output[-3000:]}"
        )
