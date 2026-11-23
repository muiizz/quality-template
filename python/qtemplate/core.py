"""Core module: the code the tests and mutation testing focus on."""

import unicodedata


class SpendCapError(Exception):
    """Raised when a spend would pass the cap."""


def normalise(text: str) -> str:
    """Fold case and compatibility forms, then collapse whitespace.

    Applying it twice gives the same result as applying it once.
    """
    folded = unicodedata.normalize("NFKD", text)
    folded = folded.casefold()
    folded = unicodedata.normalize("NFKD", folded)
    folded = folded.casefold()
    folded = unicodedata.normalize("NFKD", folded)
    return " ".join(folded.split())


def check_spend(spent_usd: float, next_cost_usd: float, cap_usd: float) -> float:
    """Return the new total, or raise before the cap is passed."""
    if spent_usd < 0 or next_cost_usd < 0 or cap_usd < 0:
        raise ValueError("amounts must not be negative")
    total = spent_usd + next_cost_usd
    if total > cap_usd:
        raise SpendCapError(f"spend {total:.2f} would pass cap {cap_usd:.2f}")
    return total
