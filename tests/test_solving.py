import sys

from computorV1 import LOG, solve

sys.path.append("..")


def test_solving():
    result = solve("x3 - 3x - 10 = 0")
    assert not result
    assert (
        LOG.error == "The polynomial degree is strictly greater than 2, I can't solve."
    )

    LOG.error = ""

    assert solve("x2 = 0") == [0]
    assert solve("2 * x^2 - 4 * x - 6 = 0") == [3, -1]
    assert solve("x - x = 4") == []
    assert solve("x + x = 4") == [2]
    assert solve("x2 = 4") == [2, -2]
    assert solve("2x - x = x") == ["any"]
    assert solve("x2 + 5 = 0") == []

    # complex numbers
    assert solve("x2 - 6x + 34 = 0") == [complex(3, 5), complex(3, -5)]
    # the same as previous one
    assert solve("x2 - 6x + 34 = 0") == [3 + 5j, 3 - 5j]

    assert not LOG.error

    assert solve("2x2 = -4 + x2 + x^2") == []


def test_task_examples():
    assert solve("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0") == [-0.475131, 0.905239]
    assert solve("5 * X^0 + 4 * X^1 = 4 * X^0") == [-0.25]
    assert solve("5 + 4 * X + X^2= X^2") == [-1.25]
