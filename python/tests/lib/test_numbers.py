import pytest

from lib import numbers


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, True),
        (121, True),
        (12321, True),
        (123454321, True),
        (1234554321, True),
        (123, False),
        (123456, False),
    ],
)
def test_arithmetic_sum(n: int, expected: int) -> None:
    assert numbers.is_palindromic(n) == expected
