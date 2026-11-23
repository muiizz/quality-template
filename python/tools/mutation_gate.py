"""Run mutmut on the core module and fail if the score is under the bar.

The bar comes from MUTATION_MIN_SCORE (default 0.95). The score is killed / total.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

STATS = Path("mutants/mutmut-cicd-stats.json")


def run(args: list[str]) -> None:
    subprocess.run([sys.executable, "-m", "mutmut", *args], check=True)  # noqa: S603


def main() -> int:
    # Cached results can hide a regression, so always start clean.
    shutil.rmtree("mutants", ignore_errors=True)
    run(["run"])
    run(["export-cicd-stats"])
    stats = json.loads(STATS.read_text())
    total = stats["total"]
    if total == 0:
        print("mutation gate: no mutants were generated", file=sys.stderr)
        return 1
    score = stats["killed"] / total
    bar = float(os.environ.get("MUTATION_MIN_SCORE", "0.95"))
    print(f"mutation gate: killed {stats['killed']} of {total} (score {score:.2f}, bar {bar:.2f})")
    return 0 if score >= bar else 1


if __name__ == "__main__":
    sys.exit(main())
