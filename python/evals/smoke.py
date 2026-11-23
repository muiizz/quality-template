"""Smoke eval: deterministic, no network, no paid model, costs USD 0.

Other repos keep this entry point and replace the cases and the system under test.
Set EVAL_MIN_PASS_RATE (default 1.0) to change the bar.
"""

import json
import os
import sys
from pathlib import Path

from qtemplate.core import normalise


def main() -> int:
    cases = json.loads((Path(__file__).parent / "cases.json").read_text())
    passed = sum(1 for case in cases if normalise(case["input"]) == case["expected"])
    rate = passed / len(cases)
    bar = float(os.environ.get("EVAL_MIN_PASS_RATE", "1.0"))
    print(f"eval-smoke: {passed}/{len(cases)} passed (rate {rate:.2f}, bar {bar:.2f})")
    return 0 if rate >= bar else 1


if __name__ == "__main__":
    sys.exit(main())
