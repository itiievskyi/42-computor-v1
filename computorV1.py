import re
import sys
from typing import List


def print_reduced_form(coeffs: List):
    reduced = ""
    for coeff in coeffs:
        sign = " + " if coeff[1] > 0 else " - "
        number = abs(coeff[1]) if abs(coeff[1]) > 1 or not coeff[0] else ""
        if coeffs.index(coeff) == 0:
            sign = "-" * bool(coeff[1] < 0)
        multiplicator = " * " if abs(coeff[1]) > 1 else ""
        var = "X" if coeff[0] else ""
        power = f"^{coeff[0]}" if coeff[0] > 1 else ""
        reduced += f"{sign}{number}{multiplicator}{var}{power}"
    reduced += " = 0"
    print(reduced)


def get_number(line: str):
    if not line:
        return 1
    elif "." in line:
        return float(line)
    else:
        return int(line)


def get_coeffs(code: str) -> List:
    right_side = False
    coeffs = {}

    token_specification = [
        (
            "EXPR_COEFF",
            r"(?P<sign0>^|\-|\+|\=){1}((?P<number0>\-?[0-9]+(?P<float0>\.[0-9]+)?){1}((?P<var0>\*?x){1}((\^|\*\*)?(?P<power0>[0-9]+))?)?){1}",
        ),
        (
            "EXPR_VAR",
            r"(?P<sign1>^|\-|\+|\=){1}((?P<number1>\-?[0-9]+(?P<float1>\.[0-9]+)?)?((?P<var1>\*?x){1}((\^|\*\*)?(?P<power1>[0-9]+))?){1}){1}",
        ),
        ("MISMATCH", r"."),  # Any other character
    ]
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        valid_tokens = ["EXPR_COEFF", "EXPR_VAR"]
        if kind in valid_tokens:
            if mo.group(f"sign{valid_tokens.index(kind)}") == "=":
                right_side = True

            number = get_number(mo.group(f"number{valid_tokens.index(kind)}"))
            if number:
                sign_multiplicator = (
                    mo.group(f"sign{valid_tokens.index(kind)}") == "-") + right_side
                power = 0
                if mo.group(f"var{valid_tokens.index(kind)}"):
                    power = 1 if not mo.group(
                        f"power{valid_tokens.index(kind)}") else int(mo.group(f"power{valid_tokens.index(kind)}"))

                if coeffs.get(power):
                    coeffs[power] += number * pow(-1, sign_multiplicator)
                else:
                    coeffs[power] = number * pow(-1, sign_multiplicator)

        elif kind == "MISMATCH":
            print(f"Unexpected value: {value!r}")
            return

    return sorted({k: v for k, v in coeffs.items() if v != 0}.items())


def solve(code: str):
    coeffs = get_coeffs(code)
    if not coeffs:
        print("Syntax Error!")
        return

    print_reduced_form(coeffs)

    degree = max(coeffs)[0]
    print(f"Polynomial degree: {degree}")
    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return


if __name__ == "__main__":
    """Entry point"""
    if len(sys.argv) != 2:
        quit("You should provide exactly 1 argument!")

    solve(sys.argv[1].lower().replace(" ", ""))
