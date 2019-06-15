import re
import sys
from typing import List


def print_reduced_form(coeffs: List):
    reduced = ""
    for coeff in coeffs:
        sign = " + " if coeff[1] > 0 else " - "
        number = abs(coeff[1])
        if coeffs.index(coeff) == 0:
            sign = ""
            number = coeff[1]
        var = " * X" if coeff[0] else ""
        power = f"^{coeff[0]}" if coeff[0] > 1 else ""
        reduced += f"{sign}{number}{var}{power}"
    reduced += " = 0"
    print(reduced)


def get_number(line: str):
    if not line:
        return 1
    else:
        return int(line)


def get_coeffs(code: str) -> List:
    right_side = False
    coeffs = {}

    token_specification = [
        (
            "EXPR",
            r"(?P<sign>^|\-|\+|\=){1}((?P<number>\-?[0-9]+(?P<float>\.[0-9]+)?)?((?P<var>\*?x){1}((\^|\*\*)?(?P<power>[0-9]+)?))?){1}",
        ),
        ("MISMATCH", r"."),  # Any other character
    ]
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "EXPR":
            if mo.group("sign") == "=":
                right_side = True

            number = get_number(mo.group("number"))
            if number:
                sign_multiplicator = (mo.group("sign") == "-") + right_side
                power = 0
                if mo.group("var"):
                    power = 1 if not mo.group("power") else int(mo.group("power"))

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
    print_reduced_form(coeffs)


if __name__ == "__main__":
    """Entry point"""
    if len(sys.argv) != 2:
        quit("You should provide exactly 1 argument!")

    solve(sys.argv[1].lower().replace(" ", ""))
