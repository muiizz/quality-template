"""`python -m qtemplate` prints a small, deterministic demo."""

from qtemplate.core import check_spend, normalise


def main() -> None:
    print(normalise("  Hello   WORLD  "))
    print(f"total spend: {check_spend(0.10, 0.05, 0.50):.2f}")


if __name__ == "__main__":  # pragma: no cover
    main()
