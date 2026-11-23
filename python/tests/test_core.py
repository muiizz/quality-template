import pytest
from hypothesis import given
from hypothesis import strategies as st

from qtemplate.core import SpendCapError, check_spend, normalise


def test_normalise_collapses_whitespace_and_case() -> None:
    assert normalise("  Hello   WORLD \n") == "hello world"


def test_normalise_empty() -> None:
    assert normalise("") == ""


@given(st.text())
def test_normalise_is_idempotent(text: str) -> None:
    assert normalise(normalise(text)) == normalise(text)


def test_spend_below_cap() -> None:
    assert check_spend(0.10, 0.05, 0.50) == pytest.approx(0.15)


def test_spend_exactly_at_cap_is_allowed() -> None:
    assert check_spend(0.25, 0.25, 0.50) == pytest.approx(0.50)


def test_spend_above_cap_is_refused() -> None:
    with pytest.raises(SpendCapError, match=r"^spend 0\.51 would pass cap 0\.50$"):
        check_spend(0.25, 0.26, 0.50)


def test_zero_amounts_are_allowed() -> None:
    assert check_spend(0.0, 0.0, 0.0) == 0.0


@pytest.mark.parametrize("args", [(-1.0, 0.0, 1.0), (0.0, -1.0, 1.0), (0.0, 0.0, -1.0)])
def test_negative_amounts_are_refused(args: tuple[float, float, float]) -> None:
    with pytest.raises(ValueError, match=r"^amounts must not be negative$"):
        check_spend(*args)


@given(st.integers(0, 1_000_000), st.integers(0, 1_000_000))
def test_spend_cap_boundary(spent: int, next_cost: int) -> None:
    # These integral dollar amounts are exactly representable as floats.
    total = spent + next_cost
    assert check_spend(spent, next_cost, total) == total
    if total > 0:
        with pytest.raises(SpendCapError):
            check_spend(spent, next_cost, total - 1)
