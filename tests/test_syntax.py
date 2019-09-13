import sys

from computorV1 import LOG, get_coeffs

sys.path.append("..")


def test_equals_and_vars():
    result = get_coeffs("")
    assert not result
    assert LOG.error == "Syntax error! No variables detected."

    result = get_coeffs("52 - 12 = 0")
    assert not result
    assert LOG.error == "Syntax error! No variables detected."

    result = get_coeffs("x2 + 0")
    assert not result
    assert LOG.error == "Syntax error! Unexpected number of '='."

    result = get_coeffs("x2 + 0 = 45 + 3x - 4x^2 = 9")
    assert not result
    assert LOG.error == "Syntax error! Unexpected number of '='."

    result = get_coeffs("x2 + 0 =")
    assert not result
    assert LOG.error == "Syntax error near '='."

    result = get_coeffs(" = x2 + 0")
    assert not result
    assert LOG.error == "Syntax error near '='."

    result = get_coeffs("4 = * x2 + 10")
    assert not result
    assert LOG.error == "Syntax error near '='."

    result = get_coeffs("x = ")
    assert not result
    assert LOG.error == "Syntax error near '='."

    result = get_coeffs(" = x")
    assert not result
    assert LOG.error == "Syntax error near '='."


def test_syntax_errors():
    result = get_coeffs(" - x - = 435")
    assert not result
    assert LOG.error == "Syntax error! Unexpected value: '-'"

    result = get_coeffs("3x = 435 + ")
    assert not result
    assert LOG.error == "Syntax error! Unexpected value: '+'"

    result = get_coeffs("3x = 435y")
    assert not result
    assert LOG.error == "Syntax error! Unexpected value: 'y'"

    result = get_coeffs("3x = 435 - 345x2 + 4/6 + y")
    assert not result
    assert LOG.error == "Syntax error! Unexpected value: '/'"

    result = get_coeffs("3*x**2 = 435 - 345*x^^2 ")
    assert not result
    assert LOG.error == "Syntax error! Unexpected value: '^'"

    result = get_coeffs("xx2 = 9")
    assert not result
    assert LOG.error == "Syntax error! Unexpected value: 'x'"

    result = get_coeffs("x*x2 = 9")
    assert not result
    assert LOG.error == "Syntax error! Unexpected value: '*'"

    result = get_coeffs("x2.1 = 9 - 1")
    assert not result
    assert LOG.error == "Syntax error! Unexpected value: '.'"

    result = get_coeffs("2.1x2 = 9. - 1")
    assert not result
    assert LOG.error == "Syntax error! Unexpected value: '.'"
