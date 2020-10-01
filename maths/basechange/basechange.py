
"""
Module docstring
"""
from collections import deque

import pytest


def change_to_radix(n, radix, nbase=10):
    """
    Change from base ``nbase`` to base ``radix``

    Args:
      n (int): number in base 10 to convert
      radix (int): radix to convert to
    Kwargs:
      nbase (int): base of n
    Returns:
      str: $$ n_{radix} $$
    """
    _n = n
    digits = deque()
    while n > 0:
        n, remainder = divmod(n, radix)
        digits.appendleft(str(remainder))  # TODO: what if this is greater than one digit?
    return ''.join(digits)


change_to_radix_test_cases = [
  (16, 2, '10000'),
  (17, 2, '10001'),
  (16, 8, '20'),
  (17, 16, '11'),
]

@pytest.mark.parametrize("n, radix, expected",
  change_to_radix_test_cases)
def test_change_to_radix(n, radix, expected):
    output = change_to_radix(n, radix)
    # print((output, expected))
    assert output == expected
