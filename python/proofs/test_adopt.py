"""The adoption script copies the gate files, and never overwrites without --force."""

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "adopt.sh"


def git(*args: str, cwd: Path) -> str:
    done = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return done.stdout.strip()


def make_source(tmp_path: Path) -> tuple[Path, str]:
    src = tmp_path / "source"
    src.mkdir()
    git("init", "-q", cwd=src)
    for rel in subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard"],
        cwd=REPO,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.split():
        target = src / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if (REPO / rel).is_file():
            target.write_bytes((REPO / rel).read_bytes())
    git("add", "-A", cwd=src)
    git("commit", "-q", "-m", "fixture", cwd=src)
    return src, git("rev-parse", "HEAD", cwd=src)


def run(target: Path, source: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(SCRIPT), *args],
        cwd=target,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin", "QT_SOURCE": str(source), "HOME": str(target)},
        capture_output=True,
        text=True,
        check=False,
    )


def test_adopt_copies_then_refuses_then_forces(tmp_path: Path) -> None:
    source, sha = make_source(tmp_path)
    target = tmp_path / "other-repo"
    target.mkdir()

    first = run(target, source, sha)
    assert first.returncode == 0, first.stderr
    assert (target / "Makefile").is_file()
    assert (target / ".github" / "workflows" / "check.yml").is_file()
    assert (target / ".quality-template-version").read_text().strip() == sha

    (target / "Makefile").write_text("mine\n")
    second = run(target, source, sha)
    assert second.returncode == 1
    assert (target / "Makefile").read_text() == "mine\n"

    third = run(target, source, sha, "--force")
    assert third.returncode == 0
    assert (target / "Makefile").read_text() != "mine\n"


def test_adopt_needs_a_ref(tmp_path: Path) -> None:
    result = run(tmp_path, tmp_path)
    assert result.returncode == 2
