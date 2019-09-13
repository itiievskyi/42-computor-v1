import sys

from computorV1 import LOG, REVERSE, get_coeffs, get_reduced_form

sys.path.append("..")


def test_coeffs():
    # {0: 0, 1: 0, 2: 0} => {a: 0, b: 0, c: 0}
    result = get_coeffs("x**2 = x^2")
    assert result == {0: 0, 1: 0, 2: 0}

    result = get_coeffs("x**2 = x^2")
    assert result == {0: 0, 1: 0, 2: 0}

    result = get_coeffs("2x**2 - 2x2 + 1x^2 + x2 = - 1 * x^2")
    assert result == {0: 0, 1: 0, 2: 3}

    result = get_coeffs("x2 = 1 - x")
    assert result == {0: -1, 1: 1, 2: 1}

    result = get_coeffs("x2 = 1 - x")
    assert result == {0: -1, 1: 1, 2: 1}

    result = get_coeffs("10*x^2=1*x^1+12*x^2-1*x^1-5*x^0")
    assert result == {0: 5, 1: 0, 2: -2}

    result = get_coeffs(
        "10 * x ^ 2 = 1 * x ^ 1 + 12 * x ^ 2 - 1 * x ^ 1 - 5 * x ^ 0")
    assert result == {0: 5, 1: 0, 2: -2}

    result = get_coeffs("45x = 4")
    assert result == {0: -4, 1: 45, 2: 0}

    result = get_coeffs("45x2 = 4")
    assert result == {0: -4, 1: 0, 2: 45}

    assert not LOG.error


def test_reduced_form():
    assert get_reduced_form(get_coeffs(
        "2x2 - 4x  + 0 = -4")) == "4 - 4 * X + 2 * X^2 = 0"
    assert get_reduced_form(get_coeffs(
        "x2 - 4x + 3 * x**2 + 0 = -4 + 0 - 34x -x2")) == "4 + 30 * X + 5 * X^2 = 0"
    assert get_reduced_form(get_coeffs(
        "2x2 - 4x  + 0 = -4")) == "4 - 4 * X + 2 * X^2 = 0"
    assert get_reduced_form(get_coeffs("2x2 = 2x2")) == "0 = 0"
    assert get_reduced_form(get_coeffs("2x2 = 3x2")) == "-X^2 = 0"
    assert get_reduced_form(get_coeffs("2x = 3x2")) == "2 * X - 3 * X^2 = 0"
    assert get_reduced_form(get_coeffs("2x = 2x - 5")) == "5 = 0"
    assert get_reduced_form(get_coeffs(" -5 - 2x = 2x - 5")) == "-4 * X = 0"
    assert get_reduced_form(get_coeffs(
        " -5 - 2x = -3 * x - 5")) == "X = 0"

    # test with dictionary passed (it's how script actually does)
    assert get_reduced_form({0: 0, 1: 2, 2: -3}) == "2 * X - 3 * X^2 = 0"

    assert not LOG.error
