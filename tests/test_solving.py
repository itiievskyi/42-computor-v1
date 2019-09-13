import sys

from computorV1 import LOG, solve

sys.path.append("..")


def test_solving():
    result = solve("x3 - 3x - 10 = 0")
    assert not result
    assert LOG.error == "The polynomial degree is strictly greater than 2, I can't solve."

    LOG.error = ""

    assert solve("x2 = 0") == [0]
    assert solve("2 * x^2 - 4 * x - 6 = 0") == [3, -1]
    assert solve("x - x = 4") == []
    assert solve("x + x = 4") == [2]
    assert solve("x2 = 4") == [2, -2]
    assert solve("2x - x = x") == ['any']
    assert solve("x2 + 5 = 0") == []

    # complex numbers
    assert solve("x2 - 6x + 34 = 0") == [complex(3, 5), complex(3, -5)]
    # the same as previous one
    assert solve("x2 - 6x + 34 = 0") == [3+5j, 3-5j]

    assert not LOG.error
